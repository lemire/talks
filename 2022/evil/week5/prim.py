number_of_rows = 25
number_of_columns = 80

UNVISITED = 0
UP = 1
DOWN = 2
LEFT = 4
RIGHT = 8

array = [[UNVISITED for i in range(number_of_columns)] for j in range(number_of_rows)]
import random

initial_location = (random.randint(0,number_of_rows-1), random.randint(0,number_of_columns-1))

removable = []

def add_removable_walls(location):
    if(location[0] > 0):
        if(array[location[0] - 1][location[1]] == UNVISITED):
            removable.append((location,UP))
    if(location[0] < number_of_rows - 1):
        if(array[location[0] + 1][location[1]] == UNVISITED):
            removable.append((location,DOWN))
    if(location[1] > 0):
        if(array[location[0]][location[1]-1] == UNVISITED):
            removable.append((location,LEFT))
    if(location[1] < number_of_columns - 1):
        if(array[location[0]][location[1]+1] == UNVISITED):
            removable.append((location,RIGHT))

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
add_removable_walls(initial_location)

room, direction = random.choice(removable)
removable.remove((room, direction))
m = move[direction]
target = (room[0]+m[0], room[1]+m[1])
array[initial_location[0]][initial_location[1]] |= direction
array[target[0]][target[1]] |= opposite[direction]
add_removable_walls(target)

while (len(removable)>0):
    room, direction = random.choice(removable)
    removable.remove((room, direction))
    # check that it is still a good choice
    m = move[direction]
    target = (room[0]+m[0], room[1]+m[1])
    if array[target[0]][target[1]] != UNVISITED:
        continue
    array[room[0]][room[1]] |= direction
    array[target[0]][target[1]] |= opposite[direction]
    add_removable_walls(target)

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

wall_array = [[UP|DOWN|LEFT|RIGHT for i in range(1+number_of_columns)] for j in range(1+number_of_rows)]
for r in range(0,number_of_rows+1):
    wall_array[r][0] ^= LEFT
    wall_array[r][number_of_columns] ^= RIGHT

for c in range(0,number_of_columns+1):
    wall_array[0][c] ^= UP
    wall_array[number_of_rows][c] ^= DOWN


def print_map(array):
    for row in array:
        print("".join([character[x] for x in row]))

print_map(array)

def in_range(r,c):
    return r>=0 and c >=0 and r < number_of_rows and c < number_of_columns

for r in range(number_of_rows+1):
    for c in range(number_of_columns+1):
        if in_range(r,c):
            if (array[r][c] & UP) == UP :
                wall_array[r][c] &= ~RIGHT
            if (array[r][c] & LEFT) == LEFT :
                wall_array[r][c] &= ~DOWN
        if in_range(r-1,c-1):
            if (array[r-1][c-1] & DOWN) == DOWN :
                wall_array[r][c] &= ~LEFT
            if (array[r-1][c-1] & RIGHT) == RIGHT :
                wall_array[r][c] &= ~UP
        if in_range(r-1,c):
            if (array[r-1][c] & DOWN) == DOWN :
                wall_array[r][c] &= ~RIGHT
            if (array[r-1][c] & LEFT) == LEFT :
                wall_array[r][c] &= ~UP
        if in_range(r,c-1):
            if (array[r][c-1] & UP) == UP :
                wall_array[r][c] &= ~LEFT
            if (array[r][c-1] & RIGHT) == RIGHT :
                wall_array[r][c] &= ~DOWN


print_map(wall_array)