import random


import math
def minimum(array):
    answer = math.inf
    for v in array:
        if v < answer:
            answer = v
    if answer == math.inf:
        answer = 0
    return answer

def construct():
  state = [[5,4,3,2,1], [],  []]
  steps = 0
  while True:
    start = random.choice([0,1,2])
    if len(state[start]) == 0:
        continue
    end = random.choice([0,1,2])
    startvalue = minimum(state[start])
    endvalue = minimum(state[end])
    if endvalue != 0 and startvalue > endvalue:
        continue
    state[start].remove(startvalue)
    state[end].append(startvalue)
    steps = steps + 1 
    if len(state[2]) == 5:
        break
  return steps

print(construct())
