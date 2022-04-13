from z3 import *
# pip3 install z3-solver

s = Solver()
a = BitVec('seed', 128)
s.add(LShR(a*0xda942042e4dd58b5,64) == 0x01020304050607)
if(s.check() == z3.sat):
    m = s.model()
    print(m[a])