import random
from numpy.random import random_integers as rand
import sys
import math

def generate_maze(w, h, maze_type=-1):
    if maze_type == -1:
        types = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3]
        maze_type = random.choice(types)
    if maze_type == 1:
        return plane(w, h, 0.05 + 0.3*random.random())
    if maze_type == 2:
        return walls(w, h, 0.1+0.7*random.random()*random.random())
    if maze_type == 3:
        return corridors(w, h)

#Please note: all coordinates are stored as [x, y]
#one can obtain the data at the corresponding coordinate in a maze using maze[y][x]
def plane(w, h, global_density = 0.4, local_density = 2):
    level = [['.' for x in range(w)] for y in range(h)]
    for i in range(int(global_density*w*h)):
        while True:
            x = random.randint(1,w)-1
            y = random.randint(1,h)-1
            if level[y][x] != '.':
                continue
            c = 0
            for dx in range(-1,2):
                for dy in range(-1,2):
                    if level[(y+dy+h)%h][(x+dx+w)%w] != '.':
                        c+=1
            if c > local_density:
                continue
            level[y][x] = '#'
            break
    return level


def walls(w, h, sqDensity = 0.3):
    level = labyrinth(w, h, 0.1)
    filled = 0
    for nTries in range(100):
        if filled > 0.9*sqDensity:
            break
        wi = random.randint(5,max(w-5, round(w/2)-5))
        hi = random.randint(5,max(h-5, round(h/2)-5))
        x = random.randint(1,w-wi-1)
        y = random.randint(1,h-hi-1)
       
        filled += wi*hi/(w*h)
        if filled > 1.1*sqDensity:#too full, try again
            filled -= wi*hi/(w*h)
            continue

        fill_square(level, x, y, wi, hi, '.')
        add_square(level, x+1, y+1, wi-1, hi-1, '#')
    return level

def fill_square(maze, x, y, w, h, c='.'):
    for xi in range(x, x+w+1):
        for yi in range(y, y+h+1):
            maze[yi][xi]=c

def add_square(maze, x, y, w, h, c='#'):
    xll= x
    xl = x+round(w/2) - 1
    xr = x+round(w/2) + 1
    xrr= x + w

    yll= y
    yl = y+round(h/2) - 1
    yr = y+round(h/2) + 1
    yrr= y + h

    add_line(maze, xll, yll, xl, yll, c)
    add_line(maze, xr, yll, xrr, yll, c)

    add_line(maze, xll, yrr, xl, yrr, c)
    add_line(maze, xr, yrr, xrr, yrr, c)

    add_line(maze, xll, yll, xll, yl, c)
    add_line(maze, xll, yr, xll, yrr, c)

    add_line(maze, xrr, yll, xrr, yl, c)
    add_line(maze, xrr, yr, xrr, yrr, c)

def add_line(maze, x0, y0, x1, y1, c='#'):
    dist = round(math.sqrt((x0-x1)**2+(y0-y1)**2))
    for ti in range(dist+1):
        t = ti/dist
        xt = round(t*x0 + (1-t)*x1)
        yt = round(t*y0 + (1-t)*y1)
        maze[yt][xt] = c

def corridors(w, h):
    maze = [[".#"[(x%2)*(y%2)] for x in range(w)] for y in range(h)]
    return maze

def labyrinth(width, height, clear=0.2, complexity=.75, density=.75):
    # Source: https://en.wikipedia.org/wiki/Maze_generation_algorithm
    # Only odd shapes
    shape = ((height // 2) * 2 + 1, (width // 2) * 2 + 1)
    h = shape[0]
    w = shape[1]
    # Adjust complexity and density relative to maze size
    complexity = int(complexity * (5 * (shape[0] + shape[1])))
    density    = int(density * (shape[0] // 2 * shape[1] // 2))
    # Build actual maze
    Z = [['.' for x in range(w)] for y in range(h)]
    # Fill borders
    for x in range(w):
        Z[0][x] = '#'
        Z[h-1][x] = '#'
    for y in range(h):
        Z[y][0] = '#'
        Z[y][w-1] = '#'
    # Make aisles
    for i in range(density):
        x, y = rand(0, shape[1] // 2) * 2, rand(0, shape[0] // 2) * 2
        Z[y][x] = '#'
        for j in range(complexity):
            neighbours = []
            if x > 1:             neighbours.append((y, x - 2))
            if x < shape[1] - 2:  neighbours.append((y, x + 2))
            if y > 1:             neighbours.append((y - 2, x))
            if y < shape[0] - 2:  neighbours.append((y + 2, x))
            if len(neighbours):
                y_,x_ = neighbours[rand(0, len(neighbours) - 1)]
                if Z[y_][x_] == '.':
                    Z[y_][x_] = '#'
                    Z[y_ + (y - y_) // 2][x_ + (x - x_) // 2] = '#'
                    x, y = x_, y_

    for i in range(round(clear*w*h)):
        x = random.randint(1,w-1)-1
        y = random.randint(1,h-1)-1
        Z[y][x] = '.'
        if x == 0:
            Z[y][w-1] = '.'
        if y == 0:
            Z[h-1][x] = '.'

    if w != width:
        for y in range(h):
            Z[y].pop()
    if h != height:
        Z.pop()
    
    return Z

def get_empty_cell(maze, w, h, c='None'):
    for i in range(100):
        x = random.randint(1,w)-1
        y = random.randint(1,h)-1
        if maze[y][x] == '.':
            if c != 'None':
                maze[y][x]=c
            return [x,y]
    return 0

def show_maze(maze, fout=sys.stdout):
    for line in maze:
        fout.write("".join(line)+"\n")
