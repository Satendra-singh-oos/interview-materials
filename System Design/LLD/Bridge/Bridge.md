# Bridge Design Pattern

Bridge is a **structural design pattern**.

> **Bridge separates an abstraction from its implementation so that both can vary independently.**

Simple meaning:

> When an object has two independent dimensions that can change, do not combine every possible variation through inheritance. Connect the two sides using composition.

---

# Why Do We Need Bridge?

Suppose we have two shapes:

```text
Circle
Square
```

and two rendering mechanisms:

```text
Vector
Raster
```

Without Bridge, we may start creating classes like:

```text
VectorCircle
RasterCircle

VectorSquare
RasterSquare
```

Now add another shape:

```text
Triangle
```

We need:

```text
VectorTriangle
RasterTriangle
```

Now add another renderer:

```text
OpenGLRenderer
```

We may need:

```text
OpenGLCircle
OpenGLSquare
OpenGLTriangle
```

This starts creating a:

> **Class Explosion**

---

# The Problem

We have two dimensions changing independently:

```text
Dimension 1
→ Shape

Circle
Square
Triangle
```

and:

```text
Dimension 2
→ Rendering Technology

Vector
Raster
OpenGL
```

If we combine both using inheritance, the number of classes grows roughly like:

```text
Shapes × Renderers
```

For example:

```text
3 Shapes × 3 Renderers
= 9 classes
```

If both sides keep growing, maintenance becomes difficult.

---

# Bridge Solution

Separate the two hierarchies.

```text
Shape Hierarchy
      ↓
   Renderer
      ↓
Renderer Hierarchy
```

More specifically:

```text
        Shape
          |
     has Renderer
          |
   -----------------
   |               |
VectorRenderer   RasterRenderer
```

Now Shape and Renderer can change independently.

---

# Renderer — Implementation Side

```python
class Renderer:
    def render_circle(self, radius):
        pass
```

`Renderer` defines:

> **How a shape should be rendered.**

It represents the implementation side of the Bridge.

---

# Vector Renderer

```python
class VectorRenderer(Renderer):
    def render_circle(self, radius):
        print(
            f"Drawing a circle "
            f"of radius {radius}"
        )
```

This renderer uses vector-style drawing.

Conceptually:

```text
Circle
→ Vector instructions
```

---

# Raster Renderer

```python
class RasterRenderer(Renderer):
    def render_circle(self, radius):
        print(
            f"Drawing pixels for "
            f"circle of radius {radius}"
        )
```

This renderer uses raster/pixel-style drawing.

Conceptually:

```text
Circle
→ Pixels
```

---

# Shape — Abstraction Side

```python
class Shape:
    def __init__(self, renderer):
        self.renderer = renderer

    def draw(self):
        pass

    def resize(self, factor):
        pass
```

`Shape` represents:

> **What we are working with.**

For example:

```text
Circle
Square
Triangle
```

Notice that Shape does not directly know how rendering works.

Instead:

```python
self.renderer
```

contains the implementation.

This is the **bridge**.

---

# Circle

```python
class Circle(Shape):
    def __init__(self, renderer, radius):
        super().__init__(renderer)
        self.radius = radius

    def draw(self):
        self.renderer.render_circle(
            self.radius
        )

    def resize(self, factor):
        self.radius *= factor
```

`Circle` handles circle-specific behavior:

```text
radius
resize()
```

but rendering is delegated to:

```text
Renderer
```

---

# The Bridge

The most important line is:

```python
self.renderer = renderer
```

This connects:

```text
Abstraction
→ Shape
```

with:

```text
Implementation
→ Renderer
```

So:

```text
Circle
   ↓
Renderer
```

is the bridge between two independent hierarchies.

---

# Runtime Selection

Now we can create:

```python
vector = VectorRenderer()
raster = RasterRenderer()
```

and choose the implementation at runtime.

For example:

```python
circle = Circle(
    vector,
    5
)
```

Flow:

```text
Circle
 radius = 5
    ↓
VectorRenderer
    ↓
Draw vector circle
```

---

# Switching Implementation

We can also create:

```python
circle = Circle(
    raster,
    5
)
```

Now:

```text
Same Circle abstraction
        ↓
Different Renderer
        ↓
Raster output
```

The Circle class itself does not change.

---

# Example Flow

```python
vector = VectorRenderer()

circle = Circle(
    vector,
    5
)

circle.draw()
```

Output:

```text
Drawing a circle of radius 5
```

Then:

```python
circle.resize(2)
circle.draw()
```

Radius becomes:

```text
5 × 2 = 10
```

Output:

```text
Drawing a circle of radius 10
```

---

# What Is Varying Independently?

## Shape Side

We can add:

```text
Circle
Square
Triangle
```

without creating new Renderer classes for every combination.

---

## Renderer Side

We can add:

```text
VectorRenderer
RasterRenderer
OpenGLRenderer
SVGRenderer
```

without changing every Shape class.

That is the key Bridge idea.

---

# Without Bridge

```text
VectorCircle
RasterCircle

VectorSquare
RasterSquare

VectorTriangle
RasterTriangle
```

Adding a new renderer requires many new classes.

---

# With Bridge

```text
         Shape
       /   |   \
  Circle Square Triangle
       \   |   /
        Renderer
       /        \
 Vector        Raster
```

Each Shape can work with each Renderer.

---

# Adding a Square

Suppose we add:

```python
class Square(Shape):
    def __init__(
        self,
        renderer,
        side
    ):
        super().__init__(renderer)
        self.side = side

    def draw(self):
        self.renderer.render_square(
            self.side
        )

    def resize(self, factor):
        self.side *= factor
```

We extend the `Renderer` abstraction with:

```python
def render_square(self, side):
    pass
```

and each renderer implements its own version.

The important point is:

```text
Square
```

does not become:

```text
VectorSquare
RasterSquare
```

The rendering concern remains separate.

---

# Abstraction vs Implementation

Bridge terminology can be confusing.

## Abstraction

The higher-level object the client works with.

In this example:

```text
Shape
Circle
```

---

## Implementation

The lower-level mechanism used by the abstraction.

In this example:

```text
Renderer
VectorRenderer
RasterRenderer
```

So:

```text
Abstraction
    ↓
Shape

Implementation
    ↓
Renderer
```

---

# Bridge Uses Composition

Instead of:

```text
Circle inherits VectorRenderer
```

we use:

```text
Circle HAS-A Renderer
```

This is composition.

```python
self.renderer = renderer
```

Simple revision:

```text
Bridge
→ Prefer composition between two changing dimensions.
```

---

# Why Is Composition Better Here?

Because we can mix and match at runtime.

```python
Circle(VectorRenderer(), 5)
Circle(RasterRenderer(), 5)
```

Same Shape:

```text
Circle
```

Different implementation:

```text
Vector
Raster
```

No new Circle subclasses are required.

---

# Real-World Example — Notifications

Suppose we have notification types:

```text
AlertNotification
ReminderNotification
PromotionNotification
```

and delivery channels:

```text
Email
SMS
Push
```

Bad inheritance approach:

```text
EmailAlert
SMSAlert
PushAlert

EmailReminder
SMSReminder
PushReminder
```

Class explosion again.

Bridge:

```text
Notification
     ↓
DeliveryChannel
```

Now:

```text
AlertNotification + Email
AlertNotification + SMS
ReminderNotification + Push
```

can be combined freely.

---

# Real-World Backend Example

Suppose we have:

```text
Report
├── SalesReport
└── AuditReport
```

and output formats:

```text
Renderer
├── PDFRenderer
├── HTMLRenderer
└── CSVRenderer
```

Bridge allows:

```text
SalesReport + PDF
SalesReport + HTML

AuditReport + PDF
AuditReport + CSV
```

without creating classes like:

```text
PdfSalesReport
HtmlSalesReport
CsvAuditReport
...
```

---

# Bridge vs Adapter

These two are easy to confuse.

## Adapter

Used when:

> Two existing interfaces are incompatible.

```text
Existing A
   ↓
Adapter
   ↓
Existing B
```

Goal:

> Compatibility.

---

## Bridge

Used when:

> You intentionally separate two dimensions so both can evolve independently.

