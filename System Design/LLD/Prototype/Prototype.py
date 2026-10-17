# Prototype design pattern
# The Prototype design pattern is a creational design pattern that allows you to create new objects by copying an existing object,deep copy, known as the prototype. This pattern is particularly useful when the process of creating a new object is resource-intensive or complex.




import copy


class Address:
    def __init__(self, street_address, city, country,suite=None):
        self.street_address = street_address
        self.city = city
        self.country = country
        self.suite = suite

    def __str__(self):
        return f"Address(street_address={self.street_address}, city={self.city}, country={self.country}), suite={self.suite}"



class Person:
    def __init__(self, name, address):
        self.name = name
        self.address = address
    
    def __str__(self):
        return f"Person(name={self.name}, address={self.address})"
    

# address = Address("123 London Road", "London", "UK")
# john= Person("John", address)

# print(john) 

# print('----------') 

# jane = john
# jane.name = "Jane" 
# print(john)  # Output: Person(name=Jane, address=Address(street_address=123 London Road, city=London, country=UK))
# print(jane)  # Output: Person(name=Jane, address=Address(street_address=123 London Road, city=London, country=UK))

# print('----------') 

john = Person("John", Address("123 London Road", "London", "UK"))
print(john)  # Output: Person(name=John, address=Address(street_address

print('----------')

jane = copy.deepcopy(john)
# jane = copy.copy(john) #not a proper copy, it will copy the reference of the address object, so if we change the address of jane, it will also change the address of john

jane.name = "Jane"
print(john)  # Output: Person(name=John, address=Address(street_address=123 London Road, city=London, country=UK))
print(jane)  # Output: Person(name=Jane, address=Address(street_address=456 Paris Street, city=Paris, country=France))


print('----------')

jane.address.street_address = "456 Paris Street"
print(jane)  # Output: Person(name=John, address=Address(street_address=123 London Road, city=London, country=UK))

print('----------')
print('----------')

# Prototype Factory: A prototype factory is a class that contains one or more prototype objects. It can be used to create new objects by copying the prototype objects. This is useful when the creation process is complex or requires additional logic.


class Employee:
    def __init__(self, name, address):
        self.name = name
        self.address = address
    
    def __str__(self):
        return f"Employee(name={self.name}, address={self.address})"
    

class EmployeeFactory:
    main_office = Employee("", Address("123 London Road", "London", "UK", 0))
    aux_office = Employee("", Address("456 Paris Street", "Paris", "France"))
    
    @staticmethod
    def __new_employee(proto, name, suite):
        employee = copy.deepcopy(proto)
        employee.name = name
        employee.address.suite = suite
        return employee

    @staticmethod
    def new_main_office_employee(name, suite):
        return EmployeeFactory.__new_employee(EmployeeFactory.main_office, name, suite)

    @staticmethod
    def new_aux_office_employee(name, suite):
        return EmployeeFactory.__new_employee(EmployeeFactory.aux_office, name, suite)


doe = EmployeeFactory.new_main_office_employee("John Doe", 101)
print(doe)  # Output: Employee(name=John Doe, address=Address(street
jelly = EmployeeFactory.new_aux_office_employee("Jelly Smith", 202)
print(jelly)  # Output: Employee(name=Jelly Smith, address=Address(street_address=456 Paris Street, city=Paris, country=France), suite=202)