import numpy
import scipy
import collections
from collections import Counter
from scipy.stats import norm
from scipy.stats import expon
import matplotlib.pyplot as plt

n = 10 
p = 0.5

s = numpy.random.binomial(n, p, 340)

print(Counter(s))
print("----------------------------------------------------------------------------")

def poisson_density(mean):
	return lambda x: mean**x * exp(-mean) / factorial(x)

mean = 1
stdD = 0.0035

rej = norm.cdf((1-stdD), loc = 1, scale = 0.002)
rej += 1 - norm.cdf((1+stdD), loc = 1, scale = 0.002)

print(rej)


print("----------------------------------------------------------------------------")


#cdf(x, loc=0, scale=1)
#pdf = lambda * exp(-lambda * x)




#print(scipy.stats.expon.cdf(1, loc = 0, scale = 1))









