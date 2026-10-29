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
| TikTok-Konto | Das Video landet über Composio als Entwurf in deinem TikTok-Posteingang. Caption einfügen und Posten machst du selbst in der App | In Composio die TikTok-App mit deinem Konto koppeln. Laut Composio brauchst du dafür meist eine eigene TikTok-Developer-App. Limit laut TikTok: höchstens 5 wartende Uploads in 24 Stunden. Voraussetzungen vorher prüfen |

Kosten: Hauptsächlich der ElevenLabs-Plan. Frage in der Einrichtung, was ein Video ungefähr kostet, bevor du es freigibst.

## Was du in jedem Tool einrichtest

**GitHub**
1. Konto anlegen.
2. Vorlage `Blueprint-automation` als **privates** Repo kopieren (macht Claude dir in Schritt 4 vor).
3. In Claude den GitHub-Connector verbinden, so dass Claude dein Repo mit Schreibzugriff (push) einbinden kann. Meldet Claude "kein GitHub-Zugriff", dort in den Connector-Einstellungen neu verbinden.

**ElevenLabs**
1. Konto anlegen, Bezahlplan wählen.
2. In Claude den ElevenLabs-Connector verbinden. Er muss Sprache erzeugen können.
3. Such dir in ElevenLabs unter **Voices** eine Stimme aus (bei Stimmen aus der Library erst "Add to my voices"). Kopiere ihre **Voice-ID** ("Copy Voice ID"). Claude fragt im Einrichtungsdialog danach, prüft die ID, spielt eine kurze Hörprobe, und erst dann geht es weiter.

**Google Drive**
1. Nichts von Hand anlegen: Sobald dein Kanalname feststeht, legt Claude in deinem Drive automatisch den Ordner `<Kanalname>` mit `erstellt` und `gepostet` an.
2. In Claude den Drive-Connector verbinden.
3. Die Ordner-IDs trägt Claude beim Einrichten in `projekt.json` ein. Der Ordner liegt in "Meine Ablage" (online). Nie Ordner unter "Mein Mac" oder "Computer" verwenden.

**Composio**
1. Konto anlegen und den Composio-Connector in Claude verbinden.
2. In Composio drei Apps koppeln: **GitHub**, **Google Drive** und **TikTok** (dein eigenes Konto jeweils). Über die TikTok-Verbindung wird das Video in den Posteingang geladen.
3. Die Hilfsdatei `tools/bridge.py` liegt in deinem Repo, und Claude lädt sie von dort in die Composio-Umgebung. Du legst nichts selbst ab. Repo-Name und Drive-Ordner übergibt Claude bei jedem Aufruf aus `projekt.json`. Die Datei wurde am 29.10.2026 live geprüft (Audio von ElevenLabs ins Repo, Video aus dem Repo nach Drive, Ordner kontrolliert).

**TikTok-Posteingang**
Bei Faktum übernimmt das Skript `run_faktum.py` (im Drive, läuft in der Composio-Umgebung) diesen Teil: Es legt das Video einige Zeit vor dem Slot als Entwurf in den TikTok-Posteingang (ohne zu veröffentlichen) und schickt dir kurz vor dem Slot eine Erinnerung mit Caption und Hashtags. Du fügst die Caption ein und postest. Außerdem pflegt es eine Themen-Tabelle mit Status und Kennzahlen. Dafür laufen zwei geplante Aufgaben: Upload und Erinnerung.

**Noch offen im Blueprint (bewusst):** Upload in den Posteingang, Erinnerung und Themen-Tabelle sind vorerst nicht Teil der Automatik. Bis dahin liegt das fertige Video im Drive-Ordner `erstellt`, und du lädst und postest selbst. `run_faktum.py` hat bei Faktum Repo-Name, Ordner-IDs und Dateipfade fest eingetragen und muss für das Blueprint erst verallgemeinert und mit einem Testkonto geprüft werden. Die Faktum-Fassung wiederholt fehlgeschlagene TikTok-Uploads bis zu viermal im Abstand von 20 bis 30 Sekunden. Die verallgemeinerte Fassung muss die Limits aus `projekt.json` beachten und bei Fehler 403 (zu viele wartende Uploads) nicht wiederholen.

## Schritt für Schritt

**1. Konten anlegen**
GitHub, ElevenLabs und Google Drive anlegen, falls du sie noch nicht hast.

**2. Claude mit den Konten verbinden**
In Claude unter Einstellungen die Verbindungen (Connectors) zu GitHub, ElevenLabs, Google Drive und Composio einschalten und jeweils anmelden. In Composio zusätzlich GitHub und Google Drive koppeln (Details im Abschnitt "Was du in jedem Tool einrichtest"). Wenn sich die Menüs anders nennen, frage Claude: "Wo verbinde ich GitHub?"

