# Singleton Design Pattern

Singleton is a **creational design pattern**.

> **Singleton ensures that a class has only one instance and provides a common way to access that instance.**

Typical idea:

```text
First request
    ↓
Create instance
    ↓
Store instance

Later requests
    ↓
Return same instance
```

---

# Why Use Singleton?

Singleton can be useful when exactly one shared object should coordinate some process.

Examples may include:

- Application configuration
- Logging service
- In-memory registry
- Shared cache manager
- Resource manager

However, Singleton should be used carefully because it introduces **global shared state**.

---

# Core Requirement

Normally:

```python
a = SomeClass()
b = SomeClass()
```

creates two independent objects.

Singleton tries to make:

```python
a = Database()
b = Database()
```

such that:

```python
a is b
```

is:

```text
True
```

---

# Singleton vs Shared State

A real Singleton means:

```text
One Object Identity
+
Shared State
```

This is different from Monostate, where:

```text
Multiple Objects
+
Shared State
```

We will see this later.

---

# 1. Singleton Using `__new__`

In Python:

```python
__new__()
```

is responsible for **creating/allocating the object**.

`__init__()` is responsible for **initializing the already-created object**.

Therefore Singleton creation can be controlled through `__new__()`.

---

# Basic Implementation

```python
import random


class Database:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance
```

Flow:

```text
Database()
    ↓
_instance exists?
   /       \
 No         Yes
 ↓           ↓
Create      Return existing
 ↓
Store
 ↓
Return
```

---

# Usage

```python
d1 = Database()
d2 = Database()

print(d1 is d2)
```

Output:

```text
True
```

Both variables reference the same object.

```text
d1 ─────┐
        ↓
    Database Object
        ↑
d2 ─────┘
```

---

# Important Problem With `__init__`

Consider:

```python
class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):
        print("Initializing database")
```

Now:

```python
d1 = Database()
d2 = Database()
```

`__new__()` returns the same object.

But:

```text
__init__()
```

can still run on every constructor call.

So you may see:

```text
Initializing database
Initializing database
```

even though only one object exists.

---

# Corrected Initialization

Use an initialization guard:

```python
class Database:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.id = random.randint(1, 100)

        print(
            f"Database instance created "
            f"with id: {self.id}"
        )

        self._initialized = True
```

Now:

```python
d1 = Database()
d2 = Database()
```

results in:

```text
One allocation
One initialization
Same object returned twice
```

---

# Important Clarification

You do **not** normally prevent repeated initialization by raising an exception.

The usual behavior of a Singleton is:

```text
Database()
Database()
Database()
```

all return the same instance.

The caller should not need special knowledge that an object already exists.

---

# `is` vs `==`

For Singleton identity, prefer:

```python
d1 is d2
```

rather than:

```python
d1 == d2
```

Why?

```text
is
→ Same object identity
```

```text
==
→ Equality according to __eq__()
```

A class can override `__eq__()`, so `==` does not necessarily prove Singleton identity.

---

# 2. Singleton Decorator

Another approach is a decorator.

```python
def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(
                *args,
                **kwargs
            )

        return instances[cls]

    return get_instance
```

Apply:

```python
@singleton
class Database:
    def __init__(self):
        self.id = random.randint(1, 100)

        print(
            f"Database created: {self.id}"
        )
```

Usage:

```python
d1 = Database()
d2 = Database()

print(d1 is d2)
```

Result:

```text
True
```

---

# How the Decorator Works

Without decorator:

```text
Database
→ Class
```

With:

```python
@singleton
class Database:
    ...
```

the name `Database` effectively becomes the wrapper returned by:

```python
singleton(Database)
```

The wrapper maintains:

```python
instances
```

and returns the existing instance after the first creation.

---

# Decorator Advantages

- Simple
- Reusable
- Creation logic separated from class implementation

---

# Decorator Drawback

This simple implementation replaces the class name with a function.

Conceptually:

```text
Database
→ get_instance function
```

That may interfere with:

- Type inspection
- Inheritance
- `isinstance()` expectations
- Some frameworks

So although useful for learning, it is not always the cleanest production design.

---

# 3. Singleton Using a Metaclass

A **metaclass** controls how classes themselves behave.

When we write:

```python
Database()
```

Python normally invokes the class's metaclass:

```python
__call__()
```

Therefore we can intercept object creation there.

---

# Singleton Metaclass

```python
class SingletonMeta(type):
    _instances = {}

    def __call__(
        cls,
        *args,
        **kwargs
    ):
        if cls not in cls._instances:

            instance = super().__call__(
                *args,
                **kwargs
            )

            cls._instances[cls] = instance

        return cls._instances[cls]
```

Then:

```python
class Database(
    metaclass=SingletonMeta
):
    def __init__(self):
        self.id = random.randint(1, 100)

        print(
            f"Database created: {self.id}"
        )
```

Usage:

```python
d1 = Database()
d2 = Database()

print(d1 is d2)
```

Output:

```text
True
```

---

# Why Metaclass Version Avoids Repeated `__init__`

The important code is:

