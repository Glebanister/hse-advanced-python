#!/usr/bin/env python3

import os
import time
import math
import functools

from concurrent.futures import ProcessPoolExecutor
from typing import Callable, TypeVar, Tuple, Iterable


def range_incl_end(a: float, b: float, step: float) -> Iterable[float]:
    x = a
    while x < b:
        yield x
        x += step
    yield b


def segments(a: float, b: float, step: float) -> Iterable[Tuple[float, float]]:
    points = list(range_incl_end(a, b, step))
    return zip(points, points[1:])


def integrate(
    function: Callable[[float], float],
    step: float,
    log: bool,
    range: Tuple[float, float]
) -> float:
    if log:
        print(f'\t process={os.getpid()}: {range=}, {step=}')
    r_begin, r_end = range
    if r_begin == r_end:
        return 0
    assert r_begin <= r_end
    res = 0.0
    for s_begin, s_end in segments(r_begin, r_end, step):
        res += function(s_begin) * (s_end - s_begin)
    return res


def integrate_with_process_pool(
    function: Callable[[float], float],
    range: Tuple[float, float],
    pool_size: int = 1,
    iterations: int = 100,
    log: bool = True
) -> float:
    r_begin, r_end = range
    step = (r_end - r_begin) / pool_size

    if log:
        print(
            f'integrate with process pool on interval {range}, {pool_size=}, {iterations=}'
        )

    partial_integrate = functools.partial(
        integrate,
        function, (r_end - r_begin) / iterations, log
    )

    with ProcessPoolExecutor(max_workers=pool_size) as executor:
        return sum(executor.map(partial_integrate, segments(r_begin, r_end, step)))


def main():
    with open('artifacts/medium_compare.txt', 'w') as measurements_file:
        for pool_size in range(1, 20):
            start_time = time.time()
            for _ in range(3):
                integrate_with_process_pool(
                    math.cos,
                    (0, math.pi / 2),
                    pool_size=pool_size,
                    iterations=200000,
                    log=False
                )
            print(f'{pool_size=}, time={str(time.time() - start_time)}',
                  file=measurements_file)


if __name__ == '__main__':
    main()
