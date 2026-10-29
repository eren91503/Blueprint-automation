# ZEITPLAN: Abfrage und Ableitung der Pläne

Jeder entscheidet für seinen Kanal selbst, wann gepostet wird und wann neue Videos bereitliegen sollen. Claude fragt das in der Einrichtung ab (Schritt 9 in `EINRICHTUNG.md`), leitet daraus alle Pläne ab und zeigt sie als Tabelle. Angelegt werden sie **erst nach der Projektfreigabe** (Schritt 10), in der die Tabelle Teil der Gesamtübersicht ist.

## Teil 1: Fragen (eine nach der anderen)

1. **Wie viele Videos pro Tag?** Gleich an allen Tagen oder je Wochentag verschieden? Gibt es Tage ohne Video?
2. **Wann willst du posten?** Uhrzeiten je Wochentag (die Slots). Beispiel: Mo bis Fr 12:00 und 18:00, Sa 11:00.
3. **Wann soll das Video spätestens fertig sein?** Vorschlag: am Vorabend, damit du es vorab ansehen kannst. Alternative: früh am selben Tag. Daraus ergibt sich `vorlauf_tage` (Standard 1).
4. **Wann soll Claude bauen?** Vorschlag: abends ab 19:00, jedes weitere Video 60 Minuten später (die Vertonungen dürfen sich nicht überlappen, siehe `LERNEN.md`). Der Nutzer kann ein anderes Zeitfenster nennen, z. B. nachts.
5. **Wie früh vor dem Slot soll das Video im TikTok-Posteingang liegen?** Vorschlag: 65 bis 100 Minuten vorher.
6. **Wann willst du erinnert werden?** Vorschlag: 20 Minuten vor dem Slot, mit Caption und Hashtags.
7. **Gibt es Pausen?** Urlaub, Feiertage, feste freie Tage.
8. **Zeitzone?** Standard `Europe/Berlin`.
9. **Themenvorrat:** Wie viele Themen liegen bereit, und wie viele Tage vor Listenende sollen neue vorgeschlagen werden? Vorschlag: 2 Tage, jeweils 17 neue (an die Wochenmenge anpassen).

10. **Welchen ElevenLabs-Plan hast du?** Wie viele Credits pro Monat? Claude rechnet später damit.
11. **TikTok über Composio:** Gibt es eine eigene TikTok-Developer-App mit freigegebenen Rechten (`video.upload`, `video.list`)? Wurde schon einmal etwas in den Posteingang hochgeladen? Antwort "weiß ich nicht" wird als offener Punkt vermerkt, nicht geraten.

Fehlt eine Antwort, wird nachgefragt oder der Standard genommen und genannt, nie stillschweigend geraten.

## Teil 1b: Limits, die Claude vor dem Plan prüft

Claude vergleicht den gewünschten Plan mit diesen Grenzen und warnt, **bevor** etwas angelegt wird. Die TikTok-Werte stammen aus der Dokumentation von TikTok for Developers und der Composio-Dokumentation (Stand 29.10.2026). Grenzen ändern sich: Claude prüft sie bei der Einrichtung noch einmal und trägt abweichende Werte in `projekt.json` unter `limits` ein.

| Bereich | Grenze | Folge für den Plan |
|---|---|---|
| TikTok, Upload in den Posteingang | Höchstens 5 wartende Uploads innerhalb von 24 Stunden je Konto. Darüber kommt Fehler 403 (`spam_risk_too_many_pending_share`) | Mehr als 5 Videos pro Tag sind über den Posteingang nicht planbar. Claude warnt schon ab 4 pro Tag, weil Entwürfe, die noch nicht gepostet oder gelöscht sind, vermutlich mitzählen (Auslegung, nicht bestätigt) |
| TikTok, Anfragen | 6 Anfragen pro Minute je Zugang. Darüber kommt Fehler 429 (`rate_limit_exceeded`) | Zwei Uploads mindestens 5 Minuten auseinander, keine Wiederholungen in Schleifen |
| TikTok, direktes Veröffentlichen | Typisch etwa 15 Posts pro Tag und Konto. Nicht geprüfte Apps dürfen nur privat posten | Wird im Blueprint nicht genutzt (`veroeffentlichen: false`). Nur wichtig, falls später direkt gepostet werden soll |
| Composio und TikTok | Composio schreibt, dass man meist eine eigene TikTok-Developer-App mit eigenen Zugangsdaten braucht. Rechte: `video.upload`, `video.publish`, `video.list`. Im Sandbox-Modus oder während der Prüfung dürfen sich nur Tester anmelden. Nicht freigegebene Rechte lassen Werkzeuge ausfallen | Claude fragt (Frage 11). Ohne `video.list` funktioniert der Abgleich "schon gepostet" und die Themen-Tabelle nicht |
| ElevenLabs | Credits pro Monat laut Plan. Tempo-Limit (429) | Claude misst die Credits pro Video im Testvideo (Schritt 8), rechnet Videos pro Monat mal Credits pro Video und warnt bei Überschreitung. Ein Aufruf zugleich (siehe `LERNEN.md`) |
| Claude, geplante Aufgaben | Normalerweise frühestens stündlich. Jede Bau-Sitzung verbraucht Nutzung deines Claude-Plans | Claude zählt die Sitzungen pro Tag und nennt sie vor dem OK |

