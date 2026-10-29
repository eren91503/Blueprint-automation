# Einrichtung: Dialog mit Claude

Diese Datei führt Claude durch die Einrichtung eines neuen Kanals. Ziel: Am Ende liegt `projekte/<kanal>/` mit `projekt.json`, `queue.json`, `schedule.json` und Caption-Regeln im Repo, und der Nutzer hat das Testvideo bestätigt und das ganze Projekt freigegeben.

Reihenfolge beim Start: Idee (Schritt 1) und Name (Schritt 2) werden schon **vor** dem Repo geklärt, weil der Repo-Name daraus entsteht. Das steht in den Start-Anweisungen (`vorlage/projektanweisungen_einrichtung.md`), dort bekommt die Person auch die Anleitung, wie das Repo aus der Vorlage angelegt wird. Ist dieses Repo eingebunden, sind Schritt 1 und 2 meist schon erledigt: Claude prüft kurz, ob Idee und Name im Chat bestätigt wurden, und macht sonst dort weiter, wo etwas fehlt.

Regeln für Claude:
- Immer nur eine Frage auf einmal, kurz, auf Deutsch, ohne Fachwörter. Der Nutzer ist kein Programmierer.
- Nichts anlegen, bis der Nutzer in Schritt 10 die **Projektfreigabe** gibt (Wort: "Freigabe").
- Keine Credits für Proben ausgeben, ohne vorher zu sagen, was es kostet (ungefähr).
- Bestehende Kanäle (z. B. Faktum) nie verändern.

## Ablauf

**1. Idee, Ziel und Zielgruppe**
Worum geht es im Kanal, wer soll zuschauen, was soll hängen bleiben? Plattform festhalten. Hat die Person noch keine klare Idee, schlägt Claude 3 bis 5 Richtungen vor und fragt, was davon passt. Erst wenn die Idee in ein bis zwei Sätzen steht und die Person sie bestätigt, geht es weiter.

**2. Name des Kanals**
Gibt es schon einen Namen (z. B. den TikTok-Namen)? Dann übernimmt Claude ihn unverändert. Wenn nicht, schlägt Claude auf Basis der Idee 6 bis 8 Namen vor (kurz, merkbar, gut aussprechbar, zur Zielgruppe passend, jeweils mit einem Halbsatz Begründung). Die Person wählt oder ändert. Claude weist darauf hin, dass er nicht prüfen kann, ob der Name auf der Plattform frei ist: Die Person schaut selbst in der App nach und meldet sich, falls er vergeben ist. **Der Name wird erst übernommen, wenn die Person ihn ausdrücklich bestätigt.** Festhalten: Kanalname (für `kanal.name`) und ein Kurzname in Kleinbuchstaben ohne Leerzeichen für den Ordner `projekte/<kanalkurz>/`.

**Direkt nach der Namensbestätigung: Zugriffe prüfen und Drive-Ordner anlegen (automatisch, ohne Rückfrage).** Das ist die einzige Ausnahme von "nichts anlegen vor der Freigabe", weil die Person die Verbindungen schon selbst freigegeben hat und ein leerer Ordner nichts verändert.
1. Claude prüft, ob GitHub, Google Drive und ElevenLabs erreichbar sind und ob in Composio GitHub und Google Drive gekoppelt sind. Fehlt etwas, sagt er genau, was die Person verbinden muss (siehe `ANLEITUNG_FREUNDE.md`), und wartet darauf.
2. Claude lädt `tools/bridge.py` in die Composio-Umgebung und ruft `drive_ordner("<Kanalname>")` auf. Das legt in "Meine Ablage" den Ordner `<Kanalname>` mit den Unterordnern `erstellt` und `gepostet` an. Gibt es sie schon, werden sie wiederverwendet, nichts wird doppelt angelegt.
3. Die zurückgegebenen Ordner-IDs merkt sich Claude für `projekt.json` (`ablage.drive_ordner_erstellt`, `ablage.drive_ordner_gepostet`) und schreibt sie beim Anlegen (Schritt 11) ein.
4. Claude sagt der Person in einem Satz, dass der Ordner da ist. Ändert die Person später den Namen, legt Claude keinen zweiten Ordner an, sondern fragt, ob der bestehende umbenannt werden soll.

**3. Format**
Länge pro Video, Videos pro Tag, Seitenverhältnis (Standard 9:16, 1080x1920, 30 fps), Sprache.

**4. Konzept und Inhaltsquelle**
Vorschläge zeigen (Fragevideo, Erklärvideo, Story, Quiz, Fakten, Ranking, Zahlen-Animation, Simulation). Der Nutzer wählt eins. Dann klären, woher die Inhalte kommen (eigene Recherche mit Quellen, Simulation, Stockmaterial, Text-Animation) und welches Modul aus `module/` passt. Gibt es noch keins, sagt Claude das offen und schlägt die nächstliegende Vorlage vor.

**5. Skriptstruktur**
Welche Blöcke hat jedes Video (z. B. Hook, Hauptteil, Ergebnis, Schluss)? Wie viele Wörter, wie viele Zeilen pro Block? Drei Beispielskripte schreiben, der Nutzer wählt und korrigiert.

