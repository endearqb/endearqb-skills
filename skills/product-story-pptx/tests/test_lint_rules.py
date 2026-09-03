from __future__ import annotations

import copy
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from lint_deck import lint, load_registry, load_tokens, load_yaml  # noqa: E402


class LintRulesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base = load_yaml(str(ROOT / "assets" / "example-deck-spec.yaml"))
        cls.registry = load_registry()
        cls.tokens = load_tokens()
        cls.spec_path = str(ROOT / "assets" / "example-deck-spec.yaml")

    def report(self, spec):
        return lint(spec, self.registry, self.tokens, self.spec_path)

    def test_example_passes(self):
        report = self.report(copy.deepcopy(self.base))
        self.assertEqual([], report.fails)
        self.assertEqual([], report.warns)

    def test_missing_big_idea_fails(self):
        spec = copy.deepcopy(self.base)
        del spec["deck"]["big_idea"]
        report = self.report(spec)
        self.assertTrue(any(x["rule"] == "L14" for x in report.fails))

    def test_flow_requires_exactly_one_highlight(self):
        spec = copy.deepcopy(self.base)
        flow = next(slide for slide in spec["slides"] if slide["type"] == "flow")
        for step in flow["steps"]:
            step.pop("highlight", None)
        report = self.report(spec)
        self.assertTrue(any(x["rule"] == "L08" for x in report.fails))

    def test_flow_rejects_manual_line_breaks(self):
        spec = copy.deepcopy(self.base)
        flow = next(slide for slide in spec["slides"] if slide["type"] == "flow")
        flow["steps"][0]["label"] = "自动\n建索引"
        report = self.report(spec)
        self.assertTrue(any(x["rule"] == "L08" and "手工换行" in x["msg"] for x in report.fails))

    def test_flow_images_require_vertical_layers(self):
        spec = copy.deepcopy(self.base)
        flow = next(slide for slide in spec["slides"] if slide["type"] == "flow")
        flow["images"] = ["placeholder.png"]
        flow["direction"] = "horizontal"
        flow["style"] = "cards"
        report = self.report(spec)
        self.assertTrue(any(x["rule"] == "L08" and "vertical" in x["msg"] for x in report.fails))

    def test_forbidden_chart_kind_fails(self):
        spec = copy.deepcopy(self.base)
        chart = next(slide for slide in spec["slides"] if slide["type"] == "chart")
        chart["chart"]["kind"] = "pie"
        report = self.report(spec)
        self.assertTrue(any(x["rule"] == "L07" for x in report.fails))

    def test_flat_energy_curve_fails(self):
        spec = copy.deepcopy(self.base)
        for slide in spec["slides"]:
            slide["energy"] = 3
        report = self.report(spec)
        self.assertTrue(any(x["rule"] == "L03" for x in report.fails))

    def test_bleed_budget_fails(self):
        spec = copy.deepcopy(self.base)
        # Use color-block only on types that accept it, enough to exceed 40%.
        changed = 0
        for slide in spec["slides"]:
            allowed = self.registry["types"][slide["type"]]["bleeds"]
            if "color-block" in allowed and changed < 5:
                slide["bleed"] = "color-block"
                slide.pop("image", None)
                slide.pop("scrim", None)
                changed += 1
        report = self.report(spec)
        self.assertTrue(any(x["rule"] == "L04" for x in report.fails))

    def test_topic_budget_fails_when_share_is_outside_range(self):
        spec = copy.deepcopy(self.base)
        spec["deck"]["topic_budgets"][0]["min_share"] = 0.90
        report = self.report(spec)
        self.assertTrue(any(x["rule"] == "L15" for x in report.fails))

    def test_iteration_lineage_requires_existing_parent_manifest(self):
        spec = copy.deepcopy(self.base)
        spec["deck"]["lineage"] = {
            "mode": "iteration",
            "version": "v2",
            "parent_manifest": "missing-v1.manifest.json",
            "change_summary": "调整 UI 外框",
            "regression_pages": [5],
            "affected_components": ["ui_mockup"],
        }
        report = self.report(spec)
        self.assertTrue(any(x["rule"] == "L16" for x in report.fails))

    def test_iteration_lineage_accepts_existing_parent_manifest(self):
        spec = copy.deepcopy(self.base)
        with tempfile.NamedTemporaryFile(dir=ROOT / "assets", suffix=".manifest.json") as parent:
            relative = Path(parent.name).relative_to(ROOT / "assets")
            spec["deck"]["lineage"] = {
                "mode": "iteration",
                "version": "v2",
                "parent_manifest": str(relative),
                "change_summary": "调整 UI 外框",
                "regression_pages": [5],
                "affected_components": ["ui_mockup"],
            }
            report = self.report(spec)
        self.assertFalse(any(x["rule"] == "L16" for x in report.fails))

    def test_ui_mockup_theme_is_checked(self):
        spec = copy.deepcopy(self.base)
        ui_slide = next(slide for slide in spec["slides"] if "ui_mockup" in slide)
        ui_slide["ui_mockup"]["theme"] = "glass"
        report = self.report(spec)
        self.assertTrue(any(x["rule"] == "L17" for x in report.fails))

    def test_media_bars_requires_one_image_per_item(self):
        spec = copy.deepcopy(self.base)
        media = next(slide for slide in spec["slides"] if slide["type"] == "media_bars")
        media["items"][0].pop("image")
        report = self.report(spec)
        self.assertTrue(any(x["rule"] == "L18" for x in report.fails))

    def test_half_top_and_half_bottom_are_valid(self):
        report = self.report(copy.deepcopy(self.base))
        used = {slide["bleed"] for slide in self.base["slides"]}
        self.assertIn("half-top", used)
        self.assertIn("half-bottom", used)
        self.assertFalse(any(x["rule"] in {"L00", "L02"} for x in report.fails))


if __name__ == "__main__":
    unittest.main()
