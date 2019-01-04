#!/usr/bin/python3

from numpy.random import exponential
from numpy import mean, median, percentile, histogram, cumsum, max
from matplotlib import pyplot

NSAMPLES = 10000000

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
    return times

def cumulative_frequency(times, label, colour):
    # <https://stackoverflow.com/a/15419072/393146>
    # evaluate the histogram
    values, base = histogram(times, bins=100)
    # evaluate the cumulative
    cumulative = cumsum(values)*100/NSAMPLES
    # plot the cumulative function
    pyplot.plot(base[:-1], cumulative, c=colour, label=label)

def frequency(times, label, colour):
    values, base = histogram(times, bins=100)
    pyplot.plot(base[:-1], values/max(values), c=colour, label=label)


results = [
    (simulate(150, 10), 150, 10, 'blue'),
    (simulate( 75, 21),  75, 21, 'green'),
]

def show_graph(plotfn, subtitle):
    for (times, expectation, confirmations, colour) in results:
        plotfn(times, "%ds blocks, %d confirmations" % (expectation, confirmations), colour)

    pyplot.title("Confirmation time simulation (%s)" % (subtitle,))
    pyplot.legend()
    pyplot.show()

show_graph(cumulative_frequency, "cumulative frequency")
show_graph(frequency, "frequency, normalized")
