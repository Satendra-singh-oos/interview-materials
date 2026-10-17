# Factory Pattern

Factory is a **creational design pattern**.

> **Factory encapsulates object-creation logic so the client does not need to know exactly how an object is constructed.**

Instead of:

```python
obj = SomeConcreteClass(...)
```

the client can use:

```python
obj = factory.create(...)
```

The factory decides:

- Which object to create
- How to initialize it
- What additional creation logic is required

---

# Why Do We Need Factories?

Constructors such as:

```python
__init__()
```

have limitations.

For example:

- Constructor name is always `__init__`
- Constructor intent may not be obvious
- Python does not support constructor overloading like separate named constructors
- Too many optional parameters can create confusing construction logic
- Complex initialization can make the constructor difficult to understand

Example:

```python
Point(3, 4)
```

What does this mean?

```text
x = 3, y = 4?
```

or:

```text
rho = 3, theta = 4?
```

The constructor itself does not clearly communicate intent.

---

# Factory vs Builder

Both are creational patterns, but they solve different problems.

## Factory

Usually creates an object in one operation.

```text
Factory
→ Create complete object
```

## Builder

Constructs an object step by step.

```text
Builder
→ Step 1
→ Step 2
→ Step 3
→ Build
```

Simple revision:

> **Factory = wholesale object creation**

> **Builder = piecewise object construction**

---

# 1. Factory Method

A Factory Method is a method responsible for creating an object.

Instead of directly calling the constructor, we expose meaningful creation methods.

---

# Point Example

Suppose a point can be represented using:

```text
Cartesian Coordinates
→ x, y
```

or:

```text
Polar Coordinates
→ rho, theta
```

---

# Bad Constructor Design

We could write:

```python
class Point:
    def __init__(
        self,
        a,
        b,
        system=CoordinateSystem.CARTESIAN
    ):
        if system == CoordinateSystem.CARTESIAN:
            self.x = a
            self.y = b

        elif system == CoordinateSystem.POLAR:
            self.x = a * math.cos(b)
            self.y = a * math.sin(b)

        else:
            raise ValueError(
                "Invalid coordinate system"
            )
```

Usage:

```python
Point(
    5,
    math.pi / 4,
    CoordinateSystem.POLAR
)
```

Problem:

```text
What does a mean?
What does b mean?
```

The arguments are not descriptive.

---

# Better — Factory Methods

```python
import math


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point({self.x}, {self.y})"

    @staticmethod
    def new_cartesian_point(x, y):
        return Point(x, y)

    @staticmethod
    def new_polar_point(rho, theta):
        return Point(
            rho * math.cos(theta),
            rho * math.sin(theta)
        )
```

Now creation becomes explicit.

---

# Cartesian Point

```python
point = Point.new_cartesian_point(
    3,
    4
)
```

This clearly means:

```text
x = 3
y = 4
```

---

# Polar Point

```python
point = Point.new_polar_point(
    5,
    math.pi / 4
)
```

The factory converts:

```text
rho + theta
      ↓
Cartesian x + y
      ↓
Point
```

The client does not need to know the conversion logic.

---

# Why Factory Method Is Better Here

Compare:

```python
Point(
    5,
    math.pi / 4,
    CoordinateSystem.POLAR
)
```

with:

```python
Point.new_polar_point(
    5,
    math.pi / 4
)
```

The second communicates intent immediately.

---

# Factory Method Idea

```text
Client
   ↓
Factory Method
   ↓
Creation Logic
   ↓
Object
```

Factory methods can also:

- Validate input
- Apply defaults
- Select subclasses
- Perform transformations
- Configure dependencies

---

# 2. Separate Factory Class

Another option is moving object-creation logic into a separate Factory class.

This can improve separation of concerns.

Instead of:

```text
Point
├── Point behavior
└── Creation logic
```

we can have:

```text
Point
→ Represents point

PointFactory
→ Creates points
```

