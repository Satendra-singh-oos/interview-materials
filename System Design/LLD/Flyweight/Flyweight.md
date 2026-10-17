# Flyweight Design Pattern

Flyweight is a **structural design pattern**.

> **Flyweight reduces memory usage by sharing common state between many similar objects instead of storing duplicate copies inside every object.**

Simple idea:

```text
Many Objects
   ↓
Same repeated data stored again and again
   ↓
High memory usage
```

Flyweight changes this to:

```text
Many Objects
   ↓
Shared Common Data
+
Small Unique Data Per Object
```

The goal is:

> **Store repeated data once and reference it from many objects.**

---

# Why Do We Need Flyweight?

Suppose an application creates:

```text
1,000,000 objects
```

and every object contains some repeated information.

Example:

```text
Character A
→ Font: Arial
→ Font Size: 12

Character B
→ Font: Arial
→ Font Size: 12

Character C
→ Font: Arial
→ Font Size: 12
```

If every object stores:

```text
Arial
12
```

separately, we waste memory.

Instead:

```text
            Shared Font Object
             Arial, Size 12
                    ↑
          ---------------------
          |         |         |
       Char A     Char B     Char C
```

All characters can reference the same shared information.

That is the main Flyweight idea.

---

# When to Use Flyweight

Flyweight becomes useful when:

- The application creates a very large number of objects
- Memory usage becomes significant
- Many objects contain duplicate state
- Object state can be separated into shared and unique parts
- Shared state can be reused safely
- Unique state can be stored separately or supplied when needed

Typical examples include:

- Text editors
- Game objects
- Map markers
- UI elements
- Repeated names/strings
- Rendering systems

---

# Intrinsic and Extrinsic State

This distinction is the most important part of Flyweight.

## Intrinsic State

Intrinsic state is:

> **State that can be shared between multiple objects because it does not depend on one particular object's context.**

Example:

```text
Font Family
Character Glyph
Texture
Model Data
```

Suppose 10,000 game trees use the same tree model.

The model data can be shared.

```text
Tree Model
   ↑
   |
10,000 Tree Instances
```

---

# Extrinsic State

Extrinsic state is:

> **Context-specific state that differs between individual objects and therefore is not part of the shared flyweight.**

For trees:

```text
Position X
Position Y
Rotation
```

Each tree has its own position.

---

# Example

```text
Tree

Intrinsic / Shared:
→ Texture
→ Mesh
→ Tree Type

Extrinsic / Unique:
→ X position
→ Y position
→ Rotation
```

Instead of:

```text
Tree 1
→ Texture copy
→ Mesh copy
→ Position

Tree 2
→ Texture copy
→ Mesh copy
→ Position
```

we do:

```text
              Shared Tree Data
             Texture + Mesh
                  ↑    ↑
                  |    |
              Tree 1 Tree 2

Tree 1 → Position A
Tree 2 → Position B
```

---

# Easy Revision

```text
Intrinsic
→ Shared

Extrinsic
→ Unique / contextual
```

---

# Example 1 — User Names

Suppose we generate many users.

```python
class User:
    def __init__(self, name):
        self.name = name
```

Now imagine these names:

```text
John Smith
John Jones
John Williams

Frank Smith
Frank Jones
Frank Williams
```

The strings:

```text
John
Frank
Smith
Jones
Williams
```

appear repeatedly.

But a normal implementation stores every complete name separately.

---

# Normal User Creation

```python
users = []

for first in first_names:
    for last in last_names:
        users.append(
            User(f"{first} {last}")
        )
```

Suppose:

```text
100 first names
×
100 last names
```

Then:

```text
10,000 users
```

are created.

Many pieces of those names repeat.

---

# Example Repetition

Instead of:

```text
User 1 → "Jim Jones"
User 2 → "Frank Jones"
User 3 → "Kevin Jones"
```

we repeatedly store:

```text
"Jones"
```

Flyweight-style optimization says:

> Store `"Jones"` once and reference it.

---

# Shared String Pool

```python
class User2:
    strings = []
```

This:

```text
strings
```

acts like a shared pool.

Example:

```text
Index 0 → Jim
Index 1 → Jones
Index 2 → Frank
```

Then users store indexes instead of duplicate strings.

---

# User2

```python
class User2:
    strings = []

    def __init__(self, full_name):
        def get_or_add(value):
            if value in self.strings:
                return self.strings.index(value)

            self.strings.append(value)

            return len(self.strings) - 1

        self.names = [
            get_or_add(part)
            for part in full_name.split(" ")
        ]

    def __str__(self):
        return " ".join(
            self.strings[index]
            for index in self.names
        )
```

---

# What Happens?

Create:

```python
u2 = User2("Jim Jones")
```

