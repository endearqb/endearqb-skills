# endearqb-skills

[English](README.md) | [简体中文](README.zh-CN.md)

这是一个用于存放可复用 Agent Skills 的开源仓库。

## 仓库说明

当前仓库包含：

- `endearqb-lab-report-writer`：用于期刊风格实验报告与技术报告撰写的技能，支持分段 HTML 生成、数据质量校验、写作逻辑自检、主题切换与可复用报告资产。
- `kimi-swarm-orchestrator`：通用多智能体编排框架，用于将复杂任务拆解为文档先行规划、隔离 Worker 目录、并行执行、错误恢复与有界精炼流程。
- `endearqb-frontend-dataviz`：用于前端数据可视化工作的技能，包含图表示例、配色方案、图标等参考资料。
- `endearqb-community-profiler`：用于群聊记录分析的技能，可生成成员画像、识别核心贡献者、评估社区健康度、总结聊天内容。
- `endearqb-svg-flowchart`：用于根据文字步骤生成高质量 SVG 流程图的技能，支持垂直/水平布局、判断分支、多列分组流程图，以及可选的 HTML 预览页输出。
- `endearqb-wechat-file-organizer`：用于整理 Windows 微信文件存储目录的技能，支持自动检测目录、重复文件分析、移入回收站去重，以及按月份和类型分类整理。
- `1nfinix-editorial-card-screenshot`：用于生成编辑部风格的 HTML 信息卡，并按固定比例截图输出 PNG，已补齐中文字体 fallback 与 Chromium 稳定截图链路。
- `readme-first-builder`：用于在项目中初始化或升级 README First 完整架构，包括 `AGENTS.md`、根 README、`.ai/changes`、`.ai/decisions` 与关键目录 README。

## 目录结构

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
```

每个 skill 目录通常包含：

- `SKILL.md`：技能说明
- `references/`：参考资料
- `scripts/`：辅助脚本

## 使用方式

克隆本仓库后，可将各个 skill 目录作为本地技能包，在 Agent Skills 工作流中直接使用。

## 贡献者

手动维护的贡献者名单见 [CONTRIBUTORS.md](CONTRIBUTORS.md)。

## 许可证

本项目采用 MIT License 开源，详见 `LICENSE` 文件。

## English README

英文说明见 `README.md`。
