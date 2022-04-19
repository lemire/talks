import math
v = float(input("What was the velocity of the throw? "))
angle = float(input("What was the angle of the throw? "))
g = 9.81
h = float(input("What was your intial height? "))

maxHeight = h + v*v * (math.sin(math.radians(angle)) * math.sin(math.radians(angle))) / (2 * g)
print("maxheight = ", maxHeight)