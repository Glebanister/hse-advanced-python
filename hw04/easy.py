#!/usr/bin/env python3

import time

from multiprocessing import Process
from threading import Thread


class Measurement:
    def __init__(self, out, name):
        self.out = out
        self.name = name
        self.start = None
        self.finish = None

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, type, value, traceback):
        self.finish = time.time()
        print(f'{self.name} time: {str(self.finish - self.start)} s', file=self.out)


def fibonacci(n):
    res = [0, 1]
    while len(res) < n:
        res.append(res[-1] + res[-2])
    return res[:n]


if __name__ == '__main__':
    n = 100000

    with open('artifacts/easy.txt', 'w') as measurements_file:
        with Measurement(measurements_file, 'sync'):
            for _ in range(10):
                fibonacci(n)

        with Measurement(measurements_file, 'threads'):
            threads = [Thread(target=fibonacci, args=(n,)) for _ in range(10)]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()

        with Measurement(measurements_file, 'process'):
            processes = [Process(target=fibonacci, args=(n,)) for _ in range(10)]
            for process in processes:
                process.start()
            for process in processes:
                process.join()
