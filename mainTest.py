import tetris2 as tt
import pygame as pg

grid = tt.Grid()
grid.move_down()
grid.move_down()

pg.init()
screen = pg.display.set_mode((960, 540))

running = True

ct = 0

while running:
    if ct ==1000:
        ct = 0
        grid.move_down()
    ct+=1
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    grid.paint(screen, 30)

    pg.display.flip()

pg.quit()