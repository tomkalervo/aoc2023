from myModules.inputParser import parseWithFunction  #type: ignore


# Build data structure (as a list)
def _stringParsing(str):
  print("hej")
  return str


# Part 1
def _listOps1(alist):
  total = sum(1 for _ in alist)

  return total


# Part 2
def _listOps2(alist):
  total = sum(1 for _ in alist)

  return total


if __name__ == "__main__":
  func = _stringParsing
  parsed_input = parseWithFunction(func)
  print(parsed_input)
  print("Part 1: ", _listOps1(parsed_input))
  print("Part 2: ", _listOps2(parsed_input))
