# Command Design Pattern

Command is a **behavioral design pattern**.

> **Command turns a request or operation into an object.**

Instead of directly doing:

```python id="1xg0r7"
account.deposit(100)
```

we create an object representing that request:

```python id="x57v0c"
command = BankAccountCommand(
    account,
    Action.DEPOSIT,
    100
)

command.invoke()
```

Now the operation itself has become data.

That means we can:

- Store it
- Queue it
- Log it
- Execute it later
- Retry it
- Undo it
- Group several commands together

---

# Core Mental Model

Without Command:

```text id="1xqzjr"
Client
  ↓
Receiver.method()
```

With Command:

```text id="ys0m3x"
Client
  ↓
Command Object
  ↓
Receiver
```

The Command object contains:

```text id="zfyv0m"
WHAT action to perform
+
WHICH object should perform it
+
Parameters needed for the action
```

---

# Why Do We Need Command?

Suppose a UI button directly calls:

```python id="xws8bd"
account.withdraw(100)
```

The button now knows:

- The receiver
- The method
- The parameters

Later we want:

- Undo
- Logging
- Delayed execution
- Queuing
- Auditing

Direct calls are harder to manage.

Instead:

```text id="g3jhyf"
Button
  ↓
WithdrawCommand
  ↓
BankAccount
```

The button only executes:

```python id="3kwzv9"
command.invoke()
```

It does not need to understand the operation itself.

---

# Main Participants

Classic Command Pattern usually contains:

```text id="3mpvka"
Client
Invoker
Command
ConcreteCommand
Receiver
```

---

# Receiver

The Receiver performs the actual work.

In your example:

```text id="gzk19f"
BankAccount
```

is the Receiver.

---

# BankAccount

```python id="8k6gf2"
class BankAccount:
    OVERDRAFT_LIMIT = -500

    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

        print(
            f"Deposited {amount}, "
            f"balance = {self.balance}"
        )

    def withdraw(self, amount):
        if (
            self.balance - amount
            >= BankAccount.OVERDRAFT_LIMIT
        ):
            self.balance -= amount

            print(
                f"Withdrew {amount}, "
                f"balance = {self.balance}"
            )

            return True

        return False

    def __str__(self):
        return f"Balance = {self.balance}"
```

`BankAccount` knows how to:

```text id="jffy61"
deposit()
withdraw()
```

But it does not know anything about:

```text id="143pxy"
Commands
Undo
Queues
Macro operations
```

That logic stays separate.

---

# Command Interface

```python id="tryp0d"
from abc import ABC, abstractmethod


class Command(ABC):

    @abstractmethod
    def invoke(self):
        pass

    @abstractmethod
    def undo(self):
        pass
```

This defines the operations every command supports.

Conceptually:

```text id="xbtzmc"
Command
├── invoke()
└── undo()
```

---

# Concrete Command

```python id="r85e2k"
from enum import Enum


class BankAccountCommand(Command):

    class Action(Enum):
        DEPOSIT = 0
        WITHDRAW = 1

    def __init__(
        self,
        account,
        action,
        amount
    ):
        self.account = account
        self.action = action
        self.amount = amount
        self.success = False
```

The command stores everything needed to perform the operation:

```text id="9ndkoe"
Receiver
→ account

Action
→ deposit / withdraw

Parameter
→ amount
```

---

# Invoking the Command

```python id="zi6tkq"
def invoke(self):

    if self.action == self.Action.DEPOSIT:

        self.account.deposit(
            self.amount
        )

        self.success = True

    elif self.action == self.Action.WITHDRAW:

        self.success = (
            self.account.withdraw(
                self.amount
            )
        )
```

The Command does not perform banking logic itself.

It delegates to:

```text id="rxsxb1"
BankAccount
```

---

# Flow

For:

```python id="7x8nrl"
cmd = BankAccountCommand(
    account,
    Action.DEPOSIT,
    100
)

cmd.invoke()
```

the flow is:

```text id="244ra6"
Client
  ↓
BankAccountCommand
  ↓
account.deposit(100)
  ↓
BankAccount
```

---

