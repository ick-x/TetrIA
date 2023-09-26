import tetris2 as tt

grid = tt.Grid()

grid.move_down()
grid.save_piece()
print(grid.grid_color)