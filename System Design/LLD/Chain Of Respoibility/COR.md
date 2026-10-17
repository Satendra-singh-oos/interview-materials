# Chain of Responsibility Design Pattern

Chain of Responsibility is a **behavioral design pattern**.

> **It passes a request through a chain of handlers. Each handler can process the request, pass it to the next handler, or stop the chain.**

Simple idea:

```text
Request
  ↓
Handler A
  ↓
Handler B
  ↓
Handler C
```

Each handler decides:

```text
Handle?
Pass?
Stop?
```

---

# Real-World Mental Model

Think about clicking a UI element.

```text
Button
  ↓
Panel
  ↓
Window
  ↓
Application
```

The button may handle the event itself.

If not:

```text
Event propagates upward
```

until some handler processes it.

That is a common Chain of Responsibility idea.

---

# Why Do We Need It?

Suppose a request may need to pass through:

```text
Authentication
Authorization
Validation
Logging
Business Logic
```

Instead of one huge function:

```python
check_auth()
check_permission()
validate()
log()
process()
```

we can separate these responsibilities:

```text
Request
  ↓
AuthenticationHandler
  ↓
AuthorizationHandler
  ↓
ValidationHandler
  ↓
BusinessHandler
```

Each handler knows only its own responsibility.

---

# When to Use Chain of Responsibility

Use it when:

- You do not know beforehand which handler will process a request
- Multiple handlers may process the same request
- Handlers must run in a particular order
- You want to add/remove handlers dynamically
- You want to avoid tightly coupling sender and receiver
- Processing should stop when one handler decides not to continue

---

# Core Structure

```text
Client
  ↓
Handler
  ↓
Handler
  ↓
Handler
```

Each handler usually has:

```text
Reference to next handler
+
handle(request)
```

---

# Example 1 — Method Chain

We have a game creature.

```python
class Creature:
    def __init__(self, name, attack, defense):
        self.name = name
        self.attack = attack
        self.defense = defense

    def __str__(self):
        return (
            f"{self.name} "
            f"({self.attack}/{self.defense})"
        )
```

Example:

```text
Goblin
Attack = 1
Defense = 1
```

Now we want to apply different modifiers.

For example:

```text
Double attack
Increase defense
Disable bonuses
```

Instead of putting all logic inside `Creature`, each modification becomes a separate handler.

---

# Base Handler

```python
class CreatureModifier:
    def __init__(self, creature):
        self.creature = creature
        self.next_modifier = None

    def add_modifier(self, modifier):
        if self.next_modifier:
            self.next_modifier.add_modifier(
                modifier
            )
        else:
            self.next_modifier = modifier

    def handle(self):
        if self.next_modifier:
            self.next_modifier.handle()
```

The important field is:

```python
self.next_modifier
```

That creates the chain.

---

# Building the Chain

Suppose:

```python
root = CreatureModifier(goblin)

root.add_modifier(
    DoubleAttackModifier(goblin)
)

root.add_modifier(
    IncreaseDefenseModifier(goblin)
)
```

The structure becomes:

```text
Root
 ↓
DoubleAttackModifier
 ↓
IncreaseDefenseModifier
```

---

# DoubleAttackModifier

```python
class DoubleAttackModifier(
    CreatureModifier
):
    def handle(self):
        print(
            f"Doubling "
            f"{self.creature.name}'s attack"
        )

        self.creature.attack *= 2

        super().handle()
```

Important:

```python
super().handle()
```

means:

> Continue to the next handler.

Flow:

```text
Double attack
    ↓
Pass to next modifier
```

---

# IncreaseDefenseModifier

```python
class IncreaseDefenseModifier(
    CreatureModifier
):
    def handle(self):
        if self.creature.attack <= 2:
            print(
                f"Increasing "
                f"{self.creature.name}'s defense"
            )

            self.creature.defense += 1

        super().handle()
```

This handler:

```text
Checks condition
     ↓
Maybe modifies defense
     ↓
Passes request onward
```

---

# NoBonusesModifier

```python
class NoBonusesModifier(
    CreatureModifier
):
    def handle(self):
        print("No bonuses for you!")
```

Notice something very important:

```python
super().handle()
```

is NOT called.

Therefore:

```text
NoBonusesModifier
      ↓
STOP
```

Everything after it is ignored.

---

# Why This Demonstrates Chain of Responsibility

Suppose the chain is:

```text
Root
 ↓
NoBonusesModifier
 ↓
DoubleAttackModifier
 ↓
DoubleAttackModifier
 ↓
IncreaseDefenseModifier
```

Calling:

```python
root.handle()
```

reaches:

```text
NoBonusesModifier
```

which does not forward the request.

