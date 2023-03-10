from enum import IntEnum
from random import Random
from typing import List, Optional, Tuple

from submission.snake import BaseAgent

BOARD_SIZE = 10
SPAWNING_CELLS = [(0, 0), (0, 1), (0, 2), (0, 3)]


class Action(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class GameOver(ValueError):
    pass


class CellState(IntEnum):
    EMPTY = 0
    TAIL = 1
    HEAD = 2
    FRUIT = 3


class Board:
    def __init__(self, size, seed=None):
        self.rng = Random(seed)

        self.size = size

        self.direction = Action.RIGHT
        self.snake = [(0, 0), (0, 1), (0, 2), (0, 3)]  # tail to head

        self.fruit = None

        self._clear_board()

    def _clear_board(self):
        self.board = [
            [CellState.EMPTY for j in range(self.size)] for i in range(self.size)
        ]

    def spawn_snake(self, cells: List[Tuple[int, int]]) -> None:
        self.snake = cells[:]

        self.board[cells[-1][0]][cells[-1][1]] = CellState.HEAD
        for cell in cells[:-1]:
            self.board[cell[0]][cell[1]] = CellState.TAIL

    def spawn_fruit(self) -> Tuple[int, int]:
        possible_cells = [
            (i, j)
            for i in range(self.size)
            for j in range(self.size)
            if (i, j) not in self.snake
        ]

        if not possible_cells:
            raise GameOver

        cell = self.rng.choice(possible_cells)
        self.board[cell[0]][cell[1]] = CellState.FRUIT

        self.fruit = cell

        return self.fruit

    def is_alive(self) -> bool:
        """Check if the snake is alive.
        Returns:
          bool: True if the snake is alive, False otherwise.
        """

        head = self.snake[-1]
        snake_body = self.snake[:-1]

        return head not in snake_body

    def _wrap_cell(self, point: Tuple[int, int]) -> Tuple[int, int]:
        """Not a very useful comment.
        Args:
            point (Tuple[int, int]): TODO
        Returns:
            Tuple[int, int]: TODO
        """

        return (point[0] % self.size, point[1] % self.size)

    def get_direction(self, direction):
        # Check if impossible direction
        if self.direction == Action.UP and direction == Action.DOWN:
            return self.direction
        elif self.direction == Action.DOWN and direction == Action.UP:
            return self.direction
        elif self.direction == Action.RIGHT and direction == Action.LEFT:
            return self.direction
        elif self.direction == Action.LEFT and direction == Action.RIGHT:
            return self.direction
        return direction

    def _get_new_head_position(self, direction: Action) -> Tuple[int, int]:
        self.direction = self.get_direction(direction)

        # Determine head coords
        x, y = self.snake[-1][:]

        # Calc new head coords
        if self.direction == Action.UP:
            x -= 1
        elif self.direction == Action.DOWN:
            x += 1
        elif self.direction == Action.RIGHT:
            y += 1
        elif self.direction == Action.LEFT:
            y -= 1

        # Wrap the board cell
        return self._wrap_cell((x, y))

    def move(
        self, direction: Action
    ) -> Tuple[Tuple[int, int], Optional[Tuple[int, int]]]:
        """Moves the snake in a particular direction one step.
        Args:
            direction (Action): The direction.
        Raises:
            GameOver: The snake tried to move into itself.
        Returns:
            Tuple[int, int]: The new head location.
        """

        head = self._get_new_head_position(direction)

        is_eating_fruit = self.fruit == head

        if not is_eating_fruit:
            self.board[self.snake[0][0]][self.snake[0][1]] = CellState.EMPTY
            self.snake.pop(0)

        self.board[self.snake[-1][0]][self.snake[-1][1]] = CellState.TAIL
        self.board[head[0]][head[1]] = CellState.HEAD
        self.snake.append(head)

        if not self.is_alive():
            raise GameOver(
                f"Snake died at {self.snake[-1]} and length {len(self.snake)}."
            )

        if is_eating_fruit:
            return head, self.spawn_fruit()

        return head, None


class SnakeGame:
    def __init__(self, agent: BaseAgent, seed: Optional[int] = None) -> None:
        self.agent = agent
        self.board = Board(BOARD_SIZE, seed)

    def initialise(self) -> Tuple[List[Tuple[int, int]], Tuple[int, int]]:
        self.board.spawn_snake(SPAWNING_CELLS)
        fruit = self.board.spawn_fruit()

        return SPAWNING_CELLS, fruit

    async def _request_move(self) -> Action:
        """Request a move from the agent.
        Returns:
          Action: The direction to move in.
        """

        self.agent.update(self.board.direction, self.board.snake)

        return await self.agent.make_move(self.board.board)

    async def run(self) -> None:
        """Plays a game of snake."""

        try:
            while True:
                direction = await self._request_move()

                yield self.board.move(direction)
        except GameOver:
            pass
