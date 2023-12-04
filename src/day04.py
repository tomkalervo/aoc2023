from myModules.inputParser import parseWithFunction  #type: ignore
def _stringParsing(str):
  str = str.split(":")
  card = []
  for c in str[0]:
    if c.isdigit():
      card.append(int(c))
      break

  str = str[1].split("|")
  winners = []
  for x in str[0].split(" "):
    if(x.isdigit()):
      winners.append(int(x))

  numbers = []
  for x in str[1].split(" "):
    if(x.isdigit()):
      numbers.append(int(x))

  card.append(winners)
  card.append(numbers)
  
  return card

def _listOps2(cards):
  sum = 0
  copiesNext = [1]
  copiesUsed = []
  while(len(cards) > 0):
    [_, winners, numbers] = cards.pop(0)
    if (len(copiesNext) == 0):
      copiesNext = [1]
    
    copies = copiesNext.pop(0)
    copiesUsed.append(copies)
    wins = 0
    for x in numbers:
      if x in winners:
        wins += 1
    for x in range(0, wins):
      if len(copiesNext) <= x:
        copiesNext.append(1)
      
      copiesNext[x] += copies
        
  for x in copiesUsed:
    sum += x
    
  return sum
  
def _listOps1(cards):
  sum = 0
  for card in cards:
    points = 0
    [_, winners, numbers] = card
    for x in numbers:
      if x in winners:
        points = 1 if points == 0 else points << 1

    sum += points
  
  return sum

if __name__ == "__main__":
  func = _stringParsing
  parsed_input = parseWithFunction(func)
  print("Part 1: ", _listOps1(parsed_input))
  print("Part 2: ", _listOps2(parsed_input))