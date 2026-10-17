# Facade Design Pattern

Facade is a **structural design pattern**.

> **Facade provides a simple, high-level interface over a complex subsystem.**

Simple meaning:

> The system may contain many classes and internal interactions, but the client gets one easy entry point for common operations.

---

# Why Do We Need Facade?

Imagine a complex system containing:

```text
Subsystem A
Subsystem B
Subsystem C
Subsystem D
```

Without a Facade, the client may need to understand:

```text
Which subsystem to call?
In what order?
Which object depends on which?
What initialization is required?
```

That creates unnecessary complexity for the caller.

With Facade:

```text
Client
  ↓
Facade
  ↓
---------------------
|    |    |    |    |
A    B    C    D
```

The client interacts mainly with:

```text
Facade
```

while the Facade coordinates the subsystem.

---

# Real-World Analogy

Think about a house.

A house internally contains many systems:

```text
Electrical System
Plumbing
Heating
Ventilation
Security
Networking
```

The homeowner usually does not need to understand every wire and pipe.

Instead, they interact with simple controls:

```text
Light Switch
Thermostat
Water Tap
Security Panel
```

These controls behave like Facades.

They expose useful functionality while hiding internal complexity.

---

# Software Example

A software application may internally need:

```text
Authentication Service
Database
Cache
Message Queue
Payment Service
Logging
```

But an API consumer may simply want:

```python
checkout(order)
```

Instead of:

```text
authenticate()
check_inventory()
reserve_stock()
charge_payment()
save_order()
publish_event()
send_notification()
```

The Facade can coordinate those operations internally.

---

# Core Idea

Without Facade:

```text
Client
 ↓
Subsystem A
 ↓
Subsystem B
 ↓
Subsystem C
 ↓
Subsystem D
```

Client knows too much.

With Facade:

```text
Client
  ↓
Facade
  ↓
Complex Subsystem
```

The client gets a simpler API.

---

# Console Example

Suppose we are building a console system.

Internally it contains:

```text
Console
├── Buffer
└── Viewport
```

The client should not need to manually manage:

- Buffer memory
- Viewport offsets
- Active buffers
- Character lookup

for simple operations such as:

```text
write text
```

So `Console` acts as the Facade.

---

# Buffer

The Buffer stores characters.

```python
class Buffer:
    def __init__(self, width=30, height=20):
        self.width = width
        self.height = height
        self.buffer = [" "] * (
            width * height
        )

    def __getitem__(self, item):
        return self.buffer[item]

    def write(self, text):
        self.buffer.extend(text)
```

The responsibility of `Buffer` is:

```text
Store characters
```

It knows:

- Width
- Height
- Character storage

The client should not necessarily need to manipulate this directly.

---

# Viewport

A Viewport represents a view into a Buffer.

```python
class Viewport:
    def __init__(self, buffer=None):
        self.buffer = (
            buffer
            if buffer is not None
            else Buffer()
        )

        self.offset = 0

    def get_char_at(self, index):
        return self.buffer[
            self.offset + index
        ]
```

The Viewport handles:

```text
Which part of the buffer
is currently visible?
```

Conceptually:

```text
Large Buffer
──────────────────────────

        Viewport
        ↓↓↓↓↓↓↓
      [visible area]
```

---

# Console — The Facade

```python
class Console:
    def __init__(self):
        buffer = Buffer()

        self.current_viewport = (
            Viewport(buffer)
        )

        self.buffers = [buffer]

        self.viewports = [
            self.current_viewport
        ]

    def write(self, text):
        self.current_viewport \
            .buffer \
            .write(text)

    def get_char_at(self, index):
        return (
            self.current_viewport
            .get_char_at(index)
        )
```

`Console` provides the simple interface.

---

# Client Usage

The client can simply do:

```python
console = Console()

console.write("hello")

character = console.get_char_at(0)
```

The caller does not need to know:

```text
Create Buffer
Create Viewport
Connect Viewport to Buffer
Find current viewport
Find its current buffer
Calculate offset
```

The Facade handles that complexity.

---

# Without Facade

The client might need something like:

```python
buffer = Buffer()

viewport = Viewport(buffer)

buffer.write("hello")

character = viewport.get_char_at(0)
```

