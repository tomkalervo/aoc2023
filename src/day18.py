import re
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

def _get_dig_dict(instructions):
  max_x = 0
  min_x = 0
  max_y = 0
  min_y = 0
  u = (0,0)
  dig_dict = {}
  for (dy,dx), distance, _ in instructions:
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
  # handle negative positions necessary
    add_x = abs(min_x)
    add_y = abs(min_y)
    new_dig_dict = {}
    for (uy,ux) in dig_dict:
      vy, vx = dig_dict[(uy,ux)]
      new_dig_dict.update({(uy+add_y,ux+add_x) : (vy+add_y, vx+add_x)})
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
    # handle negative positions necessary
    add_x = abs(min_x)
    add_y = abs(min_y)
    new_dig_dict = {}
    for (uy,ux) in dig_dict:
      vy, vx = dig_dict[(uy,ux)]
      new_dig_dict.update({(uy+add_y,ux+add_x) : (vy+add_y, vx+add_x)})
    min_x += add_x
    max_x += add_x
    min_y += add_y
    max_y += add_y
    dig_dict = new_dig_dict
  return min_x, max_x, min_y, max_y, dig_dict

def _total_dugged(rows, max_y):
  total = 0
  edges = []
  for (uy,ux),(vy,vx) in rows:
    # print("total before {},{}: {}".format((uy,ux),(vy,vx),total))
    if(ux < vx): # increase
      if vx in edges:
        edges.remove(vx)
        vx -= 1
      else:
        edges.append(vx)
      if ux in edges:
        edges.remove(ux)
        ux += 1
      else:
        edges.append(ux)
      diggs = (vx-ux)+1
      total += diggs * ((max_y+1) - uy)      
    else: # decrease
      if vx in edges:
        edges.remove(vx)
      else:
        edges.append(vx)
        vx += 1
      if ux in edges:
        edges.remove(ux) 
      else:
        edges.append(ux)
        ux -= 1

      diggs = (ux-vx)+1
      total -= diggs * (max_y - uy)

  return total
# Part 1
def _listOps1(instructions):
  _,_,_,max_y,dig_dict = _get_dig_dict(instructions)

  # My logic counts after horisontal lines, increaseing or deacreasing the dig site
  # thus, I filter out vertical lines, which could have be done earlier
  dig_rows = []
  for u in dig_dict:
    (vy,_) = dig_dict[u]
    (uy,_) = u
    if uy == vy:
      dig_rows.append((u,dig_dict[u]))

  dig_rows.sort()

  return _total_dugged(dig_rows,max_y)

# Part 2
def _listOps2(instructions):
  _,_,_,max_y,dig_dict = _get_dig_dict_rgb(instructions)

  dig_rows = []
  for u in dig_dict:
    (vy,_) = dig_dict[u]
    (uy,_) = u
    if uy == vy:
      dig_rows.append((u,dig_dict[u]))

  dig_rows.sort()
  
  return _total_dugged(dig_rows,max_y)
if __name__ == "__main__":
  func = _stringParsing
  parsed_input = parseWithFunction(func)
  # print(parsed_input)

  print("Part 1: ", _listOps1(parsed_input))
  print("Part 2: ", _listOps2(parsed_input))
