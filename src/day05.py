from myModules.inputParser import parseWithFunction  #type: ignore
from myModules.listOps import reduceList  #type: ignore

# Build data structure (as a list)
def _stringParsingSeeds(str):
  seeds = [int(x) for x in str.split(":")[1].split()]
  #print(seeds, " len ", len(seeds))
  return seeds
  
def _stringParsingMaps(str):
  # str = str.split(":")
  # map = []

  # line = input()
  # line = [int(x) for x in line.split()]
  # map.append(line)

  return parseWithFunction(lambda s : [int(x) for x in s.split()])
  
  #print(map, " len ", len(map))
  # return map

# Part 1
def _listOps1(seeds, maps):
  seeds = seeds[0]
  total = min(_mapSeeds1(maps, x) for x in seeds)
  return total
  
def _mapSeeds1(maps, seed):
  for map in maps:
    for x in map:
      if seed in range(x[1], x[1] + x[2]):
        seed = x[0] + (seed - x[1])
        break

  return seed
  
# Part 2
def _listOps2(seeds, maps):
  iterSeed = iter(seeds[0])
  seedTupleList = []
  for s in iterSeed:
    seedTupleList.append((s, next(iterSeed)))

  seeds = seedTupleList
  for map in maps:
    seeds = _mapSeeds2(map, seeds)

  #print(seeds)
  total = -1
  for s in seeds:
    if total == -1:
      total = s[0]
    elif total > s[0]:
      total = s[0]
    else:
      pass
  return total

def _mapSeeds2(map, seeds):
  nextSeeds = []
  seedOutOfTarget = []

  for x in map:
    if not seeds:
      break
    # print("Map: ", x)
    for s in seeds:
      if s[0] - (x[1] + x[2]) > 0 or ((s[0]+s[1]) - x[1] < 0):
        # starts after or ends before
        # print("s2")
        seedOutOfTarget.append((s[0],s[1]))
      elif s[0] - x[1] >= 0 and (s[0]+s[1]) - (x[1]+x[2]) <= 0:
        #print("s3")
        #starts inside, ends inside
        start = s[0]-x[1]
        nextSeeds.append((x[0]+start, s[1]))
        #print("({},{}) becomes ({},{})" .format(s[0],s[1],x[0]+start,s[1]))

      elif s[0] - x[1] >= 0 and (s[0]+s[1]) - (x[1]+x[2]) > 0:
        # print("s4")
        #starts inside, ends after
        # start = 15 - 10 = 5
        start = s[0]-x[1] 
        nextSeeds.append((x[0]+start, x[2]-start))
        seedOutOfTarget.append((x[1]+x[2]-1, s[1]-(x[2]-start)))
        # print("({},{}) becomes ({},{}) and ({},{})" .format(s[0],s[1],x[0]+start, x[2]-start,x[1]+x[2]-1,s[1]-(x[2]-start)))

      else:
        # print("**** s5 *****")
        #starts before, ends inside
        #stop (10-8-1) = 1
        stop = x[1]-s[0]
        seedOutOfTarget.append((s[0],stop))
        nextSeeds.append((x[0],s[1]-stop))
        # print("({},{}) becomes ({},{}) and ({},{})" .format(s[0],s[1],s[0],stop,x[0],s[1]-stop))

    if seedOutOfTarget:
      seeds = _sortSeeds(seedOutOfTarget)
      seedOutOfTarget = []
    else:
      seeds = []

  if seeds:
    nextSeeds.extend(seeds)
    seeds = _sortSeeds(nextSeeds)
  else:
    seeds = _sortSeeds(nextSeeds)
    
  return seeds
  
def _sortSeeds(seeds):
  if not seeds:
    return seeds
  seeds.sort(key=lambda x: x[0])
  #print("before reduce: ", seeds)
  seeds = reduceList(seeds, _unionRange)
  #print("after reduce: ", seeds)
  
  #x = []
  #for y in seeds:
  #  x += list(y)
  #seeds = x

  return seeds

def _unionRange(s1,s2):
  #print("union s1 ", s1, " with s2 ", s2)
  # s1, s2 already sorted: s1[0] < s2[0]
  if s1[0]+s1[1] < s2[0]:
    #print("u1")
    return [s1,s2]
  elif s1[0]+s1[1] > s2[0]+s2[1]:
    return [s1]
  else:
    #s1[1] = (s2[0] - s1[0]) + s2[1]
    return [(s1[0], (s2[0] - s1[0]) + s2[1])]

