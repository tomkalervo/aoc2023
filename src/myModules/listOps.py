def reduceList(list, func):
  #print("reduce list, list: ", list)
  if len(list) < 1:
    return list

  list.reverse()
  keep = []
  keep.append(list.pop())

  while list:
    item1 = keep.pop()
    item2 = list.pop()
    items = func(item1, item2)
    keep.extend(items)

  return keep

def transpose(matrix):
  t_matrix = list(map(''.join, zip(*matrix)))
  return t_matrix

def rotate_clockwise(matrix):
    # Use zip(*matrix[::-1]) to rotate anticlockwise
    rotated_matrix = [list(row) for row in zip(*matrix[::-1])]
    return rotated_matrix

def rotate_anticlockwise(matrix):
    # Reverse the columns and then transpose
    rotated_matrix = [list(row) for row in zip(*matrix)][::-1]
    return rotated_matrix