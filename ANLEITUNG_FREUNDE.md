# Anleitung für Freunde: eigener Video-Kanal auf Autopilot

Entwurf. Die genauen Klickwege in den Einstellungen und die Schritte 6 bis 8 werden nach dem ersten Testlauf mit einem zweiten Kanal überprüft und angepasst.

Du brauchst keine Programmierkenntnisse. Du bekommst deine eigene Kopie der Vorlage, mit deinen eigenen Konten. Nichts wird mit anderen geteilt.

## Was du am Ende hast
Jeden Abend baut Claude automatisch die Videos für den nächsten Tag und legt sie in deinen Google-Drive-Ordner. Du lädst sie nur noch bei TikTok hoch und postest.

## Was du vorher brauchst
- Einen Claude-Zugang mit Projekten und geplanten Aufgaben
- Ein GitHub-Konto (kostenlos)
- Ein ElevenLabs-Konto mit **Bezahlplan** (die Automatik braucht viele Sprachminuten, mit dem Gratisplan stößt du schnell an Grenzen)
- Ein Google-Konto mit Google Drive
- Ein TikTok-Konto, auf dem du selbst postest

Kosten: Hauptsächlich der ElevenLabs-Plan. Frage in der Einrichtung, was ein Video ungefähr kostet, bevor du es freigibst.

## Schritt für Schritt

**1. Konten anlegen**
GitHub, ElevenLabs und Google Drive anlegen, falls du sie noch nicht hast.

**2. Claude mit den Konten verbinden**
In Claude unter Einstellungen die Verbindungen (Connectors) zu GitHub, ElevenLabs und Google Drive einschalten und jeweils anmelden. Wenn sich die Menüs anders nennen, frage Claude: "Wo verbinde ich GitHub?"

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
Claude schlägt Themen vor (du bestätigst) und fragt, an welchen Tagen und Uhrzeiten du posten willst.

**9. Automatik anlegen**
Nach deiner Freigabe legt Claude die Dateien für deinen Kanal an, richtet die geplanten Aufgaben ein und gibt dir die fertigen Projektanweisungen.

**10. Ersten Lauf beobachten**
Am nächsten Abend prüfen, ob das Video im Ordner `erstellt` liegt und du eine Nachricht bekommen hast. Danach: Video aufs Handy, bei TikTok hochladen, posten.

## Wenn etwas schiefgeht
Die Sitzung stoppt von selbst und schickt dir eine Nachricht mit dem Problem. Du musst nichts reparieren. Antworte Claude in dem Chat, dort wird es gelöst und für alle Kanäle in `LERNEN.md` festgehalten.

## Häufige Fragen
- **Ich habe kein "Use this template".** Der Besitzer muss im Repo unter Settings die Option "Template repository" einschalten.
- **Posten die Videos automatisch?** Nein, bewusst nicht. Du postest selbst. Das schützt dein Konto.
- **Wie viele Videos pro Tag?** Das legst du in Schritt 2 des Dialogs fest.
- **Wie ändere ich später etwas?** Schreibe in deinem Claude-Projekt, was sich ändern soll. Claude passt `projekt.json` an.
