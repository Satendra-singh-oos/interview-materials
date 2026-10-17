# Adapter Design Pattern

Adapter is a **structural design pattern**.

> **Adapter allows two incompatible interfaces to work together by converting the interface/data expected by one side into the form provided by the other.**

Simple idea:

```text
Existing System A
      ↓
   Adapter
      ↓
Existing System B
```

The Adapter sits between them and performs the required conversion.

---

# Why Do We Need Adapter?

Suppose you already have a drawing function:

```python
def draw_point(point):
    print(".", end="")
```

This function knows how to draw:

```text
Point
```

But your application represents shapes using:

```text
Rectangle
   ↓
Lines
```

So we have an incompatibility:

```text
Drawing System
expects Points

Application
provides Lines
```

We do not want to rewrite either existing system.

Therefore:

```text
Line
 ↓
LineToPointAdapter
 ↓
Points
 ↓
draw_point()
```

This is the Adapter Pattern.

---

# Existing Interface — Point Renderer

Suppose this code is already provided:

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def draw_point(point):
    print(".", end="")
```

The renderer understands only individual points.

Conceptually:

```text
draw_point(Point)
```

---

# Our Application Uses Lines

Our application works with lines:

```python
class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end
```

A line contains:

```text
start Point
+
end Point
```

---

# Rectangle

A rectangle can be represented as four lines.

```python
class Rectangle(list):
    """Rectangle represented as a list of lines."""

    def __init__(self, x, y, width, height):
        super().__init__()

        self.append(
            Line(
                Point(x, y),
                Point(x + width, y)
            )
        )

        self.append(
            Line(
                Point(x + width, y),
                Point(x + width, y + height)
            )
        )

        self.append(
            Line(
                Point(x, y),
                Point(x, y + height)
            )
        )

        self.append(
            Line(
                Point(x, y + height),
                Point(x + width, y + height)
            )
        )
```

Structure:

```text
Rectangle
   ↓
4 Lines
   ↓
Each line has start/end Point
```

---

# The Incompatibility

The application gives us:

```text
Rectangle
→ Line
```

But the drawing API accepts:

```text
Point
```

We cannot directly do:

```python
draw_point(line)
```

because `draw_point()` expects a `Point`, not a `Line`.

---

# Solution — LineToPointAdapter

We create an Adapter that converts:

```text
Line
```

into:

```text
List of Points
```

---

# Basic Adapter

```python
class LineToPointAdapter(list):
    count = 0

    def __init__(self, line):
        super().__init__()

        type(self).count += 1

        print(
            f"{type(self).count}: Generating points for line "
            f"[{line.start.x},{line.start.y}]→"
            f"[{line.end.x},{line.end.y}]"
        )

        left = min(
            line.start.x,
            line.end.x
        )

        right = max(
            line.start.x,
            line.end.x
        )

        top = min(
            line.start.y,
            line.end.y
        )

        bottom = max(
            line.start.y,
            line.end.y
        )

        if right - left == 0:
            for y in range(top, bottom + 1):
                self.append(
                    Point(left, y)
                )

        elif bottom - top == 0:
            for x in range(left, right + 1):
                self.append(
                    Point(x, top)
                )
```

The Adapter itself behaves like:

```text
List[Point]
```

even though it receives:

```text
Line
```

---

# Adapter Flow

Suppose:

```text
Line:
(1,1) → (5,1)
```

Adapter converts it into:

```text
(1,1)
(2,1)
(3,1)
(4,1)
(5,1)
```

Then:

```python
for point in adapter:
    draw_point(point)
```

works normally.

---

# Drawing Rectangles

```python
def draw(rectangles):
    print("\n--- Drawing some stuff ---")

    for rectangle in rectangles:
        for line in rectangle:

            adapter = LineToPointAdapter(
                line
            )

            for point in adapter:
                draw_point(point)
```

Flow:

```text
Rectangle
   ↓
Line
   ↓
LineToPointAdapter
   ↓
Points
   ↓
draw_point()
```

This is the core Adapter Pattern.

---

# What Is the Adapter Actually Doing?

The Adapter is not changing either system.

It leaves:

```text
draw_point()
```

unchanged.

It also leaves:

```text
Rectangle / Line
```

unchanged.

Instead, it translates between them.

```text
Line representation
       ↓
     Adapter
       ↓
Point representation
```

---

# Real-World Analogy

Think about a travel power adapter.

You have:

```text
Indian Plug
```

but the wall socket expects:

```text
European Plug
```

You do not:

- Replace the appliance
- Rebuild the wall socket

You insert:

```text
Plug
 ↓
Adapter
 ↓
