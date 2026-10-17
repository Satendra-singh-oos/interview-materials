# Observer Design Pattern

Observer is a **behavioral design pattern**.

> **Observer defines a one-to-many relationship between objects so that when one object produces an event or changes state, all interested subscribers are notified automatically.**

Simple idea:

```text
           Subject
              |
       state/event changes
              ↓
       -----------------
       |       |       |
   Observer  Observer  Observer
      A         B         C
```

The Subject does not need to directly know what every Observer will do.

It simply:

```text
publishes an event
        ↓
subscribers react
```

---

# Why Do We Need Observer?

Suppose a `Person` becomes sick.

We may want several things to happen:

```text
Call Doctor
Notify Family
Update Medical System
Send Alert
```

Without Observer, `Person` might directly call all of them:

```python
doctor.call(...)
family.notify(...)
medical_system.update(...)
```

Now `Person` is tightly coupled to every dependent component.

Adding another reaction means modifying `Person`.

With Observer:

```text
Person
  ↓
falls_ill event
  ↓
----------------------
|         |          |
Doctor   Family   Medical System
```

`Person` only emits:

```text
"I fell ill."
```

It does not need to know who is listening.

---

# Main Participants

Observer normally contains:

## Subject / Observable

The object that generates events or state changes.

Example:

```text
Person
```

---

## Observer / Subscriber

The object or function interested in those changes.

Example:

```text
Doctor
TrafficAuthority
UI Component
Logger
```

---

## Subscription

Observers register themselves with the Subject.

```text
Observer
   ↓
subscribe
   ↓
Subject
```

---

## Notification

When something happens:

```text
Subject
   ↓
notify()
   ↓
Observers
```

---

# 1. Basic Event-Based Observer

Your first example uses an `Events` object.

```python
class Events(list):
    def __call__(self, *args, **kwargs):
        for func in self:
            func(*args, **kwargs)
```

This behaves like a list of subscribers.

Example:

```text
falls_ill

├── lambda subscriber
├── call_doc
└── another subscriber
```

Calling:

```python
person.falls_ill(...)
```

executes every registered function.

---

# Person

```python
class Person:
    def __init__(self, name, address):
        self.name = name
        self.address = address

        self.falls_ill = Events()

    def catch_a_cold(self):
        self.falls_ill(
            self.name,
            self.address
        )
```

Important point:

`Person` does not say:

```python
call_doc(...)
```

directly.

Instead:

```python
self.falls_ill(...)
```

means:

> Notify anyone interested that this person became sick.

---

# Observer Function

```python
def call_doc(name, address):
    print(
        f"{name} needs a doctor "
        f"at {address}"
    )
```

We subscribe it:

```python
person.falls_ill.append(
    call_doc
)
```

Now the relationship becomes:

```text
Person
  ↓
falls_ill Event
  ↓
call_doc()
```

---

# Multiple Observers

We can attach multiple subscribers:

```python
person.falls_ill.append(
    lambda name, address:
        print(
            f"{name} needs a doctor "
            f"at {address}"
        )
)

person.falls_ill.append(
    call_doc
)
```

When:

```python
person.catch_a_cold()
```

happens:

```text
Person catches cold
       ↓
falls_ill event
       ↓
--------------------
|                  |
Subscriber 1    Subscriber 2
```

Both are notified.

This is the **one-to-many** relationship.

---

# Unsubscribing

Observers can also stop listening.

```python
person.falls_ill.remove(
    call_doc
)
```

After this:

```text
falls_ill
├── Subscriber 1
└── call_doc removed
```

The Subject does not need to change.

This dynamic subscription/unsubscription is one of Observer's main benefits.

---

# Complete Basic Example

```python
class Events(list):
    def __call__(self, *args, **kwargs):
        for func in self:
            func(*args, **kwargs)


class Person:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.falls_ill = Events()

    def catch_a_cold(self):
        self.falls_ill(
            self.name,
            self.address
        )


def call_doc(name, address):
    print(
        f"{name} needs a doctor "
        f"at {address}"
    )


person = Person(
    "John",
    "abc address"
)

person.falls_ill.append(
    call_doc
)

person.catch_a_cold()
```

---

# Important Mental Model

The Subject says:

```text
"Something happened."
```

It does not say:

```text
"Doctor, do this."
"Logger, do this."
"UI, update yourself."
```

Observers decide how they react.

That reduces coupling.

---

# 2. Property Observer

Sometimes we do not care about a general event.

We care about:

> **A particular property changing.**

Example:

```text
Person.age
```

If age changes:

```text
TrafficAuthority
```

may want to react.

---

# PropertyObservable

A simple observable base class can be:

```python
class PropertyObservable:
    def __init__(self):
        self.property_changed = Events()
```

This gives subclasses a shared:

```text
property_changed event
```

The `__get__()` and `__set__()` methods from your original example are descriptor methods and are not needed for this implementation.

---

# Person With Observable Property

```python
class Person(PropertyObservable):
    def __init__(self, age=0):
        super().__init__()
        self._age = age

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if self._age == value:
            return

        self._age = value

        self.property_changed(
            "age",
            value
        )
```

Now whenever:

```python
person.age = 18
```

the setter performs:

```text
Update age
   ↓
Emit property_changed
   ↓
Observers notified
```

---

# Why Check for Same Value?

This is useful:

```python
if self._age == value:
    return
```

Without it:

```python
person.age = 18
person.age = 18
person.age = 18
```

could generate unnecessary notifications.

Normally we notify only when:

```text
Old Value ≠ New Value
```

---

# TrafficAuthority Observer

```python
class TrafficAuthority:
    def __init__(self, person):
        self.person = person

        self.person.property_changed.append(
            self.person_age_changed
        )

    def person_age_changed(
        self,
        name,
        value
    ):
        if name != "age":
            return

        if value < 18:
            print(
                "Sorry, you are not "
                "allowed to drive"
            )
        else:
            print(
                "You are allowed to drive"
            )
```

The Observer subscribes to:

```text
Person.property_changed
```

---

# Flow

When:

```python
person.age = 17
```

we get:

```text
Person.age setter
      ↓
property_changed("age", 17)
      ↓
TrafficAuthority
      ↓
17 < 18
      ↓
Not allowed to drive
```

Then:

```python
person.age = 18
```

becomes:

```text
property_changed("age", 18)
      ↓
TrafficAuthority
      ↓
Allowed to drive
```

---

# Important Correction About Unsubscribing

Your original example removed the observer inside:

```python
person_age_changed()
```

every time it received an update.

That means:

```text
First age update
     ↓
Observer runs
     ↓
Observer removes itself
```

All future age changes would be ignored.

Only unsubscribe when the Observer is genuinely finished.

For example:

```python
def stop_observing(self):
    self.person.property_changed.remove(
        self.person_age_changed
    )
```

---

# Property Observer Structure

```text
Person
  ↓
age changes
  ↓
property_changed
  ↓
TrafficAuthority
```

This allows additional observers later:

```text
Person
  ↓
property_changed
  ↓
------------------------
|          |           |
Traffic   Insurance   UI
Authority   System
```

Person does not need to know about any of them.

---

# 3. Property Dependencies

Sometimes one property depends on another property.

Example:

```text
age
 ↓
can_vote
```

`can_vote` is not stored independently.

It is calculated from:

```python
age >= 18
```

So if age changes from:

```text
17 → 18
```

then two meaningful things changed:

```text
age
can_vote
```

Observers may care about either one.

---

# Person With Dependent Property

```python
class Person(PropertyObservable):
    def __init__(self, age=0):
        super().__init__()
        self._age = age

    @property
    def can_vote(self):
        return self._age >= 18

    @property
    def age(self):
        return self._age
```

`can_vote` depends entirely on:

```text
_age
```

---

# Detecting Dependent Property Changes

Before changing age:

```python
old_can_vote = self.can_vote
```

Then:

```python
self._age = value
```

Notify age:

```python
self.property_changed(
    "age",
    value
)
```

Then compare:

```python
if old_can_vote != self.can_vote:
```

If voting eligibility changed, notify that too.

---

# Correct Setter

```python
@age.setter
def age(self, value):
    if self._age == value:
        return

    old_can_vote = self.can_vote

    self._age = value

    self.property_changed(
        "age",
        value
    )

    if old_can_vote != self.can_vote:
        self.property_changed(
            "can_vote",
            self.can_vote
        )
```

---

# Why Is This Important?

Consider:

```text
16 → 17
```

Before:

```text
can_vote = False
```

After:

```text
can_vote = False
```

So:

```text
age changed
can_vote did NOT change
```

No need to notify:

```text
can_vote
```

---

# Crossing the Boundary

Now:

```text
17 → 18
```

Before:

```text
can_vote = False
```

After:

```text
can_vote = True
```

So we notify:

```text
age changed
can_vote changed
```

---

# Example

