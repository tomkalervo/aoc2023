from myModules.inputParser import parseWithFunction  #type: ignore

def _stringParsing(str):
  e = []
  for y in str.strip("()").split(","):
    e.append(int(y))
  return e


def _listOps(ls):
  for e in ls:
    print("{} + {} = {}".format(e[0], e[1], e[0] + e[1]))


if __name__ == "__main__":
  func = _stringParsing
  parsed_input = parseWithFunction(func)
  _listOps(parsed_input)
