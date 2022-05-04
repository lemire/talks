number_of_rows = 20
number_of_columns = 50

UP=1
DOWN=2
LEFT=4
RIGHT=8

def generate_row(direction):
    r = [ LEFT | RIGHT for col in range(number_of_columns) ]
    if direction == RIGHT:
        r[0] = DOWN | RIGHT
        r[number_of_columns -1] = LEFT | UP
    elif direction == LEFT:
        r[0] = RIGHT | UP
        r[number_of_columns - 1] = LEFT | DOWN
    return r

array = []
for row in range(number_of_rows):
    if (row & 1) == 0:
        array.append(generate_row(LEFT))
    else:
        array.append(generate_row(RIGHT))



character = [' ' for i in range(16)]
character[LEFT] = '╴'
character[RIGHT] = '╶'
character[UP] = '╵'
character[DOWN] = '╷'

character[UP|RIGHT] = '└'
character[UP|LEFT] = '┘'
character[DOWN|RIGHT] = '┌'
character[DOWN|LEFT] = '┐'
character[UP|DOWN] = '│'
character[LEFT|RIGHT] = '─'

character[LEFT|RIGHT|UP] = '┴'
character[LEFT|RIGHT|DOWN] = '┬'
character[RIGHT|DOWN|UP] = '├'
character[LEFT|DOWN|UP] = '┤'

character[LEFT|RIGHT|DOWN|UP] = '┼'

def print_map(array):
    for row in array:
        print("".join([character[x] for x in row]))
print("====")
print_map(array)


print("====")
array[0][0] = RIGHT

dangling = [(0,0)]

if (number_of_rows & 1) == 0:
    array[number_of_rows-1][0] = RIGHT
    dangling.append((number_of_rows-1,0))
else:
    array[number_of_rows-1][number_of_columns-1] = LEFT
    dangling.append((number_of_rows-1,number_of_columns-1))

print_map(array)

move = {
    LEFT : (0,-1),
    RIGHT : (0,1),
    UP : (-1,0),
    DOWN : (1,0),
}

opposite = {
    UP : DOWN,
    DOWN : UP,
    LEFT : RIGHT,
    RIGHT : LEFT,
}

import random

def disconnect(startpoint, endpoint, direction):
    p = startpoint
    m = move[direction]
    p = (p[0]+m[0], p[1]+m[1])
    while p != endpoint:
        direction = array[p[0]][p[1]] ^ opposite[direction]
        m = move[direction]
        p = (p[0]+m[0], p[1]+m[1])
    array[p[0]][p[1]] ^= opposite[direction]
    array[p[0]-m[0]][p[1]-m[1]] ^= direction
    return (p[0]-m[0], p[1]-m[1])



def modify():
    pick = random.choice([0,1])
    x,y =  dangling[pick]
    value = array[x][y]
    # We connect it to a neighbour.
    # First identify the possibilities.
    possibilities = []
    if x < number_of_rows - 1 and value != DOWN:
        possibilities.append(DOWN)
    if x > 0 and value != UP:
        possibilities.append(UP)
    if y < number_of_columns - 1 and value != RIGHT:
        possibilities.append(RIGHT)
    if y > 0 and value != LEFT:
        possibilities.append(LEFT)
    newdirection = random.choice(possibilities)
    initial_direction = array[x][y]
    array[x][y] = newdirection | initial_direction
    m = move[newdirection]
    newpointer = (x+m[0],y+m[1])
    array[x+m[0]][y+m[1]] |= opposite[newdirection]
    dangling[pick] = disconnect((x,y), newpointer, initial_direction)


total = number_of_rows*number_of_columns*100
onepercent = total // 100
if onepercent == 0:
    onepercent = 1
for i in range(total):
    if  i % onepercent == 0:
        print(".", end="", flush=True)
    modify()
print()
print_map(array)
