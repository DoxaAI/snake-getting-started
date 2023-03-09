import random
from typing import List

from snake import Action, BaseAgent, main, CellState

#################################################################
#   Modify the Agent class below to implement your own agent.   #
#   You may define additional methods as you see fit.           #
#################################################################


class Agent(BaseAgent):
    """An agent for the snake competition on DOXA."""

    async def make_move(self, board: List[List[CellState]]) -> Action:
        """Makes a move.
        Args:
            board (List[List[CellState]]): The current state of the board.
        Returns:
            Tuple[Tuple[int, int], str]: The coordinates of the head and direction of the snake.
        """

        return Action(random.randrange(4))


if __name__ == "__main__":
    main(Agent())
