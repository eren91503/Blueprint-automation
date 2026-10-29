# GO: Betriebsanleitung der Automatik (für alle Kanäle)

Diese Datei gilt für jeden Kanal. Alles Kanalspezifische kommt aus `projekte/<kanal>/projekt.json`. Nichts davon wird hier fest eingetragen.

Auslöser: eine geplante Sitzung, oder der Nutzer schreibt "Go" für das nächste offene Thema.
Ziel: ein fertiges Video mit möglichst wenig Tokens und Credits. Knapp berichten, Logs nur gekürzt.

## Grundregeln
1. Design, Pipeline und Videostandard des Kanals nicht ändern. Änderungen nur auf ausdrücklichen Wunsch.
2. Zuerst `LERNEN.md` kennen. Tritt ein Fehler auf, dort nachsehen und die bekannte Lösung anwenden, bevor irgendetwas gemeldet wird.
3. Credits sparen: keine doppelten Wege, kein Testen auf Vorrat, nicht neu vertonen, wenn Audio und Sprechtext schon passen.
4. Ehrlich berichten, auch wenn ein Ergebnis "kein Unterschied" oder "schwach" lautet.

## 0. Start (immer zuerst, ohne Rückfrage)
1. Dieses Repo einbinden (`add_repo`, Zugriff push) und klonen. Meldet der Clone "could not read Username", fehlt nur das Einbinden.
2. `setup.sh` ausführen, falls vorhanden.
3. Kanal bestimmen: Der Name des Kanals steht in den Projektanweisungen der Sitzung. Dann `projekte/<kanal>/projekt.json` lesen. Fehlt die Datei: Stopp, Nutzer benachrichtigen.

## 1. Slot und Thema bestimmen
1. `schedule.json` des Kanals lesen (Ort steht in `projekt.json` unter `zeitplan`). Die Slots des Tages "heute plus `zeitplan.vorlauf_tage`" (Standard: morgen) nach Uhrzeit sortieren. Pausentage aus `zeitplan.pausentage` überspringen. Sitzung A nimmt den ersten, Sitzung B den zweiten, und so weiter. Ohne Slot morgen: nichts tun.
2. Eintrag in `queue.json` suchen (Feld `datei` entspricht dem Slot).
   - Status `fertig`, oder liegt die Datei schon in `erstellt`: nichts tun, melden "schon fertig".
   - Es gibt einen Eintrag mit Status `wartet_freigabe`: nichts Neues bauen, den Nutzer erinnern, stoppen.
3. Modus des Eintrags:
   - `neu_vertonen`: vorhandene Szene und Sprechtext nur neu vertonen, nichts umschreiben.
   - `neu_bauen`: die Schritte 2 bis 6, das Thema steht schon im Eintrag (nicht neu wählen). Das Feld `hinweis` beachten.

## 2. Inhalt erzeugen (Inhaltsmodul des Kanals)
Das Modul steht in `projekt.json` unter `inhaltsmodul`. Es liefert Szenen und Zeitmarken aus Thema und Skript.
- **Vor der Vertonung den Inhalt prüfen.** Bei Simulationen: Unterscheiden sich die Varianten, kommen die Ereignisse vor, passen die Zahlen zum Sprechtext? Sonst Sprechtext ehrlich anpassen. Nie Credits für ein leeres Ergebnis ausgeben.
- Echte Zahlen aus Quellen. Höchstens so viele Websuchen, wie `limits.websuchen` erlaubt, Quellen im Docstring des Skripts.

## 3. Sprechtext
Struktur, Blöcke, Wortzahl und Ziellänge stehen in `projekt.json` unter `skript`. Zahlen im Sprechtext ausschreiben. Nicht kürzen, um Credits zu sparen.
Ablage: `projekte/<kanal>/videos/<id>/narration.json` (Felder siehe `module/<modul>/README.md`). Danach `python3 tools/bloecke.py projekte/<kanal>/videos/<id>/narration.json projekte/<kanal>/videos/<id>/blocks.json` ausführen. Es zeigt Blöcke, Wörter und Zeichen (Richtwert für die Credits) und warnt, wenn eine Zeile nicht mit . ? ! oder : endet.

## 4. Stimme
Anbieter, Stimme, Modell und `generations_count` stehen in `projekt.json` unter `stimme`. Das Beispiel gilt für ElevenLabs:
- Vorher `creative_create_flow`, dann **ein Aufruf pro Block** (nicht pro Zeile) mit der festen `flow_id`.
- Der Blocktext steht in `blocks.json` (Feld `text` je Szene), die Zeilen sind dort schon mit dem Pausen-Tag verbunden.
- Die `voice_id` kommt aus `projekt.json`, nie aus dem Gedächtnis.
- **Immer nur ein Aufruf zugleich.** Nach jedem Block den Status abfragen, erst dann den nächsten starten.
- Fehler 429, Pausen-Tag, Signaturlinks: siehe `LERNEN.md`.

