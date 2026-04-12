# Reference 文档审查报告

- **审查日期**: 2026-04-12
- **审查范围**: `skills/typst/reference/` 下全部 33 个 `.md` 文件
- **审查基线**: Typst 0.14.2
- **审查维度**: 内容充实度、代码示例、实用性、准确性、覆盖度

---

## 一、整体评估

### 总体印象

参考文档体系**结构清晰、路由设计合理**，采用了编号目录 + 功能分层的组织方式，索引文件（`00-index.md`、`overview.md`、`workflows.md`、`source-map.md`）提供了良好的导航体验。文档在"引导 Agent 到正确的信息源"这一目标上做得不错。

### 核心问题

但几乎所有文档都存在以下**系统性缺陷**：

1. **严重缺乏代码示例** — 33 个文件中，**没有任何一个文件包含可运行的 Typst 代码片段**。文档只有概念描述、API 名称列表和规则条目，但没有展示"具体怎么写"。对于一个指导 Agent 编写 Typst 代码的参考系统来说，这是最关键的短板。

2. **内容普遍偏"骨架"** — 大多数文件在 25-50 行之间，给出了主题框架和注意事项，但缺乏深入的参数说明、行为细节、边界条件和实际使用模式。

3. **过度依赖外部查询脚本** — 许多文档的"精确查找"部分只给出 `query_reference.py` 或 `query_api_index.py` 的调用方式，而自身不包含足够的内联信息。当脚本不可用时，文档本身的价值大幅降低。

---

## 二、逐文件评分

### 评分标准

| 分数 | 含义 |
|------|------|
| 5 | 内容充实、有代码示例、可直接指导任务 |
| 4 | 内容较好、覆盖关键概念、但缺少部分示例或细节 |
| 3 | 框架完整但内容不够深入，缺少代码示例 |
| 2 | 仅有骨架/标题，内容过于简略 |
| 1 | 几乎无实质内容或有严重问题 |

---

### 根目录文件

| 文件 | 评分 | 简评 |
|------|------|------|
| `00-index.md` | 4 | 路由索引功能完善，策略清晰，版本基线明确。作为入口文件角色合适。 |
| `overview.md` | 3 | 极简路由图，完成了其设计目标（最短路径），但过于精简。 |
| `workflows.md` | 3 | 工作流程检查清单简洁有效，但缺少实际操作示例。 |
| `source-map.md` | 3 | 上游源码映射清晰，支持性文档角色合适，但对非 Rust 开发者缺少上下文。 |

### 01-workflows/

| 文件 | 评分 | 简评 |
|------|------|------|
| `compile-debug-publish.md` | **4** | **本系列最佳文档之一**。CLI 命令矩阵详细，环境变量覆盖全面，调试流程和发布检查清单实用。但缺少 CLI 使用的实际命令行示例。 |
| `project-templates-and-packages.md` | 3 | 项目布局建议和模板设计规则合理，`typst init` 说明有用。但缺少实际模板代码示例（如一个最小模板函数）。 |

### 02-language/ ⚠️ 重点关注

| 文件 | 评分 | 简评 |
|------|------|------|
| `markup-and-document-structure.md` | **2** | 核心概念仅 5 行，"结构热点"只是关键词列表。作为 Typst 最基础的文档，**严重缺乏代码示例**——没有展示 `#expr`、`[...]`、`{...}` 的实际用法，没有标题/列表/图表的标记示例。 |
| `math-and-symbols.md` | **2** | 列出了高价值主题但没有展开任何一个。内联 vs 块级方程、`mat`/`vec`/`cases`/`frac` 等核心语法完全没有示例代码。 |
| `scripting-and-context.md` | **2** | 脚本核心概念只用一句话概括。`let`、闭包、循环、`context`、`state` 等关键特性没有任何代码示例。调试分类有用但太简略。 |
| `styling-layout-and-show-rules.md` | **2** | `set`/`show` 规则是 Typst 最重要的特性之一，但文档只给出了概念描述，没有任何 `set page(...)` 或 `show heading: ...` 的实际代码。 |

