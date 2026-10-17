# Memento Design Pattern

Memento is a **behavioral design pattern**.

> **Memento captures an object's internal state at a particular moment so that the object can later be restored to that state without exposing its internal implementation.**

Simple mental model:

```text
Current Object State
        ↓
    Create Snapshot
        ↓
      Memento
        ↓
Continue changing object
        ↓
Need previous state?
        ↓
Restore from Memento
```

Typical uses:

- Undo / redo
- Editor history
- Game checkpoints
- State rollback
- Configuration snapshots
- Version/history systems

---

# Core Idea

Suppose a bank account goes through:

```text
Balance = 100
    ↓
Deposit 50
    ↓
Balance = 150
    ↓
Deposit 25
    ↓
Balance = 175
```

If we save snapshots:

```text
Memento 0 → 100
Memento 1 → 150
Memento 2 → 175
```

then:

```text
Undo
→ restore 150

Undo
→ restore 100

Redo
→ restore 150
```

We are not reversing the operation itself.

We are:

> **Restoring an earlier state.**

---

# Important Definition

A Memento can be thought of as:

> **A snapshot/token/handle representing an object's state at a particular moment.**

Conceptually:

```text
Object
  ↓
create_memento()
  ↓
Snapshot
```

Later:

```text
Snapshot
  ↓
restore()
  ↓
Object returns to previous state
```

---

# Main Participants

Classic Memento usually has three participants:

```text
Originator
Caretaker
Memento
```

---

# 1. Originator

The object whose state we want to save and restore.

In your example:

```text
BankAccount
```

is the Originator.

It owns:

```text
balance
```

and knows how to restore its own state.

---

# 2. Memento

The Memento contains the saved state.

```python
class Memento:
    def __init__(self, balance):
        self.balance = balance
```

For example:

```text
Memento(balance=100)
Memento(balance=150)
Memento(balance=175)
```

Each object represents a previous snapshot.

---

# 3. Caretaker

The Caretaker stores Mementos and manages history.

Conceptually:

```text
Caretaker
├── Snapshot 0
├── Snapshot 1
└── Snapshot 2
```

In your simplified example:

```python
self.changes
```

inside `BankAccount` is playing the Caretaker role too.

In a stricter implementation, history could be placed in a separate object.

---

# BankAccount

```python
class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance

        self.changes = [
            Memento(self.balance)
        ]

        self.current = 0
```

When the account starts:

```text
Balance = 100
```

we immediately save:

```text
changes[0]
→ Memento(100)
```

and:

```text
current = 0
```

---

# History Structure

After several changes:

```text
Index       Memento

0           Balance 100
1           Balance 150
2           Balance 175
```

And:

```text
current = 2
```

means:

> We are currently using snapshot 2.

---

# Creating a New Snapshot

Your `deposit()` changes the account and creates a Memento.

```python
def deposit(self, amount):
    self.balance += amount

    memento = Memento(
        self.balance
    )

    self.changes.append(
        memento
    )

    self.current += 1

    return memento
```

Flow:

```text
Balance = 100
    ↓
deposit(50)
    ↓
Balance = 150
    ↓
Create Memento(150)
    ↓
Store in history
```

---

# Example

Start:

```text
Balance = 100
```

History:

```text
[100]
 ↑
current
```

Then:

```python
deposit(50)
```

History:

```text
[100, 150]
       ↑
     current
```

Then:

```python
deposit(25)
```

History:

```text
[100, 150, 175]
            ↑
          current
```

---

# Undo

Undo moves the history pointer backwards.

```python
def undo(self):
    if self.current > 0:
        self.current -= 1

        memento = self.changes[
            self.current
        ]

        self.balance = (
            memento.balance
        )

        return memento

    return None
```

Suppose:

```text
[100, 150, 175]
            ↑
          current
```

Call:

```python
undo()
```

Now:

```text
[100, 150, 175]
       ↑
     current
```

and:

```text
Balance = 150
```

Another undo:

```text
[100, 150, 175]
 ↑
current
```

