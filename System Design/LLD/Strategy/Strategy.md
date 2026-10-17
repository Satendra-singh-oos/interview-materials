# Strategy Design Pattern

Strategy is a **behavioral design pattern**.

> **Strategy defines a family of interchangeable algorithms/behaviors and allows the client or Context to choose which one should be used.**

Simple idea:

```text
Context
   ↓
Strategy Interface
   ↓
-------------------------
|                       |
Strategy A          Strategy B
```

The Context does not need to know the implementation details of each algorithm.

It simply delegates the work to the selected Strategy.

---

# Why Do We Need Strategy?

Suppose a text processor needs to generate lists in different formats:

```text
Markdown
HTML
```

Without Strategy, we might write:

```python
if output_format == "markdown":
    ...
elif output_format == "html":
    ...
```

As more formats appear:

```text
Markdown
HTML
XML
JSON
AsciiDoc
```

the class starts accumulating:

```text
if
elif
elif
elif
```

and all formatting logic ends up inside one class.

Strategy solves this by separating:

```text
What the Context wants to do
```

from:

```text
How the operation is performed
```

---

# Core Mental Model

Without Strategy:

```text
TextProcessor
├── Markdown formatting logic
├── HTML formatting logic
├── XML formatting logic
└── JSON formatting logic
```

With Strategy:

```text
TextProcessor
     ↓
 ListStrategy
     ↓
---------------------
|                   |
Markdown          HTML
Strategy          Strategy
```

`TextProcessor` only knows:

> "I need to render a list."

The Strategy decides:

> "How should that list be rendered?"

---

# Main Participants

Strategy normally has three main participants:

```text
Context
Strategy
Concrete Strategies
```

---

# Context

The Context uses an algorithm but does not implement every variation itself.

In your example:

```text
TextProcessor
```

is the Context.

---

# Strategy Interface

The common contract is:

```python
class ListStrategy:
    def start(self, buffer):
        pass

    def end(self, buffer):
        pass

    def add_list_item(
        self,
        buffer,
        item
    ):
        pass
```

Every list-formatting strategy understands:

```text
start()
add_list_item()
end()
```

but each strategy can implement them differently.

---

# Concrete Strategies

Your example has:

```text
MarkdownListStrategy
HtmlListStrategy
```

Both solve:

```text
Render a list
```

but use different algorithms/formats.

---

# Markdown Strategy

```python
class MarkdownListStrategy(
    ListStrategy
):
    def add_list_item(
        self,
        buffer,
        item
    ):
        buffer.append(
            f" * {item}\n"
        )
```

For:

```python
items = [
    "foo",
    "bar",
    "baz"
]
```

it produces:

```text
 * foo
 * bar
 * baz
```

Markdown lists do not require special opening or closing tags.

Therefore:

```text
start()
end()
```

can simply do nothing.

---

# HTML Strategy

```python
class HtmlListStrategy(
    ListStrategy
):
    def start(self, buffer):
        buffer.append("<ul>\n")

    def end(self, buffer):
        buffer.append("</ul>\n")

    def add_list_item(
        self,
        buffer,
        item
    ):
        buffer.append(
            f"  <li>{item}</li>\n"
        )
```

For the same items:

```text
foo
bar
baz
```

the result becomes:

```html
<ul>
  <li>foo</li>
  <li>bar</li>
  <li>baz</li>
</ul>
```

Same goal:

```text
Render a list
```

Different algorithm:

```text
Markdown formatting
vs
HTML formatting
```

That is Strategy.

---

# TextProcessor — The Context

```python
class TextProcessor:
    def __init__(
        self,
        list_strategy=None
    ):
        self.buffer = []

        self.list_strategy = (
            list_strategy
            if list_strategy is not None
            else HtmlListStrategy()
        )
```

The important field is:

```python
self.list_strategy
```

`TextProcessor` does not care whether this currently contains:

```text
MarkdownListStrategy
```

or:

```text
HtmlListStrategy
```

as long as it follows the expected Strategy interface.

---

# Delegating Work to the Strategy

```python
def append_list(self, items):
    self.list_strategy.start(
        self.buffer
    )

    for item in items:
        self.list_strategy.add_list_item(
            self.buffer,
            item
        )

    self.list_strategy.end(
        self.buffer
    )
```

Notice that `TextProcessor` does not contain HTML-specific code such as:

```python
"<ul>"
"<li>"
```

and does not contain Markdown-specific code such as:

```python
"* item"
```

Instead:

```text
TextProcessor
     ↓
Selected Strategy
     ↓
Formatting behavior
```

