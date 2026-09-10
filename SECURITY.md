# Security Policy — steuer-assistent

`steuer-assistent` is an offline-first, local-only Python module for personal employee income-related expenses (*Werbungskosten*). It executes exclusively on local user hardware with zero network connections, zero cloud uploads, and zero third-party telemetry.

## Supported Versions

| Version | Supported | Notes |
|:---|:---:|:---|
| `0.2.x` | :white_check_mark: | Current active release branch |
| `< 0.2.0` | :x: | Legacy / unmaintained |

## Security & Privacy Invariants

1. **Zero Egress (INV-LOCAL-01):** No network sockets, HTTP requests, or external telemetry are instantiated under any circumstances.
2. **Path Confinement (INV-LOCAL-03):** Database storage, receipt links, and export outputs must strictly reside within the user home directory (`%USERPROFILE%` or `$HOME`). Traversal attempts outside the user home are rejected by `_require_user_path`.
3. **Formula Injection Defense (INV-LOCAL-07):** Exported CSV files sanitize all user-supplied cells starting with spreadsheet formula triggers (`=`, `+`, `-`, `@`) by prepending a single quote (`'`).
4. **Non-Overwriting Export (INV-LOCAL-06):** Export archives refuse to overwrite existing target files, preventing accidental data loss or file clobbering.
5. **Console Privacy Redaction (INV-LOCAL-05):** Receipt notes and absolute store paths are redacted from standard console output unless explicitly requested via `--mit-notiz` or `--mit-pfad`.

## Reporting a Vulnerability

We take the security and privacy of user financial records seriously. If you identify a security vulnerability or privacy violation, please report it through private disclosure channels.

### Preferred Channel
Submit a private advisory via [GitHub Private Vulnerability Reporting](https://github.com/ellmos-ai/steuer-assistent/security/advisories/new).

### Direct Email Contacts
Alternatively, send an encrypted or direct email report to:
- **Project Security:** `security@ellmos.ai`
- **Umbrella Security:** `security@open-bricks.org`
- **Maintainer Escalation:** `lukas@open-bricks.org` / `support@lukasgeiger.com`

### Response Service Level Agreement (SLA)
- **Initial Response:** Within **48 hours** acknowledging receipt of your report.
- **Triage & Severity Assessment:** Within **5 business days** with status update.
- **Coordinated Disclosure:** Security patches are released promptly, followed by a public advisory crediting the reporter (if desired).

Please include reproduction steps, affected environment/version, and an assessment of the security impact. Please do not open public GitHub issues for security vulnerabilities.
