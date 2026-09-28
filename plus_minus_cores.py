"""
Print 800 "+" on one CPU core and 800 "-" on another core, in parallel.

Python threads share the Global Interpreter Lock (GIL), so two threads
never execute Python code at the same time. To really use two cores we
start two worker processes and pin each one to its own core with
os.sched_setaffinity (Linux only; on other systems pinning is skipped).
"""

import os
import sys
from multiprocessing import Process

COUNT = 800


def worker(symbol, core):
    """Pin the current process to `core` and print `symbol` COUNT times."""
    if hasattr(os, "sched_setaffinity"):
        os.sched_setaffinity(0, {core})
    for _ in range(COUNT):
        # Write + flush per character so the output of both cores interleaves.
        sys.stdout.write(symbol)
        sys.stdout.flush()


def pick_cores():
    """Return two distinct cores this process is allowed to run on."""
    if hasattr(os, "sched_getaffinity"):
        cores = sorted(os.sched_getaffinity(0))
    else:
        cores = list(range(os.cpu_count() or 1))
    if len(cores) < 2:
        sys.exit("Need at least two CPU cores.")
    return cores[0], cores[1]


if __name__ == "__main__":
    core_plus, core_minus = pick_cores()
    print(f'"+" on core {core_plus}, "-" on core {core_minus}')

    workers = [
        Process(target=worker, args=("+", core_plus)),
        Process(target=worker, args=("-", core_minus)),
    ]
    for p in workers:
        p.start()
    for p in workers:
        p.join()
    print()
