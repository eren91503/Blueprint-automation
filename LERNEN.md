# LERNEN: bekannte Fehler und Lösungen

Die Automatik liest diese Datei **vor** jedem Stopp. Passt ein Fehler zu einem Eintrag, wird die Lösung angewendet und weitergemacht. Erst wenn die Lösung nach den hier genannten Versuchen nicht hilft, stoppt die Sitzung und benachrichtigt den Nutzer.

Neue Lösung gefunden? In zwei bis drei Sätzen unten anhängen (Format siehe Ende), committen und pushen.

Platzhalter in `<spitzen Klammern>` kommen aus `projekte/<kanal>/projekt.json`.

Quelle der ersten Einträge: Erfahrungen aus dem Kanal Faktum (Oktober 2026). Einträge mit "Beobachtung" sind noch nicht bestätigt.

---

## Start und Umgebung

**Clone meldet "could not read Username"**
Das Repo ist noch nicht in der Sitzung eingebunden. Zuerst `add_repo` (Zugriff push), dann klonen.

**Setup meldet eine Playwright-Warnung**
Blockiert nichts. Der Browser liegt unter `/opt/pw-browsers/`.

**Standbilder (`stills.mjs`) brechen still ab, weil der Browser in anderer Version liegt**
Verweis von der erwarteten auf die vorhandene Version anlegen. Zuerst `mkdir -p` auf den erwarteten Ordner, dann `ln -sfn` vom vorhandenen `chrome-headless-shell-linux64` auf `chrome-linux` im erwarteten Ordner, dazu `ln -sf chrome-headless-shell headless_shell` im vorhandenen Ordner. Die Versionsnummern mit `ls /opt/pw-browsers/` nachsehen.

**Schnittskript meldet fehlende Python-Pakete (z. B. pygame)**
Das Skript wurde mit dem falschen Python gestartet. Immer mit `PROJECT_PY=<Pfad zur venv>/bin/python` starten.

**Prozess beenden endet mit Exit 144**
`pkill` mit dem Namen im eigenen Befehl beendet sich selbst. Prozesse per PID beenden. Lange Renderläufe mit `setsid bash skript.sh &` starten.

**Zeilen-IDs passen nicht (KeyError im Zeitachsen-Skript)**
Vor dem Vertonen die Zeilen-IDs der Szene mit dem Sprechtext abgleichen. Hat die Szene mehr Zeilen als das Skript, die Zuordnung in der Szenendatei anpassen, nicht das Skript.

---

## Stimme (ElevenLabs)

**Fehler 429 (`rate_limited`)**
Das ist ein Tempo-Limit des Kontos, kein Credit-Problem. Es entsteht kein Audio und es wird nichts abgebucht.
1. Status des laufenden Blocks abfragen.
2. Denselben Block nach 60 Sekunden noch einmal starten. Hilft das nicht, nach 5 Minuten, dann nach 10 Minuten.
3. Danach stoppen und den Nutzer benachrichtigen. Nicht minütlich weiter probieren.
Beobachtung: Rund 16 Wiederholungen im Takt von 35 bis 60 Sekunden scheiterten alle, nach über einer Stunde Pause ging der nächste Block sofort. Nach dem Wechsel auf einen höheren Plan (Starter) kam gar kein 429 mehr, alle sechs Blöcke liefen je rund 15 Sekunden. Bei dauerhaften 429 also den Plan prüfen.

**Zweiter Zugang oder `creative_run_flow_nodes` als Ausweg**
Nicht nutzen. Gleiches Konto, gleiches Limit, es erzeugt nur Fehlversuche. Immer `creative_generate_speech` mit der festen `flow_id` aus `creative_create_flow`.

**Aufrufe parallel**
Nie. Immer nur ein Aufruf zugleich, nach jedem Block den Status abfragen, dann den nächsten starten. Ein Aufruf wird nur wiederholt, wenn der erste einen Fehler geliefert hat, nie nach einem Erfolg (sonst doppelte Kosten).

**Sechs Blöcke statt jeder Zeile einzeln**
Spart Aufrufe und Credits. Zeilen eines Blocks mit `<break time="1.0s" />` verbinden.

**Pausen-Tag wird nur etwa 0,4 s lang gesprochen**
`<break time="1.0s" />` klingt so kurz wie eine Satzpause. Schneiden nach den längsten Pausen trifft dann falsche Stellen. Das Schnittskript ordnet die Pausen den Satzzeichen (. ? ! :) der Zeilen zu und nimmt nur sonst die längsten Pausen. Nach dem Schneiden die Zeilenlängen in der Zeitachse prüfen.

**Schnitte liegen trotzdem falsch (eine Zeile ist viel zu lang)**
Die Pausenzahl passt nicht zu den Satzzeichen. Pausen mit `ffmpeg silencedetect` ansehen und `<block_dir>/cuts.json` anlegen, z. B. `{"sim":[4.6,9.1,13.5]}`. Die Schnittskripte lesen diese Datei vorrangig.

