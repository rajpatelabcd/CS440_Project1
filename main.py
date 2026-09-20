import random



GRID_SIZE = 10;

grid = [['*' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]


def get_neighbors((x, y)):
    return {
        "left": (x, y - 1),
        "right": (x, y + 1),
        "top": (x - 1, y),
        "bottom": (x + 1, y)
    }

open_cell = (random.randint(1, GRID_SIZE - 1), random.randint(1, GRID_SIZE - 1))
row, column = open_cell
grid[row][column] = '$' 

 

print(open_cell)

for i in range(GRID_SIZE):
    print(grid[i])
