# Prototype Design Pattern

Prototype is a **creational design pattern**.

> **Prototype creates new objects by copying an existing object called the prototype.**

Instead of:

```text
Create object from scratch
        ↓
Initialize many properties
        ↓
Configure nested objects
```

we can do:

```text
Existing configured object
        ↓
Clone
        ↓
Modify required fields
        ↓
New object
```

Prototype is useful when object creation is:

- Expensive
- Complex
- Repetitive
- Contains many predefined values
- Contains nested objects
- Mostly similar to an existing object

---

# Basic Idea

Suppose we already have:

```text
John
 └── Address
      ├── 123 London Road
      ├── London
      └── UK
```

Now we want another very similar person.

Instead of constructing everything again:

```python
jane = Person(
    "Jane",
    Address(
        "123 London Road",
        "London",
        "UK"
    )
)
```

we can clone `John` and modify the fields that differ.

```text
John
  ↓
Clone
  ↓
Jane
```

---

# Example Classes

```python
class Address:
    def __init__(
        self,
        street_address,
        city,
        country,
        suite=None
    ):
        self.street_address = street_address
        self.city = city
        self.country = country
        self.suite = suite

    def __str__(self):
        return (
            f"Address("
            f"street_address={self.street_address}, "
            f"city={self.city}, "
            f"country={self.country}, "
            f"suite={self.suite})"
        )
```

```python
class Person:
    def __init__(self, name, address):
        self.name = name
        self.address = address

    def __str__(self):
        return (
            f"Person("
            f"name={self.name}, "
            f"address={self.address})"
        )
```

---

# Reference Assignment Is Not Copying

Suppose:

```python
john = Person(
    "John",
    Address(
        "123 London Road",
        "London",
        "UK"
    )
)

jane = john
```

This does **not** create a new object.

Instead:

```text
john ───────┐
            ↓
         Person Object
            ↑
jane ───────┘
```

Both variables reference the same object.

Now:

```python
jane.name = "Jane"
```

also changes what `john.name` sees.

Because:

```text
john is jane
```

is effectively:

```text
True
```

So:

> Assignment copies the reference, not the object.

---

# Shallow Copy

Python provides:

```python
copy.copy()
```

Example:

```python
import copy

jane = copy.copy(john)
```

This creates a new outer `Person` object.

Conceptually:

```text
john ──→ Person A ──┐
                    ↓
                 Address
                    ↑
jane ──→ Person B ──┘
```

The `Person` objects are different.

But the nested:

```text
Address
```

is still shared.

---

# Shallow Copy Example

```python
jane = copy.copy(john)

jane.name = "Jane"
```

This does not change `john.name`.

Good.

But:

```python
jane.address.street_address = (
    "456 Paris Street"
)
```

can also affect:

```python
john.address.street_address
```

because both people still reference the same Address object.

---

# Shallow Copy

Simple revision:

```text
Shallow Copy

Outer object
→ New copy

Nested mutable objects
→ Shared references
```

---

# Deep Copy

A deep copy recursively copies nested objects.

Python:

```python
copy.deepcopy()
```

Example:

```python
jane = copy.deepcopy(john)
```

Now:

```text
john
 ↓
Person A
 ↓
Address A
```

and:

```text
jane
 ↓
Person B
 ↓
Address B
```

Both Person and Address are separate objects.

---

# Deep Copy Example

```python
import copy


john = Person(
    "John",
    Address(
        "123 London Road",
        "London",
        "UK"
    )
)

jane = copy.deepcopy(john)

jane.name = "Jane"

jane.address.street_address = (
    "456 Paris Street"
)
```

Now:

```text
John
→ 123 London Road

Jane
→ 456 Paris Street
```

Changing Jane does not modify John.

---

# Shallow Copy vs Deep Copy

| Shallow Copy | Deep Copy |
|---|---|
| Copies outer object | Copies complete object graph |
| Nested objects may be shared | Nested objects copied recursively |
| Faster | Usually more expensive |
| `copy.copy()` | `copy.deepcopy()` |

---

# Why Prototype Uses Deep Copy Often

Prototype frequently involves objects containing nested mutable state.

Example:

```text
Employee
   ↓
Address
   ↓
More nested objects
```

If nested objects are accidentally shared between clones, modifying one clone can affect another.

Therefore a proper Prototype implementation often needs:

> **Deep copying or carefully controlled cloning.**

---

# Important Note

Prototype does not always require `deepcopy()`.

The important requirement is:

> **The clone must have the independence required by your design.**

If objects are immutable, shallow copying may sometimes be sufficient.