```python
if cls not in cls._instances:
    instance = super().__call__()
```

`super().__call__()` performs:

```text
__new__()
+
__init__()
```

But it is only executed the first time.

Later calls immediately return:

```python
cls._instances[cls]
```

Therefore:

```text
First Database()
→ __new__ + __init__

Second Database()
→ Return existing object
```

---

# Metaclass Structure

```text
Database()
    ↓
SingletonMeta.__call__()
    ↓
Instance exists?
   /       \
 No         Yes
 ↓           ↓
Create      Return
Store       existing
Return
```

---

# Why Metaclass Can Be Cleaner

Advantages:

- Class remains a real class
- Reusable across multiple Singleton classes
- Centralizes Singleton logic
- `__init__` runs only during actual creation

Trade-off:

> Metaclasses are more advanced and can make code harder to understand.

Use them only when the abstraction provides real value.

---

# 4. Monostate / Borg Pattern

Monostate takes a different approach.

It does **not** guarantee one object.

Instead:

> Multiple objects share the same state.

Example:

```python
class CEO:
    _shared_state = {
        "name": "Steve",
        "age": 55
    }

    def __init__(self):
        self.__dict__ = self._shared_state
```

Now:

```python
ceo1 = CEO()
ceo2 = CEO()
```

creates:

```text
CEO Object 1
CEO Object 2
```

but:

```text
Both use same __dict__
```

---

# Shared State

Conceptually:

```text
CEO 1 ─────┐
           ↓
      Shared State
           ↑
CEO 2 ─────┘
```

If:

```python
ceo1.name = "John"
```

then:

```python
print(ceo2.name)
```

will also show:

```text
John
```

because their state is shared.

---

# Important Correction

This:

```python
print(ceo1 == ceo2)
```

will normally produce:

```text
False
```

unless you implement a custom `__eq__()`.

Why?

Because:

```text
ceo1
```

and:

```text
ceo2
```

are two different objects.

Therefore:

```python
ceo1 is ceo2
```

is:

```text
False
```

But:

```python
ceo1.__dict__ is ceo2.__dict__
```

is:

```text
True
```

---

# Monostate Base Class

```python
class Monostate:
    _shared_state = {}

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)

        obj.__dict__ = (
            cls._shared_state
        )

        return obj
```

Then:

```python
class CFO(Monostate):
    def __init__(self):
        self.name = ""
        self.money_managed = 0
```

Different `CFO` objects share state.

---

# Potential Problem With `CFO`

Consider:

```python
cfo1 = CFO()
cfo1.name = "Bill"
cfo1.money_managed = 35
```

Then:

```python
cfo2 = CFO()
```

But `CFO.__init__()` runs again:

```python
self.name = ""
self.money_managed = 0
```

Because state is shared, constructing `cfo2` can reset the values seen through `cfo1`.

Then:

```python
cfo2.name = "Ruth"
```

also changes:

```python
cfo1.name
```

because both share state.

This can be surprising and is one reason Monostate should be used carefully.

---

# Singleton vs Monostate

## Singleton

```text
One instance
+
One state
```

Example:

```text
d1 ──┐
     ↓
 Database
     ↑
d2 ──┘
```

---

## Monostate

```text
Many instances
+
One shared state
```

Example:

```text
Object A ──┐
           ↓
      Shared State
           ↑
Object B ──┘
```

---

# Singleton vs Monostate Table

| Singleton | Monostate |
|---|---|
| One object | Multiple objects |
| Same identity | Different identities |
| Shared state naturally | State manually shared |
| `a is b` → True | `a is b` → False |
| Controls construction | Controls object state |

---

# Thread Safety

A basic Singleton implementation can have a race condition.

Imagine two threads execute simultaneously:

```text
Thread A
→ instance is None

Thread B
→ instance is None
```

Both may attempt to create the object.

Conceptually:

```text
Thread A ──┐
           ├── Create instance
Thread B ──┘
```

This can violate Singleton guarantees.

A thread-safe implementation may require:

- Locking
- Language/runtime-specific synchronization
- Eager initialization

depending on the environment.

---

# Singleton Scope

Another important interview point:

> A Singleton normally guarantees one instance only within one process/runtime.

Suppose:

```text
Server 1 → Process A
Server 2 → Process B
Server 3 → Process C
```

Each process can have its own Singleton.

So:

```text
Singleton ≠ one instance across an entire distributed system
```

If you require globally coordinated uniqueness across machines, you need distributed coordination mechanisms such as:

- Distributed locks
- Leader election
- Database coordination
- Consensus systems

depending on the problem.

---

# Singleton Problems

Singleton is commonly criticized because it can behave like global state.

Possible problems:

- Hidden dependencies
- Difficult unit testing
- Tight coupling
- Shared mutable state
- Harder parallel tests
- Lifecycle management issues
- Concurrency problems

Example:

```python
class UserService:
    def save(self):
        Database()
```

The dependency on `Database` is hidden inside the service.

---

# Better Testable Design

Instead:

```python
class UserService:
    def __init__(self, database):
        self.database = database
```

Now production can provide:

```text
Real Database
```

