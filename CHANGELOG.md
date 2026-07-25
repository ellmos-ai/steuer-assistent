# Changelog

Alle nennenswerten Änderungen an `steuer-assistent`. Format angelehnt an
[Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Geändert

- `steuer_assistent/__init__.py`: Docstring-Hinweis an den öffentlichen Veröffentlichungsstatus angepasst.
- Technische Hygiene und Maintenance-Routine (Path A) durchgeführt.

## [0.2.1] — 2026-07-24

### Hinzugefügt

- `llms.txt` im Root-Verzeichnis angelegt für verbesserte KI-Agenten-Sichtbarkeit und strukturierte Auffindbarkeit.
- PyPI/GitHub Discoverability-Metadaten in `pyproject.toml` ergänzt (`keywords`, `classifiers`, `project.urls`).
- Shields.io Badges (Python, License, Privacy, Legal Status) und Feature-Übersichtstabelle in `README.md` hinzugefügt.

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

### Veröffentlicht (2026-07-23)

- Nutzerentscheidung D-20260723-020: Veröffentlichung des Moduls; ein
  Codex-Zweitreview wurde vom User als nicht erforderlich entschieden
  (vertieftes Gutachten inkl. Rechtsprechungsschicht und Fremdmodell-Review
  agy/Gemini lag bereits vor).
- Auflagen aus dem vertieften Rechtsgutachten (StBerG, RDG, UWG, BGB, DSGVO)
  vor Public-Schaltung umgesetzt: Status-Konsistenz zwischen Code-Kommentar
  und Modul-Metadaten hergestellt, realistischer Haftungstext in README
  ergänzt, zwei zusätzliche Betriebsform-Trigger dokumentiert (Cloud-Sync/
  Veröffentlichung eigener Nutzerdaten, Installation auf Firmen-/BYOD-
  Rechnern), Secret-/Privacy-Sweep durchgeführt.
- GitHub-Repository `ellmos-ai/steuer-assistent` auf `public` gestellt.

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
