def fib(n: int, next_fib = None):
    if next_fib is None:
        next_fib = fib
    if n <= 1:
        return 1
    return next_fib(n - 1) + next_fib(n - 2)
