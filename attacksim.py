#!/usr/bin/python3

from numpy.random import exponential
from matplotlib import pyplot
from collections import deque
from multiprocessing import Pool, cpu_count
import sys

PROCESSES = cpu_count()

NTRIALS = 200000

BLOCKTIME = 150.0  # for each alg
CONFIRMATIONS = 21
ALTERNATING_CONFIRMATIONS = 10
THRESHOLD = 5
GROUP = 6


def debug(*args):
    if PROCESSES == 1:
        print(*args)
    else:
        sys.stderr.write('.')
        sys.stderr.flush()

def simulate_parallel(manipulation_advantage, adv_share_A, adv_share_B):
    debug("manipulation_advantage  =", manipulation_advantage)
    debug("adv_share_A             =", adv_share_A)
    debug("adv_share_B             =", adv_share_B)

    adv_successes = deque()
    for (blocktime_A, blocktime_B) in [(BLOCKTIME*manipulation_advantage, BLOCKTIME),
                                       (BLOCKTIME, BLOCKTIME*manipulation_advantage)]:
        honest_share_A = 1.0-adv_share_A
        honest_share_B = 1.0-adv_share_B
        honest_blocktimes = [blocktime_A/honest_share_A, blocktime_B/honest_share_B]
        adv_blocktimes    = [blocktime_A/adv_share_A,    blocktime_B/adv_share_B]

        adv_wins = 0
        for i in range(NTRIALS):
            honest_time = parallel_trial(honest_blocktimes, CONFIRMATIONS)
            adv_time    = parallel_trial(adv_blocktimes,    CONFIRMATIONS)

            if adv_time < honest_time:
                adv_wins += 1

        adv_successes.append(adv_wins/NTRIALS)

    adv_success = max(adv_successes)
    debug("parallel PoW success    =", adv_success)
    debug()
    return adv_success

def parallel_trial(effective_blocktimes, confirmations):
    total_time = 0
    history = deque()
    for i in range(confirmations):
        blocktimes = [exponential(e) for e in effective_blocktimes]

        if history.count(0) >= THRESHOLD:
            alg = 1
        elif history.count(1) >= THRESHOLD:
            alg = 0
        else:
            alg = 0 if blocktimes[0] < blocktimes[1] else 1

        total_time += blocktimes[alg]
        history.append(alg)

        if len(history) >= GROUP:
            history.popleft()

    return total_time

def simulate_alternating(manipulation_advantage, adv_share_A, adv_share_B):
    debug("manipulation_advantage  =", manipulation_advantage)
    debug("adv_share_A             =", adv_share_A)
    debug("adv_share_B             =", adv_share_B)

    adv_successes = deque()
    for (blocktime_A, blocktime_B) in [(BLOCKTIME/2.0*manipulation_advantage, BLOCKTIME/2.0),
                                       (BLOCKTIME/2.0, BLOCKTIME/2.0*manipulation_advantage)]:
        honest_share_A = 1.0-adv_share_A
        honest_share_B = 1.0-adv_share_B
        honest_blocktime_A = blocktime_A/honest_share_A
        honest_blocktime_B = blocktime_B/honest_share_B
        adv_blocktime_A = blocktime_A/adv_share_A
        adv_blocktime_B = blocktime_B/adv_share_B

        adv_wins = 0
        for i in range(NTRIALS):
            honest_time = (sum(exponential(honest_blocktime_A, ALTERNATING_CONFIRMATIONS)) +
                           sum(exponential(honest_blocktime_B, ALTERNATING_CONFIRMATIONS)))
            adv_time    = (sum(exponential(adv_blocktime_A, ALTERNATING_CONFIRMATIONS)) +
                           sum(exponential(adv_blocktime_B, ALTERNATING_CONFIRMATIONS)))

            if adv_time < honest_time:
                adv_wins += 1

        adv_successes.append(adv_wins/NTRIALS)

    adv_success = max(adv_successes)
    debug("alternating PoW success =", adv_success)
    debug()
    return adv_success

def simulate_single(adv_share, confirmations):
    debug("adv_share               =", adv_share)
    debug("confirmations           =", confirmations)

    honest_share = 1.0-adv_share
    honest_blocktime = BLOCKTIME/2.0/honest_share
    adv_blocktime = BLOCKTIME/2.0/adv_share

    adv_wins = 0
    for i in range(NTRIALS):
        honest_time = sum(exponential(honest_blocktime, confirmations))
        adv_time    = sum(exponential(adv_blocktime, confirmations))

        if adv_time < honest_time:
            adv_wins += 1

    adv_success = adv_wins/NTRIALS
    debug("single PoW success      =", adv_success)
    debug()
    return adv_success


def plot_all():
    print("Using %d processes." % (PROCESSES,))
    pool = Pool(processes=PROCESSES)

    adv_share_A_range = [a/200.0 for a in range(1, 101)]
    adv_share_B_range = [b/10.0 for b in range(5, 10)]
    manipulation_advantage = 1.0

    def plot(adv_share_B):
        parallel_results    = pool.starmap(simulate_parallel,
                                           [(manipulation_advantage, adv_share_A, adv_share_B)
                                            for adv_share_A in adv_share_A_range])
        alternating_results = pool.starmap(simulate_alternating,
                                           [(manipulation_advantage, adv_share_A, adv_share_B)
                                            for adv_share_A in adv_share_A_range])

        pyplot.plot(adv_share_A_range, parallel_results,    label="adv_share_B=%f parallel" % (adv_share_B,))
        pyplot.plot(adv_share_A_range, alternating_results, label="adv_share_B=%f alternating" % (adv_share_B,))

    for confirmations in (10, CONFIRMATIONS):
        single_results = pool.starmap(simulate_single,
                                      [(adv_share_A, confirmations) for adv_share_A in adv_share_A_range])
        pyplot.plot(adv_share_A_range, single_results, label="single PoW %d conf" % (confirmations,))

    for adv_share_B in adv_share_B_range:
        plot(adv_share_B)

    pyplot.axis((0.0, 0.5, 0.0, 0.5))
    pyplot.legend()
    pyplot.show()

plot_all()
