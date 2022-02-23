import numpy as np
import operator

from matrix import Matrix
from mixins_matrix import MixinsMatrix
from pathlib import Path


def dump_if_correct(cls, np_a: np.ndarray, np_b: np.ndarray, operator, task: str, op_as_str: str):
    a = cls.from_ndarray(np_a)
    b = cls.from_ndarray(np_b)
    a_op_b: cls = operator(a, b)
    np_a_op_b: np.ndarray = operator(np_a, np_b)

    assert cls.from_ndarray(np_a_op_b) == a_op_b

    a_op_b.dump(Path('artifacts') / task / f'matrix{op_as_str}.txt')


if __name__ == '__main__':
    np.random.seed(0)

    np_a = np.random.randint(0, 10, (10, 10))
    np_b = np.random.randint(0, 10, (10, 10))

    dump_if_correct(Matrix, np_a, np_b, operator.add, 'easy', '+')
    dump_if_correct(Matrix, np_a, np_b, operator.mul, 'easy', '*')
    dump_if_correct(Matrix, np_a, np_b, operator.matmul, 'easy', '@')

    dump_if_correct(MixinsMatrix, np_a, np_b, operator.add, 'medium', '+')
    dump_if_correct(MixinsMatrix, np_a, np_b, operator.sub, 'medium', '-')
    dump_if_correct(MixinsMatrix, np_a, np_b, operator.mul, 'medium', '*')
    dump_if_correct(MixinsMatrix, np_a, np_b, operator.matmul, 'medium', '@')
    dump_if_correct(MixinsMatrix, np_a, np_b, operator.lshift, 'medium', '>>')
    dump_if_correct(MixinsMatrix, np_a, np_b, operator.rshift, 'medium', '<<')
    dump_if_correct(MixinsMatrix, np_a, np_b, operator.and_, 'medium', '&')
    dump_if_correct(MixinsMatrix, np_a, np_b, operator.or_, 'medium', '|')
    dump_if_correct(MixinsMatrix, np_a, np_b, operator.xor, 'medium', '^')
