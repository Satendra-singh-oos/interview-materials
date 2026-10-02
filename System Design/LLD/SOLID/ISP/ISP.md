# Interface Segregation Principle — ISP

ISP is the fourth principle of **SOLID**.

> **Clients should not be forced to depend on methods they do not use.**

Simple meaning:

> Prefer several small, focused interfaces over one large interface containing unrelated capabilities.

---

# Core Idea

Suppose we create one interface for every type of machine:

```python
class Machine:
    def print(self, document):
        raise NotImplementedError

    def fax(self, document):
        raise NotImplementedError

    def scan(self, document):
        raise NotImplementedError
```

This interface assumes every machine can:

```text
Print
Fax
Scan
```

That works for a modern multifunction printer.

But not every printer supports all three operations.

---

# Multi-Function Printer

A multifunction printer can implement everything:

```python
class MultiFunctionPrinter(Machine):
    def print(self, document):
        pass

    def fax(self, document):
        pass

    def scan(self, document):
        pass
```

This is fine because the device genuinely supports:

```text
Print ✅
Fax ✅
Scan ✅
```

---

# Problem — Old Fashion Printer

Suppose we have:

```python
class OldFashionPrinter(Machine):
    def print(self, document):
        pass

    def fax(self, document):
        pass

    def scan(self, document):
        raise NotImplementedError("Printer cannot scan!")
```

The old printer only supports:

```text
Print ✅
Fax ❌
Scan ❌
```

But because it implements `Machine`, its public contract says:

```text
print()
fax()
scan()
```

are available.

A caller may reasonably write:

```python
printer.scan(document)
```

because `scan()` exists in the interface.

But at runtime:

```text
NotImplementedError
```

This is bad design.

---

# Why Does This Violate ISP?

`OldFashionPrinter` is being forced to depend on:

```text
fax()
scan()
```

even though it does not support those capabilities.

The interface is too broad.

This is commonly called a:

> **Fat Interface**

---

# Fat Interface

Bad design:

```text
Machine
├── print()
├── scan()
├── fax()
├── email()
├── staple()
└── photocopy()
```

Now every implementation must support all of these methods.

But maybe:

```text
BasicPrinter
→ print only

Scanner
→ scan only

Photocopier
→ print + scan

MultiFunctionPrinter
→ print + scan + fax
```

One giant interface does not fit every client.

---

# Better Design — Split Interfaces

Instead of:

```text
Machine
→ print
→ scan
→ fax
```

create smaller capability-based interfaces.

---

# Printer Interface

```python
from abc import ABC, abstractmethod


class Printer(ABC):
    @abstractmethod
    def print(self, document):
        pass
```

Responsibility:

```text
Printing
```

---

# Scanner Interface

```python
class Scanner(ABC):
    @abstractmethod
    def scan(self, document):
        pass
```

Responsibility:

```text
Scanning
```

---

# Fax Interface

If required:

```python
class Fax(ABC):
    @abstractmethod
    def fax(self, document):
        pass
```

Responsibility:

```text
Faxing
```

---

# Old Printer

Now an old printer only implements what it actually supports:

```python
class MyPrinter(Printer):
    def print(self, document):
        print(document)
```

Its contract is:

```text
print() ✅
```

It does not expose:

```text
scan()
fax()
```

So callers cannot incorrectly assume those features exist.

---

# Photocopier

A photocopier may support:

```text
Print
+
Scan
```

So it implements both interfaces:

```python
class Photocopier(Printer, Scanner):
    def print(self, document):
        pass

    def scan(self, document):
        pass
```

This is perfectly valid.

The class only depends on capabilities it genuinely provides.

---

# Multi-Function Device

If some devices always need both printing and scanning, we can create a combined abstraction.

```python
class MultiFunctionDevice(Printer, Scanner):
    pass
```

This effectively means:

```text
MultiFunctionDevice
→ Printer
→ Scanner
```

Any implementation of `MultiFunctionDevice` must support both.

---

# Composition Example

Instead of implementing everything directly, we can compose existing implementations.

```python
class MultiFunctionMachine(MultiFunctionDevice):
    def __init__(self, printer, scanner):
        self.printer = printer
        self.scanner = scanner

    def print(self, document):
        self.printer.print(document)

    def scan(self, document):
        self.scanner.scan(document)
```

Now:

```text
MultiFunctionMachine
       ↓
-----------------
|               |
Printer       Scanner
```

The multifunction machine delegates responsibilities.

---

# Why Composition Helps Here

Suppose we already have:

```text
LaserPrinter
DocumentScanner
```

We can combine them:

```python
machine = MultiFunctionMachine(
    printer=laser_printer,
    scanner=document_scanner
)
```

Instead of rewriting printing and scanning logic.

This gives:

- Reusability
- Lower coupling
- Easier testing
- Flexible implementations

---

# Before ISP

```text
Machine
   ↓
--------------------------------
|              |               |
Printer      Scanner         Copier
```

Every class must implement:

```text
print
scan
fax
```

even if it does not support them.

Result:

```text
Empty methods
NotImplementedError
Fake implementations
```

---

# After ISP

```text
Printer
→ print()

Scanner
→ scan()

Fax
→ fax()
```

Implementations choose only the interfaces they need.

Example:

```text
BasicPrinter
→ Printer

ScannerDevice
→ Scanner

Photocopier
→ Printer + Scanner

MultiFunctionPrinter
→ Printer + Scanner + Fax
```

Much cleaner.

---

# Why Is This Better?

Benefits:

- Smaller contracts
- Less unnecessary coupling
- No unsupported methods
- Easier implementation
- Easier testing
- Easier extension
- More flexible composition

---

# Important ISP Clarification

ISP does **not** mean:

> Every interface should contain only one method.

That would be too literal.

An interface may contain multiple methods if they belong to one cohesive responsibility.

Example:

```text
Repository

save()
find_by_id()
delete()
```

These methods all belong to:

```text
Data Persistence
```

That can still satisfy ISP.

The issue is when unrelated capabilities are forced together.

---

# Real-World Example — User Service

Bad interface:

```text
UserOperations
├── create_user()
├── send_email()
├── export_pdf()
├── upload_avatar()
└── process_payment()
```

A class needing only user management now depends on many unrelated operations.

Better:

```text
UserService
→ create/update user

EmailSender
→ send email

FileUploader
→ upload files

PaymentProcessor
→ process payment
```

Each client depends only on what it needs.

---

# Real-World API Example

Suppose we have:

```text
PaymentProcessor
```

with:

```text
pay()
refund()
recurring_payment()
crypto_payment()
```

But some providers only support:

```text
pay()
```

Forcing them to implement every method causes problems.

Better:

```text
Payable
→ pay()

Refundable
→ refund()

RecurringPayment
→ charge_recurring()
```

Then:

```text
Provider A
→ Payable

Provider B
→ Payable + Refundable

Provider C
→ Payable + Refundable + RecurringPayment
```

This follows ISP.

---

# How to Identify an ISP Violation

Look for classes implementing methods like:

```python
def scan(self):
    raise NotImplementedError
```

or:

```python
def fax(self):
    pass
```

because:

> "This class does not support this."

That is a strong signal the interface may be too large.

Other signs include:

```text
Many unrelated methods in one interface
```

```text
Different implementations use only small subsets
```

```text
Methods returning unsupported errors
```

```text
Clients importing capabilities they never use
```

---

# ISP and LSP Connection

ISP can help avoid LSP violations.

Suppose:

```text
Machine
→ print
→ scan
```

and:

```text
OldPrinter(Machine)
```

throws:

```text
NotImplementedError
```

for `scan()`.

Now `OldPrinter` cannot safely substitute for `Machine`.

That creates an LSP problem too.

Splitting the interface into:

```text
Printer
Scanner
```

means `OldPrinter` only promises:

```text
Printer
```

and can correctly satisfy that contract.

---

# ISP vs SRP

They are related but different.

## SRP

Concerned with:

> **Class responsibility**

Question:

```text
How many reasons does this class have to change?
```

---

## ISP

Concerned with:

> **Interface dependencies**

Question:

```text
Is this client being forced to depend on methods it does not need?
```

---

# ISP vs LSP

## ISP

```text
Don't force unnecessary methods onto implementations.
```

## LSP

```text
A child should safely substitute for its parent.
```

A badly designed interface can often create both problems.

---

# Python Note — `abstractmethod`

If you use:

```python
@abstractmethod
```

the class should normally inherit from:

```python
ABC
```

Example:

```python
from abc import ABC, abstractmethod


class Printer(ABC):
    @abstractmethod
    def print(self, document):
        pass
```

Without `ABC`/`ABCMeta`, using `@abstractmethod` alone does not give you the normal abstract-class enforcement you expect.

---

# Interview Question

## What is the Interface Segregation Principle?

ISP states:

> **Clients should not be forced to depend on interfaces they do not use.**

For example, if a `Machine` interface contains `print()`, `scan()`, and `fax()`, an old printer that only supports printing would be forced to implement unsupported operations.

Instead, we can split the large interface into smaller interfaces such as:

```text
Printer
Scanner
Fax
```

Then each device implements only the capabilities it supports.

This reduces unnecessary coupling and avoids fake or unsupported implementations.

---

# Printer Example — Interview Explanation

Bad:

```text
Machine
→ print()
→ fax()
→ scan()
```

Problem:

```text
OldPrinter
→ print() ✅
→ fax() ❌
→ scan() ❌
```

Better:

```text
Printer
→ print()

Scanner
→ scan()

Fax
→ fax()
```

Then:

```text
OldPrinter
→ Printer

Photocopier
→ Printer + Scanner

MultiFunctionPrinter
→ Printer + Scanner + Fax
```

---

# Quick Revision

```text
ISP
→ Interface Segregation Principle
```

```text
Rule
→ Clients should depend only on methods they need
```

```text
Bad
→ One large "fat" interface
```

```text
Problem
→ Empty methods
→ Unsupported operations
→ NotImplementedError
```

```text
Better
→ Small cohesive interfaces
```

```text
Printer
→ print()
```

```text
Scanner
→ scan()
```

```text
Fax
→ fax()
```

```text
Benefit
→ Less coupling
→ Clear contracts
→ Easier implementation
```

---

# Key Takeaways

- **ISP means clients should not be forced to depend on methods they do not need.**
- **A large interface containing unrelated capabilities is called a fat interface.**
- **Unsupported or empty interface methods are a strong signal of poor interface design.**
- **Split interfaces based on cohesive capabilities.**
- **A printer should implement `Printer`; a photocopier may implement `Printer + Scanner`.**
- **ISP does not mean every interface must contain exactly one method.**
- **Composition can combine multiple capabilities without creating one huge implementation.**
- **Following ISP can also help prevent LSP violations caused by unsupported inherited behavior.**

# One-Line Revision

> **ISP = expose small, cohesive contracts so every client or implementation depends only on the capabilities it actually needs.**