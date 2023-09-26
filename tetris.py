import pygame

class Piece():
    x = 0
    y = 1
    grid = [[True,True],[False,True]]
    color = pygame.Color(0,0,0)
    
    def __init__(self, x, y, grid, color):
        self.x= x
        self.y = y
        self.grid = grid
        self.color = color
        
    def __init__(self):
        pass
        
    def paint(self, tileSize, marge, screen):
        pieceWidth = len(self.grid[0])*tileSize
        pieceHeight = len(self.grid)*tileSize
        
        pygame.Vector2
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j]:
                    rect = pygame.Rect(marge[0]+(self.x+j)*tileSize,-pieceHeight+marge[1]+(self.y-1-i)*tileSize,tileSize,tileSize)
                    pygame.draw.rect(screen, self.color, rect)
                  
                    
        
class Grid():
    x = 12
    y = 22
    pieces = [Piece()]
    gridBorderWidth = 4
    
    def __init__(self):
        pass
    
    def paint(self,screen,tileSize, marge):
        screenWidth = screen.get_width()
        screenHeight = screen.get_height()
        posX = (screenWidth-tileSize*self.x)/2
        posY = (screenHeight-tileSize*self.y)/2
        pygame.draw.rect(screen, pygame.Color(0,0,0),pygame.Rect(posX-self.gridBorderWidth, posY-self.gridBorderWidth, self.x*tileSize+self.gridBorderWidth*2,self.y*tileSize+self.gridBorderWidth*2))
        pygame.draw.rect(screen, pygame.Color(255,255,255),pygame.Rect(posX, posY, self.x*tileSize,self.y*tileSize))
        
        for piece in range(len(self.pieces)):
            self.pieces[piece].paint(tileSize,[posX,posY],screen)
    
    