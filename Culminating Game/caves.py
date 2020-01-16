import sys
import random
import time
from collections import deque

# Creates an empty grid for automata
def makeGrid(width, height):
    newgrid = [[0 for x in range(height)] for y in range(width)]
    for i in range(len(newgrid)):
        for j in range(len(newgrid[i])):
            if i==0 or j==0 or i==len(newgrid)-1 or j==len(newgrid[0])-1:
                newgrid[i][j] = 1
    return newgrid

# Randomizes the grid with 1s and 0s
def populateGrid(width, height):
    grid = makeGrid(width, height)
    for i, val in enumerate(grid):
        for j, cell in enumerate(val):
            if(random.randint(0, 100)<=30):
                grid[i][j] = 1
    return grid

# Executes one iteration of cellular automata
def automataIteration(grid, makePillars):
    new_grid = [row[:] for row in grid]
    for i in range(1, len(grid)-1):
        for j in range(1, len(grid[0])-1):
            count = 0
            for k in range(-1,2):
                for l in range(-1,2):
                    if grid[i+k][j+l]==1:
                        count+=1
            if count>=6 or (count==0 and makePillars):
                new_grid[i][j]=1
            else:
                new_grid[i][j]=0
    return new_grid

# Floodfills caves to be sure that there's only one cave in a room
def floodfill(grid):
    remakes = 0
    percentage = 0
    while remakes < 3 and percentage < 35:
        copy_grid = [row[:] for row in grid]
        open_count = 0
        remakes += 1
        unvisited = deque([])
        new_grid = [[1 for x in range(len(grid[0]))] for y in range(len(grid))]
        #find a random empty space, hope it's the biggest cave
        randx = random.randint(0,len(grid)-1)
        randy = random.randint(0,len(grid[0])-1)
        while(grid[randx][randy] == 1):
            randx = random.randint(0,len(grid)-1)
            randy = random.randint(0,len(grid[0])-1)
        unvisited.append([randx, randy])
        while len(unvisited)>0:
            current = unvisited.popleft()
            new_grid[current[0]][current[1]] = 0
            for k in range(-1,2):
                for l in range(-1,2):
                    if not abs(k) == abs(l):
                        if current[0]+k >= 0 and current[0]+k<len(grid) and current[1]+l >= 0 and current[1]+l < len(grid[0]): #if we're not out of bounds
                            if copy_grid[current[0]+k][current[1]+l]==0: #if it's an empty space
                                copy_grid[current[0]+k][current[1]+l]=23 #mark visited
                                open_count += 1
                                unvisited.append([current[0]+k, current[1]+l])
        percentage = open_count*100/(len(grid)*len(grid[0]))        
    return new_grid, percentage

# Opens passages for each direction for the room that was generated 
def transform(grid, directions): # Takes the basic map, makes walls only surround the floor, and adds entrances in specified directions
    centreX = len(grid) // 2
    centreY = len(grid[0]) // 2

    if "UP" in directions:
        i = 0
        running = True
        f = False
        while True:
            if not running: f = True
            for x in range(centreX - 1, centreX + 2):
                if grid[x][i] == 1: grid[x][i] = 20
                else: running = False; break
            if f: break
            i += 1
##        for x in range(centreX - 1, centreX + 2):
##            grid[x][i] = 20

    if "DOWN" in directions:
        i = len(grid[0]) - 1
        running = True
        f = False
        while True:
            if not running: f = True
            for x in range(centreX - 1, centreX + 2):
                if grid[x][i] == 1: grid[x][i] = 21
                else: running = False; break
            if f: break
            i -= 1
####        for x in range(centreX - 1, centreX + 2):
####            grid[x][i] = 21
            
    if "LEFT" in directions:
        for x in range(centreY - 1, centreY + 2):
            i = 0
            while True:
                if grid[i][x] == 1:
                    grid[i][x] = 22
                else: break
                i += 1
                
    if "RIGHT" in directions:
        for x in range(centreY - 1, centreY + 2):
            i = len(grid) - 1
            while True:
                if grid[i][x] == 1:
                    grid[i][x] = 23
                else: break
                i-= 1
                
    tileMap         = [x[:] for x in grid]
    collisionMap    = [x[:] for x in grid]

    fluidMap        = [[0 for x in y] for y in grid]

    for i in range(random.randint(0,4)):
        if random.randint(0, 100) > 60: fluidMap[random.randint(2, len(grid)-4)][random.randint(2, len(grid[0])-4)] = 7
        else:                           fluidMap[random.randint(2, len(grid)-4)][random.randint(2, len(grid[0])-4)] = 8

    
    for n in range(8):
        for i, val in enumerate(fluidMap):
            for j, cell in enumerate(val):
                if cell in [7, 8]:
                    count = 0
                    for k, l in [(-1, 0),(1, 0),(0, 1),(0, -1)]:
                        if i + k > len(fluidMap)-1 or j + l > len(fluidMap[0])-1 or i + k < 0 or j + l < 0: count += 1
                        else:
                            if fluidMap[i+k][j+l] == 1: count += 1
                            if random.randint(0, 4) == 2:
                                if random.randint(0, 100) > 60: fluidMap[i+k][j+l] = 7
                                else:                           fluidMap[i+k][j+l] = 8
    
    for i, val in enumerate(fluidMap):
            for j, cell in enumerate(val):
                if cell == 0:
                    count = 0
                    for k, l in [(-1, 0),(1, 0),(0, 1),(0, -1)]:
                        if i + k > len(fluidMap)-1 or j + l > len(fluidMap[0])-1 or i + k < 0 or j + l < 0: count += 1
                        else:
                            if fluidMap[i + k][j + l] in [7, 8]: fluidMap[i + k][j + l] = 1
    #printGrid(fluidMap, chr(9608) + chr(9608), "  ")
    for i, val in enumerate(grid):
        for j, cell in enumerate(val):
            if cell in [20, 21, 22, 23]: tileMap[i][j] = cell; collisionMap[i][j] = 0
            elif cell == 1:
                count = 0
                for k in range(-1, 2):
                    for l in range(-1, 2):
                        if i + k > len(grid)-1 or j + l > len(grid[0])-1 or i + k < 0 or j + l < 0: count += 1
                        else:
                            if grid[i+k][j+l] == 1:
                                count += 1
                if count == 9 or count == 8:
                    tileMap[i][j] = 13
                    collisionMap[i][j] = 1
                else: tileMap[i][j] = 9
            else: tileMap[i][j] = 0; collisionMap[i][j] = 0
            if tileMap[i][j] == 0: tileMap[i][j] = fluidMap[i][j]
    return tileMap, collisionMap

# Overall function to to all of the above functinos in one call
def generate(width, height, directions):
    iterations = 5
    pillarIterations = 2

    grid = populateGrid(width, height)

    for i in range(2):
        grid = automataIteration(grid, 1)
    for i in range(5):
        grid = automataIteration(grid, 0)

    grid, percentage = floodfill(grid)
    if percentage < 50:
        return generate(width, height, directions)
    else:
        return transform(grid, directions)

if __name__ == "__main__":
    printGrid(generate(45,30, ["UP", "DOWN", "LEFT", "RIGHT"])[0], chr(9608) + chr(9608), "  ")
