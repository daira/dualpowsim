#!/usr/bin/python3

import os, sys
from collections import deque

THRESHOLD = 5
GROUP = 6


def flip():
    return os.urandom(1)[0] & 1

def sim(count):
    history = deque()
    forced = 0

    for i in range(count):
        if history.count(0) >= THRESHOLD:
            forced += 1
            history.append(1)
        elif history.count(1) >= THRESHOLD:
            forced += 1
            history.append(0)
        else:
            history.append(flip())

        if len(history) >= GROUP:
            history.popleft()

    return forced


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 dualpowsim.py COUNT")
    else:
        print(sim(int(sys.argv[1])))
