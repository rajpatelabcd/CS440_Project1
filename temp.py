import random
import time
from collections import deque
import matplotlib.pyplot as plt
import copy
import time
import heapq


start_time = time.perf_counter()

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

stack = deque()
visited = set() 

GRID_SIZE = 30

grid = [['*' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

bot_cell = ()
switch_cell = ()

def reset_grid():
    global grid
    grid = [['*' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

#  find valid dead ends and add to list 
def update_dead_ends(dead_ends):
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

def setup_grid():

    # the first cell to open
    open_cell = (random.randint(1, GRID_SIZE - 2), random.randint(1, GRID_SIZE - 2))
    row, column = open_cell
    grid[row][column] = '.' 

    # list of all cells which are valid and we can open (with exectly one neighbor)

    valid_cells = []
    valid_cells_set = set()
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
            if grid[r][c] == '*' and n not in valid_cells_set: 
                valid_cells.append(n)
                valid_cells_set.add(n)

    dead_ends = []
    update_dead_ends(dead_ends)
    dead_ends = set(dead_ends)

    target = len(dead_ends) // 2

    while len(dead_ends) > target:
        cell = random.choice(tuple(dead_ends))

        closed_neighbors = [
            n for n in get_neighbors(cell).values()
            if grid[n[0]][n[1]] == '*'
        ]

        opened = random.choice(closed_neighbors)
        r, c = opened
        grid[r][c] = '.'

        # Only these cells can have changed dead-end status.
        affected = [opened, *get_neighbors(opened).values()]

        for position in affected:
            r, c = position
            dead_ends.discard(position)

            if grid[r][c] != '.':
                continue

            open_count = sum(
                grid[nr][nc] == '.'
                for nr, nc in get_neighbors(position).values()
            )

            if open_count == 1:
                dead_ends.add(position)

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
setup_grid()

fringe = deque()

def find_best_path(b_cell, s_cell, isbot3, ):
    global visited
    visited = set()
    fringe = deque()
    r1, c1 = b_cell
    r2, c2 = s_cell
    fringe.append((b_cell, [b_cell]))
    visited.add(b_cell) 

    while fringe:
        f, current_path = fringe.popleft()

        if (f == s_cell):
            return current_path
        # print(f'we lookin for neighbor of {f}')
        all_neighbors = get_neighbors(f)

        for neighbor in all_neighbors.values():
            r3, c3 = neighbor

            if(isbot3 == True):
                if(grid[r3][c3] == '.' or grid[r3][c3] == 's'):
                    if neighbor not in visited:
                        neighbor_of_neighbor = get_neighbors(neighbor)
                        is_cell_safe = True
                        for n in neighbor_of_neighbor.values():
                            r4, c4 = n 
                            if(grid[r4][c4] == 'f'):
                                is_cell_safe = False
                                break

                        if is_cell_safe:
                            new_path = current_path + [neighbor]
                            fringe.append((neighbor, new_path))
                            visited.add(neighbor)

            elif(grid[r3][c3] == '.' or grid[r3][c3] == 's'):
                if neighbor not in visited:
                    new_path = current_path + [neighbor]
                    fringe.append((neighbor, new_path))
                    visited.add(neighbor)
            
    return None 

def run_bot(bot_number, q, bot_cell, switch_cell):

    isbot3 = False
    
    if(bot_number == 3):
        isbot3 = True

    # for bot 1 
    init_path = find_best_path(bot_cell, switch_cell, False)
    if init_path is None:
        return 0

    current_path = init_path

    i = 0
    # for f in range(GRID_SIZE):
    #     print(grid[f])

    while True:

        if (i > len(init_path) - 1):
            # print('the first check')
            return 0 
        
        if bot_cell == -1:
            # print('something when wrong from bot')
            return 0
        
        # here also add check for bot having no path

        if bot_number == 3:
            current_path = find_best_path(bot_cell, switch_cell, True)
            if current_path is None:
                current_path = find_best_path(bot_cell, switch_cell, False)
                
            if current_path is None:
                # print("BOT LOST")
                return 0
            bot_cell = current_path[1]

            if bot_cell == -1:
                # print("BOT LOST")
                return 0
        elif bot_number == 2:
            current_path = find_best_path(bot_cell, switch_cell, False)
            if current_path is None:
                return 0
            bot_cell = current_path[1]

        elif bot_number == 1:
            i += 1

            if i >= len(init_path):
                return 0

            bot_cell = init_path[i]

            if bot_cell == switch_cell:
                return 1


        if (bot_cell == switch_cell):
            # print('IT WORKED!!')
            return 1
        
        r7, c7 = bot_cell

        if (grid[r7][c7] == 's'):
            # print('It worked')
            return 1


        if grid[r7][c7] == 'f':
            # print("BOT CAUGHT FIRE!")
            return 0


        if grid[r7][c7] != '.':
            # print("The given cell is not open")
            return 0


        temp_fire_cells = []
        visited_neighbors = set()

        # look for only neighbor of fire cells to see if they catch fire 
        for raj in fire_cells:
            fire_cell_neighbors = get_neighbors(raj)
            # look through every neigbor
            for n in fire_cell_neighbors.values():
                if n not in visited_neighbors:
                    visited_neighbors.add(n)
                    r4, c4 = n
                    if grid[r4][c4] != '.':
                        continue
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
                    visited_neighbors.add(n)

        for n in temp_fire_cells:
            r5, c5 = n 
            if grid[r5][c5] not in ('f', 'b', 's'):
                grid[r5][c5] = 'f'
                if bot_cell in fire_cells:
                    return 0
                fire_cells.append(n)
                
        if grid[r7][c7] == 'f':
            # print("BOT CAUGHT FIRE!")
            return 0
        
        # print_colored_grid(grid, visited, backtracked, bot_cell)

        # time.sleep(SPEED)

def calculate_fire_risk(cell, q):

    neighbors = get_neighbors(cell)

    fire_neighbors = 0

    for neighbor in neighbors.values():
        r, c = neighbor

        if grid[r][c] == 'f':
            fire_neighbors += 1

    probability = 1 - (1 - q) ** fire_neighbors

    return probability

def calculate_fire_distances():
    distances = {}

    queue = deque()

    for fire in fire_cells:
        distances[fire] = 0
        queue.append(fire)

    while queue:
        cell = queue.popleft()

        for neighbor in get_neighbors(cell).values():
            if neighbor not in distances:
                distances[neighbor] = distances[cell] + 1
                queue.append(neighbor)

    return distances

def find_best_path_bot4(bot_cell, switch_cell, q):

    priority_queue = []

    fire_distances = calculate_fire_distances()

    heapq.heappush(
        priority_queue,
        (0, bot_cell, [bot_cell])
    )

    visited_cost = {}

    while priority_queue:

        total_cost, current, path = heapq.heappop(priority_queue)

        if current == switch_cell:
            return path

        if current in visited_cost and total_cost >= visited_cost[current]:
            continue

        visited_cost[current] = total_cost

        for neighbor in get_neighbors(current).values():

            r, c = neighbor

            if grid[r][c] != '.' and neighbor != switch_cell:
                continue

            cell_cost = calculate_cell_cost(
                neighbor,
                q,
                fire_distances
            )

            new_cost = total_cost + cell_cost

            new_path = path + [neighbor]

            heapq.heappush(
                priority_queue,
                (new_cost, neighbor, new_path)
            )

    return None

def calculate_cell_cost(cell, q, fire_distances):

    # Normal movement cost
    distance_cost = 1

    # Current fire probability
    fire_risk = calculate_fire_risk(cell, q)

    # Distance from nearest fire
    d = fire_distances.get(cell, GRID_SIZE * 2)

    # Stronger penalty for being close to fire
    fire_distance_penalty = 5 / (d + 1)

    return distance_cost + fire_risk + fire_distance_penalty

def run_bot4(q, bot_cell, switch_cell):

    while True:

        # Find safest/shortest path using Dijkstra
        current_path = find_best_path_bot4(
            bot_cell,
            switch_cell,
            q
        )

        # No possible path
        if current_path is None:
            return 0

        # If we're already at the switch
        if bot_cell == switch_cell:
            return 1

        # Move one step along the path
        if len(current_path) < 2:
            return 0

        bot_cell = current_path[1]

        # Check if we reached switch
        if bot_cell == switch_cell:
            return 1

        r, c = bot_cell

        # Bot stepped into fire
        if grid[r][c] == 'f':
            return 0

        # Bot must be on an open cell
        if grid[r][c] not in ('.', 's', 'b'):
            return 0

        # ----------------------------------------
        # FIRE SPREADS
        # ----------------------------------------

        temp_fire_cells = []
        visited_neighbors = set()

        for fire_cell in fire_cells:

            fire_cell_neighbors = get_neighbors(fire_cell)

            for n in fire_cell_neighbors.values():

                if n in visited_neighbors:
                    continue

                r4, c4 = n

                # Don't spread fire into bot or switch
                if grid[r4][c4] in ('b', 's'):
                    visited_neighbors.add(n)
                    continue

                neighbors_of_cell_to_fire = get_neighbors(n)

                k = 0

                for l in neighbors_of_cell_to_fire.values():

                    r5, c5 = l

                    if grid[r5][c5] == 'f':
                        k += 1

                probability = 1 - (1 - q) ** k

                flammability = random.random()

                if probability > flammability:

                    if grid[r4][c4] == '.':
                        temp_fire_cells.append(n)

                visited_neighbors.add(n)

        # Actually spread the fire
        for n in temp_fire_cells:

            r5, c5 = n

            if grid[r5][c5] not in ('f', 'b', 's'):

                grid[r5][c5] = 'f'

                fire_cells.append(n)

        # Bot caught fire
        if bot_cell in fire_cells:
            return 0

# placing bot and switch
def setup_simulation():
    global bot_cell, switch_cell, fire_cells

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

    r1 = random.randint(0, len(open_cells) - 1)
    bot_cell =  open_cells[r1]
    bot_row, bot_column = bot_cell
    grid[bot_row][bot_column] = 'b'

    r2 = random.choice(list(range(0, r1)) + list(range(r1 + 1, len(open_cells))))
    switch_cell = open_cells[r2]
    switch_row, switch_column = switch_cell
    grid[switch_row][switch_column] = 's'

    for n in range(GRID_SIZE):
        for l in range(GRID_SIZE):
            if grid[n][l] == 'b':
                bot_cell = (n, l)
            if grid[n][l] == 's':
                switch_cell = (n, l)

    r3 = random.randint(0, len(open_cells) - 1)
    init_fire_cell = open_cells[r3]
    init_fire_cell_row, init_fire_cell_column = init_fire_cell

    while (grid[init_fire_cell_row][init_fire_cell_column] != '.'):
        r3 = random.randint(0, len(open_cells) - 1)
        init_fire_cell = open_cells[r3]
        init_fire_cell_row, init_fire_cell_column = init_fire_cell


    grid[init_fire_cell_row][init_fire_cell_column] = 'f'
    fire_cells = []
    fire_cells.append((init_fire_cell_row, init_fire_cell_column))



bot1 = False
bot2 = False
bot3 = False

bot1_results = {}
bot2_results = {}
bot3_results = {}
bot4_results = {}


q_values = [x / 10 for x in range(11)]


for q in q_values:

    success_count1 = 0
    success_count2 = 0
    success_count3 = 0
    success_count4 = 0

    for r in range(100):
        reset_grid()
        setup_grid()
        setup_simulation()

        original_grid = [row[:] for row in grid]
        original_fire = fire_cells.copy()
        
        grid = [row[:] for row in original_grid]
        fire_cells = original_fire.copy()
        res1 = run_bot(1, q, bot_cell, switch_cell)

        grid = [row[:] for row in original_grid]
        fire_cells = original_fire.copy()
        res2 = run_bot(2, q, bot_cell, switch_cell)

        grid = [row[:] for row in original_grid]
        fire_cells = original_fire.copy()
        res3 = run_bot(3, q, bot_cell, switch_cell)

        grid = [row[:] for row in original_grid]
        fire_cells = original_fire.copy()
        res4 = run_bot4(q, bot_cell, switch_cell)
        
        success_count1 += res1
        success_count2 += res2
        success_count3 += res3
        success_count4 += res4
    
    bot1_results[q] = success_count1   
    bot2_results[q] = success_count2
    bot3_results[q] = success_count3
    bot4_results[q] = success_count4

print(f'the result for bot 1')
print(bot1_results)
print(f'the result for bot 2')
print(bot2_results)
print(f'the result for bot 3')
print(bot3_results)
print(f'the result for bot 4')
print(bot4_results)

plt.plot(bot1_results.keys(), bot1_results.values(), marker='o', label='Bot 1')
plt.plot(bot2_results.keys(), bot2_results.values(), marker='o', label='Bot 2')
plt.plot(bot3_results.keys(), bot3_results.values(), marker='o', label='Bot 3')
plt.plot(bot4_results.keys(), bot4_results.values(), marker='o', label='Bot 4')

end_time = time.perf_counter()

# Calculate elapsed time in seconds
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.6f} seconds")

plt.xlabel("Flammability (q)")
plt.ylabel("Success Rate")
plt.title("Bot Success Rate vs Flammability")

plt.legend()
plt.grid()

plt.show()
plt.pause(3)
plt.close()