## 5. Audio holen
In der Composio-Umgebung `tools/bridge.py` aus dem Repo laden (Anleitung im Kopf der Datei) und `audio_to_repo("<owner>/<repo>", "projekte/<kanal>/videos/<id>", {"hook": <Link>, ...})` aufrufen. Die Links stammen aus dem Status-Ergebnis der Stimmen-Aufrufe. Danach `git pull`: Die Blöcke liegen in `projekte/<kanal>/videos/<id>/blocks/<szene>.mp3`. Schlägt das nach zwei Versuchen fehl: Stopp (Abschnitt 8).

## 6. Szenen und Video
- `python3 tools/finish.py projekte/<kanal> projekte/<kanal>/videos/<id> projekte/<kanal>/videos/<id>/out/<Datei>.mp4`: schneidet die Blöcke in Zeilen, erzeugt `out/uebersicht.png`, rendert das Video mit dem Modul aus `konzept.inhaltsmodul` und prüft die Länge gegen `format.laenge_sekunden`.
- Zuerst nur mit `--nur-uebersicht` aufrufen und die Übersicht ansehen (Zahlen gegen den Sprechtext abgleichen). Bei Fehlern korrigieren, dann voll rendern.
- Meldet `split_blocks.py` einen Hinweis oder eine Warnung zu einer Zeilenlänge, die Schnitte prüfen (siehe `LERNEN.md`, Pausen-Tag, und `cuts.json`).
- Ohne Credits testen: `python3 tools/trockenlauf.py projekte/<kanal> projekte/<kanal>/videos/<id>`.
- Ein ähnliches bestehendes Video des Kanals als Vorlage für das Skript nehmen, statt alles neu zu schreiben.

## 7. Abgabe (ohne Einzel-Freigabe)
1. Video in den Zweig `videos` pushen (`out_videos/<Datei>`, normal pushen, nicht mit Gewalt). Dann in der Composio-Umgebung `video_to_drive("<owner>/<repo>", "out_videos/<Datei>", "<Datei>", "<ablage.drive_ordner_erstellt>", branch="videos")` aufrufen. Das Ergebnis muss `in_ordner: true` melden, sonst Stopp (Abschnitt 8).
2. Alte Datei gleichen Namens außerhalb von `erstellt` und `gepostet` in den Drive-Papierkorb. Nie endgültig löschen.
3. `queue.json` auf `fertig` setzen, `git pull --rebase`, committen, pushen.
4. (Optional, noch nicht im Blueprint) Themen-Tabelle aktualisieren.
5. Kurze Nachricht an den Nutzer: "<Kanal> <id> <Titel> fertig (Dauer, Credits)".

## 8. Bei einem Problem
Erst `LERNEN.md` prüfen und die dort beschriebene Lösung anwenden. Hilft das nicht, gilt:
- **Stopp und Nutzer benachrichtigen** (Nachricht mit Video, Problem, was schon erledigt ist).
- Grenzen: Stimmen-Fehler nach den in `LERNEN.md` genannten Wiederholungen, Render- oder Upload-Fehler nach zwei Versuchen, Inhalt ohne brauchbares Ergebnis.
- Danach nichts weiter versuchen und keine Credits mehr ausgeben.
- Ist die Lösung inzwischen bekannt: in zwei bis drei Sätzen unter `LERNEN.md` eintragen, committen, pushen.

## 9. Themennachschub
Zwei Tage vor Ende der Liste schlägt eine geplante Aufgabe so viele neue Themen vor, wie `projekt.json` unter `themenliste.nachschub` festlegt, und wartet auf das OK des Nutzers. Nach dem OK werden sie in `queue.json` (Status `offen`, Modus `neu_bauen`) und `schedule.json` eingetragen.

## 10. Ordnung der Sitzungen
- Jedes Video läuft in einer eigenen Sitzung.
- Die Sitzungen starten zeitlich versetzt (`zeitplan.sitzungen`), damit sich die Vertonungen nicht überlappen. Ist die vorige Sitzung noch beim Vertonen, wartet die nächste, höchstens 30 Minuten.
- **Noch nicht Teil der Automatik:** Upload in den TikTok-Posteingang und die Erinnerung (Entwurf in `ANLEITUNG_FREUNDE.md`). Bis dahin liegt das fertige Video im Drive-Ordner `erstellt`, der Nutzer lädt und postet selbst. Wenn der Upload später dazukommt, gelten die Einstellungen in `projekt.json` unter `posten`.
- Vor jedem Upload die Limits aus `projekt.json` unter `limits` beachten (`tiktok_uploads_pro_24h`, `tiktok_upload_abstand_minuten`). Bei Fehler 403 wegen zu vieler wartender Uploads nicht wiederholen, den Nutzer benachrichtigen (siehe `LERNEN.md`, Abschnitt TikTok-Upload).