```text
Abstraction
   ↓
Bridge
   ↓
Implementation
```

Goal:

> Independent variation.

---

# Bridge vs Adapter — Easy Revision

```text
Adapter
→ Make old/incompatible things work together
```

```text
Bridge
→ Design two dimensions separately from the beginning
```

Adapter is often applied after incompatibility exists.

Bridge is usually an architectural/design decision made earlier.

---

# Bridge vs Strategy

They can look similar because both use composition.

## Strategy

Focuses on:

> Swapping an algorithm or behavior.

Example:

```text
Payment
→ PaymentStrategy
```

---

## Bridge

Focuses on:

> Separating two independent class hierarchies.

Example:

```text
Shape
↔
Renderer
```

A useful distinction:

```text
Strategy
→ One changing behavior
```

```text
Bridge
→ Two independently evolving dimensions
```

---

# How to Recognize Bridge

Ask:

> Do I have two different dimensions that both need to vary independently?

Example:

```text
Shape
+
Renderer
```

or:

```text
Notification Type
+
Delivery Channel
```

or:

```text
Report Type
+
Output Format
```

If combining them through inheritance would create many classes, Bridge may be appropriate.

---

# When to Use Bridge

Use Bridge when:

- Two dimensions vary independently
- Inheritance would cause class explosion
- Implementation should be replaceable at runtime
- You want abstraction and implementation hierarchies separated
- Platform-specific implementation should be hidden from higher-level code

---

# Benefits

Bridge provides:

- Avoids class explosion
- Separation of concerns
- Runtime flexibility
- Lower coupling
- Easier extension
- Better composition
- Independent development of abstraction and implementation

---

# Drawbacks

Bridge can introduce:

- More classes/interfaces
- More abstraction
- Extra indirection

For a very simple system:

```text
One Shape
+
One Renderer
```

Bridge may be unnecessary.

Use it when the independent variation actually exists.

---

# Interview Question

## What is the Bridge Pattern?

Bridge is a structural design pattern that separates an abstraction from its implementation so both can vary independently.

For example, suppose we have shapes such as Circle and Square, and rendering mechanisms such as Vector and Raster.

Without Bridge, we may create:

```text
VectorCircle
RasterCircle
VectorSquare
RasterSquare
```

which creates a growing number of subclasses.

With Bridge:

```text
Shape
    ↓
Renderer
```

each Shape stores a Renderer and delegates rendering to it.

So Circle can work with either VectorRenderer or RasterRenderer without changing the Circle implementation.

---

# Your Example — Mental Model

```text
Circle
→ Knows WHAT a circle is
→ radius
→ resize()
```

```text
Renderer
→ Knows HOW to draw
```

Then:

```text
Circle
   ↓
Renderer
```

connects the two.

That connection is:

> **The Bridge**

---

# Quick Revision

```text
Bridge
→ Structural Design Pattern
```

```text
Problem
→ Two independent dimensions
→ Inheritance creates class explosion
```

```text
Solution
→ Separate both hierarchies
→ Connect with composition
```

```text
Abstraction
→ Shape
```

```text
Implementation
→ Renderer
```

```text
Concrete Abstraction
→ Circle
```

```text
Concrete Implementations
→ VectorRenderer
→ RasterRenderer
```

```text
Core Code

self.renderer = renderer
```

```text
Benefit
→ Shape and Renderer vary independently
```

---

# Key Takeaways

- **Bridge is a structural pattern, not a creational pattern.**
- **It separates abstraction from implementation.**
- **Both sides can evolve independently.**
- **It is especially useful when two dimensions would otherwise create many subclasses.**
- **In your example, Shape is the abstraction and Renderer is the implementation hierarchy.**
- **`Circle` delegates rendering to its `Renderer`.**
- **Bridge relies heavily on composition: `Circle HAS-A Renderer`.**
- **Adding a renderer should not require creating a new Circle subclass.**
- **Adding a shape should not require combining it with every renderer through inheritance.**
- **Bridge is about independent variation; Adapter is about compatibility.**

# One-Line Revision

> **Bridge = when two dimensions vary independently, separate them into two hierarchies and connect them through composition instead of creating every possible inheritance combination.**