from myModules.inputParser import parseWithFunction  #type: ignore

def _stringParsing(str):
  # print(str)
  a = _getIntFromStart(str)
  b = _getIntFromEnd(str)
  a += b
  # print(a)
  return int(a)

def _getNumberFromString(func):
  numbers = [
    "zero", "one", "two", 
    "three", "four", "five",
    "six", "seven", "eight", 
    "nine"
  ]
  i = 0
  for number in numbers:
    if func(number):
      break
    else:
      i += 1
  if i < 10:
    return "{}".format(i)
  else:
    return ""
  
# Used for part 1
def _getInts(str, number):
  for element in str:
    if element.isdigit():
      number += element
      break
  return number
  
# Used for part 2
def _getIntFromStart(str):
  number = ""
  while str:
    if str[0].isdigit():
      number = str[0]
      break
      
    else:
      number = _getNumberFromString(str.startswith)
      if number:
        break
      else:
        str = str[1:]
    
  return number

def _getIntFromEnd(str):
  number = ""
  while str:
    if str[-1].isdigit():
      number = str[-1]
      break
  
    else:
      number = _getNumberFromString(str.endswith)
      if number:
        break
      else:
        str = str[:-1]
  
  return number

def _listOps(ls):
  return sum(ls)


if __name__ == "__main__":
  func = _stringParsing
  parsed_input = parseWithFunction(func)
  print(_listOps(parsed_input))
