# AGENTS.md — steuer-assistent

> Öffentliches Modul (MIT). Siehe README.md, Abschnitt „Rechtlicher Rahmen
> und Betriebsform" für die geltende Betriebsform und deren Grenzen.

Regeln für alle Agenten, die dieses Modul bearbeiten:

- Lies `README.md`, `SKILL.md` und `ellmos-module.json` vor jeder Änderung.
- **Niemals** auf `bach.db` oder BACH-Laufzeitpfade zugreifen.
- Der Store liegt unter `%USERPROFILE%\.steuer-assistent\steuer.db`
  (Env-Override: `STEUER_ASSISTENT_DB`). Kein hardcodierter Nutzerpfad.
- Userneutral bleiben: keine festen Windows-Nutzernamen, keine absoluten
  Pfade außerhalb des User-Home-Verzeichnisses.
- Scope: Arbeitnehmer-Werbungskosten. Kein Gewerbe, kein Betriebsausgaben-Workflow.
- Kategorien und Summen sind Nutzereingaben, keine Aussage zur steuerlichen Abziehbarkeit.
- Exporte sind private Arbeitsunterlagen, keine ELSTER-/Finanzamt-Übermittlungsformate.
- Keine Netzwerkverbindungen (offline-first).
- Kein GUI — headless CLI und Python-API.
- Nach Änderungen: `python -m compileall steuer_assistent` und Tests ausführen.
- Keine `__pycache__`-Verzeichnisse committen (`PYTHONDONTWRITEBYTECODE=1`).

## Rollen

| Rolle | Zuständigkeit |
|---|---|
| **Beleg-Agent** | Belege erfassen, validieren, B-Nummer vergeben |
| **Analyse-Agent** | Werbungskosten aggregieren, Kategorien prüfen |
| **Export-Agent** | Private Steuer-Arbeitsunterlage mit Hinweis, CSV und Zusammenfassung erstellen |
