# <Kanalname>: Projektanweisungen

Projekt: <Plattform> <@Kanalname>. <Ein Satz, worum es geht>. <Länge> pro Video, <Anzahl> Videos pro Tag. Antworten kurz, auf <Sprache>, verständlich. Ich bin kein Programmierer.

## Wie es läuft
- Ich tippe nichts. Geplante Sitzungen bauen jeden Abend die Videos für den Folgetag: Sitzung A (ca. <Uhrzeit>) das erste, Sitzung B (ca. <Uhrzeit>) das zweite. Jedes Video läuft in einer eigenen Sitzung aus diesem Projekt.
- Plan: `projekte/<kanal>/schedule.json` und `projekte/<kanal>/queue.json` im Repo <GitHub-Name>/<Repo-Name>.
- Fertige Videos kommen ohne meine Freigabe in Drive: <Ordnerpfad>/erstellt. Die alte Datei gleichen Namens außerhalb von erstellt und gepostet kommt in den Drive-Papierkorb (nie endgültig löschen). Ich bekomme eine kurze Nachricht mit Dauer und Credits.
- Ich poste manuell aus der App.
- Bei einem Problem schaut die Sitzung zuerst in LERNEN.md. Hilft das nicht, stoppt sie sofort und benachrichtigt mich (keine weiteren Versuche, keine weiteren Credits).
- Neue Themen: <Tage> Tage vor Ende der Liste schlägt eine geplante Aufgabe <Anzahl> Themen vor und wartet auf mein OK.
- Kurzbefehle nur für Sonderfälle: "<Name> neu" = bestehendes Video nur neu vertonen. "Go" = nächstes offenes Thema bauen.

## Start jeder Sitzung (immer zuerst, ohne Rückfrage)
1. Repo <GitHub-Name>/<Repo-Name> einbinden (add_repo, Zugriff push), klonen, setup.sh ausführen.
2. GO.md und LERNEN.md lesen und genau befolgen. Die Konfiguration steht in `projekte/<kanal>/projekt.json`.
3. Design, Pipeline und Videostandard nicht ändern.

## Stimme
<Anbieter>, Stimme <Name> (voice_id <ID>), Modell <Modell>, generations_count 1. Text nicht kürzen. Immer nur EIN Aufruf gleichzeitig. Wiederholungsregeln: siehe LERNEN.md.

## Qualität
Vor dem Vertonen den Inhalt prüfen. Ergebnisse ehrlich berichten. Nach dem Rendern nur eine Übersicht mit 2 bis 3 Schlüsselbildern prüfen und Zahlen im Bild mit dem Sprechtext abgleichen.

## Fehler und Lernen
Tritt ein neuer Fehler auf, löse ihn in dieser Sitzung und trage die Lösung in zwei bis drei Sätzen in LERNEN.md ein (committen und pushen). Keine langen Fehlersuchen im Chat: nach zwei erfolglosen Versuchen kurz melden, was geht und was nicht.
