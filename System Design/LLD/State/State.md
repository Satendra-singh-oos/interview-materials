# State Design Pattern

State is a **behavioral design pattern**.

> **State allows an object to change its behavior when its internal state changes.**

The object may appear to behave like a different object depending on its current state.

Simple idea:

```text
Same Object
   ↓
Current State
   ↓
Different Behavior
```

---

# Real-World Mental Model — Telephone

Consider a telephone.

What you are allowed to do depends on the current state of the phone.

Example states:

```text
ON_HOOK
OFF_HOOK
CONNECTING
CONNECTED
ON_HOLD
```

Possible actions:

```text
Pick up
Dial
Hang up
Place on hold
Resume
```

But not every action is valid in every state.

For example:

```text
ON_HOOK
→ You can pick up the phone
→ You cannot talk yet
```

```text
OFF_HOOK
→ You can dial
→ You can hang up
```

```text
CONNECTED
→ You can talk
→ You can put the call on hold
→ You can hang up
```

So:

> **Behavior depends on current state.**

---

# Core Idea

Without State:

```python
if state == "OFF":
    ...
elif state == "ON":
    ...
elif state == "FAILED":
    ...
elif state == "CONNECTED":
    ...
```

As the number of states and actions grows:

```text
More States
+
More Transitions
+
More Conditions
=
Large Conditional Logic
```

State Pattern can move behavior into separate state objects.

---

# State Transition

An object moves from one state to another because something happens.

```text
Current State
    ↓
Trigger / Event
    ↓
New State
```

Example:

```text
OFF_HOOK
   ↓
CALL_DIALED
   ↓
CONNECTING
```

---

# State Machine

A formal model containing:

```text
States
+
Triggers
+
Transitions
```

is called a:

> **State Machine**

Example:

```text
OFF_HOOK
   |
CALL_DIALED
   ↓
CONNECTING
   |
CALL_CONNECTED
   ↓
CONNECTED
```

---

# State Pattern vs State Machine

This distinction is important.

## State Machine

Describes:

```text
What states exist?
What transitions are valid?
What triggers those transitions?
```

---

## State Pattern

An object-oriented design technique where:

```text
Each state can be represented as an object
```

and behavior is delegated to the current state.

Easy revision:

```text
State Machine
→ Model of states and transitions

State Pattern
→ OO implementation of state-dependent behavior
```

---

# 1. Classic State Pattern

Your first example models a switch.

States:

```text
ON
OFF
```

Operations:

```text
on()
off()
```

---

# Switch — Context

```python
class Switch:
    def __init__(self):
        self.state = OffState()

    def on(self):
        self.state.on(self)

    def off(self):
        self.state.off(self)
```

The `Switch` is the:

> **Context**

It does not decide behavior itself.

Instead:

```text
Switch
  ↓
Current State
  ↓
Handle operation
```

---

# State Base Class

```python
from abc import ABC


class State(ABC):
    def on(self, switch):
        print("Light is already on")

    def off(self, switch):
        print("Light is already off")
```

This defines operations available to states.

---

# OnState

```python
class OnState(State):
    def __init__(self):
        print("Light turned on")

    def off(self, switch):
        print("Turning light off...")
        switch.state = OffState()
```

When the light is ON:

```text
off()
→ valid transition
→ move to OffState
```

Calling:

```text
on()
```

uses the inherited behavior:

```text
Light is already on
```

---

# OffState

```python
class OffState(State):
    def __init__(self):
        print("Light turned off")

    def on(self, switch):
        print("Turning light on...")
        switch.state = OnState()
```

When the light is OFF:

```text
on()
→ valid transition
→ move to OnState
```

Calling:

```text
off()
```

results in:

```text
Light is already off
```

---

# Execution

```python
switch = Switch()
```

State:

```text
OFF
```

Then:

```python
switch.on()
```

Flow:

```text
Switch
 ↓
OffState.on()
 ↓
Switch.state = OnState
```

Now:

```text
ON
```

