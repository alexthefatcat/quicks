# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 17:32:26 2026
@author: alexm




SamrtDict


from collections import namedtuple
from collections import OrderedDict
from types import SimpleNamespace
from collections import defaultdict




config = SimpleNamespace(host="localhost", port=8080)
config.port = 9000  # Modify existing attribute
config.debug = True  # Dynamically add new attribute
print(config.host)  # 'localhost' (dot-notation access)
print(config)  # SimpleNamespace(host='localhost', port=9000, debug=True)

# Automatically defaults missing keys to an empty list
groups = defaultdict(list)
groups["admin"].append("Alice")  # Creates key 'admin' with [] and appends
groups["admin"].append("Bob")
print(groups["admin"])  # ['Alice', 'Bob']
print(groups["user"])  # [] (created automatically on access)

d1 = {"a": 1, "b": 2}
d2 = {"b": 2, "a": 1}
print(d1 == d2)  # True (standard dict ignores order for equality)
od1 = OrderedDict([("a", 1), ("b", 2)])
od2 = OrderedDict([("b", 2), ("a", 1)])
print(od1 == od2)  # False (OrderedDict enforces strict order equality)
# Unique capability: Move a key to the beginning or end efficiently
od1.move_to_end("a")  # Moves 'a' to the end of the order

# Define the record blueprint
Point = namedtuple("Point", ["x", "y"])
p = Point(x=10, y=20)
print(p.x)  # Access by attribute name -> 10
print(p[0])  # Access by index like a regular tuple -> 10
x_val, y_val = p  # Unpackable like a regular tuple
# p.x = 15        # TypeError: cannot mutate immutable tuple fields


--------------------------------------------
from typing import TypedDict

class Movie(TypedDict):
    title: str
    year: int
# IDE will enforce that 'title' is str and 'year' is int
film: Movie = {"title": "Inception", "year": 2010}


from dataclasses import dataclass

@dataclass
class User:
    name: str
    role: str = "guest"  # Default value
    active: bool = True
u = User(name="Alice")
u.role = "admin"  # Mutable by default
print(u)  # User(name='Alice', role='admin', active=True)
--------------------------------------------

you can add new variables either by e['a'] = 1, or e.a = 1
you can set nested values with out creating there parent so p.people.bryanadams.age = 12 ? think more about this
default values?
items are in the order you put them









Feautres

d = SmartDict
d['a'] = 1
d[0] # 1
d.a =1


d() =-> call can have default v to give

#order is the order you put them in but you can change the order as well

for e in d:
    print(e)
    
for f,v in d.items():
    print(k,v)


d.person.name = 'Bob' # works

or

persons = SmartDict({'name':None, 'age':None})

d.person =??


persons('Bryan Adams', 29)






__SmartDict_v5 extends Python’s native dict with dot-notation attribute access (d.key) and dynamic autovivification. Reading non-existent nested keys automatically creates child nodes when nested=True, while assigning standard dictionary literals automatically wraps them into __SmartDict_v5 instances with shared parent configurations.

It introduces sequence-style positional lookups and slicing based on insertion order (e.g., d[0] and d[0:2]). To eliminate structural collisions between positional indices and dictionary keys, key types such as int, float, and NoneType are strictly disallowed.

The .schema() factory enables declarative data validation for types, choice sets, custom predicate functions, and field defaults. Additional features include versatile fallback defaults (__missing__), callable prime-key lookups (d()), recursive .to_dict() unwrapping, and attribute guards shielding private attributes (_) and IPython probes from accidental key creation.



