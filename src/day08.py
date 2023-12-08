import math
from myModules.inputParser import parseWithFunction  #type: ignore


# Build data structure (as a list)
def _stringParsing(str):
  instructions = str
  
  #Dummy for blank line
  parseWithFunction(lambda x : x)
  
  network = list(edge for edge in parseWithFunction(_build_network))
  merge_network = {}
  for n in network:
    merge_network.update(n)
  network = merge_network
  
  documents = []
  documents.append(instructions)
  documents.append(network)
  return documents

def _build_network(str):
  parts = str.split(" = (")
  x, yz = parts
  parts =  yz.split(",")
  y, z = parts
  z = z.replace(")", "")
  z = z.strip()
  return {x : (y,z)}

# Part 1
def _listOps1(alist):
  [documents] = alist
  [instructions, network] = documents
  turns = 0
  position = 'AAA'

  while position != 'ZZZ':
    if instructions[turns % len(instructions)] == 'L':
      #print("At {}, turn {}".format(position, "left"))
      position = network[position][0]
    else:
      #print("At {}, turn {}".format(position, "right"))
      position = network[position][1]
    turns += 1

  return turns


# Part 2
def _listOps2(alist):
  [documents] = alist
  [instructions, network] = documents
  positions = {}
  for p in network:
    if p[2] == 'A':
      positions.update({p : {}})

  for pos in positions:
    p = pos
    turns = 0
    while p[2] != 'Z':

      if instructions[turns % len(instructions)] == 'L':
          #print("At {}, turn {}".format(positions[i], "left"))
          p = network[p][0]
      else:
          #print("At {}, turn {}".format(positions[i], "right"))
          p = network[p][1]
      
      turns += 1

    positions[pos].update({p : turns})

  #apperently there is only one loop (fixed length) of each path
  #this means we can use lowest common multiple
  lcm = 1
  for p in positions:
    for turns in positions[p]:
      lcm = math.lcm(lcm, positions[p][turns])

  return lcm


if __name__ == "__main__":
  func = _stringParsing
  parsed_input = parseWithFunction(func)
  #print(parsed_input)
  print("Part 1: ", _listOps1(parsed_input))
  print("Part 2: ", _listOps2(parsed_input))
