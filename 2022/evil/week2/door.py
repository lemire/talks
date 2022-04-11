import random

times = 1000000
hit = 0
for x in range(times):
   treasure = random.choice([1,2,3])
   mychoice = random.choice([1,2,3])
   if mychoice == treasure:
       hit += 1

print(hit / times)

hit = 0

for x in range(times):
   treasure = random.choice([1,2,3])
   mychoice = random.choice([1,2,3])
   if mychoice != treasure:
       hit += 1
print(hit / times)
