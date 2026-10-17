# Vistor Desing pattern - a way of separating an algorithm from an object structure on which it operates.
# A component(visitor) that knows how to traverse a data structure composed of (possible related) types.


# Intrusive visitor
class DoubleExpression:
    def __init__(self, value):
        self.value = value

    def print(self, buffer):
        buffer.append(str(self.value))

    def eval(self): return self.value


class AdditionExpression:
    def __init__(self, left, right):
        self.right = right
        self.left = left

    def print(self, buffer):
        buffer.append('(')
        self.left.print(buffer)
        buffer.append('+')
        self.right.print(buffer)
        buffer.append(')')

    def eval(self):
        return self.left.eval() + self.right.eval()


if __name__ == '__main__':
    # represents 1+(2+3)
    e = AdditionExpression(
        DoubleExpression(1),
        AdditionExpression(
            DoubleExpression(2),
            DoubleExpression(3)
        )
    )
    buffer = []
    e.print(buffer)
    print(''.join(buffer), '=', e.eval())

    # breaks OCP: requires we modify the entire hierarchy
    # what is more likely: new type or new operation?


# Refelective Vistor

from abc import ABC


class Expression(ABC):
    pass


class DoubleExpression(Expression):
    def __init__(self, value):
        self.value = value


class AdditionExpression(Expression):
    def __init__(self, left, right):
        self.right = right
        self.left = left


class ExpressionPrinter:
    @staticmethod
    def print(e, buffer):
        """ Will fail silently on a missing case. """
        if isinstance(e, DoubleExpression):
            buffer.append(str(e.value))
        elif isinstance(e, AdditionExpression):
            buffer.append('(')
            ExpressionPrinter.print(e.left, buffer)
            buffer.append('+')
            ExpressionPrinter.print(e.right, buffer)
            buffer.append(')')

    Expression.print = lambda self, b: ExpressionPrinter.print(self, b)


# still breaks OCP because new types require M×N modifications

if __name__ == '__main__':
    # represents 1+(2+3)
    e = AdditionExpression(
        DoubleExpression(1),
        AdditionExpression(
            DoubleExpression(2),
            DoubleExpression(3)
        )
    )
    buffer = []

    # ExpressionPrinter.print(e, buffer)

    # IDE might complain here
    e.print(buffer)

    print(''.join(buffer))


# Classic Visitor
# taken from https://tavianator.com/the-visitor-pattern-in-python/


def _qualname(obj):
    """Get the fully-qualified name of an object (including module)."""
    return obj.__module__ + '.' + obj.__qualname__


def _declaring_class(obj):
    """Get the name of the class that declared an object."""
    name = _qualname(obj)
    return name[:name.rfind('.')]


# Stores the actual visitor methods
_methods = {}


# Delegating visitor implementation
def _visitor_impl(self, arg):
    """Actual visitor method implementation."""
    method = _methods[(_qualname(type(self)), type(arg))]
    return method(self, arg)


# The actual @visitor decorator
def visitor(arg_type):
    """Decorator that creates a visitor method."""

    def decorator(fn):
        declaring_class = _declaring_class(fn)
        _methods[(declaring_class, arg_type)] = fn

        # Replace all decorated methods with _visitor_impl
        return _visitor_impl

    return decorator


# ↑↑↑ LIBRARY CODE ↑↑↑

class DoubleExpression:
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        visitor.visit(self)


class AdditionExpression:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def accept(self, visitor):
        visitor.visit(self)


class ExpressionPrinter:
    def __init__(self):
        self.buffer = []

    @visitor(DoubleExpression)
    def visit(self, de):
        self.buffer.append(str(de.value))

    @visitor(AdditionExpression)
    def visit(self, ae):
        self.buffer.append('(')
        ae.left.accept(self)
        self.buffer.append('+')
        ae.right.accept(self)
        self.buffer.append(')')

    def __str__(self):
        return ''.join(self.buffer)


if __name__ == '__main__':
    # represents 1+(2+3)
    e = AdditionExpression(
        DoubleExpression(1),
        AdditionExpression(
            DoubleExpression(2),
            DoubleExpression(3)
        )
    )
    buffer = []
    printer = ExpressionPrinter()
    printer.visit(e)
    print(printer)

