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

GRID_SIZE = 30

grid = [
    ['.', '.', '*', '*', '.', '*', '*', '.', '.', '.', '.', '.', '.', '*', '.', '.', '.', '*', '.', '.', '.', '.', '.', '.', '.', '.', '.', '*', '.', '.'],
    ['.', '.', '*', '.', '.', '.', '.', '.', '*', '.', '*', '.', '.', '.', '*', '.', '*', '.', '*', '.', '.', '.', '.', '.', '.', '.', '.', '.', '*', '.'],
    ['.', '*', '.', '.', '*', '.', '*', '.', '*', '.', '.', '.', '*', '.', '*', '.', '.', '.', '*', '.', '.', '*', '.', '.', '*', '*', '.', '*', '*', '.'],
    ['.', '.', '*', '*', '.', '.', '.', '.', '.', '*', '*', '.', '*', '.', '*', '.', '*', '.', '.', '.', '*', '.', '.', '.', '.', '*', '.', '*', '.', '.'],
    ['*', '.', '.', '*', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '*', '*', '.', '.', '*', '.', '.', '*', '.', '*', '*', '.', '.', '.', '.', '*'],
    ['.', '*', '.', '.', '.', '.', '.', '.', '*', '.', '*', '*', '.', '*', '.', '.', '*', '.', '.', '*', '.', '*', '.', '.', '.', '.', '*', '.', '*', '.'],
    ['.', '.', '.', '*', '.', '.', '.', '*', '.', '.', '.', '*', '.', '.', '.', '*', '.', '.', '.', '*', '.', '.', 'b', '*', '*', '.', '.', '.', '.', '.'],
    ['*', '.', '*', '*', '.', '.', '.', '.', '*', '.', '*', '*', '*', '*', '.', '.', '*', '.', '.', '.', '.', '*', '*', '.', '.', '.', '.', '.', '*', '.'],
    ['*', '.', '*', '.', '*', '.', '*', '.', '.', '.', '.', '*', '.', '.', '.', '*', '.', '*', '.', '*', '.', '.', '.', '.', '*', '.', '*', '*', '.', '.'],
    ['.', '.', '*', '.', '.', '*', '.', '.', '*', '.', '*', '*', '.', '*', '.', '*', '.', '*', '.', '.', '.', '*', '.', '*', '.', '.', '.', '.', '.', '*'],
    ['.', '*', '.', '*', '.', '.', '.', '.', '*', '.', '.', '.', '*', '*', '.', '.', '.', '.', '*', '.', '*', '.', '.', '*', '.', '*', '.', '*', '.', '.'],
    ['.', '*', '.', '*', '.', '.', '.', '.', '.', '*', '.', '*', '.', '.', '.', '.', '*', '.', '.', '.', '.', '*', '.', '.', '.', '.', '*', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '*', '.', '.', '.', '*', '.', '*', '.', '.', '.', '*', '.', '*', '.', '.', '.', '*', '.', '*', '.', '.', '*', '.'],
    ['.', '*', '.', '.', '.', '.', '.', '.', '.', '.', '*', '*', '.', '*', '.', '.', '.', '.', '.', '.', '.', '.', '.', '*', '*', '.', '.', '*', '*', '.'],
    ['.', '.', '*', '*', '.', '.', '.', '.', '.', '.', '*', '.', '.', '.', '.', '*', '*', '.', '*', '.', '*', '*', '.', '*', '.', '.', '*', '.', '.', '.'],
    ['.', '*', '.', '.', '.', '.', '*', '.', '*', '.', '.', '.', '*', '.', 's', '.', '*', '.', '*', '.', '*', '.', '.', '.', '.', '*', '*', '.', '*', '.'],
    ['.', '.', '*', '.', '*', '.', '.', '.', '*', '*', '.', '.', '*', '.', '*', '.', '.', '.', '.', '*', '.', '*', '.', '*', '*', '*', '.', '.', '.', '.'],
    ['.', '*', '.', '*', '.', '.', '*', '.', '.', '.', '.', '*', '.', '.', '.', '*', '.', '*', '.', '.', '.', '.', '.', '.', '.', '.', '.', '*', '.', '*'],
    ['.', '.', '.', '*', '.', '*', '.', '*', '.', '.', '.', '.', '.', '*', '*', '.', '.', '.', '*', '*', '.', '*', '.', '.', '*', '.', '*', '*', '.', '.'],
    ['.', '*', '.', '.', '*', '.', '.', '.', '.', '.', '.', '*', '*', '.', '.', '.', '*', '.', '*', '.', '.', '*', '.', '.', '*', 'f', '.', '.', '.', '.'],
    ['*', '.', '.', '*', '.', '.', '.', '.', '.', '*', '.', '.', '.', '*', '.', '*', '*', '*', '.', '.', '.', '.', '.', '.', '.', '.', '*', '*', '.', '.'],
    ['.', '.', '*', '.', '.', '*', '.', '*', '*', '.', '.', '*', '.', '*', '.', '*', '*', '.', '.', '.', '.', '.', '*', '.', '.', '.', '.', '*', '.', '*'],
    ['*', '.', '.', '*', '.', '*', '.', '.', '.', '*', '.', '.', '.', '.', '.', '.', '.', '.', '*', '.', '.', '*', '.', '*', '.', '.', '.', '.', '.', '.'],
    ['.', '*', '.', '.', '.', '.', '*', '.', '*', '.', '.', '.', '.', '.', '.', '*', '*', '*', '.', '.', '.', '.', '.', '*', '.', '*', '.', '*', '*', '.'],
    ['.', '.', '.', '*', '*', '.', '.', '.', '.', '.', '*', '*', '.', '*', '.', '.', '.', '.', '.', '*', '.', '.', '.', '*', '.', '.', '.', '.', '.', '*'],
    ['*', '*', '*', '*', '.', '*', '*', '*', '*', '.', '.', '.', '.', '.', '.', '*', '*', '*', '.', '.', '.', '.', '.', '.', '.', '*', '.', '*', '.', '*'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '*', '*', '.', '.', '.', '.', '.', '.', '.', '*', '.', '.', '.', '*', '.', '*', '.', '*', '.', '.'],
    ['.', '*', '*', '.', '*', '.', '.', '.', '.', '*', '.', '*', '.', '.', '.', '.', '*', '*', '.', '.', '.', '*', '.', '.', '.', '.', '.', '*', '.', '.'],
    ['.', '.', '.', '.', '.', '*', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '*', '.', '.', '.', '.', '.', '*', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '*', '.', '.', '.', '.', '.', '.', '.', '*', '.', '.', '.', '*', '.', '.', '.', '*', '.', '.', '*', '*', '*', '.', '.', '*', '.']
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

def bot(bot_cell, switch_cell, isbot3, visited):

    visited.add(bot_cell)

    # print(f'bot was here {bot_cell}')
    # print(f'switch was here {switch_cell}')

    visited.add(bot_cell)
    directions = get_direction(bot_cell, switch_cell)

    if (directions == 'success'):
        print('succ')
        return switch_cell

    if (directions == 'Raj'):
        print('raj')
        return -1

    isOnePath = False

    if (isinstance(directions[0], int)):        
        picked_direction = directions
        isOnePath = True
    else:
        direction_1 = directions[0]
        direction_2 = directions[1]

        distance_1 = abs(switch_cell[0] - direction_1[0]) + abs(switch_cell[1] - direction_1[1])
        distance_2 = abs(switch_cell[0] - direction_2[0]) + abs(switch_cell[1] - direction_2[1])

        if distance_1 < distance_2:
            picked_direction = direction_1
        elif distance_2 < distance_1:
            picked_direction = direction_2
        else:
            picked_direction = random.choice(directions)
    
    r3, c3 = picked_direction
    r4 = c4 = None

    picked_direction_2 = None

    # if possible also find other possible path 
    if((isOnePath == False)):
        for path in directions:
            if(path != picked_direction):
                picked_direction_2 = path
                break
        r4, c4 = picked_direction_2

    if grid[r3][c3] == 's' or (r4 is not None and grid[r4][c4] == 's'):
        # print('Mission completed')
        # print()
        return switch_cell

        # if the neighbor is open we can pick it
   
    if (grid[r3][c3] == '.' and (r3, c3) not in visited):
        stack.append(bot_cell)
        visited.add((r3, c3))
        bot_cell = picked_direction
        # print(f'using this path {picked_direction}')
        # print()
        # print()
        # print()
        return bot_cell

    elif ((r4 is not None) and (grid[r4][c4] == '.' ) and ((r4, c4) not in visited)):
        stack.append(bot_cell)
        visited.add((r4, c4))
        bot_cell = picked_direction_2
        # print(f'using this path {picked_direction_2}')
        return bot_cell
    
    # if the first neighbor we picked is not open we can go to other neighbor we had 2 possible bot1_paths
    elif (r4 is not None and c4 is not None and grid[r4][c4] == '.' and (r4, c4) not in visited):
        stack.append(bot_cell)
        visited.add((r4, c4)) 
        bot_cell = picked_direction_2
        # print(f'using this path {picked_direction_2}')
        return bot_cell

    # if we can't go to any given bot1_paths either one or both you will have to pick other possible path 


    # look for any other open cell 
    else: 
        ne = get_neighbors(bot_cell)
        for n in ne.values():   
            rr, cc = n
            if(grid[rr][cc] == '.' and n not in visited):
                stack.append(bot_cell)
                visited.add((rr, cc))
                bot_cell = n
                # print(f'using this path {n}')
                return bot_cell

    if stack:
        previous_node = stack.pop()
        backtracked.add(bot_cell)
        visited.add(bot_cell)
        bot_cell = previous_node
        return bot_cell




    # No unvisited neighbors -> backtrack
    # if stack:
    #     previous_node = stack.pop()
    #     backtracked.add(bot_cell)
    #     return previous_node

    # Nothing left to explore
    return -1


    # fix this 

    # elif ():
    #     # this would be need when the first node has blocked cells in it's best path
    #     print('you are f ed')
    #     return 5

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
def find_best_path(b_cell, s_cell):
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
ans = find_best_path(bot_cell, switch_cell)
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

bot_cell_1 = bot_cell
bot1_paths = [bot_cell]
isbot3 = False

# for bot 1 

while(bot_cell_1 != switch_cell):

    bot_cell_1 = bot(bot_cell_1, switch_cell, isbot3, visited)
    if bot_cell_1 == switch_cell:
        bot1_paths.append(bot_cell_1)
        break 
    bot1_paths.append(bot_cell_1)

    if bot_cell_1 == -1 or bot_cell_1 == 2 or bot_cell_1 == 5:
        break

    if(bot_cell_1 == 0 or bot_cell_1 == 5):
        bot1_paths.append(-1)
        break


i = -1
bot2 = True
bot1 = False

while True:
    
    if (i > len(bot1_paths) - 1):
        # print('the first check')
        break 
    
    if bot_cell == -1:
        # print('something when wrong from bot')
        break
    if bot_cell == 5:
        # print('something weird happened')
        break
    if bot_cell == 2:
        # print('IT WORKED!!')
        break
    
    temp_fire_cells = []
    visited_neighbors = []

    # here also add check for bot having no path
   
    if bot2:
        bot_cell = bot(bot_cell, switch_cell, False, visited)
        if bot_cell == -1:
            # print("BOT LOST")
            break

        if bot_cell == 2:
            # print("IT WORKED!!")
            break

        if bot_cell == 5:
            # print("BOT BACKTRACKED")
            continue
        # print(f'bot moved to {bot_cell}')

    if bot1:
        if i >= len(bot1_paths):
            break
        i = i + 1 
        bot_cell = bot1_paths[i]
        # print(f'bot moved to {bot_cell}')

    if (bot_cell == switch_cell):
        # print('IT WORKED!!')
        break
    
    r7, c7 = bot_cell

    if (grid[r7][c7] == 's'):
        # print('It worked')
        break

    if grid[r7][c7] == 'f':
        # print("BOT CAUGHT FIRE!")
        break

    if grid[r7][c7] != '.':
        # print("The given cell is not open")
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

    # for now this is not random  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! [puting neighbor cell on fire]
    
    # print_colored_grid(grid, visited, backtracked, bot_cell)

    # time.sleep(SPEED)


# for row in grid:
#     print(row)

# print('')
# print('')

# print(f'this is the path for first bot {bot1_paths}')

  
