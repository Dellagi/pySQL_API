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
Setting ORM implementation aside, this application I believe is a neat approach to make a console application using PyInquirer menues with smooth and stable transitions between menus, and hadling eleagant display of information.
`state_manager` is a variable in `main.py`, the idea is inspired from the notion of state management in React/VueJS, to handle transitions between differents PyInquirer's menus to avoid having multiple recursive `eval/exec` and maintain a stable control flow while the game is running. The returns of the functions triggered via `eval` is also an analogy of `this.$emit` from React/VueJS.


__Few screenshots__:

![](https://raw.githubusercontent.com/Dellagi/pySQL_API/main/pokemonApp/assets/screenshot_1.png)

![](https://raw.githubusercontent.com/Dellagi/pySQL_API/main/pokemonApp/assets/screenshot_2.png)

![](https://raw.githubusercontent.com/Dellagi/pySQL_API/main/pokemonApp/assets/screenshot_3.png)