# Why Store `success`?

Suppose:

```python id="wnf2ld"
withdraw(1000)
```

fails because it exceeds the overdraft limit.

Then:

```text id="ejqipj"
success = False
```

If we later call:

```python id="pk8csh"
undo()
```

we should not reverse an operation that never actually happened.

That is why Command keeps execution state.

---

# Undo

```python id="m96ewj"
def undo(self):

    if not self.success:
        return

    if self.action == self.Action.DEPOSIT:

        self.account.withdraw(
            self.amount
        )

    elif self.action == self.Action.WITHDRAW:

        self.account.deposit(
            self.amount
        )
```

Conceptually:

```text id="5sy0ju"
Deposit
→ Undo using opposite operation

Withdraw
→ Undo using opposite operation
```

---

# Example

```python id="l70zid"
account = BankAccount()

command = BankAccountCommand(
    account,
    BankAccountCommand.Action.DEPOSIT,
    100
)

command.invoke()
```

Result:

```text id="uvlyqb"
Balance = 100
```

Then:

```python id="v5o5ja"
command.undo()
```

Result:

```text id="gadzxd"
Balance = 0
```

---

# Important Real-World Clarification

For this demo:

```text id="xkhqkf"
Undo deposit
→ withdraw same amount
```

works.

But in real financial systems this is usually **not a literal undo**.

You normally do not erase or reverse history as if the transaction never happened.

Instead you might create:

```text id="8cnkpp"
Original Transaction
+
Compensating Transaction
```

Example:

```text id="3efmxu"
Deposit +100
Compensation -100
```

This preserves an audit trail.

So the example demonstrates Command undo mechanics, not real banking accounting semantics.

---

# Failed Command

Suppose:

```python id="c0pxbe"
illegal_command = BankAccountCommand(
    account,
    Action.WITHDRAW,
    1000
)
```

If:

```text id="3xv589"
Withdrawal would exceed overdraft limit
```

then:

```python id="dujmuc"
self.success = False
```

Calling:

```python id="u8mtmd"
illegal_command.undo()
```

does nothing.

Correct behavior:

```text id="q8dl9x"
Command never succeeded
       ↓
Nothing to undo
```

---

# Command Pattern Structure

```text id="4nyldf"
              Command
             /      \
        invoke()    undo()
             ↑
             |
     BankAccountCommand
             |
             ↓
        BankAccount
```

---

# Command Terminology

## Receiver

Performs actual work.

```text id="962zgi"
BankAccount
```

---

## Command

Represents the request.

```text id="h3ehtp"
BankAccountCommand
```

---

## Invoker

Triggers the Command.

Could be:

```text id="icnk4h"
Button
Queue
Scheduler
Controller
```

It only needs something like:

```python id="fk0h17"
command.invoke()
```

---

## Client

Creates/configures the command.

Example:

```python id="1yvpel"
BankAccountCommand(
    account,
    DEPOSIT,
    100
)
```

---

# Why Making a Request an Object Is Powerful

Once this:

```text id="u10pvk"
Deposit $100
```

becomes an object:

```text id="ddo9cx"
DepositCommand
```

you can now put it into:

```text id="noge57"
List
Queue
Database
Log
History Stack
Scheduler
```

This is the main value of Command.

---

# Real-World Example — Job Queue

Instead of immediately:

```python id="i56ufw"
send_email()
```

you create:

```text id="122szg"
SendEmailCommand
```

and push it to:

```text id="16ex6s"
Queue
```

Later:

```text id="vfqp18"
Worker
  ↓
Command
  ↓
Email Service
```

This is conceptually very similar to background-job systems.

---

# Real-World Example — UI Undo/Redo

Text editor:

```text id="w0wh4c"
TypeCommand
DeleteCommand
PasteCommand
```

Commands can be stored:

```text id="cmublo"
History Stack
```

Undo:

```text id="qmsfe9"
Pop latest command
      ↓
command.undo()
```

Redo:

```text id="7ei446"
Execute command again
```

This is one of the classic Command Pattern applications.

---

# Composite Command

Sometimes one logical operation requires multiple Commands.