For a tiny example this does not look difficult.

But imagine the real implementation also includes:

```text
Multiple Buffers
Multiple Viewports
Scrolling
Window Management
Rendering
Cursor Handling
Terminal State
```

Then the complexity grows significantly.

---

# With Facade

The client gets:

```python
console.write("hello")
```

instead of knowing the internal object graph.

That is the value of the Facade.

---

# High-Level vs Low-Level API

A Facade usually exposes high-level operations.

For example:

```python
console.write("hello")
```

is high-level.

Internally it performs:

```text
Console
   ↓
Current Viewport
   ↓
Buffer
   ↓
write()
```

The client does not need to know this chain.

---

# Can Facade Expose Lower-Level Operations?

Yes.

Facade does not mean:

> Hide absolutely everything.

A Facade can expose both:

```text
Simple Common Operations
+
Some Advanced Operations
```

when needed.

The main purpose is:

> Provide a convenient simplified path for common use cases.

---

# Important Point

Facade does **not remove the subsystem**.

The complex classes still exist.

```text
Facade
 ↓
-----------------
Buffer
Viewport
Other Components
```

Advanced users may still interact directly with subsystem objects if the design allows it.

Facade simply provides an easier entry point.

---

# Facade Structure

Classic structure:

```text
            Client
              ↓
            Facade
              ↓
      -----------------
      |       |       |
Subsystem A   B       C
```

The Facade knows how to coordinate the subsystem.

The client knows mainly about the Facade.

---

# What Problem Does Facade Solve?

Imagine an API consumer needs to understand:

```text
10 internal classes
15 initialization steps
5 dependencies
```

just to perform one operation.

That is poor usability.

Facade turns:

```text
Complex Internal Workflow
```

into something like:

```python
system.start()
```

or:

```python
payment.checkout(order)
```

or:

```python
console.write("hello")
```

---

# Real-World Backend Example

Suppose an order system internally contains:

```text
InventoryService
PaymentService
OrderRepository
NotificationService
EventPublisher
```

Without Facade:

```python
inventory.reserve(...)
payment.charge(...)
repository.save(...)
publisher.publish(...)
notification.send(...)
```

The caller has to understand the workflow.

With Facade:

```python
order_facade.place_order(order)
```

Internally:

```text
place_order()
     ↓
Reserve Inventory
     ↓
Charge Payment
     ↓
Save Order
     ↓
Publish Event
     ↓
Send Notification
```

The client only needs one meaningful operation.

---

# Another Example — Video Processing

Internal subsystem:

```text
VideoDecoder
AudioDecoder
Codec
Compressor
FileReader
Muxer
```

Client wants:

```python
video_converter.convert(
    "movie.mp4"
)
```

`VideoConverter` acts as the Facade.

---

# Why Facade Helps

Facade improves:

- Usability
- Readability
- Encapsulation
- Separation between client and subsystem
- Reduced coupling
- Easier subsystem evolution

---

# Reduced Coupling

Without Facade:

```text
Client
├── Buffer
├── Viewport
├── Renderer
└── Window
```

Client depends on many internal classes.

With Facade:

```text
Client
   ↓
Console
```

Now internal implementation can change more easily.

---

# Facade and SRP

Facade itself has a specific responsibility:

> Provide a simplified entry point to subsystem functionality.

The subsystem classes still maintain their own responsibilities.

Example:

```text
Buffer
→ Character storage

Viewport
→ Viewing portion of Buffer

Console
→ Simplified interface
```

---

# Facade and OCP

If internal subsystem implementation changes:

```text
Old Buffer
    ↓
New Buffer Implementation
```

the client may not need to change as long as the Facade API remains stable.

This helps isolate changes.

---

# Facade vs Adapter

These are easy to confuse.

## Adapter

Problem:

> Two interfaces are incompatible.

```text
Interface A
   ↓
Adapter
   ↓
Interface B
```

Purpose:

```text
Compatibility
```

---

## Facade

Problem:

> The subsystem interface is too complicated.

```text
Complex Subsystem
       ↓
     Facade
       ↓
Simple Interface
```

Purpose:

```text
Simplicity
```

Easy revision:

```text
Adapter
→ Make incompatible interfaces work together

Facade
→ Make complicated interfaces easier to use
```

