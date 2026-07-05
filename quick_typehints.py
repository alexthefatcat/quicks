# -*- coding: utf-8 -*-
"""Created on Mon Sep 15 02:13:01 2025@author: Alexm"""


print('''
# Union    -> multiple differnt types allowed
# Sequence -> container like list dict tupple    
# Any      -> any type allowed     
# Optional -> main one type and None allowed     
          
      ''')



#%%   Get paramter names and type using __annotations__


def add(x: int, y: int) -> int:
    return x + y

print(add.__annotations__)

# {'x': <class 'int'>, 'y': <class 'int'>, 'return': <class 'int'>}


def validate(fn):
    def wrapper(*args):
        annotations = fn.__annotations__
        for arg, (name, expected) in zip(args, annotations.items()):
            if not isinstance(arg, expected):
                raise TypeError(f"{name} should be {expected}")
        return fn(*args)
    return wrapper

@validate
def greet(name: str):
    print(f"Hello {name}")
    
    
    
#%% Differnt basic Type Hints
    
from typing import Union, Callable, Sequence, Any, Optional
from numbers import Number
import pandas as pd
import numpy as np

def summarize(df: pd.DataFrame, s: pd.Series,  arr: np.ndarray, func: Callable, foo:Any, container:Sequence=[1,2,3], count:Union[int, str]='11', name:Optional[str]=None) -> None:
    return df.mean()

def multiply(value1: Union[int, float, complex], value2:Number) -> Number:
    return value1 * value2

def add_strings(string1:Optional[str], string2:Union[str, None]):
    return ''.join([e for e in (string1, string2) if e is not None])  
    
def get_user(id: int) -> Optional[str]:
    return "admin" if id == 1 else None

from typing import List
def square(elems: Sequence[float]) -> List[float]:
    return [x**2 for x in elems]
 
    
# Union    -> multiple differnt types allowed
# Sequence -> container like list dict tupple (anything with len() and .__getitem__())   
# Any      -> any type allowed     
# Optional -> main one type and None allowed     
  
    
#%% Containers with specific types inside
    
from typing import Dict, List, Tuple        
    
    
nam: str = 'Bob'
names: list = ["Guido", "Jukka", "Ivan"]


# Containers with certain types inside
names: List[str] = ["Guido", "Jukka", "Ivan"]
options: Dict[str, bool] = {"centered": False, "capitalize": True}
version: Tuple[int, int, int] = (3, 7, 1)


def create_deck(shuffle: bool = False) -> List[Tuple[str, str]]:
    import random
    """Create a new deck of 52 cards"""
    SUITS,RANKS='HDCS','23456789JQKA'
    deck = [(s, r) for r in RANKS for s in SUITS]
    if shuffle:
        random.shuffle(deck)
    return deck


#%% Classes



from datetime import date
from typing import Type, TypeVar

TAnimal = TypeVar("TAnimal", bound="Animal")

class Animal:
    def __init__(self, name: str, birthday: date) -> None:
        self.name = name
        self.birthday = birthday

    @classmethod
    def newborn(cls: Type[TAnimal], name: str) -> TAnimal:
        return cls(name, date.today())

    def twin(self: TAnimal, name: str) -> TAnimal:
        cls = self.__class__
        return cls(name, self.birthday)

class Dog(Animal):
    def bark(self) -> None:
        print(f"{self.name} says woof!")


#%% Future

from typing import Literal

def get_status(code: int) -> Literal["success", "error", "pending"]:
    return "success" if code == 200 else "error"

from typing import Callable

def apply_twice(fn: Callable[[int], int], value: int) -> int:
    return fn(fn(value))
#dataclasses?















