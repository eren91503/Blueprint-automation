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
| `LERNEN.md` | Bekannte Fehler und Lösungen, wächst mit jedem Lauf |
| `ANLEITUNG_FREUNDE.md` | Schritt für Schritt für Leute mit eigenen Konten |
| `vorlage/` | Leere Vorlagen: `projekt.json`, `queue.json`, `schedule.json`, Caption-Regeln, Projektanweisungen |
| `projekte/<kanal>/` | Pro Kanal: Konfiguration, Themenliste, Zeitplan (entsteht bei der Einrichtung) |
| `module/` | Austauschbare Inhaltsstufen pro Videoformat (entsteht beim ersten Testprojekt) |

## Stand

Konzept und Anleitungen stehen. Noch nicht getestet: die Einrichtung mit einem zweiten Kanal und die Inhaltsmodule. Was sich im Test als falsch herausstellt, wird in `LERNEN.md` und den Anleitungen korrigiert.
