# -*- coding: utf-8 -*-
"""Created on Sat Dec 21 01:56:39 2024@author: alex



"""
import sys
sys.setrecursionlimit(60)
from contextlib import contextmanager

@contextmanager
def capture_output(verbose=False):
    import io, sys
    old_stdout = sys.stdout
    captured_output = io.StringIO()
    sys.stdout = captured_output
    messages = []
    try:
        yield messages
    finally:
        messages.extend(captured_output.getvalue().splitlines())
        if verbose:
            for message in messages:
                old_stdout.write(message + '\n')
        sys.stdout = old_stdout

if False:
    #with print_red()

    
    # Example usage
    print('a')
    
    with capture_output() as messages:
        print(6)
        print(7)
    
    # Print the captured messages
    print(messages)


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtWidgets import QTextEdit, QVBoxLayout

class TextEditWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.text_edit = QTextEdit(self)
        self.text_edit.textChanged.connect(self.on_text_changed)
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        self.setLayout(layout)

    def on_text_changed(self):
        print('Text changed')




class WrapWidget(QWidget):
    def __init__(self, widget=QTextEdit):
        super().__init__()
        self.widget = widget

    def __getattr__(self, name): 
        return getattr(self.widget, name)
    
    
 







def wrapper_function():
    ''' nearly complete
    Animal wraps around Dog
    if method or attribute exists in Dog than it return it else it checks Animal
    same for setting
    in future same above but have _inner and _outer which overrides the above
    _inner i thing works and in this case as Dog methods and attribures no fallback
    _outer doesnt work should be only Animal methods and attributes this is useful for overlaps
    1) _outer
    2) maybe do the beloe
    Dog
    Animal
    Wrapper(dog,animal)?
    which i guess would be a function that has a class in it which doesnt have 
    the below functions labelled as #z
    
    
    
    '''
    class Dog:
        def __init__(self):#z
            self.woof = 'woof'
            self.value = 20
        
        def bark(self):#z
            self.woofwoof = 1
            return '>>WOOF<<'
        
        def a(self):#z
            return '#b'
    
    class Animal:
        def __init__(self):
            self._inner = Dog()
            self.value = 333
        
        def __getattribute__(self, name):
            dog = super().__getattribute__('_inner')
            if hasattr(dog, name):
                return getattr(dog, name)
            return super().__getattribute__(name)
    
        def __setattr__(self, name, value):
            print('setattr', name, value)
            if name == '_inner':
                super().__setattr__(name, value)
            # elif name == '_outer':
            #     setattr(self._inner, name, value)
            #     super().__setattr__(name, value)
                
            elif hasattr(self._inner, name):
                setattr(self._inner, name, value)
            else:
                super().__setattr__(name, value)
        
        def onion(self):#z
            return '>>ONION<<'
        
        def a(self):#z
            return '#a'
    
    animal = Animal()
    assert animal.bark() == '>>WOOF<<'
    assert animal.a() == '#b'
    assert animal.onion() == '>>ONION<<'
    assert animal._inner.a() == '#b'
    animal.value = 1
    assert animal._inner.value == 1
    assert animal.woofwoof == 1
    assert animal._inner.woofwoof == 1
    animal.woofwoof = 2
    assert animal.woofwoof == 2
    assert animal._inner.woofwoof == 2
     
    #now change it so all methods and attribures in the Animal class
    #can be acces using _outer
    assert animal._outer.value == 333
    


 
#------------------------------------------------------------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setCentralWidget(TextEditWidget())
        self.setWindowTitle('QTextEdit Example')

if False:
    if __name__ == '__main__':
        app = QApplication(sys.argv)
        main_window = MainWindow()
        main_window.show()
        sys.exit(app.exec_())
    
        
    
class A1:
    def __init__(self):
        self.value = 'A1'
    def foo(self):
        print('a1-foo')
    def foo1(self):
        print('a1-foo1') 
    def value0(self):
        print(self.value)
