# 可编辑 UI mockup 公共组件

> Skill 路径：`product-story-pptx/references/editable-ui-mockups.md`

当真实产品截图缺失、分辨率不足，或需要在 PPT 内继续编辑时，可用原生 PowerPoint 形状构造“界面示意”。它是解释产品机制的演示组件，不是伪造已上线产品。

## 1. 使用方式

`feature_hero` 或 `split` 页面可用 `ui_mockup` 替代 `image`：

```yaml
ui_mockup:
  title: "园区运营总览"
  theme: dark
  badge: "界面示意"
  sidebar: ["总览", "事件", "资产"]
  headline: "对象、事件和责任同屏"
  subhead: "可编辑原生形状 · 非真实产品截图"
  kpis:
    - {label: "在园企业", value: "326"}
    - {label: "运行事件", value: "18", highlight: true}
  items:
    - {label: "设备告警", value: "处理中", highlight: true}
    - {label: "企业诉求", value: "待复核"}
```

支持 `theme: light | dark`。同一 deck 的同类界面应共享 theme、圆角、标题栏高度和内容内边距。

## 2. 几何不变量

公共 renderer 必须生成一个整体外框，不得让标题栏像悬浮贴片：

- 单一 `SHELL` 定义整体轮廓。
- `TOPBAR` 位于 shell 内部，左右内缩一致。
- `TOPBAR_JOIN` 覆盖圆角标题栏下沿，使标题栏与内容区连续。
- `DIVIDER` 紧贴标题栏底部。
- 默认 shell 圆角约 `0.18in`，合理范围 `0.08–0.30in`。
- 标题栏高度约 `0.50in`；重复实例差异不得超过 `0.03in`。
- 阴影和主题 effect 必须关闭，避免不同 PowerPoint 主题注入意外外发光。

所有关键形状命名为 `PST_UI_MOCK_<ROLE>::<instance>`，供 `inspect_pptx.py` 做实例级 QA。

## 3. 内容密度

- Sidebar 0–5 项。
- KPI 0–3 个。
- 内容条目 0–4 个。
- 只展示足以支持本页 action title 的字段。
- 不复制完整后台系统；投影环境下读不清的小表格、密集图标和长字段应删除。

## 4. 重复实例 QA

结构检查应确认每个实例都有 shell、topbar、join 和 divider，并检查：

- topbar 是否落在 shell 内。
- divider 是否与标题栏底部对齐。
- shell 是否关闭主题 effect。
- 圆角、标题栏高度、内边距在重复实例间是否一致。

肉眼检查还要确认：

- 整个 mockup 看起来是一台完整 app，而非多个拼接卡片。
- 同一交互状态的强调色语义一致。
- “界面示意”标识清晰，但不抢主标题。
- 页面上的 UI 是主证据时足够大；否则宁可删细节。

## 5. 何时不用

- 已有高质量真实截图：优先真实截图。
- 需要像素级复刻现有 UI：在设计工具中完成，再以图片置入。
- 用户要求任意形状都可编辑但内容极复杂：拆成多页或只画关键路径。
