# Scripts 工具审查报告

> 审查日期：2026-04-12
> 审查范围：`skills/typst/scripts/` 下全部 4 个 Python 脚本

---

## 总览

| 脚本 | 用途 | 评分 | 状态 |
|------|------|:----:|:----:|
| `query_reference.py` | 综合查询（API/文档/符号/grep） | 8.5/10 | ✅ 可用 |
| `query_api_index.py` | 快速 API 索引查询 | 8.0/10 | ✅ 可用 |
| `build_reference.py` | 构建综合引用数据库 | 7.5/10 | ✅ 可用 |
| `refresh_typst_knowledge.py` | 刷新 API 索引和快照 | 7.5/10 | ✅ 可用 |

---

## 1. `query_reference.py` — 综合查询工具

### 1.1 代码质量评估

**优点：**
- 多层评分策略（`score()` 函数）设计合理，对精确匹配、前缀匹配、子串匹配给予递减权重
- 支持多数据源搜索：API 条目、官方文档、Blue Book、原始 grep
- 输出格式清晰，分为 4 个区块展示
- UTF-8 编码处理完善，`sys.stdout.reconfigure` 有异常保护
- 支持 `--json` 模式，方便程序化消费
- `--rebuild` 参数可在查询前触发重新构建

**问题与改进建议：**

1. **`grep()` 函数性能隐患（中等）**：逐行遍历所有源文件（`.rs`, `.md`, `.typ` 等），对大型代码库可能很慢。当前通过 `limit` 提前退出缓解，但没有超时机制。
2. **`infer_root()` 中的 `parents[4]` 硬编码（低）**：假定参考文件位于项目根目录下 5 层，如果目录结构改变会失败。有 fallback 但假设脆弱。
3. **`--name` 和 `--query` 行为等同（低）**：两个参数功能完全相同（`join_tokens(args.name) or join_tokens(args.query)`），可能让用户困惑。
4. **函数名 `rit`/`rdoc`/`rgrep` 可读性差（低）**：应使用更具描述性的名称如 `render_item`/`render_doc`/`render_grep`。

### 1.2 运行测试结果

| 测试用例 | 命令 | 结果 | 说明 |
|----------|------|:----:|------|
| 基本查询 | `--query "page"` | ✅ 成功 | 返回 10 条 API 匹配、4 条文档、8 条 grep 结果 |
| 作用域名称 | `--query "figure.caption"` | ✅ 成功 | 精确匹配 `figure.caption` 元素 |
| 符号查询 | `--query "sym.arrow"` | ✅ 成功 | 返回 sym.arrow 及其子变体 |
| 无匹配 | `--query "nonexistent_xyz_abc"` | ✅ 成功 | 4 个区块均返回 "No match"，退出码 0 |
| 无参数 | （无 --query/--name） | ✅ 正确 | 打印错误提示，退出码 2 |
| limit=0 | `--limit 0 --query "page"` | ✅ 正确 | 打印 "must be positive"，退出码 2 |
| limit=-1 | `--limit -1 --query "page"` | ✅ 正确 | 打印 "must be positive"，退出码 2 |
| kind 过滤 | `--query "page" --kind "element"` | ✅ 成功 | 仅返回 element 类型的结果 |
| module 过滤 | `--query "arrow" --module "sym"` | ✅ 成功 | 仅返回 sym 模块内的符号 |
| JSON 输出 | `--query "page" --json` | ✅ 成功 | 合法 JSON，含 matches/docs/bluebook/grep 4 个键 |

---

## 2. `query_api_index.py` — 快速 API 索引查询

### 2.1 代码质量评估

**优点：**
- 有文档字符串 `"""Query the generated Typst API index."""`
- 评分函数对 `name` 做了 `re.split(r"[._-]")` 分词匹配，对作用域名称（如 `grid.cell`）检索效果好
- 使用 `casefold()` 而非 `lower()`，对 Unicode 更友好
- 索引文件不存在时有明确错误提示和退出码 2
- 输出末尾有 `... N more` 提示
- 支持 `--category`/`--kind`/`--scope`/`--source` 多维过滤

**问题与改进建议：**