```python
def person_changed(name, value):
    if name == "can_vote":
        print(
            f"Voting status changed "
            f"to {value}"
        )


person = Person()

person.property_changed.append(
    person_changed
)

for age in range(16, 21):
    print(
        f"Changing age to {age}"
    )

    person.age = age
```

Output conceptually:

```text
Changing age to 16

Changing age to 17

Changing age to 18
Voting status changed to True

Changing age to 19

Changing age to 20
```

Only the transition:

```text
17 → 18
```

changes voting eligibility.

---

# Dependent Property Flow

```text
age changes
   ↓
Does can_vote result change?
   ↓
          Yes
           ↓
Notify can_vote observers
```

This becomes important when properties are derived from other state.

---

# Push vs Pull Observer

There are two common notification styles.

## Push Model

Subject sends the relevant data directly.

Example:

```python
property_changed(
    "age",
    18
)
```

The Subject pushes:

```text
Property Name
New Value
```

to the observer.

Your examples use this style.

---

# Pull Model

Subject may send only:

```text
"Something changed."
```

Then the Observer asks:

```python
person.age
```

to retrieve the current state.

Conceptually:

```text
Subject
 ↓
Notification
 ↓
Observer
 ↓
Pull current state
```

---

# Push vs Pull

```text
Push
→ Subject sends change data

Pull
→ Observer reads needed state
```

Which one is better depends on the system.

---

# Observer Structure

Classic Observer looks like:

```text
             Subject
               |
        -----------------
        |       |       |
    Observer Observer Observer
```

Subject maintains subscribers:

```text
subscribe()
unsubscribe()
notify()
```

Observers provide something like:

```text
update()
```

---

# Event-Based Version in Your Example

Instead of explicit:

```python
subscribe(observer)
```

you use:

```python
event.append(callback)
```

Instead of:

```python
notify()
```

you use:

```python
event(...)
```

Same core idea.

---

# Real-World Backend Example — Order Events

Suppose:

```text
Order
  ↓
OrderPlaced Event
```

Several components care:

```text
Payment
Inventory
Email
Analytics
```

Without Observer:

```python
payment.process()
inventory.reserve()
email.send()
analytics.track()
```

inside Order logic.

With events:

```text
OrderPlaced
    ↓
------------------------
|       |       |      |
Payment Stock   Email Analytics
```

The Order does not need to know every consumer.

---

# Real-World Example — UI

Suppose:

```text
User changes profile
```

Several UI elements might need updating.

```text
User Model
   ↓
Property Changed
   ↓
----------------------
|        |           |
Header   Profile     Sidebar
```

Observer is common in:

- UI frameworks
- Reactive systems
- Event-driven systems
- Model-view architectures

---

# Observer vs Mediator

These patterns are closely related.

## Observer

Main question:

> **Who wants to know that something happened?**

```text
Subject
 ↓
Observers
```

Purpose:

```text
Notification
```

---

## Mediator

Main question:

> **How should multiple components communicate without knowing each other directly?**

```text
Component
 ↓
Mediator
 ↓
Component
```

Purpose:

```text
Communication coordination
```

---

# Why They Often Appear Together

Your previous Mediator example had:

```text
Player
 ↓
Game
 ↓
Coach
```

The `Game` acted as:

```text
Mediator
```

while its event subscribers were:

```text
Observers
```

Patterns can be combined.

---

# Observer vs Pub/Sub

These ideas are similar but not identical.

## Observer

Usually:

```text
Subject directly maintains observers
```

Example:

```text
person.falls_ill
```

The Subject owns the subscriber list.

---

## Publish/Subscribe

Usually includes a separate broker.

```text
Publisher
   ↓
Message Broker
   ↓
Subscriber
```

Publisher and Subscriber may not know each other at all.

Examples conceptually include:

```text
Event Bus
Message Broker
RabbitMQ
Kafka
```

Easy revision:

```text
Observer
→ Subject manages subscribers

Pub/Sub
→ Broker sits between publishers and subscribers
```

---

# Observer vs Chain of Responsibility

## Observer

One event can be delivered to:

```text
many subscribers
```

Conceptually:

```text
          Observer A
         /
Subject → Observer B
         \
          Observer C
```

Usually all interested observers receive it.

---

## Chain of Responsibility

Request travels through:

```text
Handler A
 ↓
Handler B
 ↓
Handler C
```

A handler may stop the chain.

Easy revision:

```text
Observer
→ Broadcast notification

Chain of Responsibility
→ Pass request through handlers
```