---

# Example

```python
class NewPoint:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point({self.x}, {self.y})"


class PointFactory:

    @staticmethod
    def new_cartesian_point(x, y):
        return NewPoint(x, y)

    @staticmethod
    def new_polar_point(rho, theta):
        return NewPoint(
            rho * math.cos(theta),
            rho * math.sin(theta)
        )
```

Usage:

```python
p1 = PointFactory.new_cartesian_point(
    3,
    4
)

p2 = PointFactory.new_polar_point(
    5,
    math.pi / 4
)
```

---

# Why Use a Separate Factory?

The object's responsibility becomes:

```text
Point
→ Represent a point
```

The factory's responsibility becomes:

```text
PointFactory
→ Know how to create points
```

This can help with:

- SRP
- Complex creation logic
- Multiple creation strategies
- Reusability

---

# Factory Method vs Factory Class

## Factory Method

Creation method exists on or near the class.

Example:

```python
Point.new_polar_point(...)
```

---

## Factory Class

A separate object/class handles creation.

Example:

```python
PointFactory.new_polar_point(...)
```

Simple revision:

```text
Factory Method
→ Method creates object

Factory Class
→ Dedicated class containing creation methods
```

---

# Nested Factory

Your example also shows a nested Factory:

```python
class NewPoint:
    class PointFactory:
        ...
```

Then:

```python
NewPoint.factory.new_cartesian_point(...)
```

This keeps the factory logically associated with `NewPoint`.

However, a normal separate `PointFactory` class is often simpler and easier to understand.

---

# Important Correction

This would fail:

```python
NewPoint(3, 4)
```

unless `NewPoint` defines:

```python
def __init__(self, x, y):
    ...
```

The factory can avoid direct construction by keeping creation controlled through the factory API.

---

# 3. Abstract Factory

Abstract Factory is another creational pattern.

The important definition is:

> **Abstract Factory provides an interface for creating related objects or families of objects without exposing their concrete classes to the client.**

It is more than simply:

> "Create different objects based on input."

The key idea is:

```text
Client depends on Factory Abstraction
        ↓
Different Concrete Factories
        ↓
Different Concrete Products
```

---

# Hot Drink Example

We have a common product abstraction:

```python
from abc import ABC, abstractmethod


class HotDrink(ABC):

    @abstractmethod
    def consume(self):
        pass
```

Concrete products:

```python
class Tea(HotDrink):
    def consume(self):
        print(
            "This tea is nice."
        )


class Coffee(HotDrink):
    def consume(self):
        print(
            "This coffee is delicious."
        )
```

Both satisfy:

```text
HotDrink
```

---

# Factory Abstraction

Now define a common factory interface:

```python
class HotDrinkFactory(ABC):

    @abstractmethod
    def prepare(self, amount):
        pass
```

Every drink factory must implement:

```text
prepare(amount)
```

---

# Tea Factory

```python
class TeaFactory(HotDrinkFactory):

    def prepare(self, amount):
        print(
            f"Put in tea bag, "
            f"boil water, pour {amount}ml."
        )

        return Tea()
```

---

# Coffee Factory

```python
class CoffeeFactory(
    HotDrinkFactory
):

    def prepare(self, amount):
        print(
            f"Grind beans, boil water, "
            f"pour {amount}ml."
        )

        return Coffee()
```

---

# Structure

```text
                HotDrink
               /        \
             Tea       Coffee


           HotDrinkFactory
             /         \
      TeaFactory     CoffeeFactory
```

The client can work against:

```text
HotDrinkFactory
```

instead of concrete creation logic.

---

# Simple Factory Function

We could write:

```python
def make_drink(drink_type):
    if drink_type == "tea":
        return TeaFactory().prepare(200)

    elif drink_type == "coffee":
        return CoffeeFactory().prepare(50)

    return None
```

This works for a small system.

But notice:

