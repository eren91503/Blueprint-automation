# Anleitung für Freunde: eigener Video-Kanal auf Autopilot

Entwurf. Die genauen Klickwege in den Einstellungen und die Schritte 6 bis 8 werden nach dem ersten Testlauf mit einem zweiten Kanal überprüft und angepasst.

Du brauchst keine Programmierkenntnisse. Du bekommst deine eigene Kopie der Vorlage, mit deinen eigenen Konten. Nichts wird mit anderen geteilt.

## Was du am Ende hast
Jeden Abend baut Claude automatisch die Videos für den nächsten Tag und legt sie in deinen Google-Drive-Ordner. Vor dem Slot liegt das Video als Entwurf in deinem TikTok-Posteingang. Du fügst nur noch die Caption ein und postest.

## Was du vorher brauchst

| Was | Wofür | Hinweis |
|---|---|---|
| Claude mit Projekten und geplanten Aufgaben | Dialog, Bauen der Videos, Zeitplan | Prüfe in deinem Plan, ob geplante Aufgaben dabei sind |
| GitHub-Konto | Speichert Vorlage, Themenliste, Zeitplan, Fehlerwissen und das Audio auf dem Weg zur Sitzung | Kostenlos, privates Repo |
| ElevenLabs-Konto | Die Stimme | Bezahlplan. Mit dem Gratisplan stößt du schnell an Grenzen. Bei Faktum verschwanden die Tempo-Fehler (429) nach dem Wechsel auf den Starter-Plan (Beobachtung) |
| Google-Konto mit Drive | Ablage der fertigen Videos (`erstellt`, `gepostet`) | Ordner in "Meine Ablage", nicht in einem mit dem Computer synchronisierten Ordner |
| Composio-Konto | Dateibrücke: holt das Audio von ElevenLabs ins Repo, lädt das fertige Video nach Drive und legt es in den TikTok-Posteingang | Die Sitzung selbst erreicht die ElevenLabs-Links nicht (403). Preis und Plan bei Composio selbst prüfen |
| TikTok-Konto | Das Video landet über Composio als Entwurf in deinem TikTok-Posteingang. Caption einfügen und Posten machst du selbst in der App | In Composio die TikTok-App mit deinem Konto koppeln. Voraussetzungen und Freigaben von TikTok vorher prüfen |

Kosten: Hauptsächlich der ElevenLabs-Plan. Frage in der Einrichtung, was ein Video ungefähr kostet, bevor du es freigibst.

## Was du in jedem Tool einrichtest

**GitHub**
1. Konto anlegen.
2. Vorlage `Blueprint-automation` als **privates** Repo kopieren (Schritt 3).
3. In Claude den GitHub-Connector verbinden, so dass Claude dein Repo mit Schreibzugriff (push) einbinden kann. Meldet Claude "kein GitHub-Zugriff", dort in den Connector-Einstellungen neu verbinden.

**ElevenLabs**
1. Konto anlegen, Bezahlplan wählen.
2. In Claude den ElevenLabs-Connector verbinden. Er muss Sprache erzeugen können.
3. Die Stimme wählst du nicht vorher, sondern im Einrichtungsdialog (Hörproben).

**Google Drive**
1. Online-Ordner anlegen: `<Kanal>/erstellt` und `<Kanal>/gepostet`.
2. In Claude den Drive-Connector verbinden.
3. Die Ordner-IDs trägt Claude beim Einrichten in `projekt.json` ein. Nie Ordner unter "Mein Mac" oder "Computer" verwenden.

**Composio**
1. Konto anlegen und den Composio-Connector in Claude verbinden.
2. In Composio drei Apps koppeln: **GitHub**, **Google Drive** und **TikTok** (dein eigenes Konto jeweils). Über die TikTok-Verbindung wird das Video in den Posteingang geladen.
3. Die Hilfsdatei `bridge.py` in deinen Drive-Ordner legen. Sie enthält deinen Repo-Namen und die ID des Ordners `erstellt`. **Noch zu bauen:** Bei Faktum liegt eine solche Datei fest verdrahtet im Drive. Im Blueprint muss sie erst verallgemeinert und getestet werden, bevor Freunde sie nutzen können.

**TikTok-Posteingang**
Bei Faktum übernimmt das Skript `run_faktum.py` (im Drive, läuft in der Composio-Umgebung) diesen Teil: Es legt das Video einige Zeit vor dem Slot als Entwurf in den TikTok-Posteingang (ohne zu veröffentlichen) und schickt dir kurz vor dem Slot eine Erinnerung mit Caption und Hashtags. Du fügst die Caption ein und postest. Außerdem pflegt es eine Themen-Tabelle mit Status und Kennzahlen. Dafür laufen zwei geplante Aufgaben: Upload und Erinnerung.

