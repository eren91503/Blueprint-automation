#!/usr/bin/env python3
"""Aus den Stimmen-Blöcken wird ein Video: Zeilen schneiden, Übersicht, Video, Längenprüfung.

usage: python3 tools/finish.py <kanal_ordner> <video_ordner> <out.mp4> [--platzhalter] [--nur-uebersicht]

kanal_ordner   projekte/<kanal> mit projekt.json (steuert Modul, Format und Look)
video_ordner   projekte/<kanal>/videos/<id> mit narration.json, blocks/<szene>.mp3, optional bilder/
--platzhalter  Keine Stimme: Stille mit geschätzter Länge (Test ohne Credits)
--nur-uebersicht  Nur die Übersicht mit Schlüsselbildern erzeugen (zum Prüfen vor dem vollen Rendern)

Ausgabe: SHEET <pfad>, VIDEODONE <pfad> (<Sekunden>), ggf. WARNUNG.
"""
import argparse, json, os, subprocess, sys, tempfile

TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOLS)
STANDARD_FARBEN = {"hintergrund": "#F4EFE6", "panel": "#FFFFFF", "text": "#1D1D1F", "akzent": "#2F6FED",
                   "untertitel_bg": "#1D1D1F", "untertitel_text": "#FFFFFF"}


def laufe(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.stdout.strip():
        print(r.stdout.strip())
    if r.returncode != 0:
        sys.exit(f"FEHLER in {os.path.basename(cmd[1])}:\n{(r.stderr or r.stdout).strip()[-800:]}")


def baue_look(projekt):
    lk = projekt.get("look", {})
    farben = {**STANDARD_FARBEN, **(lk.get("farben") or {})}
    if not lk.get("farben"):
        print("HINWEIS: Keine Farben in projekt.json, Standardfarben werden genutzt.")
    untertitel = {"position": "unten", "groesse": 54}
    if isinstance(lk.get("untertitel"), dict):
        untertitel.update(lk["untertitel"])
    return {"kanalname": projekt["kanal"]["name"], "aufloesung": projekt["format"]["aufloesung"],
            "fps": projekt["format"]["fps"], "pause": lk.get("pause", 0.15), "schrift": lk.get("schrift") or None,
            "karte_groesse": lk.get("karte_groesse", 78), "farben": farben, "untertitel": untertitel}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("kanal_ordner"); p.add_argument("video_ordner"); p.add_argument("out")
    p.add_argument("--platzhalter", action="store_true"); p.add_argument("--nur-uebersicht", action="store_true")
    a = p.parse_args()
    projekt = json.load(open(os.path.join(a.kanal_ordner, "projekt.json"), encoding="utf-8"))
    modul = (projekt.get("konzept") or {}).get("inhaltsmodul")
    if not modul:
        sys.exit("FEHLER: projekt.json hat kein konzept.inhaltsmodul")
    render = os.path.join(ROOT, "module", modul, "render.py")
    if not os.path.exists(render):
        sys.exit(f"FEHLER: Modul '{modul}' nicht gefunden ({render})")
    nar = os.path.join(a.video_ordner, "narration.json")
    if not os.path.exists(nar):
        sys.exit(f"FEHLER: {nar} fehlt")
    vo = os.path.join(a.video_ordner, "vo")
    if a.platzhalter:
        vo = ""
    else:
        laufe([sys.executable, os.path.join(TOOLS, "split_blocks.py"), nar, os.path.join(a.video_ordner, "blocks"), vo])
    bilder = os.path.join(a.video_ordner, "bilder")
    extra = (["--bilder", bilder] if os.path.isdir(bilder) else []) + (["--platzhalter"] if a.platzhalter else [])
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        lookpfad = os.path.join(tmp, "look.json")
        json.dump(baue_look(projekt), open(lookpfad, "w", encoding="utf-8"), ensure_ascii=False)
        sheet = os.path.join(os.path.dirname(os.path.abspath(a.out)), "uebersicht.png")
        laufe([sys.executable, render, nar, vo, lookpfad, a.out, "--sheet", sheet] + extra)
        print("SHEET", sheet)
        if a.nur_uebersicht:
            return
        laufe([sys.executable, render, nar, vo, lookpfad, a.out] + extra)
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.out],
                             capture_output=True, text=True).stdout.strip())
    lim = projekt["format"]["laenge_sekunden"]
    if d < lim["min"] or d > lim["max"]:
        print(f"WARNUNG: Länge {d:.1f} s liegt außerhalb von {lim['min']} bis {lim['max']} s (projekt.json). "
              "Sprechtext anpassen, nicht kürzen, um Credits zu sparen.")
    print(f"VIDEODONE {a.out} ({d:.1f} s)")


if __name__ == "__main__":
    main()
