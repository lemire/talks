from z3 import *
# pip3 install z3-solver

# Jacques et Françoise
# Jackie et John
# Serge et Jane
# Simone et Yves

s = Solver()
jacques = Int("jacques")
francoise = Int("francoise")

jackie = Int("jackie")
john = Int("john")

serge = Int("serge")
jane = Int("jane")

simone = Int("simone")
yves = Int("yves")

s.add(jacques - francoise != 1)
s.add(jacques - francoise != -1)

s.add(jackie - john != 1)
s.add(jackie - john != -1)

s.add(serge - jane != 1)
s.add(serge - jane != -1)


s.add(simone - yves != 1)
s.add(simone - yves != -1)

s.add(jacques >= 1)
s.add(francoise >= 1)
s.add(jackie >= 1)
s.add(john >= 1)
s.add(serge >= 1)
s.add(jane >= 1)
s.add(simone >= 1)
s.add(yves >= 1)

s.add(jacques <= 8)
s.add(francoise <= 8)
s.add(jackie <= 8)
s.add(john <= 8)
s.add(serge <= 8)
s.add(jane <= 8)
s.add(simone <= 8)
s.add(yves <= 8)

s.add(jacques % 2 == 0)
s.add(francoise % 2 == 1)
s.add(jackie % 2 == 1)
s.add(john % 2 == 0)
s.add(serge % 2 == 0)
s.add(jane % 2 == 1)
s.add(simone % 2 == 1)
s.add(yves % 2 == 0)

s.add(jacques != francoise)
s.add(jacques != jackie)
s.add(jacques != john)
s.add(jacques != serge)
s.add(jacques != jane)
s.add(jacques != simone)
s.add(jacques != yves)

s.add(francoise != jackie)
s.add(francoise != john)
s.add(francoise != serge)
s.add(francoise != jane)
s.add(francoise != simone)
s.add(francoise != yves)

s.add(jackie != john)
s.add(jackie != serge)
s.add(jackie != jane)
s.add(jackie != simone)
s.add(jackie != yves)

s.add(john != serge)
s.add(john != jane)
s.add(john != simone)
s.add(john != yves)

s.add(serge != jane)
s.add(serge != simone)
s.add(serge != yves)

s.add(jane != simone)
s.add(jane != yves)

s.add(jane != simone)


s.add(simone == 1)
s.add(jacques == 8)

if(s.check() == z3.sat):
    m = s.model()
    print(m)