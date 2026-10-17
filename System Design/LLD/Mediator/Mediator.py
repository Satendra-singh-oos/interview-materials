# Mediator design pattern - components may go in and out of the system without affecting each other. The mediator handles the communication between components.like chat room ,player in multiplayer game,air traffic control system etc.
# A component that facilitates communication between other components without them needing to refer to each other directly. It promotes loose coupling and simplifies the communication logic.


# chat room 
class Person:
    def __init__(self, name):
        self.name = name
        self.chatroom = None
        self.chat_log = []
    def receive(self, from_person, message):
        session_msg=f'{from_person}: {message}'
        print(f'[{self.name}\'s chat session] {session_msg}')
        self.chat_log.append(session_msg)
        
    def send(self, message):
        self.chatroom.broadcast(self.name, message)
    
    def private_message(self, to_person, message):
        self.chatroom.direct_message(self.name, to_person, message)
        

class ChatRoom:
    def __init__(self):
        self.people = []

    def join(self, person):
        join_msg=f'{person.name} joins the chat'
        self.broadcast('room', join_msg)
        person.chatroom = self
        self.people.append(person)
        
    def broadcast(self, from_person, message):
        for person in self.people:
            if person.name != from_person:
                person.receive(from_person, message)
    
    def direct_message(self, from_person, to_person, message):
        for person in self.people:
            if person.name == to_person:
                person.receive(from_person, message)
                break
        
if __name__ == '__main__':
    chatroom = ChatRoom()
    
    person1 = Person('Alice')
    person2 = Person('Bob')
    
    chatroom.join(person1)
    chatroom.join(person2)
    
    person1.send('Hello everyone!')
    person2.send('Hi Alice!')
    
    person3 = Person('Charlie')
    chatroom.join(person3)
    person3.send('Hey folks, what\'s up?')
    
    person1.private_message('Bob', 'Hello Bob!')
    person2.private_message('Alice', 'Hi Alice!')
    person3.private_message('Alice', 'Hey Alice, how are you?')
    

# Mediator with events

class Event(list):
    def __call__(self, *args, **kwargs):
        for item in self:
            item(*args, **kwargs)
#Mediator
class Game:
    def __init__(self):
        self.events = Event()
    
    def fire(self,args):
        self.events(args)
    

class GoalScoredInfo:
    def __init__(self, team_name, goals_scored):
        self.team_name = team_name
        self.goals_scored = goals_scored


class Player:
    def __init__(self, name, team_name, game):
        self.name = name
        self.team_name = team_name
        self.game = game
        self.goals_scored = 0  
    
    def score(self):
        self.goals_scored += 1
        info = GoalScoredInfo(self.team_name, 1)
        self.game.fire(info)
    

class Coach:
    def __init__(self,  game):
        game.events.append(self.on_goal_scored)
    
    def on_goal_scored(self, info):
        if isinstance(info, GoalScoredInfo) and info.goals_scored<3:
            print(f'Coach {self.name}: Team {info.team_name} scored a goal! Total goals: {info.goals_scored}')


if __name__ == '__main__':
    game = Game()
    
    coach1 = Coach(game)
    coach1.name = 'Coach A'
    
    coach2 = Coach(game)
    coach2.name = 'Coach B'
    
    player1 = Player('Player 1', 'Team A', game)
    player2 = Player('Player 2', 'Team B', game)
    
    player1.score()
    player2.score()
    player1.score()  