Balance becomes:

```text
100
```

---

# Redo

Redo moves forward through existing snapshots.

```python
def redo(self):
    if (
        self.current + 1
        < len(self.changes)
    ):
        self.current += 1

        memento = self.changes[
            self.current
        ]

        self.balance = (
            memento.balance
        )

        return memento

    return None
```

Suppose:

```text
[100, 150, 175]
 ↑
current
```

Call:

```python
redo()
```

Now:

```text
[100, 150, 175]
       ↑
     current
```

and:

```text
Balance = 150
```

---

# Undo / Redo Mental Model

Think of history as:

```text
100 ← 150 ← 175
```

Undo moves:

```text
←
```

Redo moves:

```text
→
```

So:

```text
Undo
→ Move backward through snapshots

Redo
→ Move forward through snapshots
```

---

# Important Issue — New Change After Undo

Consider:

```text
100
 ↓
150
 ↓
175
```

Now undo:

```text
100
 ↓
150
```

At this point `175` is still stored as redo history.

Now suppose we do:

```python
deposit(10)
```

The correct history should become:

```text
100
 ↓
150
 ↓
160
```

The old:

```text
175
```

branch should normally disappear.

This is exactly how text-editor undo/redo usually works.

---

# Corrected `deposit()`

Before adding a new state, remove everything after the current position.

```python
def deposit(self, amount):
    self.balance += amount

    # We created a new branch of history.
    self.changes = self.changes[
        :self.current + 1
    ]

    memento = Memento(
        self.balance
    )

    self.changes.append(
        memento
    )

    self.current += 1

    return memento
```

Now:

```text
100 → 150 → 175
       ↑
     undo
```

then:

```text
deposit(10)
```

produces:

```text
100 → 150 → 160
```

instead of retaining an invalid redo path to `175`.

---

# Restore From a Specific Memento

Sometimes we do not want normal undo/redo.

We may already have a particular snapshot:

```python
snapshot = account.deposit(50)
```

Later:

```python
account.restore(snapshot)
```

A simple restore could be:

```python
def restore(self, memento):
    if memento is not None:
        self.balance = (
            memento.balance
        )
```

This means:

```text
Specific Snapshot
      ↓
restore()
      ↓
Object returns to that state
```

---

# Should `restore()` Add Another History Entry?

Your implementation does:

```python
self.changes.append(memento)
```

inside `restore()`.

That means restoring an old state creates another history entry pointing to that state.

That can be valid depending on the required history semantics, but it is not essential to the Memento pattern.

Often:

```text
restore()
```

simply restores the object, while the Caretaker decides how history should be managed.

So keep these two concerns separate:

```text
Memento
→ Capture/restore state

History Manager
→ Decide which snapshots to retain
```

---

# Complete Improved Example

```python
class Memento:
    def __init__(self, balance):
        self.balance = balance


class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance

        self.changes = [
            Memento(balance)
        ]

        self.current = 0

    def deposit(self, amount):
        self.balance += amount

        # New change after undo:
        # remove old redo history.
        self.changes = self.changes[
            :self.current + 1
        ]

        memento = Memento(
            self.balance
        )

        self.changes.append(
            memento
        )

        self.current += 1

        return memento

    def restore(self, memento):
        if memento is not None:
            self.balance = (
                memento.balance
            )

    def undo(self):
        if self.current == 0:
            return None

        self.current -= 1

        memento = self.changes[
            self.current
        ]

        self.balance = (
            memento.balance
        )

        return memento

    def redo(self):
        if (
            self.current + 1
            >= len(self.changes)
        ):
            return None

        self.current += 1

        memento = self.changes[
            self.current
        ]

        self.balance = (
            memento.balance
        )

        return memento

    def __str__(self):
        return (
            f"Balance = {self.balance}"
        )
```

---

# Usage

```python
account = BankAccount(100)

account.deposit(50)
account.deposit(25)

print(account)
```

Result:

```text
Balance = 175
```

Undo:

```python
account.undo()
```

