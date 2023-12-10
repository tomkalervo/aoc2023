from myModules.inputParser import parseWithFunction  #type: ignore


# Build data structure (as a list)
def _stringParsing(str):
  return tuple(str)

# functions for part 1
def _getStartPos(pipes):
    y = 0
    for rows in pipes:
        x = 0
        for pipe in rows:
            if pipe == 'S':
                return (x,y)
            else:
                x += 1
        y += 1
def _viewPos(point, pipes):
  for y in range(point[1]-1, point[1]+2):
    row = []
    for x in range(point[0]-1, point[0]+2):
        row.append(pipes[y][x])
    print(row)
def _getConnectedPipes(point, pipes):
    x,y = point
    pipe = pipes[y][x]
    match pipe:
        case '|':
            return [(x,y-1), (x,y+1)]
        case '-':
            return [(x-1,y), (x+1,y)]
        case 'L':
            return [(x,y-1), (x+1,y)]
        case 'J':
            return [(x,y-1), (x-1,y)]
        case '7':
            return [(x-1,y), (x,y+1)]
        case 'F':
            return [(x,y+1), (x+1,y)]
        case '.':
            print("Warning: Point {} is ground".format(point))
            return [(x,y), (x+y)]
def _getPipesFromStart(start, pipes):
    next_pipes = []
    for y in range(start[1]-1, start[1]+2):
        for x in range(start[0]-1, start[0]+2):
            if y == start[1] or x == start[0]:
                if not (y == start[1] and x == start[0]):
                    tmp_pipes = _getConnectedPipes((x,y), pipes)
                    #print("point {}, {} connected to {}".format((x,y), pipes[y][x], tmp_pipes))
                    if start in tmp_pipes:
                        #print("connects")
                        next_pipes.append((x,y))
    return next_pipes
def _getNextPipe(a, from_a, pipes):
    connected_pipes = _getConnectedPipes(a, pipes)
    for next_a in connected_pipes:
        if not next_a == from_a:
            return [next_a, a]
        next_pipes = []
    for y in range(start[1]-1, start[1]+2):
        for x in range(start[0]-1, start[0]+2):
            if y == start[1] or x == start[0]:
                if not (y == start[1] and x == start[0]):
                    tmp_pipes = _getConnectedPipes((x,y), pipes)
                    #print("point {}, {} connected to {}".format((x,y), pipes[y][x], tmp_pipes))
                    if start in tmp_pipes:
                        #print("connects")
                        next_pipes.append((x,y))
    return next_pipes
# Part 1
def _listOps1(pipes):
    start = _getStartPos(pipes)
    _viewPos(start, pipes)

    a,b = _getPipesFromStart(start, pipes)
    print("Start goes from {} to {} and {}".format(start, a, b))
    from_a = start
    from_b = start

    turns = 1
    while not a == b:
        [a, from_a] = _getNextPipe(a, from_a, pipes)
        [b, from_b] = _getNextPipe(b, from_b, pipes)
        turns += 1

    return turns

# functions for part 2
def _openPoints(start_point, enc_map):
    next_pipes = []
    next_pipes.append(start_point)
    while next_pipes:
        point = next_pipes.pop()
        for y in range(point[1]-1, point[1]+2):
            for x in range(point[0]-1, point[0]+2):
                if y == point[1] or x == point[0] and not ((x,y) == point):
                    if enc_map[y][x] == 'I':
                        enc_map[y][x] = 'O'
                        next_pipes.append((x,y))

    return enc_map
# Part 2
def _listOps2(pipes):
    # Create a map for keeping track of enclosed tiles
    enclosure_map = []
    for i in range(len(pipes)):
        enclosure_row = []
        for _ in range(len(pipes[i])):
            enclosure_row.append('I')
        enclosure_map.append(enclosure_row)

    start = _getStartPos(pipes)
    enclosure_map[start[1]][start[0]] = 'S'

    # Create path of pipes
    path = [start]
    a,b = _getPipesFromStart(start, pipes)
    from_a = start

    while not a == b:
        path.append(a)
        enclosure_map[a[1]][a[0]] = pipes[a[1]][a[0]]
        [a, from_a] = _getNextPipe(a, from_a, pipes)
    
    path.append(b)
    enclosure_map[a[1]][a[0]] = pipes[a[1]][a[0]]
    path.append(start)

    # Set boarders to keep index within bounderies while pruning the map
    for i in range(len(enclosure_map)):
        enclosure_map[i] = ['I'] + enclosure_map[i] + ['I' ]
    border_row = ['I' for _ in range(len(enclosure_map[0]))]
    enclosure_map.insert(0, border_row)
    enclosure_map.append(border_row)
    for i in range(len(enclosure_map)):
        enclosure_map[i] = ['B'] + enclosure_map[i] + ['B' ]
    border_row = ['B' for _ in range(len(enclosure_map[0]))]
    enclosure_map.insert(0, border_row)
    enclosure_map.append(border_row)

    # Find all 'I' along the right side of the path of pipes.
    # Those 'I', and all adjacent 'I' are set to 'O'
    path_w_borders = []
    for point in path:
        (a,b) = point
        path_w_borders.append((a+2,b+2))
    path = path_w_borders
    s1 = path.pop(0)
    while path:
        s2 = path.pop(0)
        # norm vector [1, -1]
        n = (s2[1]-s1[1], -1*(s2[0]-s1[0]))
        p1 = (s1[0]+n[0], s1[1]+n[1])
        p2 = (s2[0]+n[0], s2[1]+n[1])

        if enclosure_map[p1[1]][p1[0]] == 'I':
            enclosure_map = _openPoints(p1, enclosure_map)
        if enclosure_map[p2[1]][p2[0]] == 'I':
            enclosure_map = _openPoints(p2, enclosure_map)
        s1 = s2

    # Sum up the enclosed tiles
    total = 0
    for row in enclosure_map:
        for point in row:
            if point == 'I':
                total += 1

    return total


if __name__ == "__main__":
  func = _stringParsing
  parsed_input = tuple(parseWithFunction(func))
  #print(parsed_input)
  print("Part 1: ", _listOps1(parsed_input))
  print("Part 2: ", _listOps2(parsed_input))
