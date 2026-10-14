# Spec: textkit slug, trim and CLI

## Problem
Scripts need URL slugs and short previews of text, from Python and from the shell.

## User stories
1. As a developer, I call `slugify(text)` from `textkit.slug` to get a URL slug.
2. As a developer, I call `truncate(text, width)` from `textkit.trim` to get a preview no longer than `width`.
3. As a shell user, I run `python3 -m textkit slug <text>` or `python3 -m textkit trim <width> <text>` and get the result on stdout.

## Acceptance
- AC1 `slugify("Hello, World!") == "hello-world"`; runs of non-alphanumeric characters become one `-`; leading/trailing `-` are removed; `slugify("   ") == ""`. Reuse `textkit.core.normalize` first.
- AC2 `truncate("abcdef", 4) == "abc…"`; `truncate("abc", 4) == "abc"`; `truncate("abcd", 4) == "abcd"`; width < 1 raises `ValueError("width must be >= 1")`.
- AC3 `python3 -m textkit slug "Hello World"` prints `hello-world` and exits 0; `python3 -m textkit trim 4 abcdef` prints `abc…` and exits 0; an unknown command `x` prints `unknown command: x` to stderr and exits 2. Tests call the CLI with subprocess.

## Commands
- Init: None. Python 3 standard library only; no dependencies.
- Single test file: `python3 -B -m unittest tests.<module> -v`
- Full suite: `python3 -B -m unittest discover -s tests -v`
- Typecheck: N/A (stdlib-only fixture with no type checker configured).

## Out of scope
Unicode transliteration, configuration files, packaging.
