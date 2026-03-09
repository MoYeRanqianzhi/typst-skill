# Changelog

## 2026-03-09

- 初始化根仓库并建立 `skills/typst/` 与 `docs/` 结构。
- 基于本地 `typst` 官方源码与中文蓝皮书设计 `typst` Skill 信息架构。
- 完成 `SKILL.md`、`agents/openai.yaml`、分层参考文档与版本说明。
- 接入已有的 `build_reference.py` / `query_reference.py` 综合索引链路。
- 新增 `refresh_typst_knowledge.py` 与 `query_api_index.py`，补充轻量官方 inventory。
- 生成 `reference/generated/` 与 `reference/08-generated/` 下的索引产物。
- Finalized support-doc roles, added accessibility and HTML recipe, and normalized several reference pages to remove encoding-risk content.
