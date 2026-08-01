![steuer-assistent Banner](assets/banner.png)

# steuer-assistent

[![Tests](https://github.com/ellmos-ai/steuer-assistent/actions/workflows/tests.yml/badge.svg)](https://github.com/ellmos-ai/steuer-assistent/actions/workflows/tests.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Privacy: Offline--First](https://img.shields.io/badge/Privacy-Offline--First-green.svg)](#store-und-datenschutz)
[![Legal: Non--Official](https://img.shields.io/badge/Status-Private--Worksheet-orange.svg)](#rechtlicher-rahmen-und-betriebsform)

*Lokale Beleg-Arbeitsunterlage für Arbeitnehmer-Werbungskosten — keine Steuerberatung.*

**Local receipt worksheet for employee tax records — not tax advice.**
A small, offline-first Python module that lets you record self-categorized
receipts for employee income-related expenses (*Werbungskosten*), sum them
to the cent, and export a private, non-official ZIP worksheet. It does not
assess deductibility and does not create or submit a tax return.

Das Modul erfasst vom Nutzer eingeordnete Angaben, summiert sie centgenau und
erzeugt ein privates ZIP. Es prüft weder die steuerliche Abziehbarkeit noch
erstellt oder übermittelt es eine Steuererklärung.

Die offizielle elektronische Übermittlung erfolgt über ELSTER beziehungsweise
dafür zugelassene Software. ELSTER weist außerdem darauf hin, dass bloß in
„Meine Belege“ erfasste Dokumente noch nicht an das Finanzamt übermittelt sind:
[ELSTER-Belegverwaltung](https://portal.elster.de/eportal/helpGlobal?themaGlobal=help_meine_belege),
[ELSTER-Belegnachreichung](https://www.elster.de/eportal/formulare-leistungen/alleformulare/belegnachreichung).

> [!NOTE]
> **Offline-First & Local-Only Architecture**: `steuer-assistent` is a purely offline receipt worksheet module (`.steuer-assistent/steuer.db`). Zero network calls, zero cloud dependencies, cent-exact math (integer cents), and privacy-preserving CLI defaults.

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

## Überblicks-Features

| Feature | Beschreibung |
|---|---|
| **Offline-First & Lokal** | Datenbank ausschließlich im Benutzerverzeichnis (`%USERPROFILE%\.steuer-assistent\steuer.db`). Keine Netzverbindung. |
| **Cent-genaue Arithmetik** | Beträge werden intern als Integer-Cents gespeichert, um Fließkomma-Rundungsfehler auszuschließen. |
| **Datenschutz-CLI** | Notizen und absolute Pfade werden in der Konsole standardmäßig ausgeblendet und erfordern ein Opt-in (`--mit-notiz`). |
| **Arbeitsunterlagen-Export** | Erstellt `STEUER_UNTERLAGEN_<jahr>.zip` mit CSV, Zusammenfassung & CSV-Formelschutz. Überschreibt niemals bestehende Exporte. |
| **Standardkonform** | Benötigt nur Python 3.10+ und die Standardbibliothek (`sqlite3`). Keine externen Pip-Abhängigkeiten. |

## Verwendung

| Schritt | Befehl |
|---|---|
| Beleg erfassen | `python -m steuer_assistent.cli add --kategorie Arbeitsmittel --betrag 49.90 --datum 2026-03-15 --notiz "USB-Hub"` |
| Belege ohne Notizen anzeigen | `python -m steuer_assistent.cli list` |
| Notizen bewusst anzeigen | `python -m steuer_assistent.cli list --mit-notiz` |
| Erfasste Werbungskosten summieren | `python -m steuer_assistent.cli werbungskosten --jahr 2026` |
| Private Arbeitsunterlage erzeugen | `python -m steuer_assistent.cli export --jahr 2026` |
| Status ohne Store-Pfad | `python -m steuer_assistent.cli status` |

Der Standardexport heißt `STEUER_UNTERLAGEN_<jahr>.zip`. Vorhandene Ziele
werden nicht überschrieben. Das ZIP enthält CSV, Zusammenfassung und einen
Hinweis zur Nicht-Amtlichkeit, aber keine eigentlichen Belegdateien.

## Store und Datenschutz

- Standard: `%USERPROFILE%\.steuer-assistent\steuer.db`
- Override: `STEUER_ASSISTENT_DB=<Pfad>` oder `--store <Pfad>`
- Store, Belegpfade und Exporte müssen kanonisch im Benutzerverzeichnis liegen.
- Geld wird intern zusätzlich als Integer-Cents gespeichert; Version 0.2.0
  migriert vorhandene `REAL`-Beträge und bestehende Nummernfolgen automatisch.
- Notizen und absolute Pfade erscheinen in der CLI nur mit explizitem Opt-in.
- Das Modul versucht restriktive Dateimodi zu setzen; maßgeblich bleiben die
  Zugriffsrechte und Sicherungseinstellungen des Betriebssystems.
- Keine Netzwerkverbindung, kein Cloud-Upload, kein Zugriff auf `bach.db`.

Tabellen: `belege`, `beleg_sequences`, `werbungskosten_kategorien`,
`export_runs`.

## Installation und Prüfung

```powershell
cd <pfad-zum-modul>\steuer-assistent
python -m pip install -e .
python -B -m pytest tests -q -p no:cacheprovider
```

## Grenzen

- Scope: private Arbeitsunterlage für Arbeitnehmer-Werbungskosten;
  kein Gewerbe-/Betriebsausgaben-Workflow
- keine Steuerberatung, Rechtsprüfung oder Anerkennungsentscheidung
- kein ELSTER-, ERiC- oder amtliches Finanzamt-Format
- keine direkte Beleg- oder Steuerdatenübermittlung
- BACH-Quelle `agents/_experts/steuer/` wird nicht zur Laufzeit gelesen
- Separates, eigenständiges Produkt (nicht Teil dieses Moduls): eine
  kommerzielle Voll-Pipeline „steuer-suite" befindet sich in Vorbereitung
  und unterliegt einer eigenen rechtlichen Prüfung, sobald sie existiert.

## Rechtlicher Rahmen und Betriebsform

**Keine Steuerberatung.** Dieses Modul ist ein reines Selbstanwendungs-Werkzeug:
Es erfasst und summiert vom Nutzer selbst eingeordnete Belege, trifft aber
keine steuerliche Bewertung und übernimmt keine Gewähr für ein steuerliches
Ergebnis. Nutzung erfolgt auf eigene Verantwortung; die Gewährleistung
richtet sich — unabhängig vom MIT-Lizenztext — nach dem gesetzlich
zwingenden Umfang (Vorsatz und grobe Fahrlässigkeit bleiben nach deutschem
Recht stets haftungsbewehrt, siehe §§ 276 Abs. 3, 309 Nr. 7 lit. b BGB).

KI-gestützte Ersteinschätzung (kein Ersatz für anwaltliche Beratung, nicht
abschließend anwaltlich geprüft), Stand 2026-07-23: Für die aktuelle
Betriebsform — reine Selbstanwendung auf lokal gehaltene, vom Nutzer selbst
eingeordnete Daten, ohne Netzwerkverbindung, ohne Rechtsprüfung des
Einzelfalls — ist dieses Modul nach den einschlägigen Vorschriften des
Steuerberatungsgesetzes (StBerG, insbes. § 2 Abs. 2) und des
Rechtsdienstleistungsgesetzes (RDG, insbes. § 2 Abs. 1) keine
„geschäftsmäßige Hilfeleistung in Steuersachen" bzw. Rechtsdienstleistung.
Grundlage ist eine vertiefte interne Prüfung (StBerG, RDG, UWG, BGB, DSGVO,
mit Rechtsprechungsschicht und Fremdmodell-Review); sie ist nicht Teil
dieses Repositories.

**Diese Einschätzung gilt nur für die beschriebene Betriebsform.** Eine
erneute rechtliche Prüfung ist nötig, sobald sich die Betriebsform ändert —
insbesondere bei:

1. **automatischer steuerlicher Einordnung oder Würdigung** durch das Tool
   selbst (statt reiner Nutzereingabe),
2. **Hosting- oder Servicebetrieb**, oder Bearbeitung fremder Belege durch
   den Betreiber (statt lokaler Selbstanwendung),
3. **ELSTER-, ERiC- oder sonstiger amtlicher Übermittlungsanbindung**,
4. **entgeltlicher Vermarktung** dieses Moduls oder einer daraus
   abgeleiteten Voll-Pipeline (z. B. „steuer-suite"),
5. **Cloud-Sync oder sonstiger Veröffentlichung erfasster Nutzerdaten durch
   den Nutzer selbst** (z. B. öffentliches Repository der eigenen
   Datenbank) — die DSGVO-Haushaltsausnahme (Art. 2 Abs. 2 lit. c DSGVO)
   kann dann beim jeweiligen Nutzer entfallen,
6. **Installation auf Firmen-/BYOD-Rechnern zur Abrechnung dienstlicher
   (fremder) Spesen** — auch hier kann die DSGVO-Haushaltsausnahme beim
   Nutzer entfallen, unabhängig vom Autor.

Bei Zweifeln oder vor produktivem Einsatz mit echten Steuerdaten Dritter
empfiehlt sich eine unabhängige anwaltliche Prüfung.

## Origin

- BACH-Substanz: `agents/_experts/steuer/` (MIT)
- Extraktion: 2026-06-22
- Dieses private Modul: MIT

## Lizenz

MIT — siehe [`LICENSE`](LICENSE). Änderungen: siehe [`CHANGELOG.md`](CHANGELOG.md).
Sicherheitsmeldungen: siehe [`SECURITY.md`](SECURITY.md).
