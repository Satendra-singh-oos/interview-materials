# Proxy Desing Pattern
# a class that function as an interface to aparticular resource.that resource may be remote expensive to construct or may require logging or some other added functionality

# Protection Proxy
# provides an interface to the client , control acces to the resource
# access control
# authentication / authorization
# logging
# caching
# remote resource

class Car:
    def __init__(self,driver):
        self.driver=driver

    def drive(self):
        print(f'Car is being driven by {self.driver.name}')


class CarProxy:
    def __init__(self,driver):
        self.driver=driver
        self.car=Car(driver)
    
    def drive(self):
        if self.driver.age>=18:
            self.car.drive()
        else:
            print(f'Car is not driven by {self.driver.name}')

class Driver:
    def __init__(self,name,age):
        self.name=name
        self.age=age

if __name__=='__main__':
    driver=Driver("Jhone",20)
    car=Car(driver)
    car.drive()
    driver2=Driver("Bob",16)
    car2=CarProxy(driver2)
    car2.drive()


#Virtual Proxy - lazily load the resource
# on first access   
class Bitmap:
    def __init__(self, filename):
        self.filename = filename
        print(f'Loading image from {filename}')

    def draw(self):
        print(f'Drawing image {self.filename}')


class LazyBitmap:
    def __init__(self, filename):
        self.filename = filename
        self.bitmap = None

    def draw(self):
        if not self.bitmap:
            self.bitmap = Bitmap(self.filename)
        self.bitmap.draw()

def draw_image(image):
    print('About to draw image')
    image.draw()
    print('Done drawing image')

if __name__ == '__main__':
    bmp = LazyBitmap('facepalm.jpg')  # Bitmap
    draw_image(bmp)
