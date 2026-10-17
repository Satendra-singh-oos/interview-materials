# Proxy Design Pattern

Proxy is a **structural design pattern**.

> **A Proxy is a stand-in object that controls access to another real object or resource.**

The resource may be:

- Expensive to create
- Remote
- Sensitive / protected
- Slow to access
- In need of logging
- In need of caching
- Loaded only when required

Simple mental model:

```text
Client
  ↓
Proxy
  ↓
Real Object
```

The client interacts with the Proxy as if it were interacting with the real object.

---

# Why Do We Need Proxy?

Suppose the client wants to use:

```text
Some Resource
```

but direct access is not desirable.

For example:

```text
Resource is expensive
Resource requires authorization
Resource is remote
Resource should be lazily loaded
```

Instead of:

```text
Client
  ↓
Real Resource
```

we place another object in front:

```text
Client
  ↓
Proxy
  ↓
Real Resource
```

The Proxy decides:

> Should I forward this request to the real object, delay it, block it, cache it, or perform additional work?

---

# Core Proxy Idea

A Proxy usually exposes the same or a compatible interface as the real object.

That means the client can use:

```text
Proxy
```

without needing to know whether the real resource is directly available.

For example:

```python
object.draw()
```

could be:

```text
RealImage.draw()
```

or:

```text
ImageProxy.draw()
```

The client uses the same operation.

---

# Common Types of Proxy

Some important Proxy variants are:

```text
Protection Proxy
→ Controls access

Virtual Proxy
→ Delays expensive creation

Remote Proxy
→ Represents an object on another machine/process

Caching Proxy
→ Stores previously retrieved results

Logging / Smart Proxy
→ Performs additional control around access
```

The core pattern remains:

```text
Client
→ Proxy
→ Real Object
```

---

# 1. Protection Proxy

A Protection Proxy controls:

> **Who is allowed to access the real object.**

Typical uses:

- Authentication
- Authorization
- Permission checks
- Role checks
- Age restrictions
- Security rules

---

# Car Example

Suppose we have a real `Car`.

```python
class Car:
    def __init__(self, driver):
        self.driver = driver

    def drive(self):
        print(
            f"Car is being driven by "
            f"{self.driver.name}"
        )
```

Normally:

```python
driver = Driver("John", 20)

car = Car(driver)

car.drive()
```

The `Car` itself does not perform any access check.

It simply drives.

---

# Driver

```python
class Driver:
    def __init__(self, name, age):
        self.name = name
        self.age = age
```

Suppose the rule is:

```text
Driver must be at least 18.
```

One solution would be to modify:

```python
Car.drive()
```

and add:

```python
if driver.age >= 18:
```

But now `Car` has another responsibility:

```text
Driving
+
Access control
```

Instead, we can keep the real `Car` simple and introduce a Proxy.

---

# CarProxy

```python
class CarProxy:
    def __init__(self, driver):
        self.driver = driver
        self.car = Car(driver)

    def drive(self):
        if self.driver.age >= 18:
            self.car.drive()
        else:
            print(
                f"Car cannot be driven by "
                f"{self.driver.name}"
            )
```

Now:

```text
Car
→ Responsible for driving

CarProxy
→ Responsible for access control
```

---

# Protection Proxy Flow

For an adult driver:

```text
Client
  ↓
CarProxy.drive()
  ↓
Age >= 18?
  ↓
Yes
  ↓
Car.drive()
```

For an underage driver:

```text
Client
  ↓
CarProxy.drive()
  ↓
Age >= 18?
  ↓
No
  ↓
Block access
```

---

# Example

```python
driver = Driver(
    "John",
    20
)

car = CarProxy(driver)

car.drive()
```

Flow:

```text
John age = 20
      ↓
Proxy allows access
      ↓
Real Car drives
```

Now:

```python
driver2 = Driver(
    "Bob",
    16
)

car2 = CarProxy(driver2)

car2.drive()
```

Flow:

```text
Bob age = 16
      ↓
Proxy blocks access
      ↓
Car.drive() never called
```

The actual `Car` class remains unchanged.

---

# Why This Is a Proxy

The client wants:

```text
Car behavior
```

but instead receives:

```text
CarProxy
```

