# Iterator Design Pattern

Iterator is a **behavioral design pattern**.

> **Iterator provides a standard way to traverse elements of a collection or complex data structure without exposing how that structure is internally represented.**

Simple idea:

```text
Complex Data Structure
        ↓
      Iterator
        ↓
element
element
element
...
```

The client only asks:

```text
Give me the next element.
```

It does not need to understand:

```text
How traversal works internally.
```

---

# Why Do We Need Iterator?

For a simple list:

```python
numbers = [1, 2, 3]
```

traversal is easy:

```python
for number in numbers:
    print(number)
```

But consider a tree:

```text
        1
       / \
      2   3
```

There are several possible traversal strategies:

```text
In-order
→ 2, 1, 3

Pre-order
→ 1, 2, 3

Post-order
→ 2, 3, 1
```

The client should not need to understand:

- Parent references
- Left/right navigation
- Tree traversal algorithm
- When traversal ends

Instead:

```python
for node in root:
    print(node.value)
```

should simply work.

That is the purpose of Iterator.

---

# Core Idea

Without Iterator:

```text
Client
  ↓
Understand tree structure
  ↓
Go left
Go parent
Go right
Track traversal state
```

With Iterator:

```text
Client
  ↓
Iterator
  ↓
Tree traversal logic
```

The traversal algorithm is encapsulated.

---

# Iterable vs Iterator

This distinction is important in Python.

## Iterable

An **iterable** is something that can produce an iterator.

It implements:

```python
__iter__()
```

Example:

```python
class Node:
    def __iter__(self):
        return InOrderIterator(self)
```

So:

```python
iter(root)
```

returns an iterator.

---

# Iterator

An **iterator** is the object that actually tracks traversal state.

It implements:

```python
__iter__()
__next__()
```

Example:

```python
class InOrderIterator:
    def __iter__(self):
        return self

    def __next__(self):
        ...
```

Simple revision:

```text
Iterable
→ Can produce an iterator

Iterator
→ Knows current traversal position
→ Produces next element
```

---

# Python `for` Loop Internally

When we write:

```python
for node in root:
    print(node.value)
```

Python effectively does something similar to:

```python
iterator = iter(root)

while True:
    try:
        node = next(iterator)
        print(node.value)

    except StopIteration:
        break
```

So these methods:

```text
__iter__()
__next__()
StopIteration
```

are the core of Python's iteration protocol.

---

# Tree Node

```python
class Node:
    def __init__(
        self,
        value,
        left=None,
        right=None
    ):
        self.value = value
        self.left = left
        self.right = right
        self.parent = None

        if left:
            left.parent = self

        if right:
            right.parent = self

    def __iter__(self):
        return InOrderIterator(self)
```

Each Node stores:

```text
value
left
right
parent
```

The parent reference helps the iterator move upward through the tree.

---

# Example Tree

```python
root = Node(
    1,
    Node(2),
    Node(3)
)
```

Tree:

```text
      1
     / \
    2   3
```

Parent relationships become:

```text
2.parent → 1
3.parent → 1
1.parent → None
```

---

# In-Order Traversal

In-order traversal follows:

```text
Left
 ↓
Current Node
 ↓
Right
```

For:

```text
      1
     / \
    2   3
```

the result is:

```text
2
1
3
```

---

# InOrderIterator

```python
class InOrderIterator:
    def __init__(self, root):
        self.root = root
        self.current = root
        self.yielded_start = False

        while self.current.left:
            self.current = self.current.left
```

The iterator starts from:

```text
root
```

but immediately walks to the:

```text
left-most node
```

because that is the first element in in-order traversal.

---

# Starting Position

For:

```text
        1
       / \
      2   3
```

the iterator starts:

```text
root = 1
```

then follows:

```text
1.left
 ↓
2
```

So:

```text
current = 2
```

The first value returned will therefore be:

```text
2
```

---

# Iterator Returns Itself

```python
def __iter__(self):
    return self
```

An iterator is itself iterable.

Therefore:

```python
iter(iterator)
```

returns the same object.

This is standard Python iterator behavior.

---

# Getting the First Element

```python
def __next__(self):

    if not self.yielded_start:
        self.yielded_start = True
        return self.current
```

Initially:

```text
current = left-most node
```

so the first call:

```python
next(iterator)
```

returns it.

