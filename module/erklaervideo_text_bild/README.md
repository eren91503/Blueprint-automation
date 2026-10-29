# Modul: Text-und-Bild-Erklärvideo

Macht aus einem Sprechtext mit Karten, Bildern und Untertiteln ein Hochformat-Video (1080x1920, 30 fps, H.264 und AAC).

## Voraussetzungen
- Python 3 mit Pillow (`pip install pillow`)
- `ffmpeg` und `ffprobe`
- Eine Schrift: Standard sucht Inter, DejaVu Sans oder Liberation Sans. Eigene Schrift über `look.json` (`schrift`).

## Aufruf
```
python3 render.py <narration.json> <vo_dir> <look.json> <out.mp4> [--bilder DIR] [--platzhalter] [--sheet PNG]
```

| Option | Wirkung |
|---|---|
| `--bilder DIR` | Ordner mit den Bildern, auf die `bild` in der Skriptzeile zeigt |
| `--platzhalter` | Keine Stimme nötig: Stille mit geschätzter Länge (2,6 Wörter pro Sekunde). Für Tests ohne Credits |
| `--sheet PNG` | Schreibt nur eine Übersicht mit je einem Schlüsselbild pro Zeile, kein Video. Das ist die Prüfung vor dem vollen Rendern |

Beispiel (ohne Stimme):
```
python3 render.py beispiel/narration.json "" beispiel/look.json test.mp4 --platzhalter
```

## Felder in `narration.json`
| Feld | Pflicht | Bedeutung |
|---|---|---|
| `id` | ja | Eindeutig, bestimmt den Namen der Audiodatei (`<id>_f.wav`) |
| `say` | ja | Sprechtext. Zahlen ausschreiben |
| `sub` | nein | Untertitel als Text oder als Liste kurzer Häppchen (nach Länge auf die Zeit verteilt). Fehlt er, wird `say` genommen |
| `karte` | nein | Große Textkarte. Sie bleibt sichtbar, bis eine neue Karte oder ein neues Bild kommt |
| `bild` | nein | Dateiname im Ordner `--bilder`. Wird über der Karte gezeigt |
| `scene` | nein | Frei, z. B. hook, haupt, schluss. Wird nicht gezeichnet |

## Felder in `look.json`
`kanalname`, `aufloesung`, `fps`, `pause` (Sekunden zwischen den Zeilen), `schrift` (Pfad oder `null`), `karte_groesse`, `farben` (hintergrund, panel, text, akzent, untertitel_bg, untertitel_text), `untertitel` (`position`: oben, mitte oder unten, `groesse`). Siehe `beispiel/look.json`.

## Layout
Fortschrittsbalken oben, Kanalname, große Karte in der Mitte, Untertitel darunter. Die Untertitel liegen im oberen Teil der unteren Hälfte, damit sie nicht unter der Oberfläche der App verschwinden. Ob das für jede Plattform passt, ist nicht geprüft.

## Grenzen
- Nur Standbilder mit Einblendung, keine Videoclips und keine Bewegung im Bild.
- Das Zerschneiden eines ElevenLabs-Blocks in einzelne Zeilen (bei Faktum `tools/split_blocks.py`) ist noch **nicht** im Blueprint. Das Modul erwartet fertige Zeilen-Audios.
- Getestet mit Platzhalter-Ton und Sinustönen, nicht mit einer echten Stimme.
