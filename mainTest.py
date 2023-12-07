import tetris2 as tt
import pygame as pg


piece = tt.Piece([[True, True, True], [False, True, False]], pg.Color(175, 175, 255), 12)
print(piece.toString())
piece.rotate_right()
print(piece.toString())
piece.rotate_right()
print(piece.toString())
