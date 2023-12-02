from myModules.inputParser import parseWithFunction  #type: ignore

# Build data structure
def _stringParsing(str):
  # Example input of str:
  # Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
  [game, hands] = str.split(": ")
  game = game.split(" ")
  hands = hands.split("; ")
  resList = []
  for results in hands:
    results = results.split(", ")
    handList = []
    for result in results:
      result = result.split(" ")
      handList.append([result[1], int(result[0])])
    resList.append(handList)
  return [int(game[1]), resList]

# Part 2
def _listOps2(games):
  sum = 0
  # Calculate the cubic power, in each game
  for [_,*hands] in games:
    power = 1
    red = 0
    green = 0
    blue = 0
    powerList = [red, green, blue]
    # Calculate the cubic power of all hands
    for hand in hands:
      for colors in hand:
        powerList = _updatePower(colors, powerList)
    # Sum the cubic powers from this game
    for color in powerList:
      power *= color
    sum += power
    
  return sum

def _updatePower(hand, powerList):
  for color in hand:
    match color:
     case ["red", x] if x > powerList[0] :
      powerList[0] = x
     case ["green", x] if x > powerList[1] :
       powerList[1] = x
     case ["blue", x] if x > powerList[2] :
       powerList[2] = x
  return powerList
  
# Part 1
def _listOps1(games):
  sum = 0
  for [game,*hands] in games:
    for hand in hands:
      match = False
      for colors in hand:
        if  _matchConditions(colors):
          match = True
          break
      if not match:
        sum += game
  return sum

def _matchConditions(colors):
  for color in colors:
    match color:
     case ["red", x] if x > 12 :
      return True
     case ["green", x] if x > 13 :
      return True
     case ["blue", x] if x > 14 :
      return True
  
  return False

if __name__ == "__main__":
  func = _stringParsing
  parsed_input = parseWithFunction(func)
  print("Part 1: ", _listOps1(parsed_input))
  print("Part 2: ", _listOps2(parsed_input))