Initially:

```text
strings = []
```

After construction:

```text
strings:

0 → Jim
1 → Jones
```

And:

```text
u2.names = [0, 1]
```

So `u2` stores:

```text
[0, 1]
```

instead of storing another full copy of:

```text
Jim
Jones
```

---

# Create Another User

```python
u3 = User2("Frank Jones")
```

`Frank` is new:

```text
Add Frank
```

But `Jones` already exists.

So:

```text
strings:

0 → Jim
1 → Jones
2 → Frank
```

and:

```text
u3.names = [2, 1]
```

Notice:

```text
Jones
```

is only stored once.

Both users reference index:

```text
1
```

---

# Memory Structure

Instead of:

```text
User 1
→ Jim
→ Jones

User 2
→ Frank
→ Jones
```

we have:

```text
Shared String Pool

0 → Jim
1 → Jones
2 → Frank

User 1 → [0, 1]
User 2 → [2, 1]
```

The repeated value:

```text
Jones
```

is shared.

This is the Flyweight idea.

---

# Intrinsic vs Extrinsic in This Example

Shared state:

```text
Individual name strings
→ Jim
→ Jones
→ Frank
```

These form the shared pool.

Per-user state:

```text
Indexes describing which names belong to that user
```

Example:

```text
Jim Jones
→ [0, 1]

Frank Jones
→ [2, 1]
```

---

# Important Idea

The optimization only becomes useful when:

```text
Large number of objects
+
Lots of repeated values
```

For:

```text
2 users
```

this extra complexity is unnecessary.

For:

```text
millions of repeated records
```

it may provide substantial savings.

---

# String Interning

The username example is similar to the idea of:

> **String Interning**

Instead of keeping many equal string objects:

```text
"Jones"
"Jones"
"Jones"
"Jones"
```

we keep one canonical representation:

```text
"Jones"
   ↑
   ↑
   ↑
Many references
```

This is a common form of Flyweight-style optimization.

---

# Production Improvement

Your example uses:

```python
if value in self.strings:
    return self.strings.index(value)
```

That requires scanning the list.

As the pool gets larger, lookup becomes more expensive.

A more scalable design could use:

```python
dictionary = {
    "Jim": 0,
    "Jones": 1
}
```

Then string lookup becomes much faster.

Conceptually:

```text
String
 ↓
Dictionary
 ↓
Index
```

The design-pattern idea remains the same:

> Store shared values once.

---

# Example 2 — Text Formatting

Consider a text editor.

```text
This is a brave new world
```

Suppose some parts should be:

- Capitalized
- Bold
- Italic

One approach is to store formatting information for every character.

---

# Naive FormattedText

```python
class FormattedText:
    def __init__(self, plain_text):
        self.plain_text = plain_text

        self.caps = (
            [False]
            * len(plain_text)
        )
```

If the text contains:

```text
1,000,000 characters
```

then:

```text
1,000,000 formatting entries
```

may be created.

---

# Capitalization

```python
def capitalize(self, start, end):
    for i in range(start, end):
        self.caps[i] = True
```

Suppose:

```text
"This is a brave new world"
```

and we capitalize a range.

The object stores one boolean per character:

```text
T → False
h → False
i → False
s → False
...
b → True
r → True
a → True
v → True
e → True
...
```

Even characters with no special formatting still require a formatting entry.

---

# Memory Problem

Imagine:

```text
10 million characters
```

with only:

```text
50 specially formatted ranges
```

A per-character formatting representation can be wasteful.

Instead, we can store only:

```text
The formatting ranges
```

---

# BetterFormattedText

```python
class BetterFormattedText:
    def __init__(self, plain_text):
        self.plain_text = plain_text
        self.formatting = []
```

Instead of storing state for every character:

```text
One formatting record per character
```

we store:

```text
Only ranges that have formatting
```

---

# TextRange

```python
class TextRange:
    def __init__(
        self,
        start,
        end,
        capitalize=False,
        bold=False,
        italic=False
    ):
        self.start = start
        self.end = end

        self.capitalize = capitalize
        self.bold = bold
        self.italic = italic
```

A TextRange can represent:

```text
Characters 10–15

capitalize = True
bold = False
italic = False
```

This one object applies formatting to multiple characters.

---

# Range Check

```python
def covers(self, position):
    return (
        self.start
        <= position
        <= self.end
    )
```

This checks:

> Is this character position inside the formatting range?

---

# Adding a Range

```python
def get_range(self, start, end):
    text_range = self.TextRange(
        start,
        end
    )

    self.formatting.append(
        text_range
    )

    return text_range
```

Usage:

```python
bft.get_range(
    16,
    19
).capitalize = True
```

This means:

```text
Characters 16 → 19
→ Capitalize
```

---

# Rendering the Text

```python
def __str__(self):
    result = []

    for i, character in enumerate(
        self.plain_text
    ):
        for text_range in self.formatting:

            if (
                text_range.covers(i)
                and
                text_range.capitalize
            ):
                character = (
                    character.upper()
                )

        result.append(character)

    return "".join(result)
```

For every character:

```text
Character position
       ↓
Check formatting ranges
       ↓
Does one apply?
       ↓
Apply formatting
```

---

# Why Is This More Memory Efficient?

Naive:

```text
Text Length = 1,000,000

Formatting Metadata
≈ 1,000,000 entries
```

Range-based:

```text
Text Length = 1,000,000

Formatting Ranges
= maybe 20 entries
```

So we avoid storing redundant formatting state for each character.

---

# Important Clarification

This second example illustrates the same **memory-sharing/compression idea**, but it is not as textbook a Flyweight implementation as the username/string-pool example.

It is better understood as:

> **Represent shared formatting information once for a range instead of duplicating formatting state per character.**

The important learning idea remains:

```text
Repeated State
      ↓
Extract / Share It
      ↓
Store only unique context
```

---

# Small Range Detail

Your two examples use slightly different end semantics.

`FormattedText`:

```python
range(start, end)
```

means:

```text
start inclusive
end exclusive
```

while:

```python
start <= position <= end
```

means:

```text
start inclusive
end inclusive
```

Either style is fine, but a real implementation should choose one convention and use it consistently.

---

# Classic Flyweight Structure

Typical participants are:

## Flyweight

Contains shared intrinsic state.

Example:

```text
TreeType
```

with:

```text
Texture
Model
Color
```

---

## Concrete Flyweight

The actual reusable shared object.

Example:

```text
OakTreeType
PineTreeType
```

---

## Context

Stores the unique extrinsic state.

Example:

```text
Tree
→ X
→ Y
→ TreeType reference
```

---

## Flyweight Factory

Creates or reuses Flyweights.

Example:

```text
TreeFactory
      ↓
Already have OakTreeType?
     /              \
   Yes               No
    ↓                 ↓
Reuse             Create
                     ↓
                   Store
```

---

# Classic Game Example

Imagine a game containing:

```text
100,000 trees
```

Every tree might contain:

```text
Tree
├── X
├── Y
├── Texture
├── Mesh
├── Color
└── Tree Type
```

If texture and mesh are large, duplication becomes expensive.

---

# Without Flyweight

```text
Tree 1
→ Oak Texture
→ Oak Mesh
→ Position A

Tree 2
→ Oak Texture
→ Oak Mesh
→ Position B

Tree 3
→ Oak Texture
→ Oak Mesh
→ Position C
```

Three copies of the same large data.

---

# With Flyweight

```text
             OakTreeType
          Texture + Mesh
             ↑   ↑   ↑
             |   |   |
          Tree1 Tree2 Tree3
```

Each tree only stores:

```text
X
Y
TreeType reference
```

Much less memory.

---

# Flyweight Factory

A factory often ensures equivalent Flyweights are reused.

Conceptually:

```python
tree_type = factory.get_tree_type(
    "Oak"
)
```

Factory does:

```text
"Oak" already exists?
      ↓
Yes → Return existing Oak flyweight

No → Create and cache it
```

This is very similar to your:

```python
get_or_add()
```

function in `User2`.

---

# Flyweight and Caching

Flyweight often uses a cache/pool internally.

But Flyweight and caching are not exactly the same thing.

## Cache

Usually tries to avoid:

```text
Repeated expensive computation / retrieval
```

## Flyweight

Primarily tries to avoid:

```text
Repeated memory storage
```

Both may use:

```text
Dictionary / Pool
```

but their intent differs.

---

# Flyweight vs Prototype

## Prototype

```text
Existing object
      ↓
Clone
      ↓
Another independent object
```

Prototype intentionally creates another copy.

---

## Flyweight

```text
Existing common state
      ↓
Share
      ↓
Multiple objects reference it
```

Flyweight intentionally avoids copies.

Easy revision:

```text
Prototype
→ Copy

Flyweight
→ Share
```

---

# Flyweight vs Singleton

## Singleton

Ensures:

```text
One instance of a particular class
```

## Flyweight

Can have:

```text
Many shared objects
```

but reuses each common value.

Example:

```text
Flyweight Pool

OakTreeType
PineTreeType
MapleTreeType
```

There can be multiple Flyweights.

Each one may be shared by many context objects.

---

# Flyweight vs Object Pool

These can also be confused.

## Flyweight

Objects are shared because they are effectively common reusable state.

```text
Many clients
→ Same shared object
```

## Object Pool

