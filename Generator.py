# Random Maze Generator using Depth-first Search
# http://en.wikipedia.org/wiki/Maze_generation_algorithm

import random
from PIL import Image
import Solver

imgx = 500; imgy = 500
image = Image.new("RGB", (imgx, imgy))
pixels = image.load()
mx = 50; my = 50 # width and height of the maze
maze = [[0 for x in range(mx)] for y in range(my)]
dx = [0, 1, 0, -1]; dy = [-1, 0, 1, 0] # 4 directions to move in the maze
color = [(0, 0, 0), (255, 255, 255), (0, 255, 0), (0, 0, 255)] # RGB colors of the maze
# start the maze from a random cell
cx = random.randint(0, mx - 1); cy = random.randint(0, my - 1)
maze[cy][cx] = 1; stack = [(cx, cy, 0)] # stack element: (x, y, direction)

while len(stack) > 0:
    (cx, cy, cd) = stack[-1]
    # to prevent zigzags:
    # if changed direction in the last move then cannot change again
    if len(stack) > 2:
        if cd != stack[-2][2]: dirRange = [cd]
        else: dirRange = range(4)
    else: dirRange = range(4)

    # find a new cell to add
    nlst = [] # list of available neighbors
    for i in dirRange:
        nx = cx + dx[i]; ny = cy + dy[i]
        if nx >= 0 and nx < mx and ny >= 0 and ny < my:
            if maze[ny][nx] == 0:
                ctr = 0 # of occupied neighbors must be 1
                for j in range(4):
                    ex = nx + dx[j]; ey = ny + dy[j]
                    if ex >= 0 and ex < mx and ey >= 0 and ey < my:
                        if maze[ey][ex] == 1: ctr += 1
                if ctr == 1: nlst.append(i)

    # if 1 or more neighbors available then randomly select one and move
    if len(nlst) > 0:
        ir = nlst[random.randint(0, len(nlst) - 1)]
        cx += dx[ir]; cy += dy[ir]; maze[cy][cx] = 1
        stack.append((cx, cy, ir))
    else: stack.pop()

# paint the maze
for ky in range(imgy):
    for kx in range(imgx):
        px=int((mx+2) * kx / imgx)-1
        py=int((my+2) * ky / imgy)-1
        if (py<0) or (px<0) or (py>=my) or (px>=mx):
            if ((py<0) and (px<1)) or ((px<0) and (py<1)):
                pixels[kx, ky] = color[1]
            elif ((py>=my) and (px>=mx-1)) or ((px>=mx) and (py>=my-1)):
                pixels[kx, ky] = color[1]
            else:
                pixels[kx, ky] = color[0]
        else:
            pixels[kx, ky] = color[maze[py][px]]
image.save("output\\Maze_" + str(mx) + "x" + str(my) + ".png", "PNG")

solver=Solver.AStar()
solver.init_grid(mx, my, maze)
solver.process()

# paint the mazetrip
for ky in range(imgy):
    for kx in range(imgx):
        px=int((mx+2) * kx / imgx)-1
        py=int((my+2) * ky / imgy)-1
        if (py<0) or (px<0) or (py>=my) or (px>=mx):
            if ((py<0) and (px<1)) or ((px<0) and (py<1)):
                pixels[kx, ky] = color[1]
            elif ((py>=my) and (px>=mx-1)) or ((px>=mx) and (py>=my-1)):
                pixels[kx, ky] = color[1]
            else:
                pixels[kx, ky] = color[0]
        else:
            pixels[kx, ky] = color[solver.grid[py][px]]
image.save("output\\Maze_" + str(mx) + "x" + str(my) + "_solved.png", "PNG")