Then:

```python
switch.off()
```

Flow:

```text
Switch
 ↓
OnState.off()
 ↓
Switch.state = OffState
```

---

# Important State Pattern Idea

Notice that `Switch.on()` does not contain:

```python
if self.state == OFF:
```

Instead:

```python
self.state.on(self)
```

The current State object determines the behavior.

This is:

> **Polymorphism replacing large conditionals.**

---

# State Pattern Structure

Classic structure:

```text
             Context
                |
                |
           Current State
                |
       -------------------
       |                 |
    State A           State B
```

The Context delegates:

```text
request()
```

to the current State.

---

# Participants

## Context

The object whose behavior changes.

Example:

```text
Switch
```

---

## State

Common interface/base class.

Example:

```text
State
```

---

## Concrete States

Represent actual behavior for each state.

Example:

```text
OnState
OffState
```

---

# A Design Note About Constructors

Your example prints:

```text
Light turned on
Light turned off
```

inside state constructors.

That works for teaching, but in larger systems constructors usually should not contain too many side effects.

A cleaner design may separate:

```text
Entering state
```

from:

```text
Constructing state object
```

But the pattern idea remains the same.

---

# 2. Hand-Written State Machine — Telephone

This version does not create a class per state.

Instead, states and triggers are represented using enums.

---

# States

```python
from enum import Enum, auto


class State(Enum):
    OFF_HOOK = auto()
    CONNECTING = auto()
    CONNECTED = auto()
    ON_HOLD = auto()
    ON_HOOK = auto()
```

---

# Triggers

```python
class Trigger(Enum):
    CALL_DIALED = auto()
    HUNG_UP = auto()
    CALL_CONNECTED = auto()
    PLACED_ON_HOLD = auto()
    TAKEN_OFF_HOLD = auto()
    LEFT_MESSAGE = auto()
```

A Trigger causes a state transition.

---

# Rules

```python
rules = {
    State.OFF_HOOK: [
        (
            Trigger.CALL_DIALED,
            State.CONNECTING
        )
    ],

    State.CONNECTING: [
        (
            Trigger.HUNG_UP,
            State.ON_HOOK
        ),
        (
            Trigger.CALL_CONNECTED,
            State.CONNECTED
        )
    ],

    State.CONNECTED: [
        (
            Trigger.LEFT_MESSAGE,
            State.ON_HOOK
        ),
        (
            Trigger.HUNG_UP,
            State.ON_HOOK
        ),
        (
            Trigger.PLACED_ON_HOLD,
            State.ON_HOLD
        )
    ],

    State.ON_HOLD: [
        (
            Trigger.TAKEN_OFF_HOLD,
            State.CONNECTED
        ),
        (
            Trigger.HUNG_UP,
            State.ON_HOOK
        )
    ]
}
```

Each entry means:

```text
Current State
   ↓
Allowed Trigger
   ↓
Next State
```

---

# Example Transition

```text
CONNECTED
   ↓
PLACED_ON_HOLD
   ↓
ON_HOLD
```

Another:

```text
ON_HOLD
   ↓
TAKEN_OFF_HOLD
   ↓
CONNECTED
```

---

# Transition Table Mental Model

| Current State | Trigger | Next State |
|---|---|---|
| OFF_HOOK | CALL_DIALED | CONNECTING |
| CONNECTING | CALL_CONNECTED | CONNECTED |
| CONNECTING | HUNG_UP | ON_HOOK |
| CONNECTED | PLACED_ON_HOLD | ON_HOLD |
| ON_HOLD | TAKEN_OFF_HOLD | CONNECTED |
| ON_HOLD | HUNG_UP | ON_HOOK |

This table is effectively the state machine.

---

# Running the State Machine

Start:

```python
state = State.OFF_HOOK
exit_state = State.ON_HOOK
```

Then:

```text
While current state != ON_HOOK
```

show valid triggers.

Example:

```text
Current State:
CONNECTED

Available:
0: LEFT_MESSAGE
1: HUNG_UP
2: PLACED_ON_HOLD
```

