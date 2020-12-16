### A Pokemon game:

This is nice implementation of `__pyORM__` in a simple Pokemon game, the game is based on a public API (`https://pokeapi.co/api/v2/`)

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

* `state_manager` is a variable in `main.py`, the idea is inspired from the notion of state management in React/VueJS, I think it a niet approach to handler transitions between differents PyInquirer menus to avoid having multiple recursive `eval/exec`and maintain a smooth control flow while the game is running.


__Few screenshots__:

![](https://raw.githubusercontent.com/Dellagi/pySQL_API/main/pokemonApp/assets/screenshot_1.png)

![](https://raw.githubusercontent.com/Dellagi/pySQL_API/main/pokemonApp/assets/screenshot_2.png)

![](https://raw.githubusercontent.com/Dellagi/pySQL_API/main/pokemonApp/assets/screenshot_3.png)

