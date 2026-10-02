# Dependency Inversion Principle — DIP

DIP is the fifth principle of **SOLID**.

It states:

> **High-level modules should not depend on low-level modules. Both should depend on abstractions.**

And:

> **Abstractions should not depend on implementation details. Implementation details should depend on abstractions.**

Simple meaning:

> Depend on an interface/contract instead of directly depending on a concrete implementation.

---

# High-Level vs Low-Level Module

## High-Level Module

Contains business rules or application policy.

Example:

```text
Research
→ Find John's children
```

It should care about:

> What information it needs.

It should not care about:

> How relationships are internally stored.

---

## Low-Level Module

Handles implementation details.

Example:

```text
Relationships
→ Stores relationships in a Python list
```

Later it could store them in:

```text
Database
Graph
API
Dictionary
File
```

These are implementation details.

---

# Example

We have:

```python
from enum import Enum


class Relationship(Enum):
    PARENT = 0
    CHILD = 1
    SIBLING = 2


class Person:
    def __init__(self, name):
        self.name = name
```

The `Person` class represents a person.

The `Relationship` enum represents the relationship type.

---

# Low-Level Module

```python
class Relationships:
    def __init__(self):
        self.relations = []

    def add_parent_and_child(self, parent, child):
        self.relations.append(
            (parent, Relationship.PARENT, child)
        )

        self.relations.append(
            (child, Relationship.CHILD, parent)
        )
```

Internally:

```text
Relationships
      ↓
Python List

[
    (John, PARENT, Chris),
    (Chris, CHILD, John)
]
```

This data structure is an implementation detail.

---

# Bad Design

Suppose `Research` directly accesses:

```python
relationships.relations
```

Example:

```python
class Research:
    def __init__(self, relationships):
        relations = relationships.relations

        for relation in relations:
            if (
                relation[0].name == "John"
                and relation[1] == Relationship.PARENT
            ):
                print(
                    f"John has child called "
                    f"{relation[2].name}"
                )
```

This creates a dependency like:

```text
Research
   ↓
Relationships
   ↓
Internal Python List
```

The high-level module knows too much about the low-level implementation.

---

# Why Is This a Problem?

`Research` assumes that relationships are stored as:

```text
List of tuples
```

and that each tuple looks like:

```text
(Person, Relationship, Person)
```

Suppose tomorrow we change `Relationships` to use:

```text
Dictionary
```

or:

```text
Database
```

or:

```text
Graph Database
```

Then `Research` may break.

Example:

```text
Old:

relationships.relations
→ List
```

New:

```text
relationships
→ Database
```

Now the high-level module must also change.

That creates:

> **Tight Coupling**

---

# Dependency Direction — Bad

```text
High-Level Module

Research
   ↓
Low-Level Module

Relationships
   ↓
List Implementation
```

The business logic depends directly on implementation details.

This violates DIP.

---

# Better Design — Introduce an Abstraction

Create an abstraction that describes what the high-level module needs.

```python
from abc import ABC, abstractmethod


class RelationshipBrowser(ABC):

    @abstractmethod
    def find_all_children_of(self, name):
        pass
```

This interface says:

> Any relationship storage system that can find children should provide this operation.

Notice that it says nothing about:

- Lists
- Tuples
- Databases
- Graphs

It only describes the required behavior.

---

# Low-Level Module Implements the Abstraction

```python
class Relationships(RelationshipBrowser):
    def __init__(self):
        self.relations = []

    def add_parent_and_child(self, parent, child):
        self.relations.append(
            (parent, Relationship.PARENT, child)
        )

        self.relations.append(
            (child, Relationship.CHILD, parent)
        )

    def find_all_children_of(self, name):
        for relation in self.relations:
            if (
                relation[0].name == name
                and relation[1] == Relationship.PARENT
            ):
                yield relation[2].name
```

Now:

```text
Relationships
→ implements RelationshipBrowser
```

The implementation can still use a list internally.

But consumers do not need to know that.

---

# High-Level Module Depends on Abstraction

```python
class Research:
    def __init__(self, browser):
        for person in browser.find_all_children_of("John"):
            print(f"John has child called {person}.")
```

`Research` no longer accesses:

```python
browser.relations
```

It only uses:

```python
browser.find_all_children_of(...)
```

So its dependency is:

```text
Research
     ↓
RelationshipBrowser
```

rather than:

```text
Research
     ↓
Relationships
     ↓
List
```

---

# Final Dependency Structure

```text
            RelationshipBrowser
              ↑             ↑
              |             |
          Research     Relationships
        High-Level      Low-Level
```

Both depend on the abstraction.