Therefore:

```text
DoubleAttackModifier
IncreaseDefenseModifier
```

never execute.

---

# Important Chain Behavior

A handler may:

## Process and Continue

```python
def handle(self):
    do_something()
    super().handle()
```

---

## Process and Stop

```python
def handle(self):
    do_something()
```

---

## Skip and Continue

```python
def handle(self):
    if condition:
        do_something()

    super().handle()
```

That is the core flexibility of Chain of Responsibility.

---

# Example Without NoBonusesModifier

Suppose:

```text
Goblin
Attack = 1
Defense = 1
```

Chain:

```text
DoubleAttack
 ↓
IncreaseDefense
```

First:

```text
Attack:
1 → 2
```

Then defense handler checks:

```text
attack <= 2
```

True.

So:

```text
Defense:
1 → 2
```

Final:

```text
Goblin (2/2)
```

---

# Handler Does Not Need to Know Entire Chain

`DoubleAttackModifier` does not know:

```text
What comes after it
```

It only knows:

```text
next_modifier
```

This reduces coupling.

---

# Chain Structure

```text
CreatureModifier
      ↑
-----------------------------
|             |             |
DoubleAttack  IncreaseDef   NoBonuses
```

Each modifier can participate in the same chain.

---

# Example 2 — Dynamic / Broker Chain

The second example takes a different approach.

Instead of physically linking:

```text
Handler A
  ↓
Handler B
  ↓
Handler C
```

we use:

```text
Event Broker
```

Handlers subscribe to events.

When a query occurs:

```text
Query
 ↓
Event Broker
 ↓
All interested handlers
```

This creates a more dynamic form of Chain of Responsibility.

---

# Concepts Used

This example combines:

```text
Chain of Responsibility
+
Observer
+
Event Broker
+
Command-Query Separation
```

So it is more advanced than the first example.

---

# Event Broker

```python
class Event(list):
    def __call__(self, *args, **kwargs):
        for item in self:
            item(*args, **kwargs)
```

`Event` stores functions/subscribers.

When called:

```python
event(sender, query)
```

it executes every subscribed handler.

Conceptually:

```text
Event
├── Handler A
├── Handler B
└── Handler C
```

---

# Query Type

```python
from enum import Enum


class WhatToQuery(Enum):
    ATTACK = 1
    DEFENSE = 2
```

The system can ask:

```text
What is this creature's attack?
```

or:

```text
What is this creature's defense?
```

---

# Query Object

```python
class Query:
    def __init__(
        self,
        creature_name,
        what_to_query,
        default_value
    ):
        self.creature_name = creature_name
        self.what_to_query = what_to_query
        self.value = default_value
```

The important field is:

```python
self.value
```

Handlers can modify it.

---

# Bidirectional Query

The request goes out with:

```text
Initial Value
```

Handlers may modify:

```text
query.value
```

Then the result comes back.

Example:

```text
Attack starts as 2
      ↓
DoubleAttackModifier
      ↓
Attack becomes 4
      ↓
Return 4
```

---

# Game as Event Broker

```python
class Game:
    def __init__(self):
        self.queries = Event()

    def perform_query(
        self,
        sender,
        query
    ):
        self.queries(sender, query)
```

`Game` coordinates queries.

Flow:

```text
Creature
  ↓
Game.perform_query()
  ↓
Event
  ↓
Subscribed modifiers
```

---

# Creature

```python
class Creature:
    def __init__(
        self,
        game,
        name,
        attack,
        defense
    ):
        self.game = game
        self.name = name
        self.initial_attack = attack
        self.initial_defense = defense
```

The creature stores:

```text
Base Attack
Base Defense
```

but the effective values are calculated dynamically.

---

# Attack Property

```python
@property
def attack(self):
    query = Query(
        self.name,
        WhatToQuery.ATTACK,
        self.initial_attack
    )

    self.game.perform_query(
        self,
        query
    )

    return query.value
```

Every time:

```python
creature.attack
```

is requested:

```text
Base Attack
   ↓
Create Query
   ↓
Send through handlers
   ↓
Return modified value
```

---

# Defense Property

Correct version:

```python
@property
def defense(self):
    query = Query(
        self.name,
        WhatToQuery.DEFENSE,
        self.initial_defense
    )

    self.game.perform_query(
        self,
        query
    )

    return query.value
```

Your original code used:

```python
self.initial_attack
```

as the default defense value.

That was a bug.

It should be:

```python
self.initial_defense
```

---

# Dynamic Creature Modifier

```python
from abc import ABC


class CreatureModifier(ABC):
    def __init__(
        self,
        game,
        creature
    ):
        self.creature = creature
        self.game = game

        self.game.queries.append(
            self.handle
        )

    def handle(
        self,
        sender,
        query
    ):
        pass
```

