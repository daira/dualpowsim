#!/usr/bin/python3

from numpy.random import exponential
from numpy import mean, median, percentile, histogram, cumsum
from matplotlib import pyplot

NSAMPLES = 1000000

def simulate(expectation, confirmations, colour):
    print(expectation, confirmations, colour)
    times = [sum(exponential(expectation, confirmations)) for i in range(NSAMPLES)]

    experimental_mean   = mean(times)
    experimental_median = median(times)
    experimental_99pc   = percentile(times, 99)

    print(experimental_mean)
    print(experimental_median)
    print(experimental_99pc)
    print()

    # <https://stackoverflow.com/a/15419072/393146>
    # evaluate the histogram
    values, base = histogram(times, bins=100)
    # evaluate the cumulative
    cumulative = cumsum(values)*100/NSAMPLES
    # plot the cumulative function
    pyplot.plot(base[:-1], cumulative, c=colour, label="%d %d" % (expectation, confirmations))

simulate(150, 10, 'blue')
simulate(75, 21, 'green')

pyplot.title("Confirmation time simulation")
pyplot.legend()
pyplot.show()

