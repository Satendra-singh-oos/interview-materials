# Satate Design Pattern - conider an ordinary telphone , what you do with it depends on the state it is in. if it reigns or you wanat to make a call you can pick it up,phone must be off the hook to talk/make a call.
# You can only put it on the hook if it is already off the hook.
# You can only take it off the hook if it is already on the hook.
# You can only make a call if the phone is off the hook.

# A pattern in which the object behavior is determined by its state.An object transitions from one state to another (something needs to trigger a transition).
# A formalized construct which manages state and transitions is called a state machine.

# Example: A telephone
# - You pick up the phone, and you can talk/make a call
# - You put the phone on the hook, and you can't talk/make a call
# - You take the phone off the hook, and you can talk/make a call
# - You put the phone on the hook, and you can't talk/make a call


# Classic implementation

# interesting but not practical :)
from abc import ABC


class Switch:
    def __init__(self):
        self.state = OffState()

    def on(self):
        self.state.on(self)

    def off(self):
        self.state.off(self)


class State(ABC):
    def on(self, switch):
        print('Light is already on')

    def off(self, switch):
        print('Light is already off')


class OnState(State):
    def __init__(self):
        print('Light turned on')

    def off(self, switch):
        print('Turning light off...')
        switch.state = OffState()


class OffState(State):
    def __init__(self):
        print('Light turned off')

    def on(self, switch):
        print('Turning light on...')
        switch.state = OnState()


if __name__ == '__main__':
    sw = Switch()

    sw.on()  # Turning light on...
             # Light turned on

    sw.off()  # Turning light off...
              # Light turned off

    sw.off()  # Light is already off





# Hand State Machine
from enum import Enum, auto


class State(Enum):
    OFF_HOOK = auto()
    CONNECTING = auto()
    CONNECTED = auto()
    ON_HOLD = auto()
    ON_HOOK = auto()


class Trigger(Enum):
    CALL_DIALED = auto()
    HUNG_UP = auto()
    CALL_CONNECTED = auto()
    PLACED_ON_HOLD = auto()
    TAKEN_OFF_HOLD = auto()
    LEFT_MESSAGE = auto()


if __name__ == '__main__':
    rules = {
        State.OFF_HOOK: [
            (Trigger.CALL_DIALED, State.CONNECTING)
        ],
        State.CONNECTING: [
            (Trigger.HUNG_UP, State.ON_HOOK),
            (Trigger.CALL_CONNECTED, State.CONNECTED)
        ],
        State.CONNECTED: [
            (Trigger.LEFT_MESSAGE, State.ON_HOOK),
            (Trigger.HUNG_UP, State.ON_HOOK),
            (Trigger.PLACED_ON_HOLD, State.ON_HOLD)
        ],
        State.ON_HOLD: [
            (Trigger.TAKEN_OFF_HOLD, State.CONNECTED),
            (Trigger.HUNG_UP, State.ON_HOOK)
        ]
    }

    state = State.OFF_HOOK
    exit_state = State.ON_HOOK

    while state != exit_state:
        print(f'The phone is currently {state}')

        for i in range(len(rules[state])):
            t = rules[state][i][0]
            print(f'{i}: {t}')

        idx = int(input('Select a trigger:'))
        s = rules[state][idx][1]
        state = s

    print('We are done using the phone.')



# Switch Base State Machine
from enum import Enum, auto


class State(Enum):
    LOCKED = auto()
    FAILED = auto()
    UNLOCKED = auto()


if __name__ == '__main__':
    code = '1234'
    state = State.LOCKED
    entry = ''

    while True:
        if state == State.LOCKED:
            entry += input(entry)

            if entry == code:
                state = State.UNLOCKED

            if not code.startswith(entry):
                # the code is wrong
                state = State.FAILED
        elif state == State.FAILED:
            print('\nFAILED')
            entry = ''
            state = State.LOCKED
        elif state == State.UNLOCKED:
            print('\nUNLOCKED')
            break
