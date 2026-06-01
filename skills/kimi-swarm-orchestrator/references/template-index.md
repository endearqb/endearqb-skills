# Swarm 工作流模板索引

> Orchestrator 在 Phase 1 根据任务特征选择模板，然后加载对应的模板文件。

## 模板选择指南

| 任务特征 | 推荐模板 | 文件 | 判断标准 |
|---------|---------|------|---------|
| 可分解为 3+ 独立子任务 | **Split-Parallel-Merge** | `templates/split-parallel-merge.md` | 横向拆分后各模块可独立执行 |
| 需先探索全景再深入 | **Explore-Dive-Verify** | `templates/explore-dive-verify.md` | 范围不明，先扫描再聚焦 |
| 有明确设计标准需反复打磨 | **Design-Delegate-Iterate** | `templates/design-delegate-iterate.md` | 产出有格式/审美要求（**有界 Ralph 式迭代**） |
| 需评估/对比某个能力 | **Paired-Evaluation** | `templates/paired-evaluation.md` | 有明确评估维度和基线 |
| 有严格阶段依赖和锁定点 | **Staged-Pipeline** | `templates/staged-pipeline.md` | 后续阶段依赖前阶段冻结产出 |
| 需根据中间结果动态调整 | **Adaptive-Routing** | `templates/adaptive-routing.md` | 无法预规划完整路径（**有界 ReAct 式自适应**） |

> **循环模板的强制约束**：Design-Delegate-Iterate 与 Adaptive-Routing 都含回路结构。凡使用回路，**必须**遵守 SKILL.md `Refinement Loop` 章节的三条硬约束——迭代上限、收敛判据、无改进即停。无终止条件的回路视为缺陷。

### 组合使用

- **简单任务**：单模板
- **复杂任务**：2-3 个模板嵌套
- **大型项目**：顶层 Staged-Pipeline，各阶段内嵌其他模板

```
嵌套示例：
Staged-Pipeline
  Stage 1: Explore-Dive-Verify（需求调研）
  Stage 2: Design-Delegate-Iterate（方案设计）
  Stage 3: Split-Parallel-Merge（并行实现）
  Stage 4: Paired-Evaluation（质量评估）
```

---

## Gate 模式详解

Gate 是工作流关键检查点，确保质量达标后才进入下一阶段。

### Document Gate（文档门）

确保关键文档/设计完成后才能进入下一阶段。

| 检查项 | 说明 |
|--------|------|
| 完整性 | 文档是否覆盖所有必要内容 |
| 清晰性 | 文档是否无歧义，可被 Worker 理解 |
| 一致性 | 文档内部是否逻辑自洽 |
| 可行性 | 文档定义的规范是否可执行 |

**适用模板**：Design-Delegate-Iterate、Staged-Pipeline

### Merge Gate（合并门）

确保所有并行分支完成后才能进入整合阶段。

| 检查项 | 说明 |
|--------|------|
| 完整性 | 所有 `dim{编号}/` 产出是否都已完成 |
| 格式一致性 | 各 Worker 产出是否遵循统一格式 |
| 冲突检测 | 各 Worker 产出之间是否有重叠或矛盾 |

**适用模板**：Split-Parallel-Merge、Staged-Pipeline

### Quality Gate（质量门）

确保产出质量达标后才能交付。

| 检查项 | 说明 |
|--------|------|
| 正确性 | 产出内容是否正确无误 |
| 完整性 | 是否覆盖所有需求 |
| 一致性 | 是否符合设计规范/标准 |
| 可用性 | 是否可直接使用 |

**适用模板**：所有模板

### Gate 组合

```
单 Gate：Quality Gate（交付前检查）
双 Gate：Document Gate -> Merge Gate（先设计后合并）
三 Gate：Document Gate -> Merge Gate -> Quality Gate（完整流水线）
```

---

## 自定义模板指南

### 组合原则

1. **自顶向下**：先用 Staged-Pipeline 划分大阶段
2. **由内向外**：每个阶段内选择适合模板
3. **Gate 连接**：阶段间用 Gate 保证质量
4. **反馈闭环**：评估阶段用 Paired-Evaluation

### 常见组合模式

| 组合名称 | 结构 | 使用场景 |
|---------|------|---------|
| **研究-创作** | Explore-Dive-Verify -> Design-Delegate-Iterate | 先研究再创作 |
| **构建-评估** | Split-Parallel-Merge -> Paired-Evaluation | 实现后评估质量 |
| **完整流水线** | Staged-Pipeline(Explore->Design->Split->Evaluate) | 大型项目全周期 |
| **快速迭代** | Adaptive-Routing + Design-Delegate-Iterate | 不确定方案时反复迭代 |

### 自定义检查清单

- [ ] 任务是否可预先分解？（是 -> SPM，否 -> AR）
- [ ] 是否需要先探索？（是 -> EDV）
- [ ] 是否有统一设计规范？（是 -> DDI）
- [ ] 是否需要评估对比？（是 -> PE）
- [ ] 是否有阶段依赖？（是 -> SP）
- [ ] 是否 3+ 子任务可并行？（是 -> SPM）

### 示例：大型项目完整工作流

```
Phase 1: Explore-Dive-Verify -> 需求文档 + 技术选型报告
Phase 2: Design-Delegate-Iterate -> 架构文档 + 接口规范 + UI 原型
Phase 3: Staged-Pipeline
  Stage 3.1: Scaffold（类型/接口冻结）
  Stage 3.2: Split-Parallel-Merge（多模块并行实现）
  Stage 3.3: 集成 + 测试
  -> 输出：可运行应用
Phase 4: Paired-Evaluation -> 评估报告 + 优化建议
```
