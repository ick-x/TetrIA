import numpy as np
import pygame as pg

class Piece :
    grid = np.array([[True, True, True],[False,False,True]])
    x = 0
    y = 0
    color = pg.Color(0,0,0)
    
    def paint(self, tile_size, marge, screen):
        marge_x, marge_y = marge
        
        coord_piece_x, coord_piece_y = (marge_x + self.x*tile_size, marge_y+(self.y-1)*tile_size)
        
        tile_height = len(self.grid)
        
        for y in range(tile_height):
            for x in range(len(self.grid[0])):
                if(self.grid[y][x]):
                    coord_tile_x = coord_piece_x + x * tile_size
                    coord_tile_y = coord_piece_y + (y - tile_height) * tile_size
                
                    pg.draw.rect(screen, self.color, pg.Rect(coord_tile_x,coord_tile_y, tile_size, tile_size))
              
                
    def __init__(self):
        pass
        
        
        
class Grid:
    x = 12/2
    y = 22/2
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
        for x in range(len([piece.grid])):
            for y in range(len(piece.grid[0])):
                if piece.grid[x][y]:
                    self.grid_color[int(piece.y - len(piece.grid) + y)][int(x + piece.x)] = piece.color
                y += 1
            x += 1

    def generate_piece(self):
        self.pieces.pop()
        self.pieces.append(Piece())

    def check_collision(self):
        piece = self.current_piece
        if piece.y >= self.y:
            self.save_piece()
            self.generate_piece()
            return True

        x = 0
        for line in piece.grid:
            y = -len(piece.grid)
            for bool in line:
                if bool:
                    if self.grid_bool[y + int(piece.y)][x + int(piece.x)]:
                        self.save_piece()
                        self.generate_piece()
                        return True
                y += 1
            x += 1

    def paint(self, screen, tile_size):
        pos_x = (screen.get_width() - tile_size * self.x) / 2
        pos_y = (screen.get_height() - tile_size * self.y) / 2

        pg.draw.rect(screen, pg.Color(0, 0, 0),
                         pg.Rect(pos_x - self.gridBorderWidth, pos_y - self.gridBorderWidth,
                                     self.x * tile_size + self.gridBorderWidth * 2,
                                     self.y * tile_size + self.gridBorderWidth * 2))
        pg.draw.rect(screen, pg.Color(255, 255, 255),
                         pg.Rect(pos_x, pos_y, self.x * tile_size, self.y * tile_size))

        self.pieces[-1].paint(tile_size, (pos_x, pos_y), screen)
        self.check_collision()

        for y in range(len(self.grid_bool)):
            for x in range(len(self.grid_bool[0])):
                if (self.grid_bool[y][x]):
                    pg.draw.rect(screen, self.grid_color[y][x], pg.Rect(
                        pos_x + (x) * tile_size, (y-1) * tile_size + pos_y, tile_size, tile_size
                    ))

    def move_left(self):
        piece = self.current_piece
        if piece.x > 0:
            piece.x -= 1

    def move_right(self):
        piece = self.current_piece
        if piece.x + len(piece) < self.x:
            piece.x += 1

    def move_down(self):
        piece = self.current_piece
        if piece.y > 0:
            piece.y += 0.25
            
    def move_instant(self):
        piece = self.current_piece
        while not self.check_collision(self.current_piece):
            piece.y += 0.1          
        
    def rotate(self):
        grid = self.current_piece
        array = np.array([grid[i]for i in range(len(grid))])
        self.current_piece.grid = array.T
        
    def update(self, screen, tile_size):
        if self.current_piece.y+1 < self.y:
            self.current_piece.y += 0.1
        self.paint(screen, tile_size)
