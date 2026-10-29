# Blueprint-automation

Vorlage für automatisierte Kurzvideo-Kanäle (TikTok, Reels, Shorts). Einmal gemeinsam mit Claude einrichten, danach baut die Automatik jeden Abend die Videos für den Folgetag.

Abgeleitet aus dem Workflow des Kanals Faktum. Faktum selbst bleibt unverändert und liegt in einem eigenen Repo. Hier steht nur das Allgemeine, ohne Zugangsdaten und ohne Faktum-Inhalte.

## Wie es funktioniert

1. **Einrichtung (einmalig, im Dialog):** Idee, Format, Stimme, Look, Themenliste, Zeitplan. Ein Testvideo wird gebaut und freigegeben. Siehe `EINRICHTUNG.md`.
2. **Betrieb (automatisch):** Geplante Sitzungen lesen `projekte/<kanal>/projekt.json` und bauen pro Sitzung ein Video. Ablauf siehe `GO.md`.
3. **Lernen:** Jeder Fehler und seine Lösung steht in `LERNEN.md`. Die Automatik schaut dort zuerst nach und löst bekannte Fehler selbst.

## Ordner

| Pfad | Inhalt |
|---|---|
| `BLUEPRINT.md` | Konzept: was konstant ist, was variabel |
| `EINRICHTUNG.md` | Fragenablauf für die Einrichtung mit Claude |
| `GO.md` | Betriebsanleitung für die Automatik (gilt für alle Kanäle) |
| `ZEITPLAN.md` | Abfrage der Zeiten (posten, fertig bis, Bauzeit) und Ableitung der geplanten Aufgaben |
| `LERNEN.md` | Bekannte Fehler und Lösungen, wächst mit jedem Lauf |
| `ANLEITUNG_FREUNDE.md` | Schritt für Schritt für Leute mit eigenen Konten |
| `vorlage/` | Leere Vorlagen: `projekt.json`, `queue.json`, `schedule.json`, Caption-Regeln, Projektanweisungen (erst die Einrichtungs-Fassung, nach der Freigabe die Betriebs-Fassung) |
| `projekte/<kanal>/` | Pro Kanal: Konfiguration, Themenliste, Zeitplan (entsteht bei der Einrichtung) |
| `module/` | Austauschbare Inhaltsstufen pro Videoformat. Vorhanden: `erklaervideo_text_bild` |

## Stand

Konzept, Anleitungen und ein erstes Inhaltsmodul (`erklaervideo_text_bild`) stehen. Das Modul ist mit Platzhalter-Ton geprüft, noch nicht mit einer echten Stimme. Noch offen: Zerschneiden der Stimmen-Blöcke in Zeilen, die Hilfsdateien für Composio (Audio, Video, TikTok-Upload), `setup.sh` und ein kompletter Durchlauf mit einem Testkanal. Was sich im Test als falsch herausstellt, wird in `LERNEN.md` und den Anleitungen korrigiert.