class A2:
    def __init__(self):
        self.value = 'A2'
    def foo(self):
        print('a2-foo')
    def foo2(self):
        print('a2-foo2')
    def value0(self):
        print(self.value)
class A3:
    def __init__(self):
        self.value = 'A3'
    def foo(self):
        print('a3-foo')
    def foo3(self):
        print('a3-foo3')
    def value0(self):
        print(self.value)
class B(A3):
    def __init__(self):
        self.a1 = A1()
        self.a2 = A2()
        super().__init__()   
        self._mode = 'a1'     
        
    def __getattribute2__(self, name):
        if False:
            try:
                mode = super().__getattribute__('_mode')
            except AttributeError:
                mode = None        
            
            if name not in ('__class__', 'size','shape','__len__'):
                print('getattr', name, f', [{mode=}]')
            
            if name == 'a3':
                self._mode = 'a3'
                return self
    
            if mode == 'a1':
                #check if in a1 and get if so, repeat for a2 then just return self
                for attr_name in ('a1', 'a2'):
                    attr = super().__getattribute__(attr_name)
                    if hasattr(attr, name):
                        return getattr(attr, name)
                return super().__getattribute__(name)                   
            if mode in (None, 'a3'):
                self._mode = 'a1'
                return super().__getattribute__(name)   
        
    def __getattribute__(self, name):
        try:
            mode = super().__getattribute__('_mode')
        except AttributeError:
            mode = None        
        
        if name not in ('__class__', 'size','shape','__len__'):
            print('getattr', name, f', [{mode=}]')
        
        if name == 'a3':
            self._mode = 'a3'
            return self

        if mode == 'a1':
            #check if in a1 and get if so, repeat for a2 then just return self
            for attr_name in ('a1', 'a2'):
                attr = super().__getattribute__(attr_name)
                print('m', attr_name, name, hasattr(attr, name))
                if hasattr(attr, name):
                    return getattr(attr, name)
                
            return super().__getattribute__(name)                   
        if mode in (None, 'a3'):
            self._mode = 'a1'
            return super().__getattribute__(name)        


    def __setattr__(self, name, value, j=90):  
        try:
            mode = super().__getattribute__('_mode')
        except AttributeError:
            mode = None               
            
        print('>> setattr >>', name, value, mode)
        
        if name == '_mode':
            super().__setattr__(name, value)
            return
        if hasattr(self, '_mode'):
            if super().__getattribute__('_mode') in ('a3','a33'):
                super().__setattr__(name, value)
                return 
        if name not in ('a1', 'a2','_mode'):
            for e in ('a1', 'a2'):
                a1 = super().__getattribute__(e)
                if hasattr(a1, name):
                    print('   -appeard in a1 or a2 and set there[277]')
                    setattr(a1, name, value)       
                    return 
        
        super().__setattr__(name, value)
        return
        print('setattr', name, value)
        if name in ('a1', 'a2'):
            super().__setattr__(name, value)
        elif name == '_outer':
            setattr(self._inner, name, value)
            super().__setattr__(name, value)
            
        elif hasattr(self._inner, name):
            setattr(self._inner, name, value)
        else:
            super().__setattr__(name, value)
#assert False          
b = B() 
print('\n\n\n Pritned Created \n\n\n\n')           
b.foo() #a1           
b.foo1()#a1
b.foo2()
b.foo3()
b.a1.foo()
b.a2.foo()
with capture_output() as messages:
    b.a3.foo()# wrong
assert messages[-1] == 'a3-foo'   
print('----')
print(b.value)
assert False
p = lambda : print('<A1 A1 A2 A3>:',b.value,b.a1.value,b.a2.value,b.a3.value)
p()
b.a1.value = 'A1**'
b.a2.value = 'A2**'
p()
b.value = b.value+'*' 
p()
b.a3.value = 9 







print('Finishes !!')