Example:

```text
2
```

---

# Finding the Next Node

After returning the current node, there are two important cases.

---

# Case 1 — Current Node Has a Right Child

Suppose:

```text
Current
   \
   Right
```

Then the next in-order node is:

> The left-most node inside the current node's right subtree.

Code:

```python
if self.current.right:
    self.current = self.current.right

    while self.current.left:
        self.current = self.current.left

    return self.current
```

Conceptually:

```text
Current
   ↓
Go Right
   ↓
Go Left as far as possible
   ↓
Next Node
```

---

# Example

Consider:

```text
      10
        \
         20
        /
       15
```

After visiting:

```text
10
```

we go:

```text
Right → 20
Left → 15
```

So the next node is:

```text
15
```

---

# Case 2 — No Right Child

If there is no right subtree:

```text
Current
```

we move upward using parent references.

```python
parent = self.current.parent
```

But we cannot always immediately return the parent.

---

# Why We Sometimes Keep Moving Up

Suppose:

```text
    1
   /
  2
```

After visiting:

```text
2
```

the next node is:

```text
1
```

Easy.

But consider:

```text
      4
     /
    2
     \
      3
```

After visiting:

```text
3
```

we cannot return:

```text
2
```

because `2` has already been visited.

So we move upward while:

```text
current is the right child of parent
```

Code:

```python
while (
    parent
    and self.current == parent.right
):
    self.current = parent
    parent = parent.parent
```

This means:

> Keep moving upward while we are returning from a right subtree.

---

# Why This Works

In-order is:

```text
Left
Current
Right
```

If we just finished a parent's **right** subtree:

```text
Parent
   \
   Current
```

then:

```text
Parent
```

has already been visited.

So we must continue moving upward.

---

# Then Move to Parent

```python
self.current = parent
```

If a valid parent exists:

```python
if self.current:
    return self.current
```

Otherwise:

```python
raise StopIteration
```

Traversal is finished.

---

# Complete Iterator

```python
class InOrderIterator:
    def __init__(self, root):
        self.root = root
        self.current = root
        self.yielded_start = False

        while self.current.left:
            self.current = self.current.left

    def __iter__(self):
        return self

    def __next__(self):
        if not self.yielded_start:
            self.yielded_start = True
            return self.current

        if self.current.right:
            self.current = self.current.right

            while self.current.left:
                self.current = self.current.left

            return self.current

        parent = self.current.parent

        while (
            parent
            and self.current == parent.right
        ):
            self.current = parent
            parent = parent.parent

        self.current = parent

        if self.current:
            return self.current

        raise StopIteration
```

---

# Manual Usage

```python
iterator = iter(root)

print(
    [
        next(iterator).value
        for _ in range(3)
    ]
)
```

Output:

```text
[2, 1, 3]
```

---

# Normal Python Usage

Because `Node.__iter__()` returns an iterator:

```python
for node in root:
    print(node.value)
```

works naturally.

Output:

```text
2
1
3
```

The client does not know anything about the traversal algorithm.

---

# Why This Is the Iterator Pattern

Client code:

```python
for node in root:
    ...
```

does not need to know:

```text
Go left
Check right
Move to parent
Determine whether parent was already visited
Stop traversal
```

All of that lives inside:

```text
InOrderIterator
```

So traversal logic is separated from the data structure and the client.

---

# Iterator Holds Traversal State

An Iterator is not just a traversal function.

It usually stores state such as:

```text
Current position
Traversal progress
Previous position
Stack / parent references
Whether traversal has started
```

In this example:

```python
self.current
self.yielded_start
```

represent the traversal state.

---

# Multiple Iterators Can Exist

Because traversal state is stored in the iterator rather than globally inside the tree:

```python
iterator1 = iter(root)
iterator2 = iter(root)
```

both can traverse independently.

Conceptually:

```text
Same Tree
   ↑   ↑
   |   |
Iterator 1
Iterator 2
```

Each has its own:

```text
current
yielded_start
```

This is another important benefit.

---

# Generator-Based Iterator

Python gives us a much simpler way to create iterators:

> **Generators**

Instead of manually implementing:

```text
__iter__()
__next__()
state management
StopIteration
```

we can use:

```text
yield
```

---

# Generator Example

