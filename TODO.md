# TODO — steuer-assistent

## STATUS

| Bereich | Status | Notiz |
|---|---|---|
| Datenschutz | OK | Private Pfade bleiben im Benutzerverzeichnis; CLI redigiert Notizen und absolute Pfade standardmäßig. |
| Datenintegrität | OK | ISO-Datum, positive Cent-Beträge, bekannte Kategorien und monotone transaktionale Belegnummern. |
| Export | OK | Private Arbeitsunterlage, kein amtliches Format; kein Overwrite, temporärer Aufbau, atomare Publikation, CSV-Formelschutz. |
| CLI | OK | Modul- und Script-Entry-Point; sensible Details nur mit `--mit-notiz` beziehungsweise `--mit-pfad`. |
| Review | OK | 2026-07-17: unabhängige PRE-Review; bestätigte Findings behoben, 29/29 Tests grün. |
| Release | VERÖFFENTLICHT (public) | Nutzerentscheidung D-20260723-020: Veröffentlichung, ohne weitere Zweitmeinung (Codex-Review vom User als nicht erforderlich entschieden). Grundlage: vertieftes Rechtsgutachten 2026-07-23 (StBerG, RDG, UWG, BGB, DSGVO + Rechtsprechungsschicht + Fremdmodell-Review agy/Gemini, Ampel GRÜN unter Auflagen). Auflagen vor Public-Schaltung umgesetzt: Status-Konsistenz (core.py-Kommentar, `ellmos-module.json`/`.v2.json` synchronisiert auf public/released), realistischer Haftungstext in README, zwei zusätzliche Betriebsform-Trigger (Cloud-Sync/Nutzerdaten, Firmen-/BYOD-Installation) ergänzt, Secret-/Privacy-Sweep durchgeführt. |
| Git/Gate | OK | Commit + Push auf `origin/main`, Repo-Sichtbarkeit auf `public` gesetzt und verifiziert. |

## Release-Fahrplan „steuer-assistent light" (User-Entscheidung 2026-07-23)

- [x] Rechtsgutachten via `/rechtsabteilung` (StBerG §§ 2–6 Software-
  Selbstanwendung, UWG-Außendarstellung, Haftungstext) — erledigt 2026-07-23,
  erweitert um RDG/BGB/DSGVO + Rechtsprechungsschicht + Fremdmodell-Review.
- [x] Auflagen aus dem Gutachten umgesetzt und Public-Schaltung vollzogen
  (D-20260723-020, 2026-07-23).
- [ ] BACH-Integration: Light-Modul in BACH einbauen/verdrahten (Handler
  `hub/steuer.py` bewirbt die Domain bereits; Lücke füllen).
- [ ] Abgrenzungs-Hinweis in README: Voll-Pipeline = separates privates
  Produkt (steuer-suite), nicht Teil dieses Moduls.

## Offen

- BACH-Integration (siehe Fahrplan oben).
- Bei Betriebsform-Änderung (siehe README, Abschnitt „Rechtlicher Rahmen und
  Betriebsform") erneute rechtliche Prüfung einholen.
