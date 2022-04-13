

def find_playables(peg):
    playables = []
    for r in range(len(peg)):
        for c in range(len(peg[0])):
            if peg[r][c] == 1:
                # search neighbor
                if (r > 1 and peg[r-1][c] == 1 and peg[r-2][c] == 0):
                    playables.append(((r,c),(r-2,c)))
                if (c > 1 and peg[r][c-1] == 1 and peg[r][c-2] == 0):
                    playables.append(((r,c),(r,c-2)))
                if (r+2 <len(peg) and peg[r+1][c] == 1 and peg[r+2][c] == 0):
                    playables.append(((r,c),(r+2,c)))
                if (c+2 <len(peg[0]) and peg[r][c+1] == 1 and peg[r][c+2] == 0):
                    playables.append(((r,c),(r,c+2)))
    return playables

import random

def prettyprint(peg):
    for row in peg:
        print(row)
    print()

def tryme():
    game = []
    peg = [[2,2,1,1,1,2,2],
           [2,2,1,1,1,2,2],
           [1,1,1,1,1,1,1],
           [1,1,1,0,1,1,1],
           [1,1,1,1,1,1,1],
           [2,2,1,1,1,2,2]]
    count = 0
    for r in range(len(peg)):
      for c in range(len(peg[0])):
          if peg[r][c] == 1:
              count += 1
    while count > 1:
        playables = find_playables(peg)
        if len(playables) == 0 :
            return False, game
        source, dest = random.choice(playables)
        game.append((source,dest))
        peg[source[0]][source[1]] = 0
        peg[(source[0]+dest[0])//2][(source[1]+dest[1])//2] = 0
        peg[dest[0]][dest[1]] = 1
        count -= 1
    return True, game

count = 0
result, g = tryme()
while(not result):
    count += 1
    if(count % 1000 ==0):print(count)
    result, g = tryme()

print(g)
