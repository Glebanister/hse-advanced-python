import operator

from enum import Enum
from typing import TypeVar, Iterable, Optional, Dict
from functools import reduce
from itertools import zip_longest


class Parenthesis(Enum):
    round = ('(', ')')
    curly = ('{', '}')
    square = ('[', ']')

    def embrace(self, s: str) -> str:
        return self.value[0] + s + self.value[1]


def in_parent(a: str, parent_type: Parenthesis):
    return parent_type.embrace(a)


def lines(*args: str) -> str:
    return '\n'.join([*args])


T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')


def intercalate(a: Iterable[T], b: Iterable[T]) -> Iterable[T]:
    return filter(
        lambda x: x is not None,
        reduce(operator.add, zip_longest(a, b))
    )


def remove_null_keys(d: Dict[K, Optional[V]]) -> Dict[K, V]:
    return dict(filter(lambda entry: entry[1] is not None, d.items()))
