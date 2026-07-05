# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 02:30:39 2024

@author: Alexm



def func(value=options('blue','red', 'green'), number=options(1,(2),3), size = options(1.0 to 2.0), info = (str)):
    pass


number = options(1, (2), 3)

number = options(1, 2, 3)[1]

color1 = options('blue', 'red', ['green'])
color2 = color(0)
color3 = options(['blue'], 'red', 'green')
assert color2 == color3
assert 'blue' in color1

number = options(1, 2, [3])
number -=1
assert number == 2
print(number())

list(number)
number[0]


color1.index
color1.index = 0


cols = ['yellow', 'orange', 'red']
Options(cols, index=0)

Options(between=(1.0, 2.0))
"""





class Options(list):
    def __init__(self, *args, loc = None, cycle=True,**kwargs):
        super().__init__(*args, **kwargs)
        if loc is None:
            self.loc = 0
        else:
            self.loc = loc
        
    def __call__(self, arg=None):
        if arg is None:
            return self.value
        if arg in self:
            self.loc = self.index(arg)
            return
        print('Error')
    
    def __iadd__(self, arg):
        self.loc = (self.loc +arg) % len(self)
        return self

    def __isub__(self, arg):
        self.loc = (self.loc -arg) % len(self)
        return self
    
    @property
    def value(self):
        return self[self.loc]

    @value.setter
    def value(self, new_value):
        self(new_value)


    
e = ('blue', 'red', 'green')
#e = [1,(2),3]
option = Options(e)     

print(option())

print(option())
for n in range(10):
    
    if n>0:
        option -=1
    print(n, option()) 



option('red')

option.value = 'blue'

option()



'''
__add__(self, other): Addition (+).

__sub__(self, other): Subtraction (-).







Object Initialization and Representation:

__init__(self, ...): Object constructor.

__del__(self): Object destructor.

__repr__(self): Official string representation of an object.

__str__(self): Informal string representation of an object.

Attribute Access:

__getattr__(self, name): Called when an attribute is not found.

__setattr__(self, name, value): Called when an attribute assignment is attempted.

__delattr__(self, name): Called when an attribute deletion is attempted.

__getattribute__(self, name): Called on all attribute access attempts.

Container Emulation:

__len__(self): Called to implement the built-in len() function.

__getitem__(self, key): Called to access items.

__setitem__(self, key, value): Called to set items.

__delitem__(self, key): Called to delete items.

__iter__(self): Returns an iterator.

__next__(self): Returns the next item from an iterator.

Mathematical Operations:

__add__(self, other): Addition (+).

__sub__(self, other): Subtraction (-).

__mul__(self, other): Multiplication (*).

__truediv__(self, other): True division (/).

__floordiv__(self, other): Floor division (//).

__mod__(self, other): Modulus (%).

__pow__(self, other[, modulo]): Exponentiation (**).

Comparison Operations:

__lt__(self, other): Less than (<).

__le__(self, other): Less than or equal to (<=).

__eq__(self, other): Equal to (==).

__ne__(self, other): Not equal to (!=).

__gt__(self, other): Greater than (>).

__ge__(self, other): Greater than or equal to (>=).

Object Lifecycle:

__call__(self, *args, **kwargs): Called when the object is called as a function.

__copy__(self): Called by the copy module for shallow copies.

__deepcopy__(self, memo): Called by the copy module for deep copies.

Context Management:

__enter__(self): Enter the runtime context related to this object.

__exit__(self, exc_type, exc_value, traceback): Exit the runtime context related to this object.

Other Common Methods:

__contains__(self, item): Called to implement membership test operators (in and not in).

__hash__(self): Called by built-in function hash() and for operations on members of hashed collections.

__bool__(self): Called to implement truth value testing and the built-in bool().

'''