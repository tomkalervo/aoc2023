from myModules.inputParser import parseWithFunction  #type: ignore


# Build data structure (as a list)
def _stringParsing(str):
  rows = []
  rows.append(str)
  rows.extend(parseWithFunction(lambda x: x))
  return rows


def _equal(mirror, i):
  j = i - 1
  while i < len(mirror) and j >= 0:
    if mirror[i] != mirror[j]:
      return False
    else:
      i += 1
      j -= 1
  return True


def _getMirrors(mirrors, count):
  remaining = []
  for mirror in mirrors:
    i = 1
    while i < len(mirror):
      if mirror[i - 1] == mirror[i] and _equal(mirror, i):
        break
      i += 1

    if i >= len(mirror):
      remaining.append(mirror)
    else:
      count += i
  return (remaining, count)


def _transpose(matrix):
  t_matrix = list(map(''.join, zip(*matrix)))
  return t_matrix


# Part 1
def _listOps1(alist):
  (remeinder, total_vertical) = _getMirrors(alist, 0)
  print("count after first is ", total_vertical)

  mirrors = []
  for mirror in remeinder:
    mirrors.append(_transpose(mirror))

  (remeinder, total_horisontal) = _getMirrors(mirrors, 0)
  if remeinder:
    print("rem: ", remeinder)
  print("count after second is ", total_horisontal)

  return total_horisontal + (100 * total_vertical)


def _equalWithSmudge(mirror, i):
  diff = 0
  j = i - 1
  while i < len(mirror) and j >= 0:
    diff += sum(1 for a, b in zip(mirror[i], mirror[j]) if a != b)
    if diff > 1:
      return False
    else:
      i += 1
      j -= 1
      
  return diff == 1

def _getMirrorsWithSmudge(mirrors, count):
  remaining = []
  for mirror in mirrors:
    i = 1
    while i < len(mirror):
      if _equalWithSmudge(mirror, i):
        break
      i += 1

    if i >= len(mirror):
      remaining.append(mirror)
    else:
      count += i
  return (remaining, count)


# Part 2
def _listOps2(alist):
  (remeinder, total_vertical) = _getMirrorsWithSmudge(alist, 0)
  print("count after first is ", total_vertical)

  mirrors = []
  for mirror in remeinder:
    mirrors.append(_transpose(mirror))

  (remeinder, total_horisontal) = _getMirrorsWithSmudge(mirrors, 0)
  print("count after second is ", total_horisontal)

  if remeinder:
    print("rem: ", remeinder)

  return total_horisontal + (total_vertical * 100)


if __name__ == "__main__":
  func = _stringParsing
  parsed_input = parseWithFunction(func)
  #print(parsed_input)
  print("Part 1: ", _listOps1(parsed_input))
  print("Part 2: ", _listOps2(parsed_input))
