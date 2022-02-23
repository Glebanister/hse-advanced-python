import numpy as np
import operator

from typing import List, TypeVar, Tuple, Callable
from pathlib import Path


class MatrixLikeHashMixin:
    def __hash__(self) -> int:
        n_rows, n_cols = self.shape
        mn, mx = min(n_rows, n_cols), max(n_rows, n_cols)
        shape_hash = mx * 10 ** len(str(mn)) + mn
        values_hash = 0

        for i in range(n_rows):
            for j in range(n_cols):
                values_hash *= hash(self[i, j]) + (i ^ j) * 13 + 19
                values_hash %= MatrixLikeHashMixin._VALUES_HASH_MODULO
                if values_hash == 0:
                    values_hash = hash(self[i, j]) + i ^ j + 1013

        return int(str(shape_hash) + str(values_hash))

    @property
    def n_rows(self):
        return self.shape[0]

    @property
    def n_cols(self):
        return self.shape[1]

    def __eq__(self, other) -> bool:
        if self.shape != other.shape:
            return False
        n_rows, n_cols = self.shape
        for i in range(n_rows):
            for j in range(n_cols):
                if self[i, j] != other[i, j]:
                    return False
        return True


T = TypeVar('T')


class Matrix(MatrixLikeHashMixin):
    MATMUL_CACHE = {}

    @classmethod
    def from_ndarray(cls, rows: np.ndarray):
        ndarray_shape = rows.shape
        if len(ndarray_shape) != 2:
            raise Exception('Numpy array must have shape of lenth 2')
        return cls(list(map(list, rows)))

    @classmethod
    def of_value(cls, value: T, shape: Tuple[int, int]):
        if shape[0] < 0 or shape[1] < 0:
            raise Exception('Matrix shape must have non-negative values')
        return cls([[value for _ in range(shape[1])] for _ in range(shape[0])])

    @classmethod
    def zeros(cls, shape: Tuple[int, int]):
        return cls.of_value(0, shape)

    @classmethod
    def ones(cls, shape: Tuple[int, int]):
        return cls.of_value(1, shape)

    def __init__(self, rows: List[List[T]]):
        self._rows: List[List[T]] = rows
        self._n_rows: int = len(rows)
        self._n_cols: int = 0 if rows == [] else len(rows[0])

        all_same_len = all(
            map(lambda row: len(row) == self._n_cols, self._rows))
        if not all_same_len:
            raise Exception('All rows should have same length')

    def __getitem__(self, key: Tuple[int, int]) -> T:
        return self._rows[key[0]][key[1]]

    def __setitem__(self, key: Tuple[int, int], value: T):
        self._rows[key[0]][key[1]] = value

    @property
    def shape(self):
        return (self._n_rows, self._n_cols)

    @property
    def value(self):
        return np.array(self._rows)

    def ewise_apply(self, other, func: Callable[[[int, int], T, T], None]):
        if self.shape != other.shape:
            raise Exception('Shapes must match for an element-wise operation')
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                func((i, j), self[i, j], other[i, j])

    def ewise_binop(self, other, binop: Callable[[T, T], T]):
        result = Matrix.zeros(self.shape)

        def set_result(key, a, b):
            result[key] = binop(a, b)

        self.ewise_apply(other, set_result)
        return result

    def dump(self, file: Path):
        with file.open('w') as out:
            out.write(repr(self))

    def __ne__(self, other) -> bool:
        return not self == other

    def __add__(self, other):
        return self.ewise_binop(other, operator.add)

    def __mul__(self, other):
        return self.ewise_binop(other, operator.mul)

    def __matmul__(self, other):
        if self.n_cols != other.n_rows:
            raise Exception(
                'ncols of left operand must match nrows of right operand')

        cache_key = (hash(self), hash(other))

        if cache_key not in Matrix.MATMUL_CACHE:
            result = Matrix.zeros((self.n_rows, other.n_cols))
            for i in range(result.shape[0]):
                for j in range(result.shape[1]):
                    for k in range(self.n_cols):
                        result[i, j] += self[i, k] * other[k, j]
            Matrix.MATMUL_CACHE[cache_key] = result

        return Matrix.MATMUL_CACHE[cache_key]

    def __repr__(self) -> str:
        return f'Matrix({repr(self._rows)})'
