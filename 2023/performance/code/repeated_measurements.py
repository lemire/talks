import numpy as np #pip3 install numpy
from scipy.stats import norm #pip3 install scipy 


mu, sigma = 10000, 5000
for N in range(20, 2000+1):
    s = [sum(np.random.default_rng().normal(mu, sigma, N))/N for i in range(30)]
    print(N,np.std(s))