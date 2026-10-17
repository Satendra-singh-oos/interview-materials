# Mediator Design Pattern

Mediator is a **behavioral design pattern**.

> **Mediator introduces a central object that coordinates communication between multiple components so those components do not need to reference and communicate with each other directly.**

Simple idea:

Without Mediator:

```text
Component A ─────→ Component B
     ↓                 ↑
Component C ─────→ Component D
     ↑                 ↓
     └─────────────────┘
```

Many components know about many other components.

With Mediator:

```text
        Component A
             ↓
Component B → Mediator ← Component C
             ↑
        Component D
```

Components primarily communicate with:

```text
Mediator
```

rather than directly with each other.

---

# Why Do We Need Mediator?

Suppose we have several components:

```text
A
B
C
D
```

If every component communicates directly with every other component:

```text
A knows B
A knows C
A knows D

B knows A
B knows C
B knows D
...
```

the system becomes highly coupled.

Adding or removing one component can require changes in several others.

Mediator changes this to:

```text
Component
   ↓
Mediator
   ↓
Other Components
```

The components become less dependent on each other.

---

# Real-World Examples

Typical examples:

```text
Chat Room
Multiplayer Game
Air Traffic Control
UI Dialog / Form
Event Broker
Message Bus
```

---

# Chat Room Analogy

Without a chat room:

```text
Alice must know Bob
Alice must know Charlie

Bob must know Alice
Bob must know Charlie

Charlie must know Alice
Charlie must know Bob
```

With a mediator:

```text
Alice ──┐
Bob   ──┼──→ ChatRoom
Charlie ┘
```

The `ChatRoom` knows who is currently participating and coordinates communication.

---

# 1. Classic Mediator — Chat Room

We have two main participants:

```text
Person
ChatRoom
```

`Person` is a component.

`ChatRoom` is the Mediator.

---

# Person

```python
class Person:
    def __init__(self, name):
        self.name = name
        self.chatroom = None
        self.chat_log = []

    def receive(
        self,
        from_person,
        message
    ):
        session_msg = (
            f"{from_person}: {message}"
        )

        print(
            f"[{self.name}'s chat session] "
            f"{session_msg}"
        )

        self.chat_log.append(
            session_msg
        )

    def send(self, message):
        self.chatroom.broadcast(
            self.name,
            message
        )

    def private_message(
        self,
        to_person,
        message
    ):
        self.chatroom.direct_message(
            self.name,
            to_person,
            message
        )
```

Notice what `Person.send()` does:

```python
self.chatroom.broadcast(...)
```

It does **not** directly find every other Person and message them.

That responsibility belongs to:

```text
ChatRoom
```

---

# ChatRoom — The Mediator

```python
class ChatRoom:
    def __init__(self):
        self.people = []

    def join(self, person):
        join_msg = (
            f"{person.name} joins the chat"
        )

        self.broadcast(
            "room",
            join_msg
        )

        person.chatroom = self
        self.people.append(person)
```

When a new Person joins:

```text
Person
  ↓
ChatRoom.join()
  ↓
Register person
  ↓
Notify existing participants
```

The Person does not need to know who is already inside the room.

---

# Broadcast

```python
def broadcast(
    self,
    from_person,
    message
):
    for person in self.people:
        if person.name != from_person:
            person.receive(
                from_person,
                message
            )
```

If Alice says:

```python
alice.send(
    "Hello everyone!"
)
```

flow becomes:

```text
Alice
  ↓
ChatRoom.broadcast()
  ↓
--------------------
|                  |
Bob             Charlie
 ↓                  ↓
receive()         receive()
```

Alice does not send messages directly to Bob or Charlie.

---

# Direct Message

```python
def direct_message(
    self,
    from_person,
    to_person,
    message
):
    for person in self.people:
        if person.name == to_person:
            person.receive(
                from_person,
                message
            )
            break
```

Even private communication still goes through:

```text
ChatRoom
```

Example:

```python
alice.private_message(
    "Bob",
    "Hello Bob!"
)
```

Flow:

```text
Alice
  ↓
ChatRoom
  ↓
Find Bob
  ↓
Bob.receive()
```

Alice still does not need a direct reference to Bob.

---

# Complete Example

```python
chatroom = ChatRoom()

alice = Person("Alice")
bob = Person("Bob")

chatroom.join(alice)
chatroom.join(bob)

alice.send(
    "Hello everyone!"
)

bob.send(
    "Hi Alice!"
)

charlie = Person("Charlie")
chatroom.join(charlie)

charlie.send(
    "Hey folks, what's up?"
)

alice.private_message(
    "Bob",
    "Hello Bob!"
)
```

