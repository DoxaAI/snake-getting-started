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

                print("".join([f"{x}{y} " for x,y in self.snake]))
                print(f"{fruit[0]}{fruit[1]}")

            # request a move
            elif message[0] == "M":
                self.direction = await self.agent.make_move()
                
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

                # Wrap the board
                head = self._wrap_cell((x, y))

                self.board[self.snake[0][0]][self.snake[0][1]] = CellState.EMPTY
                self.board[self.snake[-1][0]][self.snake[-1][1]] = CellState.TAIL
                self.board[head[0]][head[1]] = CellState.HEAD
                
                self.snake.append(head)
                del self.snake[0]

                print(self.direction)

            # updates
            elif message[0] == "U":
                head = message[1]

                # Update the board
                self.board[self.snake[0][0]][self.snake[0][1]] = CellState.EMPTY
                self.board[self.snake[-1][0]][self.snake[-1][1]] = CellState.TAIL
                self.board[head[0]][head[1]] = CellState.HEAD

                print(f"{head[0]} {head[1]} ")

                if len(message) == 3:
                    tail = message[2]
                    fruit = message[3]

                    #update board
                    self.board[tail[0]][tail[1]] = CellState.TAIL
                    self.board[fruit[0]][fruit[1]] = CellState.FRUIT
                    
                    #update snake and fruit
                    self.snake.append(tail)
                    self.fruit = fruit

                    print(f"{tail[0]} {tail[1]} {fruit[0]} {fruit[1]} ")
                
            # unknown messages
            else:
                raise ValueError("Unknown command.")


def main(agent: BaseAgent):
    asyncio.run(SnakeGameRunner(agent).run())
