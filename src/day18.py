import re
import math
import sys
from myModules.inputParser import parseWithFunction  #type: ignore

# Build data structure (as a list)
def _stringParsing(str):
  # str : R 6 (#70c710)
  direction, distance, rgb_hex = filter(None, re.split("\s+|\(|#|\)", str))
  rgb = (int(rgb_hex[:-1], 16), int(rgb_hex[-1]))
  match direction:
    case 'R':
      direction = (0,1)
    case 'L':
      direction = (0,-1)
    case 'D':
      direction = (1,0)
    case 'U':
      direction = (-1,0)
  return (direction, int(distance), rgb)

def _mark_outside(dig_map,y,x):
  queue = [(y,x)]
  while queue:
    y,x = queue.pop()
    if y < 0 or y >= len(dig_map):
      continue
    if x < 0 or x >= len(dig_map[y]):
      continue
    if dig_map[y][x] != '.':
      continue
    dig_map[y][x] = 'O'
    for dy,dx in [(1,0),(-1,0),(0,1),(0,-1)]:
      queue.append((y+dy,x+dx))
    
  return dig_map

def _get_dig_dict(instructions):
  max_x = 0
  min_x = 0
  max_y = 0
  min_y = 0
  u = (0,0)
  dig_dict = {}
  for (dy,dx), distance, rgb in instructions:
    y,x = u
    
    v_y = (dy*distance) + y
    if v_y < min_y:
      min_y = v_y
    elif v_y > max_y:
      max_y = v_y
      
    v_x = (dx*distance) + x
    if v_x < min_x:
      min_x = v_x
    elif v_x > max_x:
      max_x = v_x
      
    v = (v_y,v_x)
    dig_dict.update({u : (v, rgb)})
    u = v

  if min_x < 0 or min_y < 0:
    print("handle negative positions necessary")
    add_x = abs(min_x)
    add_y = abs(min_y)
    new_dig_dict = {}
    for (uy,ux) in dig_dict:
      # print(f"{(vy,vx)} : {dig_dict[(vy,vx)]}")
      ((vy, vx), rgb) = dig_dict[(uy,ux)]
      new_dig_dict.update({(uy+add_y,ux+add_x) : ((vy+add_y, vx+add_x), rgb)})
    min_x += add_x
    max_x += add_x
    min_y += add_y
    max_y += add_y
    dig_dict = new_dig_dict
  return min_x, max_x, min_y, max_y, dig_dict

def _get_dig_dict_rgb(instructions):
  max_x = 0
  min_x = 0
  max_y = 0
  min_y = 0
  u = (0,0)
  dig_dict = {}
  for _, _, (distance, direction) in instructions:
    match direction:
      # 0 means R, 1 means D, 2 means L, and 3 means U.
      case 0:
        dy,dx = 0,1
      case 1:
        dy,dx = 1,0
      case 2:
        dy,dx = 0,-1
      case 3:
        dy,dx = -1,0
        
    y,x = u
    v_y = (dy*distance) + y
    if v_y < min_y:
      min_y = v_y
    elif v_y > max_y:
      max_y = v_y
      
    v_x = (dx*distance) + x
    if v_x < min_x:
      min_x = v_x
    elif v_x > max_x:
      max_x = v_x
      
    v = (v_y,v_x)
    dig_dict.update({u : v})
    u = v

  if min_x < 0 or min_y < 0:
    print("handle negative positions necessary")
    add_x = abs(min_x)
    add_y = abs(min_y)
    new_dig_dict = {}
    for (uy,ux) in dig_dict:
      # print(f"{(vy,vx)} : {dig_dict[(vy,vx)]}")
      ((vy, vx), rgb) = dig_dict[(uy,ux)]
      new_dig_dict.update({(uy+add_y,ux+add_x) : ((vy+add_y, vx+add_x), rgb)})
    min_x += add_x
    max_x += add_x
    min_y += add_y
    max_y += add_y
    dig_dict = new_dig_dict
  return min_x, max_x, min_y, max_y, dig_dict

