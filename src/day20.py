import re,sys
from collections import deque
from myModules.inputParser import parseWithFunction  #type: ignore

# Build data structure (as a list)
def _stringParsing(str):
  matches = re.findall(r'([%&\w]+)\s*->\s*((?:\w+\s*,\s*)*\w+)?', str)
  key, modules_str = matches[0]
  modules = modules_str.split(', ') if modules_str else []
  mod = key[0:1]
  if mod != 'b':
    key = key[1:]

  return (key,mod,tuple(modules))

def _convert_to_frozenset(obj):
    if isinstance(obj, dict):
        return frozenset((key, _convert_to_frozenset(value)) for key, value in obj.items())
    elif isinstance(obj, (list, tuple)):
        return type(obj)(_convert_to_frozenset(item) for item in obj)
    else:
        return obj
      
def _pressButton(network,state):
  rx = [] # added for part 2
  high = 0
  low = 0
  signals = deque()
  signals.append(('broadcaster','button', 0))
  while signals:
    module,sender,pulse = signals.popleft()
    if module == 'gq' and pulse == 1:
      print(f"gq got a {pulse} from {sender} -> gq states: {state['gq']}")
      sys.exit
    # if sender == 'gq':
    #   print(f"gq sent a {pulse} to {module} -> gq states: {state['gq']}")

    if pulse == 1:
      high += 1
    else:
      low += 1 
    if not module in network: # handle outputs
      continue
    operation, destinations = network[module] 
    match operation:
      case 'b':
        for destination in destinations:
          signals.append((destination,module,pulse))
      case '%':
        # Flip-flop modules (prefix %) are either on or off; they are initially off. 
        # If a flip-flop module receives a high pulse, it is ignored and nothing happens. 
        # However, if a flip-flop module receives a low pulse, it flips between on and off. 
        # If it was off, it turns on and sends a high pulse. 
        # If it was on, it turns off and sends a low pulse.
        if pulse == 1:
          continue
        else:
          state[module] = (state[module] + 1) % 2
          for destination in destinations:
            signals.append((destination,module,state[module]))
      case '&':
        # Conjunction modules (prefix &) remember the type of the most recent pulse received 
        # from each of their connected input modules; they initially default to remembering 
        # a low pulse for each input. When a pulse is received, the conjunction module 
        # first updates its memory for that input. Then, if it remembers high pulses for 
        # all inputs, it sends a low pulse; otherwise, it sends a high pulse.
        state[module][sender] = pulse
        if sum(state[module][s] for s in state[module]) == len(state[module]):
          for destination in destinations:
            signals.append((destination,module,0))
        else:
          for destination in destinations:
            signals.append((destination,module,1))
  
  return high,low,state
# Part 1
def _listOps1(network):
  # button is pressed 1000 times
  # button is only allowed to be pressed when network is stable
  # button sends low pulse to broadcast module
  button = 1000
  high_pulses = 0
  low_pulses = 0
  state = {}
  for key in network:
    mod,_ = network[key]
    if mod == '%':
      state.update({key:0})
    elif mod == '&':
      modules = list(
        filter(None, [k if key in ms else None for k in network for ms in network[k]]))
      state.update({key:{m:0 for m in modules}})

  store = {}
  state_key = _convert_to_frozenset(state)

  while button > 0:
    button -= 1
    if state_key in store:
      cycle = 1
      h, l, next_state_key = store[state_key]
      high = [h]
      low = [l]
      while state_key != next_state_key:
        cycle += 1
        h, l, next_state_key = store[state_key]
        high.append(h)
        low.append(l)
      high_pulses += sum(high)
      low_pulses += sum(low)
      while cycle <= button:
        button -= cycle
        high_pulses += sum(high)
        low_pulses += sum(low)
      i = 0
      while button > 0:
        button -= 1
        high_pulses += high[i]
        low_pulses += low[i]
        i += 1 % cycle

    else:
      next_state = state.copy()
      high, low, next_state = _pressButton(network,next_state)
      next_state_key = _convert_to_frozenset(next_state)
      store.update({state_key : (high,low,next_state_key)})
      state = next_state
      state_key = next_state_key
      high_pulses += high
      low_pulses += low
      
  return high_pulses * low_pulses
  
def _listOps2(network):
  # button is pressed 1000 times
  # button is only allowed to be pressed when network is stable
  # button sends low pulse to broadcast module
  button = 0
  high_pulses = 0
  low_pulses = 0
  state = {}
  for key in network:
    mod,_ = network[key]
    if mod == '%':
      state.update({key:0})
    elif mod == '&':
      modules = list(
        filter(None, [k if key in ms else None for k in network for ms in network[k]]))
      state.update({key:{m:0 for m in modules}})
  print("-"*20)
  rx = []
  m = 'rx'
  p = 0
  while len(rx) == 0:
    for key in network:
      op,modules = network[key]
      if m in modules:
        print(f"{key} : {modules} -> {key} states : {state[key]}")
        if op == '&':
          p = (p + 1) % 2
          rx.append(key)
        elif op == '%':
          p = (p + 1) % 2
          m = key 
          print("Flipflop module, ", m)
        else:
          pass
  print(rx)
  print(p)
  rx_input_state = {}

  while rx:
    button += 1
    _, _, state = _pressButton(network,state)
    for m in rx:
      if sum(x for _,x in state[m].items()) == len(state[m]):
        rx_input_state.update({m:button})
        print(f"{m} with state {state[m].items()}")
        rx.remove(m)
        # print(len(rx))  

  print(rx)
  print(rx_input_state)
  return 1


if __name__ == "__main__":
  func = _stringParsing
  parsed_input = parseWithFunction(func)
  network = {key : (mod,modules) for key, mod, modules in parsed_input}
  # print("Part 1: ", _listOps1(network))
  print("Part 2: ", _listOps2(network))