### 03-library/ ⚠️ 重点关注

| 文件 | 评分 | 简评 |
|------|------|------|
| `data-loading.md` | 3 | 覆盖地图清晰（`json`、`csv`、`yaml` 等），指导规则合理。但缺少 `json("data.json")` 或 `csv("file.csv")` 的实际调用示例。 |
| `export-and-platform.md` | **4** | 后端差异说明到位，PDF/HTML 笔记有价值，版本信息准确。是较好的文档之一。 |
| `foundations.md` | **2** | 作为覆盖 209 个 API 的最大类别，文档只有 5 段泛泛描述。没有列出关键函数签名，没有代码示例，实用性很低。 |
| `introspection.md` | 3 | Key APIs 列表和使用规则有参考价值，版本笔记有用。但 `counter`/`state`/`query` 的用法没有代码示例。 |
| `layout.md` | **2** | 仅列出 Key API 名称和 4 条指导规则。`page`、`grid`、`stack`、`align` 等核心布局元素没有任何使用示例。 |
| `math.md` | **2** | 列出了关键函数族但没展开。Math 库是用户高频使用的领域，缺少公式代码示例是重大缺陷。 |
| `model.md` | **2** | 文档模型（heading、figure、table、bibliography）是 Typst 的核心，但文档只有骨架。 |
| `symbols.md` | 3 | 查找规则和常见陷阱有价值，但没有展示 `sym.arrow.r`、`emoji.cat` 等实际用法。 |
| `text.md` | **2** | 覆盖地图有用但所有条目（`highlight`、`raw`、`underline` 等）没有示例。 |
| `visualize.md` | 3 | API 家族列表较完整，设计规则合理。但 `rect`、`circle`、`image` 等没有代码示例。 |

### 04-modules/

| 文件 | 评分 | 简评 |
|------|------|------|
| `std-calc-sys-sym-emoji.md` | 3 | 主要模块和分组页面的说明有用。但 `calc.abs()`、`sys.inputs`、`sym.arrow` 等没有示例。 |

### 05-recipes/ ⚠️ 重点关注

| 文件 | 评分 | 简评 |
|------|------|------|
| `accessibility-and-html.md` | **4** | **本系列最佳文档之一**。工作流清晰，常见陷阱有针对性，精确查找命令具体。但仍缺少实际 Typst 代码示例（如 `figure.alt` 的用法）。 |
| `book-paper-slide-cv-patterns.md` | **2** | 模式矩阵只有概念描述，没有实际的模板代码。作为"配方"文档，应该提供可复用的代码片段。这对 Agent 生成简历、论文等任务至关重要。 |
| `chinese-typesetting.md` | **2** | 中文排版指导过于简略。没有字体配置示例、中英混排示例、标点处理示例。作为特色功能文档，内容严重不足。 |
| `plugins-html-pdf-svg-png.md` | 3 | 插件指导和后端清单有参考价值。但缺少插件使用的代码示例。 |
| `state-counter-query-locator.md` | 3 | 调试框架和版本笔记有实用价值。但 `counter`/`state`/`query` 这些最易出错的 API 没有代码示例来展示正确用法。 |
| `tables-figures-bibliography-outline.md` | **2** | 模式检查清单过于抽象。没有表格构建、图表包装、参考文献配置的实际代码。 |

### 06-dev/

| 文件 | 评分 | 简评 |
|------|------|------|
| `architecture-and-source-map.md` | **4** | 编译管道和 crate 映射清晰，对源码维护有实际指导价值。 |
| `cli-workspace-and-testing.md` | 3 | CLI 表面和参数族有用。调试策略简洁。但缺少实际命令行示例。 |

### 07-versioning/

| 文件 | 评分 | 简评 |
|------|------|------|
| `blue-book-gaps-and-staleness.md` | **4** | 版本漂移说明对正确使用 Blue Book 非常重要。证据链和安全使用规则都很实用。 |
| `whats-new-in-0.14.x.md` | **4** | 变更日志摘要清晰，升级规则明确。三个子版本的差异说明有价值。 |