---

# What Did Mediator Solve?

Without Mediator:

```text
Person
→ Know every other Person
→ Handle routing
→ Handle broadcasting
→ Handle private messaging
```

With Mediator:

```text
Person
→ Send/receive messages

ChatRoom
→ Know participants
→ Route messages
→ Broadcast
→ Direct message
```

Communication logic is centralized.

---

# Components Can Come and Go

One major benefit of Mediator is that participants can be dynamic.

Example:

```text
Alice joins
Bob joins
Charlie joins
Bob leaves
David joins
```

Other users do not need their internal logic rewritten.

They continue talking through:

```text
ChatRoom
```

This is especially useful for:

```text
Chat rooms
Multiplayer games
Dynamic UI components
Event-driven systems
```

---

# Mediator Structure

Classic form:

```text
            Mediator
           /   |    \
          /    |     \
Component A Component B Component C
```

Components communicate indirectly:

```text
A
↓
Mediator
↓
B
```

instead of:

```text
A
↓
B
```

---

# 2. Mediator Using Events

Your second example implements mediation through an:

> **Event Broker**

Instead of the mediator explicitly calling components, components subscribe to mediator events.

Structure:

```text
Player
  ↓
Game.fire()
  ↓
Game Event
  ↓
--------------------
|                  |
Coach A          Coach B
```

The `Game` acts as the mediator.

---

# Event

```python
class Event(list):
    def __call__(
        self,
        *args,
        **kwargs
    ):
        for item in self:
            item(
                *args,
                **kwargs
            )
```

This stores subscribed handlers.

Example:

```text
game.events

├── coach1.on_goal_scored
└── coach2.on_goal_scored
```

Calling:

```python
game.events(info)
```

notifies all subscribers.

---

# Game — Mediator / Event Broker

```python
class Game:
    def __init__(self):
        self.events = Event()

    def fire(self, args):
        self.events(args)
```

The `Game` becomes the central communication mechanism.

Components do not need direct references to each other.

---

# GoalScoredInfo

Events normally carry information.

```python
class GoalScoredInfo:
    def __init__(
        self,
        team_name,
        goals_scored
    ):
        self.team_name = team_name
        self.goals_scored = goals_scored
```

This is an:

> **Event data object**

It contains information about what happened.

---

# Player

```python
class Player:
    def __init__(
        self,
        name,
        team_name,
        game
    ):
        self.name = name
        self.team_name = team_name
        self.game = game
        self.goals_scored = 0
```

Notice:

```text
Player knows Game
```

but does not know:

```text
Coach A
Coach B
Other subscribers
```

That is loose coupling.

---

# Player Scores

Correct version:

```python
def score(self):
    self.goals_scored += 1

    info = GoalScoredInfo(
        self.team_name,
        self.goals_scored
    )

    self.game.fire(info)
```

Flow:

```text
Player scores
    ↓
Update own score
    ↓
Create GoalScoredInfo
    ↓
Game.fire()
    ↓
Notify subscribers
```

---

# Important Correction

Your original code had:

```python
GoalScoredInfo(
    self.team_name,
    1
)
```

That means every event says:

```text
goals_scored = 1
```

even after the player's second or third goal.

It should be:

```python
GoalScoredInfo(
    self.team_name,
    self.goals_scored
)
```

so the event carries the actual total.

---

# Coach

A Coach subscribes to the Game mediator.

```python
class Coach:
    def __init__(self, name, game):
        self.name = name

        game.events.append(
            self.on_goal_scored
        )
```

The Coach does not need to know:

```text
Player 1
Player 2
Player 3
```

It only listens to the mediator.

---

# Coach Handler

```python
def on_goal_scored(self, info):
    if (
        isinstance(
            info,
            GoalScoredInfo
        )
        and
        info.goals_scored < 3
    ):
        print(
            f"Coach {self.name}: "
            f"Team {info.team_name} "
            f"scored a goal! "
            f"Total goals: "
            f"{info.goals_scored}"
        )
```

Flow:

```text
Game Event
   ↓
Coach receives it
   ↓
Is GoalScoredInfo?
   ↓
Condition satisfied?
   ↓
React
```

---

# Usage

```python
game = Game()

coach1 = Coach(
    "Coach A",
    game
)

coach2 = Coach(
    "Coach B",
    game
)

player1 = Player(
    "Player 1",
    "Team A",
    game
)

player2 = Player(
    "Player 2",
    "Team B",
    game
)

player1.score()
player2.score()
player1.score()
```

---

# Communication Flow

When Player 1 scores:

```text
Player 1
   ↓
Game.fire(info)
   ↓
Event
   ↓
-------------------
|                 |
Coach A         Coach B
```

