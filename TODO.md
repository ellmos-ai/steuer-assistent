# TODO — steuer-assistent

## STATUS

| Bereich | Status | Notiz |
|---|---|---|
| Datenschutz | OK | Private Pfade bleiben im Benutzerverzeichnis; CLI redigiert Notizen und absolute Pfade standardmäßig. |
| Datenintegrität | OK | ISO-Datum, positive Cent-Beträge, bekannte Kategorien und monotone transaktionale Belegnummern. |
| Export | OK | Private Arbeitsunterlage, kein amtliches Format; kein Overwrite, temporärer Aufbau, atomare Publikation, CSV-Formelschutz. |
| CLI | OK | Modul- und Script-Entry-Point; sensible Details nur mit `--mit-notiz` beziehungsweise `--mit-pfad`. |
| Review | OK | 2026-07-17: unabhängige PRE-Review; bestätigte Findings behoben, 29/29 Tests grün. |
| Release | BEDINGT FREI | Gutachten 2026-07-23 (`_gutachten/2026-07-23_gutachten_veroeffentlichung.md`): Ampel GRÜN unter 4 Bedingungen (README-Platzhalter raus, nüchterne Außendarstellung, Betriebsform-Trigger dokumentieren, Standard-Gates). StBerG/UWG-Rohbefunde liegen bei. |
| Git/Gate | N/A | Kein eigener Git-Root; Commit und Push sind für diesen lokalen Modulordner nicht anwendbar. |

## Release-Fahrplan „steuer-assistent light" (User-Entscheidung 2026-07-23)

- [ ] Rechtsgutachten via `/rechtsabteilung` (StBerG §§ 2–6 Software-
  Selbstanwendung, UWG-Außendarstellung, Haftungstext) — löst den
  Release-BLOCKED-Status auf.
- [ ] Release-Gates via `/repo-publish-check` (Voll-Modus) → User-Freigabe →
  eigenes Public-Repo (Namens-Kurzcheck GitHub/npm/PyPI für „steuer-assistent").
- [ ] BACH-Integration: Light-Modul in BACH einbauen/verdrahten (Handler
  `hub/steuer.py` bewirbt die Domain bereits; Lücke füllen). WICHTIG:
  im BACH-Dev-Repo NUR LOKAL committen, KEIN Push bis Build-Week-Judging-Ende
  (~12.08.2026, LOCK.user.buildweek-no-push.txt).
- [ ] Abgrenzungs-Hinweis in README: Voll-Pipeline = separates privates
  Produkt (steuer-suite), nicht Teil dieses Moduls.

## Offen

- Rechtliche Einordnung und Haftungstext vor jeder Veröffentlichung extern prüfen.
- Optional `LICENSE`, `CHANGELOG.md` und `SECURITY.md` ergänzen, falls das Modul später eigenständig versioniert wird.
- Private Sichtbarkeit in `.MODULES` beibehalten; bei einer späteren Änderung erneut Datenschutz und Recht prüfen.
