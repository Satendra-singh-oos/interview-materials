# Template Method Design Pattern

Template Method is a **behavioral design pattern**.

> **Template Method defines the skeleton of an algorithm in a base class while allowing subclasses to override individual steps without changing the overall algorithm structure.**

Simple idea:

```text
Base Class
   ↓
Defines Overall Algorithm
   ↓
Step 1
Step 2
Step 3
Step 4
   ↑
Some steps implemented
by subclasses
```

The important part is:

> **The base class controls the sequence. Subclasses customize the steps.**

---

# Why Do We Need Template Method?

Suppose we have different games:

```text
Chess
Checkers
Monopoly
```

They may have different rules, but the overall game lifecycle is similar:

```text
Start Game
   ↓
Take Turns
   ↓
Check Winner
   ↓
Announce Winner
```

Without Template Method, every game might repeat this structure:

```python
start()

while not have_winner():
    take_turn()

announce_winner()
```

That creates duplicated workflow logic.

Instead, put the common algorithm into:

```text
Game
```

and allow subclasses to define:

```text
How does the game start?
How is a turn taken?
How do we know someone won?
Who is the winner?
```

---

# Core Mental Model

```text
          Game
           ↓
        run()
           ↓
    ----------------
    |      |       |
 start  take_turn  winner?
    ↑      ↑       ↑
    |      |       |
          Chess
```

`Game.run()` owns the algorithm.

`Chess` supplies the details.

---

# Base Game Class

```python
from abc import ABC, abstractmethod


class Game(ABC):

    def __init__(self, number_of_players):
        self.number_of_players = number_of_players
        self.current_player = 0

    def run(self):
        self.start()

        while not self.have_winner:
            self.take_turn()

        print(
            f"Player "
            f"{self.winning_player} wins!"
        )

    @abstractmethod
    def start(self):
        pass

    @property
    @abstractmethod
    def have_winner(self):
        pass

    @abstractmethod
    def take_turn(self):
        pass

    @property
    @abstractmethod
    def winning_player(self):
        pass
```

The most important method is:

```python
run()
```

because it defines the:

> **Template Method**

---

# Why Is `run()` the Template Method?

Because it defines the fixed algorithm:

```python
def run(self):
    self.start()

    while not self.have_winner:
        self.take_turn()

    print(
        f"Player "
        f"{self.winning_player} wins!"
    )
```

The sequence is always:

```text
1. Start game
2. Check winner
3. Take turn
4. Repeat
5. Announce winner
```

Subclasses cannot accidentally change that sequence unless they override `run()` itself.

---

# What Does the Subclass Provide?

The base class knows:

```text
WHAT steps must happen
+
IN WHAT ORDER
```

The subclass knows:

```text
HOW each game-specific step works
```

This is the core Template Method idea.

---

# Chess Implementation

```python
class Chess(Game):

    def __init__(self):
        super().__init__(2)

        self.max_turns = 10
        self.turn = 1

    def start(self):
        print(
            "Starting a game of chess "
            f"with {self.number_of_players} "
            "players."
        )

    @property
    def have_winner(self):
        return (
            self.turn
            == self.max_turns
        )

    def take_turn(self):
        print(
            f"Turn {self.turn} "
            f"taken by player "
            f"{self.current_player}"
        )

        self.turn += 1

        self.current_player = (
            1 - self.current_player
        )

    @property
    def winning_player(self):
        return self.current_player
```

`Chess` does not implement the complete game loop.

It only supplies the variable steps.

---

# Execution

```python
chess = Chess()

chess.run()
```

`Chess` inherits:

```python
run()
```

from `Game`.

Flow:

```text
Chess.run()
    ↓
Game.run()
    ↓
Chess.start()
    ↓
Chess.have_winner
    ↓
Chess.take_turn()
    ↓
Chess.have_winner
    ↓
...
    ↓
Chess.winning_player
```

This is an important example of:

> **Hollywood Principle**

---

# Hollywood Principle

Template Method is often associated with:

> **"Don't call us, we'll call you."**

Meaning:

The subclass does not control the high-level workflow.

Instead:

```text
Base Class
   ↓
calls subclass methods
```

For example:

```text
Game.run()
   ↓
Chess.start()
   ↓
Chess.take_turn()
```

The framework/base class controls the execution.

---

# What Is Fixed and What Varies?

## Fixed

The base class fixes:

```text
Start
 ↓
Play turns
 ↓
Check winner
 ↓
Announce winner
```

---

## Variable

Subclass defines:

```text
How to start
How to take a turn
How winner is detected
Who won
```

This separation is the heart of Template Method.

---

# Why `ABC` and `abstractmethod` Help

Your original example inherits from:

```python
ABC
```

but the methods were only:

```python
def start(self):
    pass
```

That does not force subclasses to implement them.

Using:

```python
@abstractmethod
```

makes the contract explicit.

If a subclass forgets to implement:

```text
start()
take_turn()
have_winner
winning_player
```

Python prevents that incomplete subclass from being instantiated.

---

# Primitive Operations

The customizable methods used by a Template Method are sometimes called:

> **Primitive Operations**

In this example:

```text
start()
take_turn()
have_winner
winning_player
```

are the steps required by:

```text
run()
```

---

# Hooks

Template Method can also provide:

> **Hooks**

A Hook is an optional method with a default implementation.

Example:

```python
class Game(ABC):

    def run(self):
        self.start()

        if self.should_print_intro():
            print("Game started")

        while not self.have_winner:
            self.take_turn()

    def should_print_intro(self):
        return True
```

A subclass may override:

```python
should_print_intro()
```

but it does not have to.

---

# Abstract Step vs Hook

```text
Abstract Step
→ Subclass MUST implement
```

```text
Hook
→ Subclass MAY override
```

This distinction is useful in framework design.

---

# Real-World Example — Data Processing

Suppose several file processors follow:

```text
Open File
 ↓
Read Data
 ↓
Process Data
 ↓
Save Result
 ↓
Close File
```

Base class:

```python
class DataProcessor:

    def process(self):
        self.open_file()
        data = self.read_data()
        result = self.transform(data)
        self.save(result)
        self.close_file()
```

Subclasses might implement:

```text
CSVProcessor
JSONProcessor
XMLProcessor
```

They customize:

```text
read_data()
transform()
```

while the overall workflow remains fixed.

---

# Backend Example — Request Processing

A backend workflow might always perform:

```text
Validate Request
      ↓
Authenticate
      ↓
Execute Business Logic
      ↓
Create Response
```

Different request handlers may customize:

```text
Validation rules
Business operation
Response transformation
```

while the base class controls the sequence.

---

# Framework Example

Template Method is common in frameworks.

The framework defines:

```text
Initialize
 ↓
Execute user logic
 ↓
Cleanup
```

Your code only implements:

```text
User-specific logic
```

The framework calls you at the appropriate point.

This is another example of:

```text
Don't call us,
we'll call you.
```

---

# Template Method vs Strategy

This is one of the most important comparisons.

Both allow algorithm variation.

But they achieve it differently.

---

## Template Method

Uses:

> **Inheritance**

```text
       Base Algorithm
            ↑
        Subclass
```

The base class controls the algorithm and subclasses override parts.

Example:

```text
Game
 ↑
Chess
```

---

## Strategy

Uses:

> **Composition**

```text
Context
   ↓
Strategy Object
```

Behavior is delegated to another interchangeable object.

Example:

```text
TextProcessor
   ↓
HtmlStrategy
```

---

# Easy Revision

```text
Template Method
→ Inheritance
→ Override parts of fixed algorithm
```

```text
Strategy
→ Composition
→ Replace whole algorithm/behavior
```

---

# Example Comparison

Template Method:

```text
Game.run()

start()
take_turn()
have_winner()
```

Subclass overrides pieces.

Strategy:

```text
TextProcessor
   ↓
FormattingStrategy
```

Context swaps one Strategy object for another.

---

# Another Important Difference

Template Method:

```text
Algorithm structure
→ usually fixed by base class
```

Strategy:

```text
Algorithm implementation
→ replaceable dynamically
```

So:

```text
Template Method
→ Fixed skeleton, customizable steps
```

```text
Strategy
→ Interchangeable algorithms
```

---

# Template Method vs State

## Template Method

Behavior varies because:

```text
Different subclass
```

is being used.

---

## State

Behavior varies because:

```text
Current runtime state
```

changed.

Easy revision:

```text
Template Method
→ Subclass customizes algorithm steps
```

```text
State
→ Current state controls behavior
```

---

# Template Method vs Builder

These may both look like sequences of steps.

## Builder

Purpose:

```text
Construct complex object
```

Example:

```text
Add address
Add job
Build Person
```

---

## Template Method

Purpose:

```text
Define fixed algorithm workflow
```

Example:

```text
Start game
Take turns
Determine winner
```

---

# Connection With OCP

Suppose we add:

```text
Checkers
```

We do not modify:

```python
Game.run()
```

Instead:

```python
class Checkers(Game):
    ...
```

provides new implementations of the variable steps.

So the common workflow remains stable while new variations are added.

---

# Connection With SRP

Without Template Method:

```text
Chess
→ Game loop + Chess rules

Checkers
→ Game loop + Checkers rules

Monopoly
→ Game loop + Monopoly rules
```

The game loop gets duplicated.

With Template Method:

```text
Game
→ Common lifecycle

Chess
→ Chess-specific behavior

Checkers
→ Checkers-specific behavior
```

Responsibilities become clearer.

---

# Important Issue in the Demo

Your example has:

```python
@property
def winning_player(self):
    return self.current_player
```

but `take_turn()` changes `current_player` after every turn.

So the returned winner is not necessarily:

```text
The player who took the final turn
```

This is fine as simplified pattern-demo logic, but should not be interpreted as real Chess winner calculation.

A real implementation would determine the winner from actual game rules.

The pattern lesson is:

```text
Game.run()
does not need to know
how Chess determines its winner.
```

That is exactly what Template Method is demonstrating.

---

# When to Use Template Method

Use it when:

- Several algorithms share the same overall structure
- Some steps vary between implementations
- You want to eliminate duplicated workflow code
- The sequence of operations should remain controlled
- A framework should call subclass/user-defined behavior
- Inheritance fits the domain naturally

---

# When Not to Use Template Method

Avoid it when:

- Variations need to change dynamically at runtime
- There are many independent dimensions of variation
- Deep inheritance hierarchies would result
- Composition would be more flexible

In those cases:

```text
Strategy
```

may be better.

---

# Benefits

Template Method provides:

- Reuse of common workflow
- Reduced code duplication
- Controlled algorithm structure
- Clear extension points
- Separation of common and variable behavior
- Framework-friendly design

---

# Drawbacks

Template Method also has trade-offs:

- Relies on inheritance
- Subclasses are coupled to base-class structure
- Too many hooks can make flow difficult to understand
- Changing the template may affect every subclass
- Runtime behavior replacement is less flexible than Strategy

---

# Interview Question

## What is the Template Method Pattern?

Template Method is a behavioral design pattern where a base class defines the overall skeleton of an algorithm while subclasses override specific steps without changing the algorithm's overall structure.

For example:

```text
Game.run()
```

defines:

```text
Start
 ↓
Take Turns
 ↓
Check Winner
 ↓
Announce Winner
```

while subclasses such as `Chess` implement:

```text
start()
take_turn()
have_winner
winning_player
```

The base class controls the workflow, and subclasses customize only the variable steps.

---

# How to Recognize Template Method

Look for:

> "Several classes perform the same high-level workflow, but some steps are implemented differently."

For example:

```text
Algorithm

Step A → Same
Step B → Different
Step C → Same
Step D → Different
```

Then:

```text
Base Class
→ Common skeleton

Subclass
→ Variable steps
```

is a strong Template Method candidate.

---

# Mental Model

Think about making a beverage.

Overall algorithm:

```text
Boil Water
   ↓
Brew
   ↓
Pour Into Cup
   ↓
Add Extras
```

Tea:

```text
Brew tea
Add lemon
```

Coffee:

```text
Brew coffee
Add milk
```

The workflow stays mostly the same.

Only particular steps vary.

That is Template Method.

---

# Quick Revision

```text
Template Method
→ Behavioral Design Pattern
```

```text
Goal
→ Define fixed algorithm skeleton
```

```text
Base Class
→ Controls workflow/order
```

```text
Subclass
→ Implements variable steps
```

```text
Our Example

Game.run()
   ↓
start()
   ↓
take_turn()
   ↓
have_winner
   ↓
winning_player
```

```text
Game
→ Template

Chess
→ Concrete implementation
```

```text
Abstract Operation
→ Must override
```

```text
Hook
→ May override
```

```text
Template Method
→ Inheritance
```

```text
Strategy
→ Composition
```

```text
Template Method
→ Customize parts of fixed algorithm
```

```text
Strategy
→ Swap algorithm/behavior
```

---

# Key Takeaways

- **Template Method is a behavioral design pattern.**
- **It defines the skeleton/order of an algorithm in a base class.**
- **Subclasses customize individual steps without changing the overall workflow.**
- **In your example, `Game.run()` is the Template Method.**
- **`Chess` supplies `start`, `take_turn`, `have_winner`, and `winning_player`.**
- **The base class calls subclass behavior—an example of the Hollywood Principle: "Don't call us, we'll call you."**
- **Required extension points are clearer when defined using `@abstractmethod`.**
- **Optional extension points are often called hooks.**
- **Template Method uses inheritance; Strategy usually uses composition.**
- **Template Method is useful when multiple implementations share the same high-level workflow.**
- **Prefer Strategy when algorithms must be freely swapped at runtime.**
- **The winner calculation in this teaching example is intentionally simplistic; the pattern is about separating the fixed game loop from game-specific rules.**

# One-Line Revision

> **Template Method = put the fixed sequence of an algorithm in the base class and let subclasses fill in or override the steps that vary.**