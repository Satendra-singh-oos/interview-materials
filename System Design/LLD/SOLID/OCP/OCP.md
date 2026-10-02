# Open/Closed Principle — OCP

OCP is the second principle of **SOLID**.

> **Software entities should be open for extension but closed for modification.**

Meaning:

- **Open for extension** → we should be able to add new behavior.
- **Closed for modification** → ideally, existing stable code should not need to change every time a new requirement is introduced.

---

# Why Do We Need OCP?

Suppose we have products with:

- Color
- Size

```python
from enum import Enum


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


class Size(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3


class Product:
    def __init__(self, name, color, size):
        self.name = name
        self.color = color
        self.size = size
```

Now we want to filter products.

---

# Bad Design

```python
class ProductFilter:

    def filter_by_color(self, products, color):
        for product in products:
            if product.color == color:
                yield product

    def filter_by_size(self, products, size):
        for product in products:
            if product.size == size:
                yield product

    def filter_by_size_and_color(self, products, size, color):
        for product in products:
            if product.size == size and product.color == color:
                yield product
```

This initially looks fine.

But now imagine adding:

```text
Weight
Brand
Price
Category
Rating
```

We may start creating:

```text
filter_by_weight()

filter_by_brand()

filter_by_color_and_size()

filter_by_color_and_weight()

filter_by_size_and_weight()

filter_by_color_and_size_and_weight()

...
```

The number of combinations keeps growing.

---

# Why Does This Violate OCP?

Every time a new filtering requirement appears:

```text
New Requirement
      ↓
Modify ProductFilter
      ↓
Add Another Method
```

For example:

```text
Need filter by weight
→ Modify ProductFilter

Need brand filter
→ Modify ProductFilter

Need brand + size
→ Modify ProductFilter
```

The filtering class constantly changes.

This means it is:

```text
Open for modification ❌
```

instead of being extended using new independent behavior.

---

# Better Design — Specification Pattern

We can separate:

```text
What condition should an item satisfy?
```

from:

```text
How do we filter items?
```

This gives us:

- `Specification`
- `Filter`

---

# Specification

A specification represents one filtering rule.

```python
class Specification:
    def is_satisfied(self, item):
        raise NotImplementedError

    def __and__(self, other):
        return AndSpecification(self, other)
```

Each specification answers:

> **Does this item satisfy my condition?**

---

# Filter

The filter only knows how to apply a specification.

```python
class Filter:
    def filter(self, items, spec):
        raise NotImplementedError
```

Notice that the filter does not care whether the condition is:

```text
Color
Size
Weight
Price
Brand
```

It only depends on a specification.

---

# Color Specification

```python
class ColorSpecification(Specification):
    def __init__(self, color):
        self.color = color

    def is_satisfied(self, item):
        return item.color == self.color
```

Responsibility:

```text
Check product color
```

---

# Size Specification

```python
class SizeSpecification(Specification):
    def __init__(self, size):
        self.size = size

    def is_satisfied(self, item):
        return item.size == self.size
```

Responsibility:

```text
Check product size
```

---

# Better Filter

```python
class BetterFilter(Filter):
    def filter(self, items, spec):
        for item in items:
            if spec.is_satisfied(item):
                yield item
```

Notice something important:

`BetterFilter` does not need to know about:

- Color
- Size
- Weight
- Brand
- Price

It simply asks:

```python
spec.is_satisfied(item)
```

---

# Filtering Green Products

```python
green = ColorSpecification(Color.GREEN)

for product in better_filter.filter(products, green):
    print(product.name)
```

Flow:

```text
Product
   ↓
ColorSpecification
   ↓
is_satisfied()
   ↓
True / False
```

---

# Filtering Large Products

```python
large = SizeSpecification(Size.LARGE)

for product in better_filter.filter(products, large):
    print(product.name)
```

No modification to `BetterFilter` was required.

We simply added or used another specification.

This is the key OCP idea.

---

# Combining Specifications

Suppose we want:

> Large AND Blue

We should not create:

```python
filter_by_large_and_blue()
```

Instead, compose specifications.

---

# AndSpecification

```python
class AndSpecification(Specification):
    def __init__(self, *args):
        self.args = args

    def is_satisfied(self, item):
        return all(
            spec.is_satisfied(item)
            for spec in self.args
        )
```

Now:

```python
large_blue = AndSpecification(
    SizeSpecification(Size.LARGE),
    ColorSpecification(Color.BLUE)
)
```

or because `Specification` implements `__and__`:

```python
large_blue = (
    SizeSpecification(Size.LARGE)
    & ColorSpecification(Color.BLUE)
)
```

Then:

```python
for product in better_filter.filter(products, large_blue):
    print(product.name)
```

---

# Why Does `&` Work?

We implemented:

```python
def __and__(self, other):
    return AndSpecification(self, other)
```

Therefore:

```python
large & blue
```

becomes conceptually:

```python
AndSpecification(large, blue)
```

This is Python operator overloading.

---

# Complete Design