```text
Add Chocolate
      ↓
Modify make_drink()
```

Then:

```text
Add Green Tea
      ↓
Modify make_drink()
```

The function keeps changing.

This can become an OCP problem.

---

# HotDrinkMachine

A machine can work with factories rather than constructing drinks itself.

Conceptually:

```text
HotDrinkMachine
       ↓
Available Factories
       ↓
--------------------
|                  |
TeaFactory    CoffeeFactory
   ↓              ↓
 Tea           Coffee
```

---

# Better Factory Registration

Your original example used:

```python
eval(factory_name)
```

This is not a good production approach.

It is:

- Fragile
- Harder to refactor
- Potentially unsafe if uncontrolled input reaches it

A cleaner approach is explicit registration.

```python
class HotDrinkMachine:
    def __init__(self):
        self.factories = {
            "tea": TeaFactory(),
            "coffee": CoffeeFactory()
        }

    def make_drink(
        self,
        drink_type,
        amount
    ):
        factory = self.factories.get(
            drink_type
        )

        if factory is None:
            raise ValueError(
                "Unsupported drink type"
            )

        return factory.prepare(amount)
```

Usage:

```python
machine = HotDrinkMachine()

drink = machine.make_drink(
    "tea",
    200
)

drink.consume()
```

---

# Why Is This Better?

The machine delegates creation:

```text
Machine
  ↓
Factory
  ↓
Product
```

The machine itself does not know how tea or coffee is prepared.

It only knows:

```text
HotDrinkFactory
→ prepare()
```

---

# OCP Connection

Suppose we add:

```text
HotChocolate
```

Create:

```python
class HotChocolate(HotDrink):
    def consume(self):
        print("Drinking hot chocolate")


class HotChocolateFactory(
    HotDrinkFactory
):
    def prepare(self, amount):
        return HotChocolate()
```

Then register the factory:

```python
self.factories[
    "hot_chocolate"
] = HotChocolateFactory()
```

The core drink preparation logic remains unchanged.

---

# Abstract Factory — Important Concept

The classic Abstract Factory Pattern is especially useful when there are **families of related objects**.

Example:

```text
GUIFactory
   ↓
----------------------
|                    |
WindowsFactory    MacFactory
```

Each creates related components:

```text
WindowsFactory
├── WindowsButton
└── WindowsCheckbox
```

```text
MacFactory
├── MacButton
└── MacCheckbox
```

The client works with:

```text
Button
Checkbox
GUIFactory
```

without knowing whether the concrete family is Windows or macOS.

That is the strongest example of Abstract Factory.

---

# Factory Method vs Abstract Factory

## Factory Method

Usually creates one product through a method.

Example:

```python
Point.new_polar_point(...)
```

or conceptually:

```text
create_product()
```

---

## Abstract Factory

Provides an abstraction for creating one or more related product types.

Example:

```text
GUIFactory
├── create_button()
└── create_checkbox()
```

Concrete factories:

```text
WindowsFactory
MacFactory
```

---

# Factory Method vs Factory vs Abstract Factory

| Concept | Main Idea |
|---|---|
| Factory Method | A method encapsulates object creation |
| Factory Class | Dedicated class handles creation |
| Abstract Factory | Common factory abstraction creates related products/families |
| Builder | Constructs complex object step by step |

---

# Factory and SRP

Factory can help SRP because object creation is separated from object behavior.

Without Factory:

```text
Product
├── Business behavior
├── Validation
├── Configuration
└── Complex construction
```

With Factory:

```text
Product
→ Business behavior

Factory
→ Construction
```

---

# Factory and OCP

Factories can also help OCP.

Bad:

```python
if type == "tea":
    ...
elif type == "coffee":
    ...
elif type == "chocolate":
    ...
```

Every new product requires changing the same code.

Better:

```text
Factory Abstraction
       ↑
-------------------------
|           |           |
Tea       Coffee     Chocolate
Factory   Factory      Factory
```

