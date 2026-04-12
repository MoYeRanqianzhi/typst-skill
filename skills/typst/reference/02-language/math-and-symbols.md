# Math and Symbols

## Use

- Handle math mode, text-versus-math boundaries, symbol lookup, and formula structure questions.

## Authoritative Sources

- `typst/docs/reference/language/syntax.md`
- `typst/docs/reference/library/math.md`
- `typst/docs/reference/library/symbols.md`
- `The Raindrop-Blue Book/src/tutorial/writing-math.typ`

## Core Concepts

- Math mode and text mode follow different spacing and parsing rules.
- Prefer built-in math functions and structures over manual glyph composition.
- `sym`, `emoji`, and math syntax solve different classes of symbol problems.
- For non-trivial formulas, check matrix, delimiter, attachment, and variant APIs explicitly.

---

## Inline vs Block Equations

```typst
// Inline math — flows within text
The equation $a^2 + b^2 = c^2$ is Pythagorean.

// Block math — centered on its own line (note the space/newline after $)
$ E = m c^2 $

// Block math with numbering
#set math.equation(numbering: "(1)")
$ integral_0^infinity e^(-x^2) dif x = sqrt(pi) / 2 $
```

## Superscripts and Subscripts

```typst
$ x^2 $           // superscript
$ x_i $           // subscript
$ x_i^2 $         // both
$ a_(i j) $       // multi-char subscript needs grouping
$ e^(i pi) + 1 $  // multi-char superscript needs grouping
```

## Fractions

```typst
$ frac(a, b) $              // standard fraction
$ frac(x^2 + 1, x - 1) $   // complex numerator/denominator
$ a / b $                   // inline-style slash fraction
```

## Roots

```typst
$ sqrt(x) $         // square root
$ root(3, x) $      // cube root  — root(index, radicand)
$ sqrt(a^2 + b^2) $ // composite expression
```

## Matrices and Vectors

```typst
// Matrix
$ mat(
  1, 2, 3;
  4, 5, 6;
) $

// Matrix with custom delimiters
$ mat(delim: "[",
  a, b;
  c, d;
) $

// Column vector
$ vec(x, y, z) $

// Vector with custom delimiter
$ vec(delim: "(", 1, 2, 3) $
```

## Cases (Piecewise Functions)

```typst
$ f(x) = cases(
  x^2    &"if" x >= 0,
  -x^2   &"if" x < 0,
) $
```

## Alignment

Use `&` to align across multiple lines:

```typst
$
  a + b &= c \
        &= d + e
$
```

## Symbols — Named Access

```typst
// Math symbols (available inside $ ... $)
$ alpha, beta, gamma, delta $
$ arrow.r, arrow.l.double $
$ plus.minus, approx, equiv $

// Outside math mode, use #sym prefix
The set #sym.emptyset is empty.
Direction: #sym.arrow.r

// Emoji (always via #emoji)
#emoji.cat #emoji.rocket #emoji.checkmark
```

## Text Inside Math

```typst
// Use quotes for upright text in math
$ "if" x > 0 "then" y = 1 $

// Use upright for single-letter upright
$ upright(d) x $   // differential d
$ dif x $          // shorthand for differential
```

## Common Mistakes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Subscript only takes first char | Multi-char subscript not grouped | Use `x_(i j)` with parentheses |
| Text in math is italicized | Bare letters are variables | Wrap text in `"quotes"` |
| Wrong symbol rendered | Guessed symbol name | Look up via `sym.` namespace |
| Delimiter mismatch in matrix | Missing semicolons between rows | Rows separated by `;`, columns by `,` |
| Equation not centered | No space/newline after opening `$` | `$ ... $` (with whitespace) for block mode |

## Exact Lookup

- Use `query_reference.py` for symbol-heavy lookups because the broad index covers far more symbol data than the lightweight inventory.
