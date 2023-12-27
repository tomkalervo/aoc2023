import sys
import time

from myModules.inputParser import parseWithFunction  #type: ignore

# Build data structure (as a list)
def _stringParsing(str):
  return tuple(str)

def _elf_move(grid, state):
    next_state = {}
    for pos in state:
        y,x = pos
        for dy,dx in [(0,1),(0,-1),(1,0),(-1,0)]:
            if (len(grid) > y+dy >= 0) and (len(grid[y]) > x+dx >= 0):
                if(grid[y+dy][x+dx] != '#'):
                    next_state.update({(y+dy,x+dx):1})
    return next_state

# Part 1
def _listOps1(grid):
    start = None
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == 'S':
                start = (y,x)
                break
    
    state = {start : 1}
    # state[start] = 1

    steps = 6
    while steps > 0:
        steps -= 1
        start = time.time()
        state = _elf_move(grid, state)
        end = time.time()
        print(f"steps left: {steps}, time taken: {end-start}")

    total = sum(state[pos] for pos in state)
    return total       

# Part 2
def _elf_move_unhindered(grid, start, steps):
    store = {start:steps}
    queue = [(start,steps)]
    total = 1
    directions = [(1,0),(0,1),(-1,0),(0,-1)]
    while queue:
        (y,x), steps = queue.pop()
        print(f"at {y},{x} with {steps} steps left. Total so far is {total}")
        for dy,dx in directions:
            pos_y = y+dy
            while pos_y < 0:
                pos_y += len(grid)
            while pos_y >= len(grid):
                pos_y -= len(grid)
        
            pos_x = x+dx
            while pos_x < 0:
                pos_x += len(grid[0])
            while pos_x >= len(grid[0]):
                pos_x -= len(grid[0])
            if grid[pos_y][pos_x] != '#':
                for ddy,ddx in directions:
                    print(f"Check position1 {y+dy+ddy},{x+dx+ddx}")
                    pos_y = y+dy+ddy
                    while pos_y < 0:
                        pos_y += len(grid)
                    while pos_y >= len(grid):
                        pos_y -= len(grid)
                
                    pos_x = x+dx+ddx
                    while pos_x < 0:
                        pos_x += len(grid[0])
                    while pos_x >= len(grid[0]):
                        pos_x -= len(grid[0])

                    if grid[pos_y][pos_x] == '#':
                        print("rock")
                        continue
                    if (y+dy+ddy,x+dx+ddx) in store and store[(y+dy+ddy,x+dx+ddx)] >= steps:
                        print("visited")
                        continue
                    print("new: ", grid[pos_y][pos_x])
                    store.update({(y+dy+ddy,x+dx+ddx):steps})
                    total += 1
                    if steps - 2 > 0:
                        queue.append([(y+dy+ddy,x+dx+ddx),steps-2])
        
    return total


def _listOps2(grid):
    start = None
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == 'S':
                start = (y,x)
                break
    
    steps = 50
    total = _elf_move_unhindered(grid, start, steps)
            

    return total   


if __name__ == "__main__":
  func = _stringParsing
  parsed_input = tuple(parseWithFunction(func))
  print(parsed_input)
  print("Part 1: ", _listOps1(parsed_input))
  print("Part 2: ", _listOps2(parsed_input))
