import math
from myModules.inputParser import parseWithFunction  #type: ignore

# Build data structure (as a list)
def _stringParsing(str):
  [springs, data] = str.split(' ')
  data = [int(x) for x in data.split(',')]
  return [springs, data]

def _permutate(pruned_list):
  [springs, data] = pruned_list
  sum_data = sum(data)
  sum_assigned = springs.count('#')
  springs = list(springs)
  spring_value = sum(data)
  permutations = 0

  def backtrack(index):
    nonlocal permutations
    nonlocal sum_assigned
    nonlocal sum_data
    if (sum_assigned + (len(springs)-index) < sum_data):
      return
    elif index == len(springs):
      # All unknown springs are filled, check if the arrangement is valid
      if (sum_assigned != sum_data):
        return
      elif _feasibleRow(springs, data):
        permutations += 1
        return
      else:
        return 
    elif springs[index] == '?':
      springs[index] = '#'
      sum_assigned += 1
      backtrack(index + 1)

      springs[index] = '.'
      sum_assigned -= 1
      backtrack(index + 1)

      springs[index] = '?'
    else:
      backtrack(index + 1)

  backtrack(0)
  return permutations
def _feasibleRow(row, data):
  j = 0
  i = 0
  sum_data = 0
  while i < len(data):
    x = data[i]
    y = 0
    while j < len(row):
      if row[j] == '#':
        y += 1
      elif y > 0 and y != x:
        #print("N02 - Feasible {} is {}".format(row, False))
        return False
      elif x == y:
        break
      if y > x:
        #print("N01 - Feasible {} is {}".format(row, False))
        return False
      else:
        j += 1
    
    i += 1
    if x == y:
      sum_data += x

  if sum_data != sum(data):
    #print("N03 - Feasible {} is {}".format(row, False))
    return False
  elif j < len(row) and '#' in row[j:]:
    #print("N04 - Feasible {} is {}".format(row, False))
    return False
  else:
    #print("YYY - Feasible {} is {}".format(row, True))
    return True

# Part 1
def _listOps1(alist):

  total = sum(_permutate(springs) for springs in alist)
  return total

# TODO: Work out the logic in part 2, current not working
def _unfold_and_count(springs_list):
    [springs, data] = springs_list
    
    count = _permutate([springs, data])
    
    unfolded_springs = springs + '?'  # Unfold the arrangement once
    
    # Multiply by the count of arrangements for each unfolded arrangement
    count *= _permutate([unfolded_springs, data]) ** 4
    
    return count

# Part 2
def _listOps2(alist):
  total = sum(_unfold_and_count(springs) for springs in alist)

  return total


if __name__ == "__main__":
  func = _stringParsing
  parsed_input = parseWithFunction(func)
  #print(parsed_input)
  print("Part 1: ", _listOps1(parsed_input))
  print("Part 2: ", _listOps2(parsed_input))
