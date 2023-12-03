from myModules.inputParser import parseWithFunction  #type: ignore
def _stringParsing(str):
  return '.' + str + '.'

def _connectedToSymbol(i,j,prevRow,currentRow,nextRow):
  k = i-1
  if currentRow[k] != '.':
    return True
  if currentRow[j] != '.':
    return True
    
  while k < (j+1):
    if prevRow[k] != '.':
      return True
    elif nextRow[k] != '.':
      return True
    else:
      k += 1

  return False
    
def _listOps1(list):
  dummy = '.' * len(list[0])
  list.append(dummy)
  list.append(dummy)

  prevRow = dummy
  [currentRow, nextRow, *rest] = list
  sum = 0
  while(len(rest) > 0):
    i = 0
    while i < len(currentRow):
      j = 0
      while currentRow[i+j].isdigit():
        j += 1
      if (j+i) > i:
        if _connectedToSymbol(i,(j+i),prevRow,currentRow,nextRow):
          sum += int(currentRow[i:(j+i)])
        
        i = (j+i)
      else:
        i += 1
        
    prevRow = currentRow
    currentRow = nextRow
    [nextRow, *rest] = rest
  
  return sum

def _getNumbers(i, row, numbers):
  k = i-1
  p1 = ""
  while row[k].isdigit():
    p1 = row[k] + p1
    k -= 1

  k = i+1
  p2 = ""
  while row[k].isdigit():
    p2 = p2 + row[k] 
    k += 1

  if row[i].isdigit():
    p = p1 + row[i] + p2
    numbers.append(p)
  else:
    if p1 != "":
      numbers.append(p1)
    if p2 != "":
      numbers.append(p2)
  return numbers
  
def _getGearRatio(i, prevRow, currentRow, nextRow):
  ratio = 0
  numbers = _getNumbers(i, prevRow, [])
  numbers = _getNumbers(i, nextRow, numbers)
  numbers = _getNumbers(i, currentRow, numbers)
  # print(numbers)
  if(len(numbers) > 1):
    ratio = int(numbers[0]) * int(numbers[1])
      
  return ratio

def _listOps2(list):
  dummy = '.' * len(list[0])
  list.append(dummy)
  list.append(dummy)
  
  prevRow = dummy
  [currentRow, nextRow, *rest] = list
  sum = 0
  while(len(rest) > 0):
    i = 0
    while i < len(currentRow):
      if currentRow[i] == '*':
        sum += _getGearRatio(i, prevRow, currentRow, nextRow)
      i += 1
  
    prevRow = currentRow
    currentRow = nextRow
    [nextRow, *rest] = rest
  
  return sum

if __name__ == "__main__":
  func = _stringParsing
  parsed_input = parseWithFunction(func)
  print("Part 1: ", _listOps1(parsed_input))
  print("Part 2: ", _listOps2(parsed_input))