Regeln daraus:
- `limits.max_videos_pro_tag` (Standard 5) ist die Obergrenze. Wünscht der Nutzer mehr, sagt Claude, was dagegen spricht, und bietet Alternativen an (weniger Videos, ein zweites TikTok-Konto mit eigener Verbindung, direktes Veröffentlichen nach TikTok-Prüfung).
- Der Upload soll **spät** vor dem Slot laufen (siehe Frage 5), damit möglichst wenige Entwürfe gleichzeitig warten.
- Ein Upload-Fehler 403 wegen zu vieler wartender Uploads wird **nicht wiederholt**. Die Sitzung benachrichtigt den Nutzer, dass er wartende Entwürfe posten oder löschen soll (siehe `LERNEN.md`).

## Teil 2: Ableitung (Regeln für Claude)

Aus den Antworten entstehen drei Dinge:

| Ergebnis | Regel |
|---|---|
| `schedule.json` | Eine Zeile je Slot und Datum: Datei, Caption, Hashtags. Die Slots folgen dem Wochenmuster und überspringen Pausentage. |
| Bau-Sitzungen | Für jeden Tag, an dem Slots liegen, gibt es einen Bau-Tag `vorlauf_tage` früher. Sitzung A startet zur Bau-Startzeit, jede weitere um `abstand_minuten` später (A, B, C ...). Sitzung A baut den ersten Slot des Tages, B den zweiten usw. |
| Upload und Erinnerung | Upload: `upload_vorlauf_minuten` vor dem Slot. Erinnerung: `erinnerung_vorlauf_minuten` vor dem Slot. |
| Themen-Nachschub | Eine Aufgabe zum Zeitpunkt `nachschub_vorlauf_tage` vor dem Ende der Liste. Sie schlägt Themen vor und wartet auf das OK. |

### Welche geplanten Aufgaben angelegt werden

Bevorzugt **wenige wiederkehrende Aufgaben, die in `schedule.json` nachsehen, was fällig ist**. Dann reicht bei geänderten Slots eine Änderung der Datei, und die Aufgaben müssen nicht neu angelegt werden.

- **Bau-Sitzungen:** eine wiederkehrende Aufgabe je Sitzung (A, B, ...), jeden Tag zur festen Startzeit.
- **Upload:** wiederkehrend, sieht nach, welche Slots im Upload-Fenster liegen.
- **Erinnerung:** wiederkehrend, sieht nach, welche Slots in das Erinnerungsfenster fallen.
- **Themen-Nachschub:** wiederkehrend (z. B. täglich morgens), tut nur etwas, wenn das Listenende nah ist.

Zu beachten:
- Geplante Aufgaben laufen normalerweise **frühestens stündlich**. Läuft eine Aufgabe stündlich, muss das Fenster breit genug sein (mindestens 60 Minuten), sonst wird ein Slot verpasst. Wer genaue Uhrzeiten will, bekommt eine Aufgabe je Slot-Uhrzeit.
- Uhrzeiten in der Zeitzone des Nutzers angeben (nicht in UTC schreiben und dabei die Sommerzeit vergessen).
- Liegt die Minute auf :00 oder :30, den Start ein paar Minuten früher setzen, weil volle Stunden stark ausgelastet sind.
- Die Aufgaben-Prompts müssen eigenständig sein: Jeder Lauf beginnt ohne Gedächtnis an das Gespräch. Der Prompt verweist auf `GO.md`, den Kanalnamen und `projekte/<kanal>/projekt.json`.

### Prüfungen vor dem Anlegen

Claude rechnet nach und meldet Auffälliges:
- Reicht die Zeit? Letzte Bau-Sitzung des Tages plus Bauzeit muss vor dem Upload-Fenster des ersten Slots am Folgetag fertig sein.
- Wie viele Sitzungen pro Tag entstehen, und was kosten sie ungefähr (Credits, Aufrufe)? Vor dem OK nennen.
- Liegen Slots so eng, dass zwei Uploads zugleich fällig sind?
- Gibt es Tage ohne Slot, an denen keine Bau-Sitzung laufen soll?
- Hält der Plan alle Limits aus Teil 1b ein (Uploads pro 24 Stunden, Abstand der Uploads, Credits pro Monat)? Überschreitungen mit Zahlen nennen.

## Teil 3: Beispiel

Antworten: zwei Videos pro Tag, posten Mo bis Fr um 12:00 und 18:00, fertig bis zum Vorabend, Bau ab 19:00 mit 60 Minuten Abstand, Upload 80 Minuten vor dem Slot, Erinnerung 20 Minuten vorher, Zeitzone Berlin.

| Aufgabe | Zeit | Was sie tut |
|---|---|---|
| Bau A | täglich 19:00 | baut das erste Video für morgen |
| Bau B | täglich 20:00 | baut das zweite Video für morgen |
| Upload | 10:40 und 16:40 | legt das Video in den TikTok-Posteingang |
| Erinnerung | 11:40 und 17:40 | schickt Caption und Hashtags |
| Themen-Nachschub | täglich 09:30 | schlägt 2 Tage vor Listenende neue Themen vor |

Das Beispiel ist erfunden und dient nur der Veranschaulichung. Die echten Zeiten kommen aus den Antworten des Nutzers.

## Teil 4: Änderungen später

Sagt der Nutzer später "ich will jetzt um 20:00 posten" oder "ab nächster Woche drei Videos am Tag", passt Claude `projekt.json` und `schedule.json` an, rechnet Teil 2 neu durch, zeigt den Unterschied zur alten Planung und legt erst nach dem OK neue Aufgaben an oder ändert bestehende.
