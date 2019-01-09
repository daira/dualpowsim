#!/usr/bin/python3

from numpy.random import exponential
from numpy import histogram, mean
from matplotlib import pyplot

# Plot the sampled probability density function of an exponential distribution.

SAMPLES = 10000000

def plot_exponential(expectation):
    distribution = exponential(expectation, SAMPLES)

    values, base = histogram(distribution, bins=100)
    pyplot.plot(base[:-1], values/max(values))
    pyplot.title("mean = %f, expectation = %f" % (mean(distribution), expectation))
    pyplot.show()

plot_exponential(1.0)
plot_exponential(10.0)