**6. Stimme**
Anbieter und Stimme. **Die Person sucht die Stimme selbst aus und nennt den Stimmcode.** Ablauf:
1. Claude fragt: "Such dir in ElevenLabs unter Voices (Voice Library) eine Stimme aus, die zu deinem Kanal passt, und schick mir ihre Voice-ID." Er erklärt kurz, wo man sie findet: bei der Stimme auf "ID" bzw. "Copy Voice ID" klicken (eine lange Zeichenfolge aus Buchstaben und Zahlen). Stimmen aus der Library müssen vorher mit "Add to my voices" in die eigene Sammlung.
2. Die Person schreibt die ID in den Chat. Claude übernimmt sie unverändert, nie aus dem Gedächtnis und nie eine eigene Auswahl.
3. Claude prüft die ID mit `creative_list_voices`. Ist sie dort nicht zu finden, sagt er, was fehlt (meist "Add to my voices"), und fragt noch einmal. Nichts wird fortgesetzt, bevor die ID gefunden wurde.
4. Danach eine kurze Hörprobe (vorher Kosten nennen, ein Satz reicht). Klingt die Stimme nicht passend, fragt Claude nach einer neuen ID.
5. Festhalten in `projekt.json` unter `stimme`: `voice_id`, Modell, Sprache, Ton (ruhig, frech, sachlich). Weiter geht es erst mit der bestätigten Stimme.
Möchte die Person keine eigene Stimme suchen, kann Claude auf Wunsch mit `creative_list_voices` Vorschläge machen, die ID bestätigt trotzdem die Person.

**7. Look**
Farben, Schrift, Layout, Untertitel, Intro und Outro. Möglichst mit einem Beispielbild klären, nicht nur mit Worten.

**8. Testvideo**
Ein Video aus einem der Beispielskripte bauen. Dabei Prüfung vor der Vertonung und Prüfbild nach dem Rendern wie in `GO.md`. Dem Nutzer zeigen und die Credits pro Video nennen. Korrekturen einarbeiten, bis er sagt, dass das Testvideo passt ("Testvideo OK"). Das ist noch nicht die Projektfreigabe.

**9. Themenliste und Zeitplan**
Ersten Satz Themen vorschlagen (Anzahl nach `themenliste.nachschub`, mindestens 30 für den Start) und freigeben lassen. Dann den Zeitplan nach **`ZEITPLAN.md`** abfragen: Posting-Zeiten, bis wann die Videos fertig sein sollen, Bauzeit, Upload und Erinnerung, Pausen, Zeitzone. Daraus den Plan ableiten und als Tabelle zeigen. Der Nutzer entscheidet selbst, nichts davon wird vorgegeben.

**10. Gesamtübersicht und Projektfreigabe**
Claude fasst alles auf einer Seite zusammen, damit die Person das ganze Projekt auf einmal sieht und entscheidet:
- Idee und Zielgruppe, **Kanalname** (bestätigt), Plattform
- Format (Länge, Videos pro Tag), Konzept und Inhaltsmodul, Skriptstruktur
- Stimme (Name und Voice-ID, bestätigt), Look (Farben, Schrift)
- Testvideo (bestätigt) und Credits pro Video, daraus geschätzte Credits pro Monat im Vergleich zum Plan
- Themenliste (Anzahl, erste fünf Themen) und der Zeitplan als Tabelle mit den Limits
- Was Claude danach selbst tut (Dateien anlegen, geplante Aufgaben einrichten, Betriebs-Projektanweisungen ausgeben) und was bewusst offen bleibt (Posten von Hand)
Dann fragt Claude genau einmal: "Soll ich das Projekt so anlegen? Schreibe **Freigabe**, oder sag, was geändert werden soll." Änderungen werden eingearbeitet und die Übersicht erneut gezeigt. **Mit der Freigabe ist der restliche Ablauf (Schritte 11 und 12) ohne weitere Rückfragen freigegeben.** Claude fragt dann nur noch, wenn etwas fehlt oder nicht geht.

**11. Anlegen**
Erst jetzt: `projekte/<kanal>/` aus `vorlage/` erzeugen und ausfüllen, die Drive-Ordner `erstellt` und `gepostet` aus Schritt 2 prüfen (liegen die IDs in `projekt.json` und existieren die Ordner noch?), geplante Aufgaben nach `ZEITPLAN.md` anlegen (Bau-Sitzungen, Upload, Erinnerung, Themen-Nachschub), gemäß der freigegebenen Planungstabelle, Projektanweisungen aus `vorlage/projektanweisungen.md` für das Claude-Projekt des Kanals ausfüllen und ausgeben. Sie ersetzen die Einrichtungs-Fassung (`vorlage/projektanweisungen_einrichtung.md`).

**12. Ersten Lauf beobachten**
Am nächsten Abend prüfen, ob das Video in `erstellt` liegt. Fehler und Lösungen in `LERNEN.md` eintragen.

## Was Claude beim Einrichten festhalten muss

Alles aus den Schritten 1 bis 9 kommt in `projekt.json`. Fehlt ein Wert, wird nachgefragt, nicht geraten. Zugangsdaten (Passwörter, API-Schlüssel) kommen nie in eine Datei im Repo.
