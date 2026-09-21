import random

GRID_SIZE = 5;
grid = [['*' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def get_neighbors((x, y)):
    return {
        "left": (x, y - 1),
        "right": (x, y + 1),
        "top": (x - 1, y),
        "bottom": (x + 1, y)
    }

# the first cell to open
open_cell = (random.randint(1, GRID_SIZE - 1), random.randint(1, GRID_SIZE - 1))
row, column = open_cell
grid[row][column] = '.' 

# list of all cells which are valid and we can open 
valid_cells = [(row, column)]

# look through each valid cell and randomlly open cell 

while valid_cells:
    rand = random.randint(0, len(valid_cells) - 1)
    valid_cell = valid_cells.pop(rand)
    valid_cell_row, valid_cell_column = valid_cell

    neighbors = get_neighbors((valid_cell_row, valid_cell_column))
    neighbor_to_open = random.choice(list(neighbors))
    print(neighbors[neighbor_to_open])

    neighbor_row, neighbor_column = neighbors[neighbor_to_open]
    if((1 < neighbor_row < GRID_SIZE - 1) and (1 < neighbor_column < GRID_SIZE - 1)):
        grid[neighbor_row][neighbor_column] = '.'
  
    is_valid = all(
    grid[row][col] == "*" 
    for row, col in neighbors.values() 
    if (row, col) != (neighbor_row, neighbor_column)  
    and 0 <= row < GRID_SIZE                         
    and 0 <= col < GRID_SIZE                         
    )

    for n in neighbors.values():
        if ((n != neighbors[neighbor_to_open]) and is_valid):
            raj, patel = n 
            valid_cells.append((raj, patel))

for i in range(GRID_SIZE):
    print(grid[i])