**Noch offen im Blueprint:** `run_faktum.py` hat bei Faktum Repo-Name, Ordner-IDs und Dateipfade fest eingetragen. Für das Blueprint muss es verallgemeinert und mit einem Testkonto geprüft werden, bevor Freunde es nutzen können. Dasselbe gilt für `bridge.py`.

## Schritt für Schritt

**1. Konten anlegen**
GitHub, ElevenLabs und Google Drive anlegen, falls du sie noch nicht hast.

**2. Claude mit den Konten verbinden**
In Claude unter Einstellungen die Verbindungen (Connectors) zu GitHub, ElevenLabs, Google Drive und Composio einschalten und jeweils anmelden. In Composio zusätzlich GitHub und Google Drive koppeln (Details im Abschnitt "Was du in jedem Tool einrichtest"). Wenn sich die Menüs anders nennen, frage Claude: "Wo verbinde ich GitHub?"

**3. Vorlage kopieren**
Auf der Seite des Repos `Blueprint-automation` auf **"Use this template"** klicken (wenn dort kein Knopf ist, bittet dich der Besitzer, ihn einzuschalten) und ein **privates** Repo mit deinem Namen anlegen, z. B. `mein-kanal-automation`.

**4. Drive-Ordner anlegen**
In Google Drive einen Ordner für deinen Kanal anlegen, darin zwei Unterordner: `erstellt` und `gepostet`. Nutze den Ordner in "Meine Ablage" (online), nicht einen Ordner, der mit deinem Computer synchronisiert wird.

**5. Claude-Projekt anlegen**
In Claude ein neues Projekt anlegen, Name = dein Kanal. Als Projektanweisungen den Inhalt von `vorlage/projektanweisungen.md` einfügen (die spitzen Klammern füllt Claude in Schritt 9 für dich aus). Dann schreibst du: **"Einrichtung starten"**.

**6. Dialog mit Claude**
Claude fragt dich eins nach dem anderen: Idee, Plattform, Länge, Stil, Stimme, Look. Er spielt Stimmproben vor und zeigt Beispielskripte. Antworte einfach in normalen Sätzen. Wenn du etwas nicht weißt, sag "schlag vor".

**7. Testvideo prüfen und freigeben**
Claude baut ein Testvideo. Schau es dir an und sag, was geändert werden soll. Wenn es passt, schreibe **"Freigabe"**. Vorher wird nichts automatisch angelegt.

**8. Themenliste und Zeitplan**
Claude schlägt Themen vor (du bestätigst). Dann fragt er dich, **wann du posten willst**, **bis wann die Videos fertig sein sollen** (z. B. am Vorabend), wann er bauen darf, wie früh vor dem Slot das Video im TikTok-Posteingang liegen soll und wann du erinnert werden willst. Daraus macht er einen Plan als Tabelle. Du sagst Ja oder änderst etwas. Erst dann legt er die geplanten Aufgaben an. Alles Weitere steht in `ZEITPLAN.md`.

**9. Automatik anlegen**
Nach deiner Freigabe legt Claude die Dateien für deinen Kanal an, richtet die geplanten Aufgaben ein und gibt dir die fertigen Projektanweisungen.

**10. Ersten Lauf beobachten**
Am nächsten Abend prüfen, ob das Video im Ordner `erstellt` liegt und du eine Nachricht bekommen hast. Danach: in der TikTok-App den Entwurf im Posteingang öffnen, Caption einfügen und posten.

## Wenn etwas schiefgeht
Die Sitzung stoppt von selbst und schickt dir eine Nachricht mit dem Problem. Du musst nichts reparieren. Antworte Claude in dem Chat, dort wird es gelöst und für alle Kanäle in `LERNEN.md` festgehalten.

## Häufige Fragen
- **Ich habe kein "Use this template".** Der Besitzer muss im Repo unter Settings die Option "Template repository" einschalten.
- **Posten die Videos automatisch?** Nein, bewusst nicht. Das Video kommt als Entwurf in den Posteingang, Caption und Posten machst du selbst. Das schützt dein Konto.
- **Wie viele Videos pro Tag?** Das legst du in Schritt 2 des Dialogs fest.
- **Wie ändere ich später etwas?** Schreibe in deinem Claude-Projekt, was sich ändern soll. Claude passt `projekt.json` an.
