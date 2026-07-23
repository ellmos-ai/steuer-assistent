"""Regressionstests fuer Datenintegritaet, Privacy und sichere Exporte."""

from __future__ import annotations

import io
import json
import math
import sqlite3
import sys
import tempfile
import unittest
import zipfile
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing, redirect_stdout
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent.parent))

from steuer_assistent.core import SteuerAssistent, main

ROOT = Path(__file__).parent.parent


class HardeningCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.db_path = self.root / "steuer.db"
        self.sa = SteuerAssistent(self.db_path)
        self.sa.connect()

    def tearDown(self) -> None:
        self.sa.close()
        self.tmp.cleanup()

    def test_add_rejects_unknown_category(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unbekannte Kategorie"):
            self.sa.add_beleg("Privatvergnuegen", 10, datum="2026-01-01")

    def test_add_rejects_invalid_amounts(self) -> None:
        for value in (0, -1, math.nan, math.inf, "1.001", "kein-betrag", 10**100):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    self.sa.add_beleg("Arbeitsmittel", value, datum="2026-01-01")

    def test_add_rejects_invalid_date(self) -> None:
        for value in ("2026-02-30", "01.02.2026", "2026-1-1"):
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, "ISO-Datum"):
                    self.sa.add_beleg("Arbeitsmittel", 10, datum=value)

    def test_money_is_stored_and_aggregated_as_cents(self) -> None:
        for _ in range(10):
            self.sa.add_beleg("Arbeitsmittel", 0.1, datum="2026-01-01")
        agg = self.sa.werbungskosten(2026)
        self.assertEqual(agg["gesamt_eur"], 1.0)
        cents = self.sa.connect().execute(
            "SELECT SUM(betrag_cent) FROM belege"
        ).fetchone()[0]
        self.assertEqual(cents, 100)

    def test_numbers_are_not_reused_after_delete(self) -> None:
        first = self.sa.add_beleg("Arbeitsmittel", 10, datum="2026-01-01")
        second = self.sa.add_beleg("Arbeitsmittel", 10, datum="2026-01-01")
        self.assertTrue(self.sa.delete_beleg(second["nummer"]))
        third = self.sa.add_beleg("Arbeitsmittel", 10, datum="2026-01-01")
        self.assertEqual(first["nummer"], "B-20260101-001")
        self.assertEqual(third["nummer"], "B-20260101-003")

    def test_parallel_writers_get_unique_numbers(self) -> None:
        self.sa.close()

        def add_one(_: int) -> str:
            with SteuerAssistent(self.db_path) as assistant:
                return assistant.add_beleg(
                    "Arbeitsmittel", 1, datum="2026-01-02"
                )["nummer"]

        with ThreadPoolExecutor(max_workers=4) as pool:
            numbers = list(pool.map(add_one, range(8)))
        self.assertEqual(len(set(numbers)), 8)
        self.assertEqual(min(numbers), "B-20260102-001")
        self.assertEqual(max(numbers), "B-20260102-008")

    def test_legacy_real_amounts_are_migrated_to_cents(self) -> None:
        self.sa.close()
        legacy = self.root / "legacy.db"
        with closing(sqlite3.connect(legacy)) as conn:
            conn.executescript(
                """
                CREATE TABLE belege (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nummer TEXT NOT NULL UNIQUE,
                    datum TEXT NOT NULL,
                    kategorie TEXT NOT NULL,
                    betrag_eur REAL NOT NULL,
                    notiz TEXT,
                    beleg_datei TEXT,
                    erstellt_am TEXT NOT NULL DEFAULT (datetime('now'))
                );
                INSERT INTO belege
                    (nummer, datum, kategorie, betrag_eur)
                VALUES ('B-20260101-007', '2026-01-01', 'Arbeitsmittel', 12.34);
                """
            )
            conn.commit()
        with SteuerAssistent(legacy) as migrated:
            row = migrated.connect().execute(
                "SELECT betrag_cent FROM belege WHERE nummer = ?",
                ("B-20260101-007",),
            ).fetchone()
            self.assertEqual(row[0], 1234)
            added = migrated.add_beleg("Arbeitsmittel", 1, datum="2026-01-01")
            self.assertEqual(added["nummer"], "B-20260101-008")

    def test_export_is_neutral_private_bundle_and_formula_safe(self) -> None:
        self.sa.add_beleg(
            "Arbeitsmittel",
            49.9,
            datum="2026-03-15",
            notiz='=HYPERLINK("https://example.invalid")',
        )
        out = self.root / "STEUER_UNTERLAGEN_2026.zip"
        result = self.sa.export_steuerunterlagen(2026, out)
        self.assertEqual(result, out)
        with zipfile.ZipFile(out) as archive:
            self.assertIsNone(archive.testzip())
            self.assertEqual(
                set(archive.namelist()),
                {
                    "HINWEIS.txt",
                    "belege_2026.csv",
                    "zusammenfassung_2026.txt",
                },
            )
            notice = archive.read("HINWEIS.txt").decode("utf-8")
            self.assertIn("kein ELSTER", notice)
            self.assertIn("nicht zur direkten Übermittlung", notice)
            csv_text = archive.read("belege_2026.csv").decode("utf-8-sig")
            self.assertIn("'=HYPERLINK", csv_text)

    def test_export_refuses_overwrite_and_leaves_no_temp_file(self) -> None:
        self.sa.add_beleg("Arbeitsmittel", 10, datum="2026-01-01")
        out = self.root / "STEUER_UNTERLAGEN_2026.zip"
        out.write_bytes(b"bestehend")
        with self.assertRaises(FileExistsError):
            self.sa.export_steuerunterlagen(2026, out)
        self.assertEqual(out.read_bytes(), b"bestehend")
        self.assertEqual(list(self.root.glob(".steuer-export-*.tmp")), [])
        self.assertEqual(self.sa.status()["anzahl_exporte"], 0)

    def test_failed_export_leaves_no_target_or_temp_file(self) -> None:
        self.sa.add_beleg("Arbeitsmittel", 10, datum="2026-01-01")
        out = self.root / "STEUER_UNTERLAGEN_2026.zip"
        with mock.patch.object(zipfile.ZipFile, "writestr", side_effect=OSError("boom")):
            with self.assertRaises(OSError):
                self.sa.export_steuerunterlagen(2026, out)
        self.assertFalse(out.exists())
        self.assertEqual(list(self.root.glob(".steuer-export-*.tmp")), [])
        self.assertEqual(self.sa.status()["anzahl_exporte"], 0)

    def test_store_and_export_must_stay_below_user_home(self) -> None:
        outside = Path(Path.home().anchor) / "steuer-assistent-outside" / "test.db"
        with self.assertRaisesRegex(ValueError, "Benutzerverzeichnis"):
            SteuerAssistent(outside)

        outside_zip = outside.with_suffix(".zip")
        with self.assertRaisesRegex(ValueError, "Benutzerverzeichnis"):
            self.sa.export_steuerunterlagen(2026, outside_zip)

    def test_cli_redacts_notes_and_store_path_by_default(self) -> None:
        self.sa.add_beleg(
            "Arbeitsmittel", 10, datum="2026-01-01", notiz="VERTRAULICHE-NOTIZ"
        )
        self.sa.close()
        list_stdout = io.StringIO()
        with redirect_stdout(list_stdout):
            self.assertEqual(main(["--store", str(self.db_path), "list"]), 0)
        self.assertNotIn("VERTRAULICHE-NOTIZ", list_stdout.getvalue())

        status_stdout = io.StringIO()
        with redirect_stdout(status_stdout):
            self.assertEqual(main(["--store", str(self.db_path), "status"]), 0)
        self.assertNotIn(str(self.db_path), status_stdout.getvalue())


class MetadataContractCase(unittest.TestCase):
    def test_versions_and_private_boundaries_are_synchronized(self) -> None:
        legacy = json.loads((ROOT / "ellmos-module.json").read_text(encoding="utf-8"))
        current = json.loads((ROOT / "ellmos-module.v2.json").read_text(encoding="utf-8"))
        self.assertEqual(legacy["version"], "0.2.0")
        self.assertEqual(current["version"], "0.2.0")
        self.assertEqual(legacy["visibility"], "private")
        self.assertEqual(current["visibility"], "private")
        self.assertEqual(current["boundaries"]["network"], "none")
        self.assertEqual(current["boundaries"]["data"], "sensitive")
        self.assertIn("domain.tax.workpaper_export", current["provides"])

    def test_documentation_does_not_claim_official_export_or_deductibility(self) -> None:
        for name in ("AGENTS.md", "README.md", "SKILL.md", "pyproject.toml"):
            with self.subTest(name=name):
                text = (ROOT / name).read_text(encoding="utf-8")
                self.assertNotIn("FINANZAMT.zip", text)
                self.assertNotIn("1=absetzbar", text)


if __name__ == "__main__":
    unittest.main()