Example:

```text id="fv9pga"
Money Transfer

1. Withdraw from Account A
2. Deposit into Account B
```

Instead of treating these completely separately:

```text id="gkgoft"
WithdrawCommand
DepositCommand
```

we can combine them.

This creates a:

> **Composite Command**

Also called a:

> **Macro Command**

---

# Composite Command Mental Model

```text id="xb7n2m"
CompositeCommand
├── Command A
├── Command B
├── Command C
└── Command D
```

Calling:

```text id="ljy1tb"
composite.invoke()
```

executes all child commands.

Calling:

```text id="gsqxx4"
composite.undo()
```

undoes them.

---

# Base Command With Success State

```python id="skhdos"
class Command(ABC):
    def __init__(self):
        self.success = False

    def invoke(self):
        pass

    def undo(self):
        pass
```

All commands now have:

```text id="4znfpd"
success
```

---

# CompositeBankAccountCommand

```python id="1fmmb6"
class CompositeBankAccountCommand(
    Command,
    list
):

    def __init__(self, items=None):
        Command.__init__(self)
        list.__init__(self)

        if items is not None:
            self.extend(items)
```

Important correction:

Avoid:

```python id="nj7w8m"
def __init__(self, items=[]):
```

because mutable default arguments are shared between calls in Python.

Use:

```python id="12zqwc"
items=None
```

instead.

---

# Invoke Composite Command

```python id="y13svx"
def invoke(self):
    for command in self:
        command.invoke()
```

Flow:

```text id="59didw"
Composite
   ↓
Command 1
   ↓
Command 2
   ↓
Command 3
```

---

# Undo Composite Command

```python id="teyak6"
def undo(self):
    for command in reversed(self):
        command.undo()
```

Why reverse order?

Suppose execution was:

```text id="gwtdxm"
A
↓
B
↓
C
```

Undo should normally be:

```text id="4c7k0q"
C
↓
B
↓
A
```

This is similar to unwinding a stack.

---

# Example

```text id="829ux8"
Deposit 1000
Deposit 1000
```

Composite:

```text id="bv6js3"
Composite
├── Deposit 1000
└── Deposit 1000
```

Invoke:

```text id="um1smk"
0
↓ +1000
1000
↓ +1000
2000
```

Undo in reverse:

```text id="j80x5g"
2000
↓ -1000
1000
↓ -1000
0
```

---

# Problem With Simple Composite

Now consider a transfer:

```text id="e45zck"
Account A
    ↓
Withdraw 1000
    ↓
Account B
    ↓
Deposit 1000
```

A simple Composite executes every command regardless of whether a previous command failed.

Suppose Account A cannot withdraw 1000.

```text id="vfqt30"
Withdraw
→ FAIL
```

But the naive Composite still continues:

```text id="yzwwld"
Deposit 1000 into Account B
```

Now money has appeared in Account B even though it was never removed from Account A.

Incorrect state.

---

# This Shows an Important Lesson

A Macro/Composite Command is not automatically transactional.

```text id="on5kv2"
"Execute several commands"
```

does not automatically mean:

```text id="55gvfm"
"All succeed or all fail"
```

Those are different requirements.

---

# Better MoneyTransferCommand

```python id="7rx055"
class MoneyTransferCommand(
    CompositeBankAccountCommand
):

    def __init__(
        self,
        from_account,
        to_account,
        amount
    ):
        super().__init__([
            BankAccountCommand(
                from_account,
                BankAccountCommand.Action.WITHDRAW,
                amount
            ),

            BankAccountCommand(
                to_account,
                BankAccountCommand.Action.DEPOSIT,
                amount
            )
        ])
```

Now we override execution logic.

---

# Conditional Execution

```python id="bpnqof"
def invoke(self):
    ok = True

    for command in self:

        if ok:
            command.invoke()
            ok = command.success

        else:
            command.success = False

    self.success = ok
```

Flow:

```text id="t8t9g5"
Withdraw
   ↓
Success?
 /      \
Yes      No
 ↓        ↓
Deposit  Stop remaining
```

