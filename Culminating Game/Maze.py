from random import randint, choice; from time import time

def generate(width, height, doTimer=False, difficulty=True):
    if doTimer: startTime = time()              # If time == True it'll track how long the generation takes
    # Creates a 2D list of 1's with the point (1,1) as a 0
    mapList     = [[1 for y in range(height)] for x in range(width)]
    frontiers   = [((width - 2, width - 2), (height - 2, height - 2), -1)]
    while frontiers:                            # Keep iterating as long as there are more frontiers
        new = choice(frontiers)                 # Takes a random frontier bordering a floor tile
        frontiers.remove(new)                   # Removes the random frontier
        x, y = new[0]; i, j = new[1]            # Takes the 2 tiles that were picked from the frontiers
        if mapList[x][y] == 1:
            if difficulty:  mapList[x][y] = new[2] + 1
            else:           mapList[x][y] = 0
            mapList[i][j] = 0
        for a, b in [(-2, 0), (2, 0), (0, -2), (0, 2)]:     # Add these to the tiles to get their neighbours
            if x + a >= 0 and x + a < width and y + b >= 0 and y + b < height:  # Makes sure that the neighbours aren't out of the list
                # If the neighbour is a wall then set it and the connecting piece to be frontiers
                if mapList[x + a][y + b] == 1: frontiers.append(((x + a, y + b), (x + (a // 2), y + (b // 2)), mapList[x][y]))
    if doTimer: print("Time Elapsed: {}".format(round(time() - startTime, 20))) # Print the time from the start of the generation and the end
    return mapList

if __name__ == '__main__': print("\n".join(" ".join(" # " if y == 1 else "{:^3}".format(str(y)) for y in x) for x in generate(39, 39, doTimer=True, difficulty=False)))