---

# Runtime Strategy Selection

Your example allows changing the strategy while the program is running.

```python
def set_output_format(self, format):
    if format == OutputFormat.MARKDOWN:
        self.list_strategy = (
            MarkdownListStrategy()
        )

    elif format == OutputFormat.HTML:
        self.list_strategy = (
            HtmlListStrategy()
        )
```

This means:

```text
Same TextProcessor
        ↓
Strategy can change
        ↓
Different behavior
```

---

# Example

Start:

```python
tp = TextProcessor()
```

Then:

```python
tp.set_output_format(
    OutputFormat.MARKDOWN
)

tp.append_list(items)
```

Selected behavior:

```text
MarkdownListStrategy
```

Output:

```text
 * foo
 * bar
 * baz
```

---

# Switch Strategy

Then:

```python
tp.set_output_format(
    OutputFormat.HTML
)

tp.clear()
tp.append_list(items)
```

Now the same `TextProcessor` uses:

```text
HtmlListStrategy
```

Output:

```html
<ul>
  <li>foo</li>
  <li>bar</li>
  <li>baz</li>
</ul>
```

The Context did not change.

Only the Strategy changed.

---

# Strategy Flow

```text
Client
  ↓
TextProcessor
  ↓
Which Strategy?
  ↓
--------------------
|                  |
Markdown          HTML
Strategy          Strategy
```

---

# Better Dependency Injection Version

The enum-based setter works, but Strategy becomes even clearer if the Strategy object itself is supplied.

Example:

```python
processor = TextProcessor(
    MarkdownListStrategy()
)
```

or:

```python
processor = TextProcessor(
    HtmlListStrategy()
)
```

Then the Context does not even need:

```text
OutputFormat
```

or:

```text
if format == ...
```

A setter could simply be:

```python
def set_strategy(
    self,
    strategy
):
    self.list_strategy = strategy
```

Usage:

```python
tp.set_strategy(
    MarkdownListStrategy()
)

tp.set_strategy(
    HtmlListStrategy()
)
```

This is closer to the pure Strategy idea.

---

# Why Is This Better?

With:

```python
if format == OutputFormat.MARKDOWN:
...
elif format == OutputFormat.HTML:
...
```

`TextProcessor` still knows which concrete strategies exist.

If we later add:

```text
AsciiDocListStrategy
```

we may need to modify `TextProcessor`.

With direct Strategy injection:

```python
tp.set_strategy(
    AsciiDocListStrategy()
)
```

`TextProcessor` does not need modification.

This gives stronger:

```text
Open/Closed Principle
Dependency Inversion
```

---

# Complete Cleaner Version

```python
from abc import ABC, abstractmethod


class ListStrategy(ABC):

    def start(self, buffer):
        pass

    def end(self, buffer):
        pass

    @abstractmethod
    def add_list_item(
        self,
        buffer,
        item
    ):
        pass


class MarkdownListStrategy(
    ListStrategy
):
    def add_list_item(
        self,
        buffer,
        item
    ):
        buffer.append(
            f" * {item}\n"
        )


class HtmlListStrategy(
    ListStrategy
):
    def start(self, buffer):
        buffer.append("<ul>\n")

    def end(self, buffer):
        buffer.append("</ul>\n")

    def add_list_item(
        self,
        buffer,
        item
    ):
        buffer.append(
            f"  <li>{item}</li>\n"
        )


class TextProcessor:
    def __init__(
        self,
        strategy=None
    ):
        self.buffer = []

        self.strategy = (
            strategy
            if strategy is not None
            else HtmlListStrategy()
        )

    def set_strategy(
        self,
        strategy
    ):
        self.strategy = strategy

    def append_list(
        self,
        items
    ):
        self.strategy.start(
            self.buffer
        )

        for item in items:
            self.strategy.add_list_item(
                self.buffer,
                item
            )

        self.strategy.end(
            self.buffer
        )

    def clear(self):
        self.buffer.clear()

    def __str__(self):
        return "".join(
            self.buffer
        )
```

Usage:

```python
items = [
    "foo",
    "bar",
    "baz"
]

tp = TextProcessor(
    MarkdownListStrategy()
)

tp.append_list(items)

print(tp)

tp.clear()

tp.set_strategy(
    HtmlListStrategy()
)

tp.append_list(items)

print(tp)
```

---

# Dynamic vs Static Strategy Selection

Your note mentions:

```text
Runtime / dynamic
Compile-time / static
```

The important idea is:

> The algorithm can be selected without rewriting the Context.