Objects are temporarily borrowed and returned.

```text
Acquire object
→ Use it
→ Return to pool
```

Example:

```text
Database connection pool
```

is not normally a Flyweight.

---

# Benefits

Flyweight can provide:

- Significant memory reduction
- Reuse of immutable/shared data
- Better scalability with huge object counts
- Less duplicated state

---

# Drawbacks

Flyweight introduces trade-offs.

## More Complexity

Instead of:

```text
Object contains everything
```

we now have:

```text
Object
+
Shared Flyweight
+
Factory/Pool
```

---

## State Separation

Developers must clearly understand:

```text
Intrinsic
vs
Extrinsic
```

Poor separation can create bugs.

---

## Lookup Overhead

Finding shared Flyweights may require:

```text
Dictionary lookup
Cache lookup
```

There is a small CPU cost in exchange for lower memory usage.

---

## Shared State Should Be Safe

Intrinsic Flyweight data should generally be:

```text
Immutable
```

or treated as immutable.

Why?

Suppose:

```text
10,000 objects
→ Same Flyweight
```

and one client modifies it.

Then:

```text
All 10,000 objects
```

may see the change.

That can cause major bugs.

---

# When NOT to Use Flyweight

Do not use Flyweight just because some data repeats.

Use it when memory pressure actually justifies the added complexity.

If you have:

```text
100 objects
```

and each is small, Flyweight may provide little benefit.

Prefer:

> Measure first, optimize when repetition is significant.

---

# Real-World Examples

## Text Editor

Shared:

```text
Font / Glyph information
```

Unique:

```text
Character position
```

---

## Game Trees

Shared:

```text
Mesh
Texture
Tree Type
```

Unique:

```text
Position
Rotation
```

---

## Map Markers

Shared:

```text
Marker icon
Style
```

Unique:

```text
Latitude
Longitude
```

---

## User/String Pool

Shared:

```text
Repeated names
```

Unique:

```text
Which name indexes belong to a user
```

---

# Interview Question

## What is the Flyweight Pattern?

Flyweight is a structural design pattern used to reduce memory consumption when an application needs a very large number of similar objects.

It works by separating object state into:

```text
Intrinsic state
→ Shared

Extrinsic state
→ Unique/context-specific
```

Instead of storing duplicate intrinsic state in every object, the application stores it once and allows multiple objects to reference it.

For example, if thousands of users share the same first or last names, we can keep those strings in a shared pool and let each User store only indexes into the pool.

---

# How Do You Identify a Flyweight Opportunity?

Ask:

```text
Do I have a very large number of objects?
        ↓
Is memory usage significant?
        ↓
Do these objects duplicate lots of state?
        ↓
Can repeated state be safely shared?
```

If yes:

```text
Flyweight may help.
```

---

# Mental Model

Imagine:

```text
10,000 books
```

all containing the author's country:

```text
"India"
```

Instead of storing:

```text
India
India
India
India
...
```

10,000 times, store:

```text
India
```

once and reference it.

That is the Flyweight mindset.

---

# Quick Revision

```text
Flyweight
→ Structural Design Pattern
```

```text
Goal
→ Reduce memory usage
```

```text
Technique
→ Share repeated state
```

```text
Intrinsic State
→ Shared/common
```

```text
Extrinsic State
→ Unique/context-dependent
```

```text
User Example

Shared String Pool
→ Jim
→ Jones
→ Frank

Users
→ Store indexes
```

```text
Prototype
→ Copy objects
```

```text
Flyweight
→ Share objects/state
```

```text
Singleton
→ One object instance
```

```text
Flyweight
→ Many shared flyweight objects possible
```

---

# Key Takeaways

- **Flyweight is a structural design pattern focused primarily on memory optimization.**
- **It is useful when an application contains a very large number of similar objects.**
- **Intrinsic state is common/shared state.**
- **Extrinsic state is unique/context-dependent state.**
- **Repeated intrinsic state is stored once rather than duplicated across every object.**
- **The username example stores repeated name strings in a shared pool and users keep indexes into that pool.**
- **A Flyweight Factory commonly manages creation and reuse of shared objects.**
- **Shared Flyweight data should generally be immutable or treated as immutable.**
- **The range-formatting example demonstrates the same memory-optimization idea by representing formatting once per range instead of once per character.**
- **Prototype copies objects; Flyweight avoids copies by sharing state.**
- **Singleton restricts instance count; Flyweight may maintain many different shared objects.**
- **Flyweight adds complexity, so use it when memory savings are meaningful rather than as premature optimization.**

# One-Line Revision

> **Flyweight = when thousands or millions of objects repeat the same data, pull that common data out, store it once, and let all those objects share it while keeping only their unique state separately.**