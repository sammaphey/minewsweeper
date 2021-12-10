from __future__ import annotations
from typing import List, Literal, Set, Tuple, Union
import pygame

from constants import BLUE, GREEN, RED
from util import build_adj_list


class Tile:

    def __init__(
        self,
        board,
        position: Tuple[int, int],
        value: Union[Literal["*"], int],
        clickable_area,
        flagged=False,
    ):
        """
        Create a tile in the board.

        :param position: A tuple representing the x and y position of the tile
            (relative to the board size).
        :param flagged: Whether or not the user has flagged the tile.
        """
        self.position = position
        self.x, self.y = self.position
        self.flagged = flagged
        self.board = board
        self.value = value
        self.clickable_area = clickable_area
        self.is_mine = self.value == '*'
        self.is_revealed = False

    def adjacent_tiles(self) -> List[Tile]:
        adjs = build_adj_list(self.x, self.y)
        tiles = []
        for possible_adj in adjs:
            if (
                possible_adj[0] > self.board.dimension - 1 or
                possible_adj[1] > self.board.dimension - 1 or
                possible_adj[0] < 0 or
                possible_adj[1] < 0
            ):
                continue
            tiles.append(self.board.tiles[possible_adj[0]][possible_adj[1]])
        return tiles

    def isclicked(self, position: Tuple[int, int]):
        x, y = position
        return (
            x > self.clickable_area[0] and
            x < self.clickable_area[0] + self.clickable_area[2] and
            y > self.clickable_area[1] and
            y < self.clickable_area[1] + self.clickable_area[3]
        )

    def set_flag(self):
        self.flagged = not self.flagged

    def click(self):
        self.reveal()
        center = self.board.screen_dimensions[0] / 2, self.board.screen_dimensions[1] / 2
        if self.is_mine:
            # Game ends
            self.board.screen.blit(self.board.font.render("END GAME", True, RED), center)
            pygame.display.update()
            # self.board.restart()
        if self.board.all_tiles_revealed():
            self.board.screen.blit(self.board.font.render("WON GAME", True, GREEN), center)
            pygame.display.update()
            # self.board.restart()

    def right_click(self):
        if self.is_revealed:
            return
        pos = self.clickable_area[0], self.clickable_area[1]
        self.set_flag()
        if self.flagged:
            self.board.screen.blit(self.board.font.render('|>', True, RED), pos)
        else:
            pygame.draw.rect(self.board.screen, (0, 0, 0), self.clickable_area)
        pygame.display.update()

    def reveal(self, prev_explored: Set[Tile] = None):
        pos = self.clickable_area[0], self.clickable_area[1]
        prev_explored = prev_explored or set()
        self.is_revealed = True
        if self.flagged:
            pygame.draw.rect(self.board.screen, (0, 0, 0), self.clickable_area)
        if self.is_mine:
            text = '*'
            color = RED
        else:
            prev_explored.add(self)
            if self.value == 0:
                for adj in self.adjacent_tiles():
                    if adj in prev_explored:
                        continue
                    adj.reveal(prev_explored)
            color = GREEN
            if self.value == 1:
                color = BLUE
            if self.value > 1:
                color = RED
            text = str(self.value)

        self.board.screen.blit(self.board.font.render(text, True, color), pos)
        pygame.display.update()

    def __str__(self):
        return f"Tile {'*' if self.is_mine else '-'} at position {self.position} with " \
               f"clickable area {self.clickable_area}, num adj " \
               f"mines: {self.value}"

    def __repr__(self):
        return self.__str__()
