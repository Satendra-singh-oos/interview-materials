# Visitor Design Pattern

Visitor is a **behavioral design pattern**.

> **Visitor separates an operation from the object structure on which that operation works.**

Instead of putting every possible operation inside your domain classes:

```text
DoubleExpression
├── print()
├── eval()
├── serialize()
├── validate()
├── export()
└── ...
```

we move those operations into separate Visitor objects:

```text
Expression Objects
      ↓
    Visitor
      ↓
Operation
```

For example:

```text
Expression Structure
├── DoubleExpression
└── AdditionExpression

Visitors
├── ExpressionPrinter
├── ExpressionEvaluator
└── ExpressionSerializer
```

The expression objects mainly represent:

> **What the structure is.**

Visitors represent:

> **What we want to do with that structure.**

---

# Why Do We Need Visitor?

Suppose we are building an expression tree.

For:

```text
1 + (2 + 3)
```

the structure is:

```text
        +
       / \
      1   +
         / \
        2   3
```

We might represent it using:

```text
DoubleExpression
AdditionExpression
```

Now imagine we want several operations:

```text
Print expression
Evaluate expression
Convert to JSON
Convert to XML
Validate expression
Generate code
```

One approach is to keep adding methods to every expression class.

That can become problematic.

---

# Without Visitor

```text
DoubleExpression
├── print()
├── eval()
├── to_json()
├── to_xml()
└── validate()

AdditionExpression
├── print()
├── eval()
├── to_json()
├── to_xml()
└── validate()
```

Every time we add a new operation:

```text
generate_sql()
```

we must modify:

```text
DoubleExpression
AdditionExpression
Every other expression type
```

This means operation logic gets spread across the entire hierarchy.

Visitor turns this around.

---

# With Visitor

Objects stay focused on their structure:

```text
DoubleExpression
AdditionExpression
MultiplicationExpression
```

Operations live elsewhere:

```text
PrinterVisitor
EvaluatorVisitor
JsonVisitor
ValidationVisitor
```

Conceptually:

```text
            Expressions
                 ↓
      ------------------------
      |          |           |
   Printer    Evaluator    Serializer
   Visitor     Visitor       Visitor
```

---

# Core Visitor Mental Model

Think:

```text
Object Structure
      +
Operation Object
      =
Behavior
```

The object says:

> "This is the kind of element I am."

The Visitor says:

> "I know what to do with that kind of element."

---

# Example Expression Structure

Your examples use:

```python
class DoubleExpression:
    def __init__(self, value):
        self.value = value
```

and:

```python
class AdditionExpression:
    def __init__(self, left, right):
        self.left = left
        self.right = right
```

Expression:

```text
1 + (2 + 3)
```

becomes:

```text
AdditionExpression
├── DoubleExpression(1)
└── AdditionExpression
    ├── DoubleExpression(2)
    └── DoubleExpression(3)
```

---

# 1. Intrusive Approach

Your first implementation puts operations directly into the expression classes.

```python
class DoubleExpression:
    def __init__(self, value):
        self.value = value

    def print(self, buffer):
        buffer.append(
            str(self.value)
        )

    def eval(self):
        return self.value
```

And:

```python
class AdditionExpression:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def print(self, buffer):
        buffer.append("(")

        self.left.print(buffer)

        buffer.append("+")

        self.right.print(buffer)

        buffer.append(")")

    def eval(self):
        return (
            self.left.eval()
            + self.right.eval()
        )
```

---

# What Happens?

For:

```text
1 + (2 + 3)
```

printing recursively traverses:

```text
Addition
   ↓
Left = 1
   ↓
Right = Addition
           ↓
        2 + 3
```

Output:

```text
(1+(2+3))
```

Evaluation:

```text
2 + 3 = 5

1 + 5 = 6
```

---

# Why Is It Called Intrusive?

Because every operation must be inserted directly into the domain classes.

For example:

```text
DoubleExpression
```

