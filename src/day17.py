import sys
import math
import time
import heapq
from myModules.inputParser import parseWithFunction  #type: ignore

# Build data structure (as a list)
def _stringParsing(str):
  return [int(x) for x in list(str)]

#TODO: need better pq
def _shortestPath(city_blocks, start, stop):
  heat_map = [[0 for _ in range(len(city_blocks[0]))] for _ in range(len(city_blocks))]
  pos_map = [[[] for _ in range(len(city_blocks[0]))] for _ in range(len(city_blocks))]
  for row in heat_map:
    print(*row)
  block = [start, (1,0), 0]
  pq = [block]
  def _in_range(p,l):
    return 0 <= p[0] < l and 0 <= p[1] < l 

  def _check_block_not_visited(p0, p):
    acc_heat = heat_map[p0[0]][p0[1]]
    heat = city_blocks[p[0]][p[1]]
    if heat_map[p[0]][p[1]] == 0:
      heat_map[p[0]][p[1]] = acc_heat + heat
      pos_map[p[0]][p[1]] = p0

    elif heat_map[p[0]][p[1]] > acc_heat + heat:
      heat_map[p[0]][p[1]] = acc_heat + heat
      pos_map[p[0]][p[1]] = p0
    else:
      return False
    return True

  while pq:
    [position, direction, steps] = pq.pop(0)

    blocks = []
    #left
    left_direction = (direction[1], direction[0])
    left_position = (position[0]+left_direction[0], position[1]+left_direction[1])
    if _in_range(left_position, len(city_blocks)):
      # operations
      if _check_block_not_visited(position,left_position):
        blocks.append([left_position, left_direction, 1])

    #right
    right_direction = (0-direction[1], 0-direction[0])
    right_position = (position[0]+right_direction[0], position[1]+right_direction[1])
    if _in_range(right_position, len(city_blocks)):
      # operations
      if _check_block_not_visited(position,right_position):
        blocks.append([right_position, right_direction, 1])

    if not steps == 3:
      #straight
      forward_position = (position[0]+direction[0], position[1]+direction[1])
      if _in_range(forward_position, len(city_blocks)):
        # operations
        if _check_block_not_visited(position,forward_position):
          blocks.append([forward_position, direction, steps+1])
    # print(blocks)
    pq.extend(blocks)
    # print(pq)

  #print outs
  # print_city = list(city_blocks)
  # for row in print_city:
  #   row = list(row)
  # s = stop
  # while s != (0,0):
  #   print(s)
  #   print_city[s[0]][s[1]] = '*'
  #   s = pos_map[s[0]][s[1]]
  # print_city[s[0]][s[1]] = '*'

  return heat_map

# Part 1
def _listOps1(city_blocks):
  start = (0,0)
  stop_y = len(city_blocks[0])-1
  stop_x = len(city_blocks)-1
  stop = (stop_y, stop_x)

  city_map = _shortestPath(city_blocks, start, stop)

  for row in city_map:
    print(*row)
  for row in city_blocks:
    print(*row)

  return 1


# Part 2
def _listOps2(alist):
  total = sum(1 for _ in alist)

  return total


if __name__ == "__main__":
  func = _stringParsing
  parsed_input = parseWithFunction(func)
  for row in parsed_input:
    print(*row)
  print("Part 1: ", _listOps1(parsed_input))
  print("Part 2: ", _listOps2(parsed_input))

import heapq

# # Try heapq!!
# my_objects = [
#     [(1, 2), (0, 1), 3],
#     [(2, 3), (1, 0), 2],
#     [(0, 1), (1, 0), 5],
#     # ... add more objects as needed
# ]

# # Custom key function to use the last item (distance) for comparison
# key_function = lambda obj: obj[-1]

# # Convert the list to a heap using the custom key
# heapq.heapify(my_objects)

# # Push a new object onto the heap using the key function
# new_object = [(3, 4), (0, 1), 4]
# heapq.heappush(my_objects, new_object, key=key_function)

# # Popping the smallest object based on distance
# smallest_object = heapq.heappop(my_objects, key=key_function)

# print("Original heap of objects:", my_objects)
# print("Smallest object popped:", smallest_object)

 