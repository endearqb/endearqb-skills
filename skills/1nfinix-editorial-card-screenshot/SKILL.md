---
name: 1nfinix-editorial-card-screenshot
description: "Generate editorial-style HTML information cards and capture them as ratio-specific PNG screenshots. Use when the user wants a research card, info card, briefing card, cover card, or editorial social asset in ratios such as 3:4, 4:3, 1:1, 16:9, 9:16, 2.35:1, 3:1, or 5:2. Includes stable Chinese typography fallback and direct Chromium screenshot capture."
metadata: {"clawdbot":{"requires":{"bins":["google-chrome","chromium","chrome"]}}}
---

# Editorial Card Screenshot

## Overview

Turn source text into an editorial-style HTML information card, then capture it as a PNG in a supported ratio.
The priority is editorial hierarchy plus stable rendering: no clipped Chinese text, no accidental cropping, and no large dead zones in the lower half.

Default deliverables unless the user asks otherwise:
1. One complete HTML file with embedded CSS.
2. One PNG screenshot rendered from that HTML.

## Workflow

### 1. Analyze Content Density

Choose layout strategy from the content itself:
- Use "big-character" composition when content is sparse and a single phrase, number, or hook can carry the page.
- Use a two-column or three-column editorial grid when content is dense and needs stronger hierarchy.
- Use oversized numbers, heavy rules, tinted blocks, and pull-quote scale to avoid dead space.
- Do not force dense content into evenly weighted tiles. Build primary blocks, secondary blocks, and lighter supporting blocks.
- Match structure to content type:
  - Ranking / recommendation content: allow asymmetric hero + structured list.
  - Tutorial / analysis / interpretation content: group into overview, core judgment, interpretation, boundary, and conclusion.

Before compressing content, first change the layout skeleton.
- Ratio changes should primarily change reading path, hierarchy, and module arrangement.
- Do not treat ratio changes as a reason to delete content by default.
- Only compress, group, or summarize when the current ratio cannot hold the content clearly after layout has already been restructured.

### 2. Apply the Editorial Defaults

Use these defaults unless the user overrides them:
- Import Google Fonts:
  ```html
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@700;900&family=Noto+Sans+SC:wght@400;500;700&family=Oswald:wght@500;700&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
  ```
- For Chinese text, always declare local CJK fallbacks before generic serif/sans-serif fallbacks. Prefer:
  ```css
  font-family: "Noto Sans SC", "Noto Sans CJK SC", "Source Han Sans SC", "Microsoft YaHei", "PingFang SC", sans-serif;
  font-family: "Noto Serif SC", "Noto Serif CJK SC", "Source Han Serif SC", "Songti SC", "STSong", serif;
  ```
- Keep body text around `18px` to `20px` on a 900px-wide composition.
- Keep meta/tag text at `13px` minimum.
- Use compact spacing: outer padding `40px` to `50px`, module gaps `30px` to `40px`, line-height `1.5` to `1.6`.
- Add visual anchors with `4px` to `6px` accent rules, subtle gray planes, and a light noise overlay.
- Favor warm-paper backgrounds such as `#f5f3ed` unless the user specifies another palette.
- For Chinese-heavy cards, shorten dense column line lengths and always add `overflow-wrap` / `word-break` guards.
- If the user provides a title, use it as the main headline by default. Expand the layout before rewriting or shortening it.
- Avoid equal-weight boxes on dense cards. At least one module should feel visually heavier than the others.
- Do not hard-code signatures, creator handles, or personal branding unless requested.

### 3. Choose the Right Layout Skeleton

Pick ratio-specific structure before writing final copy.

#### `4:3`
- Best for full analytical spread or ranked lists.
- Prefer: hero + summary band + dense two-column list + stronger footer.
- Use one main judgment block before the list so the page does not become a flat wall of 10 equal items.
- Recommended reusable skeleton:
  - left heavy primary module for the main process / sequence / framework
  - right narrower stack for takeaways, pitfalls, or judgments
  - a light but intentional source / core-judgment strip at the bottom
- Avoid making `4:3` a symmetrical two-column newspaper wall from top to bottom.

#### `3:4`
- Keep the same information ambition, but change the reading path.
- Prefer: title band + insight row + mixed large/small body modules.
- Use mixed scales: one heavy primary block, one or two medium blocks, and smaller support blocks.
- Do not let the whole portrait card collapse into a long single column.
- Recommended reusable skeleton:
  - strong cover-style title zone
  - compact stat strip or insight strip
  - one large primary module
  - one medium judgment module
  - two smaller lower modules for takeaways / pitfalls / examples
- Avoid lower-half layouts that become two large empty boxes with only a few lines of copy.

#### `1:1`
- Best for ability map, grouped comparison, or balanced editorial overview.
- Prefer: strong hero + one heavier quadrant + three supporting quadrants + dense footer strip.
- Square layouts should feel centered and modular, not evenly tiled.
- Do not treat `1:1` as the default skeleton for every card. Pick it only when the output ratio is actually square.
- Recommended reusable skeleton:
  - strong title / subtitle hero across the top
  - one compact stat strip
  - one heavy left module for the main framework or sequence
  - one upper-right judgment module
  - one lower-right split for takeaways / pitfalls or compare blocks
  - one thin source / core-judgment strip at the bottom
- Avoid four equal quadrants and avoid tiny typography spread across too many boxes.

#### Wide covers (`3:1`, `5:2`, `2.35:1`)
- Reduce paragraph length aggressively.
- Use fewer but larger blocks, stronger headlines, and short support lines.

