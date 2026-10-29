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
1. `schedule.json` des Kanals lesen (Ort steht in `projekt.json` unter `zeitplan`). Die Slots von **morgen** nach Uhrzeit sortieren. Sitzung A nimmt den ersten, Sitzung B den zweiten, und so weiter. Ohne Slot morgen: nichts tun.
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

## 4. Stimme
Anbieter, Stimme, Modell und `generations_count` stehen in `projekt.json` unter `stimme`. Das Beispiel gilt für ElevenLabs:
- Vorher `creative_create_flow`, dann **ein Aufruf pro Block** (nicht pro Zeile) mit der festen `flow_id`.
- Zeilen eines Blocks mit `<break time="1.0s" />` verbinden.
- **Immer nur ein Aufruf zugleich.** Nach jedem Block den Status abfragen, erst dann den nächsten starten.
- Fehler 429, Pausen-Tag, Signaturlinks: siehe `LERNEN.md`.

## 5. Audio holen
Über die Übergabefunktion aus `projekt.json` (`audio_uebergabe`). Danach `git pull`, die Blöcke liegen im Ordner des Videos.

## 6. Szenen und Video
- Ähnlichstes bestehendes Video des Kanals als Vorlage kopieren und anpassen, statt alles neu zu schreiben.
- Nach den Schnittskripten des Kanals vorgehen (Blöcke schneiden, Zeitachse, eine Übersicht, Video).
- Nur die eine Übersicht ansehen. Zahlen im Bild gegen den Sprechtext abgleichen. Bei Fehlern korrigieren und erneut rendern.
- Nach dem Schneiden die Zeilenlängen in der Zeitachse prüfen (siehe `LERNEN.md`, Pausen-Tag).

## 7. Abgabe (ohne Einzel-Freigabe)
1. Video in den Drive-Ordner `erstellt` (ID aus `projekt.json`). Danach die `parents` prüfen.
2. Alte Datei gleichen Namens außerhalb von `erstellt` und `gepostet` in den Drive-Papierkorb. Nie endgültig löschen.
3. `queue.json` auf `fertig` setzen, `git pull --rebase`, committen, pushen.
4. Themen-Tabelle synchronisieren.
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
- Posten und TikTok-Upload laufen nach den Einstellungen in `projekt.json` unter `posten`. Der Nutzer postet manuell aus der App.
