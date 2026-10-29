#!/usr/bin/env python3
"""Teilt Stimmen-Blöcke (ein Audio je Szene) in einzelne Zeilen-WAVs.

usage: python3 tools/split_blocks.py <narration.json> <block_dir> <vo_dir>

block_dir enthält <szene>.mp3 oder <szene>.wav (eine Datei je Szene aus bloecke.py).
vo_dir bekommt <id>_f.wav je Zeile (44,1 kHz, mono, Stille an Anfang und Ende abgeschnitten).

Wie geschnitten wird (Erfahrung aus LERNEN.md): Das Pausen-Tag klingt nur etwa 0,4 s lang, genauso kurz
wie eine Satzpause. Darum wird je Satzzeichen (. ? ! :) eine Pause erwartet. Passt die Zahl der erkannten
Pausen dazu, schneidet das Skript an den Pausen hinter dem letzten Satzzeichen jeder Zeile. Sonst nimmt es die
längsten Pausen. Bleibt auch das falsch, legt man <block_dir>/cuts.json an, z. B. {"haupt": [4.6, 9.1]}
(Sekunden der Schnitte). Die Pausen findet man mit: ffmpeg -i X -af silencedetect=noise=-40dB:d=0.15 -f null -
"""
import json, os, re, subprocess, sys

WOERTER_PRO_SEKUNDE = 2.6


def dauer(f):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                       capture_output=True, text=True)
    return float(r.stdout.strip())


def stillen(src):
    out = subprocess.run(["ffmpeg", "-i", src, "-af", "silencedetect=noise=-40dB:d=0.15", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    s = [float(v) for v in re.findall(r"silence_start: ([\d.]+)", out)]
    e = [float(v) for v in re.findall(r"silence_end: ([\d.]+)", out)]
    return list(zip(s, e))


def finde_block(block_dir, szene):
    for endung in ("mp3", "wav"):
        p = os.path.join(block_dir, f"{szene}.{endung}")
        if os.path.exists(p):
            return p
    sys.exit(f"FEHLER: Kein Audio für Block '{szene}' in {block_dir} (erwartet {szene}.mp3 oder {szene}.wav)")


def schnitte(src, ids, say_von, manuell, szene):
    n = len(ids)
    if n == 1:
        return []
    if manuell and szene in manuell:
        cuts = manuell[szene]
        if len(cuts) != n - 1:
            sys.exit(f"FEHLER: cuts.json für '{szene}' hat {len(cuts)} Schnitte, nötig sind {n - 1}")
        return cuts
    gesamt = dauer(src)
    sil = sorted([(e - s, s, e) for s, e in stillen(src) if s > 0.3 and e < gesamt - 0.2], key=lambda z: z[1])
    npun = [len(re.findall(r"[.?!:]", say_von[k])) for k in ids]
    if len(sil) == sum(npun) - 1:
        kum = [sum(npun[:i + 1]) for i in range(n - 1)]
        wahl = [sil[c - 1] for c in kum]
    elif len(sil) >= n - 1:
        wahl = sorted(sorted(sil, reverse=True)[:n - 1], key=lambda z: z[1])
        print(f"HINWEIS: Block '{szene}': {len(sil)} Pausen, erwartet {sum(npun) - 1}. Es werden die längsten genommen. "
              "Zeilenlängen prüfen oder cuts.json anlegen.")
    else:
        sys.exit(f"FEHLER: Block '{szene}': nur {len(sil)} Pausen für {n} Zeilen. Pausen mit silencedetect ansehen "
                 f"und {os.path.dirname(src)}/cuts.json anlegen.")
    return [(a + c) / 2 for _, a, c in wahl]


def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    nar, block_dir, vo = sys.argv[1:4]
    os.makedirs(vo, exist_ok=True)
    zeilen = json.load(open(nar, encoding="utf-8"))
    bloecke, say_von = {}, {z["id"]: z["say"] for z in zeilen}
    for z in zeilen:
        bloecke.setdefault(z["scene"], []).append(z["id"])
    cp = os.path.join(block_dir, "cuts.json")
    manuell = json.load(open(cp)) if os.path.exists(cp) else None
    zahl, warnungen = {}, []
    for szene, ids in bloecke.items():
        src = finde_block(block_dir, szene)
        cuts = schnitte(src, ids, say_von, manuell, szene)
        pts = [0.0] + cuts + [dauer(src)]
        for i, k in enumerate(ids):
            ziel = os.path.join(vo, f"{k}_f.wav")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{pts[i]:.3f}", "-to", f"{pts[i + 1]:.3f}", "-i", src,
                            "-af", "silenceremove=start_periods=1:start_threshold=-45dB,areverse,"
                                   "silenceremove=start_periods=1:start_threshold=-45dB,areverse",
                            "-ar", "44100", "-ac", "1", ziel], check=True)
            d, erwartet = dauer(ziel), max(1.0, len(say_von[k].split()) / WOERTER_PRO_SEKUNDE)
            if d > 2.2 * erwartet + 1.0 or d < 0.4 * erwartet:
                warnungen.append(f"Zeile {k}: {d:.1f} s, erwartet etwa {erwartet:.1f} s (Schnitt prüfen)")
        zahl[szene] = len(ids)
    for w in warnungen:
        print("WARNUNG:", w)
    print("OK", zahl)


if __name__ == "__main__":
    main()
