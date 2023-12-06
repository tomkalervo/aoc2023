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
