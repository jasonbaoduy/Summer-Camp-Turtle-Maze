import turtle
import random

# 1. Fix the random seed so the maze is the same each run
def setup_random():
    random.seed(0)

# 2. Generate a maze using a simple depth-first search
def generate_maze(rows, cols):
    walls = {}  # store walls for each cell
    for col in range(cols):
        for row in range(rows):
            walls[(col, row)] = {'North': True, 'South': True, 'East': True, 'West': True}

    visited = [(0, 0)]
    stack = [(0, 0)]

    while stack:
        col, row = stack[-1]
        neighbors = []
        # check each direction for unvisited neighbors
        if row + 1 < rows and (col, row + 1) not in visited:
            neighbors.append(('North', (col, row + 1)))
        if row - 1 >= 0 and (col, row - 1) not in visited:
            neighbors.append(('South', (col, row - 1)))
        if col + 1 < cols and (col + 1, row) not in visited:
            neighbors.append(('East', (col + 1, row)))
        if col - 1 >= 0 and (col - 1, row) not in visited:
            neighbors.append(('West', (col - 1, row)))

        if neighbors:
            direction, (ncol, nrow) = random.choice(neighbors)
            # remove walls between current and next
            walls[(col, row)][direction] = False
            opposite = {'North': 'South', 'South': 'North', 'East': 'West', 'West': 'East'}
            walls[(ncol, nrow)][opposite[direction]] = False
            visited.append((ncol, nrow))
            stack.append((ncol, nrow))
        else:
            stack.pop()  # backtrack

    return walls

# 3. Draw the maze walls
def draw_maze(walls, rows, cols, cell_size):
    pen = turtle.Turtle()
    pen.hideturtle()
    pen.speed('fastest')

    half_w = cols * cell_size / 2
    half_h = rows * cell_size / 2

    for (col, row), cell_walls in walls.items():
        x0 = -half_w + col * cell_size
        y0 = -half_h + row * cell_size
        # draw each wall that remains
        if cell_walls['North']:
            pen.penup(); pen.goto(x0, y0 + cell_size); pen.setheading(0)
            pen.pendown(); pen.forward(cell_size)
        if cell_walls['South']:
            pen.penup(); pen.goto(x0, y0); pen.setheading(0)
            pen.pendown(); pen.forward(cell_size)
        if cell_walls['East']:
            pen.penup(); pen.goto(x0 + cell_size, y0); pen.setheading(90)
            pen.pendown(); pen.forward(cell_size)
        if cell_walls['West']:
            pen.penup(); pen.goto(x0, y0); pen.setheading(90)
            pen.pendown(); pen.forward(cell_size)

# 4. Main program
if __name__ == "__main__":
    screen = turtle.Screen()
    screen.setup(600, 600)
    screen.title("Maze with Start and End")

    setup_random()

    # Maze parameters (~50 cells)
    ROWS = 7    # number of rows
    COLS = 7    # number of columns (7x7 = 49 cells)
    CELL_SIZE = 40  # size of each cell in pixels

    maze = generate_maze(ROWS, COLS)
    draw_maze(maze, ROWS, COLS, CELL_SIZE)

    # Mark the start cell (0,0) in green
    marker = turtle.Turtle()
    marker.hideturtle(); marker.speed('fastest')
    half_w = COLS * CELL_SIZE / 2
    half_h = ROWS * CELL_SIZE / 2
    marker.penup()
    marker.color('green')
    marker.goto(-half_w, -half_h)
    marker.pendown(); marker.begin_fill()
    for _ in range(4):
        marker.forward(CELL_SIZE); marker.left(90)
    marker.end_fill()

    # Mark the end cell (COLS-1, ROWS-1) in red
    marker.penup()
    marker.color('red')
    marker.goto(-half_w + (COLS-1)*CELL_SIZE, -half_h + (ROWS-1)*CELL_SIZE)
    marker.pendown(); marker.begin_fill()
    for _ in range(4):
        marker.forward(CELL_SIZE); marker.left(90)
    marker.end_fill()

    # Students: write your own maze traversal here!










    screen.exitonclick()
