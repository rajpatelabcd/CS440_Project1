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



def set_maze():

    # the first cell to open
    open_cell = (random.randint(1, GRID_SIZE - 2), random.randint(1, GRID_SIZE - 2))
    row, column = open_cell
    grid[row][column] = '.' 

    # list of all cells which are valid and we can open (with exectly one neighbor)

    valid_cells = []
    for neighbor in get_neighbors(open_cell).values():
        valid_cells.append(neighbor)

    # print('initial valid cells are: ', valid_cells)
    # print('\n\n')

    # look through each valid cell and randomlly open cell 

    while valid_cells:
        rand = random.randint(0, len(valid_cells) - 1)

        valid_cell_to_open = valid_cells.pop(rand)

        valid_cell_row, valid_cell_column = valid_cell_to_open

        # print('random cell we picked to open: ', valid_cell_to_open)

        # check whether this cell is already open
        if grid[valid_cell_row][valid_cell_column] == '.':
            continue

        neighbors = get_neighbors(valid_cell_to_open)
        opened_neighbors = sum(
            1
            for r, c in neighbors.values()
            if grid[r][c] == '.'
        )

        # cell must have exactly one open neighbor
        if opened_neighbors != 1:
            continue

        # open the selected cell
        grid[valid_cell_row][valid_cell_column] = '.'

        # add blocked neighbors as possible candidates
        for n in neighbors.values():
            r, c = n
            if grid[r][c] == '*' and n not in valid_cells:
                valid_cells.append(n)
    for row in grid:
        print(row)

    dead_ends = []

    #  find valid dead ends and add to list 
    for grid_row, row in enumerate(grid):
        for grid_column, val in enumerate(row):           
            r = (grid_row, grid_column)
            neighbors2 = get_neighbors(r)
            opened_neighbors = sum(
                1
                for r, c in neighbors2.values()
                if grid[r][c] == '.'
            )
            if (opened_neighbors == 1) and (grid[grid_row][grid_column] == '.'):
                dead_ends.append((grid_row, grid_column))

    # for random dead ends open one of the neighbor cell until half list is done
    for i in range (len(dead_ends) // 2):
        rand_num = random.randint(0, len(dead_ends) - 1)
        dead_end_neighbors = get_neighbors(dead_ends[rand_num])

        # for now this is not random  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        for d in dead_end_neighbors:
            print(f'this is dead end {dead_ends[rand_num]}')
            l, m = dead_end_neighbors[d]

            if (grid[l][m] == '*'):
                print(f'     this one to open {dead_end_neighbors[d]}')
                dead_end_neighbors[d] == '.';
                break;

set_maze()