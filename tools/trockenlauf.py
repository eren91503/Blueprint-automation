#!/usr/bin/env python3
"""Trockenlauf: prüft die ganze Kette ohne Credits mit künstlichen Stimmen-Blöcken.

usage: python3 tools/trockenlauf.py <kanal_ordner> <video_ordner>

Ablauf: Blöcke bauen -> künstliches Audio je Block (Töne mit Sprechpausen) -> Zeilen schneiden -> Video rendern.
Es werden nur Kopien in einem Temp-Ordner benutzt, im Repo bleibt nichts zurück.
Prüft, dass jede geschnittene Zeile etwa so lang ist wie die künstliche Vorlage (Toleranz 0,2 s).
"""
import array, json, math, os, re, shutil, subprocess, sys, tempfile, wave

TOOLS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLS)
import bloecke  # noqa: E402

SR = 44100
PAUSE = 0.45


def schreibe(pfad, teile):
    with wave.open(pfad, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        for typ, sek, freq in teile:
            n = int(SR * sek)
            if typ == "stille":
                w.writeframes(b"\x00\x00" * n)
            else:
                a = array.array("h", (int(9000 * math.sin(2 * math.pi * freq * i / SR)) for i in range(n)))
                w.writeframes(a.tobytes())


def dauer(f):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                       capture_output=True, text=True)
    return float(r.stdout.strip())


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    kanal, video = sys.argv[1:3]
    with tempfile.TemporaryDirectory() as tmp:
        v = os.path.join(tmp, "video")
        shutil.copytree(video, v, ignore=shutil.ignore_patterns("blocks", "vo", "out"))
        zeilen = json.load(open(os.path.join(v, "narration.json"), encoding="utf-8"))
        reihenfolge, gruppen = bloecke.gruppiere(zeilen)
        os.makedirs(os.path.join(v, "blocks"))
        erwartet = {}
        for szene in reihenfolge:
            teile, ende_block = [], False
            for zi, z in enumerate(gruppen[szene]):
                saetze = [s for s in re.split(r"(?<=[.?!:])\s*", z["say"]) if s]
                summe = 0.0
                for si, s in enumerate(saetze):
                    ton = max(0.6, len(s.split()) / 2.6)
                    teile.append(("ton", ton, 200 + 40 * (zi + 1)))
                    summe += ton
                    letzter = zi == len(gruppen[szene]) - 1 and si == len(saetze) - 1
                    if not letzter:
                        teile.append(("stille", PAUSE, 0))
                        if si < len(saetze) - 1:
                            summe += PAUSE
                erwartet[z["id"]] = summe
            schreibe(os.path.join(v, "blocks", f"{szene}.wav"), teile)
        out = os.path.join(tmp, "out", "trockenlauf.mp4")
        r = subprocess.run([sys.executable, os.path.join(TOOLS, "finish.py"), kanal, v, out],
                           capture_output=True, text=True)
        print(r.stdout.strip())
        if r.returncode != 0:
            sys.exit("FEHLER im Trockenlauf:\n" + (r.stderr or "")[-800:])
        fehler = []
        for k, soll in erwartet.items():
            ist = dauer(os.path.join(v, "vo", f"{k}_f.wav"))
            ok = abs(ist - soll) <= 0.2
            print(f"  {k}: {ist:.2f} s (Soll {soll:.2f} s) {'ok' if ok else 'ABWEICHUNG'}")
            if not ok:
                fehler.append(k)
        if not os.path.exists(out):
            sys.exit("FEHLER: kein Video entstanden")
        if fehler:
            sys.exit(f"TROCKENLAUF FEHLGESCHLAGEN: Zeilen {fehler}")
    print("TROCKENLAUF OK")


if __name__ == "__main__":
    main()
