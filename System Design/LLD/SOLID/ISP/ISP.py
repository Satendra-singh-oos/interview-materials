# Interface Segregation Principle

# Don't put to many method in an interface


from abc import ABC, abstractmethod

class Machine:
    def print(self,document):
        raise NotImplementedError

    def fax(self,document):
        raise NotImplementedError

    
    def scan(self,document):
        raise NotImplementedError


# you can override those impletion from base call and can have meaning full implementation
class MultiFunctionPrinter(Machine):
    def print(self,document):
        pass

    def fax(self,document):
        pass
    
    def scan(self,document):
        pass
    

# old fashion printer can't do scan fax    
# so how we can solve that don't implement anything on those but it will create a issue if some once use the oldfashion printer they will see the fax and scan as interface member thay can assume they can use fax function but it should work but in not work other way you can raise error 
class OldFashionPrinter(Machine):
    def print(self,document):
        # ok
        pass

    def fax(self,document):
        pass # dont implement
    
    def scan(self,document):
        """Not Supported!!"""
        raise NotImplementedError("Printer cannot scan!")
    
    
    


class Printer(ABC):
    @abstractmethod
    def print(self,document):
        pass

class Scanner(ABC):
    @abstractmethod
    def scan(self,document):
        pass
    
class MyPrinter(Printer):
    def print(self, document):
        print(document)
        
class Photocopier(Printer,Scanner):
    def  print(self,document):
        pass
    
    def scan(self, document):
        pass
    

class MultiFunctionDevice(Printer,Scanner):
    @abstractmethod
    def  print(self,document):
        pass
    
    @abstractmethod
    def scan(self, document):
        pass
    

class MultiFunctionMachine(MultiFunctionDevice):
    
    def __init__(self,printer,scanner):
        
        self.scanner=scanner
        self.printer=printer
    def  print(self,document):
        self.printer.print(document)
    
    def scan(self, document):
        self.scanner.scan(document)