must know how to:

```text
print
evaluate
serialize
validate
...
```

The operation is:

> **Intruding into the object hierarchy.**

---

# OCP Problem

Suppose we now want:

```text
XML export
```

We may need to modify:

```text
DoubleExpression
AdditionExpression
MultiplicationExpression
DivisionExpression
...
```

and add:

```python
to_xml()
```

to every one.

Then later:

```text
JSON export
```

requires another round of modifications.

So if:

```text
Expression types stay mostly stable
```

but:

```text
New operations are frequently added
```

this design is inconvenient.

---

# Important Question

When choosing Visitor, ask:

> **What changes more often: element types or operations?**

If:

```text
Types are stable
Operations change frequently
```

Visitor is often useful.

If:

```text
New types appear frequently
```

Visitor can become painful.

This trade-off is central to understanding the pattern.

---

# 2. Reflective Visitor

The second approach removes:

```text
print()
```

from expression objects.

Now the classes only represent data.

```python
from abc import ABC


class Expression(ABC):
    pass


class DoubleExpression(Expression):
    def __init__(self, value):
        self.value = value


class AdditionExpression(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right
```

Printing is moved into:

```text
ExpressionPrinter
```

---

# ExpressionPrinter

```python
class ExpressionPrinter:

    @staticmethod
    def print(expression, buffer):

        if isinstance(
            expression,
            DoubleExpression
        ):
            buffer.append(
                str(expression.value)
            )

        elif isinstance(
            expression,
            AdditionExpression
        ):
            buffer.append("(")

            ExpressionPrinter.print(
                expression.left,
                buffer
            )

            buffer.append("+")

            ExpressionPrinter.print(
                expression.right,
                buffer
            )

            buffer.append(")")
```

Now:

```text
Expression Classes
→ Hold structure/data

ExpressionPrinter
→ Knows printing logic
```

This is already better separation.

---

# Why "Reflective"?

Because we inspect the runtime type:

```python
isinstance(
    expression,
    DoubleExpression
)
```

and:

```python
isinstance(
    expression,
    AdditionExpression
)
```

The operation asks:

> "What kind of object did I receive?"

Then selects behavior accordingly.

---

# Flow

Given:

```text
AdditionExpression
```

printer does:

```text
Is DoubleExpression?
→ No

Is AdditionExpression?
→ Yes

Print (
Print left
Print +
Print right
Print )
```

---

# Advantage Over Intrusive Approach

Adding a new operation:

```text
ExpressionEvaluator
```

does not require adding:

```python
eval()
```

to every Expression class.

We can create:

```text
ExpressionPrinter
ExpressionEvaluator
ExpressionSerializer
```

outside the hierarchy.

That keeps operations separated.

---

# Monkey-Patching in the Example

Your example contains:

```python
Expression.print = (
    lambda self, buffer:
        ExpressionPrinter.print(
            self,
            buffer
        )
)
```

This dynamically attaches:

```text
print()
```

to `Expression`.

Then:

```python
expression.print(buffer)
```

effectively calls:

```python
ExpressionPrinter.print(
    expression,
    buffer
)
```

This is possible in Python because classes can be modified dynamically.

However, for production code this is usually less explicit than simply writing:

```python
ExpressionPrinter.print(
    expression,
    buffer
)
```

The important Visitor idea does not depend on monkey-patching.

---

# Problem With Reflective Visitor

The biggest issue is:

```python
if isinstance(...)
elif isinstance(...)
elif isinstance(...)
```

Suppose we add:

```text
MultiplicationExpression
```

Every operation class may need another branch:

```python
elif isinstance(
    expression,
    MultiplicationExpression
):
```

For example:

```text
ExpressionPrinter
ExpressionEvaluator
ExpressionSerializer
ExpressionValidator
```

all need to learn about the new type.

---

# The Type × Operation Matrix

This is useful for understanding the Visitor trade-off.

Suppose we have element types:

