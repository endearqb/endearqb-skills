# 生成、渲染与交付 QA 清单

> Skill 路径：`product-story-pptx/references/qa-checklist.md`

质量检查分三层，缺一不可：

1. **Spec lint**：检查内容规则与叙事节奏。
2. **PPTX inspect**：检查文件结构、越界、字体、分辨率与潜在溢出。
3. **Eyes on pixels**：查看 contact sheet 与逐页 PNG，判断裁切、对比度、节奏和审美。

机器能抓到错误，但不能替你判断“这一页是不是太吵”“这张图有没有把主体裁坏”。

## 1. 标准命令

```bash
python scripts/lint_deck.py project/spec.yaml
python scripts/build_deck.py project/spec.yaml project/out/deck.pptx
python scripts/render_preview.py project/out/deck.pptx --dpi 120 --cols 4
python scripts/inspect_pptx.py project/out/deck.pptx
```

门禁：

- lint：0 FAIL。
- inspect：0 ERROR。
- WARN 全部逐条解释或修复。
- 已打开 contact sheet。
- 已逐页查看全部 PNG。
- 至少完成一轮修正与重建。

## 2. Spec lint 检查什么

### L00 Schema

- 顶层 `deck` 与 `slides`。
- 必填字段与枚举。
- Energy 为 1–5 整数。
- Language 为 zh/en。

### L01 Action title

- 标题非空。
- 中文 ≤ 24 字，英文 ≤ 14 词。
- 不是“产品介绍”“市场规模”等话题标签。

### L02 Type ↔ bleed

- 页面类型与图片模式兼容。

### L03 Energy

- 开场、早期低谷、结尾峰值、变化幅度与连续性。
- 高峰是否配强视觉。
- 峰值前是否有反差。

### L04 Bleed budget

- Full + color-block ≤ 40%。
- Full 不连续三页。
- 至少三种 bleed 且包含 none。

### L05 / L10 图片

- 需要图片的页面有文件。
- Full/overlay 有 scrim。
- 满版图宽 ≥ 1920px。
- 压图页文案不过量。

### L06 / L07 数据

- 连续图表 ≤ 2。
- 图表类型受控。
- Highlight ≤ 2。
- Source 必填。
- 数据长度与类型合法。
- 示例数据显式标注。

### L08 流程

- 3–7 个节点。
- 恰好一个高亮。
- Label 短。

### L09 文字

- Body、bullet 条数和长度在预算内。

### L11–L14

- 主题存在。
- 版式不连续重复。
- Cover/closing 与 CTA。
- Big Idea、audience、desired action 完整。

### L15–L18

- `topic_budgets` 是否在 min/max 篇幅范围内。
- iteration lineage 是否指向真实父 manifest，回归页是否有效。
- `ui_mockup` 字段、适用 type/bleed、示意标识与密度是否合法。
- `media_bars` 是否 3–5 条、每条一图、宽度和高亮受控。

## 3. Inspect 检查什么

### ERROR：必须修复

- 形状越界。
- 空占位符或占位文字。
- 字号 < 9pt。
- 图片有效分辨率 < 72ppi。
- PPTX 无法打开。

### WARN：必须看渲染图判断

- 疑似文字溢出。
- 非页脚字号 < 12pt。
- 图片有效分辨率 < 110ppi。
- 文字框显著重叠。
- 连续纯文字页。
- 非 16:9 画布。
- 重复 UI mockup 的圆角、标题栏高度或内边距漂移。

### INFO

- 实际字体清单。
- 页数与画布。
- UI mockup 实例数量。

## 4. Contact sheet 巡检

先看缩略图，不读文字，回答：

- 三幕是否能被看见？
- 章节断点是否明显？
- 峰值是否稀缺？
- 是否连续出现三页同一种构图？
- 图表页之后是否有换气？
- 明暗与色彩是否有稳定节奏？
- 是否有一页明显比其他页“像另一个模板”？

如果只看缩略图就觉得拥挤，放大后不会变好。

## 5. 逐页视觉检查

### 文字

- 是否截断、溢出或被意外换行？
- 标题是否一眼可读？
- 正文是否能在投影距离阅读？
- 行宽是否过长？
- 标点与数字格式是否一致？
- 中文字体是否变成方块或回退到宋体？

### 对齐

