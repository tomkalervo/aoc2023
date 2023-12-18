import sys
import math
import time
import heapq
from myModules.inputParser import parseWithFunction  #type: ignore


# Build data structure (as a list)
def _stringParsing(str):
  return [int(x) for x in list(str)]


def _shortestPath(city_blocks, _):
  heat_map = [[-1 for _ in range(len(city_blocks[0]))]
              for _ in range(len(city_blocks))]
  pos_map = [[(-1, -1) for _ in range(len(city_blocks[0]))]
             for _ in range(len(city_blocks))]

  heat_map[0][0] = 0
  pos_map[0][0] = (0, 0)
  pos_map[1][0] = (0, 0)
  pos_map[0][1] = (0, 0)
  block_straight = [city_blocks[0][1], [(0, 1), (0, 1), 1]]
  block_down = [city_blocks[1][0], [(1, 0), (1, 0), 1]]
  pq = []
  heapq.heappush(pq, block_straight)
  heapq.heappush(pq, block_down)

  # Movement directions
  directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

  def _in_range(psn, lgh):
    return 0 <= psn[0] < lgh and 0 <= psn[1] < lgh

  def _getHeat(psn, city_blocks):
    return city_blocks[psn[0]][psn[1]]

  while pq:
    [heat, info] = heapq.heappop(pq)
    position, direction, steps = info
    print("Checking ({},{}) with current heat {}".format(
        position[0], position[1], heat))
    for row in heat_map:
      print(*row)

    if (heat_map[position[0]][position[1]] != -1):
      continue
    
    heat_map[position[0]][position[1]] = heat

    if steps < 3:
      new_position = (position[0] + direction[0], position[1] + direction[1])
      if _in_range(new_position, len(city_blocks)):
        pos_map[new_position[0]][new_position[1]] = position
        new_heat = heat + _getHeat(new_position, city_blocks)
        block = [new_heat, [new_position, direction, steps + 1]]
        heapq.heappush(pq, block)

    for (dx, dy) in directions:
      if (dx, dy) != direction and (dx, dy) != (-direction[0], -direction[1]):
        print("dx dy", dx, dy, " direction ", direction)
        new_position = (position[0] + dx, position[1] + dy)
        if _in_range(new_position, len(city_blocks)):
          pos_map[new_position[0]][new_position[1]] = position
          new_direction = (dx, dy)
          new_heat = heat + _getHeat(new_position, city_blocks)
          block = [new_heat, [new_position, new_direction, 1]]
          heapq.heappush(pq, block)

  #print outs
  print("---" * 10, " search complete")
  # for row in pos_map:
  #   print(*row)
  # print_city = list(city_blocks)
  # s = (12, 12)
  # while s != (0, 0):
  #   print(s)
  #   print_city[s[0]][s[1]] = '*'
  #   s = pos_map[s[0]][s[1]]
  # print_city[s[0]][s[1]] = '*'

  return heat_map


# Part 1
def _listOps1(city_blocks):
  start = (0, 0)
  # stop_y = len(city_blocks[0])-1
  # stop_x = len(city_blocks)-1
  # stop = (stop_y, stop_x)

  city_map = _shortestPath(city_blocks, start)

  print(">" * 10, "Heat Map", "<" * 10)
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
