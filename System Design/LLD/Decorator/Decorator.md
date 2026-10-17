# Decorator Design Pattern

Decorator is a **structural design pattern**.

> **Decorator adds new behavior to an individual object by wrapping it, without modifying the original object's class.**

Simple idea:

```text
Existing Object
      ↓
  Decorator
      ↓
Same Object Behavior
+
Extra Behavior
```

The main goal is:

> Add functionality dynamically without changing existing code or creating a large inheritance hierarchy.

---

# Why Do We Need Decorator?

Suppose we have:

```text
Circle
Square
```

and later we want to add features such as:

```text
Color
Transparency
Border
Logging
Caching
```

One option is inheritance.

For example:

```text
Circle
├── RedCircle
├── TransparentCircle
├── RedTransparentCircle
└── ...
```

This quickly creates:

> **Class Explosion**

If every new feature needs another subclass combination, the design becomes difficult to maintain.

---

# Better Idea

Keep the original object unchanged.

Wrap it:

```text
Circle
   ↓
ColoredShape
   ↓
TransparentShape
```

Each wrapper adds one responsibility.

This follows the general idea of:

- OCP → add behavior without repeatedly modifying existing code
- SRP → keep each added behavior separate

---

# Composition Instead of Inheritance

Decorator usually relies on:

```text
HAS-A
```

rather than:

```text
IS-A only
```

Example:

```python
class ColoredShape:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
```

`ColoredShape`:

```text
HAS-A Shape
```

and wraps it.

---

# 1. Python Function Decorator

Python has language-level decorators such as:

```python
@time_it
def some_operation():
    ...
```

These are not exactly the same as the GoF Decorator pattern, but the idea is similar:

> Wrap existing behavior and add something around it.

---

# Timing Example

```python
import time
from functools import wraps


def time_it(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()

        result = func(*args, **kwargs)

        end = time.time()

        print(
            f"{func.__name__} execution time = "
            f"{int((end - start) * 1000)}ms"
        )

        return result

    return wrapper
```

Then:

```python
@time_it
def some_operation():
    print("Starting operation")
    time.sleep(1)
    print("We are done")
    return 123
```

Calling:

```python
some_operation()
```

actually behaves conceptually like:

```python
time_it(some_operation)()
```

---

# What Is Happening?

Originally:

```text
some_operation()
```

does:

```text
Operation
```

After decoration:

```text
Start Timer
    ↓
Operation
    ↓
Stop Timer
    ↓
Print Duration
```

The original function's core logic does not need to change.

---

# Why `@wraps`?

Without:

```python
@wraps(func)
```

the decorated function may appear to Python as:

```text
wrapper
```

instead of:

```text
some_operation
```

`functools.wraps()` preserves useful metadata such as:

- Function name
- Documentation
- Module metadata

---

# Function Decorator Mental Model

```text
Original Function
      ↓
Decorator Function
      ↓
Wrapper Function
      ↓
Extra Behavior + Original Function
```

---

# Python Decorator vs Decorator Pattern

## Python Function Decorator

Usually wraps:

```text
Function / Method
```

Example:

```python
@time_it
```

---

## GoF Decorator Pattern

Usually wraps:

```text
Object
```

Example:

```text
Circle
→ ColoredShape
→ TransparentShape
```

Both use the same general idea:

> Add behavior around something existing.

But do not confuse the language feature with the object-oriented design pattern.

---

# 2. Classic Decorator Pattern

Suppose we have a Shape abstraction.

```python
from abc import ABC, abstractmethod


class Shape(ABC):

    @abstractmethod
    def __str__(self):
        pass
```

Concrete shapes:

```python
class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def resize(self, factor):
        self.radius *= factor

    def __str__(self):
        return (
            f"A circle of radius "
            f"{self.radius}"
        )
```

```python
class Square(Shape):
    def __init__(self, side):
        self.side = side

    def __str__(self):
        return (
            f"A square of side "
            f"{self.side}"
        )
```

---

# Basic Shape

```python
circle = Circle(2)
```

Output:

```text
A circle of radius 2
```

Now we want:

```text
A red circle
```

We do not want to modify `Circle`.

