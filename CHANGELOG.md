# Changelog

Alle nennenswerten Änderungen an `steuer-assistent`. Format angelehnt an
[Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Behoben

- **Installation war auf aktuellen setuptools-Versionen unmöglich.**
  `pyproject.toml` führte neben `license = "MIT"` zusätzlich den Classifier
  `License :: OSI Approved :: MIT License`. Seit PEP 639 schließen sich beide
  aus; setuptools bricht mit `InvalidConfigError` ab, sodass auch der im README
  dokumentierte Weg `pip install -e .` fehlschlug. Classifier entfernt.
  Dahinter lag ein zweiter Baufehler: Ohne `[tool.setuptools] packages` sucht
  setuptools die Pakete selbst und findet im Wurzelverzeichnis zwei Kandidaten
  (`assets/` neben `steuer_assistent/`) — „Multiple top-level packages
  discovered in a flat-layout". Paket jetzt explizit benannt.
- Zwei Tests verglichen Pfade unaufgelöst und schlugen auf Windows fehl, wo
  `tempfile` die 8.3-Kurzform (`C:\Users\RUNNER~1\…`) liefert, das Modul aber
  die aufgelöste Langform. Beide Seiten werden jetzt aufgelöst verglichen.
- Die Tests legten ihre temporären Verzeichnisse über `tempfile` an und setzten
  damit stillschweigend voraus, dass das Temp-Verzeichnis im Benutzerverzeichnis
  liegt — unter Windows zutreffend, unter Linux (`/tmp`) nicht. Dort scheiterten
  sie an der Schutzregel des Moduls selbst. Die Regel bleibt; die Tests legen
  ihre Verzeichnisse jetzt mit `dir=Path.home()` an.
- Versions-Drift zwischen den Versionsträgern beseitigt: `ellmos-module.json`,
  `ellmos-module.v2.json`, `steuer_assistent/__init__.py` und `SKILL.md` standen
  noch auf `0.2.0`, während `pyproject.toml` und `llms.txt` bereits `0.2.2`
  auswiesen.
- `tests/test_hardening.py` prüft die Versionsgleichheit jetzt gegen
  `pyproject.toml` statt gegen ein fest eingetragenes Literal. Ein Literal
  bestätigt jede spätere Drift, statt sie zu melden — genau das war passiert.

### Hinzugefügt

- GitHub-Actions-Workflow `Tests`: pytest auf Linux und Windows unter
  Python 3.10, 3.11 und 3.12. Bewusst ohne Linter.
- `.gitattributes` mit LF-Pin gegen Phantomdiffs auf Windows-Klonen.

### Geändert

- `SKILL.md` auf den öffentlichen Stand gezogen (Sichtbarkeit, Statushinweis,
  Beschreibung); der Kopf wies das Modul noch als privat aus.
- Interne Prozessverweise aus diesem Changelog entfernt (Verweis auf eine
  nicht im Repository liegende Datei, interne Vorgangsnummern und
  Prüfer-Bezeichnungen). Der sachliche Gehalt bleibt erhalten.

## [0.2.2] — 2026-07-27

### Hinzugefügt

- GFM LLM Note Callout (`> [!NOTE]`) für maschinenlesbaren Offline- & Datenschutz-Kontext in `README.md`.
- Mermaid Systemarchitektur-Diagramm in `README.md` zur Visualisierung der lokalen Verarbeitungs- und Export-Pipeline.

### Geändert

- `llms.txt` Last-checked Datum auf `2026-07-27` und Version auf `0.2.2` aktualisiert.
- `pyproject.toml` Version auf `0.2.2` angehoben.
- `steuer_assistent/__init__.py`: Docstring-Hinweis an den öffentlichen Veröffentlichungsstatus angepasst.
- Technische Hygiene und Maintenance-Routine (Path A) & Discoverability Audit (Path B) durchgeführt.

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

- Rechtliche Ersteinschätzung zu StBerG und UWG durchgeführt; Freigabe unter
  Auflagen. Die Einschätzung selbst ist nicht Teil dieses Repositories;
  Geltungsbereich und Grenzen stehen in `README.md`, Abschnitt „Rechtlicher
  Rahmen und Betriebsform".
- README auf öffentliche Erstveröffentlichung vorbereitet: PRIVAT-Platzhalter
  entfernt, Abschnitt „Rechtlicher Rahmen und Betriebsform" ergänzt,
  englische Kurzzusammenfassung vorangestellt.
- `LICENSE`, `CHANGELOG.md`, `SECURITY.md` ergänzt.

### Veröffentlicht (2026-07-23)

- Modul unter MIT veröffentlicht.
- Auflagen aus der vertieften rechtlichen Ersteinschätzung (StBerG, RDG, UWG,
  BGB, DSGVO) vor der Veröffentlichung umgesetzt: Status-Konsistenz zwischen Code-Kommentar
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
