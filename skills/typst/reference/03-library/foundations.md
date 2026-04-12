# Foundations

## Use

- Handle core value types, utility functions, module-level helpers, and the broad base layer of the Typst standard library.

## Authoritative Sources

- `typst/docs/reference/library/foundations.md`
- `typst/crates/typst-library/src/foundations/**`
- `typst/docs/reference/groups.yml`

## What Lives Here

- primitive and container types such as `array`, `dictionary`, `str`, `bytes`, `version`, and `datetime`
- content-facing helpers such as `content`, `repr`, and conversion-related utilities
- globally visible helper modules and scopes such as `std`, `calc`, and `sys`
- many exact APIs that other categories build on top of

## Array Methods

```typst
#let data = (3, 1, 4, 1, 5, 9)

// map — transform each element
#data.map(x => x * 2)          // (6, 2, 8, 2, 10, 18)

// filter — keep matching elements
#data.filter(x => x > 3)       // (4, 5, 9)

// sorted — return sorted copy
#data.sorted()                  // (1, 1, 3, 4, 5, 9)

// join — combine into string
#("A", "B", "C").join(", ")    // "A, B, C"

// fold — accumulate a result
#data.fold(0, (acc, x) => acc + x)  // 23

// len, first, last, at
#data.len()                     // 6
#data.first()                   // 3
#data.at(2)                     // 4

// enumerate — index-value pairs
#for (i, v) in data.enumerate() {
  [#i: #v ]
}

// slice
#data.slice(1, 4)               // (1, 4, 1)
```

## Dictionary Operations

```typst
// Create
#let person = (name: "Alice", age: 30, city: "Zurich")

// Access
#person.name                    // Alice
#person.at("age")               // 30
#person.at("email", default: "N/A")  // N/A

// Keys and values
#person.keys()                  // ("name", "age", "city")
#person.values()                // ("Alice", 30, "Zurich")
#person.pairs()                 // (("name","Alice"), ("age",30), ...)
#person.len()                   // 3

// Iterate
#for (key, value) in person {
  [#key: #value \ ]
}

// Spread merge
#let updated = (..person, email: "alice@example.com")
```

## String Methods

```typst
#let s = "  Hello, Typst World!  "

// trim — remove surrounding whitespace
#s.trim()                       // "Hello, Typst World!"

// split — divide into array
#"a,b,c".split(",")            // ("a", "b", "c")

// replace
#"foo bar foo".replace("foo", "baz")  // "baz bar baz"

// contains, starts-with, ends-with
#"hello".contains("ell")       // true
#"hello".starts-with("he")     // true

// len and at
#"hello".len()                  // 5

// match and matches (regex)
#"hello123".match(regex("\d+"))
```

## Calc Module

```typst
// Absolute value
#calc.abs(-42)                  // 42

// Min and max
#calc.min(3, 7, 1)             // 1
#calc.max(3, 7, 1)             // 7

// Rounding
#calc.round(3.456, digits: 2)  // 3.46
#calc.floor(3.7)               // 3
#calc.ceil(3.2)                 // 4

// Power and root
#calc.pow(2, 10)               // 1024
#calc.sqrt(144)                // 12

// Trigonometry
#calc.sin(90deg)               // 1
#calc.cos(0deg)                // 1

// Logarithms
#calc.log(100, base: 10)      // 2

// Remainder
#calc.rem(17, 5)               // 2
```

## Type Conversions

```typst
// To integer
#int(3.7)                       // 3
#int("42")                      // 42

// To float
#float("3.14")                  // 3.14
#float(7)                       // 7.0

// To string
#str(42)                        // "42"
#str(3.14)                      // "3.14"
#str(true)                      // "true"

// repr — debug representation
#repr((1, "two", true))         // "(1, \"two\", true)"

// type — query value type
#type(42)                       // integer
#type("hi")                     // string
#type((1, 2))                   // array
```

## Datetime and Duration

```typst
// Create a datetime
#let d = datetime(year: 2026, month: 4, day: 12)
#d.display("[month repr:long] [day], [year]")
// → April 12, 2026

// Current date (requires --input or context)
#datetime.today().display()

// Duration
#let dur = duration(hours: 2, minutes: 30)
```

## Version Type

```typst
#let v = version(0, 13, 1)
#v.at(0)   // 0  (major)
#v.at(1)   // 13 (minor)
#v.at(2)   // 1  (patch)

// sys.version — current Typst compiler version
#sys.version
```

## Guidance

- Treat `foundations` as the broad base layer, not as a single narrow feature page.
- When answering exact API questions here, query the generated indexes instead of relying on memory.
- Distinguish between `calc` helpers, `sys` environment values, and category-specific library functions.
- If a task mixes data conversion, formatting, and generic computation, this category is often involved even when the user did not name it.

## Exact Lookup

- Start with `python skills/typst/scripts/query_reference.py --query <name>`.
- Use `query_api_index.py` when you want a quick official source anchor by name or category.
