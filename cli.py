import asyncio
import os
import sys
import time

from game import SnakeGame

sys.path.append(os.path.dirname(os.path.abspath("submission/agent.py")))

from submission.agent import Agent

CLEAR_COMMAND = "cls" if os.name == "nt" else "clear"


class SnakeCLI:
    def __init__(self, game: SnakeGame) -> None:
        self.game = game

        self.icons = {
            0: " . ",
            1: " ■ ",
            2: " □ ",
            3: " & ",
        }

    async def render(self):
        self.game.initialise()

        size = self.game.board.size

        async for _ in self.game.run():
            # Render snake on the board
            os.system(CLEAR_COMMAND)
            for i in range(size):
                print(" ".join(self.icons[c] for c in self.game.board.board[i]))

            time.sleep(0.25)


async def main():
    # Instantiate the agent
    agent = Agent()

    # Start playing the game remotely
    game = SnakeGame(agent)

    ui = SnakeCLI(game)
    await ui.render()


if __name__ == "__main__":
    asyncio.run(main())
