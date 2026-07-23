# Changelog

Alle nennenswerten Änderungen an `steuer-assistent`. Format angelehnt an
[Keep a Changelog](https://keepachangelog.com/).

## [0.2.0] — 2026-07-23

### Geändert

- Interne Geldbeträge zusätzlich als Integer-Cents gespeichert (centgenaue
  Summierung); bestehende `REAL`-Beträge und Belegnummernfolgen werden beim
  Öffnen des Stores automatisch migriert.
- Unabhängige PRE-Review (2026-07-17): bestätigte Findings behoben, 29/29
  Tests grün (`tests/test_module_smoke.py`, `tests/test_hardening.py`).

### Release-Vorbereitung

- Rechtliche Ersteinschätzung (StBerG, UWG) via Modul `law-checker`
  durchgeführt — Ampel GRÜN unter vier Bedingungen (siehe
  `_gutachten/2026-07-23_gutachten_veroeffentlichung.md`, lokal, nicht Teil
  des Repositories).
- README auf öffentliche Erstveröffentlichung vorbereitet: PRIVAT-Platzhalter
  entfernt, Abschnitt „Rechtlicher Rahmen und Betriebsform" ergänzt,
  englische Kurzzusammenfassung vorangestellt.
- `LICENSE`, `CHANGELOG.md`, `SECURITY.md` ergänzt.

## [0.1.0] — 2026-06-22

### Hinzugefügt

- Erste eigenständige Extraktion aus der BACH-Quelle
  `agents/_experts/steuer/` (MIT) als eigenständiges, offline-first Modul
  ohne Zugriff auf `bach.db`.
- CLI (`add`, `list`, `werbungskosten`, `export`, `status`) und Python-API
  (`steuer_assistent.core.SteuerAssistent`).
- Privater ZIP-Export (`STEUER_UNTERLAGEN_<jahr>.zip`) mit CSV,
  Zusammenfassung und Nicht-Amtlichkeits-Hinweis; kein Overwrite bestehender
  Ziele, atomare Publikation, CSV-Formelschutz.
- Datenschutz: Store ausschließlich im Benutzerverzeichnis
  (`%USERPROFILE%\.steuer-assistent\steuer.db`, Override via
  `STEUER_ASSISTENT_DB`), Notizen und absolute Pfade nur mit explizitem
  Opt-in in der CLI-Ausgabe.
