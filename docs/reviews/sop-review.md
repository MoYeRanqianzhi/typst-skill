# SKILL.md SOP 审查报告

- 审查日期: 2026-04-12
- 审查文件: `skills/typst/SKILL.md`
- 审查者: SOP Review Agent
- Typst 版本基线: 0.14.2

---

## 一、总体评价

SKILL.md 作为一个 Level 2 SOP，整体结构清晰、权威排序合理、路由表覆盖了主要子系统。它成功地在约 62 行（~1.5k tokens）内建立了一个可操作的工作框架。但在**新手可操作性**、**错误处理指导**、**场景覆盖完整性**方面存在明显的可改进空间。

---

## 二、优点列表

1. **权威层级清晰** — 明确规定"官方源 > 索引 > 蓝皮书"，冲突时以官方为准并标注差异，避免了知识混乱。
2. **路由表设计合理** — 按任务类型路由到最小匹配文件，符合渐进式披露原则，有效控制 token 消耗。
3. **双索引策略互补** — `query_reference.py`（广覆盖）和 `query_api_index.py`（快速官方过滤）分工明确，各有使用场景。
4. **标准工作流六步** — 从识别输出类型到验证假设，逻辑链完整。
5. **输出要求具体** — "直接可运行"、"标注版本敏感行为"、"说明指导来源"、"先解释根因再修复"等要求可执行。
6. **Token 控制出色** — 整个 SKILL.md 保持在 ~1.5k tokens，Level 2 加载成本合理。
7. **reference 知识体系完善** — 从 `01-workflows` 到 `07-versioning`，七大分区覆盖了 Typst 生态的主要维度。

---

## 三、问题列表（按严重程度排序）

### P0 — 严重缺陷

#### 3.1 缺少"从零创建文档"场景的入口路由

**问题**: 路由表完全基于"已有问题/已有代码"的假设设计。当用户请求"帮我写一个 Typst 论文/简历/幻灯片"时，路由表中没有直接匹配的入口。Agent 需要自行判断应该先去 `project-templates-and-packages.md` 还是 `book-paper-slide-cv-patterns.md`，还是直接生成代码。

**影响**: 创建新文档是最高频的使用场景之一，缺失此路由会导致 Agent 行为不一致。

#### 3.2 缺少错误处理/编译失败场景的指导

**问题**: 标准工作流假设一切顺利。当 `typst compile` 失败、脚本执行出错、索引文件缺失或损坏时，SKILL.md 没有提供任何 fallback 路径或错误恢复指导。

**影响**: Agent 在遇到编译错误时缺乏结构化的诊断策略，可能陷入反复试错。

### P1 — 重要问题

#### 3.3 路由表缺少对常见错误类型的分类路由

**问题**: 虽然 `compile-debug-publish.md` 中有 Debug Workflow，但 SKILL.md 路由表只有一个笼统的"Compile, export, debug"入口。对于常见的编译错误类别（语法错误、类型错误、找不到包/字体、context 循环依赖、show rule 冲突等），没有分类路由。

**影响**: 调试是第二高频场景，缺少分类路由降低了诊断效率。

#### 3.4 缺少对中文排版场景的专项路由说明

**问题**: 中文排版在路由表中被归入 "Chinese typesetting, bibliography, state/query, accessibility, template recipes" 这一串中，没有突出其特殊性。中文用户的典型诉求（字体配置、中西文混排、标点压缩、竖排等）需要额外的路由提示。

**影响**: 中文排版用户是该 Skill 的重要目标群体（蓝皮书就是中文资源），但 SOP 对此场景缺乏重视。

#### 3.5 工作流第3步 "Consult the smallest matching bundled reference" 缺乏具体性

**问题**: "最小匹配"的概念虽然正确，但未给出判断方法。当一个问题可能涉及多个 reference 文件时（例如 "如何在模板中设置中文字体"——涉及 `project-templates-and-packages.md`、`chinese-typesetting.md`、`text.md`），Agent 缺乏选择依据。

**影响**: 可能导致 Agent 打开过多或过少的 reference 文件。

#### 3.6 缺少多文件项目管理场景的指导

**问题**: 路由表提到 "Project structure, templates, packages"，但 reference 中缺少对以下多文件场景的系统指导：
- 多章节书稿如何组织 `import`/`include`
- `--root` 对跨目录引用的影响
- 多入口文件（main + appendix）的编译策略

**影响**: 复杂项目场景下 Agent 缺乏具体操作指引。

### P2 — 改进建议

#### 3.7 `Refresh the bundled knowledge` 部分包含硬编码路径

**问题**: 第5步使用了 `python C:/Users/MoYeR/.codex/skills/.system/skill-creator/scripts/quick_validate.py`，这是一个用户特定的绝对路径，对其他开发者或环境不可移植。

