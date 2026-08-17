![steuer-assistent Banner](assets/banner.png)

# steuer-assistent

[🇩🇪 Deutsche Version](README_de.md)

[![Tests](https://github.com/ellmos-ai/steuer-assistent/actions/workflows/tests.yml/badge.svg)](https://github.com/ellmos-ai/steuer-assistent/actions/workflows/tests.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Privacy: Offline--First](https://img.shields.io/badge/Privacy-Offline--First-green.svg)](#store-and-data-privacy)
[![Legal: Non--Official](https://img.shields.io/badge/Status-Private--Worksheet-orange.svg)](#legal-framework-and-operating-mode)

*Local receipt worksheet for employee income-related expenses — not tax advice.*

A lightweight, offline-first Python module for recording self-categorized receipts for employee income-related expenses (*Werbungskosten*), computing exact cent sums, and exporting private, non-official ZIP worksheet packages. It does not assess tax deductibility, nor does it prepare or submit tax returns.

Official electronic submission in Germany must be conducted via ELSTER or officially approved tax software. Note that documents uploaded to ELSTER's "Meine Belege" are not automatically submitted to the tax authorities until actively attached to an official declaration:
[ELSTER Document Management](https://portal.elster.de/eportal/helpGlobal?themaGlobal=help_meine_belege),
[ELSTER Document Submission](https://www.elster.de/eportal/formulare-leistungen/alleformulare/belegnachreichung).

> [!NOTE]
> **Offline-First & Local-Only Architecture**: `steuer-assistent` is a purely offline receipt worksheet module (`~/.steuer-assistent/steuer.db`). Zero network calls, zero cloud dependencies, cent-exact math (integer cents), and privacy-preserving CLI defaults.

## Architecture

```mermaid
flowchart TD
    subgraph Input["User Interaction"]
        CLI["CLI (steuer_assistent.cli)"]
        API["Python API (SteuerAssistent)"]
    end

    subgraph CoreEngine["Core Engine & Security"]
        Cents["Cent-Exact Math (Integer Cents)"]
        Redact["CLI Privacy Redactor (--mit-notiz opt-in)"]
        HomeCheck["Home Directory Bounds Enforcer"]
    end

    subgraph Storage["Local Storage"]
        DB[("SQLite Database<br/>~/.steuer-assistent/steuer.db")]
    end

    subgraph Output["Worksheet Export"]
        ZIP["Private ZIP Package<br/>STEUER_UNTERLAGEN_<jahr>.zip<br/>(CSV + Summary + Formula Shield)"]
    end

    CLI --> HomeCheck
    API --> HomeCheck
    HomeCheck --> Cents
    Cents --> DB
    DB --> Redact
    DB --> ZIP
```

## Key Features

| Feature | Description |
|---|---|
| **Offline-First & Local** | Storage strictly restricted to user home directory (`%USERPROFILE%\.steuer-assistent\steuer.db`). Zero network calls. |
| **Cent-Exact Math** | Amounts are stored internally as integer cents to eliminate floating-point rounding inaccuracies. |
| **Privacy-Preserving CLI** | Notes and absolute file paths are redacted by default in console output and require explicit opt-in (`--mit-notiz`, `--mit-pfad`). |
| **Worksheet ZIP Export** | Generates `STEUER_UNTERLAGEN_<jahr>.zip` with CSV (UTF-8 BOM), structured text summary, and spreadsheet formula injection protection. Never overwrites existing files. |
| **Standard Library Only** | Requires only Python 3.10+ and standard library modules (`sqlite3`). Zero third-party runtime dependencies. |

## Usage

### Command Line Interface (CLI)

| Action | Command |
|---|---|
| Add receipt | `python -m steuer_assistent.cli add --kategorie Arbeitsmittel --betrag 49.90 --datum 2026-03-15 --notiz "USB-Hub"` |
| List receipts without notes | `python -m steuer_assistent.cli list` |
| List receipts with notes | `python -m steuer_assistent.cli list --mit-notiz` |
| Aggregate expenses for a year | `python -m steuer_assistent.cli werbungskosten --jahr 2026` |
| Export private worksheet | `python -m steuer_assistent.cli export --jahr 2026` |
| Show status without DB path | `python -m steuer_assistent.cli status` |
| Show status with full DB path | `python -m steuer_assistent.cli status --mit-pfad` |

The default export file is named `STEUER_UNTERLAGEN_<jahr>.zip`. Existing target files are never overwritten. The ZIP archive contains a CSV export, a text summary, and a legal notice clarifying non-official status, but no original receipt image files.

### Python API

```python
from steuer_assistent.core import SteuerAssistent

with SteuerAssistent() as sa:
    # Add a receipt entry
    sa.add_beleg(
        kategorie="Arbeitsmittel",
        betrag=49.90,
        datum="2026-03-15",
        notiz="USB-Hub",
    )

    # Calculate recorded expenses
    agg = sa.get_werbungskosten(jahr=2026)
    print(f"Total 2026: {agg['gesamt_eur']:.2f} EUR")

    # Export private worksheet package
    export_zip = sa.export_arbeitsunterlage(jahr=2026)
    print(f"Exported to: {export_zip}")
```

## Store and Data Privacy

- **Default Location**: `%USERPROFILE%\.steuer-assistent\steuer.db`
- **Configuration Override**: Environment variable `STEUER_ASSISTENT_DB=<path>` or `--store <path>` argument.
- **Path Confinement**: Database store, linked receipt paths, and export files must reside strictly inside the user's home directory (`_require_user_path`).
- **Currency Storage**: Amounts are stored as integer cents (`betrag_cent`); existing legacy databases are automatically migrated on startup.
- **CLI Redaction**: Sensitive notes and absolute paths are redacted from CLI output unless explicitly requested.
- **File Permissions**: Restrictive filesystem permissions are applied (`0600`/`0700` on POSIX; user profile ACLs on Windows).
- **Isolation**: Zero network requests, zero cloud syncing, zero access to external databases.

Database schema: `belege`, `beleg_sequences`, `werbungskosten_kategorien`, `export_runs`.

## Installation and Testing

```powershell
cd steuer-assistent
python -m pip install -e .
python -B -m pytest tests -q -p no:cacheprovider
```

## Scope and Boundaries

- **Scope**: Private worksheet preparation for employee income-related expenses; no commercial or business expense workflows.
- **No Tax Advice**: No legal review, no deductibility assessment, and no individual tax consulting.
- **No Official Format**: Not an ELSTER, ERiC, or tax authority submission package.
- **No Transmission**: No automated or direct transmission to government agencies.
- **Independence**: Fully self-contained standard library tool with zero external framework runtime dependencies.

## Legal Framework and Operating Mode

**No Tax Advice.** This module is a pure self-application utility: it records and sums receipts categorized by the user, but performs no tax evaluation and provides no guarantees regarding tax recognition or deductibility. Use is at your own risk; statutory mandatory liability provisions apply under applicable law (liability for intentional misconduct and gross negligence cannot be excluded under German law pursuant to §§ 276 para. 3, 309 no. 7 lit. b BGB).

AI-assisted initial legal assessment (as of 2026-07-23, not a substitute for formal legal counsel): For the current operating mode — pure self-application on locally held data categorized solely by the user, without network communication or legal evaluation of individual cases — this tool does not constitute commercial assistance in tax matters (*geschäftsmäßige Hilfeleistung in Steuersachen*) under the German Tax Advisory Act (StBerG, esp. § 2 para. 2) or legal services under the Legal Services Act (RDG, esp. § 2 para. 1).

**This assessment applies exclusively to the described operating mode.** A new legal assessment is required if the operating mode changes — particularly in case of:

1. **Automated tax classification or evaluation** by the software itself (rather than user categorization),
2. **Hosted multi-user or service operation**, or processing third-party receipts (rather than local self-use),
3. **ELSTER, ERiC, or official tax authority submission interfaces**,
4. **Commercial marketing or paid distribution** of this module or derived pipelines,
5. **Cloud synchronization or public distribution of user database files** (which may void the GDPR household exemption under Art. 2 para. 2 lit. c GDPR),
6. **Installation on enterprise / BYOD workstations for processing employer expenses** (which may also impact GDPR household exemption applicability).

## Origin

- **Origin**: Extracted from BACH `agents/_experts/steuer/` (MIT)
- **Extraction Date**: 2026-06-22
- **License**: MIT

## License

MIT — see [`LICENSE`](LICENSE). Changes: see [`CHANGELOG.md`](CHANGELOG.md).
Security policies: see [`SECURITY.md`](SECURITY.md).
