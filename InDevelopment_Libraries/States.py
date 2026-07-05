# -*- coding: utf-8 -*-
"""
Created on Sun Sep  7 18:46:08 2025

@author: Alexm
"""

class State:
    def __init__(self, *args, index = 0):
        if len(args) == 1:
            if isinstance(args[0], (tuple,list)):
                args = args[0]
        assert isinstance(args, (list, tuple))
        self.states = tuple(args)
    def __len__(self):
        return len(self.states)




color = State('red', 'blue', 'green')
print(color())#->'red'
color +=1
print(color())#->'blue'
color -=2
print(color())#->'green'



- Named transitions (color.to('green'))
- History tracking (color.history)
- Event hooks (on_enter, on_exit)
- Immutable variants (new_color = color + 1)


from transitions import Machine

class Matter:
    pass

lump = Matter()
machine = Machine(model=lump, states=['solid', 'liquid', 'gas'], initial='solid')
machine.add_transition('melt', 'solid', 'liquid')
machine.add_transition('evaporate', 'liquid', 'gas')


from statemachine import StateMachine, State

class DoorMachine(StateMachine):
    closed = State('Closed', initial=True)
    open = State('Open')

    open_door = closed.to(open)
    close_door = open.to(closed)