Player 1 does not know:

```text
How many coaches exist
Who they are
What they will do
```

The mediator handles communication.

---

# Why Is This Better?

Without mediator/event broker:

```python
player.score()

coach1.goal_scored(...)
coach2.goal_scored(...)
scoreboard.update(...)
analytics.track(...)
commentator.announce(...)
```

Now Player directly depends on:

```text
Coach
Scoreboard
Analytics
Commentator
...
```

Every new feature requires changing Player.

Bad coupling.

With mediator:

```python
game.fire(
    GoalScoredInfo(...)
)
```

New listeners can subscribe without changing Player.

---

# Adding a New Component

Suppose later we add:

```text
Scoreboard
```

It simply subscribes:

```python
game.events.append(
    scoreboard.on_goal_scored
)
```

Player remains unchanged.

Likewise we could add:

```text
Analytics
Commentator
AchievementSystem
NotificationService
```

without modifying the Player.

---

# Classic Mediator vs Event-Based Mediator

## Classic Mediator

Mediator explicitly knows participants.

Example:

```text
ChatRoom
├── Alice
├── Bob
└── Charlie
```

and directly routes messages.

```text
Alice
 ↓
ChatRoom
 ↓
Bob
```

---

## Event-Based Mediator

Components publish events.

Mediator distributes them to subscribers.

```text
Player
 ↓
Game/Event Broker
 ↓
Subscribers
```

Publisher often does not know who receives the event.

This provides even looser coupling.

---

# Mediator vs Observer

This distinction is important because your second example uses both ideas.

## Observer

Main intent:

> Notify multiple subscribers when something changes.

```text
Subject
 ↓
Observer A
Observer B
Observer C
```

---

## Mediator

Main intent:

> Coordinate communication between components so they do not communicate directly.

```text
Component A
   ↓
Mediator
   ↓
Component B
```

---

# Why the Second Example Looks Like Both

Your `Game`:

```text
Game.events
```

acts as an event broker.

Coaches are:

```text
Observers / Subscribers
```

But architecturally:

```text
Game
```

is also mediating communication between:

```text
Players
Coaches
Other game components
```

So:

> Mediator and Observer can be used together.

Patterns describe intent, and implementations can combine multiple patterns.

---

# Mediator vs Facade

These are easy to confuse.

## Facade

Purpose:

> Give the client a simple interface to a complex subsystem.

```text
Client
 ↓
Facade
 ↓
Subsystem
```

Communication is mainly:

```text
Client → Subsystem
```

---

## Mediator

Purpose:

> Coordinate communication among components.

```text
Component A
   ↓
Mediator
   ↓
Component B
```

Communication is:

```text
Component ↔ Component
```

through the mediator.

Easy revision:

```text
Facade
→ Simplifies subsystem usage

Mediator
→ Coordinates subsystem participants
```

---

# Mediator vs Observer

Easy revision:

```text
Observer
→ Something happened; notify subscribers
```

```text
Mediator
→ Components need to communicate; coordinate them centrally
```

---

# Mediator vs Message Broker

In distributed systems, a message broker follows a similar architectural idea:

```text
Producer
  ↓
Message Broker
  ↓
Consumer
```

Producer does not directly call each consumer.

Examples conceptually include:

```text
RabbitMQ
Kafka
Event Bus
```

However:

> A distributed message broker is infrastructure, while Mediator is an object-oriented design pattern.

The decoupling idea is similar.

---

# Air Traffic Control Example

Without Mediator:

```text
Plane A talks to Plane B
Plane A talks to Plane C
Plane B talks to Plane C
...
```

Very dangerous and tightly coupled.

Instead:

```text
Plane A ─┐
Plane B ─┼→ Air Traffic Control
Plane C ─┘
```

ATC coordinates:

```text
Takeoff
Landing
Altitude
Runway
Traffic
```

Planes do not need to coordinate directly with every other plane.

This is a very strong Mediator analogy.

---

# UI Example

Suppose a dialog contains:

```text
Checkbox
Dropdown
Button
TextBox
```

Rules might be:

```text
Checkbox checked
→ Enable textbox

Dropdown changed
→ Disable button

Button clicked
→ Validate everything
```

Without Mediator, every UI control may know about other controls.

Instead:

```text
Checkbox ─┐
Dropdown ─┼→ Dialog Mediator
Button   ─┤
TextBox  ─┘
```

The Dialog coordinates interaction.

---

# When to Use Mediator

Use Mediator when:

- Many components communicate with each other
- Components are tightly coupled
- Communication logic is duplicated
- Components frequently enter/leave the system
- Communication rules should be centralized
- You want components to depend on a common coordinator instead of each other

