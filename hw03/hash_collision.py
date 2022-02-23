from matrix import Matrix
from pathlib import Path
import numpy as np





if __name__ == '__main__':
    shape = (3, 3)
    np.random.seed(0)

    root = Path('artifacts') / 'hard'

    def mat_path(m):
        return root / f'{m}.txt'

    def dump_hash(**kwargs):
        with (root / 'hash.txt').open('w') as f:
            f.write(str(dict(**kwargs)))

    while True:
        A, B, C, D = [Matrix.from_ndarray(np.random.randint(0, 10, shape)) for _ in range(4)]

        AB = A @ B
        CD = C @ D

        if (hash(A) == hash(C)) and (A != C) and (B == D) and (AB != CD):
            A.dump(mat_path('A'))
            B.dump(mat_path('B'))
            C.dump(mat_path('C'))
            D.dump(mat_path('D'))
            AB.dump(mat_path('AB'))
            CD.dump(mat_path('CD'))
            dump_hash(AB=hash(AB), CD=hash(CD))
            break