```text
Double
Addition
Multiplication
```

and operations:

```text
Print
Evaluate
Serialize
```

Conceptually:

| | Double | Addition | Multiplication |
|---|---|---|---|
| Print | ✓ | ✓ | ✓ |
| Evaluate | ✓ | ✓ | ✓ |
| Serialize | ✓ | ✓ | ✓ |

Each combination needs behavior.

Visitor reorganizes this matrix primarily by:

```text
Operation
```

rather than by:

```text
Element type
```

---

# If We Add a New Operation

Add:

```text
ValidationVisitor
```

We create one new visitor containing handling for:

```text
Double
Addition
Multiplication
```

The existing expression classes can remain unchanged.

This is where Visitor is strong.

---

# If We Add a New Element Type

Add:

```text
DivisionExpression
```

Now existing Visitors may need:

```text
visit(DivisionExpression)
```

added to each one.

That is where Visitor is weak.

---

# Visitor Trade-Off

```text
New Operation
→ Easy
```

```text
New Element Type
→ Expensive
```

This is one of the most important interview points.

---

# 3. Classic Visitor

The classic Visitor implementation introduces:

```text
accept(visitor)
```

on each element.

Example:

```python
class DoubleExpression:
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        visitor.visit(self)
```

And:

```python
class AdditionExpression:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def accept(self, visitor):
        visitor.visit(self)
```

The element itself does not implement printing.

It only knows:

> "A Visitor can visit me."

---

# ExpressionPrinter Visitor

Conceptually we want:

```python
visit(DoubleExpression)
```

and:

```python
visit(AdditionExpression)
```

to behave differently.

For `DoubleExpression`:

```python
def visit_double(self, expression):
    self.buffer.append(
        str(expression.value)
    )
```

For `AdditionExpression`:

```python
def visit_addition(self, expression):
    self.buffer.append("(")

    expression.left.accept(self)

    self.buffer.append("+")

    expression.right.accept(self)

    self.buffer.append(")")
```

---

# The Python Difficulty

Languages such as Java/C++ commonly support method overloading patterns that make Visitor examples straightforward.

Python normally does not allow this:

```python
def visit(
    self,
    DoubleExpression
):
    ...

def visit(
    self,
    AdditionExpression
):
    ...
```

because the second definition would replace the first one.

Your example therefore implements custom:

> **Multiple dispatch**

using a decorator.

---

# Visitor Decorator

The library code stores methods based on:

```text
Visitor Class
+
Argument Type
```

Conceptually:

```text
ExpressionPrinter + DoubleExpression
→ use DoubleExpression handler

ExpressionPrinter + AdditionExpression
→ use AdditionExpression handler
```

This allows syntax like:

```python
@visitor(DoubleExpression)
def visit(self, expression):
    ...
```

and:

```python
@visitor(AdditionExpression)
def visit(self, expression):
    ...
```

---

# Visitor Method Registry

The code keeps:

```python
_methods = {}
```

which acts approximately like:

```text
(ExpressionPrinter, DoubleExpression)
    → print number

(ExpressionPrinter, AdditionExpression)
    → print addition
```

When:

```python
visitor.visit(expression)
```

runs, the implementation selects the correct function based on:

```text
Runtime Visitor Type
+
Runtime Expression Type
```

---

# Classic ExpressionPrinter

```python
class ExpressionPrinter:
    def __init__(self):
        self.buffer = []

    @visitor(DoubleExpression)
    def visit(self, expression):
        self.buffer.append(
            str(expression.value)
        )

    @visitor(AdditionExpression)
    def visit(self, expression):
        self.buffer.append("(")

        expression.left.accept(
            self
        )

        self.buffer.append("+")

        expression.right.accept(
            self
        )

        self.buffer.append(")")

    def __str__(self):
        return "".join(
            self.buffer
        )
```

---

# Execution

Expression:

```python
e = AdditionExpression(
    DoubleExpression(1),
    AdditionExpression(
        DoubleExpression(2),
        DoubleExpression(3)
    )
)
```

Structure:

```text
        Addition
        /      \
       1      Addition
              /     \
             2       3
```

Create visitor:

```python
printer = ExpressionPrinter()
```

Then:

```python
printer.visit(e)
```

---

# Traversal Flow

The root is:

```text
AdditionExpression
```

So:

```text
ExpressionPrinter.visit(AdditionExpression)
```

runs.

It writes:

```text
(
```

then:

```python
ae.left.accept(self)
```

---

# First `accept()`

The left child is:

```text
DoubleExpression(1)
```

Its:

```python
accept(visitor)
```

calls:

```python
visitor.visit(self)
```

Now dispatch chooses:

```text
visit(DoubleExpression)
```

and outputs:

```text
1
```

---

# Right Side

The right child is another:

```text
AdditionExpression
```

so:

```python
accept(visitor)
```

selects:

```text
visit(AdditionExpression)
```

again.

This recursively processes:

```text
2 + 3
```

Final result:

```text
(1+(2+3))
```

---

# Double Dispatch

This is the most important technical concept behind the classic Visitor.

Visitor commonly uses:

> **Double Dispatch**

Meaning the selected behavior depends on two runtime types:

```text
1. Visitor type
2. Element type
```

Example:

```text
ExpressionPrinter
+
AdditionExpression
```

selects one implementation.

But:

```text
ExpressionEvaluator
+
AdditionExpression
```

would select another.

---

# Why `accept()` Is Needed

Think about:

```python
element.accept(visitor)
```

First dispatch:

```text
Which element object received accept()?
```

Then:

```python
visitor.visit(self)
```

causes the operation to be chosen for that concrete element type.

Conceptually:

```text
Element
   ↓
accept(visitor)
   ↓
visitor.visit(this concrete element)
   ↓
Correct Visitor operation
```

That is the classic Visitor handshake.

---

# Visitor Handshake

A useful memory diagram:

```text
Visitor          Element
   |                |
   |--- visit? ---->|
   |                |
   |<-- accept -----|
   |                |
   |-- visit(this)->|
```

Simpler mental model:

```text
Element says:
"I am an AdditionExpression."

Visitor says:
"Then I know what to do with an AdditionExpression."
```

---

# Adding Another Visitor

Suppose we want evaluation.

We could add:

```text
ExpressionEvaluator
```

with handlers:

```text
DoubleExpression
→ value

AdditionExpression
→ evaluate left + evaluate right
```

The expression classes themselves stay unchanged.

Conceptually:

```text
Expression Structure
        ↓
--------------------------
|                        |
PrinterVisitor      EvaluatorVisitor
```

---

# Why Visitor Helps OCP

Assume your hierarchy is stable:

```text
DoubleExpression
AdditionExpression
```

Now we want:

```text
Print
Evaluate
Serialize
Export
Validate
```

With Visitor we add:

```text
PrinterVisitor
EvaluatorVisitor
SerializerVisitor
ExportVisitor
ValidationVisitor
```

without continually modifying the expression classes.

So Visitor supports OCP primarily along the:

> **Operation axis.**

---

# But Visitor Has an OCP Trade-Off

Suppose we add:

```text
MultiplicationExpression
```

Now:

```text
PrinterVisitor
EvaluatorVisitor
SerializerVisitor
...
```

may all need another handler.

So Visitor does **not** magically make every kind of extension open/closed.

The important question is:

> **Which dimension do we want to optimize for extension?**

---

# Visitor's Sweet Spot

Best situation:

```text
Element Types
→ Stable

Operations
→ Frequently Added
```

Example:

```text
AST Node Types
→ Relatively stable

Operations:
→ Pretty print
→ Type check
→ Generate code
→ Optimize
→ Analyze
→ Serialize
```

This is why Visitor historically appears often around:

```text
Compilers
ASTs
Document models
Object graphs
```

