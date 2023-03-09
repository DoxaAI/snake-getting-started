import asyncio
from enum import IntEnum
from typing import List, Tuple

BOARD_SIZE = 10
SPAWNING_CELLS = [(0, 0), (0, 1), (0, 2), (0, 3)]


class Action(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class CellState(IntEnum):
    EMPTY = 0
    TAIL = 1
    HEAD = 2
    FRUIT = 3


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

    async def make_move(self, board: List[List[CellState]]) -> Action:
        """Makes a move.

        Args:
            board (List[List[CellState]]): The current state of the board.

        Returns:
            Action: The action to take.
        """

        raise NotImplementedError()


class SnakeGameRunner:
    def __init__(self, agent: BaseAgent) -> None:
        self.agent = agent
        self.board = [[CellState.EMPTY for j in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]

    def _handle_initialisation(self):
        message = input().strip()
        assert message == "INIT"

        print("OK")

    def _wrap_cell(self, point: Tuple[int, int]) -> Tuple[int, int]:
        """Not a very useful comment.

        Args:
            point (Tuple[int, int]): TODO

        Returns:
            Tuple[int, int]: TODO
        """

        return (point[0] % self.size, point[1] % self.size)

    async def run(self):
        self._handle_initialisation()

        while True:
            message = input().strip().split(" ")

            # initialisation of the fruit / snake
            if message[0] == "I":
                self.snake = [(int(message[i]), int(message[i+1])) for i in range(1, len(message) - 2, 2)]
                self.fruit = (int(message[-2]), int(message[-1]))

                #game logic
                self.board[self.fruit[0]][self.fruit[1]] = CellState.FRUIT
                self.board[self.snake[0][0]][self.snake[0][1]] = CellState.HEAD
                for cell in self.snake[1:]:
                    self.board[cell[0]][cell[1]] = CellState.TAIL

            # request a move
            elif message[0] == "M":
                move = await self.agent.make_move(self.board)
                print(move.value) 

            # updates
            elif message[0] == "U":
                
                head_x = int(message[1])
                head_y = int(message[2])

                if len(message) == 5:
                    fruit_x = int(message[3])
                    fruit_y = int(message[4])

                    self.board[fruit_x][fruit_y] = CellState.FRUIT                    
                    self.fruit = (fruit_x, fruit_y)

                else:
                    self.board[self.snake[0][0]][self.snake[0][1]] = CellState.EMPTY
                    self.snake.pop(0)

                self.board[self.snake[-1][0]][self.snake[-1][1]] = CellState.TAIL
                self.board[head_x][head_y] = CellState.HEAD
                self.snake.append((head_x, head_y))

                
            # unknown messages
            else:
                raise ValueError("Unknown command.")


def main(agent: BaseAgent):
    asyncio.run(SnakeGameRunner(agent).run())
