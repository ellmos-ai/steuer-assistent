# Beitragsrichtlinie / Contributing Guide

## Deutsch

Vielen Dank für Ihr Interesse, zu `steuer-assistent` beizutragen!

### Wie Sie beitragen können

1. **Bug melden:** Erstellen Sie ein Issue mit der Vorlage *Bug Report* (Label `bug`).
2. **Feature vorschlagen:** Erstellen Sie ein Issue mit der Vorlage *Feature Request* (Label `enhancement`).
3. **Code beitragen:** Erstellen Sie einen Pull Request.

### Pull-Request-Workflow

1. Forken Sie das Repository auf GitHub.
2. Erstellen Sie einen fokussierten Feature-Branch:
   ```bash
   git checkout -b feature/mein-beitrag
   ```
3. Testen und formatieren Sie Ihre Änderungen lokal:
   ```bash
   python -m compileall steuer_assistent tests
   pytest tests
   ruff check .
   ```
4. Committen Sie Ihre Änderungen mit einer aussagekräftigen Commit-Nachricht:
   ```bash
   git commit -m "feat(scope): kurze beschreibung der aenderung"
   ```
5. Pushen Sie Ihren Branch und eröffnen Sie einen Pull Request gegen `main`.

### Architektur- & Code-Richtlinien

- **Standard-Library-Fokus:** Zero Third-Party Dependencies (`dependencies = []`). Es dürfen keine externen Pakete als Laufzeit-Abhängigkeit eingeführt werden.
- **Cent-Exaktheit (`INV-LOCAL-02`):** Beträge werden intern ausschließlich als ganzzahlige Cents (`betrag_cent`) berechnet und gespeichert.
- **Offline & Zero-Egress (`INV-LOCAL-01`):** Das Modul arbeitet rein lokal und sendet niemals Telemetrie- oder Belegdaten über das Netzwerk.
- **Pfad-Beschränkung (`INV-LOCAL-03`):** Datenbank und Exporte bleiben strikt innerhalb des Benutzerverzeichnisses (`_require_user_path`).
- **Python-Stil:** PEP 8, Typhinweise (`from __future__ import annotations`), UTF-8-Encoding ohne BOM.

---

## English

Thank you for your interest in contributing to `steuer-assistent`!

### How to Contribute

1. **Report bugs:** Open an issue using the *Bug Report* template (label `bug`).
2. **Suggest features:** Open an issue using the *Feature Request* template (label `enhancement`).
3. **Contribute code:** Open a Pull Request.

### Pull Request Workflow

1. Fork the repository on GitHub.
2. Create a focused feature branch:
   ```bash
   git checkout -b feature/my-contribution
   ```
3. Run tests and syntax compilation locally:
   ```bash
   python -m compileall steuer_assistent tests
   pytest tests
   ruff check .
   ```
4. Commit your changes with a descriptive message:
   ```bash
   git commit -m "feat(scope): concise description of changes"
   ```
5. Push your branch and open a Pull Request against `main`.

### Architecture & Code Guidelines

- **Standard Library Core:** Zero third-party dependencies (`dependencies = []`). No external runtime dependencies may be added.
- **Cent-Exact Math (`INV-LOCAL-02`):** Amounts are handled and stored strictly as integer cents (`betrag_cent`).
- **Offline & Zero Egress (`INV-LOCAL-01`):** Completely local execution; never transmits telemetry, credentials, or receipts over the network.
- **Path Confinement (`INV-LOCAL-03`):** Database stores and exports must reside strictly within the user home directory (`_require_user_path`).
- **Python Style:** PEP 8, type hints (`from __future__ import annotations`), UTF-8 encoding.
