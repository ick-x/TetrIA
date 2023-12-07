import random

import numpy as np
import pygame as pg


class Piece:
    grid = np.array([[True, False, True], [False, True, False]])
    x = 0
    y = 0
    color = pg.Color(255, 0, 0)

    def rotate_right(self):
        new_grid = [[False for i in range(len(self.grid))] for j in range(len(self.grid[0]))]
        new_height_matrix = len(self.grid[0])-1
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                new_grid[new_height_matrix-x][y] = self.grid[y][x]
        self.grid = new_grid

    def toString(self):
        return ("(" + str(len(self.grid)) + "," + str(len(self.grid[0])) + ")", self.grid)

    def paint(self, tile_size, marge, screen, padding_y):
        marge_x, marge_y = marge

        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if (self.grid[y][x]):
                    coord_tile_x = (self.x + x) * tile_size + marge_x
                    coord_tile_y = (self.y + y) * tile_size + marge_y + padding_y
                    pg.draw.rect(screen, self.color, pg.Rect(coord_tile_x, coord_tile_y, tile_size, tile_size))

    def __init__(self, grid, color, grid_width):
        self.y = 0
        self.x = int((grid_width - len(grid[0])) / 2)
        self.grid = grid
        self.color = color
        pass


def get_pieces_list(grid_width):
    return [
        Piece([[True, True, True, True]], pg.Color(175, 175, 255), grid_width)
    ]


class Grid:
    animation_counter = 0
    x = 12
    y = 18
    gridBorderWidth = 4

    stocked_piece = None

    grid_color = []

    animation_length = 25

    def __init__(self):
        self.grid_color = [[pg.Color(155, 155, 155) for i in range(self.x)] for j in range(self.y)]
        self.current_piece = Piece([[False,True,False,False], [False,True,False,False], [False,True,False,False], [False,True,False,False]], pg.Color(175, 175, 255), self.x)
        self.next_piece = Piece([[False,True,False,False], [False,True,False,False], [False,True,False,False], [False,True,False,False]], pg.Color(175, 175, 255), self.x)
        pass

    def update_current_piece(self, pas):
        self.animation_counter = self.animation_counter + pas
        if (self.animation_counter > self.animation_length):
            self.current_piece.y += 1
            self.animation_counter = 0

    def save_piece(self):
        piece = self.current_piece
        for y in range(len(piece.grid)):
            for x in range(len(piece.grid[0])):
                if piece.grid[y][x]:
                    new_x = piece.x + x
                    new_y = piece.y + y
                    if new_x >= 0 and new_y >= 0:
                        self.grid_color[new_y][new_x] = piece.color
        self.generate_piece()

    def print(self):
        grid = ""
        for list in self.grid_color:
            for color in list:
                if color == pg.Color(155, 155, 155):
                    grid += "-"
                else:
                    grid += "o"
            grid += "\n"
        print(grid)

    def generate_piece(self):
        self.current_piece = self.next_piece
        pieces = get_pieces_list(self.x)
        self.next_piece = pieces[random.randint(0, len(pieces) - 1)]

    def check_collision(self):
        piece = self.current_piece

        if piece.y + len(piece.grid) > self.y - 1:
            return True
        if piece.x + len(piece.grid[0]) > self.x - 1:
            return True

        for y in range(len(piece.grid)):
            for x in range(len(piece.grid[0])):
                if piece.grid[y][x]:
                    new_y = int(piece.y + 1 + y)
                    new_x = int(piece.x + x)
                    if new_x >= 0 and new_y >= 0:
                        if self.grid_color[new_y][new_x] != pg.Color(155, 155, 155):
                            return True
        return False

    def paint(self, screen, tile_size):
        pos_x = (screen.get_width() - tile_size * int(self.x)) / 2
        pos_y = (screen.get_height() - tile_size * int(self.y)) / 2

        pg.draw.rect(screen, pg.Color(255, 255, 255),
                     pg.Rect(pos_x - self.gridBorderWidth, pos_y - self.gridBorderWidth,
                             self.x * tile_size + self.gridBorderWidth * 2,
                             self.y * tile_size + self.gridBorderWidth * 2))
        pg.draw.rect(screen, pg.Color(255, 255, 255),
                     pg.Rect(pos_x, pos_y, self.x * tile_size, self.y * tile_size))

        self.current_piece.paint(tile_size, (pos_x, pos_y), screen,
                                 self.animation_counter * tile_size / self.animation_length)
        self.paint_grid(tile_size, (pos_x, pos_y), screen)

        pg.draw.rect(screen, pg.Color(0, 0, 0),
                     pg.Rect(pos_x - self.gridBorderWidth, 0,
                             self.x * tile_size + self.gridBorderWidth * 2,
                             pos_y - self.gridBorderWidth))

    def move_left(self):
        piece = self.current_piece
        if piece.x > 0:
            piece.x -= 1

    def move_right(self):
        piece = self.current_piece
        if piece.x + len(piece.grid[0]) < self.x:
            piece.x += 1

    def move_down(self):
        piece = self.current_piece
        self.update_current_piece(10)
        self.check_collision_and_save()

    def move_instant(self):
        piece = self.current_piece
        while not self.check_collision():
            self.update_current_piece(10)
        self.save_piece()

    def rotate(self):
        self.current_piece.rotate_right()
        if(self.check_collision()):
            for i in range(3):
                self.current_piece.rotate_right()

    def update(self, screen, tile_size):
        self.update_current_piece(1)
        self.check_collision_and_save()
        self.paint(screen, tile_size)

    def paint_grid(self, tile_size, marge, screen):
        marge_x, marge_y = marge

        for y in range(len(self.grid_color)):
            for x in range(len(self.grid_color[0])):
                if self.grid_color[y][x] != pg.Color(155, 155, 155, 255):
                    coord_tile_y = y * tile_size + marge_y
                    coord_tile_x = x * tile_size + marge_x
                    pg.draw.rect(screen, self.grid_color[y][x],
                                 pg.Rect(coord_tile_x, coord_tile_y, tile_size, tile_size))

    def check_collision_and_save(self):
        if self.check_collision():
            self.save_piece()