# Part 1
def _listOps1(instructions):
  min_x,max_x,min_y,max_y,dig_dict = _get_dig_dict(instructions)
  dig_map = [['.' for _ in range(min_x,max_x+1)] for _ in range(min_y,max_y+1)]
  for (u_y, u_x) in dig_dict:
    ((v_y,v_x),_) = dig_dict[(u_y,u_x)]
    # print(f"digging from {u_y},{u_x} to {v_y},{v_x}")

    for i in range(u_y, v_y, -1 if v_y < u_y else 1):
      dig_map[i][u_x] = '#'
      
    for i in range(u_x, v_x, -1 if v_x < u_x else 1):
      dig_map[u_y][i] = '#'  
      
  print('-'*40)    
  for level in dig_map:
    print(*level)
    
  for y in range(0, len(dig_map)):
    for x in [0, len(dig_map[y])-1]:
      if dig_map[y][x] != '.':
        continue
      dig_map = _mark_outside(dig_map,y,x)

  # print('-'*40)    
  # y = 0
  # for level in dig_map:
  #   print("{}: {}".format(y, level))
  #   y += 1
    
  total = sum(sum(1 if yx != 'O' else 0 for yx in row) for row in dig_map)
  return total
#TODO:
# ioc. line:  (76, 66)
# edges:  [(20, 56), (66, 76)]
# result from intersection:  -45
def _intersection_of_complement(line, edges):
  print("ioc. line: ", line)
  print("edges: ", edges)
  a_left = min(line)
  a_right = max(line)
  value = 0
  for (b_left,b_right) in edges:
    # complement include all of line
    if a_left > b_right or a_right < b_left:
      return (b_left-a_left)+1
    # complement include non of line
    elif a_left >= b_left and a_right <= b_right:
      return 0
    # complement include leftmos part of line (up to b_left)
    elif a_left < b_left:
      return b_left-a_left
    # complement include rightmost part of line (down to b_right)
    else:
      return a_right-b_right
  # if empty list of edges  
  return a_right-a_left+1
def _union(edges, new_edges):
  def decrease_set(edges, a_left, a_right):
    edges.append((a_left,a_right))
    edges.sort()
    intersection = []
    a_left,a_right = edges[0]
    for i in range(1,len(edges)):
      b_left,b_right = edges[i]
      # print("a: {},{} - b: {},{}".format(a_left,a_right,b_left,b_right))
      if a_right < b_left:
        intersection.append((a_left,a_right))
        a_left,a_right = b_left,b_right
      elif a_right == b_right and a_left == b_left:
        i += 1
        if i >= len(edges):
          return intersection
        else:
          a_left,a_right = edges[i]
      else: # a_right >= b_left
        if a_left == b_left and a_right < b_right:
          a_left,a_right = a_right,b_right
        elif a_left < b_left and a_right == b_right:
          a_left,a_right = a_left,b_left
        else: # a_left < b_left < b_right < a_right
          intersection.append((a_left,b_left))  
          a_left,a_right = b_right,a_right
      print(intersection)
    intersection.append((a_left,a_right))
    
    return intersection

  def increase_set(edges, a_left, a_right):
    edges.append((a_left,a_right))
    edges.sort()
    union = []
    a_left,a_right = edges[0]
    for i in range(1,len(edges)):
      b_left,b_right = edges[i]
      if a_right < b_left:
        union.append((a_left,a_right))
        a_left,a_right = b_left,b_right
      else:
        a_left,a_right = a_left,b_right
    union.append((a_left,a_right))
    
    return union
  for (a_left, a_right) in new_edges:
    if a_left > a_right:
      edges = decrease_set(edges, a_right, a_left)
    else:
      edges = increase_set(edges, a_left, a_right)
  return edges

# Part 2
def _listOps2(instructions):
  # min_x,max_x,min_y,max_y,dig_dict = _get_dig_dict_rgb(instructions)
  min_x,max_x,min_y,max_y,dig_dict = _get_dig_dict(instructions)

  total = 0
  edges = []
  for y in range(0, max_y+1):
    used = []
    new_edges = []
    diggs = 0
    for u in dig_dict:
      (vy,vx),_ = dig_dict[u]
      (uy,ux) = u
      if vx == ux:
        used.append(u)
      elif(min(uy,vy) <= y <= max(uy,vy)):
        new_edges.append((ux,vx))
        
      elif(uy < y and vy < y):
        used.append(u) # will be removed after
        
    while used:
      del dig_dict[used.pop()]
    for pair in new_edges:
      intersec = _intersection_of_complement(pair, edges)
      print("result from intersection: ", intersec)
      diggs += intersec
    for (left,right) in edges:
      diggs += (right-left) + 1
    
    total += diggs
    if new_edges:
      print("before union. edges: ", edges, " <-> new edges: ", new_edges)
      edges = _union(edges, new_edges)    
      print("result from union: ", edges)
    print("y: {} - DIGGS {} - TOTAL {}".format(y, diggs, total))
  return total


if __name__ == "__main__":
  func = _stringParsing
  parsed_input = parseWithFunction(func)
  # print(parsed_input)

  print("Part 1: ", _listOps1(parsed_input))
  print("Part 2: ", _listOps2(parsed_input))