The user chooses a trigger.

Then:

```python
state = rules[state][idx][1]
```

moves to the next state.

---

# Phone Flow Example

```text
OFF_HOOK
   ↓ CALL_DIALED
CONNECTING
   ↓ CALL_CONNECTED
CONNECTED
   ↓ PLACED_ON_HOLD
ON_HOLD
   ↓ TAKEN_OFF_HOLD
CONNECTED
   ↓ HUNG_UP
ON_HOOK
```

Then execution stops.

---

# Classic State vs Table-Based State Machine

## Classic State Pattern

```text
State represented by objects
```

Example:

```text
OnState
OffState
```

Behavior lives inside each state.

---

## Table-Based State Machine

```text
State represented by enum/value
Transitions represented by data
```

Example:

```text
rules[state]
```

This is often simpler when:

```text
States are simple
Transitions are mostly data
```

---

# When Is the Classic State Pattern Useful?

Use state objects when each state has substantial behavior.

Example:

```text
OrderState
├── PendingState
├── PaidState
├── ShippedState
├── DeliveredState
└── CancelledState
```

Each state may contain different behavior:

```text
cancel()
ship()
refund()
pay()
```

---

# When Is a State Machine Table Useful?

Use a transition table when behavior is mainly:

```text
State A + Trigger X → State B
```

and each transition has little additional logic.

Example:

```text
Phone call workflow
Simple device states
Protocol states
Wizard/navigation flow
```

---

# 3. Switch-Based State Machine — Combination Lock

Your final example implements a state machine using conditionals.

States:

```python
class State(Enum):
    LOCKED = auto()
    FAILED = auto()
    UNLOCKED = auto()
```

---

# Initial State

```python
code = "1234"
state = State.LOCKED
entry = ""
```

Start:

```text
LOCKED
```

---

# LOCKED State

While locked:

```python
if state == State.LOCKED:
```

the user enters digits.

Conceptually:

```text
Input
 ↓
Append to entry
 ↓
Correct so far?
```

---

# Correct Code

If:

```python
entry == code
```

then:

```python
state = State.UNLOCKED
```

Transition:

```text
LOCKED
   ↓ correct code
UNLOCKED
```

---

# Wrong Code Prefix

If:

```python
not code.startswith(entry)
```

then:

```python
state = State.FAILED
```

Example:

```text
Code = 1234
Entry = 15
```

Since:

```text
1234
```

does not start with:

```text
15
```

state becomes:

```text
FAILED
```

---

# FAILED State

```python
elif state == State.FAILED:
    print("\nFAILED")
    entry = ""
    state = State.LOCKED
```

Flow:

```text
FAILED
   ↓
Clear attempt
   ↓
LOCKED
```

The user can try again.

---

# UNLOCKED State

```python
elif state == State.UNLOCKED:
    print("\nUNLOCKED")
    break
```

Flow:

```text
UNLOCKED
   ↓
Finish
```

---

# Combination Lock State Machine

```text
             correct code
LOCKED ----------------------→ UNLOCKED
   |
   | wrong prefix
   ↓
FAILED
   |
   | reset
   ↓
LOCKED
```

---

# Important Difference in This Example

This implementation uses:

```python
if state == ...
elif state == ...
```

rather than State objects.

So this is:

> **A state machine implemented with conditional logic**

rather than the classic OO State Pattern.

Both express the same underlying idea:

```text
Behavior depends on state.
```

---

# Why State Pattern Helps

Suppose this grows into:

```text
10 states
×
15 possible operations
```

A giant conditional structure might become:

```python
if state == A:
    if action == ...
elif state == B:
    if action == ...
elif state == C:
    ...
```

This becomes hard to maintain.

State Pattern can move state-specific behavior into:

```text
StateA
StateB
StateC
```

---

# State Pattern and OCP

Suppose a system has:

```text
Pending
Approved
Rejected
```

and later we introduce:

```text
UnderReview
```