**3. Claude-Projekt anlegen und Start-Anweisungen einfügen**
In Claude ein neues Projekt anlegen (Name erst mal egal, du kannst es später umbenennen). Als Projektanweisungen fügst du den kompletten Inhalt von `vorlage/projektanweisungen_einrichtung.md` ein. Es muss nichts ersetzt werden. Dann schreibst du: **"Repo installieren"**. (Claude kann Projektanweisungen nicht selbst setzen, das ist der eine Handgriff am Anfang. Wenn du den Skill "repo-installieren" hast, gibt Claude dir den Text auf dieses Stichwort in einem Kopierblock aus.)

**4. Idee, Name und Repo (Claude führt dich)**
Claude fragt zuerst nach deiner Idee und deinem **Kanalnamen** (du hast schon einen, oder er schlägt dir welche vor und du bestätigst). Danach fragt er nach deinem GitHub-Namen und leitet daraus den Namen für dein Repo ab. Dann bekommst du **im Chat die Anleitung mit deinen echten Werten**: auf der Seite der Vorlage `Blueprint-automation` auf **"Use this template"**, **"Create a new repository"**, Owner = dein GitHub-Name, Name wie genannt, **Private**, **Create repository**. Wenn dort kein Knopf ist, muss der Besitzer der Vorlage sie freigeben (Template einschalten und dich einladen). Danach schreibst du **"Repo ist angelegt"**.

**5. Drive-Ordner: entfällt**
Den Ordner für deinen Kanal legt Claude selbst an, sobald der Name feststeht und die Verbindungen stehen (Schritt 2).

**6. Dialog mit Claude**
Weiter geht es mit: Plattform, Länge, Stil, Stimme, Look (Idee und Name sind schon geklärt). Bei der Stimme nennst du ihm die Voice-ID aus ElevenLabs, er spielt eine Hörprobe vor und zeigt Beispielskripte. Antworte einfach in normalen Sätzen. Wenn du etwas nicht weißt, sag "schlag vor".

**7. Testvideo prüfen und freigeben**
Claude baut ein Testvideo. Schau es dir an und sag, was geändert werden soll. Wenn es passt, schreibe **"Testvideo OK"**. Noch wird nichts angelegt.

**8. Themenliste und Zeitplan**
Claude schlägt Themen vor (du bestätigst). Dann fragt er dich, **wann du posten willst**, **bis wann die Videos fertig sein sollen** (z. B. am Vorabend), wann er bauen darf, wie früh vor dem Slot das Video im TikTok-Posteingang liegen soll und wann du erinnert werden willst. Daraus macht er einen Plan als Tabelle. Alles Weitere steht in `ZEITPLAN.md`.

**8b. Gesamtübersicht und Projektfreigabe**
Claude zeigt dir alles auf einer Seite: Idee, Namen, Format, Stimme, Look, Testvideo, Kosten, Themen und Zeitplan. Du schreibst einmal **"Freigabe"**, oder sagst, was geändert werden soll. Mit der Freigabe ist der ganze restliche Ablauf freigegeben, Claude fragt dann nur noch, wenn etwas fehlt.

**9. Automatik anlegen**
Nach deiner Projektfreigabe legt Claude die Dateien für deinen Kanal an, richtet die geplanten Aufgaben ein und gibt dir die fertigen Betriebs-Projektanweisungen. Die ersetzen die Start-Anweisungen aus Schritt 3.

**10. Ersten Lauf beobachten**
Am nächsten Abend prüfen, ob das Video im Ordner `erstellt` liegt und du eine Nachricht bekommen hast. Danach: in der TikTok-App den Entwurf im Posteingang öffnen, Caption einfügen und posten.

## Wenn etwas schiefgeht
Die Sitzung stoppt von selbst und schickt dir eine Nachricht mit dem Problem. Du musst nichts reparieren. Antworte Claude in dem Chat, dort wird es gelöst und für alle Kanäle in `LERNEN.md` festgehalten.

## Häufige Fragen
- **Ich habe kein "Use this template".** Der Besitzer muss im Repo unter Settings die Option "Template repository" einschalten.
- **Posten die Videos automatisch?** Nein, bewusst nicht. Das Video kommt als Entwurf in den Posteingang, Caption und Posten machst du selbst. Das schützt dein Konto.
- **Wie viele Videos pro Tag?** Das legst du im Dialog bei "Format" fest.
- **Wie ändere ich später etwas?** Schreibe in deinem Claude-Projekt, was sich ändern soll. Claude passt `projekt.json` an.