This is much safer than blindly executing every child command.

---

# Successful Transfer

Suppose:

```text id="ru65qq"
Account A = 1000
Account B = 0

Transfer = 500
```

Then:

```text id="94rfqj"
Withdraw 500
→ success

Deposit 500
→ success
```

Final:

```text id="gfzbw7"
Account A = 500
Account B = 500
```

and:

```text id="iwsyao"
transfer.success = True
```

---

# Failed Transfer

Suppose:

```text id="owv3wp"
Account A = 100
Transfer = 1000
```

Withdrawal fails.

```text id="57o86e"
Withdraw 1000
→ False
```

Then:

```text id="ac9l42"
Deposit command
→ Not executed
```

So:

```text id="hetv29"
Account A unchanged
Account B unchanged
```

and:

```text id="efv8jd"
transfer.success = False
```

---

# Composite + Command

This example combines two patterns.

## Command

Each operation is represented as an object.

```text id="dbp5br"
DepositCommand
WithdrawCommand
```

## Composite

A group of Commands can itself be treated as one Command.

```text id="6lr0mv"
MoneyTransferCommand
    ↓
-----------------
|               |
Withdraw      Deposit
```

This is why it is often called:

> Macro Command.

---

# Why Composite Command Is Powerful

The client can treat:

```text id="3gdiwa"
One Command
```

and:

```text id="2e35pv"
Ten Commands grouped together
```

the same way:

```python id="u3h64l"
command.invoke()
command.undo()
```

The client does not care whether it is dealing with a simple command or a composite command.

---

# Command + Undo History

We can maintain:

```text id="q9c3xp"
Command History
```

Example:

```text id="n3kdl3"
[
  DepositCommand(100),
  WithdrawCommand(20),
  DepositCommand(50)
]
```

Undo latest:

```text id="2ij66u"
history.pop().undo()
```

This is why the Command Pattern is frequently used for:

- Undo
- Redo
- Transaction history

---

# Command + Queue

Commands can also be queued.

```text id="o2j5y7"
Client
  ↓
Command
  ↓
Queue
  ↓
Worker
  ↓
Receiver
```

Because a Command is an object, it can wait before execution.

---

# Command + Logging

A system can record:

```text id="qzfzwn"
Command Type
Parameters
Timestamp
Result
```

Example:

```text id="4arn6x"
WITHDRAW
Account=123
Amount=100
Success=True
```

This can provide an audit trail.

---

# Command + Retry

If execution fails:

```text id="jdj3v9"
Command
  ↓
Failure
  ↓
Retry Queue
  ↓
Execute Again
```

Again, representing the operation as an object makes this easier.

---

# Command vs Strategy

These can sometimes look similar.

## Command

Represents:

> **What action should be performed?**

Example:

```text id="7729qy"
DepositCommand
SendEmailCommand
DeleteUserCommand
```

It can carry:

- Receiver
- Parameters
- Execution state
- Undo state

---

## Strategy

Represents:

> **How should some behavior/algorithm be performed?**

Example:

```text id="t8azut"
PaymentStrategy
SortingStrategy
CompressionStrategy
```

Easy revision:

```text id="26ln7b"
Command
→ Encapsulate a request

Strategy
→ Encapsulate an algorithm
```

---

# Command vs Chain of Responsibility

## Command

Turns a request into an object.

```text id="hnaz6d"
Request
 ↓
Command Object
```

## Chain of Responsibility

Passes a request through handlers.

```text id="qp01r5"
Request
 ↓
Handler A
 ↓
Handler B
 ↓
Handler C
```

They can also work together:

```text id="ku4scx"
Command
 ↓
Handler Chain
```

---

# Command vs Memento

Both are often involved in undo systems.

## Command

Stores:

```text id="pjzf1z"
What operation happened
```

and may know how to reverse it.

## Memento

Stores:

```text id="hr6gfc"
Previous state
```

so the object can be restored.

Simple distinction:

```text id="kprcr3"
Command
→ Undo operation

Memento
→ Restore state
```

---

# When to Use Command

Use Command when you need:

- Undo / redo
- Job queues
- Deferred execution
- Request logging
- Scheduling
- Retry logic
- Macro operations
- Auditing
- Decoupling sender from receiver

---

# When Not to Use Command

Avoid introducing Command objects for trivial direct calls if none of those capabilities are needed.

Instead of:

```text id="voxguq"
Client
→ Command
→ Receiver
```

a simple:

```python id="gkxtad"
receiver.do_something()
```

may be clearer.

Use Command when treating operations as objects gives real value.

---

# Benefits

Command provides:

- Decoupling between caller and receiver
- Undo/redo support
- Queuing
- Deferred execution
- Logging and auditing
- Retry support
- Command composition
- Flexible scheduling

---

# Drawbacks

Command may introduce:

- Many small classes
- Additional abstraction
- More object creation
- More complex undo logic
- Difficult transaction semantics

Especially:

> Not every real-world operation can be perfectly undone.

For external side effects such as:

```text id="5rynyf"
Send email
Charge credit card
Publish external event
```

you often need compensating actions rather than true reversal.

---

# Interview Question

## What is the Command Pattern?

Command is a behavioral design pattern that encapsulates a request as an object.

The Command object stores everything required to perform an operation, such as:

- Receiver
- Action
- Parameters

Because the operation is now an object, it can be queued, logged, delayed, retried, undone, or combined with other Commands.

For example, instead of directly calling:

```python id="c48lmj"
account.deposit(100)
```

we create:

```python id="r6eab0"
DepositCommand(
    account,
    100
)
```

and later execute:

```python id="3zv86q"
command.invoke()
```

---

# How to Recognize Command

Look for:

> "I need to treat an action itself as something I can store, queue, undo, retry, log, or execute later."

Then Command is a strong candidate.

---

# Mental Model

Think about a restaurant order.

The customer does not directly instruct the chef.

Instead:

```text id="zqqx9q"
Customer
  ↓
Order Ticket
  ↓
Kitchen Queue
  ↓
Chef
```

The:

```text id="ew7u3b"
Order Ticket
```

is similar to a Command object.

It contains the instruction and can be:

- Stored
- Queued
- Reordered
- Cancelled
- Executed later

---

# Quick Revision

```text id="mz9ekb"
Command
→ Behavioral Design Pattern
```

```text id="jgvu3l"
Core Idea
→ Request becomes an object
```

```text id="odl5ow"
Receiver
→ Performs real work
```

```text id="htuzsa"
Command
→ Stores operation + receiver + parameters
```

```text id="9v23b4"
invoke()
→ Execute command
```

```text id="dd2ta1"
undo()
→ Reverse/compensate command
```

```text id="czsebe"
success
→ Know whether undo should happen
```

```text id="rwz6ot"
Composite Command
→ Group commands
→ Macro
```

```text id="1m7qnj"
Composite Undo
→ Reverse order
```

```text id="dgpj62"
MoneyTransferCommand
→ Execute next step only if previous succeeds
```

```text id="34dvuo"
Main Uses
→ Queue
→ Undo/Redo
→ Logging
→ Retry
→ Scheduling
```

---

# Key Takeaways

- **Command is a behavioral design pattern.**
- **It converts a request/action into an object.**
- **The Receiver performs the actual business operation.**
- **The Command stores the receiver, action, and parameters required to perform the request.**
- **Once an operation is represented as an object, it can be stored, queued, logged, delayed, retried, or undone.**
- **`success` prevents undoing commands that never executed successfully.**
- **Composite Command groups multiple Commands into one higher-level operation.**
- **Composite undo should generally execute in reverse order.**
- **A naive Composite Command is not automatically transactional.**
- **`MoneyTransferCommand` shows how later operations can depend on earlier command success.**
- **In real financial systems, undo is usually implemented using compensating transactions rather than deleting history.**
- **Avoid mutable default arguments such as `items=[]` in Python constructors.**
- **Command represents what should happen; Strategy represents how an algorithm should happen.**

# One-Line Revision

> **Command = turn an action into an object so the action can be executed, stored, queued, logged, retried, composed, or undone independently of the code that requested it.**