With state classes, we may add:

```text
UnderReviewState
```

without stuffing more branches into one large method.

This can support cleaner extension.

---

# State Pattern and SRP

Without State:

```text
Order
├── Order data
├── Pending behavior
├── Paid behavior
├── Shipped behavior
├── Cancelled behavior
└── Every transition rule
```

With State:

```text
Order
→ Context

PendingState
→ Pending behavior

PaidState
→ Paid behavior

ShippedState
→ Shipped behavior
```

State-specific behavior is separated.

---

# Real-World Backend Example — Order Lifecycle

Consider:

```text
CREATED
PAID
SHIPPED
DELIVERED
CANCELLED
```

Valid transitions might be:

```text
CREATED
   ↓ pay
PAID
   ↓ ship
SHIPPED
   ↓ deliver
DELIVERED
```

Cancellation might only be valid from:

```text
CREATED
PAID
```

but not:

```text
DELIVERED
```

State encapsulates these rules.

---

# Example

```text
Order = PAID
```

Calling:

```text
ship()
```

is valid.

Calling:

```text
pay()
```

again may produce:

```text
Order is already paid
```

The current state determines behavior.

---

# Real-World Example — Authentication

Possible states:

```text
LOGGED_OUT
AUTHENTICATING
AUTHENTICATED
LOCKED
```

Triggers:

```text
LOGIN
SUCCESS
FAILURE
LOGOUT
TOO_MANY_FAILURES
```

Flow:

```text
LOGGED_OUT
   ↓ LOGIN
AUTHENTICATING
   ↓ SUCCESS
AUTHENTICATED
```

or:

```text
AUTHENTICATING
   ↓ TOO_MANY_FAILURES
LOCKED
```

---

# Real-World Example — Job Processing

```text
QUEUED
RUNNING
SUCCEEDED
FAILED
RETRYING
```

Different operations may be valid depending on current state.

Example:

```text
FAILED
→ retry()
```

but:

```text
SUCCEEDED
→ retry()
```

may not make sense.

---

# State vs Strategy

These two are structurally similar.

Both may use:

```text
Context
   ↓
Behavior Object
```

But the intent differs.

---

# Strategy

Strategy answers:

> **Which algorithm should I use?**

Example:

```text
PaymentStrategy
CompressionStrategy
SortingStrategy
```

The client often chooses the Strategy.

---

# State

State answers:

> **How should this object behave in its current lifecycle state?**

Example:

```text
OrderState
PhoneState
ConnectionState
```

Transitions usually happen because events occur.

---

# Easy Revision

```text
Strategy
→ Different way to do something

State
→ Different behavior because lifecycle state changed
```

---

# State vs Command

## Command

Represents:

```text
An action/request
```

Example:

```text
HangUpCommand
```

## State

Represents:

```text
Current condition of an object
```

Example:

```text
ConnectedState
```

A Command may trigger a state transition.

```text
Command
   ↓
State transition
```

---

# State vs Memento

## State

Represents:

```text
Current behavior mode
```

Example:

```text
CONNECTED
```

## Memento

Represents:

```text
Snapshot of previous object state
```

Example:

```text
Previous connection configuration
```

Easy revision:

```text
State
→ What mode am I in now?

Memento
→ What did I look like before?
```

---

# Finite State Machine

When a system has a finite set of states:

```text
S1
S2
S3
...
```

and defined transitions between them, it is often called a:

> **Finite State Machine (FSM)**

Most examples in these notes are finite state machines.

---

# Valid and Invalid Transitions

One of the main responsibilities of a state machine is controlling valid transitions.

Example:

```text
CONNECTED
→ ON_HOLD
```

may be valid.

But:

```text
ON_HOOK
→ ON_HOLD
```

may be invalid.

This prevents impossible system states.

---

# Transition Diagram

A useful way to design stateful systems is to draw:

```text
       trigger
State A ------→ State B
```

Example:

```text
          CALL_CONNECTED
CONNECTING --------------→ CONNECTED
```