Creating a modifier automatically registers:

```python
self.handle
```

with the game's query event.

---

# Temporary Modifier

This example uses context managers:

```python
def __enter__(self):
    return self

def __exit__(
    self,
    exc_type,
    exc_val,
    exc_tb
):
    self.game.queries.remove(
        self.handle
    )
```

This gives us:

```python
with DoubleAttackModifier(
    game,
    goblin
):
    ...
```

Meaning:

```text
Enter block
   ↓
Modifier active
   ↓
Leave block
   ↓
Modifier removed
```

Very useful for temporary effects.

---

# Double Attack Modifier

```python
class DoubleAttackModifier(
    CreatureModifier
):
    def handle(
        self,
        sender,
        query
    ):
        if (
            sender.name
            == self.creature.name
            and
            query.what_to_query
            == WhatToQuery.ATTACK
        ):
            query.value *= 2
```

If the query is:

```text
Attack
```

for the correct creature:

```text
value *= 2
```

---

# Increase Defense Modifier

```python
class IncreaseDefenseModifier(
    CreatureModifier
):
    def handle(
        self,
        sender,
        query
    ):
        if (
            sender.name
            == self.creature.name
            and
            query.what_to_query
            == WhatToQuery.DEFENSE
        ):
            query.value += 3
```

---

# Execution Example

Start:

```text
Strong Goblin
Attack = 2
Defense = 2
```

No modifiers:

```text
Strong Goblin (2/2)
```

---

# Enter DoubleAttackModifier

```python
with DoubleAttackModifier(
    game,
    goblin
):
```

Now:

```text
Attack Query
2
 ↓
DoubleAttackModifier
 ↓
4
```

Result:

```text
Strong Goblin (4/2)
```

---

# Add IncreaseDefenseModifier

Inside:

```python
with IncreaseDefenseModifier(
    game,
    goblin
):
```

Now active handlers are:

```text
DoubleAttackModifier
IncreaseDefenseModifier
```

Attack:

```text
2 → 4
```

Defense:

```text
2 → 5
```

Result:

```text
Strong Goblin (4/5)
```

---

# Leave Inner Block

`IncreaseDefenseModifier` is removed.

We return to:

```text
DoubleAttackModifier only
```

---

# Leave Outer Block

`DoubleAttackModifier` is removed.

Now:

```text
No modifiers active
```

Result returns to:

```text
Strong Goblin (2/2)
```

---

# Why This Is Called a Dynamic Chain

Classic chain:

```text
A
↓
B
↓
C
```

is explicitly linked.

The broker-based version instead has:

```text
Event Broker
   ↓
Subscribers
```

Handlers can be:

```text
Added dynamically
Removed dynamically
Temporarily active
```

The chain is not stored as explicit `next` pointers.

---

# Classic Chain vs Broker Chain

## Classic Method Chain

```text
Handler A
  ↓
Handler B
  ↓
Handler C
```

Each handler knows its next handler.

---

## Broker Chain

```text
        Event Broker
        /    |     \
       A     B      C
```

Handlers subscribe to a central event.

This is more flexible when handlers frequently come and go.

---

# Command-Query Separation

The second example also demonstrates a basic CQS idea.

CQS says:

> Operations should either change state or return information, but ideally not both.

Here:

```text
Query
→ Ask for attack/defense
```

The Query object is used to calculate the effective value.

The modifiers do not permanently mutate:

```text
initial_attack
initial_defense
```

Instead, they modify:

```text
query.value
```

for that request.

---

# Why This Is Useful

Suppose a temporary game buff lasts:

```text
10 seconds
```

You do not necessarily want:

```python
creature.attack *= 2
```

permanently.

Instead:

```text
Base Attack = 2
```

remains unchanged.

While modifier exists:

```text
Effective Attack = 4
```

After modifier disappears:

```text
Effective Attack = 2
```

This is much cleaner for temporary effects.

---

# Real-World Backend Example — Middleware

HTTP middleware is a very common Chain of Responsibility example.

```text
Request
  ↓
Logging Middleware
  ↓
Authentication Middleware
  ↓
Authorization Middleware
  ↓
Validation Middleware
  ↓
Controller
```

Each middleware can:

```text
Continue
```

or:

```text
Stop and return response
```

Example:

```text
Authentication fails
      ↓
Return 401
      ↓
Do NOT call next handler
```

That is Chain of Responsibility.

---

# Express.js Mental Model

Conceptually:

```javascript
app.use(logging)
app.use(authenticate)
app.use(authorize)
app.use(validate)
```

Each middleware decides whether to call:

```text
next()
```

Calling `next()`:

```text
Continue chain
```

Not calling `next()`:

```text
Stop chain
```

This is almost exactly the same idea as:

```python
super().handle()
```

in your CreatureModifier example.

---

# Chain of Responsibility vs Observer

These can look similar in the broker version.

## Chain of Responsibility

Intent:

> Pass/process a request through handlers.

Handlers may:

```text
Process
Modify
Stop
Pass
```

---

## Observer

Intent:

> Notify interested subscribers that something happened.

```text
Event
 ↓
Observer A
Observer B
Observer C
```

The broker-based example combines ideas from both.

---

# Chain of Responsibility vs Decorator

Both can form chains.

## Decorator

```text
Object
 ↓
Decorator
 ↓
Decorator
```

Purpose:

> Add behavior around an object.

---

## Chain of Responsibility

```text
Request
 ↓
Handler
 ↓
Handler
```

Purpose:

> Pass a request through potential processors.

Easy revision:

```text
Decorator
→ Wrap object

Chain of Responsibility
→ Pass request
```

---

# Chain of Responsibility vs Pipeline

They are similar but not always identical.

## Pipeline

Usually:

```text
Every stage processes data
```

Example:

```text
Parse
 ↓
Validate
 ↓
Transform
 ↓
Store
```

---

## Chain of Responsibility

A handler may:

```text
Process
Skip
Stop
Pass
```

So the control flow is often more flexible.

---

# Benefits

Chain of Responsibility provides:

- Loose coupling between sender and handlers
- Easy reordering of handlers
- Easy addition/removal of handlers
- Separation of responsibilities
- Flexible request processing
- Ability to stop processing early

---

# Drawbacks

Possible disadvantages:

- Request may reach end without being handled
- Debugging long chains can be harder
- Execution order matters
- Too many handlers can make flow difficult to trace
- Hidden control flow can reduce readability

---

# When NOT to Use It

Avoid Chain of Responsibility when:

```text
There is exactly one known handler
```

and no flexibility is needed.

A direct method call is simpler.

Do not introduce a chain just because multiple methods happen to execute sequentially.

---

# Interview Question

## What is Chain of Responsibility?

Chain of Responsibility is a behavioral design pattern where a request is passed through a sequence of handlers.

Each handler can:

- Process the request
- Pass it to the next handler
- Stop further processing

For example, an HTTP request can pass through logging, authentication, authorization, and validation middleware before reaching the controller.

This reduces coupling because the sender does not need to know which handler will ultimately process the request.

---

# How to Recognize It

Look for:

> "I have a request that may need to pass through several processors, and each processor should decide what to do next."

Then:

```text
Request
 ↓
Handler
 ↓
Handler
 ↓
Handler
```

may be appropriate.

---

# Mental Model

Think about customer support.

```text
Customer Request
      ↓
Level 1 Support
      ↓
Can handle?
 /        \
Yes        No
 ↓          ↓
Done      Level 2
             ↓
          Can handle?
```

The requester does not need to know in advance which level will resolve the issue.

That is Chain of Responsibility.

---

# Quick Revision

```text
Chain of Responsibility
→ Behavioral Pattern
```

```text
Core Idea
→ Pass request through handlers
```

```text
Handler can
→ Handle
→ Pass
→ Stop
```

```text
Classic Chain
A → B → C
```

```text
Continue Chain
→ super().handle()
```

```text
Stop Chain
→ Do not call next handler
```

```text
NoBonusesModifier
→ Stops the chain
```

```text
Broker Version
→ Handlers subscribe dynamically
```

```text
Backend Example
→ Middleware chain
```

```text
Observer
→ Notify subscribers
```

```text
Chain
→ Process request through handlers
```

---

# Key Takeaways

- **Chain of Responsibility is a behavioral design pattern.**
- **A request is passed through multiple handlers.**
- **Each handler can process, ignore, pass, or stop the request.**
- **In the classic implementation, handlers are linked using `next_modifier`.**
- **Calling `super().handle()` continues the chain.**
- **Not calling it stops the chain.**
- **`NoBonusesModifier` demonstrates chain termination.**
- **The broker-based example creates a dynamic chain using events/subscribers rather than explicit next pointers.**
- **Temporary modifiers can be added and removed dynamically using context managers.**
- **The query-based version keeps base creature stats unchanged and computes effective values dynamically.**
- **HTTP middleware is one of the clearest real-world examples of Chain of Responsibility.**
- **Execution order matters, so long chains should remain understandable.**

# One-Line Revision

> **Chain of Responsibility = send a request through a sequence of handlers, where each handler decides whether to process it, pass it onward, or stop the chain.**