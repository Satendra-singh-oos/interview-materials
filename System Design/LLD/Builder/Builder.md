# Builder Pattern

Builder is a **creational design pattern** used to construct complex objects step by step.

> **Instead of exposing complicated construction logic to the client, move the construction process into a Builder.**

Useful when:

- Object creation requires multiple steps
- There are many optional properties
- Constructors become too large
- The object contains nested structures
- You want a readable fluent API

---

# 1. Basic Builder

Suppose we want to create:

```html
<p>hello</p>
```

For something simple:

```python
text = "hello"
parts = ["<p>", text, "</p>"]

print("".join(parts))
```

This is completely fine.

---

# Building More Complex HTML

Suppose:

```python
words = ["hello", "world"]

parts = ["<ul>"]

for word in words:
    parts.append(f"<li>{word}</li>")

parts.append("</ul>")

print("\n".join(parts))
```

Output:

```html
<ul>
<li>hello</li>
<li>world</li>
</ul>
```

This still works.

But as HTML becomes more complex, the client must remember:

- Opening tags
- Closing tags
- Correct nesting
- Child elements
- Formatting

Example mistake:

```text
<ul>
   <li>...</li>
   <li>...</li>

Missing </ul> ❌
```

Instead of making the caller manage construction details, we can outsource them to a:

> **Builder**

---

# HtmlElement

`HtmlElement` represents the final object being constructed.

```python
class HtmlElement:
    indent_size = 2

    def __init__(self, name="", text=""):
        self.name = name
        self.text = text
        self.elements = []

    def _str(self, indent):
        lines = []

        i = " " * (indent * self.indent_size)
        lines.append(f"{i}<{self.name}>")

        if self.text:
            i1 = " " * (
                (indent + 1) * self.indent_size
            )

            lines.append(
                f"{i1}{self.text}"
            )

        for element in self.elements:
            lines.append(
                element._str(indent + 1)
            )

        lines.append(
            f"{i}</{self.name}>"
        )

        return "\n".join(lines)

    def __str__(self):
        return self._str(0)

    @staticmethod
    def create(name):
        return HtmlBuilder(name)
```

The structure is:

```text
HtmlElement
├── name
├── text
└── child elements
```

For example:

```text
ul
├── li → hello
└── li → world
```

---

# HtmlBuilder

The Builder knows how to create the HTML structure.

```python
class HtmlBuilder:
    def __init__(self, root_name):
        self.root_name = root_name
        self._root = HtmlElement(root_name)

    def add_child(
        self,
        child_name,
        child_text
    ):
        self._root.elements.append(
            HtmlElement(
                child_name,
                child_text
            )
        )

    def add_child_fluent(
        self,
        child_name,
        child_text
    ):
        self._root.elements.append(
            HtmlElement(
                child_name,
                child_text
            )
        )

        return self

    def clear(self):
        self._root = HtmlElement(
            self.root_name
        )

    def __str__(self):
        return str(self._root)
```

Important:

```python
self._root = HtmlElement(root_name)
```

should be created per Builder instance.

Avoid:

```python
class HtmlBuilder:
    _root = HtmlElement()
```

because then multiple builders may share the same mutable object.

---

# Ordinary Builder

```python
builder = HtmlElement.create("ul")

builder.add_child(
    "li",
    "hello"
)

builder.add_child(
    "li",
    "world"
)

print(builder)
```

Here each method is called separately.

---

# Fluent Builder

If the method returns:

```python
return self
```

we can chain methods.

```python
builder.clear()

builder \
    .add_child_fluent(
        "li",
        "hello"
    ) \
    .add_child_fluent(
        "li",
        "world"
    )

print(builder)
```

This is a:

> **Fluent Interface**

Flow:

```text
add_child()
   ↓
return self
   ↓
add_child()
   ↓
return self
```

---

# Builder vs Fluent Interface

They are related but not identical.

## Builder

Focuses on:

> Constructing an object step by step.

## Fluent Interface

Focuses on:

> Making method calls readable through chaining.

A Builder can be fluent, but it does not have to be.

---

