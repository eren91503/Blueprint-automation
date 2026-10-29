#!/usr/bin/env python3
"""Baut aus narration.json die Stimmen-Blöcke (ein Block je Szene).

usage: python3 tools/bloecke.py <narration.json> [<out_blocks.json>] [--pause-tag TAG]

Je Szene (Feld "scene", in der Reihenfolge des ersten Auftretens) entsteht ein Block:
die Sprechtexte der Zeilen, verbunden mit dem Pausen-Tag. Pro Block wird EIN Stimmen-Aufruf gemacht
(nicht pro Zeile), das spart Aufrufe und Credits (siehe LERNEN.md).

Jede Zeile soll mit . ? ! oder : enden. Der Zeilen-Schnitt (split_blocks.py) ordnet die Pausen
den Satzzeichen zu.
"""
import argparse, json, re, sys

PAUSE_TAG = '<break time="1.0s" />'


def gruppiere(zeilen):
    """Gibt (Reihenfolge, {szene: [zeilen]}) zurück."""
    reihenfolge, gruppen = [], {}
    for z in zeilen:
        for pflicht in ("id", "scene", "say"):
            if not z.get(pflicht):
                sys.exit(f"FEHLER: Zeile ohne Feld '{pflicht}': {z}")
        if z["scene"] not in gruppen:
            reihenfolge.append(z["scene"]); gruppen[z["scene"]] = []
        gruppen[z["scene"]].append(z)
    ids = [z["id"] for z in zeilen]
    if len(ids) != len(set(ids)):
        sys.exit("FEHLER: Zeilen-IDs sind nicht eindeutig")
    return reihenfolge, gruppen


def baue(zeilen, pause_tag=PAUSE_TAG):
    reihenfolge, gruppen = gruppiere(zeilen)
    bloecke, warnungen = {}, []
    for szene in reihenfolge:
        zs = gruppen[szene]
        for z in zs:
            if not re.search(r"[.?!:]\s*$", z["say"].strip()):
                warnungen.append(f"Zeile {z['id']} endet ohne . ? ! oder : (der Zeilen-Schnitt braucht das)")
        text = f" {pause_tag} ".join(z["say"].strip() for z in zs)
        bloecke[szene] = {"ids": [z["id"] for z in zs], "text": text,
                          "woerter": sum(len(z["say"].split()) for z in zs), "zeichen": len(text)}
    return reihenfolge, bloecke, warnungen


def main():
    p = argparse.ArgumentParser()
    p.add_argument("narration"); p.add_argument("out", nargs="?"); p.add_argument("--pause-tag", default=PAUSE_TAG)
    a = p.parse_args()
    zeilen = json.load(open(a.narration, encoding="utf-8"))
    reihenfolge, bloecke, warnungen = baue(zeilen, a.pause_tag)
    ausgabe = {"reihenfolge": reihenfolge, "bloecke": bloecke}
    if a.out:
        json.dump(ausgabe, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for w in warnungen:
        print("WARNUNG:", w)
    gesamt_w = sum(b["woerter"] for b in bloecke.values()); gesamt_z = sum(b["zeichen"] for b in bloecke.values())
    for s in reihenfolge:
        b = bloecke[s]
        print(f"{s}: {len(b['ids'])} Zeilen, {b['woerter']} Wörter, {b['zeichen']} Zeichen")
    print(f"BLOECKE {len(reihenfolge)} Aufrufe, {gesamt_w} Wörter, {gesamt_z} Zeichen (Richtwert für Credits), "
          f"ca. {gesamt_w / 2.6:.0f} s Sprechzeit")


if __name__ == "__main__":
    main()
