"""Vertragstests fuer Metadaten, Governance-Invarianten und Discoverability-Paritaet."""

from __future__ import annotations

import json
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
        self.third_party_licenses = (ROOT / "THIRD_PARTY_LICENSES.md").read_text(encoding="utf-8")
        self.tests_workflow = (ROOT / ".github" / "workflows" / "tests.yml").read_text(encoding="utf-8")
        self.stale_workflow = (ROOT / ".github" / "workflows" / "stale.yml").read_text(encoding="utf-8")
        self.welcome_workflow = (ROOT / ".github" / "workflows" / "welcome.yml").read_text(encoding="utf-8")
        self.changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")

    def test_quick_navigation_anchors_exist(self) -> None:
        en_anchors = re.findall(r"\[([^\]]+)\]\(#([^\)]+)\)", self.readme_en)
        self.assertGreaterEqual(len(en_anchors), 10)
        for label, anchor in en_anchors:
            # Check if header exists in README.md
            pattern = re.compile(r"^#+\s+.*", re.MULTILINE)
            headers = [h.strip("#").strip().lower() for h in pattern.findall(self.readme_en)]
            slugs = [re.sub(r"[^a-z0-9\-_ ]", "", h).strip().replace(" ", "-") for h in headers]
            self.assertIn(anchor, slugs, f"Anchor #{anchor} ({label}) not found in README.md headers: {slugs}")

        de_anchors = re.findall(r"\[([^\]]+)\]\(#([^\)]+)\)", self.readme_de)
        self.assertGreaterEqual(len(de_anchors), 10)
        for label, anchor in de_anchors:
            pattern = re.compile(r"^#+\s+.*", re.MULTILINE)
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
            self.assertIn(inv, self.third_party_licenses, f"{inv} missing in THIRD_PARTY_LICENSES.md")

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
        # Multi-Host und Lock-System Erweiterungen
        self.assertIn("*conflicted copy*", self.gitignore)
        self.assertIn("*-ASUS*", self.gitignore)
        self.assertIn("*-WORKSTATION*", self.gitignore)
        self.assertIn("*-LAPTOP*", self.gitignore)
        self.assertIn("*-Mac Studio*", self.gitignore)
        self.assertIn("LOCK.user.*", self.gitignore)
        self.assertIn("LOCK.until.*", self.gitignore)
        self.assertIn("LOCK.condition.*", self.gitignore)
        self.assertIn("LOCK.permissions.json", self.gitignore)
        self.assertIn("uv.lock", self.gitignore)

    def test_pyproject_ecosystem_urls_and_tool_config(self) -> None:
        self.assertIn('"Parent Organization" = "https://github.com/ellmos-ai"', self.pyproject)
        self.assertIn('"Umbrella Ecosystem" = "https://github.com/open-bricks"', self.pyproject)
        self.assertIn('"Third-Party Licenses" = "https://github.com/ellmos-ai/steuer-assistent/blob/main/THIRD_PARTY_LICENSES.md"', self.pyproject)
        self.assertIn('"LLM Ready" = "https://raw.githubusercontent.com/ellmos-ai/steuer-assistent/main/llms.txt"', self.pyproject)
        self.assertIn('"Marketing Log" = "https://github.com/ellmos-ai/steuer-assistent/blob/main/MARKETING-LOG.txt"', self.pyproject)
        self.assertIn("Documentation =", self.pyproject)
        self.assertIn("Changelog =", self.pyproject)
        self.assertIn("Security =", self.pyproject)
        self.assertIn('license-files = ["LICENSE", "THIRD_PARTY_LICENSES.md"]', self.pyproject)
        self.assertIn("norecursedirs =", self.pyproject)
        self.assertIn("[tool.ruff]", self.pyproject)
        self.assertIn('"Programming Language :: Python :: 3.13"', self.pyproject)

    def test_third_party_licenses_inventory(self) -> None:
        self.assertIn("Zero-Copyleft Guarantee", self.third_party_licenses)
        self.assertIn("RunAsInvoker", self.third_party_licenses)
        self.assertIn("PSF-2.0", self.third_party_licenses)
        self.assertIn("dependencies = []", self.third_party_licenses)
        self.assertIn("Python Standard Library", self.third_party_licenses)

    def test_github_workflows_integrity(self) -> None:
        # tests.yml
        self.assertIn("timeout-minutes: 15", self.tests_workflow)
        self.assertIn('"3.13"', self.tests_workflow)
        self.assertIn("cancel-in-progress: true", self.tests_workflow)
        self.assertIn("contents: read", self.tests_workflow)

        # stale.yml
        self.assertIn("actions/stale@v9", self.stale_workflow)
        self.assertIn("timeout-minutes: 10", self.stale_workflow)
        self.assertIn("cancel-in-progress: true", self.stale_workflow)
        self.assertIn("issues: write", self.stale_workflow)
        self.assertIn("pull-requests: write", self.stale_workflow)

        # welcome.yml
        self.assertIn("actions/first-interaction@v3", self.welcome_workflow)
        self.assertIn("timeout-minutes: 5", self.welcome_workflow)
        self.assertIn("cancel-in-progress: true", self.welcome_workflow)
        self.assertIn("issues: write", self.welcome_workflow)
        self.assertIn("pull-requests: write", self.welcome_workflow)

    def test_version_parity_across_all_manifests(self) -> None:
        import steuer_assistent
        match = re.search(r'version = "([^"]+)"', self.pyproject)
        self.assertIsNotNone(match)
        expected = match.group(1)

        self.assertEqual(steuer_assistent.__version__, expected)

        v1 = json.loads((ROOT / "ellmos-module.json").read_text(encoding="utf-8"))
        self.assertEqual(v1["version"], expected)

        v2 = json.loads((ROOT / "ellmos-module.v2.json").read_text(encoding="utf-8"))
        self.assertEqual(v2["version"], expected)

        skill_de = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn(f"version: {expected}", skill_de)

        skill_en = (ROOT / "SKILL.en.md").read_text(encoding="utf-8")
        self.assertIn(f"version: {expected}", skill_en)

        self.assertIn(f"Version: {expected}", self.llms)
        self.assertIn(f"## [{expected}]", self.changelog)


if __name__ == "__main__":
    unittest.main()