---

# Facade vs Decorator

## Decorator

Adds behavior to an object.

```text
Object
 ↓
Decorator
 ↓
Extra Behavior
```

## Facade

Simplifies access to a subsystem.

```text
Subsystem
 ↓
Facade
 ↓
Simple API
```

Easy revision:

```text
Decorator
→ Enhancement

Facade
→ Simplification
```

---

# Facade vs Bridge

## Bridge

Separates two independently varying hierarchies.

```text
Abstraction
↔
Implementation
```

## Facade

Creates one simple interface over complexity.

```text
Client
 ↓
Facade
 ↓
Subsystem
```

---

# Facade vs Proxy

## Proxy

Usually represents another object and controls access to it.

```text
Client
 ↓
Proxy
 ↓
Real Object
```

## Facade

Usually represents an entire subsystem.

```text
Client
 ↓
Facade
 ↓
Many Subsystem Components
```

---

# When to Use Facade

Use Facade when:

- Subsystem has many classes
- Common operations require many steps
- Clients should not understand internal details
- You want a clean public API
- You want to isolate clients from subsystem changes
- Third-party/library API is overly complicated

---

# When Not to Use Facade

Do not create a Facade if:

```text
Subsystem is already simple
```

or if the Facade becomes:

```text
One giant class containing every operation
```

A Facade should simplify access, not become another God Object.

---

# Important Facade Design Rule

A Facade should:

```text
Coordinate subsystem objects
```

but should generally avoid absorbing all subsystem business logic.

Bad:

```text
Facade
├── Every business rule
├── Every database operation
├── Every calculation
├── Every validation
└── Every subsystem detail
```

Then the Facade becomes another overly large class.

Better:

```text
Facade
→ Coordinate

Subsystem Classes
→ Perform actual specialized work
```

---

# Interview Question

## What is the Facade Pattern?

Facade is a structural design pattern that provides a simplified interface to a complex subsystem.

For example, a console may internally contain Buffers, Viewports, rendering logic, and state management.

Instead of requiring the client to interact with all these objects, we expose a `Console` Facade:

```python
console.write("hello")
```

The Facade coordinates the underlying components internally.

This reduces coupling and makes the subsystem easier to use.

---

# How to Recognize Facade

Look for the situation:

> "The subsystem works, but clients need to understand too many internal classes just to perform simple tasks."

Then:

```text
Complex Subsystem
       ↓
     Facade
       ↓
Simple Client API
```

may be appropriate.

---

# Mental Model

Think of a restaurant.

As a customer you say:

```text
"I want this meal."
```

You do not coordinate:

```text
Chef
Waiter
Inventory
Kitchen
Billing
Cleaning
```

The front-facing service hides that complexity.

That is the Facade idea.

---

# Quick Revision

```text
Facade
→ Structural Design Pattern
```

```text
Problem
→ Complex subsystem
```

```text
Solution
→ Simple high-level interface
```

```text
Client
 ↓
Facade
 ↓
Subsystems
```

```text
Our Example

Client
 ↓
Console
 ↓
Viewport
 ↓
Buffer
```

```text
Adapter
→ Compatibility
```

```text
Facade
→ Simplicity
```

```text
Decorator
→ Add behavior
```

```text
Benefit
→ Lower coupling
→ Easier API
→ Hide complexity
```

---

# Key Takeaways

- **Facade is a structural design pattern.**
- **It provides a simpler interface over one or more complex subsystem components.**
- **The subsystem itself is not removed; the Facade hides unnecessary details from common clients.**
- **In your example, `Console` acts as the Facade over `Buffer` and `Viewport`.**
- **Clients can call `console.write()` instead of manually coordinating Buffer and Viewport objects.**
- **Facade reduces coupling between clients and internal subsystem classes.**
- **Facade can expose some advanced functionality when necessary; it does not have to hide everything.**
- **Adapter solves incompatibility; Facade solves complexity.**
- **Decorator adds behavior; Facade simplifies interaction.**
- **A Facade should coordinate subsystem behavior rather than becoming a God Object itself.**

# One-Line Revision

> **Facade = put a simple front door in front of a complex subsystem so clients can use its main functionality without understanding all the internal components.**