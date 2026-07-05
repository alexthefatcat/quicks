# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 10:55:50 2025

@author: Alexm
"""
from quick_decorators import CapturePrint








class AddPostInitializeMeta(type):
    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)
        original_init = cls.__init__

        def new_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)

            # Ensure post_init() runs only once, after the last class is initialized
            if self.__class__ == cls:
                self.post_init()

        cls.__init__ = new_init  # Override init dynamically





if __name__ == '__main__':
    class bang:
        def __init__(self):
            self.a = 1
        def b(self):
            self.c=4
    
    class Base(bang, metaclass=AddPostInitializeMeta):
        def __init__(self):
            super().__init__()
            print("Base class initialized")
    
        def post_init(self):
            print(f"Post-init method in {self.__class__.__name__}")
    
    class Intermediate(Base):
        def __init__(self):
            super().__init__()
            print("Intermediate class initialized")
    
    class Child(Intermediate):
        def __init__(self):
            super().__init__()
            print("Child class initialized")
    
    with CapturePrint(False) as captureprint:
        # Example usage
        base_instance = Base()  
        print("-----")
        inte_instance = Intermediate()  
        print("-----")
        child_instance = Child()
        child_instance.a
    
    expected = '''Base class initialized
Post-init method in Base
-----
Base class initialized
Intermediate class initialized
Post-init method in Intermediate
-----
Base class initialized
Intermediate class initialized
Child class initialized
Post-init method in Child
'''  
    

    assert str(captureprint) == expected, 'Error AddPostInitializeMeta does not act as expected'





















