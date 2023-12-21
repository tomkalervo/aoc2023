import re
from myModules.inputParser import parseWithFunction  #type: ignore


# Build data structure (as a list)
def _stringParsing(str):
  # rfg{s<537:gd,x>2440:R,A}
  rule = [e for e in filter(None, re.split("\{|\}|,|\)", str))]
  workflow = {rule[0] : rule[1:]}
  for rule in parseWithFunction(lambda x: 
    [e for e in filter(None, re.split("\{|\}|,|\)", x))]):
      workflow.update({rule[0] : rule[1:]})

  # {x=787,m=2655,a=1222,s=2876}
  ratings = parseWithFunction(lambda x: 
      [(k, int(v)) for k, v in re.findall(r'(\w+)=(\d+)', x)])

  return workflow,ratings

def work(workflow,xmas,name):
  if name == 'A':
    return True 
  if name == 'R':
    return False
  
  flow = workflow[name]
  # in  :  ['s<1351:px', 'qqz']
  for rule in flow:
    matches = re.match(r'([x,m,a,s])([<,>])(\d+):(\w+)', rule)
    if matches:
      k, o, v, n = matches.groups()
      for (item,value) in xmas:
        if item == k:
          difference = value - int(v)
          if o == '<' and difference < 0:
              return work(workflow,xmas,n)
          if o == '>' and difference > 0:
              return work(workflow,xmas,n)  
    else:
      return work(workflow,xmas,rule)
  return False
# Part 1
def _listOps1(alist):
  [(workflow,ratings)] = alist
  accepted = []
  
  while ratings:
    xmas = ratings.pop()
    if work(workflow,xmas,'in'):
      accepted.append(xmas)

  return sum(v for xmas in accepted for _,v in xmas)

#Recursive function
def _findAllWork(xmas,workflow,name,total):
  if name == 'A':
    permutations = 1
    for z in xmas:
      x,y = xmas[z]
      permutations *= 1 + (y-x)
    return total + permutations
  if name == 'R':
    return 0
  for rule in workflow[name]:
    matches = re.match(r'([x,m,a,s])([<,>])(\d+):(\w+)', rule)
    if matches:
      k, o, v, n = matches.groups()
      for ok,xs in _update_set(xmas, k, o, int(v), n):
        if ok:
          total += _findAllWork(xs,workflow,n,0)
        else:
          xmas = xs
    else:
      total += _findAllWork(xmas,workflow,rule,0)
  return total
    
  print("End of function..")
def _update_set(xmas, k, o, v, n):
  x,y = xmas[k]
  if o == '>':
    if y <= v:
      return [(False, xmas)]
    elif x > v:
      return[(True,xmas)]
    else: #split
      xmas1 = xmas.copy()
      xmas2 = xmas.copy()
      xmas1[k] = (x,v)
      xmas2[k] = (v+1,y)
      return [(False, xmas1),(True, xmas2)]
  else: # o == <
    if y < v:
      return [(True, xmas)]
    elif x >= v:
      return[(False,xmas)]
    else: #split
      xmas1 = xmas.copy()
      xmas2 = xmas.copy()
      xmas1[k] = (x,v-1)
      xmas2[k] = (v,y)
      return [(True, xmas1),(False, xmas2)]
      

# Part 2
def _listOps2(alist):
  [(workflow,_)] = alist
  total = 0
  min_v = 1
  max_v = 4001
  xmas = {x : (1,4000) for x in 'xmas'}

  return _findAllWork(xmas,workflow,'in',0)



if __name__ == "__main__":
  func = _stringParsing
  parsed_input = parseWithFunction(func)
  print("Part 1: ", _listOps1(parsed_input))
  print("Part 2: ", _listOps2(parsed_input))