---

# Benefits

Mediator provides:

- Loose coupling
- Centralized communication logic
- Easier component replacement
- Easier addition/removal of components
- Reduced direct dependencies
- Better separation of responsibilities

---

# Drawbacks

Mediator can become too powerful.

Suppose:

```text
Mediator
├── Every routing rule
├── Every business rule
├── Every state transition
├── Every validation
└── Every interaction
```

Then the mediator becomes:

> **God Object / God Class**

This replaces many component dependencies with one huge central dependency.

So the Mediator should coordinate communication, not absorb all business logic.

---

# Another Drawback — Hidden Flow

Without Mediator:

```text
A → B
```

is easy to see.

With an event mediator:

```text
A
 ↓
Event
 ↓
?
```

several subscribers may react.

This can make debugging harder because communication becomes indirect.

Good:

```text
Loose coupling
```

Trade-off:

```text
Less obvious control flow
```

---

# Mediator and SRP

Without Mediator:

```text
Player
├── Player behavior
├── Notify coach
├── Update scoreboard
├── Notify analytics
└── Notify commentator
```

Too many communication responsibilities.

With Mediator:

```text
Player
→ Player behavior

Game
→ Communication coordination
```

This can help separation of concerns.

---

# Mediator and OCP

Suppose we add:

```text
AchievementSystem
```

With direct communication, `Player` might need modification.

With event-based mediation:

```text
AchievementSystem
→ Subscribe to Game events
```

Player remains unchanged.

This supports extension with less modification to existing components.

---

# Interview Question

## What is the Mediator Pattern?

Mediator is a behavioral design pattern that centralizes communication between components so they do not need direct references to one another.

For example, in a chat application:

```text
Alice
Bob
Charlie
```

do not send messages directly to each other.

They communicate through:

```text
ChatRoom
```

The ChatRoom knows the participants and routes broadcast and private messages.

This reduces coupling and allows participants to enter or leave without requiring other participants to change.

---

# Event-Based Mediator Interview Example

In a game:

```text
Player
 ↓
Game/Event Broker
 ↓
Coach
Scoreboard
Analytics
```

The Player publishes:

```text
GoalScoredInfo
```

without knowing which components are listening.

This combines Mediator-style communication with Observer-style event subscription.

---

# How to Recognize Mediator

Look for:

> "These components are starting to know too much about each other."

For example:

```text
A knows B
A knows C
B knows A
B knows C
C knows A
...
```

Then consider:

```text
A ─┐
B ─┼→ Mediator
C ─┘
```

---

# Mental Model

Think:

```text
Group of people
```

Instead of everyone maintaining direct connections:

```text
Everyone ↔ Everyone
```

introduce:

```text
Central Coordinator
```

Then:

```text
Everyone ↔ Coordinator
```

The coordinator manages interaction.

That is the Mediator mindset.

---

# Quick Revision

```text
Mediator
→ Behavioral Design Pattern
```

```text
Goal
→ Reduce direct communication between components
```

```text
Without Mediator

A ↔ B
A ↔ C
B ↔ C
```

```text
With Mediator

A ─┐
B ─┼→ Mediator
C ─┘
```

```text
Chat Example

Person
 ↓
ChatRoom
 ↓
Other Person
```

```text
Game Example

Player
 ↓
Game/Event Broker
 ↓
Coach
```

```text
Classic Mediator
→ Explicitly routes communication
```

```text
Event Mediator
→ Publishes events to subscribers
```

```text
Observer
→ Notify subscribers
```

```text
Mediator
→ Coordinate communication
```

```text
Facade
→ Simplify subsystem
```

```text
Mediator
→ Connect subsystem components
```

---

# Key Takeaways

- **Mediator is a behavioral design pattern.**
- **It centralizes communication between components.**
- **Components communicate through the Mediator rather than referring directly to one another.**
- **This reduces coupling between participants.**
- **In your first example, `ChatRoom` is the Mediator and `Person` objects are components.**
- **Broadcast and private messages are routed through `ChatRoom`.**
- **The second example uses `Game` as an event-based Mediator/Event Broker.**
- **Players publish events without knowing which Coaches or other components are listening.**
- **The event-based implementation also demonstrates Observer concepts.**
- **Mediator and Observer can be combined; their intent is different.**
- **Components can be added or removed with fewer changes to other components.**
- **A Mediator should coordinate communication, not become a God Object containing all business logic.**

# One-Line Revision

> **Mediator = when many components need to communicate, make them talk through one coordinator instead of giving every component direct knowledge of every other component.**