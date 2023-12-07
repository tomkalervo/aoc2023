from functools import cmp_to_key
from myModules.inputParser import parseWithFunction  #type: ignore

# Build data structure (as a list)
# List of tuples (hand of cards, bid)
def _stringParsing(str):
  hand, bid = str.split()
  return (hand, int(bid))

# Part 1
def _listOps1(list_of_hands):
  list_of_hands = _sortHands(list_of_hands)
  #print(list_of_hands)
  total = 0
  i = 0
  for (_,bid) in list_of_hands:
    i += 1
    total += bid * i

  return total
def _sortHands(list_of_hands):
  fiveKind = []
  fourKind = []
  fullHouse = []
  threeKind = []
  twoPair = []
  onePair = []
  highCard = []

  for (hand, bid) in list_of_hands:
    cards = {}
    for card in hand:
      if card in cards:
        cards[card] += 1
      else:
        cards.update({card: 1})
        
    if len(cards) == 1:
      fiveKind.append((hand, bid))
    elif len(cards) == 5:
      highCard.append((hand, bid))
    elif len(cards) == 4:
      onePair.append((hand, bid))
    elif len(cards) == 3:
      #either three-of-a-kind or two-pair
      three_of_a_kind = False
      for card in cards:
        if cards[card] == 3:
          three_of_a_kind = True
          break
      if three_of_a_kind:
        threeKind.append((hand, bid))
      else:
        twoPair.append((hand, bid))
    else:
      #either four-of-a-kind or full-house  
      four_of_a_kind = False
      for card in cards:
        if cards[card] == 4:
          four_of_a_kind = True
          break
      if four_of_a_kind:
        fourKind.append((hand, bid))
      else:
        fullHouse.append((hand, bid)) 

  sortedHands = []
  # order
  if highCard:
    highCard = sorted(highCard, key = cmp_to_key(_sortCards))
    sortedHands.extend(highCard)
  if onePair:
    onePair = sorted(onePair, key = cmp_to_key(_sortCards))
    sortedHands.extend(onePair)
  if twoPair:
    twoPair = sorted(twoPair, key = cmp_to_key(_sortCards))
    sortedHands.extend(twoPair)
  if threeKind:
    threeKind = sorted(threeKind, key = cmp_to_key(_sortCards))
    sortedHands.extend(threeKind)
  if fullHouse:
    fullHouse = sorted(fullHouse, key = cmp_to_key(_sortCards))
    sortedHands.extend(fullHouse)
  if fourKind:
    fourKind = sorted(fourKind, key = cmp_to_key(_sortCards))
    sortedHands.extend(fourKind)
  if fiveKind:
    fiveKind = sorted(fiveKind, key = cmp_to_key(_sortCards))
    sortedHands.extend(fiveKind)
    
  return sortedHands
def _sortCards(hand1, hand2):
  # print("Sorting {} with {}".format(hand1, hand2))
  card1, _ = hand1
  card2, _ = hand2
  cardValue = {
    'A' : 14,
    'K' : 13,
    'Q' : 12,
    'J' : 11,
    'T' : 10,
    '9' : 9,
    '8' : 8,
    '7' : 7,
    '6' : 6,
    '5' : 5,
    '4' : 4,
    '3' : 3,
    '2' : 2
  }
  
  for i in range(0, len(card1)):
    c1 = cardValue[card1[i]]
    c2 = cardValue[card2[i]]
    if c1 > c2:
      return 1
    elif c1 < c2:
      return -1
      
  return 0

# Part 2 - The Joker
def _listOps2(list_of_hands):
  list_of_hands = _sortHandsWithJoker(list_of_hands)
  #print(list_of_hands)
  total = 0
  i = 0
  for (_,bid) in list_of_hands:
    i += 1
    total += bid * i

  return total
