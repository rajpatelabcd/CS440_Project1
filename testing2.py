import random
import time
from collections import deque


SPEED = 1


RED = '\033[91m'
RESET = '\033[0m'
GREEN = '\033[92m'
ORANGE = '\033[33m' 

backtracked = set() 
# * is closed
# . is open
# b is bot
# s is switch
# f is fire 

q = 0.4
stack = deque()
visited = set() 

GRID_SIZE = 10

grid = [
    ['.', '.', '.', '.', '.', '*', '.', '.', '*', '*'],
    ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
    ['.', 's', '.', '*', '*', '.', '*', '.', '.', '.'],
    ['*', '.', '*', '.', '*', '.', '.', '.', '*', '.'],
    ['*', '.', '*', '.', '.', '.', '*', '*', '*', '.'],
    ['.', '.', '.', '.', '*', '.', '.', '.', '.', 'b'],
    ['.', '.', '.', '*', '.', '.', '.', '.', '*', '.'],
    ['.', '.', '.', '*', '*', '*', '.', '.', '*', '.'],
    ['.', '*', '.', '.', '.', '.', '*', '*', '.', '.'],
    ['.', '.', '.', '*', '*', '.', '.', '.', '.', '.']
]

bot_cell = ()
switch_cell = ()


def print_colored_grid(grid, visited_set, backtracked_set, current_bot):
    print("\n--- Grid Update ---")
    for r in range(GRID_SIZE):
        row_str = []
        for c in range(GRID_SIZE):
            if (r, c) == current_bot:
                row_str.append('b')
            elif (r, c) in backtracked_set:
                row_str.append(f"{GREEN}.{RESET}")    # Green star for backtracking
            elif (r, c) in visited_set:
                row_str.append(f"{RED}.{RESET}")     # Red star for regular visited
            elif grid[r][c] == 'f':
                row_str.append(f"{ORANGE}f{RESET}")    # Orange 'f' for fire
            else:
                row_str.append(grid[r][c])
        print(" ".join(row_str))
    print("-------------------")

def get_neighbors(pos):
    x, y = pos
    neighbors = {}

    if x > 0: neighbors["top"] = (x - 1, y)
    if x < GRID_SIZE - 1: neighbors["bottom"] = (x + 1, y)
    if y > 0: neighbors["left"] = (x, y - 1)
    if y < GRID_SIZE - 1: neighbors["right"] = (x, y + 1)

    return neighbors

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

# look for all paths to find the best one using bfs

for n in range(GRID_SIZE):
    for l in range(GRID_SIZE):
        if grid[n][l] == 'b':
            bot_cell = (n, l)
        if grid[n][l] == 's':
            switch_cell = (n, l)


fringe = []

def find_best_path(b_cell, s_cell, isbot3):
    visited = []
    fringe = []
    r1, c1 = b_cell
    r2, c2 = s_cell
    fringe.append((b_cell, [b_cell]))
    visited.append(b_cell) 

    while fringe:
        f, current_path = fringe.pop(0)

        if (f == s_cell):
            return current_path
        # print(f'we lookin for neighbor of {f}')
        all_neighbors = get_neighbors(f)
        for neighbor in all_neighbors.values():
            r3, c3 = neighbor
            if(grid[r3][c3] == '.' or grid[r3][c3] == 's'):
                if neighbor not in visited:
                    new_path = current_path + [neighbor]
                    fringe.append((neighbor, new_path))
                    visited.append(neighbor)
            
    return None 


print(f'{bot_cell}, {switch_cell}')
ans = find_best_path(bot_cell, switch_cell, False)
print(ans)

# placing bot and switch
# r1 = random.randint(0, len(open_cells) - 1)
# bot_cell =  open_cells[r1]
# bot_row, bot_column = bot_cell
# grid[bot_row][bot_column] = 'b'

# r2 = random.choice(list(range(0, r1)) + list(range(r1 + 1, len(open_cells))))
# switch_cell = open_cells[r2]
# switch_row, switch_column = switch_cell

# grid[switch_row][switch_column] = 's'

for n in range(GRID_SIZE):
    for l in range(GRID_SIZE):
        if grid[n][l] == 'b':
            bot_cell = (n, l)
        if grid[n][l] == 's':
            switch_cell = (n, l)


open_cells = [
    (r, c)
    for r, row in enumerate(grid)
    for c, val in enumerate(row)
    if val == '.'
]

r3 = random.randint(0, len(open_cells) - 1)
init_fire_cell = open_cells[r3]
init_fire_cell_row, init_fire_cell_column = init_fire_cell

while (grid[init_fire_cell_row][init_fire_cell_column] != '.'):
    r3 = random.randint(0, len(open_cells) - 1)
    init_fire_cell = open_cells[r3]
    init_fire_cell_row, init_fire_cell_column = init_fire_cell
    break

grid[init_fire_cell_row][init_fire_cell_column] = 'f'
fire_cells = []
fire_cells.append((init_fire_cell_row, init_fire_cell_column))

# for bot 1 

init_path = find_best_path(bot_cell, switch_cell, False)
current_path = init_path

i = 0

bot2 = False
bot1 = False
bot3 = False

while True:
    bot_number = input("WHich bot you would like to run: ")
    if(bot_number == "1"):
        bot1 = True
        break
    elif(bot_number == "2"):
        bot2 = True
        break
    elif(bot_number == "3"):
        bot3 = True
        break
    else:
        print("Enter Valid numer")


for f in range(GRID_SIZE):
    print(grid[f])

while True:
    if (i > len(init_path) - 1):
        print('the first check')
        break 
    
    if bot_cell == -1:
        print('something when wrong from bot')
        break
    
    # here also add check for bot having no path

    if bot3:
        current_path = find_best_path(bot_cell, switch_cell, True)
        bot_cell = current_path[1]

        if bot_cell == -1:
            print("BOT LOST")
            break
   
    if bot2:
        current_path = find_best_path(bot_cell, switch_cell, False)
        bot_cell = current_path[1]

        if bot_cell == -1:
            print("BOT LOST")
            break

    if bot1:
        if i >= len(init_path):
            break
        i = i + 1
        bot_cell = init_path[i]
        print(f'bot moved to {bot_cell}')


    if (bot_cell == switch_cell):
        print('IT WORKED!!')
        break
    
    r7, c7 = bot_cell
    print(f'the bot wr got is {bot_cell} the value is {grid[r7][c7]}')

    if (grid[r7][c7] == 's'):
        print('It worked')
        break

    if grid[r7][c7] == 'f':
        print("BOT CAUGHT FIRE!")
        break

    if grid[r7][c7] != '.':
        print("The given cell is not open")
        break


    temp_fire_cells = []
    visited_neighbors = []

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
                if probability > flammability:
                    r, c = n
                    if grid[r][c] == '.':
                        if n not in temp_fire_cells:
                            temp_fire_cells.append(n)
                visited_neighbors.append(n)

    for n in temp_fire_cells:
        r5, c5 = n 
        if grid[r5][c5] not in ('f', 'b', 's'):
            grid[r5][c5] = 'f'
            fire_cells.append(n)  
    
    print_colored_grid(grid, visited, backtracked, bot_cell)

    time.sleep(SPEED)
