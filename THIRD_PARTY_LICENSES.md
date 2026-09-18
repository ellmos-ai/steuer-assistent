# Third-Party Licenses & Software Inventory

- **Project:** `steuer-assistent`
- **License:** [MIT License](LICENSE)
- **Audit Date:** 2026-09-18
- **Repository:** [ellmos-ai/steuer-assistent](https://github.com/ellmos-ai/steuer-assistent)
- **Umbrella Collective:** [open-bricks](https://github.com/open-bricks)

---

## Runtime Architecture & Dependencies

`steuer-assistent` is an offline-first, local-only Python module for personal employee income-related expenses (*Werbungskosten*). It records self-categorized receipts, calculates exact cent sums, and exports private, non-official ZIP worksheets with spreadsheet formula injection protection.

### Mandatory Runtime Dependencies

`steuer-assistent` maintains a **zero external runtime dependency footprint** (`dependencies = []`). The entire runtime execution relies strictly on the official Python Standard Library:

| Package / Module | Version Spec | License | Type | Purpose |
|---|---|---|---|---|
| *Python Standard Library* | `>=3.10` | PSF-2.0 | Built-in | Core runtime: `argparse`, `csv`, `datetime`, `io`, `json`, `os`, `pathlib`, `re`, `shutil`, `sqlite3`, `sys`, `typing`, `zipfile` |

All state persistence is handled entirely via Python's built-in `sqlite3` engine (`~/.steuer-assistent/steuer.db`). Zero third-party telemetry, tracking, or external network egress calls are made.

### Development & Test Tooling

The following tools are utilized exclusively for offline automated testing, code quality auditing, packaging, and linting:

| Package / Tool | Version Spec | License | Scope | Purpose |
|---|---|---|---|---|
| [pytest](https://pytest.org/) | `>=7.0` | MIT | `[dev]` | Automated unit, contract, and metadata test runner |
| [ruff](https://github.com/astral-sh/ruff) | `>=0.1.0` | MIT OR Apache-2.0 | `[dev]` | High-performance Python code style and lint enforcement |
| [setuptools](https://github.com/pypa/setuptools) | `>=68.0` | MIT | `[build-system]` | Standard packaging and build backend |
| [wheel](https://github.com/pypa/wheel) | `>=0.40` | MIT | `[build-system]` | Standard built-package distribution format |

---

## Zero-Copyleft Guarantee & Unprivileged Execution

- **Zero-Copyleft Guarantee:** All runtime code and development dependencies are governed strictly by permissive, business-friendly open-source licenses (MIT, Apache-2.0, PSF-2.0). The codebase contains **zero** GPL, AGPL, or viral copyleft components.
- **Unprivileged User-Mode Operation (`RunAsInvoker`):** All CLI commands, SQLite transactions, and state queries execute purely within unprivileged user space. No administrative rights, root elevation, sudo, or UAC prompts are ever required.

---

## Governance & Runtime Invariants

`steuer-assistent` strictly enforces 10 foundational system and local invariants:

### Local Invariants (INV-LOCAL-01 .. INV-LOCAL-10)

| Invariant | Scope | Guarantee |
|---|---|---|
| `INV-LOCAL-01` | **Zero Network Egress** | Pure offline execution. Stores receipts in `%USERPROFILE%\.steuer-assistent\steuer.db`. Zero network calls, zero analytics, zero cloud sync. |
| `INV-LOCAL-02` | **Cent-Exact Math** | Stores amounts as integer cents (`betrag_cent`) to eliminate floating-point rounding errors. |
| `INV-LOCAL-03` | **Path Confinement** | Database store, linked receipts, and exports are strictly bounded within the user home directory (`_require_user_path`). |
| `INV-LOCAL-04` | **Unprivileged RunAsInvoker** | Requires no root or administrator elevation. |
| `INV-LOCAL-05` | **Privacy-Preserving CLI** | Redacts notes and absolute file paths by default unless `--mit-notiz` or `--mit-pfad` is specified. |
| `INV-LOCAL-06` | **Non-Overwriting Export** | Generates `STEUER_UNTERLAGEN_<jahr>.zip` and strictly refuses to overwrite existing archives. |
| `INV-LOCAL-07` | **CSV Formula Shield** | Neutralizes spreadsheet formula injection by prepending a single quote (`'`) to values starting with `=`, `+`, `-`, or `@`. |
| `INV-LOCAL-08` | **Monotonic Sequence Integrity** | Assigns monotonic daily receipt numbers (`B-YYYYMMDD-XXX`) that are never reused. |
| `INV-LOCAL-09` | **Standard Library Core** | Zero third-party runtime dependencies; standard library Python 3.10+ only. |
| `INV-LOCAL-10` | **Security SLA** | Binding 48-hour response SLA and 5-business-day triage commitment for security disclosures. |