Result:

```text
Balance = 150
```

Undo again:

```python
account.undo()
```

Result:

```text
Balance = 100
```

Redo:

```python
account.redo()
```

Result:

```text
Balance = 150
```

---

# State Timeline

```text
Initial
100

deposit(50)
↓
150

deposit(25)
↓
175

undo()
↓
150

undo()
↓
100

redo()
↓
150
```

Mementos allow us to jump back to previously stored state.

---

# Memento Does Not Mean "Save Every Moment"

Important correction:

You do not necessarily save:

```text
every point in time
```

You save at meaningful:

> **Checkpoints**

For example:

```text
Before editing
After command
Before risky operation
At save point
At game checkpoint
```

Saving every tiny state may be unnecessarily expensive.

---

# Snapshot Can Contain More Than One Field

Our example only stores:

```text
balance
```

but imagine:

```python
class EditorMemento:
    def __init__(
        self,
        text,
        cursor_position,
        selection
    ):
        ...
```

One Memento might capture:

```text
Text
Cursor Position
Selection
Formatting
```

Whatever state is required to restore the Originator correctly.

---

# Black-Box Memento

With a **Black-Box Memento**:

> The Caretaker can store the Memento but should not know or manipulate its internal state.

Conceptually:

```text
Caretaker
   ↓
[Memento]
   ↓
Opaque snapshot
```

Only the Originator understands what is inside.

This gives stronger encapsulation.

---

# White-Box Memento

With a **White-Box Memento**:

> The saved state is more openly accessible.

Your current Python example:

```python
memento.balance
```

is closer to a white-box style because external code can inspect the state directly.

Example:

```python
print(
    memento.balance
)
```

The state is exposed.

---

# Black Box vs White Box

```text
Black Box

Caretaker
→ Stores Memento
→ Cannot inspect internal state

Originator
→ Creates and understands Memento
```

versus:

```text
White Box

Caretaker / client
→ May inspect Memento state
```

The trade-off is:

```text
Black Box
→ Better encapsulation

White Box
→ Simpler implementation
```

---

# Classic Memento

The classic pattern usually looks like:

```text
Originator
    ↓
create_memento()
    ↓
Memento
    ↓
Caretaker stores it
```

Later:

```text
Caretaker
    ↓
returns Memento
    ↓
Originator.restore()
```

---

# Text Editor Example

Suppose:

```text
Hello
```

then:

```text
Hello World
```

then:

```text
Hello World!!!
```

Snapshots:

```text
M1 → "Hello"
M2 → "Hello World"
M3 → "Hello World!!!"
```

Undo:

```text
M3
 ↓
M2
```

Now editor contains:

```text
Hello World
```

This is one of the clearest Memento examples.

---

# Game Checkpoint Example

Game state:

```text
Player Position
Health
Inventory
Score
Level
```

At checkpoint:

```text
Game State
    ↓
Memento
```

Player dies:

```text
Current state lost
```

Restore:

```text
Checkpoint Memento
        ↓
Game restored
```

---

# Memento vs Command

This is a very important interview distinction.

## Command

Stores:

> **What action was performed.**

Example:

```text
Deposit 100
```

Undo may perform an inverse operation:

```text
Withdraw 100
```

---

## Memento

Stores:

> **What the object's state was.**

Example:

```text
Balance = 500
```

Undo simply restores:

```text
Balance = 500
```

---

# Easy Revision

```text
Command
→ Remember operation

Memento
→ Remember state
```

---

# Example

Suppose balance is:

```text
500
```

then deposit:

```text
+100
```

Command remembers:

```text
DEPOSIT 100
```

Memento remembers:

```text
Balance = 500
```

To undo:

```text
Command
→ Execute compensation/inverse

Memento
→ Restore saved snapshot
```

---

# Memento vs Prototype

Both may copy state, but intent is different.

## Prototype

Goal:

```text
Create another object
```

by cloning an existing object.

```text
Object
 ↓
Clone
 ↓
New independent object
```

---

## Memento