```text
                  Specification
                       ↑
            ----------------------
            |                    |
   ColorSpecification     SizeSpecification
            \                    /
             \                  /
              AndSpecification


Products
   ↓
BetterFilter
   ↓
Specification
   ↓
is_satisfied()
```

---

# Adding a New Requirement

Suppose tomorrow we add:

```python
class WeightSpecification(Specification):
    def __init__(self, weight):
        self.weight = weight

    def is_satisfied(self, item):
        return item.weight == self.weight
```

What changes in `BetterFilter`?

```text
Nothing ✅
```

We extended the system by adding:

```text
WeightSpecification
```

instead of modifying existing filtering logic.

That is:

> **Open for extension, closed for modification.**

---

# Another Example — Price

Suppose the requirement becomes:

> Filter products cheaper than ₹10,000.

We can add:

```python
class MaxPriceSpecification(Specification):
    def __init__(self, max_price):
        self.max_price = max_price

    def is_satisfied(self, item):
        return item.price <= self.max_price
```

Again:

```text
BetterFilter unchanged ✅
```

---

# OCP Before and After

## Without OCP

```text
New Filter Requirement
        ↓
Modify ProductFilter
        ↓
Add More if/else or methods
        ↓
Class keeps growing
```

---

## With OCP

```text
New Filter Requirement
        ↓
Create New Specification
        ↓
Existing Filter Unchanged
```

---

# Why Is This Better?

Benefits:

- Less modification of tested code
- Lower regression risk
- Easier extension
- Better separation of concerns
- Easier testing
- Smaller classes
- Better composition

---

# Specification Pattern

The design in this example is commonly called the:

> **Specification Pattern**

A specification encapsulates a business rule.

Examples:

```text
ColorSpecification
→ Product must have particular color

SizeSpecification
→ Product must have particular size

PriceSpecification
→ Product must satisfy price rule
```

Specifications can then be composed:

```text
AND
OR
NOT
```

For example:

```text
Large AND Blue
```

or conceptually:

```text
Large OR Medium
```

---

# Important OCP Clarification

OCP does **not** mean:

> Never modify an existing class.

You can still modify code for:

- Bug fixes
- Refactoring
- Changed core requirements

The principle mainly says:

> **When predictable variations or new behaviors are added, prefer extension points instead of repeatedly editing large existing conditional logic.**

---

# Real-World Example

Imagine a payment system.

Bad:

```python
if payment_type == "card":
    ...
elif payment_type == "paypal":
    ...
elif payment_type == "upi":
    ...
elif payment_type == "wallet":
    ...
```

Every new payment type requires modifying the same code.

Better:

```text
PaymentProcessor
      ↑
--------------------------
|          |             |
Card      UPI         PayPal
Processor Processor    Processor
```

Adding:

```text
CryptoPaymentProcessor
```

should ideally not require rewriting existing processors.

This follows OCP.

---

# How to Identify an OCP Violation?

Look for code that constantly grows like:

```python
if type == "A":
    ...
elif type == "B":
    ...
elif type == "C":
    ...
```

or:

```text
filter_by_color()
filter_by_size()
filter_by_price()
filter_by_color_and_size()
filter_by_color_and_size_and_price()
```

Ask:

> **When I add a new behavior, do I have to keep changing this same class?**

If yes, there may be an OCP problem.

---

# Interview Question

## What is the Open/Closed Principle?

Open/Closed Principle states:

> **Software entities should be open for extension but closed for modification.**

This means new behavior should ideally be added through extension rather than repeatedly modifying existing stable code.

For example, instead of adding a new filtering method every time we introduce a product property, we can create separate specification classes implementing a common interface.

The filter remains unchanged while new specifications such as color, size, weight, or price can be added independently.

---

# SRP vs OCP

## SRP

```text
Why should this class change?
```

Goal:

> One responsibility / one reason to change.

---

## OCP

```text
What happens when a new behavior is added?
```

Goal:

> Extend behavior without repeatedly modifying stable code.

---

# Quick Revision

```text
OCP
→ Open/Closed Principle
```

```text
Open
→ Open for extension
```

```text
Closed
→ Closed for unnecessary modification
```

```text
Bad Design
→ Every new requirement changes existing class
```

```text
Better Design
→ Add new implementation/specification
→ Existing logic stays unchanged
```

```text
Specification Pattern
→ Encapsulate individual business/filter rules
```

```text
AndSpecification
→ Compose multiple specifications
```

---

# Key Takeaways

- **OCP means open for extension and closed for modification.**
- **A new requirement should not force repeated changes to stable code when a clean extension point can be provided.**
- **A large collection of `if/elif` statements or combination-specific methods can indicate an OCP problem.**
- **The Specification Pattern is one way to apply OCP to filtering rules.**
- **Each filtering condition becomes an independent specification.**
- **Specifications can be composed instead of creating methods for every possible combination.**
- **`BetterFilter` does not change when color, size, weight, or price specifications are introduced.**
- **OCP reduces regression risk and makes systems easier to extend.**
- **OCP does not mean existing code can literally never be modified.**

# One-Line Revision

> **OCP = add new behavior by extending the system rather than repeatedly changing existing stable logic.**