import asyncio
from enum import IntEnum
from typing import List, Tuple

BOARD_SIZE = 10


class Action(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class BaseAgent:
    direction: Action
    cells: List[Tuple[int, int]]

    def __init__(self) -> None:
        self.direction = None
        self.cells = None

    def update(self, direction: Action, cells: List[Tuple[int, int]]) -> None:
        """Updates the current direction and location of the snake.

        Args:
            direction (Action): The direction to move in.
            cells (List[Tuple[int, int]]): The cells that make up the snake.
        """

        self.direction = direction
        self.cells = cells


class SnakeGameRunner:
    def __init__(self, agent: BaseAgent) -> None:
        self.agent = agent

    async def run(self):
        pass


def main(agent: BaseAgent):
    asyncio.run(SnakeGameRunner(agent).run())
