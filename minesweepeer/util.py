from typing import List, Tuple


def build_adj_list(x, y) -> List[Tuple[int, int]]:
    return [
        ((x + 1), (y)),
        ((x), (y + 1)),
        ((x + 1), (y + 1)),
        ((x - 1), (y)),
        ((x), (y - 1)),
        ((x - 1), (y - 1)),
        ((x + 1), (y - 1)),
        ((x - 1), (y + 1)),
    ]