---

# Visitor Is Not Primarily a Traversal Pattern

Your original definition says:

> Visitor knows how to traverse a data structure.

That can happen, but it is not the defining feature.

For example:

```python
ae.left.accept(self)
ae.right.accept(self)
```

means your `ExpressionPrinter` is performing traversal.

But another architecture could have a separate traversal mechanism.

The true idea is:

> **The Visitor contains operations for different element types.**

Traversal and Visitor are related but separate concerns.

---

# Traversal Responsibility

In your printer:

```python
ae.left.accept(self)
ae.right.accept(self)
```

the Visitor controls traversal.

So:

```text
AdditionExpression
 ↓
Visitor
 ↓
Visit Left
 ↓
Visit Right
```

But it is possible to use:

```text
Iterator
+
Visitor
```

where Iterator handles traversal and Visitor handles operations.

---

# Visitor vs Iterator

This distinction is important.

## Iterator

Answers:

> **How do I move through the object structure?**

```text
Tree
 ↓
Iterator
 ↓
Node
Node
Node
```

---

## Visitor

Answers:

> **What operation do I perform on each kind of object?**

```text
Node
 ↓
Visitor
 ↓
Type-specific operation
```

Easy revision:

```text
Iterator
→ Traversal

Visitor
→ Operation
```

They can work together.

---

# Visitor vs Strategy

## Strategy

Encapsulates different ways of performing:

```text
one general algorithm
```

Example:

```text
HTML formatting
Markdown formatting
```

You select one strategy.

---

## Visitor

Defines operations across:

```text
multiple object types
```

Example:

```text
Print:
→ Double differently
→ Addition differently

Evaluate:
→ Double differently
→ Addition differently
```

Easy revision:

```text
Strategy
→ Choose one algorithm

Visitor
→ Apply one operation across many element types
```

---

# Visitor vs Template Method

## Template Method

Uses inheritance to define:

```text
Fixed algorithm skeleton
+
Customizable steps
```

## Visitor

Moves operations outside the element hierarchy.

```text
Elements
+
External operation object
```

They solve different problems.

---

# Visitor vs Interpreter

These can appear together.

Your expression example resembles an AST:

```text
Addition
Double
```

An Interpreter may use those classes to represent grammar expressions.

Then a Visitor may perform operations such as:

```text
Evaluate AST
Print AST
Optimize AST
Validate AST
```

So:

```text
Interpreter
→ Represents/evaluates a language
```

while:

```text
Visitor
→ Separates operations on that object structure
```

---

# Visitor vs Composite

Composite often creates tree structures:

```text
Folder
├── File
├── Folder
│   ├── File
│   └── File
```

Visitor can then perform operations over that tree:

```text
SizeVisitor
PermissionVisitor
SearchVisitor
ExportVisitor
```

These patterns frequently complement each other.

---

# Real-World Example — Compiler AST

Imagine an Abstract Syntax Tree:

```text
Expression
├── NumberNode
├── AddNode
├── MultiplyNode
├── FunctionNode
└── VariableNode
```

We may need:

```text
PrettyPrintVisitor
TypeCheckVisitor
OptimizationVisitor
CodeGenerationVisitor
```

The AST structure is relatively stable.

But many operations need to inspect it.

This is one of the strongest Visitor use cases.

---

# Real-World Example — Document Model

Suppose:

```text
DocumentElement
├── Paragraph
├── Image
├── Table
└── Heading
```

Visitors:

```text
HtmlExportVisitor
PdfExportVisitor
AccessibilityVisitor
WordCountVisitor
```

Each Visitor knows how to handle each element type.

---

# Real-World Example — File System

Elements:

```text
File
Directory
SymbolicLink
```

Visitors:

```text
SizeCalculator
PermissionChecker
BackupVisitor
VirusScanner
```

The same object structure can support multiple operations without putting every operation directly into each element.

---

