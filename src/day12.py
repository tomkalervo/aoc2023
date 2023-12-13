from myModules.inputParser import parseWithFunction  #type: ignore

# Build data structure (as a list)
def _stringParsing(str):
  [springs, data] = str.split(' ')
  data = [int(x) for x in data.split(',')]
  return [springs, data]

# Entry point for the exhaustive search for feasible permutations
def _exSearchEntry(pruned_list):
  [springs, data] = pruned_list
  (count,_) = _exSearch(list(springs), data, {}, 0)
  return count
  
# Recursive function for exhaustive search
def _exSearch(springs, data, map, count):
  # Basecase 1, out of values to assign
  if not data:
    if '#' not in springs:
      return (1, map)
    else:
      return (0, map)
  # Basecase 2, out elements in the list
  if not springs:
    if not data:
      return (1, map)
    else:
      return (0, map)

  # Found in chache
  if (tuple(springs), tuple(data)) in map:
    return (map[(tuple(springs), tuple(data))], map)

  next_spring = springs[0]
  next_value = data[0]
  # Basecase 3, cannot fill the next value
  if next_value > len(springs):
    return (0, map)

  # Continue to next spring
  if next_spring == '.':
    return _exSearch(springs[1:], data, map, count)
  elif next_spring == '#':
    if '.' in springs[:next_value]:
      return (0, map)
    else:
      if next_value == len(springs):
        return _exSearch(springs[next_value+1:], data[1:], map, count)
      elif springs[next_value] == '#':
        return (0, map)
      else:
        return _exSearch(springs[next_value+1:], data[1:], map, count)
  else:
    # next_spring == '?'
    # Recursive cases
    springs[0] = '#'
    (c1, map) = _exSearch(springs, data, map, 0)
    map.update({(tuple(springs), tuple(data)) : c1})

    springs[0] = '.'
    (c2, map) = _exSearch(springs, data, map, 0)
    map.update({(tuple(springs), tuple(data)) : c2})

    return (count+c1+c2, map)

# Part 1
def _listOps1(alist):
  total = sum(_exSearchEntry(springs) for springs in alist)
  return total

# Part 2
def _listOps2(alist):
  total = 0
  for item in alist:
    [springs, data] = item
    unfolded_springs = springs + (('?' + springs) * 4)
    unfolded_data = data * 5
    total += _exSearchEntry([unfolded_springs, unfolded_data])

  return total


if __name__ == "__main__":
  func = _stringParsing
  parsed_input = parseWithFunction(func)
  #print(parsed_input)
  print("Part 1: ", _listOps1(parsed_input))
  print("Part 2: ", _listOps2(parsed_input))