Socket
```

Software Adapter works similarly.

---

# Problem With the Basic Adapter

Now suppose:

```python
rectangles = [
    Rectangle(1, 1, 10, 10),
    Rectangle(3, 3, 6, 6)
]

draw(rectangles)
draw(rectangles)
```

Every time `draw()` executes:

```text
Line
 ↓
Generate all points again
```

Even though the same lines were already adapted during the first draw.

That means repeated computation.

---

# Adapter With Caching

We can store the conversion result.

```text
Line
 ↓
Already converted?
   ↓
Yes → Return cached points

No → Generate points
      ↓
     Cache
      ↓
     Return
```

---

# Cached Adapter

```python
class LineToPointAdapter:
    count = 0
    cache = {}

    def __init__(self, line):
        self.key = (
            line.start.x,
            line.start.y,
            line.end.x,
            line.end.y
        )

        if self.key in self.cache:
            return

        type(self).count += 1

        print(
            f"{type(self).count}: Generating points for line "
            f"[{line.start.x},{line.start.y}]→"
            f"[{line.end.x},{line.end.y}]"
        )

        left = min(
            line.start.x,
            line.end.x
        )
        right = max(
            line.start.x,
            line.end.x
        )
        top = min(
            line.start.y,
            line.end.y
        )
        bottom = max(
            line.start.y,
            line.end.y
        )

        points = []

        if right - left == 0:
            for y in range(top, bottom + 1):
                points.append(
                    Point(left, y)
                )

        elif bottom - top == 0:
            for x in range(left, right + 1):
                points.append(
                    Point(x, top)
                )

        self.cache[self.key] = points

    def __iter__(self):
        return iter(
            self.cache[self.key]
        )
```

---

# First Draw

The first time:

```text
Line
 ↓
Cache miss
 ↓
Generate Points
 ↓
Store in Cache
```

Example:

```text
Line (1,1) → (11,1)

Cache:
{
   (1,1,11,1): [Point, Point, ...]
}
```

---

# Second Draw

The second time:

```text
Same Line
   ↓
Cache hit
   ↓
Reuse points
```

No conversion work is repeated.

---

# Why Cache Inside the Adapter?

The conversion:

```text
Line → Points
```

may be expensive if:

- There are many lines
- Lines are long
- Drawing happens repeatedly

Caching means:

```text
Convert once
Reuse many times
```

---

# Important Note About Your Original Cache

Your original code used:

```python
hash(line)
```

as the cache key.

Without implementing custom:

```python
__eq__()
__hash__()
```

Python normally hashes custom objects using their identity.

That means two separate `Line` objects with identical coordinates may have different hashes.

Example:

```python
Line(Point(1, 1), Point(5, 1))
Line(Point(1, 1), Point(5, 1))
```

They represent the same logical line but are different objects.

For this example, a coordinate tuple is clearer:

```python
(
    start.x,
    start.y,
    end.x,
    end.y
)
```

---

# Adapter With Caching Flow

```text
Line
 ↓
Build cache key
 ↓
Is key cached?
 /          \
Yes          No
 ↓            ↓
Reuse      Convert Line
Points       ↓
             Cache Points
             ↓
          Return Points
```

---

# Adapter Participants

The classic Adapter Pattern usually contains:

## Client

The code that wants to perform some operation.

In our example:

```text
draw()
```

---

## Target Interface

The interface expected by the client.

Here:

```text
Point / iterable of Points
```

because ultimately:

```python
draw_point(point)
```

must receive Points.

---

## Adaptee

The existing incompatible object.

Here:

```text
Line
```

---

## Adapter

The component that translates the Adaptee into the Target format.

Here:

```text
LineToPointAdapter
```

---

# Structure

```text
Client
  |
  | expects
  ↓
Point Interface
  ↑
  |
Adapter
  ↑
  |
Line
```

Or specifically:

```text
draw()
   ↓
LineToPointAdapter
   ↓
Line → Points
   ↓
draw_point()
```

---

# Object Adapter vs Class Adapter

Two common Adapter approaches exist.

## Object Adapter

Uses **composition**.

```text
Adapter
  ↓
contains/wraps
  ↓
Adaptee
```

Example conceptually:

```python
class Adapter:
    def __init__(self, old_service):
        self.old_service = old_service
```

This is generally flexible and commonly used.

---

## Class Adapter

Uses **inheritance** to adapt behavior.

Conceptually:

```text
Adapter
inherits from
Adaptee
```

This depends on language capabilities and is usually more tightly coupled.

---

# Real-World Backend Example

Suppose your application expects:

```python
class PaymentGateway:
    def pay(self, amount):
        ...
```

But an external provider gives:

```python
legacy_provider.make_payment(
    rupees=amount,
    transaction_type="debit"
)
```

Instead of changing your entire application:

```text
Application
   ↓