We also do not want:

```text
RedCircle
BlueCircle
GreenCircle
...
```

So we wrap it.

---

# Colored Decorator

```python
class ColoredShape(Shape):
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color

    def __str__(self):
        return (
            f"{self.shape} "
            f"has color {self.color}"
        )
```

Usage:

```python
circle = Circle(2)

red_circle = ColoredShape(
    circle,
    "red"
)

print(red_circle)
```

Conceptually:

```text
ColoredShape
      ↓
   Circle
```

The decorator adds:

```text
Color
```

while reusing the wrapped object's existing representation.

---

# Transparency Decorator

```python
class TransparentShape(Shape):
    def __init__(
        self,
        shape,
        transparency
    ):
        self.shape = shape
        self.transparency = transparency

    def __str__(self):
        return (
            f"{self.shape} "
            f"has transparency "
            f"{self.transparency}"
        )
```

Now:

```python
red_half_transparent_circle = (
    TransparentShape(
        red_circle,
        "50%"
    )
)
```

The object graph becomes:

```text
TransparentShape
       ↓
ColoredShape
       ↓
Circle
```

Each layer adds behavior.

---

# Output

Conceptually:

```text
Circle
→ A circle of radius 2
```

then:

```text
ColoredShape
→ A circle of radius 2 has color red
```

then:

```text
TransparentShape
→ A circle of radius 2
  has color red
  has transparency 50%
```

This is the core Decorator idea.

---

# Decorators Can Be Stacked

This is one of the biggest advantages.

```text
Base Object
   ↓
Decorator A
   ↓
Decorator B
   ↓
Decorator C
```

Example:

```text
Circle
 ↓
Color
 ↓
Transparency
 ↓
Border
```

Each feature remains separate.

---

# Why Not Create Every Combination?

Without Decorator:

```text
RedCircle
TransparentCircle
RedTransparentCircle
BlueCircle
BlueTransparentCircle
...
```

With Decorator:

```text
Circle
+
ColoredShape
+
TransparentShape
```

The features are composable.

---

# Decorator Structure

Classic structure:

```text
          Component
          /       \
 Concrete         Decorator
 Component           |
                     |
              Concrete Decorator
```

In your example:

```text
Shape
├── Circle
├── Square
├── ColoredShape
└── TransparentShape
```

And decorators internally contain:

```text
another Shape
```

---

# Core Property of Decorator

The decorator should ideally expose the same general interface as the wrapped object.

That allows:

```text
Client
 ↓
Shape
```

without caring whether it receives:

```text
Circle
```

or:

```text
ColoredShape
```

or:

```text
TransparentShape
```

This makes decorators interchangeable with the underlying abstraction.

---

# Preventing Duplicate Decoration

Your example includes:

```python
if isinstance(
    shape,
    ColoredShape
):
    raise Exception(
        "You cannot color a colored shape"
    )
```

This is a business rule, not a requirement of the Decorator Pattern.

Decorator itself does not inherently prevent:

```text
ColoredShape(
    ColoredShape(...)
)
```

Whether duplicate decoration is allowed depends on the domain.

For example:

```text
LoggingDecorator
→ LoggingDecorator
```

may be pointless.

But other decorators may legitimately appear multiple times.

---

# Dynamic Object Decoration

Python allows us to wrap objects dynamically at runtime.

Your file example demonstrates this idea.

---

# FileWithLogging

Suppose we have a normal file object:

```python
file = open(
    "hello.txt",
    "w"
)
```

It already knows how to:

- `write()`
- `writelines()`
- `close()`

Now we want logging behavior.

Instead of rewriting the file implementation, wrap it.

```python
class FileWithLogging:
    def __init__(self, file):
        self.file = file

    def writelines(self, strings):
        self.file.writelines(strings)

        print(
            f"Wrote {len(strings)} lines"
        )
```

Now:

```text
FileWithLogging
       ↓
    File Object
```

---

# Delegating Unknown Operations

We do not want to manually rewrite every file method.

Python provides:

```python
__getattr__()
```

Example:

```python
def __getattr__(self, item):
    return getattr(
        self.file,
        item
    )
```

If `FileWithLogging` does not have:

```text
write()
```

Python forwards it to:

```text
self.file.write()
```

---

# Flow

```python
file.write("testing")
```

becomes:

```text
FileWithLogging.write
      ↓
Not found
      ↓
__getattr__("write")
      ↓
Underlying File.write
```

So the decorator can intercept selected methods and delegate everything else.

---

# Corrected Dynamic Decorator

```python
class FileWithLogging:
    def __init__(self, file):
        object.__setattr__(
            self,
            "file",
            file
        )

    def writelines(self, strings):
        self.file.writelines(strings)

        print(
            f"Wrote {len(strings)} entries"
        )

    def __iter__(self):
        return iter(self.file)

    def __next__(self):
        return next(self.file)

    def __getattr__(self, item):
        return getattr(
            self.file,
            item
        )

    def __setattr__(
        self,
        key,
        value
    ):
        setattr(
            self.file,
            key,
            value
        )

    def __delattr__(self, item):
        delattr(
            self.file,
            item
        )
```

---

# Important Bug in Your Original Code

You had:

```python
setattr(
    self.__dict__["file"],
    key
)
```

But `setattr()` requires:

```python
setattr(
    object,
    attribute_name,
    value
)
```

So the value argument was missing.

---

# Dynamic Decorator Idea

The decorator can:

```text
Intercept selected operations
        ↓
Add behavior
        ↓
Delegate remaining operations
        ↓
Wrapped object
```

Example:

```text
writelines()
→ Add logging

write()
→ Delegate directly

close()
→ Delegate directly
```

---

# Real-World Backend Example — Logging

Suppose we have:

```python
class PaymentService:
    def pay(self, amount):
        ...
```

We want logging without changing it.

```text
PaymentService
      ↓
LoggingDecorator
```

Then:

```text
Before payment
→ log request

Payment
→ execute

After payment
→ log result
```

---

# Real-World Example — Caching

```text
Repository
    ↓
CachingDecorator
```

Flow:

```text
find_user()
   ↓
Cache hit?
 /       \
Yes       No
 ↓         ↓
Return    Call real repository
          ↓
        Cache result
```

The original repository remains unchanged.

---

# Real-World Example — Retry

```text
External API Client
        ↓
RetryDecorator
```

The decorator can:

```text
Call API
 ↓
Failure?
 ↓
Retry
```

without changing the external API client implementation.

---

# Decorator and OCP

Decorator supports the Open/Closed Principle.

Existing class:

```text
Circle
```

does not need modification.

New behavior:

```text
ColoredShape
TransparentShape
```

is added through extension/composition.

---

# Decorator and SRP

Each decorator can own one additional concern.

Example:

```text
LoggingDecorator
→ Logging

CachingDecorator
→ Caching

RetryDecorator
→ Retry logic
```

Instead of:

```text
Service
├── Business logic
├── Logging
├── Caching
├── Retry
└── Metrics
```

This helps keep concerns separate.

---

# Decorator vs Inheritance

## Inheritance

Behavior is usually fixed at class definition time.

```text
RedCircle
extends
Circle
```

---

## Decorator

Behavior can be composed at runtime.

```text
Circle
 ↓
ColoredShape
 ↓
TransparentShape
```

You can dynamically decide which features an individual object gets.

---

# Decorator vs Adapter

Both are structural patterns.

## Adapter

Changes the interface.

```text
Interface A
 ↓
Adapter
 ↓
Interface B
```

Goal:

> Compatibility.

---

## Decorator

Keeps the same conceptual interface and adds behavior.

```text
Component
 ↓
Decorator
 ↓
Extra Behavior
```

Goal:

> Enhancement.

Easy revision:

```text
Adapter
→ Changes interface

Decorator
→ Adds behavior
```

---

# Decorator vs Proxy

These can look very similar because both wrap another object.

## Decorator

Main intent:

> Add behavior.

Examples:

```text
Logging
Formatting
Caching
Compression
```

---

## Proxy

Main intent:

> Control access to another object.

Examples:

```text
Lazy loading
Authorization
Remote proxy
Access control
```

The class structure may look similar.

The main difference is:

> **Intent**

---