---

## Dynamic Strategy

Selected while the application is running.

Example:

```python
tp.set_strategy(
    MarkdownListStrategy()
)
```

Later:

```python
tp.set_strategy(
    HtmlListStrategy()
)
```

This is the normal Strategy implementation in Python.

---

## Static Selection

In statically typed languages, a strategy can sometimes be fixed through:

```text
Generics
Templates
Compile-time configuration
```

so the algorithm choice is known earlier.

For your Python notes, the most important form is:

```text
Runtime Strategy Selection
```

---

# Real-World Example — Payment Processing

Suppose checkout supports:

```text
Credit Card
UPI
PayPal
```

Without Strategy:

```python
if payment_type == "card":
    ...
elif payment_type == "upi":
    ...
elif payment_type == "paypal":
    ...
```

With Strategy:

```text
CheckoutService
       ↓
PaymentStrategy
       ↓
-------------------------
|          |            |
Card      UPI         PayPal
```

Usage:

```python
checkout.pay(
    amount
)
```

The selected strategy decides how payment is performed.

---

# Real-World Example — Compression

```text
CompressionService
       ↓
CompressionStrategy
       ↓
-----------------------
|          |          |
ZIP       GZIP       BZIP2
```

Same operation:

```python
compress(data)
```

Different algorithms.

---

# Real-World Example — Sorting

Suppose a system can choose:

```text
Sort by price
Sort by rating
Sort by date
```

Instead of putting all sorting logic into one component:

```text
ProductService
       ↓
SortStrategy
       ↓
-----------------------
|          |          |
Price     Rating      Date
```

---

# Real-World Backend Example — Retry Strategy

A backend client could support:

```text
No Retry
Fixed Retry
Exponential Backoff
```

Structure:

```text
API Client
    ↓
RetryStrategy
    ↓
-----------------------------
|             |             |
NoRetry     Fixed       Exponential
```

The networking code stays the same.

Only retry behavior changes.

---

# Strategy and OCP

Suppose we add:

```text
JsonListStrategy
```

With a well-designed Strategy setup:

```text
TextProcessor
```

does not need to change.

We simply create another implementation.

```text
Existing Context
     ↓
New Strategy
```

This supports:

> **Open for extension, closed for modification.**

---

# Strategy and SRP

Without Strategy:

```text
TextProcessor
├── Text management
├── Markdown formatting
├── HTML formatting
├── XML formatting
└── JSON formatting
```

With Strategy:

```text
TextProcessor
→ Coordinates text processing

MarkdownListStrategy
→ Markdown formatting

HtmlListStrategy
→ HTML formatting
```

Each behavior has a clearer responsibility.

---

# Strategy and DIP

Instead of depending directly on:

```text
HtmlListStrategy
MarkdownListStrategy
```

the Context conceptually depends on:

```text
ListStrategy
```

Therefore:

```text
TextProcessor
       ↓
ListStrategy
       ↑
--------------------
|                  |
Markdown          HTML
```

This reduces coupling to concrete implementations.

---

# Strategy vs State

These patterns can look almost identical structurally.

Both often have:

```text
Context
   ↓
Behavior Object
```

But their **intent is different**.

---

## Strategy

Question:

> **Which algorithm should I use?**

Example:

```text
Markdown
or
HTML
```

The Strategy is generally selected because the caller wants a particular behavior.

---

## State

Question:

> **How should I behave because of my current state?**

Example:

```text
Order is PAID
Order is SHIPPED
```

The behavior changes because the object's lifecycle state changed.

---

# Easy Revision

```text
Strategy
→ Client/configuration chooses behavior
```

```text
State
→ Current state determines behavior
```

Another useful distinction:

```text
Strategy
→ Usually strategies don't transition each other
```

```text
State
→ State transitions are central to the pattern
```

---

# Strategy vs Command

## Strategy

Encapsulates:

```text
How to perform an algorithm
```

Example:

```text
HtmlFormattingStrategy
```

---

## Command

Encapsulates:

```text
A request/action to perform
```

Example:

```text
GenerateReportCommand
```

Easy revision:

```text
Strategy
→ HOW
```

```text
Command
→ WHAT action
```

---

# Strategy vs Template Method

These are also closely related.

## Strategy

Uses:

```text
Composition
```

Different algorithm is provided as another object.

```text
Context
 ↓
Strategy
```

---

## Template Method

Uses:

```text
Inheritance
```

A base class defines an algorithm skeleton and subclasses override specific steps.

Conceptually:

