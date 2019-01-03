#!/usr/bin/python3

from numpy.random import exponential
from numpy import mean, median, percentile

NSAMPLES = 1000000

def simulate(expectation, confirmations):
    print(expectation, confirmations)
    times = [sum(exponential(expectation, confirmations)) for i in range(NSAMPLES)]

    experimental_mean   = mean(times)
    experimental_median = median(times)
    experimental_99pc   = percentile(times, 99)

    print(experimental_mean)
    print(experimental_median)
    print(experimental_99pc)
    print()

simulate(150, 10)
simulate(75, 21)