# Intrusive vs Reflective vs Classic Visitor

## Intrusive

Operations live inside objects.

```text
Expression
├── print()
├── eval()
└── ...
```

Advantage:

```text
Simple
Natural polymorphism
```

Problem:

```text
Adding operation
→ Modify whole hierarchy
```

---

# Reflective

Operations live outside objects and inspect runtime types.

```python
if isinstance(...):
```

Advantage:

```text
Operations separated
Simple in dynamic languages
```

Problem:

```text
Missing type branch may fail silently
Large isinstance chains
```

---

# Classic Visitor

Elements expose:

```python
accept(visitor)
```

Visitors provide type-specific:

```python
visit(...)
```

Advantage:

```text
Strong separation of operations
Easy to add new Visitors
Explicit type handling
```

Problem:

```text
Adding a new element type
→ Update existing Visitors
```

---

# Comparison

| Approach | Operation Location | Adding New Operation | Adding New Element |
|---|---|---:|---:|
| Intrusive | Element classes | Expensive | Easy |
| Reflective | External operation class | Easier | Update operations |
| Classic Visitor | Visitor classes | Easy | Expensive |

This table captures the main trade-off.

---

# Python Note

Classic Visitor was designed largely around statically typed OO languages.

Python gives us other options such as:

```text
isinstance()
duck typing
decorators
single/multiple dispatch
```

So Python code does not always need the full traditional Visitor ceremony.

The important thing is understanding the architectural goal:

> **Keep operations separate from the object model when that separation makes extension easier.**

---

# Modern Python Alternative

Python's standard library also supports dispatch-based techniques such as:

```python
functools.singledispatchmethod
```

which can simplify type-based visitor implementations.

Conceptually:

```python
@visit.register
def _(self, expression: DoubleExpression):
    ...
```

and:

```python
@visit.register
def _(self, expression: AdditionExpression):
    ...
```

This achieves a similar goal without manually building a dispatch dictionary.

The design concept is still Visitor-like:

```text
One Visitor
+
Different behavior per element type
```

---

# When to Use Visitor

Use Visitor when:

- You have a stable hierarchy of element types
- Many different operations must work across those types
- You do not want to pollute domain classes with unrelated operations
- Operations frequently change or are added
- Double dispatch/type-specific behavior is useful

---

# When NOT to Use Visitor

Avoid Visitor when:

```text
Element types change frequently
```

because every new type may require modifying every Visitor.

Also avoid it when:

```text
Only one or two simple operations exist
```

and normal polymorphism is clearer.

Visitor can introduce significant complexity.

---

# Benefits

Visitor provides:

- Separation between data structures and operations
- Easy addition of new operations
- Centralized logic for one operation
- Better SRP for element classes
- Useful double-dispatch behavior
- Good fit for ASTs and stable object hierarchies

---

# Drawbacks

Visitor can introduce:

- More classes
- More indirection
- Double-dispatch complexity
- Coupling between Visitors and all concrete element types
- Cost when adding new element types
- More ceremony in languages such as Python

---

# Visitor and SRP

Without Visitor:

```text
Expression
├── Expression data
├── Printing
├── Evaluation
├── Serialization
└── Validation
```

With Visitor:

```text
Expression
→ Expression structure

PrinterVisitor
→ Printing

EvaluatorVisitor
→ Evaluation

SerializerVisitor
→ Serialization
```

Each operation has a clearer home.

---

# Visitor and OCP

Visitor gives us an important OCP trade-off.

If we add:

```text
New Operation
```

we usually create:

```text
New Visitor
```

without changing element classes.

Good.

But if we add:

```text
New Element Type
```

existing Visitors may need updates.

So memorize:

```text
Visitor favors extending operations
over extending element types.
```

---

# Interview Question

## What is the Visitor Pattern?

Visitor is a behavioral design pattern that separates operations from the object structure on which those operations operate.

Instead of adding methods such as:

```text
print()
evaluate()
serialize()
validate()
```