while tests can provide:

```text
Fake Database
```

This is Dependency Injection.

---

# Singleton and Dependency Injection

Singleton and DI are not opposites.

A dependency container may create:

```text
One Logger
One Configuration
One Database Pool
```

and inject the same instance wherever needed.

Conceptually:

```text
Application Container
      ↓
Create one instance
      ↓
-------------------------
|           |           |
Service A  Service B   Service C
```

This often gives Singleton-like lifetime behavior without every class knowing about a global Singleton.

---

# Database Singleton — Important Practical Note

The example:

```text
Database
→ Singleton
```

is commonly used to teach the pattern.

But in real applications, you usually do **not** want one literal database connection globally.

Instead, applications often use:

```text
Connection Pool
```

containing multiple reusable DB connections.

You might have one shared:

```text
Database client / connection pool manager
```

but many underlying connections.

---

# When Singleton Can Be Appropriate

Possible cases:

- Immutable application configuration
- Logging infrastructure
- Shared registry
- Dependency container-managed shared service
- Resource manager with clearly defined application-wide lifetime

Use it when:

> There is a real architectural requirement for one shared instance.

Not merely because:

> "It is convenient to access globally."

---

# When to Avoid Singleton

Avoid or reconsider it when:

- Different instances may be needed later
- Tests need isolated dependencies
- Shared mutable state creates problems
- The dependency can simply be injected
- Object lifetime should be controlled externally
- Distributed uniqueness is actually required

---

# Singleton Implementations in Your Examples

## `__new__`

```text
Control object allocation directly
```

Pros:

- Easy to understand

Watch out:

- `__init__` can run repeatedly

---

## Decorator

```text
Wrap object creation
```

Pros:

- Reusable
- Concise

Watch out:

- Simple implementation replaces class name with a function

---

## Metaclass

```text
Control Class.__call__()
```

Pros:

- Reusable
- Class remains a class
- Centralized creation logic

Watch out:

- More advanced/complex

---

## Monostate

```text
Share state rather than identity
```

It is:

> **Not technically the same as Singleton.**

---

# Interview Question

## What is the Singleton Pattern?

Singleton is a creational design pattern that ensures a class has only one instance and provides controlled access to that instance.

For example, the first call to:

```python
Database()
```

creates the instance.

Subsequent calls return the same instance rather than creating another one.

Singleton can be implemented in Python using:

- `__new__`
- Decorators
- Metaclasses

However, it should be used carefully because it introduces shared global state and can make testing and dependency management harder.

---

# How Would You Implement Singleton in Python?

A simple approach:

```python
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = (
                super().__new__(cls)
            )

        return cls._instance
```

Then:

```python
a = Singleton()
b = Singleton()

print(a is b)
```

Output:

```text
True
```

For real use, initialization and thread safety must also be considered.

---

# Singleton vs Static Class

A Singleton:

```text
Is an actual object
```

so it can:

- Implement interfaces
- Be passed as a dependency
- Maintain instance state
- Potentially participate in inheritance

A collection of static methods is simply:

```text
Class-level functionality
```

They solve different design problems.

---

# Singleton vs Factory

## Factory

Controls:

```text
How objects are created
```

It may create many objects.

## Singleton

Controls:

```text
How many instances exist
```

A factory itself could even return the same Singleton instance every time.

---

# Singleton vs Prototype

```text
Singleton
→ Prevent multiple instances
```

```text
Prototype
→ Intentionally create multiple objects by cloning
```

They solve almost opposite object-creation goals.

---

# Quick Revision

```text
Singleton
→ Creational Design Pattern
```

```text
Goal
→ One instance per intended scope
```

```text
__new__
→ Controls object allocation
```

```text
__init__
→ Initializes object
→ May run repeatedly with basic __new__ Singleton
```

```text
Metaclass
→ Intercept class creation calls
```

```text
Decorator
→ Wrap class construction
```

```text
Monostate
→ Multiple objects
→ Shared state
→ Not true Singleton identity
```

```text
Important
→ Use `is` to check same object
```

```text
Distributed System
→ Process-level Singleton is not global Singleton
```

---

# Key Takeaways

- **Singleton is a creational design pattern that restricts a class to one instance within its defined scope.**
- **`__new__()` controls object creation, while `__init__()` performs initialization.**
- **A basic `__new__` Singleton must guard against repeated `__init__()` calls when that matters.**
- **Use `a is b` to verify that two references point to the same Singleton instance.**
- **A decorator can implement Singleton but may change the class's normal type behavior.**
- **A metaclass can centralize Singleton instance management cleanly.**
- **Monostate/Borg shares state but still creates multiple objects; it is not a true identity-based Singleton.**
- **Singleton implementations must consider thread safety.**
- **A Singleton is normally one instance per process, not one instance across an entire distributed system.**
- **Singleton can introduce global state, hidden dependencies, and testing difficulties.**
- **Dependency Injection can often provide a shared application-wide instance with clearer dependency management.**

# One-Line Revision

> **Singleton = ensure one object instance exists within a defined scope and return that same instance whenever it is requested.**