More accurately:

```text
Research
   ↓
RelationshipBrowser
   ↑
Relationships
```

The implementation dependency points toward the abstraction.

This is why it is called:

> **Dependency Inversion**

---

# What Was Inverted?

Before:

```text
High-Level
    ↓
Low-Level
```

After:

```text
High-Level
    ↓
Abstraction
    ↑
Low-Level
```

The low-level implementation now conforms to an abstraction required by the higher-level policy.

---

# Why Is This Better?

Suppose we create:

```python
class DatabaseRelationships(RelationshipBrowser):
    def find_all_children_of(self, name):
        # query database
        pass
```

Now we can use:

```python
Research(DatabaseRelationships())
```

without changing `Research`.

Or:

```python
class GraphRelationships(RelationshipBrowser):
    def find_all_children_of(self, name):
        # graph database lookup
        pass
```

Then:

```python
Research(GraphRelationships())
```

Again:

```text
Research unchanged ✅
```

---

# Swappable Implementations

DIP allows:

```text
RelationshipBrowser
       ↓
--------------------------
|            |           |
List       Database     Graph
Storage     Storage     Storage
```

The high-level code works against the same contract.

This improves:

- Flexibility
- Maintainability
- Testability
- Loose coupling

---

# Dependency Injection

DIP and Dependency Injection are related, but they are not the same thing.

## Dependency Inversion Principle

A **design principle**.

It says:

> Depend on abstractions rather than concrete implementations.

---

## Dependency Injection

A **technique** for providing dependencies from outside.

Your code:

```python
class Research:
    def __init__(self, browser):
        self.browser = browser
```

The dependency is passed in:

```python
Research(relationships)
```

instead of being created internally:

```python
class Research:
    def __init__(self):
        self.browser = Relationships()
```

This is **constructor injection**.

---

# Bad Dependency Creation

```python
class Research:
    def __init__(self):
        self.browser = Relationships()
```

Now:

```text
Research
→ explicitly knows Relationships
```

It is tightly coupled.

---

# Better

```python
class Research:
    def __init__(self, browser):
        self.browser = browser
```

Now callers decide what implementation to provide.

Example:

```python
Research(list_relationships)
```

or:

```python
Research(database_relationships)
```

---

# Why Dependency Injection Helps Testing

Suppose `Relationships` uses a real database.

Testing:

```text
Research
   ↓
Production Database
```

would be slow and inconvenient.

With an abstraction, we can create:

```python
class FakeRelationshipBrowser(RelationshipBrowser):
    def find_all_children_of(self, name):
        return ["Chris", "Matt"]
```

Then:

```python
Research(FakeRelationshipBrowser())
```

Now tests do not require the real database.

This makes code easier to test.

---

# Real-World Example — Notification System

Bad:

```python
class OrderService:
    def __init__(self):
        self.email_service = GmailService()
```

Now:

```text
OrderService
   ↓
GmailService
```

If we move to another provider, `OrderService` changes.

---

# Better

Create:

```text
NotificationSender
```

Then:

```text
             NotificationSender
                  ↑
          ------------------
          |                |
      GmailSender      SESNotification
```

`OrderService` depends on:

```text
NotificationSender
```

not Gmail.

Now providers can be swapped without changing business logic.

---

# Another Real-World Example — Database

Bad:

```python
class UserService:
    def __init__(self):
        self.db = PostgreSQLDatabase()
```

Strong dependency:

```text
UserService
    ↓
PostgreSQL
```

Better:

```text
UserRepository
```

Then:

```text
UserService
     ↓
UserRepository
     ↑
----------------------
|          |         |
Postgres   Mongo    Fake
```

Business logic does not care where users are stored.

---

# DIP and Layers

A common architecture:

```text
Controller
   ↓
Service
   ↓
Repository Interface
   ↑
Database Repository
```

The service depends on:

```text
Repository Interface
```

not directly on:

```text
PostgreSQL / MongoDB
```

This makes infrastructure replaceable.

---

# Important DIP Clarification

DIP does not mean:

> Every class needs an interface.

Creating abstractions everywhere can create unnecessary complexity.

Use an abstraction when:

- Implementation may change
- Multiple implementations exist
- External dependency should be isolated
- Testing requires substitution
- High-level policy should not know infrastructure details

---

# High-Level Policy Should Own the Abstraction

A useful deeper idea is:

> The abstraction should represent what the high-level module needs, not expose every detail of the low-level implementation.

Bad abstraction:

```text
RelationshipStorage

get_internal_tuple_list()
```

This still leaks implementation details.

Better:

```text
RelationshipBrowser

find_all_children_of(name)
```

