# Dependency Inversion Principle

# High Level classes/modules should not depend on low level module/classes instead of that they should depend on abstraction what we mean by asbstraction calls with abstract methrod you should depend on interface rather then complete implemetaion you can swap one for other

from enum import Enum
from abc import ABC,abstractmethod

class Relationship(Enum):
    PARENT=0
    CHILD=1
    SIBLING=2

class Person:
    def __init__(self,name):
        self.name=name

class RelationshipBrowser(ABC):
    @abstractmethod
    def find_all_children_of(self,name):pass
    
    
# low level module
class Relationships(RelationshipBrowser):
    def __init__(self):
        self.relations=[]

    def add_parent_and_child(self,parent,child):
        self.relations.append((parent,Relationship.PARENT,child))
        self.relations.append((child,Relationship.CHILD,parent))
        
    def find_all_children_of(self,name):
        for r in self.relations:
            if r[0].name == name and   r[1] == Relationship.PARENT:
                yield r[2].name
        

# high level module 


class Research:
    # here the reactions are depend on the low level module they define how relation looks like right now its and array suppose in future you want some thing else
    # def __init__(self,relationships):
    #     relations = relationships.relations
    #     for r in relations:
    #         if r[0].name == 'John' and r[1] == Relationship.PARENT:
    #             print(f'John has child called {r[2].name}. ')
    
    def __init__(self,browser):
        for p in browser.find_all_children_of('John'):
            print(f'John has child called {p}. ')

parent = Person('John')    
child1 = Person('Chris')    
child2 = Person('Matt')    

relationships=Relationships()

relationships.add_parent_and_child(parent=parent,child=child1)
relationships.add_parent_and_child(parent=parent,child=child2)


Research(relationships)