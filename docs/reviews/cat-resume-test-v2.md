# 可爱小猫简历 v2 - Typst Skill 优化后测试报告

- **测试日期**: 2026-04-12
- **测试人**: isolated-test-agent (隔离环境, worktree)
- **测试目标**: 使用 v0.4.0 优化后的 Typst Skill 创建可爱风格猫咪简历, 对比 v1 测试结果
- **Typst CLI 版本**: 0.13.1 (本机安装)
- **Skill 声明的目标版本**: 0.14.2

---

## 1. SKILL.md 路由体验评价

### 路由过程记录

任务: "创建可爱小猫简历"

v0.4.0 新增的 **Quick intent check** 表格直接命中:
> Create a new Typst document → `reference/05-recipes/book-paper-slide-cv-patterns.md`, then `reference/01-workflows/project-templates-and-packages.md`

**Creating from scratch** 路径进一步明确了步骤:
> 1. 确定文档类型 → 2. 查阅 patterns → 3. 考虑 typst init → 4. 从最小模板迭代

| 改进项 | v1 体验 | v2 体验 |
|--------|---------|---------|
| "创建新文档"路由 | ❌ 无直接入口, 需自行推断 | ✅ Quick intent check 直接命中 |
| 文档类型判断 | ❌ CV 归属不明确 | ✅ Creating from scratch 明确 CV 属于 patterns |
| 组合路由指引 | ❌ 路由互斥, 缺少组合建议 | ✅ Quick intent → 然后 subsystem routes |
| 中文排版路由 | ❌ 混在一串中 | ✅ 独立条目 |

### 评分: ⭐⭐⭐⭐⭐ (5/5) — v1 为 4/5, 提升 +1

---

## 2. 参考文档有用程度评价

### 逐文档评价

| 文档 | v1 评分 | v2 评分 | 改进 |
|------|---------|---------|------|
| `05-recipes/book-paper-slide-cv-patterns.md` | 3/5 | **5/5** | 新增 3 个最小可运行模板(论文/CV/幻灯片), CV 模板的 `cv-entry` 函数可直接参考 |
| `05-recipes/chinese-typesetting.md` | N/A(v1未评) | **5/5** | 字体回退链示例直接可用, **中文引号陷阱 ⚠️ 警告**非常关键 |
| `02-language/scripting-and-context.md` | 3/5 | **4/5** | let/闭包/for 循环代码示例帮助编写辅助函数 |
| `03-library/visualize.md` | 3/5 | **5/5** | rect/circle/gradient 示例 + **卡片组合模式**直接指导了布局 |
| `03-library/layout.md` | 3/5 | **5/5** | grid(columns: (1fr, 2fr)) 示例和 stack 示例直接指导了双栏布局 |
| `03-library/text.md` | 3/5 | **4/5** | text 参数速查表有用, highlight/underline 示例为装饰提供了参考 |

### v1 vs v2 关键差异

- **v1**: "大量的具体语法需要依赖 Agent 自身的 Typst 知识, 参考文档无法提供直接可用的代码片段"
- **v2**: 代码中可见大量 `// 参考: xxx.md — yyy` 注释, 说明代码直接受参考文档指导:
  - 字体回退链 → `chinese-typesetting.md`
  - 卡片组合模式 → `visualize.md`
  - grid 双栏布局 → `layout.md`
  - cv-entry 函数模式 → `book-paper-slide-cv-patterns.md`
  - skill-rating 用 for+range → `scripting-and-context.md`

### 评分: ⭐⭐⭐⭐⭐ (4.7/5) — v1 为 3/5, 提升 +1.7

---

## 3. 脚本工具查询体验评价

脚本工具本次未做修改, 体验与 v1 一致。参考文档的代码示例减少了对脚本查询的依赖频次。

### 评分: ⭐⭐⭐⭐ (4/5) — 与 v1 持平

---

## 4. 编写过程中遇到的困难

### 4.1 中文引号问题 ✅ 已由文档覆盖

v1 中的头号陷阱。v2 的 `chinese-typesetting.md` 明确标注:
> ⚠️ 中文引号陷阱: Typst 字符串字面量中 `""` `''` 会被解析为字符串分隔符...必须使用 `「」`

