import sys
from myModules.inputParser import parseWithFunction  #type: ignore

class Direction:
  north = (-1,0)
  south = (1,0)
  west = (0,-1)
  east = (0,1)

# Build data structure (as a list)
def _stringParsing(str):
  str = list(str)
  return str

# Use BFS, matrix with (x,y) positions
# Priority Queue
# Matrix with visited points
def _searchBeam(beam_map, beam_visited, start):
  [(y,x), direction] = start
  beam_visited[y][x] = [1,[direction]]
  pq = [start]
  while pq:
    [point, direction] = pq.pop(0)
    directions = _checkGrid(point, direction, beam_map)
    for direction in directions:
      # get new points
      (y,x) = (point[0]+direction[0], point[1]+direction[1])
      if x >= 0 and y >= 0 and x < len(beam_map[0]) and y < len(beam_map):
        # check if visisted with current direction
        if not direction in beam_visited[y][x][1]:
          # if not, add to pq, add to visisted
          beam_visited[y][x][0] += 1
          beam_visited[y][x][1].append(direction)
          pq.append([(y,x), direction])

  return beam_visited

def _checkGrid(point, direction, beam_map):
  (y,x) = point
  match beam_map[y][x]:
    case '.':
      return [direction]
    case '/':
      match direction:
        case Direction.north: 
          return[Direction.east]
        case Direction.south:
          return[Direction.west]
        case Direction.east:
          return[Direction.north]
        case Direction.west:
          return[Direction.south]

    case '\\':
      match direction:
        case Direction.north: 
          return[Direction.west]
        case Direction.south:
          return[Direction.east]
        case Direction.east:
          return[Direction.south]
        case Direction.west:
          return[Direction.north]

    case '|':
      match direction:
        case Direction.north: 
          return [Direction.north]
        case Direction.south:
          return [Direction.south]
        case Direction.east:
          return [Direction.north,Direction.south]
        case Direction.west:
          return [Direction.north,Direction.south]

    case '-':
      match direction:
        case Direction.north: 
          return [Direction.west, Direction.east]
        case Direction.south:
          return [Direction.west, Direction.east]
        case Direction.east:
          return [Direction.east]
        case Direction.west:
          return [Direction.west]

    case _:
      print("error in matching")
      sys.exit(1)

# Part 1
def _listOps1(beam_map):
  # n x n matrix for visited points
  beam_visited = [[[0,[]] for _ in range(len(beam_map))] for _ in range(len(beam_map))]

  beam_visited = _searchBeam(beam_map, beam_visited, [(0,0), Direction.east])

  total = 0
  for y in range(len(beam_visited)):
    for x in range(len(beam_visited[0])):
      if beam_visited[y][x][0] > 0:
        total += 1

  return total

def countTotal(beam_visited):
  total = 0
  for y in range(len(beam_visited)):
    for x in range(len(beam_visited[0])):
      if beam_visited[y][x][0] > 0:
        total += 1
  return total

# Part 2
def _listOps2(beam_map):
  # n x n matrix for visited points
  max_total = 0
  for start_y in range(len(beam_map)):
    # start from left, going east 
    start_x = 0
    direction = Direction.east
    beam_visited = [[[0,[]] for _ in range(len(beam_map))] for _ in range(len(beam_map))]
    beam_visited = _searchBeam(beam_map, beam_visited, [(start_y,start_x), direction])
    total = countTotal(beam_visited)
    if total > max_total:
      max_total = total

    # start from right, going west
    start_x = len(beam_map)-1
    direction = Direction.west
    beam_visited = [[[0,[]] for _ in range(len(beam_map))] for _ in range(len(beam_map))]
    beam_visited = _searchBeam(beam_map, beam_visited, [(start_y,start_x), direction])
    total = countTotal(beam_visited)
    if total > max_total:
      max_total = total
    if total > max_total:
      max_total = total

  for start_x in range(len(beam_map[0])):
    # start from top, going south 
    start_y = 0
    direction = Direction.south
    beam_visited = [[[0,[]] for _ in range(len(beam_map))] for _ in range(len(beam_map))]
    beam_visited = _searchBeam(beam_map, beam_visited, [(start_y,start_x), direction])
    total = countTotal(beam_visited)
    if total > max_total:
      max_total = total

    # start from bottom, going north
    start_y = len(beam_map[0])-1
    direction = Direction.north
    beam_visited = [[[0,[]] for _ in range(len(beam_map))] for _ in range(len(beam_map))]
    beam_visited = _searchBeam(beam_map, beam_visited, [(start_y,start_x), direction])
    total = countTotal(beam_visited)
    if total > max_total:
      max_total = total

  return max_total


if __name__ == "__main__":
  func = _stringParsing
  parsed_input = parseWithFunction(func)
  # print(parsed_input)
  print("Part 1: ", _listOps1(parsed_input))
  print("Part 2: ", _listOps2(parsed_input))
