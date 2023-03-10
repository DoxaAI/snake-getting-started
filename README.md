# Getting Started with Snake on DOXA

This repository contains everything you need to get started with Snake on DOXA. For more information, check out the [competition page](https://doxaai.com/competition/snake). 😎

Feel free to fork this repository and use it as the foundation for your own agents. You can also join the conversation on the [DOXA Community Discord server](https://discord.gg/MUvbQ3UYcf). 👀

## Prerequisites

Before you begin, please ensure that you have Python 3.9+ and the DOXA CLI installed.

If you do not yet have the DOXA CLI installed, you may do so using `pip`:

```bash
pip install -U doxa-cli
```

## Repository structure

- `submission/`: the directory that gets uploaded to DOXA
  - `submission/agent.py`: this is where you should implement your own agent!
  - `submission/doxa.yaml`: this is a configuration file used by DOXA to handle your submission
  - `submission/snake.py`: this is supporting code so that your agent can run on DOXA
- `game.py`: a local version of the Snake game engine
- `cli.py`: a CLI for playing against your own Snake agent (run with `python cli.py`)

## Snake rules

For this competition, we start with a 4-cell-long snake in the top left corner of a 10 &times; 10 board, moving right. A fruit will be randomly placed on the board as well. The goal of the game is to have the snake eat as many fruit as it can, growing a cell each time, before it runs into its own tail! The game ends when either the board is full (wow!) or you make an illegal move into your own tail. In this version of the game, the edges of the board wrap around, so you cannot die from running into a wall.

## Implementing an agent

First, clone this repository if you have not already done so. You can then start implementing your first agent by modifying the `Agent` class in `submission/agent.py`.

The only method in the `Agent` class that you have to change is `make_move()`.

### `make_move()` method

In Snake, the only input your agent has to provide is the direction which the snake will move in the next tick. Each direction has an 'Action' value.

```py
class Action(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
```

`make_move()` should return one of the four possible directions.

```py
Action.UP or Action.RIGHT or Action.DOWN or Action.LEFT
```

In order to determine which direction to move, you have access to the current Snake game board. The `board` parameter within `make_move()` is a list of lists of `CellState` values. The `CellState` enum represents all the possible states each cell can be in.

```py
class CellState(IntEnum):
    EMPTY = 0
    TAIL = 1
    HEAD = 2
    FRUIT = 3
```

`EMPTY` means that no snake nor fruit is within that cell at that tick in the game. `TAIL` indicates that **any** part of the snakes tail which is not its head is in that cell. `HEAD` indicates the front of the snake is in that cell. `FRUIT` means that the cell contains the fruit. There is only piece of fruit on the board at any given time.

**Note**: keep in mind that a move which is opposite of the current direction the snake is moving will be ignored (becuase otherwise the snake would instantly die), and the snake will continue moving in the direction it was previously moving.

By default, the agent tells the snake to move in random directions. What interesting strategies can you come up with? 👀

## Running the game locally

You can see how your agent (as defined in `submission/agent.py`) performs locally using the CLI script provided.

To launch the Snake CLI script, run the following command from the root of this repository:

```py
python cli.py
```

**Note**: on macOS and some flavours of Linux, use `python3` instead of `python`.

## Submitting to DOXA

Before you can submit your agent to DOXA, you must first ensure that you are logged into the DOXA CLI. You can do so with the following command:

```bash
doxa login
```

You should also make sure that you are enrolled on the [Snake competition page](https://doxaai.com/competition/snake).

Then, when you are ready to submit your agent (contained within the `submission` directory) to DOXA, run the following command from the root of the repository:

```bash
doxa upload submission
```

Please ensure that the `submission` directory only contains the files you wish to upload to DOXA. If you have renamed your submission directory to something else, substitute `submission` for the new directory name.
