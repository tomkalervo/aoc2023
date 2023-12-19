import sys
import math
import time
import heapq
from myModules.inputParser import parseWithFunction  #type: ignore


# Build data structure (as a list)
def _stringParsing(str):
  return [int(x) for x in list(str)]

# used for part 1
def _shortestPath(city_blocks):
  visited = set()
  block = [0,0,(0,0),(0,1)]
  pq = []
  heapq.heappush(pq, block)

  def _in_range(y,x, lgh):
    return 0 <= y < lgh and 0 <= x < lgh

  # Dijkstra algorithm with constraints
  while pq:
    heat,steps,(y,x),(dy,dx) = heapq.heappop(pq)
    # print("({},{}) = {}".format(y,x,heat))
    
    # We reached our goal
    if (y,x) == (len(city_blocks)-1,len(city_blocks)-1):
      return heat
    
    # Because of constraint max 3 steps in a row, 
    # we need to store direction and steps
    if (y,x,dy,dx,steps) in visited:
      continue
    visited.add((y,x,dy,dx,steps))

    if steps < 3:
      (new_y,new_x) = (y+dy,x+dx)
      if _in_range(new_y,new_x,len(city_blocks)):
        new_heat = heat + city_blocks[new_y][new_x]
        block = [new_heat,steps+1,(new_y,new_x),(dy,dx)]
        heapq.heappush(pq, block)

    for (new_dy,new_dx) in [(-dx,dy),(dx,-dy)]:
      (new_y,new_x) = (y+new_dy,x+new_dx)
      if _in_range(new_y,new_x,len(city_blocks)):
        new_heat = heat + city_blocks[new_y][new_x]
        block = [new_heat,1,(new_y,new_x),(new_dy,new_dx)]
        heapq.heappush(pq, block)

  return -1

# used for part 2
def _shortestPathUltra(city_blocks):
  visited = set()
  block = [0,0,(0,0),(0,1)]
  pq = []
  heapq.heappush(pq, block)

  def _in_range(y,x,l_y,l_x):
    return 0 <= y < l_y and 0 <= x < l_x

  # Dijkstra algorithm with constraints
  while pq:
    heat,steps,(y,x),(dy,dx) = heapq.heappop(pq)
    
    # We reached our goal, and are allowed to stop (minimum steps of 4)
    if (y,x) == (len(city_blocks)-1,len(city_blocks[0])-1) and steps > 3:
      return heat
    
    # Because of constraint max 3 steps in a row, 
    # we need to store direction and steps
    if (y,x,dy,dx,steps) in visited:
      continue
    visited.add((y,x,dy,dx,steps))
    
    if steps < 10:
      (new_y,new_x) = (y+dy,x+dx)
      if _in_range(new_y,new_x,len(city_blocks),len(city_blocks[0])):
        new_heat = heat + city_blocks[new_y][new_x]
        block = [new_heat,steps+1,(new_y,new_x),(dy,dx)]
        heapq.heappush(pq, block)

    if steps > 3 or steps == 0:
      for (new_dy,new_dx) in [(-dx,dy),(dx,-dy)]:
        (new_y,new_x) = (y+new_dy,x+new_dx)
        if _in_range(new_y,new_x,len(city_blocks),len(city_blocks[0])):
          new_heat = heat + city_blocks[new_y][new_x]
          block = [new_heat,1,(new_y,new_x),(new_dy,new_dx)]
          heapq.heappush(pq, block)

  return -1


# Part 1
def _listOps1(city_blocks):
  heat = _shortestPath(city_blocks)

  return heat


# Part 2
def _listOps2(city_blocks):
  heat = _shortestPathUltra(city_blocks)

  return heat


if __name__ == "__main__":
  func = _stringParsing
  parsed_input = parseWithFunction(func)
  # for row in parsed_input:
  #   print(*row)
  print("Part 1: ", _listOps1(parsed_input))
  print("Part 2: ", _listOps2(parsed_input))

