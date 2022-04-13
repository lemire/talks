seed = 1234

def random():
    global seed
    seed = seed * 0xda942042e4dd58b5
    value = seed >> 64
    value = seed % 2**64
    return value

for i in range(10):
    print(random())

for i in range(10):
    print(random()%3)

# D. H. Lehmer, Mathematical methods in large-scale computing units.
# Proceedings of a Second Symposium on Large Scale Digital Calculating
# Machinery;
# Annals of the Computation Laboratory, Harvard Univ. 26 (1951), pp. 141-146.
#
# P L'Ecuyer,  Tables of linear congruential generators of different sizes and
# good lattice structure. Mathematics of Computation of the American
# Mathematical
# Society 68.225 (1999): 249-260.