PaymentGatewayAdapter
   ↓
Legacy Payment Provider
```

Adapter converts your expected call into the provider's API.

---

# Another Example — Different APIs

Application expects:

```text
send(message)
```

Third-party system provides:

```text
publish(topic, payload)
```

Adapter:

```text
send(message)
      ↓
Adapter
      ↓
publish(topic, payload)
```

The rest of your application does not need to understand the third-party interface.

---

# When to Use Adapter

Use Adapter when:

- Two components have incompatible interfaces
- You are integrating legacy code
- You are integrating a third-party library/API
- You cannot or should not modify either system
- You want to isolate external API differences
- Data representation must be transformed

---

# When Not to Use Adapter

Do not add an Adapter simply because two classes are different.

There should be a genuine compatibility problem.

If you control both systems and can define a clean shared abstraction directly, that may be simpler.

---

# Benefits

Adapter gives:

- Reuse of existing code
- Integration without modifying existing classes
- Isolation of third-party/legacy APIs
- Lower coupling
- Easier replacement of external systems
- Cleaner client code

---

# Drawbacks

Adapter can add:

- Additional classes
- Additional abstraction
- Conversion overhead
- Complexity when many adapters exist

Caching can help if conversion is expensive and repeated.

---

# Adapter vs Decorator

These are both structural patterns, but solve different problems.

## Adapter

Changes:

> **Interface**

```text
Interface A
   ↓
Adapter
   ↓
Interface B
```

Goal:

> Make incompatible objects work together.

---

## Decorator

Keeps the same interface but adds:

> **Behavior**

```text
Component
   ↓
Decorator
   ↓
Same interface + extra behavior
```

Easy revision:

```text
Adapter
→ Change interface

Decorator
→ Add behavior
```

---

# Adapter vs Facade

## Adapter

Makes one interface compatible with another.

```text
A
↓
Adapter
↓
B
```

## Facade

Provides a simplified interface over a more complicated subsystem.

```text
Complex Subsystem
       ↓
     Facade
       ↓
Simple Interface
```

Easy revision:

```text
Adapter
→ Compatibility

Facade
→ Simplicity
```

---

# Interview Question

## What is the Adapter Pattern?

Adapter is a structural design pattern that allows objects with incompatible interfaces to work together.

For example, suppose a rendering library can only draw individual `Point` objects, while our application represents a rectangle as a collection of `Line` objects.

Instead of modifying the renderer or rectangle model, we introduce a `LineToPointAdapter`.

The Adapter converts each `Line` into the sequence of `Point` objects expected by the renderer.

```text
Line
 ↓
Adapter
 ↓
Points
 ↓
Renderer
```

---

# Why Add Caching to an Adapter?

If conversion is expensive and the same object is adapted repeatedly, the Adapter can cache the conversion result.

Example:

```text
First draw
Line → Generate Points → Cache

Second draw
Line → Cache Hit → Reuse Points
```

Caching is an optimization, not a required part of the Adapter Pattern itself.

---

# How to Recognize Adapter Pattern?

Look for this situation:

```text
I have something that provides A,
but my code expects B.
```

and you cannot or do not want to change either side.

Then:

```text
A
↓
Adapter
↓
B
```

may be appropriate.

---

# Quick Revision

```text
Adapter
→ Structural Design Pattern
```

```text
Problem
→ Incompatible interfaces
```

```text
Solution
→ Translate one interface/data representation into another
```

```text
Adaptee
→ Existing incompatible object
```

```text
Target
→ Interface client expects
```

```text
Adapter
→ Converts Adaptee → Target
```

```text
Our Example

Line
→ LineToPointAdapter
→ Points
→ draw_point()
```

```text
Caching
→ Avoid repeated expensive conversion
```

```text
Adapter vs Decorator
→ Interface vs behavior
```

```text
Adapter vs Facade
→ Compatibility vs simplification
```

---

# Key Takeaways

- **Adapter is a structural design pattern.**
- **It connects components with incompatible interfaces.**
- **The Adapter converts what one system provides into what another system expects.**
- **In this example, the application provides Lines but the renderer requires Points.**
- **`LineToPointAdapter` converts each Line into drawable Points.**
- **Neither the renderer nor Rectangle needs to be modified.**
- **Caching is optional and only optimizes repeated adaptation.**
- **Cache keys should represent logical identity if equivalent objects should reuse cached data.**
- **Object Adapter typically uses composition; Class Adapter uses inheritance.**
- **Adapter changes compatibility/interface; Decorator adds behavior; Facade simplifies a subsystem.**

# One-Line Revision

> **Adapter = when I already have A but my client expects B, place an Adapter between them that translates A into B without changing either side.**