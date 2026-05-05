# Typst Skill

> **当前覆盖的 Typst 版本: `0.14.2`**

一个面向 AI Agent 的 [Typst](https://typst.app) 专家技能，提供源码级 API 查询、分层参考文档和标准工作流。

## 特性

- **智能路由** — 根据任务类型（创建 / 调试 / 解释 / 模板）自动导航到最相关的参考文档
- **33 篇分层参考文档** — 涵盖工作流、语言核心、标准库、配方、版本变更，均包含可运行代码示例
- **双索引查询系统** — `query_reference.py`（广覆盖：API + 文档 + 蓝皮书 + grep）和 `query_api_index.py`（快速官方索引）
- **中文排版支持** — 字体配置、中英混排、引号陷阱警告、标点规则，基于《雨滴蓝皮书》
- **渐进式披露** — L1 描述 (~30 词) → L2 SKILL.md (97 行) → L3 按需加载参考文档和脚本

## 快速开始

### 安装

```bash
npx skills add MoYeRanqianzhi/typst-skill@typst -g -y
```

> 更多安装方式（手动安装、无 npx 环境等）请参阅 [docs/INSTALL.md](docs/INSTALL.md)

### 发送给任意 AI Agent

将以下内容复制发送给你的 AI Agent 即可自动安装：

```
Install the Typst skill by following the instructions at: https://raw.githubusercontent.com/MoYeRanqianzhi/typst-skill/main/docs/INSTALL.md
```

### 验证

安装后，向 Agent 提问：

```
帮我写一个 Typst 中文学术论文模板
```

如果技能加载成功，Agent 会通过 SKILL.md 路由到 `book-paper-slide-cv-patterns.md` 和 `chinese-typesetting.md`，并产出可编译的 Typst 代码。

## 目录结构

```
skills/typst/
├── SKILL.md                       # 核心 SOP — 路由、工作流、权威层级
├── scripts/                       # 确定性查询工具
│   ├── query_reference.py         # 广覆盖查询（API + 文档 + 蓝皮书 + grep）
│   ├── query_api_index.py         # 快速官方 API 索引查询
│   ├── build_reference.py         # 构建综合引用数据库
│   └── refresh_typst_knowledge.py # 刷新 API 索引
└── reference/                     # 33 篇分层参考文档
    ├── 01-workflows/              # 编译、调试、发布、模板
    ├── 02-language/               # 标记、样式、脚本、数学
    ├── 03-library/                # 布局、文本、模型、可视化等
    ├── 05-recipes/                # 简历、论文、幻灯片、中文排版
    ├── 07-versioning/             # 版本变更、蓝皮书差异
    └── 08-generated/              # 自动生成的 API 索引
```

## 工作原理

```
用户请求 → SKILL.md 路由表 → 最小匹配参考文档 → query_reference.py 精确查询 → 生成可运行代码
```

**权威层级**: 官方源码 > 生成索引 > 蓝皮书

**路由流程**:
1. Quick intent check — 创建 / 解释 / 修复 / 修改
2. Error triage — 语法 / 类型 / 字体 / 状态 / 布局 / 版本
3. Subsystem routes — 按子系统精确导航
4. Creating from scratch — 快速起步路径

## 测试结果

使用"可爱小猫简历"作为端到端测试：

| 维度 | v0.3.0 | v0.4.0 | 变化 |
|------|:------:|:------:|:----:|
| 路由体验 | 4/5 | 5/5 | +1 |
| 参考文档 | 3/5 | 4.7/5 | +1.7 |
| 脚本工具 | 4/5 | 4/5 | — |
| 编写体验 | 4/5 | 4.8/5 | +0.8 |
| **综合** | **3.75** | **4.6** | **+0.85** |

## 依赖

- **Python 3.10+** — 查询脚本运行环境
- **Typst CLI** — 编译 `.typ` 文件 ([安装](https://github.com/typst/typst/releases))
- **PyYAML** — `refresh_typst_knowledge.py` 需要 (`pip install pyyaml`)

## 许可

MIT
