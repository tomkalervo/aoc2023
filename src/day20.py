import re,sys,math
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

def _get_default_state(network):
  state = {}
  for key in network:
    mod,_ = network[key]
    if mod == '%':
      state.update({key:0})
    elif mod == '&':
      modules = list(
        filter(None, [k if key in ms else None for k in network for ms in network[k]]))
      state.update({key:{m:0 for m in modules}})
  return state

# Part 1
def _listOps1(network):
  # button is pressed 1000 times
  # button is only allowed to be pressed when network is stable
  # button sends low pulse to broadcast module
  button = 1000
  high_pulses = 0
  low_pulses = 0
  state = _get_default_state(network)

  while button > 0:
    button -= 1
    high, low, state = _pressButton(network,state)
    high_pulses += high
    low_pulses += low
      
  return high_pulses * low_pulses
  
def _minClick(incoming,network,relations):
  module, pulse, x = incoming
  operand,_ = network[module]
  #basecase
  match operand: 
    case 'b':
      if pulse == 'low':
        return x
      else:
        return None
    case '%':
      values = []
      for input_module in relations[module]:
        value = _minClick((input_module,'low',x),network,relations)
        if value != None:
          values.append(value)
      values.sort()
      if not values:
        return None
      elif pulse == 'low':
        if values > 1:
          return min(values[0]+values[1], 2*values[0])
        else:
          return 2*values[0]
      else:
        return min(values)
      
    case '&':
      #This logic needs to handle the distance to the broadcaster ?
      if pulse == 'low':
        values = [_minClick((inpt,'high',1),network,relations) for inpt in relations[module]]
        if None in values:
          return None
        else:
          return x * math.lcm(*values)
      else:
        values = []
        for input_module in relations[module]:
          value = _minClick((input_module,pulse,x),network,relations)
          if value != None:
            values.append(value)

        values.sort()
        if not values:
          return None
        else:
          v = 0
          while x > 0:
            x -= 1
            v += values[0]
            values[0] *= 2
            values.sort()
          return v
  
  
def _listOps2(network):
  # button is pressed 1000 times
  # button is only allowed to be pressed when network is stable
  # button sends low pulse to broadcast module
  button = 0
  high_pulses = 0
  low_pulses = 0
  relations = {}
  for key in network: 
    # mod,_ = network[key]
    modules = list(
      filter(None, [k if key in ms else None for k in network for ms in network[k]]))
    relations.update({key:modules})
  output_key = 'rx'
  output_modules = []
  for key in network: #get relations to output
    _,modules = network[key]
    # print(modules)
    if output_key in modules:
      output_modules.append(key)
  relations.update({output_key:output_modules})
  print(network)
  print("-"*20)
  print(relations)

  p = 'low'
  for ms in relations[output_key]:
    print(f"min from {ms}: {_minClick((ms,p,1),network,relations)}")

  # _, _, state = _pressButton(network,_get_default_state(network))
  # print(state)
  return 1


if __name__ == "__main__":
  func = _stringParsing
  parsed_input = parseWithFunction(func)
  network = {key : (mod,modules) for key, mod, modules in parsed_input}
  # print("Part 1: ", _listOps1(network))
  print("Part 2: ", _listOps2(network))