# 2. Faceted Builder

Sometimes one object contains several groups of properties.

Consider:

```text
Person
├── Address
│   ├── street
│   ├── postcode
│   └── city
│
└── Job
    ├── company
    ├── position
    └── income
```

Putting all construction methods inside one Builder can eventually make the Builder too large.

We can divide construction into:

> **Builder Facets**

---

# Person

```python
class Person:
    def __init__(self):
        print("Creating an instance of Person")

        # Address
        self.street_address = None
        self.postcode = None
        self.city = None

        # Employment
        self.company_name = None
        self.position = None
        self.annual_income = None

    def __str__(self):
        return (
            f"Address: "
            f"{self.street_address}, "
            f"{self.postcode}, "
            f"{self.city}\n"
            f"Employed at "
            f"{self.company_name} "
            f"as a {self.position} "
            f"earning {self.annual_income}"
        )
```

---

# Main PersonBuilder

```python
class PersonBuilder:
    def __init__(self, person=None):
        if person is None:
            self.person = Person()
        else:
            self.person = person

    @property
    def lives(self):
        return PersonAddressBuilder(
            self.person
        )

    @property
    def works(self):
        return PersonJobBuilder(
            self.person
        )

    def build(self):
        return self.person
```

This Builder acts as a:

> **Facade over multiple specialized builders.**

It gives access to:

```text
.lives
.works
```

---

# Address Builder

```python
class PersonAddressBuilder(PersonBuilder):
    def __init__(self, person):
        super().__init__(person)

    def at(self, street_address):
        self.person.street_address = (
            street_address
        )
        return self

    def with_postcode(self, postcode):
        self.person.postcode = postcode
        return self

    def in_city(self, city):
        self.person.city = city
        return self
```

This Builder only handles:

```text
Address Information
```

---

# Job Builder

```python
class PersonJobBuilder(PersonBuilder):
    def __init__(self, person):
        super().__init__(person)

    def at(self, company_name):
        self.person.company_name = (
            company_name
        )
        return self

    def as_a(self, position):
        self.person.position = position
        return self

    def earning(self, annual_income):
        self.person.annual_income = (
            annual_income
        )
        return self
```

This Builder only handles:

```text
Employment Information
```

---

# Using the Faceted Builder

```python
pb = PersonBuilder()

person = (
    pb
    .lives
        .at("123 London Road")
        .in_city("London")
        .with_postcode("SW12BC")
    .works
        .at("Fabrikam")
        .as_a("Engineer")
        .earning(123000)
    .build()
)

print(person)
```

Notice how naturally this reads:

```text
Person

lives
   at ...
   in city ...
   with postcode ...

works
   at ...
   as ...
   earning ...
```

---

# Important Faceted Builder Idea

All Builders modify the **same Person object**.

```text
                Person
                  ↑
          ----------------
          |              |
AddressBuilder       JobBuilder
```

When:

```python
pb.lives
```

returns a `PersonAddressBuilder`, it receives:

```python
self.person
```

When:

```python
.works
```

returns a `PersonJobBuilder`, it receives the exact same:

```python
Person
```

Therefore construction can move between different facets.

---

# Why Use Faceted Builder?

Without facets:

```text
PersonBuilder
├── at_address()
├── postcode()
├── city()
├── company()
├── position()
├── salary()
├── education()
├── phone()
├── ...
```

Eventually the Builder itself becomes huge.

With facets:

```text
PersonBuilder
├── PersonAddressBuilder
├── PersonJobBuilder
├── PersonEducationBuilder
└── ...
```

Each Builder handles one logical area.

---

# Faceted Builder Benefits

- Better organization
- Smaller specialized builders
- Fluent API
- Easier maintenance
- Separates construction concerns
- Still produces one final object

---

# Faceted Builder Structure

```text
                    PersonBuilder
                    /          \
                   /            \
       PersonAddressBuilder   PersonJobBuilder
               \                /
                \              /
                     Person
```

---

# 3. Builder Inheritance

Another approach is to extend Builder functionality using inheritance.

Suppose:

