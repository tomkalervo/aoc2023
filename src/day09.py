from myModules.inputParser import parseWithFunction  #type: ignore

# Build data structure (as a list)
def _stringParsing(str):
  
  return [int(x) for x in str.split(" ")]


# Part 1
def _list_op1(alist):
  total = 0
  for l in alist:
    l = _get_levels(l)
    l = _get_next_values(l)
    future_value = l[-1][-1]
    total += future_value

  return total

def _get_levels(line_of_history):
    lines = [line_of_history]
    while not all(i == 0 for i in line_of_history):
        new_line = []
        for i in range(0, len(line_of_history)-1):
            # Increase from a to b
            a = line_of_history[i]
            b = line_of_history[i+1]
            new_line.append(b - a)
        lines.append(new_line)
        line_of_history = new_line
    return lines

def _get_next_values(lines_of_history):
    future_lines = []
    prev_line = lines_of_history.pop()
    prev_line.append(0)
    future_lines.append(prev_line)
    while lines_of_history:
        line = lines_of_history.pop()
        a = prev_line[-1]
        b = line[-1]
        future = a + b
        line.append(future)
        future_lines.append(line)
        prev_line = line

    return future_lines

# Part 2
def _list_op2(alist):
  total = 0
  for l in alist:
    l = _get_levels(l)
    l = _get_next_values_before(l)
    future_value = l[-1][0]
    total += future_value

  return total

def _get_next_values_before(lines_of_history):
    future_lines = []
    prev_line = lines_of_history.pop()
    prev_line.append(0)
    future_lines.append(prev_line)
    while lines_of_history:
        line = lines_of_history.pop()
        a = prev_line[0]
        b = line[0]
        future = b - a
        line = [future] + line
        future_lines.append(line)
        prev_line = line

    return future_lines


if __name__ == "__main__":
  func = _stringParsing
  parsed_input = parseWithFunction(func)
  #print(parsed_input)
  print("Part 1: ", _list_op1(parsed_input))
  print("Part 2: ", _list_op2(parsed_input))
