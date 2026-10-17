# Singleton Design Pattern: The singleton pattern is a design pattern that restricts the instantiation of a class to one single instance. This is useful when exactly one object is needed to coordinate actions across the system. The singleton pattern can be implemented in various ways, such as using a class variable to store the instance, using a metaclass, or using decorators.
# we have to prevent anyone creating additional copies of the singleton class, so we have to override the __new__ method and check if an instance already exists, if it does, we return that instance, otherwise we create a new instance and return it. We also have to override the __init__ method to prevent anyone from creating additional copies of the singleton class. We can do this by checking if an instance already exists, if it does, we raise an exception, otherwise we initialize the instance.




# Singleton Allocator: A singleton allocator is a class that is responsible for creating and managing the single instance of a singleton class. It can be used to create the singleton instance and provide access to it. This is useful when the creation process is complex or requires additional logic. 

import random


class Database:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Database, cls).__new__(cls,*args,**kwargs)
        return cls.__instance

    def __init__(self):
        id=random.randint(1,100)
        print(f"Database instance created with id: {id}")
        
        
if __name__ == '__main__':
    d1=Database()
    d2=Database()
    print(d1 == d2) # True


print("------") 
    
# Singleton Decorator: A singleton decorator is a function that takes a class as an argument and returns a new class that is a singleton. It can be used to create the singleton instance and provide access to it. This is useful when the creation process is complex or requires additional logic.

def singleton(cls):
    instances={}
    
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls]=cls(*args, **kwargs)
        return instances[cls]
    return get_instance


@singleton
class Database2:
    def __init__(self):
        id=random.randint(1,100)
        print(f"Database2 instance created with id: {id}")
if __name__ == '__main__':
    d1=Database2()
    d2=Database2()
    print(d1 == d2) # True

print("------")


# Singleton Metaclass: A singleton metaclass is a class that is responsible for creating and managing the single instance of a singleton class. It can be used to create the singleton instance and provide access to it. This is useful when the creation process is complex or requires additional logic.

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super(SingletonMeta, cls).__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Database3(metaclass=SingletonMeta):
    def __init__(self):
        id=random.randint(1,100)
        print(f"Database3 instance created with id: {id}")
        

if __name__ == '__main__':
    d1=Database3()
    d2=Database3()
    print(d1 == d2) # True


print("------")


# Monostate Singleton: A monostate singleton is a class that is responsible for creating and managing the single instance of a singleton class. It can be used to create the singleton instance and provide access to it. This is useful when the creation process is complex or requires additional logic. 
# Not a good approch

class CEO:
    _shared_state={
        "name":"Steve",
        'age':55
    }

    def __init__(self):
        self.__dict__=self._shared_state

    def __str__(self):
        return f'{self.name} is {self.age} years old.'


class Monostate:
    __shared_state={}

    def __new__(cls,*args,**kwargs):
        obj=super(Monostate,cls).__new__(cls,*args,**kwargs)
        obj.__dict__=cls.__shared_state
        return obj



class CFO(Monostate):
    def __init__(self):
        self.name=''
        self.money_managed=0

    def __str__(self):
        return f'{self.name} manages ${self.money_managed} billion' 


if __name__=='__main__':
    c1=CEO()
    c2=CEO()
    print(c1 == c2) # True
    print(c1)
    print(c2)

    cfo1=CFO()
    cfo1.name="Bill"
    cfo1.money_managed=35
    print(cfo1)

    cfo2=CFO()
    cfo2.name="Ruth"
    cfo2.money_managed=35
    print(cfo2)
