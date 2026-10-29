#!/usr/bin/env python3
"""Inhaltsmodul: Text-und-Bild-Erklärvideo (neutral, nicht auf einen Kanal zugeschnitten).

Aufruf:
  python3 render.py <narration.json> <vo_dir> <look.json> <out.mp4> [--bilder DIR] [--platzhalter] [--sheet PNG]

Eingabe
  narration.json  Liste von Zeilen: id, say (Sprechtext), sub (Untertitel, Text oder Liste von Häppchen),
                  optional karte (große Karte im Bild), bild (Dateiname im Ordner --bilder), scene (frei)
  vo_dir          je Zeile eine Datei <id>_f.wav (oder .mp3/.wav gleichen Namens) mit der Stimme
  look.json       Farben, Schrift, Untertitel-Position (siehe README)
  --platzhalter   Keine Stimme nötig: Stille mit geschätzter Länge (2,6 Wörter pro Sekunde). Für Tests ohne Credits.
  --sheet PNG     Schreibt nur eine Übersicht mit Schlüsselbildern (je Zeile eins), kein Video.

Ausgabe: MP4, H.264, AAC, Standard 1080x1920 bei 30 fps.
"""
import argparse, json, math, os, subprocess, sys, tempfile, wave

from PIL import Image, ImageDraw, ImageFont

SCHRIFT_KANDIDATEN = [
    "/usr/share/fonts/opentype/inter/Inter-Bold.otf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]
WOERTER_PRO_SEKUNDE = 2.6
SR = 44100


def fehler(msg):
    sys.exit("FEHLER: " + msg)


def hexfarbe(h, a=255):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


def schrift(pfad, groesse):
    for p in ([pfad] if pfad else []) + SCHRIFT_KANDIDATEN:
        if p and os.path.exists(p):
            return ImageFont.truetype(p, groesse)
    return ImageFont.load_default(groesse)


def umbrechen(text, font, maxbreite, draw):
    zeilen, aktuell = [], ""
    for wort in text.split():
        probe = (aktuell + " " + wort).strip()
        if draw.textlength(probe, font=font) > maxbreite and aktuell:
            zeilen.append(aktuell)
            aktuell = wort
        else:
            aktuell = probe
    if aktuell:
        zeilen.append(aktuell)
    return zeilen


def text_ebene(text, font, maxbreite, farbe, zeilenabstand=1.25):
    """Zentrierter, umbrochener Text als transparente Ebene."""
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    zeilen = umbrechen(text, font, maxbreite, tmp)
    hoehe_z = int(font.size * zeilenabstand)
    ebene = Image.new("RGBA", (maxbreite, max(1, hoehe_z * len(zeilen))), (0, 0, 0, 0))
    d = ImageDraw.Draw(ebene)
    for i, z in enumerate(zeilen):
        d.text((maxbreite // 2, i * hoehe_z + hoehe_z // 2), z, font=font, fill=farbe, anchor="mm")
    return ebene


def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def dauer_datei(pfad):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", pfad],
        capture_output=True, text=True)
    try:
        return float(out.stdout.strip())
    except ValueError:
        fehler(f"Dauer von {pfad} nicht lesbar")


def als_wav(quelle, ziel):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", quelle, "-ar", str(SR), "-ac", "1",
                    "-c:a", "pcm_s16le", ziel], check=True)


def finde_audio(vo_dir, zid):
    for name in (f"{zid}_f.wav", f"{zid}.wav", f"{zid}_f.mp3", f"{zid}.mp3"):
        p = os.path.join(vo_dir, name)
        if os.path.exists(p):
            return p
    return None