New factories can extend the system.

---

# Factory and DIP

Client code can depend on:

```text
HotDrinkFactory
```

instead of:

```text
TeaFactory
CoffeeFactory
```

This reduces coupling to concrete implementations.

---

# When to Use Factory

Use Factory when:

- Object creation is complex
- Constructor intent is unclear
- Multiple creation paths exist
- The concrete implementation should be hidden
- Creation requires validation/transformation
- You may swap implementations
- Different subclasses/products may be created

---

# When Not to Use Factory

Do not create unnecessary Factory classes for simple construction.

If:

```python
User("John", 25)
```

is already clear and simple, a factory may add unnecessary abstraction.

---

# Real-World Example — Notification Factory

Suppose:

```text
Notification
├── Email
├── SMS
└── Push
```

Instead of:

```python
if type == "email":
    return EmailNotification()

elif type == "sms":
    return SMSNotification()
```

creation could be handled by a factory.

The rest of the system only works with:

```text
Notification
```

---

# Real-World Example — Database Connections

A factory may create:

```text
DatabaseConnection
       ↑
----------------------
|                    |
PostgreSQL       MongoDB
Connection       Connection
```

Client:

```text
DatabaseFactory.create(...)
```

The client does not need to understand connection initialization details.

---

# Interview Question

## What is the Factory Pattern?

Factory is a creational design pattern that encapsulates object creation.

Instead of directly invoking constructors throughout the application, the client asks a factory to create the object.

Factories are useful when creation:

- Is complex
- Requires additional logic
- Has multiple possible implementations
- Should be hidden from the client

---

# What Is Factory Method?

A Factory Method is a method that encapsulates object creation.

Example:

```python
Point.new_cartesian_point(...)
Point.new_polar_point(...)
```

The method name clearly describes how the object is being created.

---

# What Is Abstract Factory?

Abstract Factory provides:

> **A common interface for creating related products without depending on their concrete implementations.**

For example:

```text
GUIFactory
   ↓
WindowsFactory / MacFactory
```

can create:

```text
Button
Checkbox
```

for the selected platform.

---

# Factory vs Builder — Interview Answer

Factory:

```text
Usually creates the complete object
in one operation.
```

Builder:

```text
Constructs a complex object
step by step.
```

Example:

```text
Factory
→ Give me a Coffee object.
```

```text
Builder
→ Add CPU
→ Add RAM
→ Add Storage
→ Build PC
```

---

# Quick Revision

```text
Factory
→ Creational pattern
→ Encapsulates object creation
```

```text
Factory Method
→ Named method creates object
```

```text
Factory Class
→ Separate class responsible for creation
```

```text
Abstract Factory
→ Interface for creating related products/families
```

```text
Factory
→ Usually wholesale creation
```

```text
Builder
→ Piecewise / step-by-step creation
```

```text
Benefits
→ Clear creation intent
→ Lower coupling
→ Hide complex initialization
→ Easier extension
```

---

# Key Takeaways

- **Factory encapsulates object-creation logic.**
- **Factory Method is a named method that creates an object.**
- **Named factory methods can be clearer than ambiguous constructors.**
- **A Factory class moves creation responsibilities into a dedicated component.**
- **Factories can improve SRP by separating creation from object behavior.**
- **Abstract Factory is primarily about creating families of related objects through common factory abstractions.**
- **Factory and Builder are different: Factory usually creates the object at once; Builder constructs it step by step.**
- **Factories can help OCP and DIP by hiding concrete implementations behind abstractions.**
- **Avoid unsafe reflection techniques such as uncontrolled `eval()` when explicit registration is sufficient.**
- **Do not introduce a Factory when normal construction is already simple and expressive.**

# One-Line Revision

> **Factory = hide and centralize object-creation logic so clients ask for an object without needing to know exactly how that object is constructed.**