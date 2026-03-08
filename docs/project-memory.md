# Project Memory

## 项目简介

- 项目名称：`Typst Skill`
- Skill 名称：`typst`
- 目标：提供面向 `Typst 0.14.2` 的完整 Agent Skill，覆盖官方开发规范、语言参考、库 API 索引、调试流程、蓝皮书中文实践与版本风险提示。

## 当前基线

- 官方源码快照：`./typst`
- 中文蓝皮书快照：`./The Raindrop-Blue Book`
- 官方稳定版本：`Typst 0.14.2`
- 蓝皮书依赖版本：存在 `0.11/0.12/0.13.1` 混合痕迹，必须通过版本文档兜底。

## 目录约定

- `skills/typst/`：Skill 主体。
- `skills/typst/SKILL.md`：SOP 与调度逻辑。
- `skills/typst/scripts/build_reference.py`：全量跨源索引构建器。
- `skills/typst/scripts/query_reference.py`：全量跨源查询入口。
- `skills/typst/scripts/refresh_typst_knowledge.py`：轻量官方索引刷新器。
- `skills/typst/scripts/query_api_index.py`：轻量官方索引查询器。
- `skills/typst/reference/`：按任务和主题拆分的参考资料。
- `skills/typst/reference/generated/`：综合索引产物。
- `skills/typst/reference/08-generated/`：轻量官方 API inventory。
- `docs/`：项目长期记忆与维护记录。

## 维护与刷新流程

1. 更新本地 `typst` 或蓝皮书快照。
2. 运行 `python skills/typst/scripts/build_reference.py`。
3. 运行 `python skills/typst/scripts/refresh_typst_knowledge.py`。
4. 检查 `skills/typst/reference/generated/` 与 `skills/typst/reference/08-generated/`。
5. 如 Typst 版本变化，更新 `skills/typst/reference/07-versioning/`。
6. 运行 `python C:/Users/MoYeR/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/typst`。

## 设计决策

- 以“`SKILL.md` 负责调度，`reference/` 负责知识承载”为核心。
- 以官方 Typst docs/source 为主，蓝皮书用于中文经验、案例和模板模式补强。
- 同时保留“综合索引”和“轻量官方 inventory”，兼顾覆盖率与查询速度。

## Encoding

- All Skill and docs files should be stored as UTF-8.
