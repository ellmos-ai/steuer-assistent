---
name: steuer-assistent
version: 0.2.2
type: service
standalone: true
visibility: public
author: ellmos / BACH Team
created: 2026-06-22
updated: 2026-07-27
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
tags: [steuer, werbungskosten, belege, arbeitsunterlage, offline-first]
description: >
  Erfasst vom Nutzer eingeordnete Belege, summiert Beträge centgenau und
  erzeugt eine lokale, nicht-amtliche Steuer-Arbeitsunterlage. Kein
  ELSTER-Format, keine Steuerberatung und kein Zugriff auf bach.db.
---

# steuer-assistent

> **Öffentliches Modul (MIT).** Reine lokale Selbstanwendung — keine
> Steuerberatung, keine Bewertung der Abziehbarkeit, keine amtliche
> Übermittlung. Die geltende Betriebsform und ihre Grenzen stehen in
> [`README.md`](README.md), Abschnitt „Rechtlicher Rahmen und Betriebsform".

Verwende dieses Modul, wenn:

- Arbeitnehmer-Belege lokal erfasst werden sollen,
- der Nutzer seine Einträge für ein Jahr summieren möchte,
- eine private CSV-/Text-Arbeitsunterlage benötigt wird.

Verwende es nicht, um Abziehbarkeit zu bestätigen, eine Steuererklärung zu
erstellen oder Daten an ELSTER beziehungsweise ein Finanzamt zu übermitteln.

## Trigger

| Formulierung | Aktion |
|---|---|
| „Trage diesen Beleg ein“ | `cli add` |
| „Zeige meine erfassten Werbungskosten“ | `cli werbungskosten` |
| „Erstelle eine private Steuer-Arbeitsunterlage“ | `cli export` |
| „Wie viele Belege habe ich?“ | `cli status` |

## Kategorien

`Arbeitsmittel`, `Fahrtkosten`, `Fortbildung`, `Homeoffice`, `Kommunikation`
und `Sonstiges` sind Eingabegruppen. `aktiv=1` bedeutet nur, dass die Kategorie
im Modul auswählbar ist; es ist keine Aussage zur steuerlichen Anerkennung.

## Daten- und Sicherheitsvertrag

- `datum`: echtes ISO-Datum `YYYY-MM-DD`
- `betrag`: positiv, endlich, maximal zwei Nachkommastellen
- Geldquelle der Summen: `betrag_cent` als Integer
- Belegnummern: monotone Tagessequenz `B-YYYYMMDD-NNN`, transaktional reserviert
- Store, Belegpfade und Exporte: nur innerhalb des Benutzerverzeichnisses
- Notizen und absolute Store-Pfade: standardmäßig nicht in CLI-Ausgaben
- Export: vorhandene Ziele ablehnen, temporär aufbauen, atomar publizieren
- CSV-Textfelder: gegen Formeleinstiege neutralisieren
- keine Netzwerk-, GUI- oder BACH-Laufzeitabhängigkeit

Bestehende 0.1.0-Datenbanken werden beim Öffnen um Cent-Spalten, neutrale
Kategorieaktivität und die Belegsequenz ergänzt. Die ursprüngliche
`betrag_eur`-Spalte bleibt zur Rückwärtskompatibilität erhalten.

## CLI

```powershell
# Beleg hinzufügen
python -m steuer_assistent.cli add --kategorie Arbeitsmittel --betrag 49.90 --datum 2026-03-15

# Liste; Notizen nur mit explizitem Opt-in
python -m steuer_assistent.cli list [--jahr 2026] [--kategorie Arbeitsmittel] [--mit-notiz]

# Vom Nutzer erfasste Werte aggregieren
python -m steuer_assistent.cli werbungskosten --jahr 2026

# Private Arbeitsunterlage; Standardname STEUER_UNTERLAGEN_<jahr>.zip
python -m steuer_assistent.cli export --jahr 2026 [--out <pfad-im-benutzerverzeichnis>.zip]

# Store-Status; Pfad nur mit explizitem Opt-in
python -m steuer_assistent.cli status [--mit-pfad]
```

## Exportinhalt

- `HINWEIS.txt`: Abgrenzung von Steuerberatung und amtlicher Übermittlung
- `belege_<jahr>.csv`: erfasste Werte, UTF-8 mit BOM
- `zusammenfassung_<jahr>.txt`: Summen der vom Nutzer eingeordneten Werte

Das ZIP enthält keine Belegdateien und ist kein ELSTER-/Finanzamt-Format.

## Changelog

| Version | Datum | Änderung |
|---|---|---|
| 0.2.2 | 2026-07-27 | Doku-Pflege: Mermaid-Architekturbild, LLM-Hinweis, Statusangaben dieser Datei auf den öffentlichen Stand gezogen |
| 0.2.1 | 2026-07-24 | `llms.txt`, Discoverability-Metadaten, Badges |
| 0.2.0 | 2026-07-17 | Validierung, Cent-Migration, transaktionale Nummern, privater atomarer Export, CLI-Redaktion |
| 0.1.0 | 2026-06-22 | Initiale Version; aus BACH `agents/_experts/steuer/` extrahiert |
