import numpy as np
import pygame as pg


class Piece:
    grid = np.array([[True, False, True], [False, True, False]])
    x = 0
    y = -2
    color = pg.Color(255, 0, 0)

    def paint(self, tile_size, marge, screen):
        marge_x, marge_y = marge

        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if (self.grid[y][x]):
                    coord_tile_x = (self.x + x) * tile_size + marge_x
                    coord_tile_y = (self.y + y) * tile_size + marge_y
                    pg.draw.rect(screen, self.color, pg.Rect(coord_tile_x, coord_tile_y, tile_size, tile_size))

    def __init__(self):
        pass


class Grid:
    x = 12
    y = 18
    gridBorderWidth = 4

    current_piece = Piece()
    next_piece = Piece()
    stocked_piece = None

    grid_color = []

    def __init__(self):
        self.grid_color = [[pg.Color(155, 155, 155) for i in range(int(self.x))] for j in range(int(self.y))]
        pass

    def save_piece(self):
        piece = self.current_piece
        for y in range(len(piece.grid)):
            for x in range(len(piece.grid[0])):
                if piece.grid[y][x]:
                    new_x = int(piece.x + x)
                    new_y = int(piece.y + y)
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
        self.next_piece = Piece()

    def check_collision(self):
        piece = self.current_piece

        if piece.y + len(piece.grid) > self.y:
            return True

        for y in range(len(piece.grid)):
            for x in range(len(piece.grid[0])):
                if piece.grid[y][x]:
                    new_y = int(piece.y + y)
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
        pg.draw.rect(screen, pg.Color(155, 155, 155),
                     pg.Rect(pos_x, pos_y, self.x * tile_size, self.y * tile_size))

        self.current_piece.paint(tile_size, (pos_x, pos_y), screen)
        self.paint_grid(tile_size, (pos_x, pos_y), screen)

    def move_left(self):
        piece = self.current_piece
        if piece.x > 0:
            piece.x -= 1

    def move_right(self):
        piece = self.current_piece
        if piece.x + len(piece.grid) < self.x:
            piece.x += 1

    def move_down(self):
        piece = self.current_piece
        piece.y += 1
        if self.check_collision():
            piece.y -= 1
            self.save_piece()

    def move_instant(self):
        piece = self.current_piece
        while not self.check_collision():
            piece.y += 0.1
        piece.y -= 0.1

    def rotate(self):
        grid = self.current_piece.grid
        array = np.array([grid[i] for i in range(len(grid))])
        self.current_piece.grid = array.T

    def update(self, screen, tile_size):
        if self.current_piece.y + 1 < self.y:
            self.current_piece.y += 0.1
        self.paint(screen, tile_size)

    def paint_grid(self, tile_size, marge, screen):
        marge_x, marge_y = marge

        for y in range(len(self.grid_color)):
            for x in range(len(self.grid_color[0])):
                if self.grid_color[y][x] != pg.Color(155, 155, 155, 255):
                    coord_tile_y = y * tile_size + marge_y
                    coord_tile_x = x * tile_size + marge_x
                    pg.draw.rect(screen, self.grid_color[y][x], pg.Rect(coord_tile_x, coord_tile_y, tile_size, tile_size))
