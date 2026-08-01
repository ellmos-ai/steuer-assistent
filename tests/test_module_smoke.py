"""
test_module_smoke.py — Smoke + Unit-Tests für steuer-assistent
==============================================================

Kein BACH-Import, kein Netzwerk. Env-Override auf tempdir → sauberer Teardown.
"""

import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

# Modul aus dem Eltern-Verzeichnis laden (editable install nicht voraussetzen)
sys.path.insert(0, str(Path(__file__).parent.parent))

from steuer_assistent.core import SteuerAssistent, _store_path


class TestStorePath(unittest.TestCase):
    def test_env_override(self):
        # dir=Path.home(): Das Modul laesst den Store nur innerhalb des
        # Benutzerverzeichnisses zu (_require_user_path). Unter Windows liegt
        # das Temp-Verzeichnis dort, unter Linux in /tmp -- also ausserhalb.
        with tempfile.TemporaryDirectory(dir=Path.home()) as td:
            # Aufgeloest: _store_path() loest den Pfad auf, tempfile liefert
            # auf Windows teilweise die 8.3-Kurzform. Ohne resolve() vergleicht
            # der Test Kurz- gegen Langform desselben Verzeichnisses.
            db = str(Path(td).resolve() / "test.db")
            os.environ["STEUER_ASSISTENT_DB"] = db
            try:
                self.assertEqual(_store_path(), Path(db))
            finally:
                del os.environ["STEUER_ASSISTENT_DB"]

    def test_default_under_home(self):
        os.environ.pop("STEUER_ASSISTENT_DB", None)
        p = _store_path()
        self.assertIn(".steuer-assistent", str(p))


