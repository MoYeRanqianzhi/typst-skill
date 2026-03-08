# Typst Skill Shared Memory

## 项目简介

- 项目名称：Typst Skill
- Skill 名称：`typst`
- 目标：基于本地 `typst` 源码仓库与 `The Raindrop-Blue Book` 中文蓝皮书，构建一个可追溯、可验证、可解释的 Typst Agent Skill。

## 目录约定

- Skill 主目录：`skills/typst/`
- 持久化文档：`docs/`
- 上游官方源码：`typst/`
- 上游中文蓝皮书：`The Raindrop-Blue Book/`

## 当前实现策略

1. 使用 `npx skills init typst` 初始化 `skills/typst/SKILL.md`。
2. 使用本地 Typst 官方源码与官方 docs 源文件作为第一事实来源。
3. 使用中文蓝皮书作为中文示例、教程、模板、包与插件实践来源。
4. 使用 `skills/typst/scripts/build_reference.py` 构建机器可检索索引。
5. 使用 `skills/typst/scripts/query_reference.py` 统一查询 API、官方文档、蓝皮书与原始源码 grep 结果。

## 已确认的上游信息

- Typst 版本：`0.14.2`
- Typst 当前提交：`364ece3cb37975f509a779fc3ddc929285971d73`
- Typst 远程：`https://github.com/typst/typst`
- 蓝皮书当前提交：`f8d51ad0cb99a886dbe347f0d71c4f3a49c1f59f`
- 蓝皮书远程：`https://github.com/typst-doc-cn/tutorial`

## 关键技术决策

- 决策：不依赖上下文记忆，所有重要事实写入本文件与 `skills/typst/reference/`。
- 决策：优先用本地源码和文档求证，不凭印象回答 Typst 语义。
- 决策：官方 `typst-docs` 可执行文档生成器在本机尝试构建时失败，因此当前采用“源码解析 + 本地缓存数据源”的轻量索引方案。

## 已知问题

- `cargo run -p typst-docs` 调试构建在 Windows 上触发 PDB/链接错误。
- `cargo run --release -p typst-docs` 受本机磁盘空间不足阻塞。
- 因此当前 `reference/generated/typst-reference.json` 不是 `typst-docs` 产出的官方 JSON，而是从源码、官方 docs 源、Cargo 缓存中的 `typst-assets` 与 `codex` 数据组合生成的索引。

## 使用说明

- 重建索引：`python skills/typst/scripts/build_reference.py`
- 查询 API：`python skills/typst/scripts/query_reference.py --name page`
- 模糊查询：`python skills/typst/scripts/query_reference.py --query wasm plugin`

## 后续待办

- 若环境允许，补充一次基于 `typst-docs` 二进制的官方 JSON 对照校验。
- 审视 `query_reference.py` 的命中质量，按真实使用反馈迭代权重与输出格式。
- 视需要补充更细粒度的 HTML typed attribute 查询展示。

## 更新日志

- 2026-03-09：初始化根仓库、创建 `skills/typst/` 与 `docs/`。
- 2026-03-09：确认本地 Typst 版本为 `0.14.2`，并核验 GitHub 最新 release 仍为 `0.14.2`。
- 2026-03-09：确认官方文档模型入口在 `typst/docs/src/model.rs`，但受本机构建限制改走源码索引方案。
- 2026-03-09：新增 `SKILL.md`、参考文档、索引构建脚本和查询脚本。
