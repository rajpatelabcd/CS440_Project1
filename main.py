import random

GRID_SIZE = 5

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
open_cell = (random.randint(1, GRID_SIZE - 2), random.randint(1, GRID_SIZE - 2))
row, column = open_cell
grid[row][column] = '.' 

# list of all cells which are valid and we can open (with exectly one neighbor)

valid_cells = []
for neighbor in get_neighbors(open_cell).values():
    valid_cells.append(neighbor)

print('initial valid cells are: ', valid_cells)
print('\n\n')

# look through each valid cell and randomlly open cell 
while valid_cells:

    rand = random.randint(0, len(valid_cells) - 1)
    valid_cell_to_open = valid_cells.pop(rand)
    valid_cell_row, valid_cell_column = valid_cell_to_open

    print('random cells we picked to open: ', valid_cell_to_open)

    if grid[row][column] == '.':
        continue
    print('\n\n')

    neighbors = get_neighbors(valid_cell_to_open)

    opened_neighbors = sum( 1 for r, c in neighbors.values() if grid[r][c] == '.')
    if opened_neighbors != 1:
        continue
    grid[row][column] = '.'


    for n in neighbors.values():
        r, c = n
        if grid[r][c] == '*' and n not in valid_cells:
            valid_cells.append(n)
    print('the list after adding the valid neighbor: ', valid_cells)
    print('\n\n')
    for row in grid:
        print(row)