The Proxy decides whether the request reaches the real Car.

```text
Client
  ↓
CarProxy
  ↓
Permission check
  ↓
Car
```

That is a Protection Proxy.

---

# Real-World Backend Example

Imagine:

```text
AdminService
```

has:

```python
delete_user()
```

Instead of modifying the service with permission logic everywhere:

```text
Client
  ↓
AuthorizationProxy
  ↓
AdminService
```

The Proxy can check:

```text
Does user have ADMIN role?
```

If yes:

```text
Forward request
```

If no:

```text
Reject request
```

---

# 2. Virtual Proxy

A Virtual Proxy is used when:

> **Creating the real object is expensive, so we delay creating it until it is actually needed.**

This is basically:

> Lazy initialization through a Proxy.

---

# Image Example

Suppose loading an image from disk is expensive.

```python
class Bitmap:
    def __init__(self, filename):
        self.filename = filename

        print(
            f"Loading image from "
            f"{filename}"
        )

    def draw(self):
        print(
            f"Drawing image "
            f"{self.filename}"
        )
```

Important point:

```python
Bitmap("facepalm.jpg")
```

immediately performs:

```text
Load Image
```

even if we never draw it.

---

# Problem

Suppose:

```python
bitmap = Bitmap(
    "facepalm.jpg"
)
```

but the program never calls:

```python
bitmap.draw()
```

We paid the loading cost unnecessarily.

That is wasteful when:

- Image is large
- File access is slow
- Resource may never be used

---

# Virtual Proxy Solution

Instead of constructing `Bitmap` immediately:

```python
class LazyBitmap:
    def __init__(self, filename):
        self.filename = filename
        self.bitmap = None
```

At this point:

```text
LazyBitmap exists
```

but:

```text
Bitmap does NOT exist yet.
```

---

# Lazy Loading

```python
def draw(self):
    if self.bitmap is None:
        self.bitmap = Bitmap(
            self.filename
        )

    self.bitmap.draw()
```

The first call to:

```python
draw()
```

does:

```text
Bitmap does not exist
      ↓
Create Bitmap
      ↓
Load image
      ↓
Draw image
```

Later calls:

```text
Bitmap already exists
      ↓
Reuse it
      ↓
Draw
```

---

# Complete Virtual Proxy

```python
class Bitmap:
    def __init__(self, filename):
        self.filename = filename

        print(
            f"Loading image from "
            f"{filename}"
        )

    def draw(self):
        print(
            f"Drawing image "
            f"{self.filename}"
        )


class LazyBitmap:
    def __init__(self, filename):
        self.filename = filename
        self.bitmap = None

    def draw(self):
        if self.bitmap is None:
            self.bitmap = Bitmap(
                self.filename
            )

        self.bitmap.draw()
```

---

# Client Function

```python
def draw_image(image):
    print("About to draw image")

    image.draw()

    print("Done drawing image")
```

Notice:

```python
draw_image()
```

does not care whether `image` is:

```text
Bitmap
```

or:

```text
LazyBitmap
```

As long as both provide:

```python
draw()
```

the client works.

---

# Usage

```python
bmp = LazyBitmap(
    "facepalm.jpg"
)
```

At this point:

```text
LazyBitmap created
```

but:

```text
Image NOT loaded yet
```

Now:

```python
draw_image(bmp)
```

causes:

```text
About to draw image
        ↓
LazyBitmap.draw()
        ↓
Real Bitmap does not exist
        ↓
Load Bitmap
        ↓
Draw Bitmap
        ↓
Done drawing image
```

---

# Second Draw

If:

```python
draw_image(bmp)
```

is called again:

```text
LazyBitmap.draw()
        ↓
Bitmap already exists
        ↓
Reuse Bitmap
        ↓
Draw
```

The expensive loading operation happens only once.

---

# Why This Is a Virtual Proxy

The `LazyBitmap` represents the real:

```text
Bitmap
```

before the Bitmap actually exists.

The client interacts with:

```text
LazyBitmap
```

as though it were the image.

The Proxy controls when the real resource gets created.

---

# Proxy Structure

Classic structure:

```text
          Subject
          /     \
       Proxy   RealSubject
          |
          |
      RealSubject
```