**影响**: 可维护性降低；新贡献者无法直接使用。

#### 3.8 description 字段过长

**问题**: YAML frontmatter 的 `description` 约 55 词 / ~350 characters。作为 Level 1 披露层，理想长度应在 20-30 词以内。当前 description 试图列举所有功能而非给出精准的触发条件。

**影响**: 在 skill 列表页面中占用过多 token，降低了 Level 1 的扫描效率。

#### 3.9 路由表没有为 "解释/教学" 类请求提供路由

**问题**: 当用户请求 "解释一下 Typst 的 show rule 是什么" 或 "Typst 和 LaTeX 有什么区别" 这类纯教学/解释请求时，路由表没有明确的入口。

**影响**: 解释类请求虽然不需要生成代码，但占 Typst 使用场景的相当比例。

#### 3.10 标准工作流缺少 "回答前验证" 环节

**问题**: 第5步是 "Produce runnable Typst code or a concrete remediation plan"，第6步是 "State assumptions"。但缺少一个明确的验证步骤：在提交最终答案前，检查生成的代码是否真的能编译通过。

**影响**: 可能导致 Agent 输出语法正确但语义错误的代码。

---

## 四、缺失场景分析

### 4.1 从零创建新文档

| 缺失项 | 当前状态 | 建议 |
|---------|---------|------|
| 创建路由入口 | 无 | 在路由表中增加 "Create new document from scratch" 路由 |
| 最小可行文档模板 | reference 中有模式但无 quickstart | 在 SKILL.md 或 reference 中增加 quickstart snippet |
| `typst init` 提示 | 仅在 reference 中 | 在路由表中提及 `typst init` 作为快速启动路径 |

### 4.2 模板定制和修改

| 缺失项 | 当前状态 | 建议 |
|---------|---------|------|
| 修改已有模板的路由 | 被归入 "Project structure, templates, packages" | 增加明确的模板修改路由 |
| 模板调试路由 | 无 | 当模板行为不符合预期时的诊断路径 |

### 4.3 多文件项目管理

| 缺失项 | 当前状态 | 建议 |
|---------|---------|------|
| 多文件组织模式 | reference 中有 recommended layout | SKILL.md 路由应更明确地指向多文件场景 |
| `--root` 使用指导 | 分散在多个 reference 中 | 汇总到 workflows reference 中 |

### 4.4 常见编译错误排查

| 缺失项 | 当前状态 | 建议 |
|---------|---------|------|
| 错误分类路由 | 仅有 "Compile, export, debug" | 按错误类别细分路由 |
| 常见错误速查表 | 无 | 在 reference 中增加 common-errors.md |
| fallback 策略 | 无 | 在 SKILL.md 工作流中增加 "如果查不到匹配项" 的兜底指引 |

### 4.5 中文排版特殊处理

| 缺失项 | 当前状态 | 建议 |
|---------|---------|------|
| 字体配置 quickstart | reference 中有 practice notes | 增加具体的中文字体配置示例或路由 |
| 中西文混排间距 | reference 中提及 | 突出为高频问题 |
| CJK 标点优化 | reference 中提及 | 增加路由可见度 |

---

## 五、具体改进建议

### 建议 1：重写 description（Level 1 精简）

**当前文本**:
```
Comprehensive Typst authoring, debugging, refactoring, template design, package and module work, and source-grounded API lookup for Typst 0.14.2. Use when Codex needs to write or fix Typst documents, explain Typst syntax or layout behavior, build templates, diagnose compilation or state or query issues, or consult bundled official and Chinese Typst references.
```

**建议文本**:
```
Source-grounded Typst 0.14.2 specialist. Triggers on: write, fix, debug, explain, or template Typst documents; API or symbol lookup; Chinese typesetting guidance.
```

理由: 从 ~55 词压缩到 ~25 词，保留所有关键触发词，提高 Level 1 扫描效率。

---

### 建议 2：扩展路由表，增加高频场景

在现有路由表 **之前** 增加一个"任务类型速判"小节：

```markdown
## Route the task first

### Quick intent check
- Create a new Typst document -> `reference/05-recipes/book-paper-slide-cv-patterns.md`, then `reference/01-workflows/project-templates-and-packages.md`
- Explain Typst concepts or compare with LaTeX -> the relevant file under `reference/02-language/`
- Fix a compilation error -> see **Error triage** below
- Modify an existing template -> `reference/01-workflows/project-templates-and-packages.md`

### Error triage
- Syntax or parse error -> `reference/02-language/markup-and-document-structure.md`
- Type mismatch or function signature error -> run `query_reference.py` for the exact API, then consult the matching `reference/03-library/` file
- Font or package not found -> `reference/01-workflows/compile-debug-publish.md` (World and Environment Inputs)
- Context or state bug -> `reference/05-recipes/state-counter-query-locator.md`
- Layout or page overflow -> `reference/02-language/styling-layout-and-show-rules.md`
- Version-related behavioral change -> `reference/07-versioning/`

### Subsystem routes
(keep existing routes here unchanged)
```

