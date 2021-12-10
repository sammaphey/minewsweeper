from typing import List
import math
import pygame
import pygame.gfxdraw
import random
import functools
from dataclasses import dataclass
from enum import Enum
from util import build_adj_list

from tile import Tile

pygame.init()


class Dimension(Enum):

    NINE = 9
    SIXTEEN = 16
    TWENTY_FOUR = 24


MINES = {
    Dimension.NINE: {
        "probability": 10/81,
        "num_mines": 10,
        "difficulty": "beginner",
    },
    Dimension.SIXTEEN: {
        "probability": 40/256,
        "num_mines": 40,
        "difficulty": "intermediate",
    },
    Dimension.TWENTY_FOUR: {
        "probability": 99/576,
        "num_mines": 99,
        "difficulty": "expert",
    },
}


@dataclass
class Board:

    def __init__(self, dimension: Dimension = Dimension.NINE):
        """
        Create a minesweeper board.

        :param dimension: The dimension of the board (defaults to 9x9)
        """
        self.dimension: int = dimension.value
        self.difficulty: str = MINES[dimension]["difficulty"]
        self.mine_probability: float = MINES[dimension]["probability"]
        self.num_mines: int = MINES[dimension]["num_mines"]
        self.running = False
        self.EVENT_DISPATCH = {
            pygame.QUIT: self._handle_quit,
            pygame.MOUSEBUTTONDOWN: self._handle_click,
        }
        self.LCM = 144
        self.screen_dimensions = (self.LCM * 10, self.LCM * 7)
        pixel = math.floor(self.screen_dimensions[0] / self.dimension), \
            math.floor(self.screen_dimensions[1] / self.dimension)
        self.font = pygame.font.SysFont('Courier', math.floor(self.LCM / self.dimension) + 50)
        self.mines = []
        placed_mines = 0
        # gnerate bomb positions
        for _ in range(self.num_mines):
            while placed_mines < self.num_mines:
                x = random.randint(0, self.dimension - 1)
                y = random.randint(0, self.dimension - 1)
                if ((x, y) not in self.mines):
                    self.mines.append((x, y))
                    placed_mines += 1
        self.tiles: List[List[Tile]] = []
        # Construct the board in memory
        for i in range(self.dimension):
            self.tiles.append([])
            for j in range(self.dimension):
                # place a bomb in a random position
                rect = (i * pixel[0], j * pixel[1], pixel[0]-10, pixel[1]-10)
                # Determine the number of adjacent bombs
                adjs = build_adj_list(i, j)
                num = functools.reduce(
                    lambda acc, adj: int(adj in self.mines) + acc, adjs, 0
                )
                value = '*' if ((i, j) in self.mines) else num
                self.tiles[i].append(Tile(self, (i, j), value, rect))

    @classmethod
    def beginner(cls):
        """Start a beginner game, board size set to 9x9."""
        return cls(dimension=Dimension.NINE)

    @classmethod
    def intermediate(cls):
        """Start an intermediate game, board size set to 16x16."""
        return cls(dimension=Dimension.SIXTEEN)

    @classmethod
    def expert(cls):
        """Start an expert game, board size set to 24x24."""
        return cls(dimension=Dimension.TWENTY_FOUR)

    def run_game(self, logger):
        # Setup the display
        background_colour = (255, 255, 255)
        self.screen: pygame.Surface = pygame.display.set_mode(self.screen_dimensions)
        pygame.display.set_caption('Minesweeper')
        self.screen.fill(background_colour)
        self.running = True
        self.logger = logger

        # Construct the board look
        for row in self.tiles:
            [pygame.draw.rect(self.screen, (0, 0, 0), t.clickable_area) for t in row]
        pygame.display.update()

        while self.running:
            for event in pygame.event.get():
                self._handle_game_event(event)

    def all_tiles_revealed(self):
        return all(t.is_revealed or t.flagged for row in self.tiles for t in row)
        
    def _handle_game_event(self, event):
        func = self.EVENT_DISPATCH.get(event.type)
        if func:
            func(event)
        else:
            # self.logger.info(f"unrecognized event {event}")
            pass

    def _handle_quit(self, _):
        self.running = False

    def _handle_click(self, event):
        # Check if clicked on a tile
        for row in self.tiles:
            for tile in row:
                if tile.isclicked(event.pos):
                    if event.button == 1:
                        tile.click()
                    elif event.button == 3:
                        tile.right_click()

    def __str__(self):
        head = f"{self.difficulty.capitalize()} Board ({self.dimension}/{self.dimension})"
        board = ""
        for row in self.tiles:
            board += "  ".join(
                ["*" if t.is_mine else str(t.get_adjacent_mine_num()) for t in row]
            ) + "\n"
        return f"\n\n{head}\n\n{board}\n\n{self.mines}"
