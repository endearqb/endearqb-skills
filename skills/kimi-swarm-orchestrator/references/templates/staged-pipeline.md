# 模板：Staged-Pipeline（分阶段流水线）

## 适用场景
任务有严格阶段依赖，前一阶段产出是后一阶段输入，需在特定节点冻结。典型场景：软件构建、数据处理流水线。

## 不适用场景
阶段间无依赖可并行、无法预定义阶段、需频繁回溯。

## Agent 需求

| 角色 | 数量 | 职责 |
|------|------|------|
| Orchestrator | 1 | 阶段管理、进度控制、最终整合 |
| Scaffold | 1（可选） | 创建基础设施和模板 |
| Worker | 2-N/阶段 | 各阶段执行者 |

## 流程图

```
Orchestrator: Define Stages + Freeze Points
  -> Stage 1: Scaffold (shared/) + Early Workers (dim01-N/) -> Freeze Core Definitions
  -> Stage 2: More Workers (dim01-N/) Implement -> Freeze Core Code
  -> Stage 3: All Workers Polish + Integrate
  -> Orchestrator: Final Merge -> Deliver (output/)
```

**阶段间目录复用**：每个 Stage 可以复用或新建 dim 目录。如果 Stage 2 的 Worker 需要读取 Stage 1 的产出，Orchestrator 负责在 Stage 间将冻结产出移入 `shared/` 供后续 Stage 读取。

## Phase 分解

| Phase | 执行者 | 输入 | 输出 | Gate |
|-------|--------|------|------|------|
| P1-Define | Orchestrator | 项目需求 | 阶段计划 + 冻结点定义 | 划分合理 |
| P2-Stage1 | Scaffold+Workers | 阶段计划 | Stage1 冻结产出（移入 shared/） | **Document Gate** |
| P3-Stage2 | Workers | shared/ 内 Stage1 冻结产出 | Stage2 冻结产出 | **Merge Gate** |
| P4-Stage3 | Workers | Stage2 冻结产出 | Stage3 产出 | **Merge Gate** |
| P5-Final | Orchestrator | 所有阶段产出 | output/ 内整合完整产物 | **Quality Gate** |
| P6-Deliver | Orchestrator | 整合产物 | 最终交付物 | **Quality Gate** |

## 具体示例

**示例 A：渐进式软件开发** —— Stage1 定义类型/接口并冻结 types.ts 到 shared/，Stage2 基于冻结类型实现业务逻辑，Stage3 做 UI/集成测试后构建交付。

**示例 B：数据处理流水线** —— Stage1 清洗数据输出标准化数据集到 shared/(冻结)，Stage2 特征工程(冻结)，Stage3 分析建模后验证端到端正确性交付报告。

## 变体
| 变体 | 说明 |
|------|------|
| **Overlapping Pipeline** | 前一阶段未完全结束即启动下一阶段 |
| **Conditional Pipeline** | 根据中间结果跳过后续阶段 |
| **Nested Pipeline** | 每个阶段内部使用其他模板 |
