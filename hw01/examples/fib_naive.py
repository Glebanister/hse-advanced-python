def fib(n: int, next_fib = None) -> int:
    if next_fib is None:
        next_fib = fib
    if n <= 1:
        return 1
    return next_fib(n - 1) + next_fib(n - 2)

def fib_seq(n: int) -> list[int]:
    return [fib(n) for _ in range(n)]