# Decorator vs Bridge

## Bridge

Separates two independent hierarchies.

```text
Shape
↔
Renderer
```

## Decorator

Wraps one object with additional behavior.

```text
Shape
↓
ColoredShape
↓
TransparentShape
```

Bridge is about:

```text
Independent variation
```

Decorator is about:

```text
Behavioral enhancement
```

---

# When to Use Decorator

Use Decorator when:

- You want to add behavior without modifying a class
- Features should be composable
- Different individual objects need different behavior
- Inheritance would cause too many subclasses
- Behavior should be added/removed dynamically

---

# When Not to Use Decorator

Avoid excessive decoration when the object chain becomes difficult to understand.

For example:

```text
A
 ↓
B
 ↓
C
 ↓
D
 ↓
E
 ↓
F
```

Debugging can become harder because behavior is spread across many wrappers.

Use it when composition actually improves the design.

---

# Benefits

Decorator provides:

- Runtime flexibility
- No modification of original class
- Avoids subclass explosion
- Composable behaviors
- Better separation of concerns
- Supports OCP
- Often favors composition over inheritance

---

# Drawbacks

Possible disadvantages:

- Many small wrapper objects
- Deep decorator chains
- Harder debugging
- Object identity can become confusing
- Ordering of decorators can matter

Example:

```text
Compression
→ Encryption
```

may behave differently from:

```text
Encryption
→ Compression
```

So decorator order can sometimes matter.

---

# Interview Question

## What is the Decorator Pattern?

Decorator is a structural design pattern that adds new behavior to an existing object by wrapping it rather than modifying its original class.

For example, instead of creating separate classes such as:

```text
RedCircle
TransparentCircle
RedTransparentCircle
```

we can start with:

```text
Circle
```

and dynamically wrap it:

```text
Circle
 ↓
ColoredShape
 ↓
TransparentShape
```

Each decorator adds one capability while preserving the underlying Shape behavior.

This avoids class explosion and helps follow the Open/Closed Principle.

---

# How to Recognize Decorator?

Look for this requirement:

> I already have an object that works, but I want to add optional behavior to some instances without changing its class.

Then:

```text
Object
 ↓
Decorator
 ↓
Enhanced Object
```

may be appropriate.

---

# Mental Model

Think:

```text
Coffee
```

then:

```text
Coffee
+ Milk
```

then:

```text
Coffee
+ Milk
+ Sugar
```

Each layer wraps the previous one.

You do not need classes such as:

```text
MilkCoffee
SugarCoffee
MilkSugarCoffee
...
```

That is the essence of Decorator.

---

# Quick Revision

```text
Decorator
→ Structural Design Pattern
```

```text
Goal
→ Add behavior to an object dynamically
```

```text
Core Technique
→ Composition / wrapping
```

```text
Base Object
→ Circle
```

```text
Decorators
→ ColoredShape
→ TransparentShape
```

```text
Structure

Circle
 ↓
ColoredShape
 ↓
TransparentShape
```

```text
OCP
→ Add behavior without modifying existing class
```

```text
SRP
→ Keep added concerns separate
```

```text
Adapter
→ Changes interface
```

```text
Decorator
→ Adds behavior
```

```text
Proxy
→ Controls access
```

---

# Key Takeaways

- **Decorator is a structural design pattern.**
- **It adds behavior to an individual object without modifying the object's original class.**
- **Decorator primarily uses composition and wrapping.**
- **Decorators can be stacked to combine multiple behaviors.**
- **It avoids creating subclasses for every possible feature combination.**
- **Decorator supports OCP because existing code remains unchanged.**
- **Each decorator can represent a separate concern, helping SRP.**
- **Python's `@decorator` syntax and the GoF Decorator Pattern share the wrapping idea but are not the exact same mechanism.**
- **Decorator differs from Adapter: Adapter changes compatibility/interface; Decorator adds behavior.**
- **Decorator differs from Proxy mainly by intent: Decorator enhances behavior, Proxy controls access.**
- **Decorator order can sometimes affect behavior.**

# One-Line Revision

> **Decorator = wrap an existing object with another object that exposes compatible behavior while adding extra functionality around it.**