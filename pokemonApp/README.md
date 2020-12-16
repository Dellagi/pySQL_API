### A Pokemon game:

This is a nice implementation of `__pyORM__` in a simple Pokemon game, the game is based on a public API (`https://pokeapi.co/api/v2/`)

__Requirements__:
* python +3.6 is required

__Libraries__:

- requests
- tqdm
- PyInquirer
- prompt-toolkit==1.0.14
- prettytable
- pyfiglet

### Setup and run

```bash
$ pip3 install -r requirements.txt
$ python3 main.py
```

__Important__:
Setting ORM implementation aside, there's also PokemonApp in the repo, it's an approach to make a console application using PyInquirer menues with smooth and stable transitions between menus, hadling easily (I hope) the display of information and messages. `state_manager` is a variable in `main.py`, the idea is inspired from the notion of state management in React/VueJS, when added to the form of returns from `poktools.py` it became able to handles the transitions between menus in a way that avoids having multiple nested `eval/exec` and maintain a stable flow of execution. Those returns (of the functions triggered via eval) are also an analogy of `this.$emit` from React/VueJS.


__Few screenshots__:

![](https://raw.githubusercontent.com/Dellagi/pySQL_API/main/pokemonApp/assets/screenshot_1.png)

![](https://raw.githubusercontent.com/Dellagi/pySQL_API/main/pokemonApp/assets/screenshot_2.png)

![](https://raw.githubusercontent.com/Dellagi/pySQL_API/main/pokemonApp/assets/screenshot_3.png)

