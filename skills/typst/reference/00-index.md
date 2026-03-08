# Typst Reference Index

## 基线

- 官方基线：`Typst 0.14.2`
- 主权威源：`typst/docs/reference/**`、`typst/docs/tutorial/**`、`typst/docs/guides/**`、`typst/docs/changelog/**`
- 全量跨源索引：`reference/generated/typst-reference.json`
- 轻量官方索引：`reference/08-generated/typst-api-index.json` 与 `reference/08-generated/typst-api-index.md`
- 中文经验补强：`The Raindrop-Blue Book/src/**`

## 任务路由

- 编译、导出、调试：`01-workflows/compile-debug-publish.md`
- 项目结构、模板、包：`01-workflows/project-templates-and-packages.md`
- 语言层：`02-language/`
- 官方库分类：`03-library/`
- 模块组：`04-modules/std-calc-sys-sym-emoji.md`
- 中文 recipes：`05-recipes/`
- CLI / 源码地图：`06-dev/`
- 版本与蓝皮书时效：`07-versioning/`
- 根级补充说明：`overview.md`、`source-map.md`、`workflows.md`

## 索引使用建议

- 默认先用 `python scripts/query_reference.py --query <keyword>` 做跨源搜索。
- 如果已知大致 API 名称，或只想查官方 inventory，用 `python scripts/query_api_index.py --name <keyword>`。
- 搜索结果一旦命中源码位置，就回查原始 `typst` 文件确认最终行为。

## 刷新机制

- 更新本地上游后运行 `python scripts/build_reference.py`
- 如需同步轻量官方索引，再运行 `python scripts/refresh_typst_knowledge.py`
- 如果 Typst 版本变化，必须同步更新 `07-versioning/`