def _sortHandsWithJoker(list_of_hands):
  fiveKind = []
  fourKind = []
  fullHouse = []
  threeKind = []
  twoPair = []
  onePair = []
  highCard = []
  
  for (hand, bid) in list_of_hands:
    cards = {}
    for card in hand:
      if card in cards:
        cards[card] += 1
      else:
        cards.update({card: 1})
  
    if len(cards) == 1:
      # no effect
      fiveKind.append((hand, bid))
    elif len(cards) == 5:
      # could be a pair
      if 'J' in cards:
        onePair.append((hand, bid))
      else:
        highCard.append((hand, bid))
    elif len(cards) == 4:
      # could be three-of-a-kind, (1 or 2 J possible)
      if 'J' in cards:
        threeKind.append((hand, bid))
      else:
        onePair.append((hand, bid))
    elif len(cards) == 3:
      #either three-of-a-kind or two-pair
      three_of_a_kind = False
      for card in cards:
        if cards[card] == 3:
          three_of_a_kind = True
          break
      if three_of_a_kind:
        #could be four-of-a-kind (always beat full house)
        if 'J' in cards:
          fourKind.append((hand, bid))
        else:
          threeKind.append((hand, bid))
      else:
        #could be full-house or four-of-a-kind
        if 'J' in cards:
          if cards['J'] == 1:
            fullHouse.append((hand, bid))
          else:
            fourKind.append((hand, bid))
        else:
          twoPair.append((hand, bid))
    else:
      # either four-of-a-kind or full-house  
      # could be five-of-a-kind
      if 'J' in cards:
        fiveKind.append((hand, bid))
      else:
        four_of_a_kind = False
        for card in cards:
          if cards[card] == 4:
            four_of_a_kind = True
            break
        if four_of_a_kind:
          fourKind.append((hand, bid))
        else:
          fullHouse.append((hand, bid)) 
  
  sortedHands = []
  # order
  if highCard:
    highCard = sorted(highCard, key = cmp_to_key(_sortCardsWithJoker))
    sortedHands.extend(highCard)
    #print(highCard)
  if onePair:
    onePair = sorted(onePair, key = cmp_to_key(_sortCardsWithJoker))
    sortedHands.extend(onePair)
    #print(onePair)
  if twoPair:
    twoPair = sorted(twoPair, key = cmp_to_key(_sortCardsWithJoker))
    sortedHands.extend(twoPair)
    #print(twoPair)
  if threeKind:
    threeKind = sorted(threeKind, key = cmp_to_key(_sortCardsWithJoker))
    sortedHands.extend(threeKind)
    #print(threeKind)
  if fullHouse:
    fullHouse = sorted(fullHouse, key = cmp_to_key(_sortCardsWithJoker))
    sortedHands.extend(fullHouse)
    #print(fullHouse)
  if fourKind:
    fourKind = sorted(fourKind, key = cmp_to_key(_sortCardsWithJoker))
    sortedHands.extend(fourKind)
    #print(fourKind)
  if fiveKind:
    fiveKind = sorted(fiveKind, key = cmp_to_key(_sortCardsWithJoker))
    sortedHands.extend(fiveKind)
    #print(fiveKind)
  
  return sortedHands
def _sortCardsWithJoker(hand1, hand2):
  # print("Sorting {} with {}".format(hand1, hand2))
  card1, _ = hand1
  card2, _ = hand2
  cardValue = {
    'A' : 14,
    'K' : 13,
    'Q' : 12,
    'J' : 1,
    'T' : 10,
    '9' : 9,
    '8' : 8,
    '7' : 7,
    '6' : 6,
    '5' : 5,
    '4' : 4,
    '3' : 3,
    '2' : 2
  }
  
  for i in range(0, len(card1)):
    c1 = cardValue[card1[i]]
    c2 = cardValue[card2[i]]
    if c1 > c2:
      return 1
    elif c1 < c2:
      return -1
      
  return 0

if __name__ == "__main__":
  func = _stringParsing
  parsed_input = parseWithFunction(func)
  #print(parsed_input)
  print("Part 1: ", _listOps1(parsed_input))
  print("Part 2: ", _listOps2(parsed_input))