"""



from itertools import islice
_PARAMETER_BLANK = object()



class __SmartDict_v1(dict):
    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)
        
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(f"'DotDict' object has no attribute '{key}'")

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError:
            raise AttributeError(f"'DotDict' object has no attribute '{key}'")



class __SmartDict_v2(dict):
    DISALLOWED_TYPES = (int, float, type(None))  # bool is a subclass of int

    def _validate_key(self, key):
        """Raises TypeError if key is int, float, bool, or None."""
        if isinstance(key, self.DISALLOWED_TYPES):
            type_name = type(key).__name__
            raise TypeError(f"SmartDict does not allow {type_name} keys: {repr(key)}")

    def __init__(self, *args, default=_PARAMETER_BLANK, prime=None, **kwargs):
        super().__init__()
        object.__setattr__(self, '_default', default)
        object.__setattr__(self, '_prime', prime)

        # Route initial keys through __setitem__ to trigger validation
        initial_data = dict(*args, **kwargs)
        for key, value in initial_data.items():
            self[key] = value

    def __setitem__(self, key, value):
        """Validates key type before setting key-value pair."""
        self._validate_key(key)
        super().__setitem__(key, value)
    
    def __getitem__(self, key):
        if isinstance(key, int) and not isinstance(key, bool):
            if key < 0:
                key += len(self)  # Handle negative indices like p3[-1]
            if 0 <= key < len(self):
                return next(islice(self.values(), key, None))
            raise KeyError(f"Index {key} out of range for dict of size {len(self)}")
        return super().__getitem__(key)

    def __missing__(self, key):
        default = object.__getattribute__(self, '_default')
        if default is _PARAMETER_BLANK:
            raise KeyError(key)
        return default(key) if callable(default) else default

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(f"'SmartDict' object has no attribute '{key}'")

    def __setattr__(self, key, value):
        if key in ('_default', '_prime'):
            super().__setattr__(key, value)
        else:
            self[key] = value  # Calls __setitem__ validation

    def __delattr__(self, key):
        if key in self:
            del self[key]
        else:
            raise AttributeError(f"'SmartDict' object has no attribute '{key}'")

    def __call__(self):
        prime = object.__getattribute__(self, '_prime')
        if prime is None:
            raise TypeError("No prime key configured for this SmartDict.")
        return self[prime]
    





class __SmartDict_v5(dict):
    """

    #Features of SmartDict:-
       #access values keys as well as [] and with prime set default key on call
    user = SmartDict(name = 'Bob', age=90, prime='name')
    user.name == user['name'] == user() == 'Bob' == user[0] 
    tuple(user[:]) == ('Bob', 90)
    tuple(user) == ('name', 'age')
    
    # nested attribute automaitcally setting
    user.conditions.heart.rate = 65
    user.conditions.heart.pressure = 150
    
    # convert to normal dic
    ndic = user.to_dict()
    
    # Schemas
    UserSchema = SmartDict.schema(
        name=str,    role=('admin', 'editor', 'viewer'), 
        age=lambda x: x >= 18,      status="active")
    
    u1 = UserSchema(name="Bob", role="admin", age=25)
    # -> SmartDict({'name': 'Bob', 'role': 'admin', 'age': 25, 'status': 'active'})
    u2 = UserSchema("Bryan", "admin", 45)
    


    
    
    
    
    Unified __SmartDict_v5 combining:
      1. Schema Validation (types, permitted choices, predicate lambdas, nested schemas)
      2. Interactive Dict Features (dot-notation, positional slicing d[0:2], index lookup d[0])
      3. Autovivification with nested=True (default=self.__class__ automatically set)
      4. Fallback Defaults (__missing__), Prime-Key Caller d(), and Auto-Nesting.
    """
    DISALLOWED_TYPES = (int, float, type(None))
    RESERVED_PROBE_ATTRS = {'getdoc', 'doc', 'help'}

    def __init__(self, data=None, *, default=_PARAMETER_BLANK, prime=None, _schema=None, nested=True, **kwargs):
        super().__init__()
        object.__setattr__(self, '_is_schema', _schema is not None)
        object.__setattr__(self, '_schema', _schema or {})
        object.__setattr__(self, '_prime', prime)
        object.__setattr__(self, '_nested', nested)

        # If nested=True and no explicit default was provided, default becomes self.__class__
        if nested and default is _PARAMETER_BLANK:
            default = self.__class__

        object.__setattr__(self, '_default', default)

        if not self._is_schema:
            initial_data = (data or {}) | kwargs
            for key, val in initial_data.items():
                self[key] = val

    @classmethod
    def schema(cls, default=_PARAMETER_BLANK, prime=None, nested=True, **fields):
        """Creates a schema factory supporting field validation, choice sets, lambdas, and defaults."""
        return cls(_schema=fields, default=default, prime=prime, nested=nested)

    def _validate_key(self, key):
        if isinstance(key, self.DISALLOWED_TYPES):
            type_name = type(key).__name__
            raise TypeError(f"'{self.__class__.__name__}' does not allow {type_name} keys: {repr(key)}")

    def __setitem__(self, key, value):
        self._validate_key(key)
        default = object.__getattribute__(self, '_default')
        prime = object.__getattribute__(self, '_prime')
        nested = object.__getattribute__(self, '_nested')

        # Auto-wrap raw nested dictionaries while preserving nested flag
        if isinstance(value, dict) and not isinstance(value, self.__class__):
            value = self.__class__(value, default=default, prime=prime, nested=nested)

        super().__setitem__(key, value)

    def __getitem__(self, key):
        # 1. Handle Slicing (e.g. d[0:2] or d[:-1])
        if isinstance(key, slice):
            return list(self.values())[key]

        # 2. Handle Positional Indexing (e.g. d[0], d[-1])
        if isinstance(key, int) and not isinstance(key, bool):
            length = len(self)
            idx = key + length if key < 0 else key
            if 0 <= idx < length:
                return next(islice(self.values(), idx, None))
            raise KeyError(f"Index {key} out of range for '{self.__class__.__name__}' of size {length}")

        return super().__getitem__(key)

    def __missing__(self, key):
        default = object.__getattribute__(self, '_default')
        if default is _PARAMETER_BLANK:
            raise KeyError(key)

        # Generate missing value using self.__class__ to prevent name mangling NameError
        if isinstance(default, type) and issubclass(default, self.__class__):
            val = default(nested=True)
        elif callable(default):
            try:
                val = default(key)
            except TypeError:
                val = default()
        else:
            val = default

        # Autovivification: save auto-created node if nested=True
        nested = object.__getattribute__(self, '_nested')
        if nested:
            self[key] = val

        return val

    def __getattr__(self, key):
        if key.startswith('_') or key in self.RESERVED_PROBE_ATTRS:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{key}'")
        try:
            return self[key]
        except KeyError:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{key}'")

    def __setattr__(self, key, value):
        if key.startswith('_'):
            super().__setattr__(key, value)
        else:
            self[key] = value

    def __delattr__(self, key):
        if key in self:
            del self[key]
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{key}'")

    def __call__(self, *args, **kwargs):
        if self._is_schema:
            return self._instantiate_schema(*args, **kwargs)

        if args or kwargs:
            raise TypeError(f"'{self.__class__.__name__}' instance call does not accept arguments unless configured as a schema.")
        prime = object.__getattribute__(self, '_prime')
        if prime is None:
            raise TypeError(f"No prime key configured for this '{self.__class__.__name__}'.")
        return self[prime]

    def _instantiate_schema(self, *args, **kwargs):
        input_data = {}
        schema_keys = list(self._schema.keys())

        if len(args) == 1 and isinstance(args[0], dict):
            input_data.update(args[0])
        elif args:
            if len(args) > len(schema_keys):
                raise TypeError(f"Schema accepts at most {len(schema_keys)} positional argument(s), got {len(args)}.")
            for key, val in zip(schema_keys, args):
                input_data[key] = val

        for key, val in kwargs.items():
            if key in input_data:
                raise TypeError(f"Got multiple values for argument '{key}'")
            input_data[key] = val

        validated = {}
        for field, rule in self._schema.items():
            if field not in input_data:
                if (
                    not isinstance(rule, type)
                    and not callable(rule)
                    and not isinstance(rule, (tuple, set, list))
                    and not (isinstance(rule, self.__class__) and rule._is_schema)
                ):
                    input_data[field] = rule
                else:
                    raise KeyError(f"Missing required field: '{field}'")

            val = input_data[field]

            if isinstance(rule, type):
                if not isinstance(val, rule):
                    raise TypeError(f"Field '{field}' expects type {rule.__name__}, got {type(val).__name__}")
            elif isinstance(rule, (tuple, set, list)):
                if val not in rule:
                    raise ValueError(f"Field '{field}' must be one of {tuple(rule)}, got '{val}'")
            elif isinstance(rule, self.__class__) and rule._is_schema:
                val = rule(val)
            elif callable(rule):
                if not rule(val):
                    raise ValueError(f"Value '{val}' failed validation for field '{field}'")
            else:
                if rule is not None and not isinstance(val, type(rule)):
                    raise TypeError(f"Field '{field}' expects type {type(rule).__name__}, got {type(val).__name__}")

            validated[field] = val

        default = object.__getattribute__(self, '_default')
        prime = object.__getattribute__(self, '_prime')
        nested = object.__getattribute__(self, '_nested')
        return self.__class__(validated, default=default, prime=prime, nested=nested)

    def to_dict(self, recursive=True):
        if not recursive:
            return dict(self)

        result = {}
        for key, value in self.items():
            if isinstance(value, self.__class__):
                result[key] = value.to_dict(recursive=True)
            elif isinstance(value, list):
                result[key] = [v.to_dict(recursive=True) if isinstance(v, self.__class__) else v for v in value]
            elif isinstance(value, tuple):
                result[key] = tuple(v.to_dict(recursive=True) if isinstance(v, self.__class__) else v for v in value)
            else:
                result[key] = value
        return result

    def update(self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).items():
            self[k] = v

    def __repr__(self):
        cls_name = self.__class__.__name__
        if self._is_schema:
            return f"{cls_name}.schema({', '.join(f'{k}={v!r}' for k, v in self._schema.items())})"

        default = object.__getattribute__(self, '_default')
        prime = object.__getattribute__(self, '_prime')
        nested = object.__getattribute__(self, '_nested')
        items_str = super().__repr__()
        extras = []
        if default is not _PARAMETER_BLANK and default is not self.__class__:
            extras.append(f"default={default!r}")
        if prime is not None:
            extras.append(f"prime={prime!r}")
        if not nested:
            extras.append("nested=False")

        suffix = f", {', '.join(extras)}" if extras else ""
        return f"{cls_name}({items_str}{suffix})"





# =====================================================================
# INTEGRATED ASSERTION TEST SUITE
# =====================================================================

def run_unified_tests(SmartDict):
    print("Running Unified SmartDict test suite...")

    # 1. Positional Indexing and Slicing
    d1 = SmartDict({'first': 10, 'second': 20, 'third': 30})
    assert d1[0] == 10, "Positional index [0] failed"
    assert d1[-1] == 30, "Positional index [-1] failed"
    assert d1[0:2] == [10, 20], "Positional slice [0:2] failed"

    # 2. Dynamic Default Fallback & Prime Key
    d2 = SmartDict({'id': 42, 'name': 'Alice'}, default='N/A', prime='name')
    assert d2.missing_key == 'N/A', "Missing default fallback failed"
    assert d2() == 'Alice', "Prime key caller failed"

    # 3. Auto-Nesting and Attribute Deletion
    d2.config = {'theme': 'dark'}
    assert isinstance(d2.config, SmartDict), "Auto-nesting standard dict failed"
    assert d2.config.theme == 'dark', "Nested dot notation failed"
    del d2.config
    assert 'config' not in d2, "Attribute deletion failed"

    # 4. Key Type Restrictions
    try:
        d2[100] = "forbidden"
        assert False, "Failed to block integer key"
    except TypeError as e:
        assert "does not allow int keys" in str(e)

    # 5. Schema Creation & Combined Validation
    UserSchema = SmartDict.schema(
        name=str,
        age=int,
        role=('Admin', 'User', 'Guest'),
        score=lambda s: 0 <= s <= 100,
        bio='No bio provided',
        default='UNSET',
        prime='name'
    )

    user = UserSchema('Bob', 28, 'Admin', 95)

    # Validate Schema Fields + Defaults
    assert user.name == 'Bob' and user.age == 28 and user.role == 'Admin'
    assert user.bio == 'No bio provided', "Schema default field assignment failed"

    # Validate v3 Features inside Schema Instances
    assert user() == 'Bob', "Prime caller inside schema instance failed"
    assert user.unknown_attribute == 'UNSET', "Schema dynamic default fallback failed"
    assert user[0] == 'Bob', "Positional index inside schema instance failed"
    assert user[0:2] == ['Bob', 28], "Positional slice inside schema instance failed"

    # 6. Recursive Export
    raw_dict = user.to_dict()
    assert type(raw_dict) is dict, "to_dict failed to return primitive dict"
    assert raw_dict['name'] == 'Bob'

    print("All unified test assertions passed successfully!")


if __name__ == '__main__':
    run_unified_tests(__SmartDict_v5)

    user = __SmartDict_v5()
    user.bryanadams.age =900
    user.bryanadams.health.bloodpressure = 120   
    user.bryanadams.health.heartrate =65
    user.bryanadams.name ='Bryan Adams'
    user.bryanadams._prime = 'name'
    heartrate = user[0][1][1]
    user.bryanadams()
    
    assert user['bryanadams']['age'] == 900
    
    for k,v in user.items():
        print(k,v)
        
    ndic = user.to_dict()
            
        
    User = __SmartDict_v5.schema(name=str, age=int, status=['Dead','Alive','CriticallyIll'], notes='')
    user1 = User('Bob', 56, 'Alive')
    
    assert tuple(list(user1)) == ('name', 'age', 'status', 'notes')
    assert tuple(user1[:]) == ('Bob', 56, 'Alive', '')

    for k,v in user1.items():
        print(f'{k} -> {repr(v)}')
    
    smart_dict_text0 = __SmartDict_v5({'a':1,'b':2})
    smart_dict_text1 = __SmartDict_v5({'a':1,'b':2}, default=56, prime='b')

    
    smart_dict_text0 = __SmartDict_v2({'a':1,'b':2})
    smart_dict_text1 = __SmartDict_v2({'a':1,'b':2}, default=56, prime='b')
    
    # Feature 1 add values using "."
    smart_dict_text0.c =3
    assert smart_dict_text0.c ==3
    
    # Feature 2 add values using default value
    assert smart_dict_text1.j == 56
    
    # Feature 3 add values using default value
    assert smart_dict_text1() == 2
    
    # Feature 4 add values using default value
    assert smart_dict_text1[1] == 2
    


    d = __SmartDict_v5({'a': 10, 'b': 20, 'c': 30}, default=99, prime='a')
    
    # Slicing support
    print(d[0:2])     # -> [10, 20]
    print(d[-2:])     # -> [20, 30]
    
    # Auto-nesting
    d.config = {'port': 8080, 'host': 'localhost'}
    print(d.config.port)  # -> 8080 (SmartDict powers passed down)
    
    # Custom Representation
    print(d)  # -> SmartDict({'a': 10, 'b': 20, 'c': 30, 'config': SmartDict({'port': 8080, 'host': 'localhost'}, default=99, prime='a')}, default=99, prime='a')
    
    




# protect keywords or they cant be acceses only specially
# for k,v in km: # would be the default





'''


2)  and isdea overcome shadowing keywords
3) why is the vairable not showing up in spyder vaible explorer any wat to overcome this   

    
    
Possbiel problems
   should dicts be autoconverted to samrt dicts inside the smart dict


Shdownaming is a possible huge problem


Some other relevent functions to investigate:-
    collections.ChainMap: Combines multiple dictionaries or mappings into a single logical view. When you look up a key, it searches through the underlying dictionaries sequentially from first to last until it finds a match.
    types.MappingProxyType: A dynamic, read-only wrapper around a standard dictionary. It allows you to expose dictionary data to other code or APIs while preventing any modifications or mutations.






'''





class SmartDict(__SmartDict_v5):
    pass









  




























