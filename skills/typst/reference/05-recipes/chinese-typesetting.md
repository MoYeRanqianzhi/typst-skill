# Chinese Typesetting

## Use

- Provide Chinese typography, font setup, mixed-language layout, and local best-practice guidance.

## Authoritative Sources

- `The Raindrop-Blue Book/src/tutorial/writing-chinese.typ`
- `The Raindrop-Blue Book/src/tutorial/scripting-style.typ`
- `typst/crates/typst-cli/src/args.rs`
- `typst/docs/guides/page-setup.md`

---

## ⚠️ Critical: Chinese Quotation Mark Trap

Typst uses `"` and `'` as string delimiters. **Chinese full-width quotation marks `""` `''` look identical or near-identical in many editors and will cause cryptic compile errors.** This is the #1 pitfall for Chinese users.

**Wrong — causes parse error:**
```typst
// ❌ The full-width quotes below look like string delimiters to Typst
#let title = "这是标题"   // Compile error!
```

**Correct approaches:**
```typst
// ✅ Use standard ASCII quotes for code strings
#let title = "这是标题"

// ✅ In body text, use corner brackets instead
这本书叫「Typst 入门」，其中第一章叫『基础语法』。

// ✅ Or use Unicode escapes when you truly need full-width quotes in output
#"他说：\u{201C}你好\u{201D}"
```

---

## Font Configuration

### Cross-Platform Fallback Chain

```typst
// Serif (recommended for body text)
#set text(
  font: (
    "Source Han Serif SC",    // Adobe — Linux / macOS
    "Noto Serif CJK SC",     // Google — Linux
    "SimSun",                 // Windows built-in
    "STSong",                 // macOS built-in
  ),
  lang: "zh",
  region: "cn",
)

// Sans-serif (recommended for headings / slides)
#set text(
  font: (
    "Source Han Sans SC",
    "Noto Sans CJK SC",
    "Microsoft YaHei",        // Windows
    "PingFang SC",            // macOS / iOS
  ),
  lang: "zh",
  region: "cn",
)
```

### Language and Region Settings

| Parameter    | Value   | Effect                                        |
|-------------|---------|-----------------------------------------------|
| `lang`      | `"zh"`  | Enables CJK line-breaking and spacing rules   |
| `region`    | `"cn"`  | Selects Simplified Chinese glyph variants     |
| `region`    | `"tw"`  | Selects Traditional Chinese glyph variants    |

```typst
// Traditional Chinese setup
#set text(
  font: ("Source Han Serif TC", "Noto Serif CJK TC", "PMingLiU"),
  lang: "zh",
  region: "tw",
)
```

### Lock Fonts for Reproducibility

```bash
# Use --font-path to pin fonts across machines
typst compile --font-path ./fonts main.typ
```

Place `.otf` / `.ttf` files in a project `fonts/` directory and commit them or document the expected font list.

---

## Mixed Chinese-English Paragraphs

```typst
#set text(
  font: ("Source Han Serif SC", "Noto Serif CJK SC", "SimSun"),
  lang: "zh",
  region: "cn",
)

// Typst automatically inserts thin spacing between CJK and Latin characters
// when lang is set to "zh". No manual spaces needed.
这是一段包含 English 单词的中文段落。Typst 会自动处理中英文之间的间距，
无需手动插入空格。数字如 2026 和缩写如 API 也会被正确处理。
```

If automatic spacing is insufficient, you can fine-tune with `#h(0.25em)` but this is rarely needed with `lang: "zh"` set.

---

## Punctuation and Line-Breaking Rules

With `lang: "zh"` enabled, Typst applies CJK-aware line breaking:

- **Line-start prohibition (行首禁则)**: closing punctuation `）」』】》` and period/comma `。，` will not appear at the start of a line.
- **Line-end prohibition (行尾禁则)**: opening punctuation `（「『【《` will not appear at the end of a line.
- **Punctuation compression**: consecutive full-width punctuation may be squeezed to avoid excessive whitespace.

```typst
#set text(lang: "zh", region: "cn")
#set par(first-line-indent: 2em, leading: 1em)

// Standard body paragraph with first-line indent (Chinese convention)
#par[这是第一段正文。中文排版通常要求首行缩进两个字符宽度，
Typst 通过 `first-line-indent` 参数实现这一效果。]

#par[这是第二段正文。段落之间可以通过 `leading` 和 `spacing`
参数控制行距和段距。]
```

---

## Minimal Complete Chinese Document Template

```typst
#set page(paper: "a4", margin: (x: 2.5cm, y: 2cm))
#set text(
  font: ("Source Han Serif SC", "Noto Serif CJK SC", "SimSun"),
  size: 12pt,
  lang: "zh",
  region: "cn",
)
#set par(first-line-indent: 2em, leading: 1em, spacing: 1.2em)
#set heading(numbering: "一、")

#align(center)[
  #text(size: 22pt, weight: "bold")[文档标题]

  #text(size: 14pt, fill: gray)[作者姓名 — 2026 年 4 月]
]

#v(1em)

= 引言

这是一份使用 Typst 排版的中文文档模板。它包含了基本的页面设置、
字体配置、段落格式和标题编号。

= 正文

中文排版需要注意字体回退链的配置，确保在不同操作系统上都能
正确显示。使用「角括号」代替中文引号可以避免编译错误。

== 小节标题

这是一个二级标题下的段落。
```

---

## Practice Notes

- Lock fonts with `--font-path` or a stable project font directory for reproducibility.
- Solve Chinese and mixed-language spacing with fonts, language settings, and paragraph rules instead of manual spaces.
- Put typography decisions such as margins, emphasis, heading style, and punctuation strategy into templates when possible.
- Re-check emoji, icon, and fallback font behavior on the actual target machine.

## Validation

- Confirm the chosen fonts really contain the required Han glyph coverage.
- Verify punctuation, quotation, and line-break behavior in realistic paragraphs.
- Check exact API usage against the official `0.14.2` baseline before repeating older blue-book examples verbatim.

## Also See

- `../../03-library/text.md`
- `../../02-language/styling-layout-and-show-rules.md`