v2 代码中正确使用了 `「歪头杀」`「闪电爪」` 等中文引号, **未遇到编译错误**。

### 4.2 字体 warning (预期行为)

编译时出现 `Noto Sans CJK SC` 和 `PingFang SC` 未找到的 warning, 但这是 Windows 环境的预期行为 — 回退链中的 `Microsoft YaHei` 正确接管。`chinese-typesetting.md` 中的跨平台回退链建议是正确的。

### 4.3 emoji 语法

`emoji.cat.face`、`emoji.prints.paw`、`emoji.sparkles` 等语法来自 Agent 内置知识, 参考文档中对 emoji 访问的覆盖仍不够详细。

### 4.4 gradient 语法

`gradient.linear(color1, color2, angle: 135deg)` 在 `visualize.md` 中有了示例, 直接参考即可, **v1 中这是空白**。

---

## 5. 与 v1 测试的对比

| 维度 | v1 问题 | v2 状态 |
|------|---------|---------|
| "创建新文档"路由缺失 | ❌ 需自行推断 | ✅ Quick intent check 直接命中 |
| 参考文档无代码示例 | ❌ 33 个文件 0 个代码片段 | ✅ 核心文件全部包含可运行代码 |
| CV 模板代码 | ❌ 只有概念描述 | ✅ 最小 CV 模板可直接参考 |
| 中文引号陷阱 | ❌ 编译错误, 无文档覆盖 | ✅ 明确 ⚠️ 警告 |
| gradient 文档 | ❌ 几乎未覆盖 | ✅ visualize.md 有示例 |
| grid 列定义语法 | ❌ 未说明 | ✅ layout.md 有 `(1fr, 2fr)` 示例 |
| 字体跨平台建议 | ❌ 无具体方案 | ✅ 回退链示例 |
| description 过长 | ❌ ~55 词 | ✅ ~30 词 "Use when..." |
| 错误诊断路由 | ❌ 无 | ✅ Error triage 表 |

### 仍存在的问题

1. **emoji 覆盖不足** — `emoji.cat.face` 等具体访问路径未在参考文档中列出
2. **3/5 评分文件未更新** — `data-loading.md`, `introspection.md`, `symbols.md` 仍缺代码示例
3. **第三方包生态** — cetz, tablex 等常用包仍无参考

---

## 6. 最终产物

- **Typst 源文件**: `build/cute-cat-resume-v2.typ` (387 行)
- **PDF 输出**: `build/cute-cat-resume-v2.pdf`
- **编译状态**: ✅ 成功 (2 个字体 warning, 预期行为)

### v2 vs v1 代码对比

| 维度 | v1 | v2 |
|------|----|----|
| 代码行数 | 307 行 | 387 行 |
| 参考文档引用注释 | 0 处 | 12+ 处 |
| 中文引号使用 | `「」` (修复后) | `「」` (首次正确) |
| 字体回退链 | 3 个字体 | 5 个字体(跨平台) |
| 辅助函数 | 4 个 | 6 个(含 tag-badge, info-row) |
| CV entry 模式 | 自创 timeline-item | 参考 cv-entry 模式 |

---

## 7. 总结评分

| 维度 | v1 评分 | v2 评分 | 变化 |
|------|---------|---------|------|
| SKILL.md 路由 | 4/5 | **5/5** | +1 |
| 参考文档 | 3/5 | **4.7/5** | +1.7 |
| 脚本工具 | 4/5 | **4/5** | 0 |
| 编写体验 | 4/5 | **4.8/5** | +0.8 |
| **综合** | **3.75/5** | **4.6/5** | **+0.85** |

### 结论

v0.4.0 优化显著提升了 Skill 的实际指导能力:
- **路由**: 从"需要猜测"到"直接命中", 新增的 Quick intent check 和 Creating from scratch 路径解决了 v1 最大的体验痛点
- **参考文档**: 从"话题目录"升级为"可操作指南", 代码示例直接指导了 6+ 个核心编码决策
- **中文排版**: 引号陷阱警告避免了 v1 中最严重的编译错误
- **综合评分 4.6/5**, 达到了 ≥ 4.5/5 的目标
