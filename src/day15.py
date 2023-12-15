import sys
from myModules.inputParser import parseWithFunction  #type: ignore


# Build data structure (as a list)
def _stringParsing(str):
  return str.split(",")

def _hashASCII(lens):
  total = 0
  for s in lens:
    # Determine the ASCII code for the current character of the string.
    _ascii = ord(s)

    # Increase the current value by the ASCII code you just determined.
    total += _ascii
    
    # Set the current value to itself multiplied by 17.
    total *= 17

    # Set the current value to the remainder of dividing itself by 256.
    total = total % 256
  return total
# Part 1
def _listOps1(alist):
  [lenses] = alist
  total = 0
  for lens in lenses:
    total += _hashASCII(lens)

  return total

def _addLens(new_lens, box):
  checked = []
  while box:
    lens = box.pop(0)
    # Compare labels
    if lens[0] == new_lens[0]:
      # new_lens exists in box
      lens[1] = new_lens[1]
      checked.append(lens)
      checked.extend(box)
      return checked
    else:
      checked.append(lens)
  # new_lens did not exist in box
  checked.append(new_lens)
  return checked

def _removeLens(label, box):
  checked = []
  while box:
    lens = box.pop(0)
    if not lens[0] == label:
      checked.append(lens)
  
  return checked
def _operate(lens, boxes):
  lens = lens.split('=')
  if len(lens) > 1:
    position = _hashASCII(lens[0])
    # Add
    boxes[position] = _addLens(lens, boxes[position])

  else:
    [lens] = lens
    [lens,_] = lens.split('-')
    position = _hashASCII(lens)
    # Remove
    boxes[position] = _removeLens(lens, boxes[position])
  return boxes

# Part 2
def _listOps2(alist):
  [lenses] = alist
  boxes = [[] for _ in range(257)]
  for lens in lenses:
    boxes = _operate(lens, boxes)

  total = 0
  for i in range(len(boxes)):
    for j in range(len(boxes[i])):
      total += (i+1) * (j+1) * int(boxes[i][j][1])
  return total


if __name__ == "__main__":
  func = _stringParsing
  parsed_input = parseWithFunction(func)
  # print(parsed_input)
  print("Part 1: ", _listOps1(parsed_input))
  print("Part 2: ", _listOps2(parsed_input))
