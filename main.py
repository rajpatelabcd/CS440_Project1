import random

GRID_SIZE = 5;
grid = [['*' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def get_neighbors(pos):
    x, y = pos
    neighbors = {}

    if x > 0: neighbors["top"] = (x - 1, y)
    if x < GRID_SIZE - 1: neighbors["bottom"] = (x + 1, y)
    if y > 0: neighbors["left"] = (x, y - 1)
    if y < GRID_SIZE - 1: neighbors["right"] = (x, y + 1)

    return neighbors

# the first cell to open
open_cell = (random.randint(1, GRID_SIZE - 1), random.randint(1, GRID_SIZE - 1))
row, column = open_cell
grid[row][column] = '.' 

# list of all cells which are valid and we can open (with exectly one neighbor)

valid_cells = []    
neighbors = get_neighbors((row, column))

if neighbors:
    valid_cells = list(neighbors.values())

# look through each valid cell and randomlly open cell 
while valid_cells:
    rand = random.randint(0, len(valid_cells) - 1)
    valid_cell_to_open = valid_cells.pop(rand)
    valid_cell_row, valid_cell_column = valid_cell_to_open

    neighbors = get_neighbors(valid_cell_to_open)

    if((1 < valid_cell_row < GRID_SIZE - 1) and (1 < valid_cell_column < GRID_SIZE - 1)):
        grid[valid_cell_row][valid_cell_column] = '.'
  
    is_valid = all(
        grid[row][col] == "*" 
        for row, col in neighbors.values() 
        if (row, col) != (valid_cell_row, valid_cell_column)                          
    )
    neighbor_list = list(neighbors.values())

    for n in neighbors.values():
        if rand < len(neighbor_list) and n != neighbor_list[rand] and is_valid:
            valid_cells.append(n)


    print(valid_cells)

for i in range(GRID_SIZE):
    print(grid[i])
