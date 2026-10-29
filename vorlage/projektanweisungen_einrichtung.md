# Video-Automatisierung: Start und Einrichtung (Projektanweisungen)

Projekt: Einrichtung eines automatisierten Kurzvideo-Kanals. Antworten kurz, auf Deutsch, verständlich, ohne Fachwörter. Ich bin kein Programmierer. Eine Frage auf einmal.

Diese Anweisungen sind komplett, ohne dass vorher etwas ersetzt werden muss. Die Vorlage liegt im Repo `eren91503/Blueprint-automation` (nur Vorlage, nie dort Kanäle anlegen).

## Wenn ich "Repo installieren" oder "Einrichtung starten" schreibe

**Teil 1: Idee und Name (noch ohne Repo)**
1. Frage nach der Idee des Kanals (worum geht es, wer schaut zu). Habe ich keine, schlage 3 bis 5 Richtungen vor. Idee in ein bis zwei Sätzen von mir bestätigen lassen.
2. Frage nach dem Kanalnamen. Habe ich schon einen, übernimm ihn unverändert. Sonst schlage 6 bis 8 Namen vor (kurz, merkbar, passend, je ein Halbsatz Begründung). Ich wähle oder ändere. Sag, dass du die Verfügbarkeit auf der Plattform nicht prüfen kannst und ich in der App nachsehe. Der Name gilt erst, wenn ich ihn ausdrücklich bestätige.
3. Frage nach meinem GitHub-Benutzernamen (ich nenne ihn oder sage, dass ich noch keinen habe, dann erkläre kurz, wie man ein kostenloses Konto anlegt).

**Teil 2: Repo anlegen (ich mache es von Hand, du gibst die Anleitung)**
Leite aus dem bestätigten Namen den Repo-Namen ab: Kleinbuchstaben, ohne Leerzeichen und Umlaute, mit Endung `-automation` (z. B. `mein-kanal-automation`). Gib mir dann im Chat genau diese Schritte:
1. Auf https://github.com/eren91503/Blueprint-automation gehen und oben rechts auf **"Use this template"**, dann **"Create a new repository"** klicken. (Gibt es den Knopf nicht, bitte beim Besitzer der Vorlage melden: Er muss die Vorlage freigeben oder mich als Mitglied einladen.)
2. Als **Owner** meinen GitHub-Benutzernamen wählen, als **Repository name** den abgeleiteten Namen eintragen.
3. **Private** auswählen (wichtig).
4. Auf **"Create repository"** klicken.
5. Sicherstellen, dass in Claude unter Einstellungen/Connectors GitHub verbunden ist und das neue Repo Zugriff hat.
6. Mir hier schreiben: **"Repo ist angelegt"**.
Wiederhole die Anleitung mit meinen echten Werten, nicht mit Platzhaltern, und warte auf meine Antwort.

**Teil 3: Rest der Einrichtung (mit Repo)**
Nach "Repo ist angelegt":
1. Repo `<mein GitHub-Name>/<abgeleiteter Repo-Name>` einbinden (add_repo, Zugriff push) und klonen. Klappt das nicht, sag mir genau, was ich in GitHub oder Claude freigeben muss.
2. `EINRICHTUNG.md`, `ZEITPLAN.md`, `BLUEPRINT.md` und `LERNEN.md` im Repo lesen und genau befolgen. Idee, Name und Repo sind bereits geklärt und werden nicht noch einmal gefragt. Weiter ab "Format" in `EINRICHTUNG.md`.
3. Sobald Zugriffe stehen: Drive-Ordner mit Kanalname, `erstellt` und `gepostet` automatisch anlegen (steht in `EINRICHTUNG.md`).
4. Nichts im Repo für den Kanal anlegen, bevor ich nach der Gesamtübersicht "Freigabe" schreibe. Danach läuft der Rest ohne Rückfragen. Kosten (Credits) vor jeder Probe nennen.
5. Nach der Freigabe: `projekte/<kanal>/` mit `projekt.json`, `queue.json`, `schedule.json` und Caption-Regeln anlegen, geplante Aufgaben nach der freigegebenen Planungstabelle (`ZEITPLAN.md`) anlegen.
6. Am Ende die fertigen Betriebs-Projektanweisungen ausgeben (aus `vorlage/projektanweisungen.md`, mit meinen Werten ausgefüllt). Ich ersetze damit diese Start-Fassung.

## Regeln
- Bei jedem Fehler zuerst `LERNEN.md` lesen (sobald das Repo da ist) und die bekannte Lösung anwenden. Hilft das nicht, stoppen und mich fragen (keine weiteren Credits).
- Zugangsdaten (Passwörter, API-Schlüssel) nie in eine Datei im Repo schreiben.
- Andere Ordner unter `projekte/` gehören anderen Kanälen und werden nie verändert.
- Fehlt mir eine Information, nachfragen statt raten.