**Signaturlinks von ElevenLabs sind aus der Sitzung gesperrt (403 per curl)**
Die Shell erreicht diese Adressen nicht. Audio über die Übergabefunktion holen, die in `projekt.json` unter `audio_uebergabe` steht (bei Faktum: Composio-Workbench mit einer Hilfsdatei im Drive, die die Blöcke ins Repo legt). Danach `git pull`, die Blöcke liegen im Ordner des Videos.

**Audio schon vorhanden und Sprechtext unverändert**
Nicht neu vertonen. Nur schneiden und rendern. Das spart Credits.

---

## Inhalt und Qualität

**Vergleich leer (Variante B erzeugt keine Wechsel oder Ereignisse)**
Vor dem Vertonen den Zähler für Ereignisse ausgeben. Sind beide Varianten gleich oder fehlt das Ereignis, Sprechtext ehrlich anpassen ("kein Unterschied" ist ein gültiges Ergebnis). Nie Credits für ein leeres Ergebnis ausgeben. Gibt es auch dann kein brauchbares Ergebnis: Stopp.

**Zahlen im Bild weichen vom Sprechtext ab**
Nach dem Rendern nur eine Übersicht mit zwei bis drei Schlüsselbildern ansehen und die Zahlen gegen den Sprechtext abgleichen. Bei Abweichung korrigieren und erneut rendern, nicht neu vertonen.

**Zahlen im Sprechtext**
Ausschreiben (sonst liest die Stimme sie falsch). Im Feld `check` steht die Variante mit Ziffern, so wie die Spracherkennung sie schreibt.

---

## TikTok-Upload (über Composio)

Diese Einträge stammen aus der TikTok-Dokumentation, nicht aus eigenen Läufen. Sie sind noch nicht in der Praxis bestätigt.

**Fehler 403 `spam_risk_too_many_pending_share`**
Es warten zu viele Uploads im Posteingang (Grenze: 5 innerhalb von 24 Stunden je Konto). Nicht wiederholen. Nutzer benachrichtigen, dass er wartende Entwürfe posten oder löschen soll, und den Upload erst danach neu starten. Den Upload-Zeitpunkt näher an den Slot legen.

**Fehler 429 `rate_limit_exceeded`**
Zu viele Anfragen (Grenze: 6 pro Minute je Zugang). 60 Sekunden warten, einmal erneut versuchen, nicht in einer Schleife.

**Anmeldung bei Composio schlägt fehl oder Werkzeuge fehlen**
Mögliche Ursachen laut Composio: keine eigene TikTok-Developer-App, App im Sandbox-Modus (nur Tester dürfen sich anmelden), oder Rechte angefordert, die nicht freigegeben sind. Eine ausdrückliche Rechteliste mit nur den freigegebenen Rechten setzen und neu verbinden. Ohne `video.list` fehlt die Abfrage, ob schon gepostet wurde.

---

## Git

**`git push -f` auf einen Branch wird vom Sicherheitsfilter blockiert**
Normal pushen (Fast-Forward). Vorher `git pull --rebase`.

**Push wird mit HTTP 413 abgelehnt**
Der Klon ist flach und veraltet. Vorher `git fetch origin <branch>`, dann pushen.

**Clone liefert HTTP 429 (zu viele gleichzeitige Übertragungen)**
Das ist die Sitzungsgrenze, kein GitHub-Limit. Einmal nach 5 Sekunden erneut klonen, nicht in einer Schleife.

---

## Drive und Ablage

**Falscher Ordner**
Nur die Ordner-IDs aus `projekt.json` benutzen. Lokal synchronisierte Ordner (z. B. "Mein Mac" oder "Computer") nie anfassen und nicht als "alte Datei" ansehen. Bei Faktum lag genau hier ein Fehler: zwei ähnliche Ordner, nur einer ist richtig.

**Datei landet nicht im Ordner `erstellt`**
Manche Upload-Funktionen legen in einen Standardordner. Nach dem Upload immer die `parents` der Datei prüfen. Ist es der falsche Ordner, mit der Verschieben-Funktion (`add_parents`, `remove_parents`) korrigieren und erneut prüfen.

**Alte Datei gleichen Namens**
Außerhalb von `erstellt` und `gepostet` in den Drive-Papierkorb legen. Nie endgültig löschen.

**Themen-Tabelle zeigt veraltete Stati**
Nach jeder Abgabe die Tabelle synchronisieren (Stati: offen, erstellt, im Postfach, gepostet). Jeder Produktionslauf macht das zusätzlich zu Beginn.

---

## Format der Einträge

```
**<Kurztitel des Fehlers>**
<Ursache in einem Satz.> <Lösung in ein bis zwei Sätzen.> (Datum, Kanal, bestätigt oder Beobachtung)
```
