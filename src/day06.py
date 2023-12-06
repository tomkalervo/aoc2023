from myModules.inputParser import parseWithFunction  #type: ignore

# Build data structure (as a list)
def _stringParsing(str):
  [_,str] = str.split(":")
  str = [int(x) for x in str.strip().split()]
  return str

# Part 1
def _listOps1(alist):
  milliseconds, distances = alist
  ways_to_win = 1
  for _ in range(0, len(milliseconds)): 
    ms = milliseconds.pop()
    ds = distances.pop()
    ways_to_win *= _beatDistance(ms, ds)

  return ways_to_win

def _beatDistance(ms, ds):
  ways_to_win = 1
  start = ms // 2
  d = start * (ms - start)
  if d > ds:
    for i in range(1, start):
      #print("i, ", i)
      current_wins = ways_to_win
      d = (start-i) * (ms-(start-i))
      if d > ds:
        #print("d, ", d)
        ways_to_win += 1
        
      d = (i+start) * (ms-(i+start))
      if d > ds:
        #print("d, ", d)
        ways_to_win += 1

      if(current_wins == ways_to_win):
        break
  print(ways_to_win)
  return ways_to_win

# Part 2
def _listOps2(alist):
  print("solver 2")
  milliseconds, distances = alist
  ms = 0
  ds = 0
  i = 0
  while(distances):
    d = distances.pop()
    ds += pow(10, i) * d
    while(d > 0):
      i += 1
      d = d // 10
  i = 0
  while(milliseconds):
    n = milliseconds.pop()
    ms += pow(10, i) * n
    while(n > 0):
      i += 1
      n = n // 10

  print(ms)
  print(ds)
  ways_to_win = _loseDistance(ms,ds)

  return ways_to_win

def _loseDistance(ms,ds):
  lose_up_to = 0
  for i in range(0, ms):
    #print("i at ", i)
    ms_left = ms - i
    d = i * ms_left
    if(d > ds):
      #print("Stop i at ", i)
      break
    else:
      lose_up_to = (i+1)
      
  lose_down_to = 0
  for i in range(ms, -1, -1):
    #print("i at ", i)
    ms_left = ms - i
    d = i * ms_left
    if(d > ds):
      #print("Stop i at ", i)
      break
    else:
      lose_down_to = i

  print(lose_up_to)
  print(lose_down_to)
  return lose_down_to - lose_up_to

if __name__ == "__main__":
  func = _stringParsing
  parsed_input = parseWithFunction(func)
  print(parsed_input)
  parsed_input1 = []
  parsed_input2 = []
  for x in parsed_input:
    parsed_input1.append(x.copy())
    parsed_input2.append(x.copy())
  print("Part 1: ", _listOps1(parsed_input1))
  print("Part 2: ", _listOps2(parsed_input2))
