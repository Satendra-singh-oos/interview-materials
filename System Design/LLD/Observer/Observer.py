# Observer Design Pattern - we need to be informed when certain events happen in our system. The observer pattern allows us to do this by defining a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically.


#Events

class Events(list):
    def __call__(self, *args, **kwargs):
        for func in self:
            func(*args, **kwargs)



class Person:
    def __init__(self, name,address):
        self.name = name
        self.address = address
        self.falls_ill=Events()
        
    def catch_a_cold(self):
        self.falls_ill(self.name,self.address)
    

def call_doc(name,address):
    print(f'{name} needs a doctor at {address}')
    

if __name__ == '__main__':
    person=Person("John","abc address")
    person.falls_ill.append(lambda name,address: print(f'{name} needs a doctor at {address}'))
    person.falls_ill.append(call_doc)
    person.catch_a_cold()

    person.falls_ill.remove(call_doc)
    person.catch_a_cold()

# Property Observer

class PropertyObservable:
    def __init__(self):
        self.property_changed=Events()

    def __get__(self,instance,owner):
        return instance.__dict__[self.name]
    
    def __set__(self,instance,value):
        instance.__dict__[self.name]=value
        self.property_changed(instance)

class Person(PropertyObservable):
    def __init__(self,age=0):
        super().__init__()
        self._age=age

    @property
    def age(self):
        return self._age
    
    @age.setter
    def age(self,value):
        self._age=value
        self.property_changed('age',value)

class TrafficAuthority:
    def __init__(self,person):
        self.person=person
        self.person.property_changed.append(self.person_age_changed)

    def person_age_changed(self,name,value):
        if name == 'age':
            if value < 18:
                print('Sorry, you are not allowed to drive')
            else:
                print('You are allowed to drive')
                self.person.property_changed.remove(self.person_age_changed)

if __name__ == '__main__':
    person=Person(10)
    traffic_authority=TrafficAuthority(person)
    for age in range(14,20):
        print(f'Setting age to {age}')
        person.age=age


# property dependencies

class Event(list):
  def __call__(self, *args, **kwargs):
    for item in self:
      item(*args, **kwargs)


class PropertyObservable:
  def __init__(self):
    self.property_changed = Event()


class Person(PropertyObservable):
  def __init__(self, age=0):
    super().__init__()
    self._age = age

  @property
  def can_vote(self):
    return self._age >= 18

  @property
  def age(self):
    return self._age

  # @age.setter
  # def age(self, value):
  #   if self._age == value:
  #     return
  #   self._age = value
  #   self.property_changed('age', value)

  @age.setter
  def age(self, value):
    if self._age == value:
      return

    old_can_vote = self.can_vote

    self._age = value
    self.property_changed('age', value)

    if old_can_vote != self.can_vote:
      self.property_changed('can_vote', self.can_vote)


if __name__ == '__main__':
  def person_changed(name, value):
    if name == 'can_vote':
      print(f'Voting status changed to {value}')

  p = Person()
  p.property_changed.append(
    person_changed
  )

  for age in range(16, 21):
    print(f'Changing age to {age}')
    p.age = age