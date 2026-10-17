    # Interpreter Design Pattern

Interpreter is a **behavioral design pattern**.

> **Interpreter defines a representation for a small language or grammar and provides a way to evaluate expressions written in that language.**

A common implementation has stages such as:

```text
Raw Text
   ↓
Lexing
   ↓
Tokens
   ↓
Parsing
   ↓
Expression Tree
   ↓
Interpret / Evaluate
   ↓
Result
```

For example:

```text
"(13+4)-(12+1)"
```

can be converted into structured objects and then evaluated.

---

# Why Do We Need Interpreter?

Suppose an application must understand a small language such as:

```text
1 + 2
```

or:

```text
(13 + 4) - (12 + 1)
```

A normal program sees this as:

```text
characters in a string
```

It does not automatically understand:

```text
13
+
4
-
(...)
```

We need to convert the text into something the program understands.

---

# High-Level Flow

```text
"(13+4)-(12+1)"
          ↓
        Lexer
          ↓
( 13 + 4 ) - ( 12 + 1 )
          ↓
        Parser
          ↓
Expression Objects / Tree
          ↓
       Evaluate
          ↓
           4
```

---

# Important Terminology

## Lexing

Lexing means:

> Breaking raw text into meaningful lexical tokens.

Input:

```text
13 + 4
```

Tokens:

```text
INTEGER(13)
PLUS
INTEGER(4)
```

The lexer answers:

> What symbols are present?

---

## Parsing

Parsing means:

> Taking those tokens and determining their structure according to the grammar.

Tokens:

```text
13
+
4
```

become conceptually:

```text
Addition
├── 13
└── 4
```

The parser answers:

> How are these tokens related?

---

## Interpretation

Interpretation means:

> Evaluate the structured expression according to the language rules.

```text
Addition
├── 13
└── 4
```

becomes:

```text
17
```

---

# Easy Revision

```text
Lexer
→ Characters → Tokens

Parser
→ Tokens → Structure

Interpreter
→ Structure → Meaning / Result
```

---

# Our Small Language

This example understands:

```text
Integers
+
-
(
)
```

So the grammar is intentionally small.

It does **not** currently support:

```text
*
/
operator precedence
variables
functions
complex nested expressions
```

without additional parser logic.

---

# Token

A Token represents one meaningful piece of the input.

```python
from enum import Enum


class Token:
    class Type(Enum):
        INTEGER = 0
        PLUS = 1
        MINUS = 2
        LPAREN = 3
        RPAREN = 4

    def __init__(self, token_type, text):
        self.type = token_type
        self.text = text

    def __str__(self):
        return f"`{self.text}`"
```

Examples:

```text
"13"
→ INTEGER

"+"
→ PLUS

"("
→ LPAREN
```

---

# Why Tokens?

Instead of repeatedly reasoning about raw characters:

```text
'1'
'3'
'+'
'4'
```

we create meaningful objects:

```text
INTEGER("13")
PLUS("+")
INTEGER("4")
```

This makes later processing much easier.

---

# Lexing

The lexer reads the input from left to right.

Conceptually:

```text
Input Character
      ↓
What is it?
      ↓
------------------------
|   |    |    |       |
+   -    (    )     Number
```

and emits the corresponding Token.

---

# Corrected Lexer

Your original lexer has one important edge case:

If the expression ends with a number, the number may not be appended because the code only appends the integer when it encounters a non-digit.

A cleaner version is:

```python
def lex(expression):
    result = []
    i = 0

    while i < len(expression):

        char = expression[i]

        if char == "+":
            result.append(
                Token(Token.Type.PLUS, "+")
            )

        elif char == "-":
            result.append(
                Token(Token.Type.MINUS, "-")
            )

        elif char == "(":
            result.append(
                Token(Token.Type.LPAREN, "(")
            )

        elif char == ")":
            result.append(
                Token(Token.Type.RPAREN, ")")
            )

        elif char.isdigit():
            digits = []

            while (
                i < len(expression)
                and expression[i].isdigit()
            ):
                digits.append(expression[i])
                i += 1

            result.append(
                Token(
                    Token.Type.INTEGER,
                    "".join(digits)
                )
            )

            continue

        i += 1

    return result
```

---

# Lexing Example

Input:

```text
(13+4)
```

Output:

```text
`
(`
`13`
`+`
`4`
`)`
```

More meaningfully:

```text
LPAREN
INTEGER(13)
PLUS
INTEGER(4)
RPAREN
```

---

# Why Multi-Digit Handling Matters

Without grouping digits:

```text
13
```

could incorrectly become:

```text
INTEGER(1)
INTEGER(3)
```

Instead, the lexer must recognize:

```text
13
```

as one token.

---

# Parsing

After lexing, we have tokens but still need to represent the expression itself.

For example:

```text
13 + 4
```

should become:

```text
BinaryOperation
├── left  = Integer(13)
├── type  = ADDITION
└── right = Integer(4)
```

This is where parsing starts.

---

# Integer Expression

```python
class Integer:
    def __init__(self, value):
        self.value = value
```

This represents a terminal expression:

```text
13
```

Its interpretation is simply:

```text
13
```

---

# BinaryOperation

```python
class BinaryOperation:
    class Type(Enum):
        ADDITION = 0
        SUBTRACTION = 1

    def __init__(self):
        self.type = None
        self.left = None
        self.right = None

    @property
    def value(self):
        if self.type == self.Type.ADDITION:
            return (
                self.left.value
                + self.right.value
            )

        elif self.type == self.Type.SUBTRACTION:
            return (
                self.left.value
                - self.right.value
            )
```

A BinaryOperation represents:

```text
Left Expression
      ↓
   Operator
      ↓
Right Expression
```

For example:

```text
13 + 4
```

becomes:

```text
BinaryOperation
├── left  → Integer(13)
├── type  → ADDITION
└── right → Integer(4)
```

---

# Recursive Expressions

The important part is that:

```text
left
```

and:

```text
right
```

do not necessarily have to be plain integers.

They can themselves be:

```text
BinaryOperation
```

That lets us represent:

```text
(13 + 4) - (12 + 1)
```

as a tree.

---

# Expression Tree

Conceptually:

```text
            SUBTRACTION
            /         \
      ADDITION       ADDITION
      /     \         /     \
    13       4      12       1
```

Evaluation happens from the leaves upward.

```text
13 + 4 = 17
12 + 1 = 13

17 - 13 = 4
```

---

# Parser

Your parser builds a `BinaryOperation` from the tokens.

Core idea:

```python
def parse(tokens):
    result = BinaryOperation()

    have_lhs = False
    i = 0
```

`have_lhs` means:

> Have we already found the left-hand side?

---

# Integer Token

```python
if token.type == Token.Type.INTEGER:
    integer = Integer(
        int(token.text)
    )

    if not have_lhs:
        result.left = integer
        have_lhs = True
    else:
        result.right = integer
```

So:

```text
13 + 4
```

first gives:

```text
left = 13
```

and later:

```text
right = 4
```

---

# Operator Tokens

```python
elif token.type == Token.Type.PLUS:
    result.type = (
        BinaryOperation.Type.ADDITION
    )
```

and:

```python
elif token.type == Token.Type.MINUS:
    result.type = (
        BinaryOperation.Type.SUBTRACTION
    )
```

This determines how:

```text
left
```

and:

```text
right
```

will be interpreted.

---

# Parentheses

When the parser encounters:

```text
(
```

it extracts the tokens inside the parentheses.

Conceptually:

```text
(13 + 4)
   ↓
13 + 4
   ↓
parse(...)
   ↓
BinaryOperation
```

That parsed expression can then become either:

```text
left
```

or:

```text
right
```

of another BinaryOperation.

---

# Recursive Parsing

This is an important Interpreter idea.

Given:

```text
(13 + 4)
```

the parser recursively calls:

```python
parse(subexpression)
```

So:

```text
Expression
   ↓
Contains Expression
   ↓
parse()
   ↓
Contains Expression
```

This naturally produces a tree.

---

# Evaluation

The `value` property performs the actual interpretation.

For:

```text
13 + 4
```

we get:

```python
left.value + right.value
```

Result:

```text
17
```

For:

```text
(13 + 4) - (12 + 1)
```

evaluation becomes:

```text
left.value
→ 17

right.value
→ 13

17 - 13
→ 4
```

---

# Full Flow

```python
def evaluate(expression):
    tokens = lex(expression)

    print(
        " ".join(
            map(str, tokens)
        )
    )

    parsed = parse(tokens)

    print(
        f"{expression} = "
        f"{parsed.value}"
    )
```

I would prefer the name:

```python
evaluate()
```

instead of:

```python
eval()
```

because Python already has a built-in function called:

```python
eval()
```

Shadowing built-ins can make code confusing.

---

# Example 1

```python
evaluate(
    "(13+4)-(12+1)"
)
```

Conceptually:

```text
Lex

(
13
+
4
)
-
(
12
+
1
)
```

Then parse:

```text
           -
         /   \
        +     +
       / \   / \
      13  4 12  1
```

Then evaluate:

```text
17 - 13
= 4
```

---

# Example 2

```python
evaluate(
    "1+(3-4)"
)
```

Expression tree:

```text
       +
      / \
     1   -
        / \
       3   4
```

Evaluation:

```text
3 - 4 = -1

1 + (-1)
= 0
```

---

# Why `1+2+(3-4)` Does Not Work

Your parser is deliberately simple.

It assumes roughly:

```text
left
operator
right
```

So it works well for:

```text
A + B
```

or:

```text
A - B
```

where `A` and `B` may themselves contain a parenthesized expression.

But:

```text
1 + 2 + (3 - 4)
```

has multiple operations at the same level:

```text
1
+
2
+
(...)
```

The current `BinaryOperation` parser does not properly build a tree for that sequence.

---

# What a More Complete Parser Would Do

It could transform:

```text
1 + 2 + (3 - 4)
```

into something such as:

```text
           +
         /   \
        +     -
       / \   / \
      1   2 3   4
```

Then:

```text
1 + 2 = 3
3 - 4 = -1

3 + (-1)
= 2
```

Building this correctly requires a more capable grammar/parser.

---

# Another Limitation — Parentheses Matching

Your parser searches for the next:

```text
RPAREN
```

after an `LPAREN`.

That works for simple parentheses such as:

```text
(1 + 2)
```

but may fail for deeply nested expressions such as:

```text
(1 + (2 - 3))
```

because proper parenthesis matching needs to track nesting depth.

Conceptually:

```text
(
   (
   )
)
```

requires:

```text
depth = 0
```

and increment/decrement while scanning.

---

# This Is Still Fine for Learning the Pattern

The purpose of this example is not to build a production compiler.

It demonstrates:

```text
Text
 ↓
Tokens
 ↓
Expression Objects
 ↓
Recursive Interpretation
```

That is the important design idea.

---

# Interpreter Pattern Structure

A classic Interpreter design often contains:

```text
Expression
├── TerminalExpression
└── NonTerminalExpression
```

---

# Terminal Expression

A terminal expression cannot be broken into smaller expressions.

In this example:

```text
Integer
```

is effectively a terminal expression.

Example:

```text
13
```

---

# Non-Terminal Expression

A non-terminal expression contains other expressions.

In this example:

```text
BinaryOperation
```

is a non-terminal expression.

Example:

```text
13 + 4
```

contains:

```text
Integer(13)
Integer(4)
```

---

# Structure of This Example

```text
Expression Concept
       ↓
---------------------------
|                         |
Integer             BinaryOperation
Terminal            Non-Terminal
                         |
                  ----------------
                  |              |
                Left           Right
```

---

# Grammar Idea

We can think about the language roughly as:

```text
Expression
→ Integer
→ Expression + Expression
→ Expression - Expression
→ (Expression)
```

This is not a full formal grammar for the exact parser implementation, but it captures the idea.

The Interpreter implementation represents these grammar rules using objects.

---

# Real-World Examples

Interpreter is useful for relatively small languages such as:

## Mathematical Expressions

```text
1 + 2 - 3
```

---

## Search Filters

```text
age > 18 AND country = "India"
```

---

## Rule Engines

```text
IF balance > 1000
AND user_is_active
THEN allow
```

---

## Configuration Expressions

```text
environment == "production"
```

---

## Query Languages / DSLs

A domain-specific language might support:

```text
SEND email TO user
```

and interpret that according to its grammar.

---

# When to Use Interpreter

Use Interpreter when:

- You have a small language or DSL
- Input follows a defined grammar
- Rules can be represented as expression objects
- Expressions need to be evaluated repeatedly
- The grammar is relatively simple

---

# When NOT to Use Interpreter

Avoid building your own Interpreter for a large language such as:

```text
Java
Python
SQL
```

A real language may require:

- Complex grammar
- Operator precedence
- Error recovery
- Type checking
- Scope handling
- Optimization
- Large ASTs

For complex grammars, use established parser/compiler tooling.

