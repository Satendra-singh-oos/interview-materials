# Memento design pattern is a behavioral design pattern that allows an object to capture its internal state and restore it later without exposing its implementation details. It is useful for implementing undo/redo functionality, version control, and state management in applications. eg back account get deposit and withdraw and undo the last operation. there are diffrent types of memento pattern like classic memento pattern, black box memento pattern and white box memento pattern.save the snapshot at every point of time and restore it when needed.
# A token/handle representing the system state. let us rollback to the state when the token was generated. May or may not directly expose the state information.
class Memento:
    def __init__(self, balance):
        self.balance = balance


class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance
        self.changes=[Memento(self.balance)]
        self.current=0

    def deposit(self, amount):
        self.balance += amount
        memento = Memento(self.balance)
        self.changes.append(memento)
        self.current += 1
        return memento

    def restore(self, memento):
        if memento:
            self.balance = memento.balance
            self.changes.append(memento)
            self.current =len(self.changes)-1
    
    
    def undo(self):
        if self.current > 0:
            self.current -= 1
            memento = self.changes[self.current]
            self.balance = memento.balance
            return memento
        return None
    
    def redo(self):
        if self.current + 1 < len(self.changes):
            self.current += 1
            memento = self.changes[self.current]
            self.balance = memento.balance
            return memento
        return None

    def __str__(self):
        return f'Balance = {self.balance}'


if __name__ == '__main__':
    ba = BankAccount(100)
    ba.deposit(50)
    ba.deposit(25)
    print(ba)

    ba.undo()
    print(f'After undo 1: {ba}')
    ba.undo()
    print(f'After undo 2: {ba}')
    ba.redo()
    print(f'After redo 1: {ba}')
    