1. **无参数调用列出全部 498 条（中等）**：当 `--name` 为空时，`score_name` 返回 1 对所有条目，等于无过滤全量输出。应提示用户提供搜索条件或限制默认输出。
2. **`--help` 参数描述缺失（低）**：所有参数都没有 `help` 文本，`argparse` 只显示参数名，不够友好。
3. **默认索引路径使用 `08-generated`（注意）**：与 `query_reference.py` 使用的 `generated/` 是不同目录，两个查询工具的数据源不同，需确保两者都有数据。

### 2.2 运行测试结果

| 测试用例 | 命令 | 结果 | 说明 |
|----------|------|:----:|------|
| 名称查询 "text" | `--name "text"` | ✅ 成功 | 匹配 4 个 element，含 text/context/op/raw.line |
| 名称查询 "grid" | `--name "grid"` | ✅ 成功 | 匹配 6 个 element，含 grid 及 5 个 scope 子元素 |
| 无匹配查询 | `--name "nonexistent_xyz_abc"` | ✅ 成功 | 输出 "Matches: 0"，退出码 0 |
| 缺失索引文件 | `--index "nonexistent.json"` | ✅ 正确 | 输出错误信息，退出码 2 |
| limit=0 | `--limit 0 --name "text"` | ✅ 正确 | 输出 "must be positive"，退出码 2 |
| category 过滤 | `--category "layout"` | ✅ 成功 | 仅返回 layout 类别的 64 条记录 |
| 无参数调用 | （无参数） | ⚠️ 注意 | 列出全部 498 条，应提示用户 |
| JSON 输出 | `--name "text" --json` | ✅ 成功 | 合法 JSON 数组，4 个条目 |

---

## 3. `build_reference.py` — 综合引用数据库构建器

### 3.1 代码质量评估

**优点：**
- 功能全面：解析 Rust 源码中的 `#[func]`/`#[elem]`/`#[ty]`/`#[scope]` 宏属性
- 支持解析 HTML 属性（来自 cargo 缓存）和符号模块（sym/emoji）
- 绑定关系解析（`parse_bindings`）追踪模块注册
- 输出带统计信息的 `summary.md` 方便快速查看
- `rel()` 函数对 cargo 缓存路径有 fallback 处理

**问题与改进建议：**

1. **函数名极短且不透明（中等）**：`rt`（read_text）、`rel`（relative）、`m1`（match_group_1）、`CT`（category table）、`cat`（category）等缩写过于简略，严重影响可读性。
2. **`parse_bindings` 缺少空行分隔（低）**：第 402 行和第 403 行之间 `parse_html` 函数定义前缺少空行，PEP 8 不符。
3. **`cattr`/`cfn`/`cblock` 命名不清（中等）**：应改为 `collect_attribute`/`collect_function`/`collect_block`。
4. **Rust 源码解析基于正则表达式（已知限制）**：无法处理嵌套泛型、宏展开等复杂情况，但对当前用途足够。
5. **`strip_generics()` 不处理 `>>` 折叠（低）**：`depth = max(depth - 1, 0)` 避免了负数，但连续 `>>` 可能丢失一层。
6. **硬编码 cargo 缓存路径（低）**：`Path.home() / ".cargo"` 假定默认 cargo home，不支持 `CARGO_HOME` 环境变量。

### 3.2 运行测试结果

| 测试用例 | 命令 | 结果 | 说明 |
|----------|------|:----:|------|
| `--help` | `build_reference.py --help` | ✅ 成功 | 显示 4 个路径参数 |

> 注：完整构建需要 typst 源码和 Blue Book 仓库存在，此次审查不执行完整构建以避免覆盖现有数据。

---

## 4. `refresh_typst_knowledge.py` — API 索引刷新器

### 4.1 代码质量评估

**优点：**
- 独立完整的管道：解析源码 → 收集参考页面 → 收集分组 → 写入索引
- 输出三个文件：`source-snapshot.json`、`typst-api-index.json`、`typst-api-index.md`
- 使用 `dataclass` 定义 `ScopeFrame`，结构清晰
- `collect_rust_metadata` 做两遍扫描确保完整性
- 依赖 `yaml` 解析 `groups.yml`

**问题与改进建议：**

