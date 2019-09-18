from random import randint, choice; from time import time

def generate(width, height, doTimer=False):
    if doTimer: startTime = time() # If time == True it'll track how long the generation takes
    # Creates a 2D list of 1's with the point (1,1) as a 0
    mapList     = [ [1 for y in range(height) ] for x in range(width) ]
    frontiers   = [((1,1), (1,1))]   # The starting frontiers bordering the point (1,1)
    while frontiers:            # Continue as long as there are more frontiers to go over
        new     = choice(frontiers) # Takes a random frontier bordering a floor tile
        frontiers.remove(new)   # Removes the random frontier
        x, y = new[0]; i, j = new[1] # Takes the 2 tiles that were picked from the frontiers
        if mapList[x][y] == 1: mapList[x][y] = 0; mapList[i][j] = 0 # If the tile is a wall, set the 2 tiles to be floor
        for a, b in [(-2, 0), (2, 0), (0, -2), (0, 2)]:    # Add these to the tiles to get their neighbours
            if x + a >= 0 and x + a < width and y + b >= 0 and y + b < height:  # Makes sure that the neighbours aren't out of the list
                # If the neighbour is a wall then set it and the connecting piece to be frontiers
                if mapList[x + a][y + b] != 0: frontiers.append(((x + a, y + b), (x + (a // 2), y + (b // 2))))
    if doTimer: print("Time Elapsed: {}".format(time() - startTime))   # Print the time from the start of the generation and the end
    return mapList

if __name__ == '__main__': print("\n".join(" ".join("#" if y == 1 else " " for y in x) for x in generate(39, 39, doTimer=True)))