to every element class, we create separate Visitors such as:

```text
PrinterVisitor
EvaluatorVisitor
SerializerVisitor
```

Each Visitor knows how to process every relevant concrete element type.

The classic implementation uses `accept(visitor)` and `visitor.visit(element)`, often providing double dispatch.

Visitor is particularly useful when the element hierarchy is stable but new operations are frequently added.

---

# What Is Double Dispatch?

Double dispatch means the operation selected depends on:

```text
Visitor runtime type
+
Element runtime type
```

For example:

```text
PrinterVisitor
+
AdditionExpression
```

produces printing behavior.

While:

```text
EvaluatorVisitor
+
AdditionExpression
```

produces evaluation behavior.

That combination determines which operation executes.

---

# How to Recognize Visitor

Look for:

> "I have a stable object hierarchy, but I keep adding new operations that must behave differently for each object type."

Example:

```text
Object Types
→ Number
→ Addition
→ Multiplication

Operations
→ Print
→ Evaluate
→ Validate
→ Serialize
```

Then Visitor can reorganize the system around:

```text
One class per operation
```

rather than:

```text
Every operation duplicated across every element class
```

---

# Mental Model

Imagine a museum containing:

```text
Painting
Sculpture
HistoricalArtifact
```

Different visitors enter:

```text
InsuranceVisitor
CleaningVisitor
ValuationVisitor
```

Each Visitor performs a different operation depending on what it visits.

For example:

```text
ValuationVisitor
→ values Painting one way
→ values Sculpture another way
```

The museum items do not need:

```text
calculate_insurance()
clean_for_every_possible_team()
calculate_every_possible_report()
```

inside themselves.

That is the Visitor mindset.

---

# Quick Revision

```text
Visitor
→ Behavioral Design Pattern
```

```text
Goal
→ Separate operations from object structure
```

```text
Elements
→ Hold structure/data
```

```text
Visitors
→ Hold operations
```

```text
Classic Visitor

Element
 ↓
accept(visitor)
 ↓
visitor.visit(element)
```

```text
Double Dispatch
→ Visitor type + Element type
```

```text
Intrusive Visitor

Operations live inside elements
```

```text
Reflective Visitor

External operation
+
isinstance()
```

```text
Classic Visitor

accept()
+
visit()
```

```text
Visitor Strength

New operations
→ Easy
```

```text
Visitor Weakness

New element types
→ Existing Visitors may change
```

```text
Iterator
→ How to traverse
```

```text
Visitor
→ What to do with each type
```

```text
Best Fit

Stable element hierarchy
+
Frequently changing operations
```

---

# Key Takeaways

- **Visitor is a behavioral design pattern.**
- **Its primary goal is separating operations from the object hierarchy they operate on.**
- **Traversal can be performed by a Visitor, but traversal itself is not the defining purpose of Visitor.**
- **The intrusive approach puts operations such as `print()` and `eval()` directly into expression classes.**
- **This becomes inconvenient when many new operations are added.**
- **The reflective approach moves operations outside the hierarchy but relies on runtime type checks such as `isinstance()`.**
- **The classic Visitor uses `accept(visitor)` and `visitor.visit(element)`.**
- **Classic Visitor commonly relies on double dispatch.**
- **Visitor makes adding new operations easier when element types are stable.**
- **Adding a new element type may require updating all existing Visitors.**
- **Visitor therefore optimizes extensibility along the operation dimension, not every possible dimension.**
- **Iterator answers how to traverse; Visitor answers what operation to perform on different element types.**
- **ASTs, compilers, document models, and stable object trees are common Visitor use cases.**
- **In Python, reflection or dispatch utilities can sometimes provide a simpler implementation than the traditional Visitor ceremony.**

# One-Line Revision

> **Visitor = keep your object hierarchy focused on representing data, and move operations over those different object types into separate Visitor objects—especially when new operations are added more often than new element types.**