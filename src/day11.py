from myModules.inputParser import parseWithFunction  #type: ignore


# Build data structure (as a list)
def _stringParsing(str):
  return str


def _getGalaxyPositions(map, expand_space):
  vertical_spaces = []
  for x in range(len(map)):
    spaces = 0
    for row in map:
      if row[x] == '.':
        spaces += 1
    if spaces == len(map[x]):
      vertical_spaces.append(x)

  points = []
  galaxy = 0
  y = 0
  y_real = 0
  while map:
    row = map.pop(0)
    x = 0
    x_real = 0
    spaces = 0
    for space in row:
      if space == '.':
        spaces += 1
      else:
        points.append((x_real, y_real, galaxy))
        galaxy += 1
      if x in vertical_spaces:
        x_real += expand_space
      else:
        x_real += 1

      x += 1
    if spaces == len(row):
      y_real += expand_space
    else:
      y_real += 1

    y += 1
  return points


# Part 1
def _listOps1(alist):
  list_of_positions = _getGalaxyPositions(alist, 2)
  list_of_distances = []
  while list_of_positions:
    galaxy1 = list_of_positions.pop(0)
    for galaxy2 in list_of_positions:
      distance = abs(galaxy1[0] - galaxy2[0]) + abs(galaxy1[1] - galaxy2[1])
      #print("distance from galaxy {} to galaxy {} is {}".format(galaxy1, galaxy2, distance))
      list_of_distances.append(distance)

  return sum(list_of_distances)


# Part 2 - distance of 1 000 000
def _listOps2(alist):
  list_of_positions = _getGalaxyPositions(alist, 1000000)
  list_of_distances = []
  while list_of_positions:
    galaxy1 = list_of_positions.pop(0)
    for galaxy2 in list_of_positions:
      distance = abs(galaxy1[0] - galaxy2[0]) + abs(galaxy1[1] - galaxy2[1])
      list_of_distances.append(distance)

  return sum(list_of_distances)


if __name__ == "__main__":
  func = _stringParsing
  parsed_input1 = parseWithFunction(func)
  parsed_input2 = []
  for x in parsed_input1:
    parsed_input2.append(x)
  #print(parsed_input)
  print("Part 1: ", _listOps1(parsed_input1))
  print("Part 2: ", _listOps2(parsed_input2))
