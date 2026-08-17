---
name: steuer-assistent
version: 0.2.3
type: service
standalone: true
visibility: public
author: ellmos / BACH Team
created: 2026-06-22
updated: 2026-08-17
anthropic_compatible: true
status: active
provenance:
  bach_origin: true
  origin_path: agents/_experts/steuer/
  extraction_date: 2026-06-22
  license: MIT
dependencies:
  tools: [python, sqlite3]
  optional: []
  services: []
tags: [tax, income-related-expenses, receipts, worksheet, offline-first]
description: >
  Records user-categorized receipts, sums amounts with exact cent precision, and
  generates a local, non-official tax worksheet bundle. No ELSTER format, no tax advice,
  and no access to bach.db.
---

# steuer-assistent

> **Public Module (MIT).** Pure local self-application tool — no tax advice,
> no assessment of deductibility, no official tax authority transmission.
> The applicable operating mode and its boundaries are documented in
> [`README.md`](README.md), section "Legal Framework and Operating Mode".

Use this module when:

- Employee expense receipts should be recorded locally,
- The user wants to aggregate their entries for a tax year,
- A private CSV/text worksheet package is needed.

Do not use this module to confirm tax deductibility, prepare official tax declarations,
or transmit data to ELSTER or tax authorities.

## Triggers

| Utterance | Action |
|---|---|
| "Record this receipt" | `cli add` |
| "Show my recorded expenses" | `cli werbungskosten` |
| "Create a private tax worksheet package" | `cli export` |
| "How many receipts do I have?" | `cli status` |

## Categories

`Arbeitsmittel`, `Fahrtkosten`, `Fortbildung`, `Homeoffice`, `Kommunikation`,
and `Sonstiges` are user input categories. `aktiv=1` simply indicates that the category
is selectable in the module; it constitutes no statement regarding tax recognition or deductibility.

## Data and Security Contract

- `datum`: valid ISO date `YYYY-MM-DD`
- `betrag`: positive, finite, maximum of two decimal places
- Summation source: `betrag_cent` as integer (cent-exact)
- Receipt numbers: monotonic daily sequence `B-YYYYMMDD-NNN`, transactionally allocated
- Store, receipt paths, and exports: strictly restricted to user home directory
- Notes and absolute store paths: omitted from default CLI output for privacy
- Export: reject existing files (no overwrite), build in temporary file, publish atomically
- CSV text fields: sanitized against spreadsheet formula injection
- Zero network, GUI, or external runtime dependencies

## CLI Usage

```powershell
# Add receipt
python -m steuer_assistent.cli add --kategorie Arbeitsmittel --betrag 49.90 --datum 2026-03-15

# List receipts; notes require explicit opt-in
python -m steuer_assistent.cli list [--jahr 2026] [--kategorie Arbeitsmittel] [--mit-notiz]

# Aggregate user-recorded values
python -m steuer_assistent.cli werbungskosten --jahr 2026

# Export private worksheet; default name STEUER_UNTERLAGEN_<jahr>.zip
python -m steuer_assistent.cli export --jahr 2026 [--out <user-path>.zip]

# Store status; absolute path requires explicit opt-in
python -m steuer_assistent.cli status [--mit-pfad]
```

## Export Bundle Contents

- `HINWEIS.txt`: Clarification of self-application and non-official status
- `belege_<jahr>.csv`: Recorded values, UTF-8 with BOM
- `zusammenfassung_<jahr>.txt`: Summary of user-entered expense totals

The generated ZIP contains no receipt image files and is not an ELSTER or tax office submission format.

## Changelog

| Version | Date | Changes |
|---|---|---|
| 0.2.3 | 2026-08-17 | Ergonomics update (API aliases, `betrag` kwarg), bilingual documentation (`README.md` EN / `README_de.md` DE), PEP 639 setuptools fix |
| 0.2.2 | 2026-07-27 | Documentation maintenance: Mermaid architecture diagram, LLM note callout, public status alignment |
| 0.2.1 | 2026-07-24 | `llms.txt`, discoverability metadata, shields badges |
| 0.2.0 | 2026-07-17 | Validation, cent migration, transactional numbers, private atomic export, CLI redaction |
| 0.1.0 | 2026-06-22 | Initial extraction from BACH `agents/_experts/steuer/` |
