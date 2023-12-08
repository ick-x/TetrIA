import random
import pygame as pg


class Piece:
    grid = []
    x = 0
    y = 0
    color = pg.Color(255, 0, 0)
    border_size = 2

    def rotate_right(self):
        new_grid = [[False for i in range(len(self.grid))] for j in range(len(self.grid[0]))]
        new_height_matrix = len(self.grid[0]) - 1
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                new_grid[new_height_matrix - x][y] = self.grid[y][x]
        self.grid = new_grid

    def paint(self, tile_size, marge, screen, padding_y, shadow):
        marge_x, marge_y = marge

        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if self.grid[y][x]:
                    coord_tile_x = (self.x + x) * tile_size + marge_x
                    coord_tile_y = (self.y + y) * tile_size + marge_y + padding_y
                    pg.draw.rect(screen, get_border_color(shadow, self.color),
                                 pg.Rect(coord_tile_x, coord_tile_y, tile_size, tile_size))
                    pg.draw.rect(screen, self.color, pg.Rect(coord_tile_x, coord_tile_y, tile_size - self.border_size,
                                                             tile_size - self.border_size))

    def __init__(self, grid, color, grid_width, ):
        self.y = 0
        self.x = int((grid_width - len(grid[0])) / 2)
        self.grid = grid
        self.color = color
        pass


def get_pieces_list(grid_width):
    return [
        Piece([
            [False, True, False, False],
            [False, True, False, False],
            [False, True, False, False],
            [False, True, False, False]], pg.Color(0, 240, 240), grid_width)
    ]


def get_random_piece(grid_width):
    piece_list = get_pieces_list(grid_width)
    piece = piece_list[random.randint(0, len(piece_list) - 1)]
    nb_rota = random.randint(0, 3)
    for i in range(nb_rota):
        piece.rotate_right()
    return piece


def get_border_color(shadow, color):
    return pg.Color(0 if color.r < shadow else color.r - shadow,
                    0 if color.g < shadow else color.g - shadow,
                    0 if color.b < shadow else color.b - shadow)


class Grid:
    animation_counter = 0
    x = 12
    y = 18
    gridBorderWidth = 4
    shadow = 20
    score = 0

    stocked_piece = None

    grid_color = []

    animation_length = 25

    def __init__(self):
        self.square_border_size = 2
        self.grid_color = [[pg.Color(155, 0, 0) if j == 0 else pg.Color(155, 155, 155) for i in range(self.x)] for j in
                           range(self.y)]

        self.current_piece = get_random_piece(self.x)
        self.next_piece = get_random_piece(self.x)

    def update_current_piece(self, pas):
        self.animation_counter = self.animation_counter + pas
        if self.animation_counter > self.animation_length:
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

        for y in range(len(piece.grid)):
            for x in range(len(piece.grid[0])):
                if piece.grid[y][x]:
                    new_y = int(piece.y + 1 + y)
                    new_x = int(piece.x + x)
                    if new_x > self.x - 1 or new_y > self.y - 1 or new_x < 0 or new_y < 0:
                        return True
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
        pg.draw.rect(screen,
                     pg.Color(255, 255, 255),
                     pg.Rect(
                         pos_x,
                         pos_y,
                         self.x * tile_size,
                         self.y * tile_size))

        self.current_piece.paint(tile_size,
                                 (pos_x, pos_y),
                                 screen,
                                 self.animation_counter * tile_size / self.animation_length, self.shadow)
        self.paint_grid(tile_size, (pos_x, pos_y), screen)
        self.next_piece.paint(tile_size, ((pos_x - tile_size * (self.next_piece.x + 7), pos_y)), screen, 0, self.shadow)

    def move_left(self):
        piece = self.current_piece
        piece.x -= 1
        if self.check_collision():
            piece.x += 1

    def move_right(self):
        piece = self.current_piece
        piece.x += 1
        if self.check_collision():
            piece.x -= 1

    def move_down(self):
        self.update_current_piece(10)
        self.check_collision_and_save()

    def move_instant(self):
        while not self.check_collision():
            self.update_current_piece(10)
        self.save_piece()

    def rotate(self):
        self.current_piece.rotate_right()
        if self.check_collision():
            for i in range(3):
                self.current_piece.rotate_right()

    def update(self, screen, tile_size):
        self.update_current_piece(1)
        self.check_collision_and_save()
        self.check_full_line()
        self.paint(screen, tile_size)

    def paint_grid(self, tile_size, marge, screen):
        marge_x, marge_y = marge

        for y in range(len(self.grid_color)):
            for x in range(len(self.grid_color[0])):
                if self.grid_color[y][x] != pg.Color(155, 155, 155, 255):
                    coord_tile_y = y * tile_size + marge_y
                    coord_tile_x = x * tile_size + marge_x
                    pg.draw.rect(screen,
                                 get_border_color(self.shadow, self.grid_color[y][x]),
                                 pg.Rect(
                                     coord_tile_x,
                                     coord_tile_y,
                                     tile_size,
                                     tile_size))

                    pg.draw.rect(screen,
                                 self.grid_color[y][x],
                                 pg.Rect(
                                     coord_tile_x,
                                     coord_tile_y,
                                     tile_size - self.square_border_size,
                                     tile_size - self.square_border_size))

    def check_collision_and_save(self):
        if self.check_collision():
            self.save_piece()

    def check_full_line(self):
        lines = []
        for line in range(self.y):
            full_line = True
            for case in range(self.x):
                if self.grid_color[line][case] == pg.Color(155, 155, 155):
                    full_line = False
                    break
            if full_line:
                lines.append(line)
        nb_lines = len(lines)
        for i in range(nb_lines):
            self.grid_color.remove(self.grid_color[lines[i] - i])
        self.grid_color = [
            [pg.Color(155, 155, 155) for i in range(self.x)] if j < nb_lines else self.grid_color[j - nb_lines] for j in
            range(self.y)]

        if nb_lines > 0:
            match nb_lines:
                case 1:
                    self.score += 40
                case 2:
                    self.score += 100
                case 3:
                    self.score += 300
                case _:
                    self.score += 1200
