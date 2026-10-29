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
Anbieter und Stimme. **Die Person sucht die Stimme selbst aus und nennt den Stimmcode.** Ablauf:
1. Claude fragt: "Such dir in ElevenLabs unter Voices (Voice Library) eine Stimme aus, die zu deinem Kanal passt, und schick mir ihre Voice-ID." Er erklärt kurz, wo man sie findet: bei der Stimme auf "ID" bzw. "Copy Voice ID" klicken (eine lange Zeichenfolge aus Buchstaben und Zahlen). Stimmen aus der Library müssen vorher mit "Add to my voices" in die eigene Sammlung.
2. Die Person schreibt die ID in den Chat. Claude übernimmt sie unverändert, nie aus dem Gedächtnis und nie eine eigene Auswahl.
3. Claude prüft die ID mit `creative_list_voices`. Ist sie dort nicht zu finden, sagt er, was fehlt (meist "Add to my voices"), und fragt noch einmal. Nichts wird fortgesetzt, bevor die ID gefunden wurde.
4. Danach eine kurze Hörprobe (vorher Kosten nennen, ein Satz reicht). Klingt die Stimme nicht passend, fragt Claude nach einer neuen ID.
5. Festhalten in `projekt.json` unter `stimme`: `voice_id`, Modell, Sprache, Ton (ruhig, frech, sachlich). Weiter geht es erst mit der bestätigten Stimme.
Möchte die Person keine eigene Stimme suchen, kann Claude auf Wunsch mit `creative_list_voices` Vorschläge machen, die ID bestätigt trotzdem die Person.

**6. Look**
Farben, Schrift, Layout, Untertitel, Intro und Outro. Möglichst mit einem Beispielbild klären, nicht nur mit Worten.

**7. Testvideo und Freigabe**
Ein Video aus einem der Beispielskripte bauen. Dabei Prüfung vor der Vertonung und Prüfbild nach dem Rendern wie in `GO.md`. Dem Nutzer zeigen. Korrekturen einarbeiten, bis er "Freigabe" schreibt.

**8. Themenliste und Zeitplan**
Ersten Satz Themen vorschlagen (Anzahl nach `themenliste.nachschub`, mindestens 30 für den Start) und freigeben lassen. Dann den Zeitplan nach **`ZEITPLAN.md`** abfragen: Posting-Zeiten, bis wann die Videos fertig sein sollen, Bauzeit, Upload und Erinnerung, Pausen, Zeitzone. Daraus den Plan ableiten und als Tabelle zeigen. Der Nutzer entscheidet selbst, nichts davon wird vorgegeben.

**9. Anlegen**
Erst jetzt: `projekte/<kanal>/` aus `vorlage/` erzeugen und ausfüllen, Drive-Ordner `erstellt` und `gepostet` prüfen oder anlegen, geplante Aufgaben nach `ZEITPLAN.md` anlegen (Bau-Sitzungen, Upload, Erinnerung, Themen-Nachschub), erst nach dem OK des Nutzers zur Planungstabelle, Projektanweisungen aus `vorlage/projektanweisungen.md` für das Claude-Projekt des Kanals ausfüllen und ausgeben. Sie ersetzen die Einrichtungs-Fassung (`vorlage/projektanweisungen_einrichtung.md`).

**10. Ersten Lauf beobachten**
Am nächsten Abend prüfen, ob das Video in `erstellt` liegt. Fehler und Lösungen in `LERNEN.md` eintragen.

## Was Claude beim Einrichten festhalten muss

Alles aus den Schritten 1 bis 8 kommt in `projekt.json`. Fehlt ein Wert, wird nachgefragt, nicht geraten. Zugangsdaten (Passwörter, API-Schlüssel) kommen nie in eine Datei im Repo.