The abstraction expresses a meaningful business operation.

---

# How to Identify DIP Violation

Look for high-level business classes doing things like:

```python
self.db = PostgreSQL()
```

```python
self.email = GmailService()
```

```python
self.storage = S3Client()
```

or directly reading implementation internals:

```python
relationships.relations
```

Ask:

> If I replace this implementation, how much business logic must change?

If many high-level classes change, coupling is probably too strong.

---

# Interview Question

## What is the Dependency Inversion Principle?

DIP states:

> **High-level modules should not depend on low-level modules. Both should depend on abstractions.**

Also:

> **Abstractions should not depend on details; details should depend on abstractions.**

For example, a `Research` class should not directly know that relationships are stored in a Python list.

Instead, it depends on a `RelationshipBrowser` abstraction exposing:

```text
find_all_children_of()
```

The concrete `Relationships` implementation implements that abstraction.

This allows the storage implementation to change without modifying the high-level business logic.

---

# DIP vs Dependency Injection

```text
Dependency Inversion
→ Design Principle
```

```text
Dependency Injection
→ Technique
```

DIP says:

```text
Depend on abstraction
```

DI helps achieve that by:

```text
Providing dependency from outside
```

---

# DIP vs OCP

They often work together.

## OCP

```text
Add new implementation
without changing existing business logic
```

## DIP

```text
Business logic depends on abstraction
rather than concrete implementation
```

Example:

```text
PaymentProcessor
      ↑
------------------------
Stripe      PayPal     UPI
```

DIP gives the abstraction.

OCP allows another payment provider to be added without changing core business logic.

---

# DIP vs ISP

## ISP

Focus:

```text
Keep interfaces focused.
```

## DIP

Focus:

```text
Depend on those abstractions rather than concrete details.
```

For example:

```text
RelationshipBrowser
```

should expose only the behavior the high-level client actually needs.

That also connects with ISP.

---

# Complete Example

```python
from abc import ABC, abstractmethod
from enum import Enum


class Relationship(Enum):
    PARENT = 0
    CHILD = 1
    SIBLING = 2


class Person:
    def __init__(self, name):
        self.name = name


class RelationshipBrowser(ABC):
    @abstractmethod
    def find_all_children_of(self, name):
        pass


class Relationships(RelationshipBrowser):
    def __init__(self):
        self.relations = []

    def add_parent_and_child(self, parent, child):
        self.relations.append(
            (parent, Relationship.PARENT, child)
        )

        self.relations.append(
            (child, Relationship.CHILD, parent)
        )

    def find_all_children_of(self, name):
        for relation in self.relations:
            if (
                relation[0].name == name
                and relation[1] == Relationship.PARENT
            ):
                yield relation[2].name


class Research:
    def __init__(self, browser: RelationshipBrowser):
        for child in browser.find_all_children_of("John"):
            print(f"John has child called {child}.")


parent = Person("John")
child1 = Person("Chris")
child2 = Person("Matt")

relationships = Relationships()

relationships.add_parent_and_child(parent, child1)
relationships.add_parent_and_child(parent, child2)

Research(relationships)
```

---

# Quick Revision

```text
DIP
→ Dependency Inversion Principle
```

```text
High-Level Module
→ Business logic
```

```text
Low-Level Module
→ Implementation/infrastructure details
```

```text
Bad

High-Level
   ↓
Concrete Implementation
```

```text
Good

High-Level
   ↓
Abstraction
   ↑
Low-Level Implementation
```

```text
DIP
→ Depend on interfaces/contracts
→ Not concrete implementation details
```

```text
DI
→ Inject implementation from outside
```

```text
Benefit
→ Loose coupling
→ Easier testing
→ Swappable implementations
→ Easier maintenance
```

# Key Takeaways

- **High-level modules should not directly depend on low-level implementation details.**
- **Both high-level and low-level modules should depend on abstractions.**
- **Details should implement the abstraction rather than forcing high-level business logic to understand internal details.**
- **`Research` should depend on `RelationshipBrowser`, not on the internal `relations` list.**
- **Changing list storage to a database or graph should not require changing `Research`.**
- **Dependency Injection is one common technique used to supply the concrete implementation.**
- **DIP and DI are related but not the same thing.**
- **Interfaces should expose meaningful behavior rather than leaking implementation details.**
- **DIP improves testability because real implementations can be replaced with fakes or mocks.**
- **Not every class requires an abstraction; add one where decoupling provides real value.**

# One-Line Revision

> **DIP = high-level business logic depends on stable abstractions, while low-level infrastructure provides implementations of those abstractions.**