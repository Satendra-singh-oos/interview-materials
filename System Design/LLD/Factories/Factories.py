# Factories
# Object creation logic is encapsulated in a factory class. This allows for the creation of objects without exposing the instantiation logic to the client and refers to the newly created object using a common interface.
# Initializer is not descriptive 
# Name is always __init , cannot overload with same sets of arguments with different names can turn into 'optional parameter hell'
# Wholesale object creation (non-piecewise,unlike builder)can be  outsourced to a factory class, which can be used to create objects of different types based on input parameters. This is useful when the creation process is complex or requires additional logic.
# Type-> Separate method(Factory Method),that may exist in a separate class (Factory), can create hierarchy of factories with abstract factory



# Factory Method: A factory method is a method that returns an instance of a class. It can be used to create objects of different types based on input parameters. This is useful when the creation process is complex or requires additional logic.
from enum import Enum, auto
import math

class CoordinateSystem(Enum):
    CARTESIAN = 1
    POLAR = 2


class Point:
    # def __init__(self, a,b,system=CoordinateSystem.CARTESIAN):
    #     if system == CoordinateSystem.CARTESIAN:
    #         self.x = a
    #         self.y = b
    #     elif system == CoordinateSystem.POLAR:
    #         self.x = a * math.cos(b)
    #         self.y = a * math.sin(b)
    #     else:
    #         raise ValueError("Invalid coordinate system")
    
    # we make factories method
    def __init__(self, x=0, y=0):   
        self.x = x
        self.y = y
        
    def __str__(self):
        return f"Point({self.x}, {self.y})"
        
    @staticmethod 
    def new_cartesian_point(x, y):
        return Point(x, y)
    
    @staticmethod
    def new_polar_point(rho, theta):
        return Point(rho * math.cos(theta), rho * math.sin(theta))
    
    

if __name__ == "__main__": 
    p = Point(3, 4)
    p1 = Point.new_cartesian_point(3, 4)
    p2 = Point.new_polar_point(5, math.pi / 4)
    print(p)
    print(p1)   
    print(p2)
    

# Factory: A factory is a class that contains one or more factory methods. It can be used to create objects of different types based on input parameters. This is useful when the creation process is complex or requires additional logic.
# Single Responsibility Principle: A class should have only one reason to change. This means that a class should have only one responsibility or job. If a class has more than one responsibility, it becomes more difficult to maintain and test.
# A factory is separate entity .
class NewPoint:
    class PointFactory:
        def new_cartesian_point(self,x, y):
            p= NewPoint()
            p.x=x
            p.y=y
            return p
        
        def new_polar_point(self,rho, theta):
            p= NewPoint()
            p.x=rho * math.cos(theta)
            p.y=rho * math.sin(theta)
            return p
    factory = PointFactory()
    

if __name__ == "__main__": 
    p = NewPoint(3, 4)
    p1 = NewPoint.factory.new_cartesian_point(3, 4)
    p2 = NewPoint.factory.new_polar_point(5, math.pi / 4)
    print(p)
    print(p1)   
    print(p2)



# Factory Abstract: An abstract factory is a factory that creates objects of different types based on input parameters. It can be used to create objects of different types based on input parameters. This is useful when the creation process is complex or requires additional logic.

from abc import ABC, abstractmethod

class HotDrink(ABC):
    @abstractmethod
    def consume(self):
        pass

class Tea(HotDrink):
    def consume(self):
        print("This tea is nice but I'd prefer it with milk.") 

class Coffee(HotDrink):    
    def consume(self):
        print("This coffee is delicious.")
        
class HotDrinkFactory(ABC):
    @abstractmethod
    def prepare(self, amount):
        pass  

class TeaFactory(HotDrinkFactory): 
    def prepare(self, amount):
        print(f"Put in a tea bag, boil water, pour {amount}ml, add lemon, enjoy!")
        return Tea()

class CoffeeFactory(HotDrinkFactory):        
    def prepare(self, amount):
        print(f"Grind some beans, boil water, pour {amount}ml, add cream and sugar, enjoy!")
        return Coffee()


def make_drink(drink_type):
    if drink_type == "tea":
        return TeaFactory().prepare(200)
    elif drink_type == "coffee":
        return CoffeeFactory().prepare(50)
    else:
        return None
    


class HotDrinkMachine:
    class AvailableDrink(Enum):  # violates OCP
        COFFEE = auto()
        TEA = auto()

    factories = []
    initialized = False

    def __init__(self):
        if not self.initialized:
            self.initialized = True
            for d in self.AvailableDrink:
                name = d.name[0] + d.name[1:].lower()
                factory_name = name + 'Factory'
                factory_instance = eval(factory_name)()
                self.factories.append((name, factory_instance))





    def make_drink(self):
        print('Available drinks:')
        for f in self.factories:
            print(f[0])

        s = input(f'Please pick drink (0-{len(self.factories)-1}): ')
        idx = int(s)
        s = input(f'Specify amount: ')
        amount = int(s)
        return self.factories[idx][1].prepare(amount)



def make_drink(type):
    if type == 'tea':
        return TeaFactory().prepare(200)
    elif type == 'coffee':
        return CoffeeFactory().prepare(50)
    else:
        return None


if __name__ == '__main__':
    # entry = input('What kind of drink would you like?')
    # drink = make_drink(entry)
    # drink.consume()

    hdm = HotDrinkMachine()
    drink = hdm.make_drink()
    drink.consume()

