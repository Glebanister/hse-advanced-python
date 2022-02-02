from examples.fib_naive import fib as fib_naive

memo = {}

def fib(n: int):
    if n not in memo:
        memo[n] = fib_naive(n, fib)
    return memo[n]

def fib_seq(n: int) -> list[int]:
    return list(map(fib, range(n)))
