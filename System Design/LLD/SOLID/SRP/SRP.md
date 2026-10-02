

# Single Responsibility Principle — SRP

SRP is the first principle of **SOLID**.

> **A class should have one responsibility and therefore only one reason to change.**

Another way to understand it:

> A class should focus on doing **one type of job well**.

---

# Why Do We Need SRP?

Suppose one class handles:

- Business logic
- File storage
- Database operations
- Network calls
- Logging

Then the class becomes responsible for too many things.

This makes it:

- Harder to maintain
- Harder to test
- Harder to modify
- More tightly coupled
- Easier to break

An object/class that handles too many unrelated responsibilities is often called a:

> **God Object / God Class**

This is considered an anti-pattern.

---

# Example — Journal

The responsibility of the `Journal` class should be:

> **Manage journal entries.**

```python
class Journal:
    def __init__(self):
        self.entries = []
        self.count = 0

    def add_entry(self, text):
        self.count += 1
        self.entries.append(f"{self.count}: {text}")

    def remove_entry(self, pos):
        del self.entries[pos]

    def __str__(self):
        return "\n".join(self.entries)
```

Responsibilities of this class:

```text
Journal
   ↓
Add Entry
Remove Entry
Display Entries
```

These operations belong to the journal itself.

---

# SRP Violation

Suppose we also add:

```python
def save(self, filename):
    file = open(filename, "w")
    file.write(str(self))
    file.close()

def load(self, filename):
    pass

def load_from_web(self, uri):
    pass
```

Now `Journal` has multiple responsibilities.

```text
Journal
   ├── Manage Journal Entries
   ├── Save Files
   ├── Load Files
   └── Load Data From Web
```

This violates SRP.

Why?

Because the class now has multiple **reasons to change**.

For example:

```text
Journal entry logic changes
→ Journal class changes

File storage logic changes
→ Journal class changes

Web loading logic changes
→ Journal class changes
```

The class knows too much about unrelated concerns.

---

# Better Design

Separate persistence from journal management.

```python
class Journal:
    def __init__(self):
        self.entries = []
        self.count = 0

    def add_entry(self, text):
        self.count += 1
        self.entries.append(f"{self.count}: {text}")

    def remove_entry(self, pos):
        del self.entries[pos]

    def __str__(self):
        return "\n".join(self.entries)
```

Now create another class responsible for persistence:

```python
class JournalManager:

    @staticmethod
    def save(journal, filename):
        with open(filename, "w") as file:
            file.write(str(journal))

    @staticmethod
    def load(journal, filename):
        pass

    @staticmethod
    def load_from_web(journal, uri):
        pass
```

Now responsibilities are separated:

```text
Journal
→ Manage journal entries

JournalManager
→ Save / Load journal data
```

---

# Why Is This Better?

If journal business logic changes:

```text
Change Journal
```

If file-storage logic changes:

```text
Change JournalManager
```

The two responsibilities are separated.

This gives:

- Better maintainability
- Easier testing
- Lower coupling
- Smaller classes
- Easier future changes

---

# Reason to Change

This is the most important SRP concept.

Bad:

```text
Journal

Reason 1:
Journal entry behavior changed

Reason 2:
File format changed

Reason 3:
Storage location changed

Reason 4:
Web API changed
```

Too many reasons to change.

Better:

```text
Journal
→ Changes when journal behavior changes
```

```text
JournalManager
→ Changes when persistence behavior changes
```

---

# Separation of Concerns

Separation of Concerns is a broader design idea.

It says:

> Different parts of a system should handle different concerns.

Example:

```text
Controller
→ HTTP handling

Service
→ Business logic

Repository
→ Database access
```

SRP applies this idea mainly at the **class/module level**.

So:

```text
Separation of Concerns
→ Broad architectural/design concept

SRP
→ A class should have one reason to change
```

They are related, but not identical.

---

# Real-World Example

Consider a `UserService`.

Bad:

```text
UserService
├── Create User
├── Validate Password
├── Send Email
├── Save Database
├── Generate PDF
└── Upload Image
```

This class is doing too much.

Better:

```text
UserService
→ User business logic

UserRepository
→ Database access

EmailService
→ Send emails

FileService
→ File handling
```

Each class has a clear responsibility.

---

# Interview Question

## What is the Single Responsibility Principle?

SRP states:

> **A class should have only one responsibility or one reason to change.**

For example, if a `Journal` class manages journal entries, it should not also handle saving files or loading data from the web.

Persistence logic should be moved into a separate class.

This reduces coupling and makes the system easier to maintain and test.

---

# How to Identify an SRP Violation?

Ask:

> **How many different reasons can cause this class to change?**

If the answer is:

```text
Business logic changes
Database changes
Email changes
File format changes
```

then the class probably has too many responsibilities.

Another signal is when the class name becomes vague:

```text
Manager
Utility
Helper
System
Processor
```

because such classes sometimes accumulate unrelated responsibilities.

---

# Important Note

SRP does **not** mean:

> Every class must have only one method.

A class can have many methods.

Example:

```text
Journal
├── add_entry()
├── remove_entry()
├── edit_entry()
└── get_entries()
```

All of these methods belong to the same responsibility:

> **Managing journal entries**

That still follows SRP.

---

# Quick Revision

```text
SRP
→ Single Responsibility Principle
```

```text
Rule
→ One class = one main responsibility
```

```text
Better definition
→ One reason to change
```

```text
Anti-pattern
→ God Class / God Object
```

```text
Journal
→ Manage entries
```

```text
Persistence Manager
→ Save / Load entries
```

```text
Benefit
→ Low coupling
→ Easy testing
→ Easy maintenance
→ Easier changes
```

# One-Line Revision

> **SRP means a class should own one cohesive responsibility and have only one reason to change.**