This helps before writing code.

---

# When to Use State Pattern

Use State when:

- Behavior depends heavily on current state
- There are many state-specific conditions
- State transitions are important
- Giant `if/elif` or `switch` statements are growing
- Each state has meaningful behavior
- Invalid transitions must be controlled

---

# When Not to Use State

Do not create separate state classes for:

```text
Two trivial booleans
```

if a simple condition is enough.

Example:

```python
if enabled:
    ...
```

may be clearer than creating:

```text
EnabledState
DisabledState
```

Use the pattern when state complexity justifies it.

---

# Benefits

State provides:

- Separation of state-specific behavior
- Fewer giant conditional blocks
- Explicit transitions
- Better readability
- Easier extension
- Better lifecycle modeling

---

# Drawbacks

State can introduce:

- Many small classes
- More indirection
- More complex transition management
- Overengineering for simple systems

---

# Interview Question

## What is the State Pattern?

State is a behavioral design pattern where an object's behavior changes depending on its current internal state.

Instead of using large conditional statements, state-specific behavior can be encapsulated in separate State objects.

For example, a switch can have:

```text
OnState
OffState
```

Calling:

```python
switch.off()
```

while in `OnState` transitions the Switch to `OffState`.

The same operation can behave differently depending on the current State.

---

# What Is a State Machine?

A state machine formally defines:

```text
States
Triggers
Transitions
```

Example:

```text
OFF_HOOK
   ↓ CALL_DIALED
CONNECTING
   ↓ CALL_CONNECTED
CONNECTED
```

A State Pattern implementation is one way of implementing such behavior.

---

# How to Recognize State Pattern

Look for this problem:

> "This object behaves very differently depending on what state it is currently in."

And especially:

```text
Many:
if state == ...
elif state == ...
elif state == ...
```

Then State Pattern may help.

---

# Mental Model

Think about a traffic light.

Same traffic light object:

```text
TrafficLight
```

but behavior depends on:

```text
RED
YELLOW
GREEN
```

A transition changes what happens next.

```text
RED
 ↓
GREEN
 ↓
YELLOW
 ↓
RED
```

That is the State mindset.

---

# Quick Revision

```text
State
→ Behavioral Design Pattern
```

```text
Core Idea
→ Behavior depends on current state
```

```text
Transition
→ State A + Trigger → State B
```

```text
State Machine
→ States + Triggers + Transitions
```

```text
Classic State Pattern

Context
 ↓
Current State Object
```

```text
Switch Example

OFF
 ↓ on()
ON
 ↓ off()
OFF
```

```text
Phone Example

OFF_HOOK
 ↓ CALL_DIALED
CONNECTING
 ↓ CALL_CONNECTED
CONNECTED
```

```text
Combination Lock

LOCKED
 ↓ correct code
UNLOCKED

LOCKED
 ↓ wrong code
FAILED
 ↓ reset
LOCKED
```

```text
Strategy
→ Change algorithm
```

```text
State
→ Change behavior because current state changed
```

---

# Key Takeaways

- **State is a behavioral design pattern.**
- **An object's behavior depends on its current state.**
- **A trigger/event causes transition from one state to another.**
- **A state machine formalizes states, triggers, and transitions.**
- **The classic State Pattern represents states as objects and delegates behavior to the current State.**
- **`Switch` is the Context; `OnState` and `OffState` are concrete State objects.**
- **The phone example demonstrates a table-driven state machine using enums and transition rules.**
- **The combination-lock example demonstrates a state machine using conditionals rather than separate State objects.**
- **State Pattern can replace large state-dependent `if/elif` blocks with polymorphism.**
- **Strategy changes how something is done; State changes behavior because lifecycle state changes.**
- **State machines are especially useful when valid and invalid transitions must be clearly controlled.**
- **Do not introduce separate State classes when the state logic is trivial.**

# One-Line Revision

> **State = let an object's current state decide how it behaves, and move between states through explicit triggers and transitions.**