### 08-generated/

| 文件 | 评分 | 简评 |
|------|------|------|
| `typst-api-index.md` | **4** | API 统计摘要和示例条目对了解库规模有用。作为生成文件角色合适。 |

### generated/

| 文件 | 评分 | 简评 |
|------|------|------|
| `summary.md` | 3 | 自动生成的统计摘要，角色合适。Blue Book commit 与 Typst commit 相同看起来可能有 bug。 |

---

## 三、最需要改进的 Top 5 文件

### 1. 🔴 `02-language/markup-and-document-structure.md` — 评分 2

**问题**: Typst 最基础的入门概念文档，但几乎没有实质内容。

**建议扩充内容**:
- `#expr`、`[content]`、`{code}` 三种模式的代码示例
- 标题层级（`=`, `==`, `===`）的完整示例
- 列表（`-`、`+`、`/`）的语法示例
- 标签和引用（`<label>`、`@ref`）的使用示例
- `import` 和 `include` 的区别示例
- 图表（`figure`、`table`）的基本包装示例

### 2. 🔴 `02-language/styling-layout-and-show-rules.md` — 评分 2

**问题**: `set`/`show` 规则是 Typst 区别于其他排版系统的核心机制，文档严重不足。

**建议扩充内容**:
- `set text(font: "...")` 基本用法示例
- `set page(margin: ...)` 页面配置示例
- `show heading: it => ...` 自定义标题样式示例
- `show link: set text(fill: blue)` 简写形式示例
- 选择器的种类和用法（元素选择器、标签选择器、`where` 过滤器）
- `set`/`show` 规则的作用域和层叠行为说明

### 3. 🔴 `05-recipes/book-paper-slide-cv-patterns.md` — 评分 2

**问题**: 作为"配方"文档，应该是最具实操性的内容，但只有概念框架。

**建议扩充内容**:
- 一个最小可用的论文模板函数（含 title、author、abstract）
- 一个最小可用的简历模板片段
- 一个最小可用的幻灯片页面设置
- 每种模式的完整 `.typ` 示例代码（可编译运行）

### 4. 🔴 `03-library/foundations.md` — 评分 2

**问题**: 覆盖 209 个 API 的最大类别，文档只有泛泛描述。

**建议扩充内容**:
- `array` 常用方法（`map`、`filter`、`join`、`sorted`）示例
- `dictionary` 操作示例
- `str` 方法（`split`、`trim`、`replace`）示例
- `calc` 模块关键函数（`abs`、`min`、`max`、`round`）示例
- `datetime` 和 `version` 类型的使用示例
- 类型转换函数（`int()`、`float()`、`str()`）示例

### 5. 🔴 `05-recipes/chinese-typesetting.md` — 评分 2

**问题**: 中文排版是项目的特色功能（有 Blue Book 加持），但文档极其简略。

**建议扩充内容**:
- 中文字体配置的完整示例（`set text(font: ("Source Han Serif SC", ...))`)
- 中英文混排的段落示例
- 中文标点处理和行首行尾规则
- 中文简历/论文的排版示例
- `lang: "zh"` 和 `region: "cn"` 的设置示例

---

## 四、缺失的参考文档建议

以下 Typst 重要功能/概念**没有被任何参考文档充分覆盖**：

### 高优先级缺失

| 缺失主题 | 说明 | 建议位置 |
|----------|------|----------|
| **函数定义与闭包** | `let f(x) = ...` 和 `(x) => ...` 是 Typst 编程的基础，完全没有示例 | `02-language/scripting-and-context.md` 扩充 |
| **条件分支与循环** | `if`/`else`、`for`、`while` 没有代码示例 | `02-language/scripting-and-context.md` 扩充 |
| **模块系统** | `import`/`include` 的详细用法、相对路径、选择性导入 | `02-language/` 新增或扩充到 markup 文档 |
| **错误处理** | `panic`、`assert`、类型检查模式 | `02-language/scripting-and-context.md` 扩充 |
| **常用第三方包** | 如 `cetz`（绘图）、`tablex`（增强表格）等生态包 | `05-recipes/` 新增 |