Conceptually:

```text
Client
  ↓
Common Interface
  ↓
Proxy
  ↓
Real Object
```

In the image example:

```text
Client
  ↓
draw()
  ↓
LazyBitmap
  ↓
Bitmap
```

---

# Common Subject Interface

A cleaner formal implementation could define:

```python
from abc import ABC, abstractmethod


class Image(ABC):

    @abstractmethod
    def draw(self):
        pass
```

Then:

```python
class Bitmap(Image):
    ...
```

and:

```python
class LazyBitmap(Image):
    ...
```

Both satisfy the same interface.

Now the client can depend on:

```text
Image
```

instead of either concrete class.

---

# 3. Remote Proxy

Another important Proxy type is:

> **Remote Proxy**

Suppose the actual object exists on another server.

Client code might think it is calling:

```python
service.get_user()
```

but internally:

```text
Client
  ↓
Remote Proxy
  ↓
HTTP / RPC / Network
  ↓
Remote Service
```

The Proxy hides:

- Serialization
- Network calls
- Deserialization
- Connection details

from the client.

---

# Remote Proxy Mental Model

The client sees:

```python
user_service.get_user(10)
```

but the Proxy may internally perform:

```text
HTTP Request
      ↓
Remote Server
      ↓
JSON Response
      ↓
Convert to User
```

The remote resource appears almost like a local object.

---

# 4. Caching Proxy

A Proxy can also cache results.

Example:

```text
Client
  ↓
Caching Proxy
  ↓
Database / Remote API
```

Flow:

```text
Request
  ↓
Cache hit?
 /       \
Yes       No
 ↓         ↓
Return    Call real service
          ↓
        Cache result
          ↓
        Return
```

This reduces expensive calls.

---

# Proxy and Additional Functionality

A Proxy can perform work:

```text
Before accessing resource
```

or:

```text
After accessing resource
```

Examples:

- Logging
- Authentication
- Caching
- Lazy initialization
- Remote communication
- Usage counting
- Rate limiting

But the defining idea is still:

> **The Proxy controls access to another object/resource.**

---

# Proxy vs Decorator

These two can look almost identical structurally.

Both may do:

```text
Wrapper
  ↓
Wrapped Object
```

The main difference is:

> **Intent**

---

## Decorator

Main goal:

> Add behavior.

Example:

```text
Coffee
 ↓
MilkDecorator
 ↓
SugarDecorator
```

or:

```text
Shape
 ↓
ColoredShape
 ↓
TransparentShape
```

---

## Proxy

Main goal:

> Control access to the real object.

Example:

```text
Client
 ↓
ProtectionProxy
 ↓
Real Service
```

or:

```text
Client
 ↓
LazyProxy
 ↓
Expensive Resource
```

---

# Easy Revision

```text
Decorator
→ Enhance object
```

```text
Proxy
→ Control access to object
```

The implementation may look similar, but the purpose is different.

---

# Proxy vs Adapter

## Adapter

Purpose:

> Make incompatible interfaces compatible.

```text
A
↓
Adapter
↓
B
```

---

## Proxy

Purpose:

> Stand in front of the same conceptual resource and control access.

```text
Client
↓
Proxy
↓
Real Object
```

Easy revision:

```text
Adapter
→ Compatibility

Proxy
→ Access control / indirection
```

---

# Proxy vs Facade

## Facade

Provides:

```text
Simple interface
```

over:

```text
Complex subsystem
```

```text
Client
 ↓
Facade
 ↓
Many subsystem objects
```

---

## Proxy

Usually represents:

```text
One underlying object/resource
```

```text
Client
 ↓
Proxy
 ↓
Real Object
```

Easy revision:

```text
Facade
→ Simplify a subsystem

Proxy
→ Represent/control another object
```

---

# Proxy vs Flyweight

## Flyweight

Goal:

```text
Reduce memory
```

by sharing common state.

## Proxy

Goal:

```text
Control access
```

to a resource.

They solve completely different problems.

---

# Protection Proxy vs Virtual Proxy

## Protection Proxy

Question:

> Is the client allowed to access this resource?

```text
Client
 ↓
Permission Check
 ↓
Real Object
```

Example:

```text
CarProxy
→ Check driver age
```

---

## Virtual Proxy

Question:

> Do we need to create this expensive resource yet?

```text
Client
 ↓
Proxy
 ↓
Resource exists?
 ↓
Create only when required
```

Example:

```text
LazyBitmap
→ Load Bitmap on first draw()
```

---

# When to Use Proxy

Use Proxy when you need to control access to another object because:

- It is expensive to create
- It should be lazily initialized
- It requires authorization
- It lives remotely
- Calls should be cached
- Calls need additional monitoring/control
- Direct access should be restricted

---

# Benefits

Proxy can provide:

- Access control
- Lazy initialization
- Remote access abstraction
- Caching
- Logging
- Reduced resource usage
- Separation of infrastructure concerns

without heavily modifying the real object.

---

# Drawbacks

Proxy also adds:

- Another layer of indirection
- Additional classes
- More debugging complexity
- Potential latency
- Potential hidden behavior

For example:

```python
service.get_data()
```

might appear local but could actually trigger:

```text
Network Request
```

through a Remote Proxy.

So Proxy abstractions should remain understandable.

---

# Interview Question

## What is the Proxy Pattern?

Proxy is a structural design pattern in which a stand-in object represents another real object and controls access to it.

The Proxy normally exposes the same interface as the real object, so the client can interact with the Proxy without needing to know whether it is using the real resource directly.

For example, a Virtual Proxy can delay loading an expensive image until `draw()` is first called, while a Protection Proxy can check authorization before forwarding a request to the real object.

---

# Interview Example — Protection Proxy

```text
Client
 ↓
CarProxy
 ↓
Check driver's age
 ↓
Car
```

The real `Car` handles driving.

The Proxy handles permission.

---

# Interview Example — Virtual Proxy

```text
Client
 ↓
LazyBitmap
 ↓
First draw?
 ↓
Create Bitmap
 ↓
Draw
```

The expensive Bitmap is not loaded until it is actually needed.

---

# How to Recognize Proxy

Look for:

> "I want the client to interact with an object, but something should stand between the client and the real resource."

Then ask why.

If the reason is:

```text
Authorization
Lazy Loading
Remote Access
Caching
Access Control
```

Proxy may be appropriate.

---

# Mental Model

Think about a security guard.

You want to enter:

```text
Secure Building
```

but you do not directly access it.

Instead:

```text
You
 ↓
Security Guard
 ↓
Check Permission
 ↓
Building
```

The security guard represents the access point to the protected resource.

That is a Protection Proxy.

---

# Quick Revision

```text
Proxy
→ Structural Design Pattern
```

```text
Core Idea
→ Stand-in for another object
```

```text
Structure

Client
 ↓
Proxy
 ↓
Real Object
```

```text
Protection Proxy
→ Authorization / access control
```

```text
Virtual Proxy
→ Lazy initialization
```

```text
Remote Proxy
→ Represent remote resource
```

```text
Caching Proxy
→ Cache expensive results
```

```text
Car Example
→ Proxy checks driver age
```

```text
Bitmap Example
→ Proxy loads image only on first draw
```

```text
Decorator
→ Add behavior
```

```text
Proxy
→ Control access
```

```text
Adapter
→ Make interfaces compatible
```

```text
Facade
→ Simplify subsystem
```

---

# Key Takeaways

- **Proxy is a structural design pattern.**
- **A Proxy stands in for another real object/resource.**
- **The client usually interacts with the Proxy through the same or a compatible interface as the real object.**
- **Protection Proxy controls who can access the real object.**
- **Your `CarProxy` checks the driver's age before delegating to `Car`.**
- **Virtual Proxy delays creation of an expensive resource.**
- **Your `LazyBitmap` creates the real `Bitmap` only on the first `draw()` call.**
- **Remote Proxy hides communication with a remote resource.**
- **Caching Proxy avoids repeated expensive calls.**
- **Proxy and Decorator can look structurally similar, but Proxy primarily controls access while Decorator primarily adds behavior.**
- **Proxy introduces indirection, so it should be used when that extra control provides real value.**

# One-Line Revision

> **Proxy = put a stand-in object between the client and the real resource so you can control when, how, or whether that resource is accessed.**