Use deep copy when nested mutable objects need to be independent.

---

# Prototype Example

```python
john = Person(
    "John",
    Address(
        "123 London Road",
        "London",
        "UK"
    )
)

jane = copy.deepcopy(john)

jane.name = "Jane"
jane.address.street_address = (
    "456 Paris Street"
)
```

Conceptually:

```text
Prototype
   John
    ↓
Deep Copy
    ↓
Jane
    ↓
Modify required values
```

---

# Why Use Prototype?

Suppose constructing an Employee requires:

```text
Employee
├── Address
├── Department
├── Permissions
├── Configuration
├── Office information
└── Default settings
```

Most employees may share the same configuration.

Instead of recreating everything:

```text
Create Employee
Configure Office
Configure Address
Configure Defaults
Configure Permissions
...
```

we can create a preconfigured prototype:

```text
Main Office Employee Prototype
```

and clone it.

---

# Prototype Factory

A Prototype Factory stores predefined prototype objects and creates new objects by cloning them.

Example:

```text
EmployeeFactory

├── Main Office Prototype
└── Auxiliary Office Prototype
```

Client asks:

```text
Create Main Office Employee
```

Factory:

```text
Clone Main Office Prototype
        ↓
Change Name
        ↓
Change Suite
        ↓
Return Employee
```

---

# Employee

```python
class Employee:
    def __init__(self, name, address):
        self.name = name
        self.address = address

    def __str__(self):
        return (
            f"Employee("
            f"name={self.name}, "
            f"address={self.address})"
        )
```

---

# Employee Factory

```python
class EmployeeFactory:

    main_office = Employee(
        "",
        Address(
            "123 London Road",
            "London",
            "UK",
            0
        )
    )

    aux_office = Employee(
        "",
        Address(
            "456 Paris Street",
            "Paris",
            "France",
            0
        )
    )
```

These are:

> **Prototype objects**

They contain common configuration.

---

# Internal Clone Method

```python
@staticmethod
def _new_employee(
    prototype,
    name,
    suite
):
    employee = copy.deepcopy(
        prototype
    )

    employee.name = name
    employee.address.suite = suite

    return employee
```

Flow:

```text
Prototype
   ↓
deepcopy()
   ↓
New Employee
   ↓
Customize
```

---

# Main Office Employee

```python
@staticmethod
def new_main_office_employee(
    name,
    suite
):
    return EmployeeFactory._new_employee(
        EmployeeFactory.main_office,
        name,
        suite
    )
```

Usage:

```python
john = (
    EmployeeFactory
    .new_main_office_employee(
        "John Doe",
        101
    )
)
```

Result:

```text
John Doe

123 London Road
London
UK
Suite 101
```

---

# Auxiliary Office Employee

```python
@staticmethod
def new_aux_office_employee(
    name,
    suite
):
    return EmployeeFactory._new_employee(
        EmployeeFactory.aux_office,
        name,
        suite
    )
```

Usage:

```python
jelly = (
    EmployeeFactory
    .new_aux_office_employee(
        "Jelly Smith",
        202
    )
)
```

Result:

```text
Jelly Smith

456 Paris Street
Paris
France
Suite 202
```

---

# Why Prototype Factory Helps

Without prototypes:

```python
employee = Employee(
    "John Doe",
    Address(
        "123 London Road",
        "London",
        "UK",
        101
    )
)
```

and for every main-office employee, we repeat:

```text
123 London Road
London
UK
```

With Prototype Factory:

```python
EmployeeFactory.new_main_office_employee(
    "John Doe",
    101
)
```

The shared configuration is already stored in the prototype.

---

# Prototype Factory Structure

```text
EmployeeFactory
       ↓
------------------------
|                      |
Main Prototype     Aux Prototype
     ↓                  ↓
deepcopy()          deepcopy()
     ↓                  ↓
Employee           Employee
```

---

# Prototype vs Factory

They can work together.

## Prototype

Answers:

> **Can I create this object by cloning an existing configured object?**

```text
Existing Object
     ↓
Clone
     ↓
New Object
```

---

## Factory

Answers:

> **Who should handle object creation?**

```text
Client
  ↓
Factory
  ↓
Object
```

A Prototype Factory combines both:

```text
Client
   ↓
Factory
   ↓
Clone Prototype
   ↓
Return Object
```

---

# Prototype vs Builder

## Prototype

Creates an object by:

```text
Copying an existing object
```

Example:

```python
copy.deepcopy(template)
```

---

## Builder

Creates an object:

```text
Step by step
```

Example:

```text
set_name()
set_address()
set_job()
build()
```

Simple revision:

```text
Prototype
→ Copy existing object
```

```text
Builder
→ Assemble new object
```

---

# Prototype vs Factory Method

Factory Method may create:

```text
New object from scratch
```

Prototype creates:

```text
New object from existing object
```

A Factory Method can internally use Prototype cloning.

These patterns are not mutually exclusive.

---

# When to Use Prototype

Use Prototype when:

- Object initialization is expensive
- Objects share lots of common configuration
- Creation involves many nested objects
- You frequently create similar objects
- You want preconfigured templates
- Reconstructing everything repeatedly is unnecessary

---

# Real-World Examples

Possible uses include:

## Document Templates

```text
Invoice Template
       ↓
Clone
       ↓
Customer Invoice
```

---

## Game Objects

```text
Enemy Prototype
      ↓
Clone
      ↓
Enemy 1
Enemy 2
Enemy 3
```

Each clone can then have different:

- Position
- Health
- Name

---

## Configuration Objects

```text
Production Config Template
         ↓
Clone
         ↓
Customize one service
```

---

## UI Components

```text
Configured UI Component
        ↓
Clone
        ↓
Modify label/content
```

---

# Advantages

Prototype provides:

- Faster creation for complex objects
- Reuse of existing configuration
- Less repeated initialization
- Easy creation of similar objects
- Reduced constructor complexity
- Convenient templates

---

# Drawbacks

Prototype can also introduce problems.

## Deep Copy Cost

Large object graphs can make:

```python
copy.deepcopy()
```

expensive.

---

## Complex References

Objects may contain:

- File handles
- Database connections
- Locks
- Network connections
- External resources

These should not always be blindly deep-copied.

---

## Cyclic Object Graphs

Objects may reference each other.

Example:

```text
A → B
↑   ↓
└───┘
```

Cloning such structures requires careful handling.

---

# Custom Clone Logic

Sometimes instead of blindly using:

```python
copy.deepcopy()
```

a class may provide:

```python
def clone(self):
    ...
```

Then the class controls what should and should not be copied.

Conceptually:

```python
new_object = prototype.clone()
```

This is closer to the classic Prototype pattern.

---

# Interview Question

## What is the Prototype Pattern?

Prototype is a creational design pattern where new objects are created by cloning an existing configured object.

It is useful when object initialization is expensive or when many objects share similar configuration.

For example, instead of repeatedly constructing an Employee with the same office address, we can create a preconfigured Employee prototype, deep-copy it, and then modify only the employee-specific fields such as name and suite number.

---

# What Is the Difference Between Shallow and Deep Copy?

## Shallow Copy

```text
New outer object
+
Shared nested references
```

Python:

```python
copy.copy()
```

---

## Deep Copy

```text
New outer object
+
Copied nested objects
```

Python:

```python
copy.deepcopy()
```

For prototypes with nested mutable objects, deep copy is often necessary so clones remain independent.

---

# How Prototype Works

```text
1. Create/configure prototype
        ↓
2. Clone prototype
        ↓
3. Modify clone
        ↓
4. Use independent new object
```

---

# Quick Revision

```text
Prototype
→ Creational Design Pattern
```

```text
Core Idea
→ Clone an existing object
```

```text
Prototype
→ Preconfigured object/template
```

```text
Assignment
→ Copies reference
→ Not cloning
```

```text
Shallow Copy
→ New outer object
→ Nested objects shared
```

```text
Deep Copy
→ Copy entire required object graph
```

```text
Prototype Factory
→ Stores prototypes
→ Clones + customizes them
```

```text
Builder
→ Construct step by step
```

```text
Prototype
→ Copy and modify
```

---

# Key Takeaways

- **Prototype is a creational design pattern.**
- **It creates objects by cloning an existing configured object.**
- **Simple assignment does not clone an object; it copies the reference.**
- **`copy.copy()` performs a shallow copy.**
- **`copy.deepcopy()` recursively copies nested objects.**
- **Nested mutable state is the main reason deep copying matters.**
- **Prototype is useful when many objects share common configuration.**
- **A Prototype Factory can store predefined templates and clone them on demand.**
- **Prototype and Factory can be combined.**
- **Prototype differs from Builder: Prototype copies an existing object, while Builder constructs one step by step.**
- **Do not blindly deep-copy external resources such as DB connections, locks, sockets, or file handles.**
- **For complex cases, custom `clone()` logic may be safer than generic deep copying.**

# One-Line Revision

> **Prototype = create a new object by cloning an existing configured object and then customize only what needs to change.**