# Blueprint: konstant und variabel

Prinzip: Die Automatik ist für alle Kanäle gleich. Alles, was sich pro Kanal unterscheidet, steht in `projekte/<kanal>/projekt.json`. Es gibt keinen Code, der auf einen bestimmten Kanal zugeschnitten ist.

## Konstante Bausteine (für alle gleich)

| Baustein | Inhalt |
|---|---|
| Ablaufsteuerung | Geplante Sitzungen, ein Video pro Sitzung, Slots aus dem Zeitplan, Reihenfolge der Sitzungen |
| Startroutine | Repo einbinden, klonen, Setup, `GO.md` und `LERNEN.md` lesen |
| Fehlerregel | Erst in `LERNEN.md` nachsehen und bekannte Lösung anwenden. Sonst Stopp, Benachrichtigung, keine weiteren Versuche und Credits |
| Qualitätsprüfung | Inhalt vorab prüfen (vor jeder Ausgabe von Credits), danach Schlüsselbilder prüfen, Zahlen gegen Sprechtext, ehrlich berichten |
| Stimmen-Ablauf | Ein Aufruf zugleich, Status abfragen, Wiederholungsregeln, Blöcke statt Einzelzeilen |
| Schnitt und Zeitachse | Blöcke in Zeilen teilen, Zeitachse erzeugen, Audio zusammenführen, Video rendern |
| Ablage | Drive-Ordner `erstellt` und `gepostet`, alte Datei in den Papierkorb, nie endgültig löschen, Ordner nach dem Upload prüfen |
| Nachricht | Kurze Meldung pro Video mit Dauer und Credits |
| Themennachschub | Zwei Tage vor Listenende neue Vorschläge, Freigabe durch den Nutzer |
| Lernschleife | Neue Lösung kommt in zwei bis drei Sätzen in `LERNEN.md` |

## Variable Bausteine (pro Kanal in `projekt.json`)

| Bereich | Beispiele |
|---|---|
| Kanal | Name, Plattform, Sprache |
| Format | Länge, Videos pro Tag, Seitenverhältnis, Bildrate |
| Konzept | Fragevideo, Erklärvideo, Story, Quiz, Fakten, Ranking |
| Inhaltsquelle | Simulation, Recherche mit Quellen, Stockmaterial, Text-Animation |
| Skriptstruktur | Reihenfolge der Blöcke (z. B. Hook, Setup, Hauptteil, Ergebnis, Schluss), Wortzahl, Zeilen pro Block |
| Look | Farben, Schrift, Layout, Untertitel, Intro und Outro |
| Stimme | Anbieter, Stimme, Modell, Sprache, Ton, Pausen |
| Themenliste | Themen, Reihenfolge, Quelle neuer Ideen |
| Zeitplan | Wochentage, Uhrzeiten, Vorlauf, Startzeit der Sitzungen |
| Zugänge | Repo, Drive-Ordner, Stimmenanbieter, Benachrichtigung |
| Caption | Hashtag-Regeln, Tonalität, Länge |
| Limits | Credit-Grenze pro Video und pro Tag, Wiederholungen |

## Austauschbare Inhaltsstufe

Der schwierigste Teil ist der Inhalt eines Videos. Faktum nutzt eine Simulation. Andere Kanäle brauchen etwas anderes. Darum gibt es eine feste Schnittstelle:

- **Eingabe:** Thema (Eintrag aus `queue.json`) und Skript
- **Ausgabe:** Szenen mit Zeitmarken und Sprechtext, bereit zum Rendern

Dahinter liegt pro Formatart ein Modul in `module/`. Geplant sind zunächst zwei bis drei Vorlagen (Text-und-Bild-Erklärvideo, Zahlen-Animation, Simulation). Weitere kommen, wenn ein Kanal sie braucht.

## Was bewusst nicht automatisch läuft

- **Posten:** Das Posten übernimmt der Nutzer manuell aus der App. Automatisches Posten ist bei TikTok eingeschränkt und riskiert das Konto.
- **Freigabe der Einrichtung:** Ohne Freigabe des Testvideos wird keine Automatik angelegt.
- **Endgültiges Löschen:** Es gibt keins. Dateien wandern in den Drive-Papierkorb.
