# Einrichtung: Dialog mit Claude

Diese Datei führt Claude durch die Einrichtung eines neuen Kanals. Ziel: Am Ende liegt `projekte/<kanal>/` mit `projekt.json`, `queue.json`, `schedule.json` und Caption-Regeln im Repo, und der Nutzer hat ein Testvideo freigegeben.

Regeln für Claude:
- Immer nur eine Frage auf einmal, kurz, auf Deutsch, ohne Fachwörter. Der Nutzer ist kein Programmierer.
- Nichts anlegen, bis der Nutzer in Schritt 7 "Freigabe" sagt.
- Keine Credits für Proben ausgeben, ohne vorher zu sagen, was es kostet (ungefähr).
- Bestehende Kanäle (z. B. Faktum) nie verändern.

## Ablauf

**1. Ziel und Zielgruppe**
Worum geht es im Kanal, wer soll zuschauen, was soll hängen bleiben? Plattform und Kanalname festhalten.

**2. Format**
Länge pro Video, Videos pro Tag, Seitenverhältnis (Standard 9:16, 1080x1920, 30 fps), Sprache.

**3. Konzept und Inhaltsquelle**
Vorschläge zeigen (Fragevideo, Erklärvideo, Story, Quiz, Fakten, Ranking, Zahlen-Animation, Simulation). Der Nutzer wählt eins. Dann klären, woher die Inhalte kommen (eigene Recherche mit Quellen, Simulation, Stockmaterial, Text-Animation) und welches Modul aus `module/` passt. Gibt es noch keins, sagt Claude das offen und schlägt die nächstliegende Vorlage vor.

**4. Skriptstruktur**
Welche Blöcke hat jedes Video (z. B. Hook, Hauptteil, Ergebnis, Schluss)? Wie viele Wörter, wie viele Zeilen pro Block? Drei Beispielskripte schreiben, der Nutzer wählt und korrigiert.

**5. Stimme**
Anbieter und Stimme. Bei ElevenLabs: mit `creative_list_voices` passende Stimmen vorschlagen, kurze Hörproben erzeugen (vorher Kosten nennen). Die Stimme-ID, das Modell und die Sprache festhalten. Ton (ruhig, frech, sachlich).

**6. Look**
Farben, Schrift, Layout, Untertitel, Intro und Outro. Möglichst mit einem Beispielbild klären, nicht nur mit Worten.

**7. Testvideo und Freigabe**
Ein Video aus einem der Beispielskripte bauen. Dabei Prüfung vor der Vertonung und Prüfbild nach dem Rendern wie in `GO.md`. Dem Nutzer zeigen. Korrekturen einarbeiten, bis er "Freigabe" schreibt.

**8. Themenliste und Zeitplan**
Ersten Satz Themen vorschlagen (Anzahl nach `themenliste.nachschub`, mindestens 30 für den Start) und freigeben lassen. Wochentage und Uhrzeiten der Slots festlegen. Die Sitzungen für den Vortag mit mindestens 60 Minuten Abstand planen.

**9. Anlegen**
Erst jetzt: `projekte/<kanal>/` aus `vorlage/` erzeugen und ausfüllen, Drive-Ordner `erstellt` und `gepostet` prüfen oder anlegen, geplante Aufgaben anlegen (Sitzung A, B, Themen-Nachschub), Projektanweisungen aus `vorlage/projektanweisungen.md` für das Claude-Projekt des Kanals ausgeben.

**10. Ersten Lauf beobachten**
Am nächsten Abend prüfen, ob das Video in `erstellt` liegt. Fehler und Lösungen in `LERNEN.md` eintragen.

## Was Claude beim Einrichten festhalten muss

Alles aus den Schritten 1 bis 8 kommt in `projekt.json`. Fehlt ein Wert, wird nachgefragt, nicht geraten. Zugangsdaten (Passwörter, API-Schlüssel) kommen nie in eine Datei im Repo.
