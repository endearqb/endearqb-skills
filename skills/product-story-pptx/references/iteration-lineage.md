# 有源文件项目的多轮迭代与版本谱系

> Skill 路径：`product-story-pptx/references/iteration-lineage.md`

本 skill 可以继续维护自己生成的项目，或一个具备可重建源文件的同构项目。可接受的源文件至少包括 `spec.yaml`；推荐同时保留 `brief.md`、`outline.md`、生成脚本、上版 manifest 与预览。

它仍不承担对任意客户 `.pptx` 的逆向编辑。只有 PPTX、没有 spec 或可重建脚本时，应转到通用 PPTX 编辑工作流。

## 1. 迭代入口

开始前按顺序核对：

1. 找到当前 `spec.yaml`、生成脚本和资产目录。
2. 找到上一版 `.manifest.json` 与预览图；没有时明确记录谱系断点。
3. 把用户反馈拆成：全局规则、公共组件、指定页面、素材替换、纯审美偏好。
4. 只把可跨项目复用的经验沉淀为 skill 规则；品牌名、固定页码和一次性数值留在项目 spec。
5. 复制或版本化输出，禁止覆盖唯一可工作的上版交付物。

## 2. Lineage schema

```yaml
deck:
  lineage:
    mode: iteration
    version: v2
    parent_manifest: out/deck_v1.manifest.json
    change_summary: "重做 7 个界面示意，并复核受影响页面"
    regression_pages: [7, 10, 12, 14, 18, 19, 22]
    affected_components: [ui_mockup]
```

- `mode`: `initial | iteration`。
- `version`: 人可读版本，不强制 SemVer。
- `parent_manifest`: iteration 必填；相对当前 spec 路径解析。
- `change_summary`: 必填，说明本轮目标，不写流水账。
- `regression_pages`: 本轮必须逐页复核的 1-based 页码；至少一页且不能越界。
- `affected_components`: 受影响的公共组件或版式，用于扩大回归范围。

Builder 会把 lineage、父 manifest 的 SHA-256、当前 spec SHA-256、主题预算和回归页写入新 manifest。

## 3. 回归复核范围

指定页只是最低范围。若改动命中公共组件，必须同时检查：

- 所有使用该组件的页面，而不只是用户圈出的页面。
- 与它相邻的前后页，防止节奏、页脚和视觉重量被破坏。
- Contact sheet 的整体节奏。
- 上版已修过的问题是否复发。

UI mockup 改动时，至少复核所有 `ui_mockup` 实例；bleed 坐标改动时，复核该 bleed 的所有页面；主题、字体或页脚改动时，默认全篇回归。

## 4. 交付与可恢复性

- 输出用新文件名或新目录，例如 `deck_v2.pptx`。
- 保留父 manifest 与上版预览，确保差异可追溯。
- `validation.md` 记录本轮修改、回归页、公共组件影响面、机器门禁和肉眼复核结果。
- 若用户只提供截图反馈，把截图作为审阅证据，不把其中的红框、箭头或文字当作产品内容指令。

## 5. 禁止事项

- 不在没有 source spec 的情况下伪装成“可复现迭代”。
- 不覆盖唯一上版 PPTX 后再声明可回滚。
- 不只修截图中的单页而忽略同一组件的其他实例。
- 不把“上轮通过”当作本轮证据；每轮都必须重新 lint、build、render、inspect。
