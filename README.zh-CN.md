# Typst Skill

[English](README.md)

帮助 Agent 编写、修改、调试和迁移真实 Typst 项目的技能。以 **2026-10-09 核实的最新稳定版 Typst 0.15.1** 为基线。

新设计从用户的文档、编译器和交付格式出发：短入口、按任务读取的指南、统一的官方文档查询工具。要求实际编译，并在版式或导出任务中检查相应结果。

## 能做什么

- 文档与组件编写，`set`/`show`、上下文、状态、计数器和错误定位。
- 数学、数据表格、参考文献、中文排版及长文档布局。
- 模块、模板、包，PDF/PNG/SVG、实验性 HTML/bundle，以及 0.15 迁移。
- 离线定位官方 API、参数、作用域成员、符号和 typed HTML；按需获取官方完整段落并缓存，保留来源和版本信息。

目录索引保存检索位置，不复制整本手册，也不从 Rust 签名猜测 Typst API。完整 API 说明首次读取需要联网；缓存和符号信息支持离线使用。工具检查网页宣告的版本差异，版本敏感问题仍需使用对应编译器或发布 tag 源码验证。

## 安装

```sh
npx skills add MoYeRanqianzhi/typst-skill@typst -g -y
```

也可以将整个 `skills/typst/` 目录复制到 Agent 的技能目录。只安装 `SKILL.md` 会缺少引用指南和工具。详见[安装说明](docs/INSTALL.md)。

示例请求：

> 使用 $typst，将这份 CSV 制作成中文报告，包含重复表头、编号公式和 PDF，保留项目现有风格，并验证结果。

## 查询官方文档

在本仓库执行：

```sh
python skills/typst/scripts/docs.py search "table.cell"
python skills/typst/scripts/docs.py show "table.cell:colspan"
python skills/typst/scripts/docs.py show "sym.arrow.r.squiggly" --offline
python skills/typst/scripts/docs.py status --check-latest
```

脚本可从其他工作目录执行，也可在单独安装的技能目录中使用。`figure.caption` 表示作用域函数，`figure:caption` 表示参数；冒号只是检索记法，不是 Typst 语法。详见[检索与版本边界](skills/typst/references/docs-and-versions.md)。

## 依赖与维护

- 查询工具只需要 **Python 3.11+ 标准库**。
- 编译需要 Typst CLI；指南和示例基于 **0.15.1**，不会自动升级用户项目。
- 文档需要相应字体；技能不会自动安装字体或编译器。
- 使用技能不需要源码仓库、蓝皮书仓库、Cargo 或 PyYAML。

贡献者文档：[设计与维护](docs/maintenance.md)、[验证说明](docs/validation.md)、[已知限制](docs/known-issues.md)。

项目代码及原创指南采用 MIT 许可；索引中的官方 API 名称、符号和地址保留来源信息，链接或下载的上游文档遵循各自许可。