Goal:

```text
Restore historical state
```

```text
Object
 ↓
Snapshot
 ↓
Store
 ↓
Restore later
```

Easy revision:

```text
Prototype
→ Object creation

Memento
→ State history / rollback
```

---

# Memento vs Serialization

Serialization converts object state into:

```text
JSON
Binary
File
Database representation
```

for storage or transfer.

Memento describes:

```text
How application state is captured
and restored
```

A Memento could internally be serialized, but they are not the same concept.

---

# Memory Trade-Off

Suppose we store a complete snapshot after every edit.

If each state is:

```text
10 MB
```

and we store:

```text
100 snapshots
```

memory could become very large.

So real systems may use:

- Limited history
- Incremental snapshots
- Deltas
- Compression
- Periodic checkpoints

Memento gives the design concept; storage strategy depends on the application.

---

# When to Use Memento

Use Memento when:

- Undo / redo is required
- State needs rollback
- Checkpoints are needed
- You want previous versions
- Restoring state should not expose object internals

---

# Benefits

Memento provides:

- State rollback
- Undo / redo
- Encapsulation
- History management
- Clean snapshot representation
- Separation between object state and history management

---

# Drawbacks

Possible problems:

- High memory usage
- Large snapshots
- Complex deep state
- Version compatibility
- Managing history branches
- Expensive snapshot creation

For large systems, blindly copying the entire object may not be practical.

---

# Interview Question

## What is the Memento Pattern?

Memento is a behavioral design pattern that captures an object's internal state at a particular point so that the object can later be restored to that state without exposing its internal implementation.

For example, a bank account might save snapshots:

```text
100
150
175
```

Undo simply moves back to:

```text
150
```

and restores that balance.

The typical participants are:

```text
Originator
Memento
Caretaker
```

The Originator creates/restores snapshots, the Memento contains the saved state, and the Caretaker stores the history.

---

# How to Recognize Memento

Look for:

> "I need to restore this object to a previous state."

Then think:

```text
Object
 ↓
Snapshot
 ↓
History
 ↓
Restore
```

Memento may be appropriate.

---

# Mental Model

Think about:

```text
Ctrl + Z
```

Before each meaningful change, the application remembers enough state to return to an earlier version.

```text
State A
 ↓
State B
 ↓
State C
```

Undo:

```text
C → B
```

Undo:

```text
B → A
```

Redo:

```text
A → B
```

That is the Memento mindset.

---

# Quick Revision

```text
Memento
→ Behavioral Design Pattern
```

```text
Goal
→ Capture and restore state
```

```text
Originator
→ Object whose state is saved
```

```text
Memento
→ Snapshot
```

```text
Caretaker
→ Stores/manages snapshots
```

```text
Undo
→ Previous snapshot
```

```text
Redo
→ Next snapshot
```

```text
Black Box
→ Snapshot internals hidden
```

```text
White Box
→ Snapshot state accessible
```

```text
Command
→ Remember action
```

```text
Memento
→ Remember state
```

```text
Prototype
→ Clone to create another object
```

```text
Memento
→ Snapshot for restoration
```

---

# Key Takeaways

- **Memento is a behavioral design pattern.**
- **It captures an object's state so that state can be restored later.**
- **Snapshots are normally created at meaningful checkpoints, not literally every moment.**
- **The Originator owns the state being saved.**
- **The Memento represents the snapshot.**
- **The Caretaker stores and manages snapshots.**
- **Undo moves backward through saved states; redo moves forward.**
- **If a new change is made after undo, old redo history should normally be discarded.**
- **Black-box Memento hides snapshot internals; white-box Memento exposes them more openly.**
- **Command stores an operation; Memento stores state.**
- **Prototype creates a new object from an existing one; Memento preserves state for restoration.**
- **Snapshot history can consume significant memory, so real systems may limit or optimize stored state.**

# One-Line Revision

> **Memento = take a snapshot of an object's state at a checkpoint, store it, and use that snapshot later to restore the object without exposing how the object stores its internal state.**