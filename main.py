import random
import time
from collections import deque


# * is closed
# . is open
# b is bot
# s is switch
# f is fire 

q = 0.4
stack = deque()

GRID_SIZE = 5
grid = [['*' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

bot_cell = ()
switch_cell = ()

def get_neighbors(pos):
    x, y = pos
    neighbors = {}

    if x > 0: neighbors["top"] = (x - 1, y)
    if x < GRID_SIZE - 1: neighbors["bottom"] = (x + 1, y)
    if y > 0: neighbors["left"] = (x, y - 1)
    if y < GRID_SIZE - 1: neighbors["right"] = (x, y + 1)

    return neighbors

def get_direction(b_cell, s_cell): 
    r1, c1 = b_cell
    r2, c2 = s_cell
    if ((r1 == r2) and (c1 == c2)):
        return 'success'
    if ((r2 < r1) and (c2 < c1) and (0 < c1 <= GRID_SIZE - 1) and (0 <= c2 <= GRID_SIZE - 1) and (0 < r1 <= GRID_SIZE - 1)  and (0 <= r2 <= GRID_SIZE - 1)):
        return ((r1 - 1, c1), (r1, c1 - 1)) # up or left 
    if ((r2 < r1) and (c2 > c1) and (0 <= c1 < GRID_SIZE - 1) and (0 <= c2 <= GRID_SIZE - 1) and (0 < r1 <= GRID_SIZE - 1)  and (0 <= r2 <= GRID_SIZE - 1)):
        return ((r1 - 1, c1), (r1, c1 + 1)) # up or right 
    if ((r2 > r1) and (c2 < c1) and (0 < c1 <= GRID_SIZE - 1) and (0 <= c2 <= GRID_SIZE - 1) and (0 <= r1 < GRID_SIZE - 1)  and (0 <= r2 <= GRID_SIZE - 1)):
        return ((r1 + 1, c1), (r1, c1 - 1)) # down or left
    if ((r2 > r1) and (c2 > c1) and (0 <= c1 < GRID_SIZE - 1) and (0 <= c2 <= GRID_SIZE - 1) and (0 <= r1 < GRID_SIZE - 1)  and (0 <= r2 <= GRID_SIZE - 1)):
        return ((r1 + 1, c1), (r1, c1 + 1)) # down or right 
    # if (r2 < r1) and (0 <= c1 <= GRID_SIZE - 1) and (0 <= c2 <= GRID_SIZE - 1) and (0 < r1 <= GRID_SIZE - 1)  and (0 <= r2 <= GRID_SIZE - 1):
    #     return (r1 - 1, c1) # up
    # if (r2 > r1 and (0 <= c1 <= GRID_SIZE - 1) and (0 <= c2 <= GRID_SIZE - 1) and (0 <= r1 < GRID_SIZE - 1)  and (0 <= r2 <= GRID_SIZE - 1)):
    #     return (r1 + 1, c1) # down
    # if (c2 < c1 and (0 <= c1 < GRID_SIZE - 1) and (0 <= c2 <= GRID_SIZE - 1) and (0 <= r1 <= GRID_SIZE - 1)  and (0 <= r2 <= GRID_SIZE - 1)):
    #     return(r1, c1 - 1) # left
    # if (c2 > c1 and (0 < c1 <= GRID_SIZE - 1) and (0 <= c2 <= GRID_SIZE - 1) and (0 <= r1 <= GRID_SIZE - 1)  and (0 <= r2 <= GRID_SIZE - 1)):
    #     return (r1, c1 + 1) # right
    if r2 < r1: return (r1 - 1, c1)  # up
    if r2 > r1: return (r1 + 1, c1)  # down
    if c2 < c1: return (r1, c1 - 1)  # left
    if c2 > c1: return (r1, c1 + 1)  # right

    return 'Raj'

def setup_grid():

    # the first cell to open
    open_cell = (random.randint(1, GRID_SIZE - 2), random.randint(1, GRID_SIZE - 2))
    row, column = open_cell
    grid[row][column] = '.' 

    # list of all cells which are valid and we can open (with exectly one neighbor)

    valid_cells = []
    for neighbor in get_neighbors(open_cell).values():
        valid_cells.append(neighbor)

    # look through each valid cell and randomlly open cell 

    while valid_cells:
        rand = random.randint(0, len(valid_cells) - 1)

        valid_cell_to_open = valid_cells.pop(rand)

        valid_cell_row, valid_cell_column = valid_cell_to_open

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
            l, m = dead_end_neighbors[d]

            if (grid[l][m] == '*'):
                grid[l][m] = '.'
                break;
def bot(bot_cell, switch_cell, isbot3):

    print(f'bot was here {bot_cell}')
    print(f'switch was here {switch_cell}')
    visited = set()
    visited.add(bot_cell)
    directions = get_direction(bot_cell, switch_cell)

    if (directions == 'success'):
        print('succ')
        return switch_cell

    if (directions == 'Raj'):
        print('raj')
        return 0 

    isOnePath = False

    if (isinstance(directions[0], int)):        
        picked_direction = directions
        isOnePath = True
    else:
        picked_direction = random.choice(directions)
    
    r3, c3 = picked_direction
    r4, c4 = picked_direction

        # if possible also find other possible path 
    if((isOnePath == False)):
        for path in directions:
            if(path != picked_direction):
                picked_direction_2 = path
                break
        r4, c4 = picked_direction_2

    if(grid[r3][c3] == 's' or grid[r4][c4] == 's'):
        print('Mission completed')
        print()
        return switch_cell

        # if the neighbor is open we can pick it
    if (grid[r3][c3] == '.' and (r3, c3) not in visited):
        stack.append(bot_cell)
        visited.add((r3, c3)) 
        bot_cell = picked_direction
        print(f'using this path {picked_direction}')
        print()
        print()
        print()
        return bot_cell

    # if the first neighbor we picked is not open we can go to other neighbor we had 2 possible paths
    elif (grid[r4][c4] == '.' and (r4, c4) not in visited):
        stack.append(bot_cell)
        visited.add((r4, c4)) 
        bot_cell = picked_direction_2
        print(f'using this path {picked_direction_2}')
        return bot_cell

    # if we can't go to any given paths either one or both you will have to pick other possible path 
    elif (stack):
        previous_node = stack.pop()
        bot_cell = previous_node
        return 5
    else:
        # this would be need when the first node has blocked cells in it's best path
        print('you are f ed')
        return 0;
    return 5
    

# the bot one is this

setup_grid()
# listing open and closed cell 
open_cells = [
    (r_idx, c_idx) 
    for r_idx, row in enumerate(grid) 
    for c_idx, val in enumerate(row) 
    if val == '.'
]
closed_cells = [
    (r_idx, c_idx) 
    for r_idx, row in enumerate(grid) 
    for c_idx, val in enumerate(row) 
    if val == '*'
]

# placing bot and switch
r1 = random.randint(0, len(open_cells) - 1)
bot_cell =  open_cells[r1]
bot_row, bot_column = bot_cell
grid[bot_row][bot_column] = 'b'

r2 = random.choice(list(range(0, r1)) + list(range(r1 + 1, len(open_cells))))
switch_cell = open_cells[r2]
switch_row, switch_column = switch_cell

grid[switch_row][switch_column] = 's'

r3 = random.randint(0, len(open_cells) - 1)
init_fire_cell = open_cells[r3]
init_fire_cell_row, init_fire_cell_column = init_fire_cell

while (grid[init_fire_cell_row][init_fire_cell_column] != '.'):
    r3 = random.randint(0, len(open_cells) - 1)
    init_fire_cell = open_cells[r3]
    init_fire_cell_row, init_fire_cell_column = init_fire_cell
    break;
grid[init_fire_cell_row][init_fire_cell_column] = 'f'
fire_cells = []
fire_cells.append((init_fire_cell_row, init_fire_cell_column))

bot_cell_1 = bot_cell
paths = []
isbot3 = False

# for bot 1 
while(bot_cell_1 != switch_cell):
   bot_cell_1 = bot(bot_cell_1, switch_cell, isbot3)
   paths.append(bot_cell_1)

   if(bot_cell_1 == 0 or bot_cell_1 == 5):
    print('one condition with 5 ran')
    break

i = -1
while True:
    i = i + 1 
    temp_fire_cells = []
    visited_neighbors = []

    bot_cell = bot(bot_cell, switch_cell, False)
    print(f'bot moved to {bot_cell}')

    if (bot_cell == switch_cell):
        print('IT WORKED!!')
        break
    # look for only neighbor of fire cells to see if they catch fire 
    for raj in fire_cells:
        fire_cell_neighbors = get_neighbors(raj)
        # look through every neigbor
        for n in fire_cell_neighbors.values():
            if n not in visited_neighbors:
                r4, c4 = n
                neighbors_of_cell_to_fire = get_neighbors(n)
                # count how many neigbor of them are on fire 
                k = 0
                for l in neighbors_of_cell_to_fire.values():
                    r5, c5 = l
                    if(grid[r5][c5] == 'f'):
                        k = k + 1
                
                flammability = random.random()
                probability = 1 - (1 - q) ** k
                if (probability > flammability):
                    if n not in temp_fire_cells:
                        temp_fire_cells.append(n)
                visited_neighbors.append(n)

    for n in temp_fire_cells:
        r5, c5 = n 
        if(grid[r5][c5] != 'f'):
            grid[r5][c5] = 'f'
            fire_cells.append(n)  

    # for now this is not random  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! [puting neighbor cell on fire]
    
    time.sleep(1)


for row in grid:
    print(row)

print('')
print('')

print(f'this is the path for first bot {paths}')

