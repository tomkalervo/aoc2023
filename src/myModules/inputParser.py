def parseWithFunction(fun):
  return_list = []
  line = input()
  while line:
    return_list.append(fun(line))
    try:
      line = input()
    except EOFError:
      break

  return return_list