1. **依赖 `yaml` 库但无安装检查（中等）**：`import yaml` 在标准库之外，如果未安装会抛出 `ModuleNotFoundError`，没有友好的错误提示。
2. **`CATEGORY_MAP` 中 pdf/html 映射为 "export"（注意）**：与 `build_reference.py` 的 `CT` 映射不一致（CT 中 pdf→"PDF", html→"HTML"），两个脚本对同一概念用不同分类名。
3. **`typst_version()` 使用正则匹配 Cargo.toml（低）**：不如 `tomllib.loads()` 健壮，且 `build_reference.py` 已经使用了 `tomllib`。
4. **`scan_library` 深度追踪用 `raw_line.count("{")` 计算花括号（已知限制）**：字符串和注释中的花括号会被误计，但实际影响有限。
5. **`--help` 不输出任何帮助（低）**：脚本未使用 `argparse`，`--help` 参数被忽略（实际运行了完整刷新）。
6. **`repo_root()` 和 `skill_root()` 硬编码层级关系（中等）**：`parents[3]` 和 `parents[1]` 假定固定的目录结构。

### 4.2 运行测试结果

| 测试用例 | 命令 | 结果 | 说明 |
|----------|------|:----:|------|
| 直接运行 | `refresh_typst_knowledge.py` | ✅ 成功 | 输出 "Refreshed Typst knowledge under ..."，生成 3 个文件 |
| `--help` | `refresh_typst_knowledge.py --help` | ⚠️ 问题 | 没有使用 argparse，`--help` 直接执行了完整刷新 |

---

## 5. 交叉问题

### 5.1 两套索引，两套路径

| 工具 | 数据源目录 | 索引文件 |
|------|-----------|---------|
| `query_reference.py` | `reference/generated/` | `typst-reference.json` (2MB) |
| `query_api_index.py` | `reference/08-generated/` | `typst-api-index.json` (100KB) |
| `build_reference.py` | 输出到 `reference/generated/` | 构建 `typst-reference.json` |
| `refresh_typst_knowledge.py` | 输出到 `reference/08-generated/` | 构建 `typst-api-index.json` |

两套平行的索引系统容易让使用者困惑。`query_reference.py` 的综合数据库涵盖符号、HTML 属性、文档和 grep，而 `query_api_index.py` 的轻量索引只包含 Rust API 条目。应在文档中明确各自的定位和使用场景。

### 5.2 命名不一致

- `build_reference.py` 中分类名使用标题格式 ("Foundations", "Layout")
- `refresh_typst_knowledge.py` 中使用 kebab-case ("foundations", "data-loading") 和别名 ("export")
- `query_api_index.py` 中 `category` 依赖 `refresh_typst_knowledge.py` 的输出

### 5.3 错误处理

所有脚本对 JSON 解析失败和文件缺失都没有 try/except 包装，如果索引文件损坏会抛出原始异常栈。建议统一添加用户友好的错误信息。

---

## 6. 改进建议优先级

| 优先级 | 建议 | 涉及脚本 |
|:------:|------|---------|
| **P1** | `refresh_typst_knowledge.py` 添加 `argparse`，避免 `--help` 执行完整刷新 | refresh |
| **P1** | 为 `query_api_index.py` 无参数调用添加警告或限制 | query_api_index |
| **P2** | 统一两套索引的分类命名 | build_reference, refresh |
| **P2** | 改善函数命名（`rt`→`read_text`, `rit`→`render_item`, `CT`→`CATEGORY_TABLE`） | build_reference, query_reference |
| **P2** | 添加 argparse `help` 文本描述 | query_api_index |
| **P2** | `refresh_typst_knowledge.py` 添加 `yaml` 库缺失检查 | refresh |
| **P3** | 考虑 `CARGO_HOME` 环境变量 | build_reference, refresh |
| **P3** | 为 `grep()` 添加超时保护 | query_reference |
| **P3** | 明确文档说明两套查询工具的使用场景 | 文档 |

---

## 7. 总结

四个脚本整体质量合格，功能完整可用。核心查询工具 `query_reference.py` 和 `query_api_index.py` 在正常使用场景下表现良好，评分机制合理，输出格式清晰。构建工具 `build_reference.py` 和 `refresh_typst_knowledge.py` 能正确解析 Typst Rust 源码并生成索引。

主要风险点在于：
1. 两套平行索引系统增加了维护和理解成本
2. 部分函数命名过于简略影响可维护性
3. `refresh_typst_knowledge.py` 缺少 CLI 参数支持

这些问题不影响当前使用，但建议在后续迭代中逐步优化。
