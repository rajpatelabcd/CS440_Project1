import random

GRID_SIZE = 5;
grid = [['*' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def get_neighbors((x, y)):
    if((x > 0) and (x < GRID_SIZE - 1) and (y > 0) and (y < GRID_SIZE - 1)):
        return {
            "left": (x, y - 1),
            "right": (x, y + 1),
            "top": (x - 1, y),
            "bottom": (x + 1, y)
        }
    else:
        return 0

# the first cell to open
open_cell = (random.randint(1, GRID_SIZE - 1), random.randint(1, GRID_SIZE - 1))
row, column = open_cell
grid[row][column] = '.' 

# list of all cells which are valid and we can open (with exectly one neighbor)

valid_cells = []    
neighbors = get_neighbors((row, column))

if(neighbors != 0):
    valid_cells = list(neighbors.values())

# look through each valid cell and randomlly open cell 
while valid_cells:
    rand = random.randint(0, len(valid_cells) - 1)
    valid_cell_to_open = valid_cells.pop(rand)
    valid_cell_row, valid_cell_column = valid_cell_to_open

    neighbors = get_neighbors((valid_cell_row, valid_cell_column))

    if((1 < valid_cell_row < GRID_SIZE - 1) and (1 < valid_cell_column < GRID_SIZE - 1)):
        grid[valid_cell_row][valid_cell_column] = '.'
  
    is_valid = all(
    grid[row][col] == "*" 
    for row, col in neighbors.values() 
    if (row, col) != (valid_cell_row, valid_cell_column)  
    and 0 <= row < GRID_SIZE                         
    and 0 <= col < GRID_SIZE                         
    )
    neighbor_list = list(neighbors.values())

    for n in neighbors.values():
        if ((n != neighbor_list[rand]) and is_valid):
            raj, patel = n 
            valid_cells.append((raj, patel))

    print(valid_cells)

for i in range(GRID_SIZE):
    print(grid[i])
