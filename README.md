# pySQL_API

[![Version](https://img.shields.io/badge/version-1.0.0-blue)]() [![Python](https://img.shields.io/badge/python-%2B3.6-green)]() [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


This is a simple approach to Object relational mapping, that allows you to you focus on objects manipulations and ligcal structures,
without the need to write the appropriate queries, insert/update..., for different elements

* Python +3.6 is required, only build-in libraries were used.
*
__Add__:
  In order to insert an object, all you have to do is:
```python
>>> from pyORM import orm
>>> obj_ = yourClass(args....)
# 'orm' will identify the object's attributes to generate the DB schema, and will also create the required table if it doesn't exist.
>>> dbSession = orm(obj_) # This will also create the required table if it doesn't exist
>>> dbSession.add()
```

__Update__:
  In order To save the updates:
  > Automatic update (using a decorator):
    As you can see in `classExample.py`, all you need to do is to put is `@updateAfterEvent` on top of the method,
    once the method returns the updated object (Example: `return self` or `return Obj`), the decorator will catch it
    and apply the updates to the appropriate table in the database
   
```python
@updateAfterEvent
def method1(self, args...):
  ...
  return self

@updateAfterEvent
def method2(self, obj_2, args ...):
  ...
  return obj_2
```
 * You can put the decorator in a separate file then import it wherever you'll be using it (Ex: `pokemonApp/mytools/utils.py`)
 
  > Manual update
  
  You can use the function `updateObj` (defined also in `pokemonApp/mytools/utils.py`):
```python
from utils import updateObj
obj_.attr += 10
updateObj(obj_)
````
  Or you can do the same manually:
  
```python
obj_.attr += 10
dbSession = orm(obj_)
updates_ = {k:v[0] for k, v in obj_.__dict__.items() if k[0]!="_"}
# pKey is the name of the primary key
dbSession.update({pKey: getattr(obj_, pKey)[0]}, **updates_)
```


__Get__:
  This module works in two directions, either it project your python's objects to a relational database,
  or create/reinitiate previously created objects based on the data saved in the DB.
  
> In this case you shouldn't initialize `orm` with an object like in the previous examples.
```python
dbSession = orm()
#Specifying tablename is the only requirement, then you can send any number of arguments (the logical operator between them is 'AND')
respSQL = dbSession.filterBy.get(tablename="dummy", arg1="...", arg2=1, ...)[0]
# I added [0] because I only wanted the first item from the array, but you can iterate you initiate multiple objects
obj_ = yourClass(*respSQL)
```

__Delete__:
  The same as in __Get__
  
```python
dbSession = orm()
#Specifying tablename is the only requirement, then 
respSQL = dbSession.filterBy.get(tablename="dummy", arg1="...", arg2=1, ...)[0]
obj_ = yourClass(*respSQL)
```

 ### In a nutshell:
 
 All you need to do to implement this module is having the initialized attributes follow this struct:
 
 ```python
 class dummy:
   # setting __tablename__ is mandatory
   __tablename__ = "dummy"
   def __init__(self, name, args...):
      ...
     # Just replace self.name = name with
    self.name = [name, "VARCHAR(255)", {"PRIMARY KEY": False, "AUTOINCREMENT": False, "FOREIGN KEY {} REFERENCES ...": False}]
```
  > In `self.name[2]` you can set any number of contrains you wish or none, but you must specify whether it's a primary key.
  
  Let make this more interesting and add the decorator!
  
   ```python
 from mytools.utils import updateAfterEvent
  
 class dummy:
   ...
   def __init__(self, args...):
      ...
   @updateAfterEvent
   def method(self, args...):
      ...
      return self #Or return the object you wish to update
  ```
  
  ### Example: (from PokemonApp)
  

```python
pika = PokemonClass(name="Pikachu", ..., hp=90)
crocodil = PokemonClass(name="Crocordil", ... , hp=90)


dbSession = orm(pika)
if not dbSession.add():
  print("{} Added successfully".format(pika.name[0]))

dbSession = orm(crocodil)
if not dbSession.add():
  print("{} Added successfully".format(crocodil.name[0]))



#Example of an attack
print(pika.hp[0], crocodil.hp[0])
# After the attack 'crocodil' will lose health points and the decorator will save the updated value in the database
crocodil = pika.attack(crocodil)
print(pika.hp[0], crocodil.hp[0])



# Extract pokemons attributes and instantiate pokemon object
dbSession = orm()

pokSQL = dbSession.filterBy.get(tablename="dummy", name="Pikachu")[0]
pika = dummyPokemonClass(*pokSQL)

pokSQL = dbSession.filterBy.get(tablename="dummy", name="Crocordil")[0]
crocodil = dummyPokemonClass(*pokSQL)



print(pika.name[0], crocodil.name[0])

# This time crocodil's hp will be 80 due to the previous attack
print(pika.hp[0], crocodil.hp[0])
```
  