def schreibe_stille(pfad, sekunden):
    with wave.open(pfad, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(b"\x00\x00" * int(SR * sekunden))


def baue_audio(zeilen, vo_dir, platzhalter, pause, arbeitsordner):
    """Gibt (Liste der (start, ende) je Zeile, Pfad der Gesamt-Wav, Gesamtdauer) zurück."""
    wavs, zeiten, t = [], [], 0.0
    for z in zeilen:
        quelle = finde_audio(vo_dir, z["id"]) if vo_dir else None
        ziel = os.path.join(arbeitsordner, f"{z['id']}.wav")
        if quelle:
            als_wav(quelle, ziel)
        elif platzhalter:
            sek = max(1.0, len(z["say"].split()) / WOERTER_PRO_SEKUNDE)
            schreibe_stille(ziel, sek)
        else:
            fehler(f"Keine Audiodatei für Zeile {z['id']} in {vo_dir} (oder --platzhalter nutzen)")
        d = dauer_datei(ziel)
        zeiten.append((t, t + d))
        wavs.append(ziel)
        t += d + pause
    gesamt = t + 0.6
    pfad = os.path.join(arbeitsordner, "gesamt.wav")
    with wave.open(pfad, "wb") as out:
        out.setnchannels(1); out.setsampwidth(2); out.setframerate(SR)
        stille = b"\x00\x00" * int(SR * pause)
        for w in wavs:
            with wave.open(w, "rb") as r:
                out.writeframes(r.readframes(r.getnframes()))
            out.writeframes(stille)
        out.writeframes(b"\x00\x00" * int(SR * 0.6))
    return zeiten, pfad, gesamt


class Bildaufbau:
    def __init__(self, zeilen, zeiten, look, bilder_dir):
        self.zeilen, self.zeiten, self.look = zeilen, zeiten, look
        res = look.get("aufloesung", "1080x1920").split("x")
        self.W, self.H = int(res[0]), int(res[1])
        f = look["farben"]
        self.c = {k: hexfarbe(v) for k, v in f.items()}
        pfad = look.get("schrift")
        self.f_karte = schrift(pfad, look.get("karte_groesse", 78))
        self.f_sub = schrift(pfad, look.get("untertitel", {}).get("groesse", 54))
        self.f_kanal = schrift(pfad, 40)
        self.gesamt = zeiten[-1][1] + 0.6
        self.panel = (60, 300, self.W - 60, 1180)
        self.base = self._base()
        self.karten = self._karten(bilder_dir)
        self.subs = self._subs()

    def _base(self):
        im = Image.new("RGB", (self.W, self.H), self.c["hintergrund"][:3])
        d = ImageDraw.Draw(im)
        d.rounded_rectangle(self.panel, radius=36, fill=self.c["panel"][:3])
        name = self.look.get("kanalname", "")
        if name:
            d.text((self.W // 2, 150), name, font=self.f_kanal, fill=self.c["akzent"][:3], anchor="mm")
        return im

    def _karten(self, bilder_dir):
        """Je Zeile: (Ebene oder None, Startzeit). Die Karte bleibt sichtbar, bis eine neue kommt."""
        x0, y0, x1, y1 = self.panel
        pw, ph = x1 - x0, y1 - y0
        ergebnis, aktuell = [], None
        for i, z in enumerate(self.zeilen):
            if z.get("karte") or z.get("bild"):
                teile, hoehe = [], 0
                if z.get("bild"):
                    pfad = os.path.join(bilder_dir or ".", z["bild"])
                    if not os.path.exists(pfad):
                        fehler(f"Bild nicht gefunden: {pfad}")
                    b = Image.open(pfad).convert("RGBA")
                    maxb, maxh = pw - 80, 460
                    s = min(maxb / b.width, maxh / b.height)
                    b = b.resize((max(1, int(b.width * s)), max(1, int(b.height * s))))
                    teile.append(b); hoehe += b.height + 40
                if z.get("karte"):
                    t = text_ebene(z["karte"], self.f_karte, pw - 100, self.c["text"])
                    teile.append(t); hoehe += t.height
                ebene = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
                y = max(20, (ph - hoehe) // 2)
                for t in teile:
                    ebene.paste(t, ((pw - t.width) // 2, y), t)
                    y += t.height + 40
                aktuell = (ebene, self.zeiten[i][0])
            ergebnis.append(aktuell)
        return ergebnis

    def _subs(self):
        """Je Zeile eine Liste von (von, bis, Ebene) für die Untertitel-Häppchen."""
        u = self.look.get("untertitel", {})
        bg = hexfarbe(self.look["farben"].get("untertitel_bg", "#000000"), 215)
        fg = self.c.get("untertitel_text", self.c["text"])
        maxb = self.W - 200
        alle = []
        for i, z in enumerate(self.zeilen):
            teile = z.get("sub") or z["say"]
            if isinstance(teile, str):
                teile = [teile]
            start, ende = self.zeiten[i]
            gewicht = [max(1, len(t)) for t in teile]
            summe, t0, liste = sum(gewicht), start, []
            for t, g in zip(teile, gewicht):
                t1 = t0 + (ende - start) * g / summe
                txt = text_ebene(t, self.f_sub, maxb - 80, fg, 1.2)
                box = Image.new("RGBA", (txt.width + 80, txt.height + 50), (0, 0, 0, 0))
                ImageDraw.Draw(box).rounded_rectangle((0, 0, box.width - 1, box.height - 1), radius=24, fill=bg)
                box.paste(txt, (40, 25), txt)
                liste.append((t0, t1, box))
                t0 = t1
            alle.append(liste)
        return alle

    def bild(self, t, zeile):
        im = self.base.copy()
        d = ImageDraw.Draw(im)
        d.rectangle((0, 0, int(self.W * min(1.0, t / self.gesamt)), 10), fill=self.c["akzent"][:3])
        karte = self.karten[zeile]
        if karte:
            ebene, t_start = karte
            x0, y0 = self.panel[0], self.panel[1]
            f = ease((t - t_start) / 0.35)
            versatz = int((1 - f) * 40)
            if f < 1.0:
                a = ebene.getchannel("A").point(lambda p: int(p * f))
                e = ebene.copy(); e.putalpha(a)
            else:
                e = ebene
            im.paste(e, (x0, y0 + versatz), e)
        for von, bis, box in self.subs[zeile]:
            if von <= t < bis:
                pos = self.look.get("untertitel", {}).get("position", "unten")
                y = {"oben": 220, "mitte": 1240, "unten": 1290}.get(pos, 1290)
                im.paste(box, ((self.W - box.width) // 2, y), box)
                break
        return im


def zeile_bei(zeiten, t):
    for i, (a, b) in enumerate(zeiten):
        if t < b + 0.05:
            return i
    return len(zeiten) - 1


def uebersicht(aufbau, pfad):
    kachel = (270, 480)
    spalten = min(6, len(aufbau.zeilen))
    reihen = math.ceil(len(aufbau.zeilen) / spalten)
    blatt = Image.new("RGB", (spalten * kachel[0], reihen * kachel[1]), (0, 0, 0))
    for i, (a, b) in enumerate(aufbau.zeiten):
        im = aufbau.bild((a + b) / 2, i).resize(kachel)
        blatt.paste(im, ((i % spalten) * kachel[0], (i // spalten) * kachel[1]))
    blatt.save(pfad)
    print("UEBERSICHT", pfad)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("narration"); p.add_argument("vo_dir"); p.add_argument("look"); p.add_argument("out")
    p.add_argument("--bilder"); p.add_argument("--platzhalter", action="store_true"); p.add_argument("--sheet")
    a = p.parse_args()
    zeilen = json.load(open(a.narration, encoding="utf-8"))
    look = json.load(open(a.look, encoding="utf-8"))
    fps = int(look.get("fps", 30))
    pause = float(look.get("pause", 0.15))
    with tempfile.TemporaryDirectory() as tmp:
        zeiten, audio, gesamt = baue_audio(zeilen, a.vo_dir, a.platzhalter, pause, tmp)
        aufbau = Bildaufbau(zeilen, zeiten, look, a.bilder)
        if a.sheet:
            uebersicht(aufbau, a.sheet)
            return
        n = int(math.ceil(gesamt * fps))
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
               "-s", f"{aufbau.W}x{aufbau.H}", "-r", str(fps), "-i", "-", "-i", audio,
               "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p",
               "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", a.out]
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        for f in range(n):
            t = f / fps
            proc.stdin.write(aufbau.bild(t, zeile_bei(zeiten, t)).tobytes())
        proc.stdin.close()
        if proc.wait() != 0:
            fehler("ffmpeg ist fehlgeschlagen")
    print(f"VIDEODONE {a.out} ({gesamt:.1f} s)")


if __name__ == "__main__":
    main()