---

### 建议 3：在标准工作流中增加错误处理和验证步骤

```markdown
## Follow the standard workflow

1. Identify the requested output: snippet, template, edit, debug help, or explanation.
2. Confirm the subsystem: workflow, language, library category, recipe, or versioning.
3. Consult the smallest matching bundled reference. When multiple files match, prefer the one most specific to the user's exact question.
4. Run `query_reference.py` before answering exact API questions.
5. Produce runnable Typst code or a concrete remediation plan.
6. **Verify**: mentally walk through the generated code for syntax, type, and semantic correctness. If unsure, suggest the user run `typst compile` to confirm.
7. State assumptions, compatibility notes, and validation commands when relevant.

### If stuck or no match found
- If the route is unclear, start with `query_reference.py --query <keyword>` to discover the right subsystem.
- If an index file is missing or corrupt, note the issue and work from raw reference files under `reference/`.
- If a compilation error cannot be diagnosed from bundled references, suggest the user provide the full error message and a minimal reproduction.
```

---

### 建议 4：修复硬编码路径

将:
```markdown
5. Validate with `python C:/Users/MoYeR/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/typst`.
```

改为:
```markdown
5. Validate with the skill-creator's `quick_validate.py` script (e.g., `python <skill-creator-path>/scripts/quick_validate.py skills/typst`).
```

---

### 建议 5：增加中文排版路由可见度

在路由表中将中文排版从混合列表中独立出来:

```markdown
- Chinese typesetting (fonts, CJK spacing, punctuation) -> `reference/05-recipes/chinese-typesetting.md`
- Bibliography, state/query, accessibility, template recipes -> the relevant file under `reference/05-recipes/`
```

---

### 建议 6：增加"创建新文档"的快速路径提示

在路由表或工作流中增加:

```markdown
### Creating a document from scratch
1. Determine the document type: paper, book, slides, CV, letter, or custom.
2. Check `reference/05-recipes/book-paper-slide-cv-patterns.md` for the matching pattern.
3. Consider using `typst init <template>` if a published template fits (see `reference/01-workflows/project-templates-and-packages.md`).
4. If building from scratch, start with a minimal template function and iterate.
```

---

## 六、渐进式披露评估

| 层级 | 评估 | 评分 |
|------|------|------|
| **Level 1** (description) | 功能覆盖全面但过于冗长，需压缩至 ~25 词 | ⚠️ 需改进 |
| **Level 2** (SKILL.md) | ~62 行 / ~1.5k tokens，在合理范围内；内容结构清晰但场景覆盖有盲区 | ✅ 良好，有改进空间 |
| **Level 3** (scripts + reference) | 双索引 + 7 大分区 reference，按需加载设计良好 | ✅ 优秀 |

---

## 七、新手友好度评估

**测试问题**: 一个不熟悉 Typst 的 Agent 能否仅凭 SKILL.md 完成 "帮我写一个中文学术论文模板" 的任务？

| 步骤 | 能否完成 | 障碍 |
|------|---------|------|
| 1. 判断任务类型 | ⚠️ 不确定 | "写新模板"在路由表中没有直接匹配 |
| 2. 找到正确的 reference | ⚠️ 需要猜测 | 需要同时打开 templates + chinese + patterns 三个文件 |
| 3. 生成代码 | ✅ 可行 | reference 中有足够信息 |
| 4. 处理中文字体 | ⚠️ 信息分散 | 中文字体配置分散在多个文件中 |
| 5. 验证输出 | ✅ 可行 | 工作流第6步有提示 |

**结论**: 有经验的 Agent 可以完成，但新手 Agent 需要在路由阶段做出多个不确定的判断。**增加建议 2 和建议 6 可显著改善新手可操作性。**

---

## 八、总结

SKILL.md 是一个扎实的 SOP 框架，在权威管理、索引策略、渐进式披露方面表现出色。主要改进方向是：

1. **扩展路由表**（P0）— 增加"创建新文档"和"错误分类"路由
2. **增加错误处理指导**（P0）— 工作流增加 fallback 和验证步骤  
3. **提升中文排版可见度**（P1）— 独立路由条目
4. **精简 Level 1 description**（P2）— 压缩至 ~25 词
5. **修复硬编码路径**（P2）— 改为相对或占位符路径

实施以上改进后，SKILL.md 将从"可用"提升为"新手友好且场景完备"。
