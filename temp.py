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
visited = set() 

GRID_SIZE = 10

grid = [
    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
    ['*', 'b', '.', '.', '*', '.', '.', '.', 'f', '*'],
    ['*', '.', '*', '*', '*', '.', '*', '*', '.', '*'],
    ['*', '.', '.', '.', '.', '.', '*', '.', '.', '*'],
    ['*', '.', '*', '*', '*', '.', '*', '.', '*', '*'],
    ['*', '.', '.', 'f', '*', '.', '.', '.', '.', '*'],
    ['*', '*', '.', '*', '*', '*', '*', '*', '.', '*'],
    ['*', '.', '.', '.', '.', '.', 'f', '.', '.', '*'],
    ['*', '.', '*', '*', '*', '*', '*', '.', 's', '*'],
    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*']
]

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
    if (r2 < r1) and (0 <= c1 <= GRID_SIZE - 1) and (0 <= c2 <= GRID_SIZE - 1) and (0 < r1 <= GRID_SIZE - 1)  and (0 <= r2 <= GRID_SIZE - 1):
        return (r1 - 1, c1) # up
    if (r2 > r1 and (0 <= c1 <= GRID_SIZE - 1) and (0 <= c2 <= GRID_SIZE - 1) and (0 <= r1 < GRID_SIZE - 1)  and (0 <= r2 <= GRID_SIZE - 1)):
        return (r1 + 1, c1) # down
    if (c2 < c1 and (0 <= c1 < GRID_SIZE - 1) and (0 <= c2 <= GRID_SIZE - 1) and (0 <= r1 <= GRID_SIZE - 1)  and (0 <= r2 <= GRID_SIZE - 1)):
        return(r1, c1 - 1) # left
    if (c2 > c1 and (0 < c1 <= GRID_SIZE - 1) and (0 <= c2 <= GRID_SIZE - 1) and (0 <= r1 <= GRID_SIZE - 1)  and (0 <= r2 <= GRID_SIZE - 1)):
        return (r1, c1 + 1) # right
    return 'Raj'

def bot2(bot_cell, switch_cell):
    
    print('this is bot 2')
    print(f'bot was here {bot_cell}')
    print(f'switch was here {switch_cell}')

    for row in grid:
        print(row)

    while (bot_cell != switch_cell):
        visited.add(bot_cell)
        directions = get_direction(bot_cell, switch_cell)
        if (directions == 'success'):
            print('succ')
            break   

        if (directions == 'Raj'):
            print('raj')
            break  

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
            print('this is the end, hold your ...')
            break
    # if the neighbor is open we can pick it
        if (grid[r3][c3] == '.' and picked_direction not in visited):
            stack.append(bot_cell)
            bot_cell = picked_direction
            print(f'using this path {picked_direction}')

    # if the first neighbor we picked is not open we can go to other neighbor we had 2 possible paths
        elif (grid[r4][c4] == '.' and picked_direction not in visited):
            stack.append(bot_cell)
            bot_cell = picked_direction_2
            print(f'using this path {picked_direction_2}')

    # if we can't go to any given paths either one or both you will have to pick other possible path 
        elif (stack):
            print('this ran')
            previous_node = stack.pop()
            bot_cell = previous_node
        else:
            print('you are f ed')
            break

for r in range(GRID_SIZE):
    for c in range(GRID_SIZE):
        if grid[r][c] == 'b':
            bot_cell = ((r,c))
        if grid[r][c] == 's':
            switch_cell = ((r,c))    


bot2(bot_cell, switch_cell)