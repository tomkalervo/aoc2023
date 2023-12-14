import sys
from myModules.inputParser import parseWithFunction  #type: ignore
from myModules.listOps import transpose, rotate_anticlockwise, rotate_clockwise #type: ignore

# Build data structure (as a list)
def _stringParsing(str):
  return list(str)
def _tilt(rocks):
  tilted_rocks = []
  for line in rocks:
    row = list(line)
    i = 0
    j = 0
    while i < len(row):
      match row[i]:
        case 'O':
          tmp = row[i]
          row[i] = row[j]
          row[j] = tmp
          i = j
          while i < len(row) and row[i] in ['#', 'O']:
            i += 1
            j = i # j points to next available
        case '#':
          while i < len(row) and row[i] in ['#', 'O']:
            i += 1
            j = i # j points to next available
        case _:
          i += 1
    tilted_rocks.append(row)
  return tilted_rocks

def _sumTiltedRocks(rocks):
  total = 0
  for row in rocks:
    length = len(row)
    for i in range(length):
      if row[i] == 'O':
        total += (length - i)
  return total

# Part 1
def _listOps1(alist):
  rocks = transpose(alist)
  rocks = _tilt(rocks)

  total = _sumTiltedRocks(rocks)

  return total

# Part 2
def _listOps2(rocks):

  def cycle(rocks):
    # Transpose
    rocks = transpose(rocks)

    # North tilt
    rocks = _tilt(rocks)

    # West rotate & tilt
    rocks = rotate_anticlockwise(rocks)
    rocks = _tilt(rocks)

    # South rotate & tilt
    rocks = rotate_anticlockwise(rocks)
    rocks = _tilt(rocks)
    
    # East rotate & tilt
    rocks = rotate_anticlockwise(rocks)
    rocks = _tilt(rocks)

    # North rotate
    rocks = rotate_anticlockwise(rocks)
    # Transpose back
    load = _sumTiltedRocks(rocks)
    rocks = transpose(rocks)

    return [load, rocks]

  # Mapping the entire rock-schema might not 
  # be the most effecient way to find a loop, 
  # but optimisation not needed this time
  rock_map = {}
  [load, rocks] = cycle(rocks)
  iterations = 1000000000-1
  rock_map.update({tuple([load, tuple(rocks)]) : iterations})

  # Find a loop
  while(iterations > 0):
    iterations -= 1
    [load, rocks] = cycle(rocks)
    rock_cycle = tuple([load, tuple(rocks)])
    if rock_cycle in rock_map:
      break
    else:
      rock_map.update({rock_cycle : iterations})

  # utilise the properties from a loop
  loop_length = rock_map[rock_cycle] - iterations
  iterations = iterations % loop_length

  # iterate through the last cycles
  while(iterations > 0):
    iterations -= 1
    [load, rocks] = cycle(rocks)

  return load



if __name__ == "__main__":
  func = _stringParsing
  parsed_input = parseWithFunction(func)
  #print(parsed_input)
  print("Part 1: ", _listOps1(parsed_input))
  print("Part 2: ", _listOps2(parsed_input))
