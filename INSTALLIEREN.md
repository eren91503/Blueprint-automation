# Installieren: Link einfügen, "installiere" schreiben

Die Person fügt den Link dieses Repos (z. B. `https://github.com/eren91503/Blueprint-automation`) in einen Claude-Chat ein und schreibt dazu **"installiere"** (oder "Repo installieren"). Claude macht den Rest. Diese Datei ist die Anleitung für Claude dabei.

Regeln:
- Eine Frage auf einmal, kurz, Deutsch, ohne Fachwörter. Die Person ist kein Programmierer.
- Das Vorlage-Repo (dieses hier) wird nur gelesen und nie verändert. Kanäle entstehen immer in einem **eigenen, neuen privaten Repo** der Person.
- Zugangsdaten nie in Dateien schreiben.

## Ablauf

**0. Vorlage einbinden**
Besitzer und Repo-Name aus dem Link lesen. `add_repo` mit Zugriff `read`, dann klonen (z. B. nach `~/vorlage`). Klappt das nicht (privat, kein Zugriff), sagt Claude genau, was fehlt: Der Besitzer muss die Person als Mitglied einladen oder das Repo öffentlich stellen. Danach Stopp.

**1. Idee**
Worum geht es im Kanal, wer soll zuschauen? Hat die Person keine Idee, 3 bis 5 Richtungen vorschlagen. Idee in ein bis zwei Sätzen bestätigen lassen.

**2. Name des Kanals**
Hat die Person schon einen Namen, wird er unverändert übernommen. Sonst 6 bis 8 Vorschläge (kurz, merkbar, passend, je ein Halbsatz Begründung). Hinweis: Ob der Name auf der Plattform frei ist, kann Claude nicht prüfen, die Person schaut in der App nach. Der Name gilt erst nach ausdrücklicher Bestätigung. Daraus ableiten: Kurzname in Kleinbuchstaben ohne Leerzeichen und Umlaute (`<kanalkurz>`) und Repo-Name `<kanalkurz>-automation`.

**3. Zugriffe prüfen**
Prüfen, ob GitHub, Google Drive und ElevenLabs in Claude verbunden sind und ob in Composio GitHub und Google Drive gekoppelt sind. Fehlt etwas, sagt Claude genau, was die Person verbinden muss (siehe `ANLEITUNG_FREUNDE.md`), und wartet. Den GitHub-Benutzernamen liest Claude in der Composio-Umgebung selbst aus: `proxy_execute("GET", "/user", "github")`, Feld `login`. Er nennt ihn der Person zur Bestätigung ("Ich lege das Repo in deinem GitHub-Konto <login> an, richtig?").

**4. Eigenes Repo anlegen (automatisch)**
In der Composio-Umgebung:
`proxy_execute("POST", "/user/repos", "github", body={"name": "<kanalkurz>-automation", "private": True, "description": "Video-Automatisierung <Kanalname>"})`.
- Existiert der Name schon, nicht überschreiben: der Person den Namen melden und einen anderen vorschlagen.
- Klappt der Aufruf nicht (fehlende Rechte), Rückfall auf die Handarbeit: Claude gibt der Person im Chat die Schritte mit ihren echten Werten (GitHub, oben rechts "+", "New repository", Name, **Private**, "Create repository") und wartet auf "Repo ist angelegt".

**5. Vorlage in das neue Repo kopieren**
`add_repo` für das neue Repo (Zugriff `push`), klonen (z. B. nach `~/kanal`). Den Inhalt der Vorlage ohne `.git` hineinkopieren, committen und pushen. Danach prüfen, dass `GO.md`, `tools/bridge.py` und `vorlage/projekt.json` im neuen Repo ankommen sind. Die Vorlage selbst bleibt unberührt. Im neuen Repo `setup.sh` ausführen (Trockenlauf muss "TROCKENLAUF OK" melden).

**6. Rest der Einrichtung**
Weiter mit `EINRICHTUNG.md` des **neuen** Repos ab Schritt 3 (Format). Idee, Name und Repo sind geklärt. Der Drive-Ordner wird nach der Namensbestätigung automatisch angelegt (siehe `EINRICHTUNG.md`, Schritt 2). Bis zur **Projektfreigabe** (Schritt 10) wird im Repo nichts für den Kanal angelegt, danach läuft der Rest ohne Rückfragen.

**7. Der eine Handgriff zum Schluss**
Claude kann Projektanweisungen nicht selbst setzen. Am Ende gibt er die fertigen Betriebs-Projektanweisungen (aus `vorlage/projektanweisungen.md`, mit den Werten der Person) in einem Kopierblock aus. Die Person legt in Claude ein Projekt an (Name = Kanal), fügt den Text bei "Anweisungen" ein und sagt dann Bescheid. Erst damit starten die geplanten Sitzungen sinnvoll.
