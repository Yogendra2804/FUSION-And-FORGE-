# FUSION-And-FORGE 𒚡🛠

## A language interoperability experiment between Java-like syntax and Python

**FUSION-And-FORGE** is an experimental language-processing and runtime project exploring whether Java-like syntax can be interpreted and executed within a Python environment.

The project started from a simple problem:

> What if you remember how to solve something in another programming language, but don’t remember the exact syntax required to express it in Python?

For example:

```python
arr = [3, 1, 2]

result = java("""
    Collections.sort(arr);
    return arr;
""")
```

The goal is for FORGE to understand the Java-like source, determine its structure, resolve the Python objects referenced by it, and execute the supported operation against the existing Python runtime.

The long-term vision is to make this a genuine language-processing system rather than a collection of string replacements.

---

## 🛠 FUSION and FORGE

### FUSION

FUSION is the broader language idea behind the project:

> A system where constructs inspired by different programming languages can coexist through a common execution model.

### FORGE

FORGE is the experimental toolchain being built to explore that idea.

The current work focuses on building the fundamental components required for such a system:

```
Source Code
     |
     v
 Tokenization
     |
     v
   Parsing
     |
     v
    AST
     |
     v
Runtime Resolution
     |
     v
 Interpretation / Execution
     |
     v
 Python Runtime
```

Each stage is being developed and tested independently before being connected into the larger system.

---

## 🔍 Why build this?

Different languages often express the same programming idea using different syntax and APIs.

For example:

```java
Collections.sort(arr);
```

and:

```python
arr.sort()
```

may represent the same underlying intention while requiring different language knowledge.

FUSION explores whether the developer can express that intention using familiar syntax while FORGE handles the language-processing and runtime side of the problem.

The interesting part of the project is therefore not simply translating one string into another.

It is understanding:

- What does the source code contain?
- What structure does it represent?
- What does that structure mean?
- Which runtime objects does it reference?
- What operation should actually be performed?
- How should the result be returned to the host program?

---

## 🧩 Current Architecture

### 1. Tokenization

The first stage converts source code into meaningful tokens.

For example:

```
Collections.sort(arr);
```

becomes:

```
IDENTIFIER   Collections
DOT          .
IDENTIFIER   sort
LPAREN       (
IDENTIFIER   arr
RPAREN       )
SEMICOLON    ;
```

The tokenizer currently experiments with:

- Identifiers
- Keywords
- Integer literals
- Floating-point literals
- Boolean literals
- String literals
- Operators
- Parentheses, commas, semicolons
- Member access (`.`)

Keywords and operators are represented through lookup structures so that the lexer can grow without requiring a separate conditional branch for every new language element.

```python
KEYWORDS = {
    "int": "INT",
    "float": "FLOAT",
    "double": "DOUBLE",
    "boolean": "BOOLEAN",
    "true": "BOOLEAN TRUE",
    "false": "BOOLEAN FALSE",
    "char": "CHAR",
    "String": "STRING",
    "return": "RETURN",
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE"
}
```

This means adding a new keyword is a single dictionary entry, not a new branch in the logic.

---

### 🌳 2. Parsing and AST

Tokens alone do not describe the complete meaning of a program.

Consider:

```java
method(a, getValue(x, y), c)
```

The parser needs to understand that `method(...)` is a call containing multiple arguments, while `getValue(x, y)` is itself another nested call.

This requires a hierarchical representation rather than a flat list.

The AST is intended to represent relationships such as:

```
MethodCall
├── method
├── a
├── MethodCall
│   ├── getValue
│   ├── x
│   └── y
└── c
```

This structure will eventually allow FORGE to reason about expressions rather than individual characters or strings.

---

### 🔗 3. Runtime Integration

One of the interesting problems in the project is connecting the Java-like code with the Python program that called it.

For example:

```python
arr = [3, 1, 2]

java("""
    Collections.sort(arr);
""")
```

The `arr` inside the Java-like source is not a new Forge variable. It refers to an existing Python object.

FORGE therefore needs to discover the identifiers referenced by the source and resolve them against the runtime environment of the calling Python program.

The project has already explored Python’s frame inspection mechanisms to access the caller’s runtime locals:

```python
import inspect

def java(code):
    caller = inspect.currentframe().f_back
    # tokenize the source to find which identifiers are referenced
    # then resolve only those names from the caller's locals
    caller_locals = caller.f_locals
```