def solve_part_2(initial_seeds, maps):
  iterSeed = iter(initial_seeds[0])
  seed_tuples = []
  for s in iterSeed:
    seed_tuples.append((s, next(iterSeed)))
  seed_tuples = _sortSeeds(seed_tuples)
  print("start st: ", seed_tuples)  
  for stage_map in maps:
    updated_seeds = []
    for seed in seed_tuples:
        updated_seeds.extend(update_seed_tuple(seed, stage_map))

    #seed_tuples = remove_seeds_outside_range(updated_seeds)
    seed_tuples = _sortSeeds(updated_seeds)
    print("st: ", seed_tuples)  

  # Find the minimum location among the remaining seed tuples
  min_location = min(seed[0] for seed in seed_tuples)
  return min_location

def update_seed_tuple(seed, stage_map):
  updated_seeds = []
  # Extract values from seed
  seed_start = seed[0]
  seed_length = seed[1]
  seed_end = seed_start + seed_length
  #print("Seed:")
  #print(seed_start, seed_length, seed_end)
  for x in stage_map:
    # Extract relevant values from the map
    map_destination_start, map_source_start, map_length = x
    map_source_end = map_source_start + map_length
    map_destination_end = map_destination_start + map_length
    # print("Map:")
    # print(map_destination_start, map_source_start, map_length)
    #check if seed is outside the target
    if(seed_start >= map_source_end or seed_end <= map_source_start):
      continue
    else:
      #check if seed starts inside the target
      if(seed_start >= map_source_start):
        #check if seed ends inside the target
        if(seed_length < map_source_end):
          #seed starts and ends inside the target
          #print("seed starts and ends inside the target")
          new_start = (seed_start - map_source_start)
          #print("new: ({},{})".format(map_destination_start + new_start, seed_length))
          updated_seeds.append((map_destination_start + new_start, seed_length))
        else:
          #seed starts inside and ends outside the target
          #print("seed starts inside and ends outside the target")
          new_start = (seed_start - map_source_start)
          new_length = (map_length - new_start)
          #print("new 1: ({},{})".format(map_destination_start + new_start, new_length))
          #print("new 2: ({},{})".format(map_destination_end, seed_length - new_length))
          updated_seeds.append((map_destination_start + new_start, new_length))
          updated_seeds.append((map_destination_end, seed_length - new_length))
          if((seed_length - new_length) < 0):
            print("ERROR: negative length")
            print("a1")
      else:
        #seed starts outside (before) the target range
        #check if seed ends inside the target
        if(seed_end <= map_source_end):
          #seed starts before and ends inside the target
          #print("seed ends inside the target")
          new_start = map_destination_start
          new_length = seed_end - map_source_start
          #print("new 1: ({},{})".format(new_start, new_length))
          #print("new 2: ({},{})".format(seed_start, seed_length - new_length))
          updated_seeds.append((new_start, new_length))
          updated_seeds.append((seed_start, seed_length - new_length))
          if((seed_length - new_length) < 0):
            print("ERROR: negative length")
            print("a2")
          if(new_length < 0):
            print("ERROR: negative length")
            print("a3")
        else:
          #seed starts before and ends outside (after) the target range
          #print("seed ends after target range")
          new_start = map_destination_start
          new_length = map_length
          new_length_before = map_source_start-seed_start
          new_length_after = seed_end-map_source_end
          
          if not (seed_length == (new_length+new_length_before+new_length_after)):
            print("ERROR: ", seed_length, " != ", (new_length+new_length_before+new_length_after))
          #print("new 1: ({},{})".format(new_start, new_length))
          #print("new 2: ({},{})".format(seed_start, new_length_before))
          #print("new 3: ({},{})".format(map_source_end, new_length_after))
          updated_seeds.append((new_start, new_length))
          updated_seeds.append((seed_start, new_length_before))
          updated_seeds.append((map_source_end, new_length_after))
          if(new_length_before < 0):
            print("ERROR: negative length")
            print("a4")
          if(new_length_after < 0):
            print("ERROR: negative length")
            print("a5")
            print("seed: ", seed)
            print("map: ", x)
      if updated_seeds:
        break
  if not updated_seeds:
    updated_seeds.append(seed)
  
  return updated_seeds


if __name__ == "__main__":
  func = _stringParsingSeeds
  seeds = parseWithFunction(func)
  func = _stringParsingMaps
  parsed_input = parseWithFunction(func)

  print("Part 1: ", _listOps1(seeds, parsed_input))
  print("Part 2 v1: ", _listOps2(seeds, parsed_input))
  
  
  result = solve_part_2(seeds, parsed_input)
  print("Part 2 v2: ", result)
