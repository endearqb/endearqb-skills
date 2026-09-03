#!/usr/bin/env python3
"""Run the complete product-story-pptx regression pipeline.

Checks:
  1. Required files exist and SKILL.md frontmatter is valid.
  2. All Python files compile.
  3. YAML files parse.
  4. Unit tests pass.
  5. Example spec lints with 0 FAIL / 0 WARN.
  6. Example deck builds.
  7. Generated PPTX inspects with 0 ERROR / 0 WARN.
  8. LibreOffice + Poppler render PDF, slide PNGs and contact sheet.

Usage:
    python scripts/smoke_test.py
    python scripts/smoke_test.py --keep --outdir validation-output
    python scripts/smoke_test.py --skip-render
"""
from __future__ import annotations

import argparse
import json
import os
import py_compile
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "SKILL.md",
    "README.md",
    "LICENSE",
    "requirements.txt",
    "agents/openai.yaml",
    "assets/design-tokens.yaml",
    "assets/layout-registry.yaml",
    "assets/example-deck-spec.yaml",
    "scripts/lint_deck.py",
    "scripts/build_deck.py",
    "scripts/chart_swd.py",
    "scripts/flow_diagram.py",
    "scripts/ui_mockup.py",
    "scripts/render_preview.py",
    "scripts/inspect_pptx.py",
    "references/INDEX.md",
    "references/narrative-arc.md",
    "references/bleed-layouts.md",
    "references/layout-system.md",
    "references/diagram-patterns.md",
    "references/data-storytelling.md",
    "references/visual-language.md",
    "references/qa-checklist.md",
    "references/research-basis.md",
    "references/iteration-lineage.md",
    "references/editable-ui-mockups.md",
]