---

# Benefits

Observer provides:

- Loose coupling
- Dynamic subscriptions
- Multiple reactions to one event
- Easy extension
- Better separation of concerns
- Event-driven architecture support

---

# Drawbacks

Observer also introduces problems.

## Hidden Control Flow

This:

```python
person.catch_a_cold()
```

may trigger:

```text
Doctor
Logger
Notification
Analytics
...
```

The caller may not easily know everything that happens.

---

## Subscriber Lifecycle

Observers should unsubscribe when necessary.

Otherwise long-lived Subjects may retain references to observers.

This can cause:

```text
Memory leaks
Unexpected callbacks
Stale listeners
```

depending on the implementation.

---

## Notification Order

If multiple subscribers exist:

```text
Observer A
Observer B
Observer C
```

code may accidentally depend on their execution order.

That creates fragile behavior.

Observers should ideally not rely heavily on ordering unless the design explicitly guarantees it.

---

## Exceptions

If:

```text
Observer B
```

throws an exception, you must decide:

```text
Should Observer C still run?
```

A production event system normally needs an explicit policy.

---

# When to Use Observer

Use Observer when:

- One object's change matters to multiple others
- Subscribers should be added dynamically
- Publisher should not know concrete subscribers
- Event-driven behavior is useful
- Properties/state changes need notifications

---

# When Not to Use Observer

Avoid it when:

- There is exactly one known receiver
- A direct method call is clearer
- Event flow would become too difficult to trace
- Strong ordering/transactional guarantees are required and Observer does not provide them

Do not replace every direct method call with events.

---

# Interview Question

## What is the Observer Pattern?

Observer is a behavioral design pattern that defines a one-to-many relationship between a Subject and its Observers.

When the Subject changes state or produces an event, all subscribed Observers are notified automatically.

For example, a `Person` can expose a `falls_ill` event.

Doctor, logging, or notification functions can subscribe to that event without the `Person` class directly depending on them.

This allows new observers to be added or removed without modifying the Subject.

---

# How to Recognize Observer

Look for this requirement:

> "When this object changes or something happens, several other components may need to know about it."

Then:

```text
Subject
 ↓
Event
 ↓
Subscribers
```

is a good candidate.

---

# Mental Model

Think about a YouTube channel.

```text
Channel
   ↓
Uploads Video
   ↓
Subscribers notified
```

The channel does not individually ask:

```text
Subscriber A, do this.
Subscriber B, do this.
Subscriber C, do this.
```

Subscribers register interest.

When something happens, they are notified.

That is the Observer mindset.

---

# Quick Revision

```text
Observer
→ Behavioral Design Pattern
```

```text
Relationship
→ One Subject
→ Many Observers
```

```text
Subject
→ Publishes changes/events
```

```text
Observer
→ Subscribes and reacts
```

```text
Subscribe
→ Add callback
```

```text
Unsubscribe
→ Remove callback
```

```text
Basic Example

Person
 ↓
falls_ill
 ↓
call_doc
```

```text
Property Observer

age changes
 ↓
property_changed
 ↓
TrafficAuthority
```

```text
Dependent Property

age
 ↓
can_vote
```

```text
Push
→ Event carries data
```

```text
Pull
→ Observer reads current state
```

```text
Mediator
→ Coordinate communication
```

```text
Observer
→ Notify interested subscribers
```

```text
Pub/Sub
→ Usually introduces a broker
```

---

# Key Takeaways

- **Observer is a behavioral design pattern.**
- **It creates a one-to-many dependency between a Subject and its subscribers.**
- **The Subject publishes changes/events without depending on concrete Observers.**
- **Observers can subscribe and unsubscribe dynamically.**
- **Your `Events` class is a simple callback-based Observer implementation.**
- **`Person.falls_ill` demonstrates general event notification.**
- **`property_changed` demonstrates observing object-property changes.**
- **Derived properties such as `can_vote` may also need notifications when their underlying dependencies change.**
- **Avoid duplicate notifications when a property is assigned the same value.**
- **Observers should unsubscribe when they are genuinely no longer interested.**
- **Observer and Mediator can work together but solve different problems.**
- **Observer and Pub/Sub are related, but Pub/Sub normally uses an intermediary broker.**
- **Observer introduces indirect control flow, so event systems should remain understandable and manageable.**

# One-Line Revision

> **Observer = when one object changes or emits an event, notify all interested subscribers automatically without making the publisher directly depend on those subscribers.**