- 标题左边缘是否对齐网格？
- 图表、流程与标题带是否对齐？
- 相同类型页面的基线是否稳定？
- 页脚是否落在可读背景上？

### 图片

- 是否拉伸？
- 是否裁到脸、logo、接口、关键 UI？
- 焦点是否与文字竞争？
- Full 页是否有足够负空间与 scrim？
- 相邻图片色温与风格是否一致？

### 图表

- 标题是否已说结论？
- 高亮是否唯一明确？
- 其他数据是否退后但仍可读？
- 标签、单位、来源是否清楚？
- 柱状图是否从 0 开始？
- 图表是否大到足以阅读，而非被缩成装饰？

### 流程图

- 方向是否 3 秒可懂？
- 节点是否等大等距？
- 箭头是否安静？
- 高亮节点是否与标题一致？
- 标签是否短到能扫读？

### 对比度

- 暗色图上的文字是否清晰？
- Muted 是否投影后消失？
- Accent 是否过多？
- 页脚是否在浅色图片上变灰？

### 可编辑 UI mockup

- 外框、标题栏和内容区是否形成一个整体？
- 标题栏是否落在 shell 内，divider 是否贴合下沿？
- 同类页面的圆角、标题栏高度和内边距是否一致？
- 是否明确标注“界面示意”，避免被当成真实产品截图？
- 是否复核了所有重复实例，而不只看用户指出的一页？

## 6. 内容检查

- 每页 action title 是否推进 Big Idea？
- 数字在标题、图表、备注和讲稿中是否一致？
- 产品名、功能名、单位与术语是否统一？
- 所有示例/虚构数据是否明确标注？
- 所有合成占位图是否列入待替换清单？
- Quote 是否有真实来源或明确标注为示例？
- 是否存在用户未提供却被写成事实的声明？

## 7. 演讲节奏检查

快速翻页并模拟讲述：

- 每页能否用一句话解释存在理由？
- 第一幕是否建立了真实代价？
- Reveal 前是否有停顿或低谷？
- 功能段是否在体验和机制之间交替？
- 证据是否在观众产生质疑时出现？
- Closing 是否给出明确行动，而不是“谢谢”？
- 总建议时长是否给停顿和互动留出 10% 缓冲？

## 8. 修复优先级

### 文字问题

```text
删字 → 拆页 → 换 type → 调整框 → 最后微调字号
```

不要先把字体缩小。

### 图片问题

```text
调 image_focus → 调 scrim → 改 bleed → 换图
```

### 节奏问题

```text
改页面顺序 → 调 energy → 调 bleed → 换 type
```

### 图表问题

```text
重写 action title → 决定 highlight → 删系列/类别 → 换图表类型
```

## 9. 可复现修复

只修改：

- `spec.yaml`
- `assets/design-tokens.yaml`
- `assets/layout-registry.yaml`
- `scripts/*.py`

不要直接拖动 PPTX 中的元素作为最终修复。否则：

- 下一次构建会丢失。
- 无法复现。
- 机器门禁无法保护。
- 团队无法审查差异。

多轮迭代还必须保留父 manifest，在 `deck.lineage` 中声明版本、变更摘要、回归页和受影响公共组件；具体规则见 `iteration-lineage.md`。

## 10. Validation 文档模板

```markdown
# Validation

- Spec: project/spec.yaml
- Output: project/out/deck.pptx
- Generated at:
- Slides:
- Big Idea:
- Energy:
- Bleed:

## Machine gates
- lint: 0 FAIL / X WARN
- inspect: 0 ERROR / X WARN
- render: PASS / FAIL

## Visual review
- Contact sheet reviewed: yes/no
- All full-resolution slides reviewed: yes/no
- Refinement rounds: N

## Remaining placeholders
- ...

## Known limitations
- ...
```

## 11. 最终签字条件

只有以下全部为真，才能交付：

- [ ] `lint_deck.py` 返回 0。
- [ ] `inspect_pptx.py` 返回 0。
- [ ] LibreOffice 成功导出 PDF。
- [ ] Contact sheet 已查看。
- [ ] 所有逐页 PNG 已查看。
- [ ] 已至少修正并重新构建一轮。
- [ ] 示例数据和合成图片已声明。
- [ ] PPTX、manifest、preview 与 validation 均存在。