### 中优先级缺失

| 缺失主题 | 说明 | 建议位置 |
|----------|------|----------|
| **字体管理** | 字体发现、回退链、嵌入行为的详细说明 | `01-workflows/` 或 `05-recipes/` 新增 |
| **自定义编号** | 页码、标题编号、图表编号的自定义模式 | `05-recipes/` 扩充 |
| **PDF 元数据** | 作者、标题、关键词、创建日期的设置 | `03-library/export-and-platform.md` 扩充 |
| **多文件项目** | 大型项目的文件组织和编译策略 | `01-workflows/project-templates-and-packages.md` 扩充 |
| **Typst vs LaTeX 迁移** | LaTeX 用户的快速对照 | `05-recipes/` 新增 |

---

## 五、具体的内容扩充建议

### 5.1 为所有文档添加代码示例（最高优先级）

每个参考文档至少应包含：
- **最小完整示例**（Minimal Complete Example）：一段可编译运行的 Typst 代码
- **常见模式示例**：2-3 个该主题下最常用的代码模式
- **错误示例 + 正确写法**：展示常见错误及其修正

示例格式建议：

```
## 示例

### 基本用法
\`\`\`typst
// 描述该示例的目的
#set text(font: "New Computer Modern")
#set page(margin: 2cm)

= 一级标题
== 二级标题

这是正文内容。
\`\`\`

### 常见错误
\`\`\`typst
// ❌ 错误：忘记了 # 前缀
set text(size: 12pt)

// ✅ 正确
#set text(size: 12pt)
\`\`\`
```

### 5.2 为 `02-language/` 补充语言核心示例

这是最紧迫的改进。四个语言核心文件应各扩充到 80-150 行，包含：
- 语法速查表（Quick Reference）
- 3-5 个可运行示例
- 常见错误对照表

### 5.3 为 `05-recipes/` 补充实用代码配方

配方文档应该是"拿来就能用"的，建议：
- `book-paper-slide-cv-patterns.md`: 每种模式提供一个 20-40 行的最小模板
- `chinese-typesetting.md`: 提供完整的中文文档配置模板
- `tables-figures-bibliography-outline.md`: 提供表格、图表、参考文献的组合示例

### 5.4 为 `03-library/` 补充 API 速查

至少对每个类别的 Top 5 高频 API 提供签名和使用示例。特别是：
- `foundations.md`: `array`, `dictionary`, `str`, `calc` 模块
- `layout.md`: `page`, `grid`, `stack`, `columns`
- `model.md`: `heading`, `figure`, `table`, `bibliography`
- `text.md`: `text`, `raw`, `highlight`

---

## 六、评分汇总

| 评分 | 文件数 | 占比 |
|------|--------|------|
| 5 分 | 0 | 0% |
| 4 分 | 8 | 24% |
| 3 分 | 12 | 36% |
| 2 分 | 13 | 40% |
| 1 分 | 0 | 0% |

**平均分: 2.85 / 5**

---

## 七、结论

参考文档体系的**架构和组织优秀**（编号目录、路由索引、版本跟踪），但**内容深度严重不足**。核心问题是：

> **没有任何一个文件包含可运行的 Typst 代码示例。**

这使得整个参考系统更像一个"话题目录"而非"操作手册"。对于指导 Agent 完成实际 Typst 编写任务来说，当前文档的实用性有限——Agent 仍然需要依赖查询脚本或自身的训练知识来编写代码。

### 改进优先级排序

1. **P0** — 为 `02-language/` 四个文件补充代码示例（语言核心，影响所有任务）
2. **P0** — 为 `05-recipes/book-paper-slide-cv-patterns.md` 补充模板代码（直接影响文档生成任务）
3. **P1** — 为 `03-library/` 关键文件补充 API 示例（`foundations`、`layout`、`model`）
4. **P1** — 扩充 `chinese-typesetting.md`（项目特色功能）
5. **P2** — 为其余文件逐步补充示例和深入说明