def run(cmd: list[str], cwd: Path = ROOT) -> dict:
    print("$", " ".join(cmd))
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=420)
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip(), file=sys.stderr)
    return {"cmd": cmd, "returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr}


def parse_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    try:
        raw = text.split("\n---\n", 1)[0][4:]
    except Exception as exc:  # pragma: no cover
        raise ValueError("SKILL.md frontmatter is not closed") from exc
    data = yaml.safe_load(raw)
    if not isinstance(data, dict):
        raise ValueError("SKILL.md frontmatter must be a mapping")
    for key in ("name", "description"):
        if not str(data.get(key) or "").strip():
            raise ValueError(f"SKILL.md frontmatter missing {key}")
    if data["name"] != ROOT.name:
        raise ValueError(f"frontmatter name {data['name']!r} != folder name {ROOT.name!r}")
    return data


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--keep", action="store_true", help="keep generated test outputs")
    parser.add_argument("--outdir", default=None)
    parser.add_argument("--skip-render", action="store_true")
    args = parser.parse_args(argv)

    report: dict = {"passed": False, "checks": [], "environment": {"python": sys.version}}
    failed = False

    missing = [name for name in REQUIRED if not (ROOT / name).exists()]
    report["checks"].append({"name": "required_files", "passed": not missing, "missing": missing})
    if missing:
        print("Missing:", *missing, sep="\n  - ", file=sys.stderr)
        failed = True

    try:
        frontmatter = parse_frontmatter(ROOT / "SKILL.md")
        report["frontmatter"] = frontmatter
        report["checks"].append({"name": "frontmatter", "passed": True})
    except Exception as exc:
        report["checks"].append({"name": "frontmatter", "passed": False, "error": str(exc)})
        print(f"Frontmatter: {exc}", file=sys.stderr)
        failed = True

    compile_errors = []
    for path in sorted((ROOT / "scripts").glob("*.py")) + sorted((ROOT / "tests").glob("*.py")):
        try:
            py_compile.compile(str(path), doraise=True)
        except Exception as exc:  # pragma: no cover
            compile_errors.append({"file": str(path.relative_to(ROOT)), "error": str(exc)})
    report["checks"].append({"name": "python_compile", "passed": not compile_errors, "errors": compile_errors})
    failed |= bool(compile_errors)

    yaml_errors = []
    for path in sorted(ROOT.rglob("*.yaml")):
        try:
            yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception as exc:
            yaml_errors.append({"file": str(path.relative_to(ROOT)), "error": str(exc)})
    report["checks"].append({"name": "yaml_parse", "passed": not yaml_errors, "errors": yaml_errors})
    failed |= bool(yaml_errors)

    if not failed:
        unit = run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"])
        report["checks"].append({"name": "unit_tests", "passed": unit["returncode"] == 0})
        failed |= unit["returncode"] != 0

    if args.outdir:
        outdir = Path(args.outdir).resolve()
        outdir.mkdir(parents=True, exist_ok=True)
        temporary = False
    elif args.keep:
        outdir = ROOT / "validation-output"
        if outdir.exists():
            shutil.rmtree(outdir)
        outdir.mkdir(parents=True)
        temporary = False
    else:
        outdir = Path(tempfile.mkdtemp(prefix="product-story-pptx-smoke-"))
        temporary = True

    example = ROOT / "assets" / "example-deck-spec.yaml"
    example_spec = yaml.safe_load(example.read_text(encoding="utf-8"))
    expected_slides = len(example_spec["slides"])
    pptx = outdir / "example.pptx"

    if not failed:
        lint_result = run([sys.executable, "scripts/lint_deck.py", str(example)])
        lint_ok = lint_result["returncode"] == 0 and "0 FAIL, 0 WARN" in lint_result["stdout"]
        report["checks"].append({"name": "lint", "passed": lint_ok})
        failed |= not lint_ok

    if not failed:
        build_result = run([sys.executable, "scripts/build_deck.py", str(example), str(pptx)])
        build_ok = build_result["returncode"] == 0 and pptx.exists() and pptx.stat().st_size > 10_000
        report["checks"].append({"name": "build", "passed": build_ok, "pptx_bytes": pptx.stat().st_size if pptx.exists() else 0})
        failed |= not build_ok

    if not failed:
        manifest_path = pptx.with_suffix(".manifest.json")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
        lineage = manifest.get("lineage") or {}
        manifest_ok = (
            len(manifest.get("slides") or []) == expected_slides
            and lineage.get("mode") == "initial"
            and lineage.get("version") == "v1.1-example"
            and len(manifest.get("topic_budgets") or []) == 1
            and sum(1 for slide in manifest.get("slides") or [] if slide.get("ui_mockup")) == 2
        )
        report["checks"].append({"name": "manifest_lineage", "passed": manifest_ok})
        failed |= not manifest_ok

    if not failed:
        inspect_result = run([sys.executable, "scripts/inspect_pptx.py", str(pptx)])
        inspect_ok = inspect_result["returncode"] == 0 and "0 ERROR, 0 WARN" in inspect_result["stdout"]
        report["checks"].append({"name": "inspect", "passed": inspect_ok})
        failed |= not inspect_ok

    if not failed and not args.skip_render:
        render_result = run([sys.executable, "scripts/render_preview.py", str(pptx), "--dpi", "80", "--cols", "4"])
        preview = outdir / "example_preview"
        contact = preview / "contact_sheet.png"
        pngs = sorted(preview.glob("slide-*.png")) if preview.exists() else []
        render_ok = render_result["returncode"] == 0 and contact.exists() and len(pngs) == expected_slides
        report["checks"].append({"name": "render", "passed": render_ok, "slides": len(pngs), "contact_sheet": str(contact)})
        failed |= not render_ok
    elif args.skip_render:
        report["checks"].append({"name": "render", "passed": True, "skipped": True})

    report["passed"] = not failed
    report_path = outdir / "smoke-test-report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nReport: {report_path}")
    print("PASS" if report["passed"] else "FAIL")

    if temporary and not args.keep:
        # Preserve the report path only for the duration of this process; CI consumes stdout/exit code.
        shutil.rmtree(outdir, ignore_errors=True)
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
