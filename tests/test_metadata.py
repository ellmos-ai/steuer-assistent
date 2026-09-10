"""Vertragstests fuer Metadaten, Governance-Invarianten und Discoverability-Paritaet."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).parent.parent


class MetadataDiscoverabilityContractCase(unittest.TestCase):
    def setUp(self) -> None:
        self.readme_en = (ROOT / "README.md").read_text(encoding="utf-8")
        self.readme_de = (ROOT / "README_de.md").read_text(encoding="utf-8")
        self.security = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
        self.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        self.marketing = (ROOT / "MARKETING-LOG.txt").read_text(encoding="utf-8")
        self.gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")

    def test_quick_navigation_anchors_exist(self) -> None:
        en_anchors = re.findall(r"\[([^\]]+)\]\(#([^\)]+)\)", self.readme_en)
        self.assertGreaterEqual(len(en_anchors), 10)
        for label, anchor in en_anchors:
            # Check if header exists in README.md
            pattern = re.compile(rf"^#+\s+.*", re.MULTILINE)
            headers = [h.strip("#").strip().lower() for h in pattern.findall(self.readme_en)]
            slugs = [re.sub(r"[^a-z0-9\-_ ]", "", h).strip().replace(" ", "-") for h in headers]
            self.assertIn(anchor, slugs, f"Anchor #{anchor} ({label}) not found in README.md headers: {slugs}")

        de_anchors = re.findall(r"\[([^\]]+)\]\(#([^\)]+)\)", self.readme_de)
        self.assertGreaterEqual(len(de_anchors), 10)
        for label, anchor in de_anchors:
            pattern = re.compile(rf"^#+\s+.*", re.MULTILINE)
            headers = [h.strip("#").strip().lower() for h in pattern.findall(self.readme_de)]
            # German headers slug conversion
            slugs = [
                re.sub(r"[^a-z0-9äöüß\-_ ]", "", h)
                .strip()
                .replace(" ", "-")
                .replace("ä", "a")
                .replace("ö", "o")
                .replace("ü", "u")
                .replace("ß", "ss")
                for h in headers
            ]
            # Some markdown engines keep umlauts, check both raw and ascii-slug
            raw_slugs = [re.sub(r"[^a-z0-9äöüß\-_ ]", "", h).strip().replace(" ", "-") for h in headers]
            self.assertTrue(
                anchor in slugs or anchor in raw_slugs,
                f"Anchor #{anchor} ({label}) not found in README_de.md headers: {raw_slugs}",
            )

    def test_governance_invariants_parity(self) -> None:
        expected_invariants = [f"INV-LOCAL-{i:02d}" for i in range(1, 11)]
        for inv in expected_invariants:
            self.assertIn(inv, self.readme_en, f"{inv} missing in README.md")
            self.assertIn(inv, self.readme_de, f"{inv} missing in README_de.md")
            self.assertIn(inv, self.llms, f"{inv} missing in llms.txt")

    def test_mermaid_sequence_diagrams_present(self) -> None:
        self.assertIn("```mermaid\nsequenceDiagram", self.readme_en)
        self.assertIn("```mermaid\nsequenceDiagram", self.readme_de)
        self.assertIn("autonumber", self.readme_en)
        self.assertIn("autonumber", self.readme_de)

    def test_security_policy_sla_and_contacts(self) -> None:
        self.assertIn("48 hours", self.security)
        self.assertIn("5 business days", self.security)
        self.assertIn("security@open-bricks.org", self.security)
        self.assertIn("security@ellmos.ai", self.security)
        self.assertIn("lukas@open-bricks.org", self.security)

    def test_marketing_log_structure(self) -> None:
        self.assertIn("Positionierung & Kernnutzen", self.marketing)
        self.assertIn("Zielgruppen (Personas)", self.marketing)
        self.assertIn("Discoverability & SEO-Keywords", self.marketing)
        self.assertIn("Externe Ökosystem-Vernetzung", self.marketing)

    def test_gitignore_contains_conflict_and_lock_rules(self) -> None:
        self.assertIn("*-conflict-*", self.gitignore)
        self.assertIn("*.sync-conflict-*", self.gitignore)
        self.assertIn("LOCK", self.gitignore)
        self.assertIn(".ruff_cache/", self.gitignore)

    def test_pyproject_ecosystem_urls(self) -> None:
        self.assertIn('"Parent Organization" = "https://github.com/ellmos-ai"', self.pyproject)
        self.assertIn('"Umbrella Ecosystem" = "https://github.com/open-bricks"', self.pyproject)
        self.assertIn("Documentation =", self.pyproject)
        self.assertIn("Changelog =", self.pyproject)
        self.assertIn("Security =", self.pyproject)


if __name__ == "__main__":
    unittest.main()
