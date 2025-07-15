import numpy as np #pip3 install numpy
from scipy.stats import norm #pip3 install scipy 

minimums = []
averages = []
medians = []

for N in range(1,10):
    data = [np.random.default_rng().lognormal(1, 4, N) for i in range(30)]
    #print(np.min(data), np.mean(data), np.median(data), np.max(data))
    minimums.append(np.min(data))
    averages.append(np.mean(data))
    medians.append(np.median(data))

print(np.std(minimums), np.std(averages), np.std(medians))