# Liskov Substitution Principle — LSP

LSP is the third principle of **SOLID**.

> **Objects of a base class should be replaceable with objects of a derived class without breaking the expected behavior of the program.**

Simple meaning:

> If `B` is a subtype of `A`, then wherever the program expects `A`, we should be able to use `B` without producing unexpected behavior.

---

# Core Idea

Suppose:

```text
Square IS-A Rectangle
```

From a mathematical perspective this seems correct.

But in software design, inheritance also means:

> `Square` must behave according to the contract expected from `Rectangle`.

If replacing:

```text
Rectangle
```

with:

```text
Square
```

changes the expected behavior, then the inheritance relationship violates LSP.

---

# Rectangle Example

```python
class Rectangle:
    def __init__(self, width, height):
        self._height = height
        self._width = width

    @property
    def area(self):
        return self._width * self._height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    def __str__(self):
        return f"Width: {self.width}, height: {self.height}"
```

A normal `Rectangle` allows width and height to change independently.

Example:

```python
rectangle = Rectangle(2, 3)

rectangle.width = 5
rectangle.height = 10
```

Now:

```text
width = 5
height = 10
area = 50
```

This is expected Rectangle behavior.

---

# Square Inheriting Rectangle

```python
class Square(Rectangle):
    def __init__(self, size):
        super().__init__(size, size)

    @Rectangle.width.setter
    def width(self, value):
        self._width = value
        self._height = value

    @Rectangle.height.setter
    def height(self, value):
        self._width = value
        self._height = value
```

A square must maintain:

```text
width == height
```

Therefore if we change:

```python
square.width = 10
```

we must also change:

```text
square.height = 10
```

This maintains the Square invariant.

But this creates a problem with the Rectangle contract.

---

# The Problem

Consider:

```python
def use_it(rc):
    width = rc.width

    rc.height = 10

    expected = width * 10

    print(
        f"Expected an area of {expected}, "
        f"got {rc.area}"
    )
```

The function assumes:

> Changing the height of a Rectangle does not change its width.

That is a reasonable expectation based on `Rectangle`.

---

# Using Rectangle

```python
rc = Rectangle(2, 3)
use_it(rc)
```

Flow:

```text
Initial:
width = 2
height = 3

Set:
height = 10

Result:
width = 2
height = 10

Area = 20
```

Expected:

```text
20
```

Actual:

```text
20
```

Everything works.

---

# Using Square

Now:

```python
sq = Square(5)
use_it(sq)
```

Initial state:

```text
width = 5
height = 5
```

The function stores:

```python
width = rc.width
```

So:

```text
width = 5
```

Then:

```python
rc.height = 10
```

But because it is a `Square`, its setter does this:

```text
height = 10
width = 10
```

Now:

```text
width = 10
height = 10
area = 100
```

But `use_it()` expected:

```text
original width × new height

5 × 10 = 50
```

Result:

```text
Expected area = 50
Actual area   = 100
```

Unexpected behavior.

---

# Why Does This Violate LSP?

`use_it()` works correctly with:

```text
Rectangle
```

but behaves incorrectly when we substitute:

```text
Square
```

even though Square inherits from Rectangle.

Therefore:

> `Square` is not behaviorally substitutable for `Rectangle`.

That violates:

> **Liskov Substitution Principle**

---

# The Real Problem

The problem is not inheritance syntax.

The problem is the **behavioral contract**.

`Rectangle` promises:

```text
Width can change independently.

Height can change independently.
```

But `Square` requires:

```text
Width and height must always remain equal.
```

These contracts conflict.

---

# LSP and Behavioral Contracts

A child class should preserve the expectations established by the parent.

Conceptually:

```text
Parent Contract
      ↓
Child must respect it
```

A child should not introduce surprising side effects.

Bad:

```text
rectangle.height = 10

Expected:
Only height changes

Square behavior:
Height AND width change
```

That is the unexpected side effect.

---

# Important Rule

Inheritance should not be based only on:

> "Is this conceptually an IS-A relationship?"

You must also ask:

> "Can the child behave everywhere the parent is expected?"

That second question is what matters for LSP.

---

# Better Design

Instead of forcing:

```text
Square extends Rectangle
```

we can model both under a more general abstraction.

Example:

```python
from abc import ABC, abstractmethod


class Shape(ABC):

    @property
    @abstractmethod
    def area(self):
        pass
```

Then:

```python
class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    @property
    def area(self):
        return self.width * self.height
```

And:

```python
class Square(Shape):
    def __init__(self, size):
        self.size = size

    @property
    def area(self):
        return self.size * self.size
```

Now:

```text
          Shape
         /     \
Rectangle       Square
```

Both satisfy the `Shape` contract:

```text
Every shape has an area.
```

But we do not incorrectly claim:

```text
Square behaves exactly like Rectangle.
```

---

# Why Is This Better?

Now a function can depend on:

```python
def print_area(shape):
    print(shape.area)
```

and both work correctly:

```python
print_area(Rectangle(2, 10))
print_area(Square(5))
```

The shared abstraction only exposes behavior that both classes can honor.

---

# LSP Is About Behavior, Not Just Types

This is important.

Code may compile or run correctly from a type perspective:

```python
Square(Rectangle)
```

but still violate LSP because behavior changes unexpectedly.

So LSP means:

> **Subtype compatibility must be behavioral, not merely syntactic.**

---

# Preconditions and Postconditions

A deeper way to understand LSP is through contracts.

A subtype should generally not:

- Require stronger preconditions
- Provide weaker guarantees
- Break invariants of the base type
- Introduce unexpected side effects

---

# Stronger Preconditions

Suppose the parent accepts:

```text
Any positive number
```

but child accepts only:

```text
Numbers > 100
```

Then the child is more restrictive.

Code that worked with the parent may fail with the child.

This can violate LSP.

---

# Weaker Postconditions

Suppose parent promises:

```text
save()
→ Data definitely persisted
```

but child implementation only:

```text
save()
→ Maybe persisted
```

The child provides a weaker guarantee.

That can violate LSP.

---

# Breaking Invariants

Rectangle invariant:

```text
Width and height are independent.
```

Square adds:

```text
Width == Height
```

Changing one property unexpectedly affects another.

This breaks assumptions clients may make about Rectangle behavior.

---

# Real-World Example

Suppose we have:

```python
class Bird:
    def fly(self):
        pass
```

Then:

```python
class Sparrow(Bird):
    def fly(self):
        print("Flying")
```

works.

But:

```python
class Penguin(Bird):
    def fly(self):
        raise Exception("Penguins cannot fly")
```

Now code:

```python
def make_bird_fly(bird):
    bird.fly()
```

works for `Sparrow` but fails for `Penguin`.

This suggests the abstraction is wrong.

Better:

```text
Bird

FlyingBird → Sparrow
SwimmingBird → Penguin
```

Do not force all birds into a `fly()` contract they cannot satisfy.

---

# Another Real-World Example

Suppose:

```python
class PaymentProcessor:
    def refund(self, payment):
        pass
```

Then every subtype is expected to support refunds.

If:

```python
class SomePaymentProcessor(PaymentProcessor):
    def refund(self, payment):
        raise Exception("Refund unsupported")
```

then it may violate the parent's contract.

A better abstraction may separate capabilities.

---

# How to Identify an LSP Violation

Ask:

> If I replace the parent object with the child object, will the client code still behave correctly?

Warning signs include:

```text
Child throws "Not Supported"
```

```text
Child ignores inherited methods
```

```text
Child changes unrelated properties
```

```text
Child requires more restrictive input
```

```text
Client code checks subtype:
if isinstance(x, Child):
```

Frequent subtype checks may indicate that subclasses are not truly substitutable.

---

# LSP and Inheritance

Inheritance should mean more than code reuse.

Bad reason:

> "These classes share some fields, so let one inherit from another."

Better reason:

> "The child satisfies the complete behavioral contract of the parent."

---

# Composition Can Be Better Than Inheritance

If two classes share implementation but not behavioral contracts, consider:

```text
Composition
```

instead of forcing inheritance.

General rule:

> **Prefer composition when the IS-A relationship is not behaviorally valid.**

---

# Interview Question

## What is the Liskov Substitution Principle?

LSP states:

> **A derived class should be substitutable for its base class without changing the correctness or expected behavior of the program.**

For example, making `Square` inherit from `Rectangle` can violate LSP because Rectangle clients expect width and height to be independently modifiable.

When a Square's height changes, its width must also change, producing unexpected behavior.

Therefore, Square and Rectangle may be better modeled as separate implementations of a common `Shape` abstraction.

---

# Rectangle-Square Interview Explanation

You can explain it simply:

```text
Rectangle says:
width and height are independent.

Square says:
width must always equal height.
```

Therefore:

```text
Changing height on Rectangle
→ Only height changes.

Changing height on Square
→ Width also changes.
```

So code written for Rectangle can behave differently with Square.

Hence:

> **Square is not safely substitutable for Rectangle.**

---

# LSP vs OCP

## OCP

Question:

> Can I add new behavior without continuously modifying existing code?

```text
Open for extension
Closed for modification
```

---

## LSP

Question:

> Can I replace the parent with the child without breaking expected behavior?

```text
Parent
  ↓
Child substitution
  ↓
Behavior remains valid
```

---

# Quick Revision

```text
LSP
→ Liskov Substitution Principle
```

```text
Rule
→ Child should replace parent safely
```

```text
Main Focus
→ Behavioral compatibility
```

```text
Rectangle
→ Width and height independent
```

```text
Square
→ Width == Height
```

```text
Problem
→ Square changes behavior expected from Rectangle
```

```text
Better Design
→ Shape
   ├── Rectangle
   └── Square
```

```text
Warning Signs
→ Unsupported methods
→ Unexpected side effects
→ Stronger restrictions
→ Weaker guarantees
```

---

# Key Takeaways

- **LSP means a subtype must be usable anywhere its parent type is expected.**
- **Substitution must preserve behavior, not just type compatibility.**
- **A child should respect the behavioral contract of its parent.**
- **Square inheriting Rectangle can violate LSP because width and height are not independently modifiable.**
- **Inheritance should represent behavioral substitutability, not merely code reuse.**
- **A child should not unexpectedly reject operations supported by the parent.**
- **A child should not weaken guarantees provided by the parent.**
- **When subtype behavior differs fundamentally, use a better abstraction or composition.**

# One-Line Revision

> **LSP = if `B` extends `A`, replacing `A` with `B` should not break the assumptions or expected behavior of client code.**