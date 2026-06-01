# 模板：Design-Delegate-Iterate（设计-委托-迭代）

## 适用场景
产出物有明确设计标准，需先做统一设计再分发创建，并需质量检查和迭代修正。典型场景：PPT 制作、UI 设计、标准化文档。

## 不适用场景
无统一格式要求、时间极短无法迭代、各部件间无关联。

## Agent 需求

| 角色 | 数量 | 职责 |
|------|------|------|
| Orchestrator (Designer) | 1 | 制定设计规范、质量检查、迭代修正 |
| Worker | 2-N | 按规范创建各部件 |

## 流程图

```
Orchestrator: Design Spec + Outline -> Create Master Template (shared/)
  -> Worker 1 (dim01/, Create Part 1)   --
  -> Worker 2 (dim02/, Create Part 2)     |-- Parallel Creation
  -> Worker N (dimN/,  Create Part N)   --
  -> Orchestrator: Check All
       -> Issues Found? -> Yes: Iterate+Fix (loop back，受 max_iterations 上限约束)
                         -> No:  Deliver
```

## 终止条件与上限（有界 Ralph）

本模板的 P5-Check → P6-Iterate 是 Ralph 式"批评→修复→再检查"回路，**必须有界**，遵守 SKILL.md `Refinement Loop` 的护栏：

1. **迭代上限** `max_iterations`：默认 2，绝对不超过 3。达到上限 → 交付当前最佳版本 + 标注遗留问题。
2. **收敛判据**：每轮用可度量信号（问题清单条数、合规项数）记录进度，写入 `{任务根}/refine_log.md`。
3. **无改进即停**：若某轮问题数相比上轮没有减少，回滚到上轮最佳版本并停止，不再迭代。
4. **范围锁定**：每轮只修复 P5 问题清单里**已定位**的具体缺口，不得整体重做或扩大范围。

## Phase 分解

| Phase | 执行者 | 输入 | 输出 | Gate |
|-------|--------|------|------|------|
| P1-Design | Orchestrator | 任务需求 + 设计约束 | 设计规范 + 大纲 | **Document Gate** |
| P2-Create-Master | Orchestrator | 设计规范 | shared/ 内主模板/框架 | 主文件合规 |
| P3-Delegate | Orchestrator | 大纲 + 规范 | Worker 任务分配 + dim 分配 | 理解规范 |
| P4-Create | Workers(并行) | 任务 + shared/模板 + 规范 | 各 dim{编号}/ 内部件产出 | 格式合规 |
| P5-Check | Orchestrator | 所有 dim 内部件 + 规范 | 检查报告 + 问题清单 | **Quality Gate** |
| P6-Iterate | 相关 Worker | 问题清单 | 修正后部件（原 dim 目录内） | 问题全解 |
| P7-Deliver | Orchestrator | 所有部件 | output/ 内最终整合产物 | **Quality Gate** |

## 具体示例

**示例 A：PPT 制作** —— 制定视觉规范 + 15 页大纲，创建母版放入 shared/ 后分发给 3 Worker 各做 5 页，检查修正后输出最终 PPT。

**示例 B：标准化 API 文档集** —— 制定文档格式规范 + 目录，创建模板后分章节并行编写，检查交叉引用后输出完整文档集。

## 变体
| 变体 | 说明 |
|------|------|
| **DDI with Reviewer** | 引入独立 Reviewer Agent |
| **Fast DDI** | 跳过迭代一次性交付 |
| **Hierarchical DDI** | Worker 内部再次使用 DDI |