---

# Benefits

Interpreter provides:

- Clear representation of grammar rules
- Easy extension for small languages
- Recursive composition
- Separation between parsing and evaluation
- Natural representation using expression trees

---

# Drawbacks

As grammar grows:

```text
More grammar rules
      ↓
More expression classes
      ↓
More parser complexity
```

The design can become difficult to maintain.

Interpreter works best for:

> Small and focused languages.

---

# Interpreter vs Command

These are both behavioral patterns, but different.

## Command

Represents:

```text
An instruction/action to execute
```

Example:

```text
DepositCommand
```

---

## Interpreter

Represents:

```text
Grammar/expression to understand
```

Example:

```text
13 + 4
```

Easy revision:

```text
Command
→ Execute an instruction

Interpreter
→ Understand/evaluate a language expression
```

---

# Interpreter vs Strategy

## Strategy

Chooses between different algorithms.

```text
Sort Strategy
Payment Strategy
```

## Interpreter

Processes expressions according to grammar rules.

```text
Tokens
→ Expression Tree
→ Evaluate
```

---

# AST — Useful Related Concept

A parser commonly produces an:

> **Abstract Syntax Tree (AST)**

For:

```text
13 + 4
```

an AST might look like:

```text
   +
  / \
13   4
```

For:

```text
(13 + 4) - 1
```

it could look like:

```text
       -
      / \
     +   1
    / \
   13  4
```

Your:

```text
Integer
BinaryOperation
```

objects effectively form a very small expression tree similar to an AST.

---

# Interview Question

## What is the Interpreter Pattern?

Interpreter is a behavioral design pattern used when an application needs to understand expressions written in a small language or grammar.

The input is usually transformed into structured expressions and then evaluated according to grammar rules.

For example:

```text
"(13+4)-(12+1)"
```

can be:

```text
Lexed
→ Tokens

Parsed
→ Expression Tree

Interpreted
→ 4
```

In this example, `Integer` represents terminal expressions and `BinaryOperation` represents compound expressions.

---

# How to Recognize Interpreter

Look for this problem:

> "My application receives structured text containing rules or expressions, and I need to understand and evaluate what that text means."

Then think:

```text
Text
 ↓
Tokenize
 ↓
Parse
 ↓
Expression Representation
 ↓
Interpret
```

Interpreter may be appropriate.

---

# Mental Model

Think about a calculator.

You enter:

```text
2 + 3
```

The calculator cannot treat:

```text
"2 + 3"
```

as just meaningless characters.

It must understand:

```text
2
→ number

+
→ addition

3
→ number
```

and then interpret:

```text
2 + 3
= 5
```

That is the Interpreter mindset.

---

# Quick Revision

```text
Interpreter
→ Behavioral Design Pattern
```

```text
Goal
→ Understand/evaluate a small language
```

```text
Lexing
→ Raw characters → Tokens
```

```text
Parsing
→ Tokens → Expression structure/tree
```

```text
Interpretation
→ Expression tree → Meaning/result
```

```text
Integer
→ Terminal Expression
```

```text
BinaryOperation
→ Non-Terminal Expression
```

```text
Example

"(13+4)-(12+1)"

Text
 ↓
Tokens
 ↓
Tree
 ↓
4
```

```text
AST
→ Structured representation of expression
```

```text
Best Fit
→ Small grammars / DSLs
```

---

# Key Takeaways

- **Interpreter is a behavioral design pattern.**
- **Its purpose is to represent and evaluate expressions from a small language or grammar.**
- **Lexing converts raw text into tokens.**
- **Parsing converts tokens into meaningful structure.**
- **Interpretation evaluates that structure.**
- **`Integer` acts like a terminal expression.**
- **`BinaryOperation` acts like a non-terminal expression containing other expressions.**
- **Recursive expressions naturally form a tree similar to an AST.**
- **Your current parser supports only a limited subset of expressions.**
- **`1+2+(3-4)` fails because the parser does not properly support multiple same-level binary operations.**
- **Nested parentheses require proper matching rather than simply selecting the next `)` token.**
- **Avoid naming your own function `eval()` because it shadows Python's built-in `eval`.**
- **Interpreter is best suited to small DSLs and simple grammars rather than full programming languages.**

# One-Line Revision

> **Interpreter = define a small language as expression objects, turn input text into those expressions, and evaluate the resulting structure according to the language's grammar.**