```python
class Person:
    def __init__(self):
        self.name = None
        self.position = None
        self.date_of_birth = None

    def __str__(self):
        return (
            f"{self.name} "
            f"born on {self.date_of_birth} "
            f"works as a {self.position}"
        )

    @staticmethod
    def new():
        return PersonBuilder()
```

---

# Base Builder

```python
class PersonBuilder:
    def __init__(self):
        self.person = Person()

    def build(self):
        return self.person
```

This contains the shared construction state.

---

# PersonInfoBuilder

```python
class PersonInfoBuilder(
    PersonBuilder
):
    def called(self, name):
        self.person.name = name
        return self
```

Adds:

```text
Name construction
```

---

# PersonJobBuilder

```python
class PersonJobBuilder(
    PersonInfoBuilder
):
    def works_as_a(self, position):
        self.person.position = position
        return self
```

Now this Builder has:

```text
called()
+
works_as_a()
```

because it inherits from `PersonInfoBuilder`.

---

# PersonBirthDateBuilder

```python
class PersonBirthDateBuilder(
    PersonJobBuilder
):
    def born(self, date_of_birth):
        self.person.date_of_birth = (
            date_of_birth
        )
        return self
```

It now has:

```text
called()
works_as_a()
born()
build()
```

through inheritance.

---

# Usage

```python
pb = PersonBirthDateBuilder()

person = (
    pb
    .called("Dmitri")
    .works_as_a("quant")
    .born("1/1/1980")
    .build()
)

print(person)
```

The inheritance chain is:

```text
PersonBuilder
      ↑
PersonInfoBuilder
      ↑
PersonJobBuilder
      ↑
PersonBirthDateBuilder
```

Each Builder adds another construction capability.

---

# Builder Inheritance Idea

Instead of putting every operation inside:

```text
PersonBuilder
```

we gradually extend builder capabilities:

```text
PersonBuilder
   ↓
Add name
   ↓
Add job
   ↓
Add birth date
```

The most specialized Builder has access to all previous Builder methods.

---

# Important Limitation

This fluent inheritance style behaves differently across programming languages.

In Python:

```python
return self
```

naturally preserves the runtime object's actual type.

So chaining inherited Builder methods generally works.

In statically typed languages such as Java/C#/C++, fluent Builder inheritance may require:

- Generics
- Recursive generic types
- Covariant return types
- Specialized builder return types

Otherwise a parent method may return the parent Builder type and break access to child-specific methods.

So this example works naturally in Python but needs more careful type design in some other languages.

---

# Faceted Builder vs Builder Inheritance

## Faceted Builder

Splits construction by logical areas.

Example:

```text
PersonBuilder
├── AddressBuilder
└── JobBuilder
```

Usage:

```text
.lives...
.works...
```

Good when the object has clearly separated groups of properties.

---

## Builder Inheritance

Extends Builder capability through inheritance.

```text
BaseBuilder
    ↑
InfoBuilder
    ↑
JobBuilder
    ↑
BirthDateBuilder
```

Good for demonstrating progressive Builder specialization.

---

# Basic Builder vs Faceted Builder vs Builder Inheritance

| Type | Main Idea |
|---|---|
| Basic Builder | Construct complex object step by step |
| Fluent Builder | Builder methods return `self` |
| Faceted Builder | Split construction into specialized builders |
| Builder Inheritance | Extend builder capabilities through inheritance |

---

# Builder Pattern Structure

Classic Builder concept:

```text
Client
   ↓
Builder
   ↓
Construction Steps
   ↓
Product
```

For HTML:

```text
Client
   ↓
HtmlBuilder
   ↓
HtmlElement
```

For Person:

```text
Client
   ↓
PersonBuilder
   ↓
Person
```

---

# Builder vs Constructor

Simple object:

```python
Person("John", 25)
```

A normal constructor is sufficient.

Builder becomes useful when construction looks like:

```python
Person(
    name,
    age,
    address,
    city,
    postcode,
    company,
    position,
    salary,
    phone,
    email
)
```

Instead:

```python
builder \
    .called("John") \
    .works_as_a("Engineer") \
    .born("2000-01-01")
```

The intent becomes clearer.

---

# Builder vs Factory

## Factory

Usually answers:

> **Which object should I create?**

Example:

```python
VehicleFactory.create_car()
```

Usually creation happens in one operation.

---

## Builder

Answers:

> **How should this complex object be assembled?**

Example:

```python
builder \
    .add_cpu() \
    .add_ram() \
    .add_storage() \
    .build()
```

---

# When to Use Builder

Use Builder when:

- Constructor has many parameters
- Many parameters are optional
- Construction involves multiple steps
- Object has nested structure
- Construction needs validation
- Different representations can be constructed
- Readable configuration is valuable

Examples:

- HTML/XML generation
- SQL query builders
- HTTP request builders
- Configuration objects
- Complex domain objects

---

# When Not to Use Builder

Avoid unnecessary Builder classes when:

```python
User("John", 25)
```

already clearly expresses construction.

Builder introduces:

- Extra classes
- More abstraction
- More code

Use it only when construction complexity justifies it.

---

# Common Builder Mistakes

## 1. Shared Mutable Builder State

Bad:

```python
class HtmlBuilder:
    _root = HtmlElement()
```

This can share `_root` between instances.

Better:

```python
def __init__(self, root_name):
    self._root = HtmlElement(root_name)
```

---

## 2. Forgetting `return self`

Without:

```python
return self
```

this will not work:

```python
builder \
    .add_a() \
    .add_b()
```

because `add_a()` would return `None`.

---

## 3. Builder Becomes Too Large

If one Builder has dozens of unrelated construction methods, consider:

> **Faceted Builder**

---

# Interview Question

## What is the Builder Pattern?

Builder is a creational design pattern used to construct complex objects step by step.

Instead of putting all construction logic in a large constructor or requiring the client to manually assemble the object, a Builder exposes meaningful construction methods.

For example:

```python
person = (
    PersonBuilder()
    .lives
        .at("123 London Road")
        .in_city("London")
    .works
        .at("Fabrikam")
        .as_a("Engineer")
    .build()
)
```

This separates object construction from the object itself and makes construction easier to understand and maintain.

---

# What is a Faceted Builder?

A Faceted Builder divides construction into multiple specialized Builders.

Example:

```text
PersonBuilder
├── PersonAddressBuilder
└── PersonJobBuilder
```

All specialized Builders operate on the same final `Person` object.

This is useful when a complex object's construction naturally has separate concerns.

---

# What is a Fluent Builder?

A fluent Builder returns:

```python
self
```

from construction methods.

This allows:

```python
builder \
    .add_a() \
    .add_b() \
    .add_c()
```

Fluent API improves readability, but fluent interface and Builder are not the same pattern.

---

# Quick Revision

```text
Builder
→ Creational Pattern
```

```text
Purpose
→ Construct complex objects step by step
```

```text
Product
→ Final object being created
```

```text
Builder
→ Handles construction logic
```

```text
Fluent Builder
→ return self
→ Method chaining
```

```text
Faceted Builder
→ Multiple specialized builders
→ Same final object
```

```text
Builder Inheritance
→ Extend builder capability through inheritance
```

```text
Factory
→ Usually one-step creation
```

```text
Builder
→ Multi-step construction
```

---

# Key Takeaways

- **Builder is a creational design pattern.**
- **It separates complex object construction from the final object.**
- **A fluent Builder returns `self` so methods can be chained.**
- **Fluent interface and Builder are related but are not the same thing.**
- **Faceted Builder separates different construction concerns into specialized builders.**
- **Faceted builders still modify the same underlying object.**
- **Builder inheritance gradually adds additional construction capabilities.**
- **Python supports fluent inherited builders naturally because `self` retains the runtime type.**
- **Builder state should normally be instance-specific, not shared mutable class state.**
- **Use Builder only when construction is sufficiently complex to justify the abstraction.**

# One-Line Revision

> **Builder = move complex object construction into a dedicated step-by-step API; use fluent chaining for readability and facets when different parts of the object require separate builders.**