import pygame


class Piece:
    x = 0
    y = 0
    grid = [[True, True, True], [False, False, True]]
    color = pygame.Color(0, 0, 0)

    def __init__(self, x=0, y=2, grid=[[True, True, True], [False, False, True]], color=pygame.Color(0, 0, 0)):
        self.x = x
        self.y = y
        self.grid = grid
        self.color = color

    def paint(self, tile_size, marge, screen):
        piece_height = len(self.grid)
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j]:
                    rect = pygame.Rect(marge[0] + (self.x + j) * tile_size,
                                       marge[1] + (self.y - piece_height + i) * tile_size, tile_size, tile_size)
                    pygame.draw.rect(screen, self.color, rect)


class Grid:
    x = 12
    y = 22
    pieces = [Piece(0, 0, [[True, True, True, True]], pygame.Color(255, 0, 0)), Piece()]
    gridBorderWidth = 4

    grid_bool = []
    grid_color = []

    def __init__(self):
        self.grid_bool = [[False for i in range(self.x + 1)] for j in range(self.y + 1)]
        self.grid_color = [[pygame.Color(155, 155, 155) for i in range(self.x + 1)] for j in range(self.y + 1)]
        pass

    def save_piece(self):
        piece = self.pieces[1]
        for x in range(len([piece.grid])):
            for y in range(len(piece.grid[0])):
                if piece.grid[x][y]:
                    self.grid_bool[int(piece.y - len(piece.grid) + y)][int(x + piece.x)] = True
                    self.grid_color[int(piece.y - len(piece.grid) + y)][int(x + piece.x)] = piece.color
                y += 1
            x += 1

    def generate_piece(self):
        self.pieces.pop()
        self.pieces.append(Piece())

    def check_collision(self, piece):
        if piece.y >= 22:
            self.save_piece()
            self.generate_piece()
            return

        x = 0
        for line in piece.grid:
            y = -len(piece.grid) + 1
            for bool in line:
                if bool:
                    if piece.y == self.y or self.grid_bool[y + 1 + int(piece.y)][x + int(piece.x)]:
                        self.save_piece()
                        self.generate_piece()
                        return
            y += 1
        x += 1

    def paint(self, screen, tile_size):
        pos_x = (screen.get_width() - tile_size * self.x) / 2
        pos_y = (screen.get_height() - tile_size * self.y) / 2

        pygame.draw.rect(screen, pygame.Color(0, 0, 0),
                         pygame.Rect(pos_x - self.gridBorderWidth, pos_y - self.gridBorderWidth,
                                     self.x * tile_size + self.gridBorderWidth * 2,
                                     self.y * tile_size + self.gridBorderWidth * 2))
        pygame.draw.rect(screen, pygame.Color(255, 255, 255),
                         pygame.Rect(pos_x, pos_y, self.x * tile_size, self.y * tile_size))

        self.pieces[-1].paint(tile_size, [pos_x, pos_y], screen)
        self.check_collision(self.pieces[1])

        for y in range(len(self.grid_bool)):
            print("okk")
            for x in range(len(self.grid_bool[0])):
                print("ok")
                if (self.grid_bool[y][x]):
                    pygame.draw.rect(screen, self.grid_color[y][x], pygame.Rect(
                        pos_x + (x) * tile_size, (y-1) * tile_size + pos_y, tile_size, tile_size
                    ))

    def move_left(self):
        piece = self.pieces[1]
        if piece.x > 0:
            piece.x -= 1

    def move_right(self):
        piece = self.pieces[1]
        if piece.x + len(piece.grid[0]) < self.x:
            piece.x += 1

    def update(self, screen, tile_size):
        if self.pieces[1].y < self.y:
            self.pieces[1].y += 0.1
        self.paint(screen, tile_size)
