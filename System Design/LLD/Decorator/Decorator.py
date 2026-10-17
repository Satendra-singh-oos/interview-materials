# Decorator Desing Pattern
# want to argment an object with additional functionality
# do not wan to rewrite or alter exisiting code (break the open close principle)
# open close principle state that once you writen the code you should not jumping and performing modification
# so you want to keep new cunctionality seprate (SRP)
# 2 options inhere the requrie object OR use composition (Decorator-> Faciliates the addition of behavior to individual object without inherting from them.)

# Python funciton decorator
import time


def time_it(func):
    def wrapper():
        start = time.time()
        result = func()
        end = time.time()
        print(f'{func.__name__} execution time = {int((end - start)*1000)}ms')
        return result
    return wrapper 

@time_it
def some_operation():
    print("Starting operation")
    time.sleep(1)
    print("we are done")
    return 123

if __name__ == '__main__':
    #some_operation()
    # time_it(some_operation)()
    some_operation()


print("-----------")

# Classic Decorator

from abc import ABC

class Shape(ABC):
    def __str__(self):
        return ''

class Circle(Shape):
    def __init__(self,radius):
        self.radius=radius
    def resize(self,factor):
        self.radius*=factor
    def __str__(self):
        return f'A circle of radius {self.radius}'


class Square(Shape):
    def __init__(self,side):
        self.side=side

    def __str__(self):
        return f'A square of side {self.side}'

class ColouredShape(Shape):
    def __init__(self,shape,color):

        if isinstance(shape,ColouredShape):
            raise Exception('You cannot colour a colored shape')
        self.shape=shape
        self.color=color

    def __str__(self):
        return f'{self.shape} has color {self.color}'


class TransperentShape(Shape):
    def __init__(self,shape,transperency):
        self.shape=shape
        self.transperency=transperency

    def __str__(self):
        return f'{self.shape} has transperency {self.transperency}'
    



if __name__ == '__main__':
    circle = Circle(2)
    print(circle)   

    red_circle = ColouredShape(circle,'red')
    print(red_circle)   


    red_half_transperent_circle = TransperentShape(red_circle,'50%')
    print(red_half_transperent_circle)   

    # mixed =ColouredShape(ColouredShape(Square(3),'red'),'green')
    # print(mixed)



# Dynamic Decorator - In python you can apply decorator dynamically 
class FileWithLogging:
  def __init__(self, file):
    self.file = file

  def writelines(self, strings):
    self.file.writelines(strings)
    print(f'wrote {len(strings)} lines')

  def __iter__(self):
    return self.file.__iter__()

  def __next__(self):
    return self.file.__next__()

  def __getattr__(self, item):
    return getattr(self.__dict__['file'], item)

  def __setattr__(self, key, value):
    if key == 'file':
      self.__dict__[key] = value
    else:
      setattr(self.__dict__['file'], key)

  def __delattr__(self, item):
    delattr(self.__dict__['file'], item)


if __name__ == '__main__':
  file = FileWithLogging(open('hello.txt', 'w'))
  file.writelines(['hello', 'world'])
  file.write('testing')
  file.close()