```python
def traverse_in_order(root):

    def traverse(current):

        if current.left:
            yield from traverse(
                current.left
            )

        yield current

        if current.right:
            yield from traverse(
                current.right
            )

    yield from traverse(root)
```

---

# How This Works

For each node:

```text
Traverse Left
     ↓
Yield Current
     ↓
Traverse Right
```

which exactly matches:

```text
In-order traversal
```

---

# `yield`

Instead of:

```python
return current
```

we use:

```python
yield current
```

`yield`:

1. Produces a value
2. Pauses the function
3. Remembers its state
4. Continues from the same place on the next iteration

This is essentially iterator state management handled by Python.

---

# `yield from`

This:

```python
yield from traverse(current.left)
```

means:

> Yield every item produced by this nested generator.

So:

```text
Parent Generator
       ↓
Child Generator
       ↓
Yield values one by one
```

---

# Generator Traversal Flow

For:

```text
      1
     / \
    2   3
```

call:

```python
traverse_in_order(root)
```

Flow:

```text
Traverse 1
 ↓
Traverse left 2
 ↓
Yield 2
 ↓
Yield 1
 ↓
Traverse right 3
 ↓
Yield 3
```

Output:

```text
2
1
3
```

---

# Usage

```python
for node in traverse_in_order(root):
    print(node.value)
```

The returned generator is itself an iterator.

---

# Manual Iterator vs Generator

## Manual Iterator

```text
InOrderIterator
```

You explicitly manage:

```text
Current node
Parent navigation
Traversal state
StopIteration
```

Advantages:

- Full control
- Can expose additional iterator operations
- Useful when traversal state is complex or reusable

---

## Generator

```python
yield
```

Python manages:

```text
State
Next value
Pausing
Resuming
StopIteration
```

Advantages:

- Much shorter
- Easier to understand
- Very natural in Python

---

# Comparison

| Manual Iterator | Generator |
|---|---|
| Implement `__iter__` | Generator automatically supports iteration |
| Implement `__next__` | Use `yield` |
| Manage state manually | Python stores generator state |
| Raise `StopIteration` | Happens automatically |
| More control | Less code |

For many Python traversal cases:

> **Generator is usually the simpler implementation.**

---

# Different Tree Iterators

The same tree could expose different traversal strategies.

```text
Tree
├── InOrderIterator
├── PreOrderIterator
└── PostOrderIterator
```

Same data:

```text
      1
     / \
    2   3
```

Different traversal:

```text
In-order
→ 2, 1, 3

Pre-order
→ 1, 2, 3

Post-order
→ 2, 3, 1
```

The underlying `Node` objects do not need to change.

---

# Real-World Examples

## Database Result Iterator

Instead of loading:

```text
1,000,000 records
```

into memory at once:

```text
Database
   ↓
Iterator
   ↓
Record
Record
Record
...
```

Rows can be processed progressively.

---

## File Iterator

Python files support:

```python
for line in file:
    ...
```

The caller does not need to know how:

- File buffering works
- Disk reads happen
- Current position is tracked

---

## Paginated API Iterator

Suppose an API returns:

```text
Page 1
Page 2
Page 3
...
```

The caller might simply use:

```python
for user in users:
    ...
```

while an iterator internally:

```text
Fetch Page 1
Yield users
Fetch Page 2
Yield users
...
```

The pagination details are hidden.

---

# Internal vs External Iteration

Useful distinction:

## External Iterator

The client explicitly controls iteration.

Example:

```python
iterator = iter(root)

next(iterator)
next(iterator)
```

The client decides:

```text
When to ask for next item
```

---

## Internal Iteration

The traversal mechanism controls iteration.

Example:

```python
collection.for_each(callback)
```

or similar APIs.

The client provides behavior, and the collection controls traversal.

Python's normal iterator protocol is primarily an external iteration model.

---

# Iterator and Encapsulation

Iterator helps preserve encapsulation.

Without an Iterator, the caller may need direct access to:

```text
left
right
parent
internal collection
```

With Iterator:

```text
for item in collection:
```

is enough.

The data structure can potentially change internally while traversal API stays stable.

---

# Iterator vs Visitor

These can be confused because both often involve traversing structures.

## Iterator

Answers:

> **How do I move through the elements?**

```text
Tree
 ↓
Iterator
 ↓
Node
Node
Node
```

---

## Visitor

Answers:

> **What operation should I perform on different element types?**

```text
Element
 ↓
Visitor
 ↓
Operation
```

Easy revision:

```text
Iterator
→ Traversal

Visitor
→ Operation on elements
```

---

# Iterator vs Composite

Composite often creates tree structures.

Example:

```text
Folder
├── File
├── Folder
│   ├── File
│   └── File
```

Iterator can then provide:

```text
Traversal through that Composite structure.
```

So these patterns often work together.

---

# When to Use Iterator

Use Iterator when:

- Data structure has complex traversal
- Client should not know internal representation
- Multiple traversal strategies are needed
- Multiple independent traversals should be possible
- You want uniform traversal across different collections

---

# Benefits

Iterator provides:

- Encapsulated traversal logic
- Simple client API
- Multiple traversal strategies
- Independent simultaneous iterators
- Separation between storage and traversal
- Consistent iteration interface

---

# Drawbacks

Iterator may introduce:

- Additional classes
- Additional state
- More complexity for simple collections

In Python, generators often eliminate much of this boilerplate.

---

# Interview Question

## What is the Iterator Pattern?

Iterator is a behavioral design pattern that provides sequential access to elements of a collection without exposing the collection's internal structure.

For example, traversing a binary tree requires logic for moving left, right, and back to parent nodes.

Instead of forcing the client to understand that logic, an `InOrderIterator` encapsulates it.

The client can simply write:

```python
for node in root:
    print(node.value)
```

while the Iterator determines which node comes next.

---

# What Is the Difference Between Iterable and Iterator?

An iterable:

```text
Can produce an iterator
```

and typically implements:

```python
__iter__()
```

An iterator:

```text
Tracks traversal state
Produces the next item
```

and implements:

```python
__iter__()
__next__()
```

---

# What Does `StopIteration` Mean?

`StopIteration` tells Python:

> There are no more elements.

Example:

```python
raise StopIteration
```

When a `for` loop encounters it, the loop ends automatically.

---

# Why Use a Generator Instead?

Generators implement iterator behavior with much less code.

Instead of manually tracking:

```text
Current state
Next node
Stop condition
```

we can write:

```python
yield node
```

and Python handles the iterator machinery.

---

# How to Recognize Iterator

Look for this requirement:

> "I need to traverse a collection or complex structure, but I don't want callers to know how traversal works internally."

Then:

```text
Collection
   ↓
Iterator
   ↓
Elements
```

is a good fit.

---

# Mental Model

Think of a playlist.

Internally, songs may be stored in:

```text
Array
Linked List
Database
Remote API
```

The user just wants:

```text
Next Song
Next Song
Next Song
```

The Iterator knows how to find the next item.

The user does not need to understand the storage mechanism.

---

# Quick Revision

```text
Iterator
→ Behavioral Design Pattern
```

```text
Purpose
→ Traverse elements without exposing internal structure
```

```text
Iterable
→ __iter__()
→ Produces iterator
```

```text
Iterator
→ __iter__()
→ __next__()
```

```text
Traversal End
→ StopIteration
```

```text
Our Example

Node
 ↓
InOrderIterator
 ↓
2 → 1 → 3
```

```text
In-order
→ Left → Node → Right
```

```text
Generator
→ yield
→ Python manages iterator state
```

```text
Manual Iterator
→ More control

Generator
→ Less boilerplate
```

---

# Key Takeaways

- **Iterator is a behavioral design pattern.**
- **It separates traversal logic from the underlying data structure.**
- **An iterable produces an iterator; an iterator produces elements one at a time.**
- **Python iterators implement `__iter__()` and `__next__()`.**
- **`StopIteration` indicates that traversal has finished.**
- **`Node.__iter__()` makes the tree directly usable in a `for` loop.**
- **`InOrderIterator` encapsulates all parent/left/right traversal logic.**
- **In-order traversal is Left → Current → Right.**
- **Iterator state belongs to the iterator, allowing multiple independent traversals over the same collection.**
- **Generators using `yield` are often the simplest way to implement iterators in Python.**
- **Iterator controls traversal; Visitor controls what operation is performed on visited elements.**
- **Complex structures such as trees, paginated APIs, files, and database results are common Iterator use cases.**

# One-Line Revision

> **Iterator = hide how a collection is traversed and give the client a simple “give me the next element” interface.**