```text
Template Method
→ Inheritance-based variation

Strategy
→ Composition-based variation
```

---

# Why Composition Is Useful Here

Instead of:

```text
MarkdownTextProcessor
HtmlTextProcessor
XmlTextProcessor
```

we can have:

```text
TextProcessor
   +
Chosen Strategy
```

So behavior can change without creating a different Context object.

---

# Strategy Is More Than `if/else` Removal

Do not think:

> Strategy exists only to remove an `if` statement.

A small:

```python
if condition:
```

is perfectly fine.

Strategy becomes useful when:

```text
Algorithms are substantial
+
They vary independently
+
They may be added/changed
+
You want them testable separately
```

---

# When to Use Strategy

Use Strategy when:

- Several algorithms solve the same type of problem
- You need to switch behavior at runtime
- Algorithms should be independently testable
- Large conditionals select between behaviors
- You want algorithms separated from the Context
- New algorithms are likely to be added

---

# When Not to Use Strategy

Avoid Strategy when:

```text
There are only two trivial branches
```

and they are unlikely to change.

For example:

```python
if uppercase:
    text = text.upper()
```

does not necessarily require:

```text
UppercaseStrategy
NormalCaseStrategy
```

Do not add unnecessary abstraction.

---

# Benefits

Strategy provides:

- Interchangeable algorithms
- Runtime behavior selection
- Separation of concerns
- Easier testing
- Reduced conditional complexity
- Better extensibility
- Composition instead of inheritance

---

# Drawbacks

Strategy may introduce:

- More classes
- More objects
- More indirection
- Configuration complexity
- Overengineering for simple logic

Clients may also need to understand:

```text
Which Strategy should I choose?
```

---

# Interview Question

## What is the Strategy Pattern?

Strategy is a behavioral design pattern that defines a family of interchangeable algorithms, encapsulates each algorithm separately, and allows a Context to delegate behavior to the selected Strategy.

For example, a `TextProcessor` can use either:

```text
MarkdownListStrategy
```

or:

```text
HtmlListStrategy
```

to render the same list.

The `TextProcessor` remains unchanged while the formatting algorithm can be swapped dynamically.

---

# How to Recognize Strategy

Look for:

> "I have several different ways to perform the same operation, and I want to choose between them without changing the main class."

Then:

```text
Context
 ↓
Strategy
 ↓
Different Algorithms
```

is a strong candidate.

---

# Mental Model

Think about navigation software.

You want:

```text
Route from A to B
```

but there are multiple strategies:

```text
Driving
Walking
Cycling
Public Transport
```

Same goal:

```text
Find route
```

Different algorithm:

```text
Routing Strategy
```

The navigation application does not need to rewrite itself for every routing method.

That is Strategy.

---

# Quick Revision

```text
Strategy
→ Behavioral Design Pattern
```

```text
Goal
→ Make algorithms interchangeable
```

```text
Context
→ Uses Strategy
```

```text
Strategy Interface
→ Common contract
```

```text
Concrete Strategies
→ Different implementations
```

```text
Our Example

TextProcessor
     ↓
ListStrategy
     ↓
-------------------
|                 |
Markdown         HTML
```

```text
Runtime Change

Markdown
   ↓
set_strategy()
   ↓
HTML
```

```text
Strategy
→ Which algorithm?
```

```text
State
→ Which lifecycle state?
```

```text
Command
→ Which action/request?
```

```text
Template Method
→ Variation through inheritance
```

```text
Strategy
→ Variation through composition
```

---

# Key Takeaways

- **Strategy is a behavioral design pattern.**
- **It encapsulates interchangeable algorithms behind a common interface.**
- **The Context delegates behavior to the selected Strategy.**
- **In your example, `TextProcessor` is the Context.**
- **`ListStrategy` defines the common formatting contract.**
- **`MarkdownListStrategy` and `HtmlListStrategy` are concrete Strategies.**
- **The same `TextProcessor` can switch formatting behavior at runtime.**
- **Passing Strategy objects directly is usually cleaner than making the Context know every concrete Strategy through `if/elif`.**
- **Strategy supports OCP, SRP, and dependency inversion when used appropriately.**
- **Strategy and State can look structurally similar, but Strategy represents interchangeable algorithms while State represents lifecycle-dependent behavior.**
- **Strategy uses composition to vary behavior rather than creating many subclasses of the Context.**
- **Do not introduce Strategy when a tiny conditional is already clear enough.**

# One-Line Revision

> **Strategy = extract different ways of performing the same job into interchangeable objects, then let the Context use whichever algorithm is appropriate.**