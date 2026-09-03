# endearqb-skills

[English](README.md) | [简体中文](README.zh-CN.md)

An open-source collection of reusable Agent Skills maintained in this repository.

## Overview

This repository currently includes:

- `endearqb-lab-report-writer`: A journal-style lab and technical report skill with staged HTML generation, data-quality verification, writing-logic self-checks, theme support, and reusable report assets.
- `kimi-swarm-orchestrator`: A general multi-agent orchestration framework for decomposing complex work into documented plans, isolated worker directories, parallel execution, error recovery, and bounded refinement.
- `endearqb-frontend-dataviz`: A skill for frontend data visualization work with design references such as chart examples, palettes, and pictograph icons.
- `endearqb-community-profiler`: A skill for analyzing chat records to generate member profiles, identify key contributors, assess community health, and summarize chat content.
- `endearqb-svg-flowchart`: A skill for generating high-quality SVG flowcharts from textual steps, supporting vertical and horizontal layouts, branch decisions, grouped multi-column flows, and optional HTML preview output.
- `endearqb-wechat-file-organizer`: A skill for organizing WeChat file storage on Windows, with WeChat directory detection, duplicate-file analysis, recycle-bin deduplication, and month/type-based file organization.
- `1nfinix-editorial-card-screenshot`: A skill for generating editorial-style HTML information cards and capturing them as ratio-specific PNG screenshots, with stable Chinese typography fallback and Chromium screenshot rendering.
- `readme-first-builder`: A skill for initializing or upgrading a project to the README First architecture with `AGENTS.md`, root README guidance, `.ai/changes`, `.ai/decisions`, and key directory READMEs.
- `anti-ai-slop-swarm`: A multi-agent de-slop pipeline that diagnoses text through six independent review lenses, merges and prioritizes findings, rewrites once from a unified issue list, and verifies against information loss or over-humanization.
- `product-story-pptx`: A source-backed product-deck skill that turns a brief into a narrative PPTX with a three-act emotional arc, image-led bleed layouts, editable UI mockups, focused data storytelling, version lineage, and executable lint/render/inspect QA.

`anti-ai-slop-swarm` synthesizes and rewrites methods from the following open-source projects:

- [blader/humanizer](https://github.com/blader/humanizer)
- [op7418/Humanizer-zh](https://github.com/op7418/Humanizer-zh)
- [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop)
- [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill)
- [hylarucoder/ai-flavor-remover](https://github.com/hylarucoder/ai-flavor-remover)
- [sptuan/shuo-ren-hua.rule](https://github.com/sptuan/shuo-ren-hua.rule)
- [alchaincyf/nuwa-skill](https://github.com/alchaincyf/nuwa-skill)
- [dongbeixiaohuo/writing-agent](https://github.com/dongbeixiaohuo/writing-agent)
- [Hello-SimpleAI/chatgpt-comparison-detection](https://github.com/Hello-SimpleAI/chatgpt-comparison-detection)
- [OUBIGFA/De-AI-Prompt-Enhancer-Writer-Booster-SKILL](https://github.com/OUBIGFA/De-AI-Prompt-Enhancer-Writer-Booster-SKILL)

## Repository Structure

```text
skills/
  endearqb-lab-report-writer/
  kimi-swarm-orchestrator/
  endearqb-frontend-dataviz/
  endearqb-community-profiler/
  endearqb-svg-flowchart/
  endearqb-wechat-file-organizer/
  1nfinix-editorial-card-screenshot/
  readme-first-builder/
  anti-ai-slop-swarm/
  product-story-pptx/
```

Each skill directory may contain:

- `SKILL.md`: skill instructions
- `agents/`: UI metadata and invocation policy
- `references/`: supporting reference materials
- `scripts/`: helper scripts when needed
- `assets/`, `examples/`, `tests/`, and `evals/`: reusable resources and validation fixtures when needed

## Usage

Clone the repository and use the skill directories as local skill packages in your Agent Skills workflow.

## Contributors

See [CONTRIBUTORS.md](CONTRIBUTORS.md) for the manual contributor list.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Chinese README

For the Chinese version, see `README.zh-CN.md`.
