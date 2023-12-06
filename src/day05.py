from myModules.inputParser import parseWithFunction  #type: ignore
from myModules.listOps import reduceList  #type: ignore

# Build data structure (as a list)
def _stringParsingSeeds(str):
  seeds = [int(x) for x in str.split(":")[1].split()]
  return seeds
  
def _stringParsingMaps(str):
  return parseWithFunction(lambda s : [int(x) for x in s.split()])

# Part 1
def _listOps1(seeds, maps):
  seeds = seeds[0]
  total = min(_mapSeeds1(maps, x) for x in seeds)
  return total
  
def _mapSeeds1(maps, seed):
  print(seed)
  for map in maps:
    for x in map:
      if seed in range(x[1], x[1] + x[2]):
        seed = x[0] + (seed - x[1])
        break
    print("-", seed)
  return seed
  
# Part 2
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

def _listOps2(initial_seeds, maps):
  #Create list with seed-tuples
  iterSeed = iter(initial_seeds[0])
  seed_tuples = []
  for s in iterSeed:
    seed_tuples.append((s, next(iterSeed)))
  seed_tuples = _sortSeeds(seed_tuples)
  print("start st: ", seed_tuples)  

  #compare results from one map
  if(False):
    seed_test = (seed_tuples[0][0],seed_tuples[0][1])
    seed1 = list(range(seed_test[0], seed_test[0] + seed_test[1]))
    
    seed1 = [_mapSeeds1(maps, x) for x in seed1]
    print("seed1: ", seed1)
  
    s2 = [seed_test]
    for stage_map in maps:
      print("seeds s in seed2: ", s2)
      s2_ny = []
      for s in s2:
        s2_ny.extend(update_seed_tuple(s, stage_map))
        s2 = _sortSeeds(s2_ny)
  
    print("seed2: ", s2)
    return 0

  
  for stage_map in maps:
    updated_seeds = []
    for seed in seed_tuples:
        updated_seeds.extend(update_seed_tuple(seed, stage_map))

    seed_tuples = _sortSeeds(updated_seeds)
    print("st: ", seed_tuples)  

  # Find the minimum location among the remaining seed tuples
  min_location = min(seed[0] for seed in seed_tuples)
  return min_location

def update_seed_tuple(s, stage_map):
  #print(" ")
  #print("Updating seed ", s)
  updated_seeds = []
  # Extract values from seed
  seed_list = [s]
  for x in stage_map:
    #print("Check map: ", x)
    unmoved_seeds = []
    for seed in seed_list:
      seed_start = seed[0]
      seed_length = seed[1]
      seed_end = seed_start + seed_length
      #print("Seed:")
      #print(seed_start, seed_length, seed_end)
      # Extract relevant values from the map
      map_destination_start, map_source_start, map_length = x
      map_source_end = map_source_start + map_length
      map_destination_end = map_destination_start + map_length

      #check if seed is outside the target
      if(seed_start >= map_source_end or seed_end <= map_source_start):
        unmoved_seeds.append((seed_start, seed_length))
      else:
        #check if seed starts inside the target
        if(seed_start >= map_source_start):
          #check if seed ends inside the target
          if(seed_end <= map_source_end):
            #seed starts and ends inside the target
            #print("seed starts and ends inside the target")
            #print("Map ", x)
            new_start = (seed_start - map_source_start)
            #print("new: ({},{})".format(map_destination_start + new_start, seed_length))
            updated_seeds.append((map_destination_start + new_start, seed_length))

          else:
            #seed starts inside and ends outside the target
            #print("seed starts inside and ends outside the target")
            relative_start = (seed_start - map_source_start)
            new_length = (map_source_end - seed_start)
            #print("Map ", x)
            #print("new seed 1: ({},{})".format(map_destination_start + relative_start, new_length))
            #print("left of seed 2: ({},{})".format(map_destination_end, seed_length - new_length))
            
            updated_seeds.append((map_destination_start + relative_start, new_length))
            seed_start = map_source_end
            seed_length = seed_end - map_source_end
            unmoved_seeds.append((seed_start, seed_length))
            
            if(seed_length < 0):
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
            #print("new seed 1: ({},{})".format(new_start, new_length))
            #print("leftover seed 2: ({},{})".format(seed_start, seed_length - new_length))
            updated_seeds.append((new_start, new_length))
            #updated_seeds.append((seed_start, seed_length - new_length))
  
            # Update leftover seeds
            seed_length = seed_length - new_length
            # seed_end = seed_start + seed_length
            unmoved_seeds.append((seed_start, seed_length))
            if(seed_length < 0):
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
            #print("leftover 2: ({},{})".format(seed_start, new_length_before))
            #print("leftover 3: ({},{})".format(map_source_end, new_length_after))
            updated_seeds.append((new_start, new_length))
            #updated_seeds.append((seed_start, new_length_before))
            #updated_seeds.append((map_source_end, new_length_after))
  
            # Update leftover seed, start
            s1_start = seed_start
            s1_length = new_length_before
            unmoved_seeds.append((s1_start, s1_length))
            # Update leftover seed, end
            s2_start = map_source_end
            s2_length = new_length_after
            unmoved_seeds.append((s2_start, s2_length))
            
            if(new_length_before < 0):
              print("ERROR: negative length")
              print("a4")
            if(new_length_after < 0):
              print("ERROR: negative length")
              print("a5")
              print("seed: ", seed)
              print("map: ", x)

    seed_list = unmoved_seeds
    #print("SEEDS LEFT AFTER ITErATE: ", unmoved_seeds)
    if not (len(seed_list) > 0):
      break
  if len(seed_list) > 0:
    updated_seeds.extend(seed_list)
  
  return updated_seeds


if __name__ == "__main__":
  func = _stringParsingSeeds
  seeds = parseWithFunction(func)
  func = _stringParsingMaps
  parsed_input = parseWithFunction(func)

  print("Part 1: ", _listOps1(seeds, parsed_input))
  print("Part 2: ", _listOps2(seeds, parsed_input))
  