### 4. Build HTML for Rendering

When HTML will be screenshotted, design the page as a fixed-size canvas instead of a responsive webpage:
- Match the exact pixel dimensions of the selected ratio preset from `references/ratios.md`.
- Add an explicit `@page { size: ...; margin: 0; }` rule that matches the fixed canvas when using PDF-based capture flows, otherwise Chromium print rendering may silently crop or scale the right edge.
- Treat the card as a design board with explicit `width` and `height`, not as a fluid `100vw / 100vh` layout.
- Remove browser-default margins with `html, body { margin: 0; }`.
- Make the card itself fill the screenshot viewport exactly.
- Avoid interactions, sticky headers, or long scrolling sections.
- Use fixed pixel wrappers, for example:
  ```css
  .frame {
    width: 2000px;
    height: 1500px;
  }

  .card {
    width: 100%;
    height: 100%;
    padding: 48px;
    background: #f5f3ed;
  }
  ```

Do not rely on `100vw`, `100vh`, or responsive container widths as the primary design size for screenshot output.

If the user asks only for HTML, still make the layout screenshot-ready.

At the same time, preserve basic browser preview behavior:
- In screenshot mode, `html`, `body`, and the outer frame should match the target canvas size exactly.
- In mobile / narrow-width preview mode, add a media-query fallback that returns the page to normal flow so the HTML is still readable outside the screenshot workflow.

Use these structural heuristics when composing the card:
- Fill the proportion intentionally. Rebalance layout according to width / height instead of scaling one static template.
- In `4:3` landscape, asymmetric left-right layouts often work best for dense analytical content.
- In `3:4` portrait, use portrait-friendly mixed grids rather than a single narrow column.
- Keep title, subtitle, summary, and modules separated by explicit rows or bands so they do not collide.
- When the user supplied the title, protect it as a first-class anchor. Expand the layout around it before you consider shortening or paraphrasing it.
- If using numbered modules, keep numbers visually weak enough that they never collide with titles.
- If a section becomes visually monotonous, introduce contrast through hierarchy changes rather than decorative clutter.
- Let big modules carry richer copy than small modules. Do not give every block the same amount of text.
- Do not use `1fr` rows or columns in ways that can create large accidental voids near the footer or push important content to the canvas edge.
- If the lower half feels empty, first rebalance module hierarchy or add a stronger bottom band before shrinking text or stretching containers.
- If a lower module is visually large, give it enough internal structure or a secondary judgment line so it earns the area it occupies.
- In screenshot HTML, make grid children explicitly `min-width: 0` and use text wrapping guards on title/body/caption/list content; otherwise Chromium may clip long Chinese phrases inside narrow columns even when the layout looks mathematically valid.

### 5. Capture the Screenshot

Use the bundled shell script when the user wants a PNG output:
```bash
./scripts/capture_card.sh input.html output.png 3:4
```

Supported ratios and render sizes live in [references/ratios.md](references/ratios.md).

Before running the script:
- Save the generated HTML to a local file.
- Keep the page self-contained except for fonts.
- Ensure the HTML uses a fixed-size design canvas that matches the chosen ratio preset.
- Ensure fallback fonts are declared so layout remains stable even if remote font downloads fail.

If the screenshot still has bottom whitespace, fix the layout skeleton first. Do not treat cropping or trimming as the default solution.

### 6. Ratio Policy

Accept only these ratio presets:
- `3:4`
- `4:3`
- `1:1`
- `16:9`
- `9:16`
- `2.35:1`
- `3:1`
- `5:2`

If the user gives a ratio outside this set, ask them to map it to the nearest supported preset rather than inventing a new one.

## Output Contract

When responding to a card-generation request:
- Keep prose short.
- Output the complete HTML as the primary deliverable.
- If the user also requested an image, state the ratio used and the screenshot command after the HTML.

## Resources

### `references/ratios.md`
Open this when you need the exact preset names or capture dimensions.

### `references/editorial-card-prompt.md`
Use this as the canonical prompt spec when the user wants the latest validated editorial-card behavior.

### `references/recommended-skeletons.md`
Use this when you want ratio-specific reusable skeletons rather than one-off composition ideas.

### `scripts/capture_card.sh`
Run this to capture a PNG from a local HTML file using a supported ratio preset.
It requires a local Chrome or Chromium binary or an explicit `CHROME_BIN` override.

### `assets/card-template.html`
Use this as a starting shell when you want a minimal ratio-ready HTML canvas before filling in real content.
The template syncs its canvas size to the active viewport during capture, while still falling back to readable normal flow on narrower browser widths.

## Failure Checks

Before finalizing HTML or PNG, explicitly reject the result if any of these happen:
- A user-provided title was silently rewritten even though the ratio could have held it with a better layout.
- The title overlaps, visually collides with, or blocks summary/body content.
- The title becomes a narrow vertical strip when more horizontal width is available.
- Dense cards are split into too many equal-weight boxes.
- Large blocks contain too little copy and read like empty containers.
- The canvas shows large areas of dead space that could be filled by stronger hierarchy, richer block content, or a heavier main module.
- The PNG feels meaningfully emptier than the HTML layout intent.
- The rendered PNG uses a different reading rhythm than the HTML because remote fonts failed and no local fallback stack was provided.
- Chinese text renders as tofu boxes, garbled glyphs, or visibly wrong fallback because the HTML omitted explicit local CJK fallback families.
- The footer or bottom band is cropped, or a large bottom whitespace strip appears because the grid sizing pushed content away from the lower edge.