Conceptually:

```
Forge source
     |
     v
Referenced identifier
     |
     v
Caller runtime environment  (via inspect.currentframe().f_back)
     |
     v
Python object
```

This allows FORGE to work with the actual objects already present in the host Python program — without the user manually passing variables.

---

### ⚙️ 4. Execution

Once the source has been tokenized, parsed, and represented structurally, FORGE can determine what operation is being requested.

For example:

```java
Collections.sort(arr);
```

can eventually be represented conceptually as:

```
MethodCall
│
├── Collections
├── sort
└── arr
```

The runtime can then resolve:

```
Collections  ->  supported library/object
arr          ->  existing Python object from caller
sort         ->  supported operation
```

and perform the corresponding operation within the Python runtime.

---

## 🧠 Design Direction

The project is intentionally being built around language-processing concepts rather than treating the source as plain text.

The intended progression is:

```
Characters
    |
Tokens
    |
Syntax
    |
AST
    |
Meaning
    |
Runtime values
    |
Execution
```

This separation is important because syntax and execution are different problems.

`Collections.sort(arr)` first needs to be understood structurally. Only after that should FORGE determine what `Collections`, `sort`, and `arr` represent and how the operation should be executed.

---

## 🚧 Current Status — Early Development (V0)

### ✅ Completed / experimentally demonstrated

- [x] Initial FUSION/FORGE concept
- [x] Runtime frame inspection experiments
- [x] Caller-local variable resolution
- [x] Identifier discovery from source
- [x] Tokenization prototype
  - [x] Keyword recognition
  - [x] Operator recognition
  - [x] Integer literals
  - [x] Floating-point literals
  - [x] Boolean literals
  - [x] String literals
  - [x] Parentheses and nested-expression handling

### 🔄 Currently being developed

- [ ] Robust parser
- [ ] Formal AST structure
- [ ] Semantic analysis
- [ ] Runtime environment
- [ ] Operation dispatch
- [ ] Java-like library abstractions
- [ ] Execution engine
- [ ] Forge-specific error reporting
- [ ] Test suite
- [ ] Integrated V0

---

## 🗺 Roadmap

### Phase 1 — Language Foundation
Build a reliable foundation for the language:
- Lexer / tokenizer
- Parser
- AST
- Syntax validation

### Phase 2 — Runtime Bridge
Connect the language to the Python environment:
- Identifier resolution
- Runtime scope
- Argument resolution
- Object references
- Return values

### Phase 3 — Execution
Build the execution layer:
- Expressions
- Method calls / function calls
- Operators and assignments
- Java-like library operations

### Phase 4 — Control Flow
Expand the language:
- `if` / `else`
- `while`
- Functions and scope

### Phase 5 — Developer Experience
Make FORGE usable:
- Line/column-aware error messages
- Syntax errors with context
- Runtime errors with diagnostics
- Test coverage
- Documentation

### Phase 6 — V0
Combine the components into a small but functional Java-like execution environment running inside Python.

---

## 🔬 Development Approach

FORGE is being developed incrementally.

Instead of designing the entire language first, individual problems are explored through small experiments.

For example:

```
"How do I access the caller's runtime variables?"
        |
inspect.currentframe()
        |
caller frame  (f_back)
        |
f_locals
        |
actual Python values
```

Similarly:

```
"How do I understand nested calls?"
        |
tokenization
        |
parenthesis depth tracking
        |
parser
        |
AST
```

The experiments in the `experiments/` directory are part of this process. They validate the underlying ideas before those ideas become integrated components.

---

## ⚠️ Current Scope

FUSION-And-FORGE is not intended to implement the entire Java language.

The initial goal is a focused Java-like subset that demonstrates the core architecture:

```
Java-like syntax
        |
Language processing
        |
AST
        |
Runtime resolution
        |
Python execution
```

The supported language will grow only as the underlying architecture becomes capable of handling it.

---

## 🌱 Long-Term Vision

The immediate goal is **FORGE V0**.

The larger goal is **FUSION**.

FORGE provides a practical environment in which ideas around language interoperability, interpreters, parsers, ASTs, runtime environments, and execution models can be explored.

The long-term vision is to investigate whether constructs from different programming languages can be represented through a shared execution model — rather than treating each language as an isolated system.

---

**Status:** 🚧 Under active development

**FUSION ⚡️ × FORGE 🛠**
