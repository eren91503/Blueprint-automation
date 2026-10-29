# Inhaltsmodule

Ein Modul macht aus einem Thema und einem Skript ein fertiges Video. Die Pipeline (Ablauf, Fehler, Ablage, Zeitplan) bleibt für alle Kanäle gleich. Nur das Modul unterscheidet sich je nach Videoart.

## Schnittstelle (gilt für jedes Modul)

**Eingabe**
- `narration.json`: Liste von Zeilen mit `id`, `say` (Sprechtext), `sub` (Untertitel). Weitere Felder je nach Modul.
- Ordner mit den Zeilen-Audios: je Zeile `<id>_f.wav` (oder `.mp3` gleichen Namens).
- `look.json`: Look des Kanals (Farben, Schrift, Untertitel). Kommt aus der Einrichtung.

**Ausgabe**
- Eine MP4-Datei im Format aus `projekt.json` unter `format`.
- Auf Wunsch eine Übersicht mit Schlüsselbildern für die Prüfung (`--sheet`).

**Pflichtverhalten**
- Fehlt Audio, bricht das Modul mit einer klaren Meldung ab (keine stille Ersatzlösung).
- Ein Testmodus ohne Stimme (`--platzhalter`) erlaubt Vorschau ohne Credits.
- Kein Kanalname, keine Farben und keine Pfade im Code. Alles kommt aus `look.json` und den Argumenten.

## Verfügbare Module

| Modul | Eignet sich für | Stand |
|---|---|---|
| `erklaervideo_text_bild` | Erklärvideos mit Textkarten, optionalen Bildern und Untertiteln | Läuft, mit Platzhalter-Ton und Testtönen geprüft. Noch nicht mit einer echten Stimme und nicht mit 60 bis 80 Sekunden Länge getestet |

Weitere Vorlagen (Zahlen-Animation, Simulation) entstehen, wenn ein Kanal sie braucht. Faktums eigene Pipeline (Simulation, Remotion, Schilder-Design) ist ein Sonderfall und gehört nicht in dieses Verzeichnis.