class TestCliEntrypoint(unittest.TestCase):
    def test_module_cli_help(self):
        env = dict(os.environ)
        env["PYTHONIOENCODING"] = "utf-8"
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        result = subprocess.run(
            [sys.executable, "-X", "utf8", "-m", "steuer_assistent.cli", "--help"],
            cwd=Path(__file__).parent.parent,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Private Beleg-Arbeitsunterlage", result.stdout)


class TestSteuerAssistentCRUD(unittest.TestCase):
    def setUp(self):
        # dir=Path.home(): siehe Kommentar in test_env_override -- das Modul
        # laesst den Store nur im Benutzerverzeichnis zu, /tmp liegt dort nicht.
        self.td = tempfile.mkdtemp(dir=Path.home())
        self.db_path = Path(self.td).resolve() / "steuer_test.db"
        self.sa = SteuerAssistent(db_path=self.db_path)
        self.sa.connect()

    def tearDown(self):
        self.sa.close()
        import shutil
        shutil.rmtree(self.td, ignore_errors=True)

    # ------------------------------------------------------------------
    # Store-Init
    # ------------------------------------------------------------------

    def test_store_init_creates_db(self):
        self.assertTrue(self.db_path.exists())

    def test_kategorien_seeded(self):
        conn = self.sa.connect()
        rows = conn.execute("SELECT kategorie FROM werbungskosten_kategorien").fetchall()
        kategorien = {r[0] for r in rows}
        self.assertIn("Arbeitsmittel", kategorien)
        self.assertIn("Fahrtkosten", kategorien)
        self.assertIn("Fortbildung", kategorien)

    # ------------------------------------------------------------------
    # CRUD-Zyklus
    # ------------------------------------------------------------------

    def test_add_beleg(self):
        b = self.sa.add_beleg(
            kategorie="Arbeitsmittel",
            betrag_eur=49.90,
            datum="2026-03-15",
            notiz="USB-Hub",
        )
        self.assertEqual(b["kategorie"], "Arbeitsmittel")
        self.assertAlmostEqual(b["betrag_eur"], 49.90)
        self.assertTrue(b["nummer"].startswith("B-20260315-"))

    def test_beleg_nummer_sequence(self):
        b1 = self.sa.add_beleg("Arbeitsmittel", 10.0, datum="2026-03-01")
        b2 = self.sa.add_beleg("Fahrtkosten", 20.0, datum="2026-03-01")
        self.assertEqual(b1["nummer"], "B-20260301-001")
        self.assertEqual(b2["nummer"], "B-20260301-002")

    def test_list_belege(self):
        self.sa.add_beleg("Arbeitsmittel", 49.90, datum="2026-03-15")
        self.sa.add_beleg("Fahrtkosten",   120.0, datum="2026-04-10")
        belege = self.sa.list_belege()
        self.assertEqual(len(belege), 2)

    def test_list_belege_filter_jahr(self):
        self.sa.add_beleg("Arbeitsmittel", 49.90, datum="2026-03-15")
        self.sa.add_beleg("Fahrtkosten",   120.0, datum="2025-11-01")
        belege_2026 = self.sa.list_belege(jahr=2026)
        self.assertEqual(len(belege_2026), 1)
        self.assertEqual(belege_2026[0]["kategorie"], "Arbeitsmittel")

    def test_get_beleg(self):
        b = self.sa.add_beleg("Fortbildung", 299.0, datum="2026-05-20", notiz="Python-Kurs")
        found = self.sa.get_beleg(b["nummer"])
        self.assertIsNotNone(found)
        self.assertEqual(found["notiz"], "Python-Kurs")

    def test_delete_beleg(self):
        b = self.sa.add_beleg("Sonstiges", 5.0, datum="2026-06-01")
        self.assertTrue(self.sa.delete_beleg(b["nummer"]))
        self.assertIsNone(self.sa.get_beleg(b["nummer"]))

    def test_delete_nonexistent(self):
        self.assertFalse(self.sa.delete_beleg("B-99999999-000"))

    # ------------------------------------------------------------------
    # Werbungskosten
    # ------------------------------------------------------------------

    def test_werbungskosten_aggregation(self):
        self.sa.add_beleg("Arbeitsmittel", 100.0, datum="2026-01-10")
        self.sa.add_beleg("Arbeitsmittel", 50.0,  datum="2026-02-15")
        self.sa.add_beleg("Fahrtkosten",   200.0, datum="2026-03-01")
        agg = self.sa.werbungskosten(2026)
        self.assertEqual(agg["jahr"], 2026)
        self.assertAlmostEqual(agg["gesamt_eur"], 350.0)
        kategorien = {k["kategorie"]: k["summe"] for k in agg["kategorien"]}
        self.assertAlmostEqual(kategorien["Arbeitsmittel"], 150.0)
        self.assertAlmostEqual(kategorien["Fahrtkosten"],   200.0)

    def test_werbungskosten_empty_year(self):
        agg = self.sa.werbungskosten(2099)
        self.assertAlmostEqual(agg["gesamt_eur"], 0.0)
        self.assertEqual(len(agg["kategorien"]), 0)

    # ------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------

    def test_export_finanzamt_creates_zip(self):
        self.sa.add_beleg("Arbeitsmittel", 49.90, datum="2026-03-15")
        self.sa.add_beleg("Fahrtkosten",   120.0, datum="2026-04-10")
        out = Path(self.td) / "FINANZAMT_2026.zip"
        result = self.sa.export_finanzamt(2026, out_path=out)
        self.assertTrue(result.exists())
        with zipfile.ZipFile(result) as zf:
            names = zf.namelist()
            self.assertIn("belege_2026.csv", names)
            self.assertIn("zusammenfassung_2026.txt", names)

    def test_export_logs_run(self):
        self.sa.add_beleg("Arbeitsmittel", 49.90, datum="2026-03-15")
        out = Path(self.td) / "FINANZAMT_2026.zip"
        self.sa.export_finanzamt(2026, out_path=out)
        s = self.sa.status()
        self.assertEqual(s["anzahl_exporte"], 1)

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def test_status(self):
        self.sa.add_beleg("Arbeitsmittel", 10.0, datum="2026-01-01")
        s = self.sa.status()
        self.assertEqual(s["anzahl_belege"], 1)
        # db_path zeigt auf den tempdir-Override; Store-Datei muss erkennbar sein
        self.assertIn("steuer_test.db", s["db_path"])


if __name__ == "__main__":
    unittest.main()
