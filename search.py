import numpy as np
from copy import copy
from input import input_value, T_poly, T_start


(N, M) = (0, 0)


def _chech_matrix(i: int, j: int, matrix: np.ndarray) -> bool:
    if not matrix[i, j]:
        matrix[i, j] = True
        return True
    else:
        return False


def _packing_rec(start: T_start, index_poly: int, poly: T_poly, rotate: int, rec_polyominos: list[T_poly],
                 matrix: np.ndarray) -> bool:
    """Trying to put this rec-poly with this rotation on matrix"""
    (h, w), count = poly
    if rotate == 1:
        h, w = w, h
    if start[0] - h + 1 < 0 or start[1] + w - 1 >= N:  # check dimensions
        return False
    for i in range(start[0], start[0] - h, -1):  # trying to fill
        for j in range(start[1], start[1] + w):
            if not _chech_matrix(i, j, matrix):
                return False
    # delete this poly
    if count - 1 > 0:
        poly = (h, w), count - 1
        rec_polyominos[index_poly] = poly
    else:
        rec_polyominos.pop(index_poly)
    return True


def _rotate_arc_hor(start: T_start, poly: T_poly, matrix: np.ndarray, edge: int) -> bool:
    """Trying to put this arc-poly with horizontal rotation on matrix"""
    (h, w), count = poly
    if start[0] - h + 1 < 0 or start[1] + w - 1 >= N:  # check dimensions
        return False
    for i in range(start[0], start[0] - h, -1):  # trying to fill
        if i == edge:  # fill the 'roof'
            for j in range(start[1], start[1] + w):
                if not _chech_matrix(i, j, matrix):
                    return False
        else:  # fill the 'legs'
            for j in (start[1], start[1] + w - 1):
                if not _chech_matrix(i, j, matrix):
                    return False
    return True


def _rotate_arc_ver(start: T_start, poly: T_poly, matrix: np.ndarray, edge: int) -> bool:
    """Trying to put this arc-poly with vertical rotation on matrix"""
    (h, w), count = poly
    if start[0] - w + 1 < 0 or start[1] + h - 1 >= N:  # check dimensions
        return False
    for i in range(start[0], start[0] - w, -1):  # trying to fill with reversed (w, h)
        if i in (start[0], start[0] - w + 1):  # fill the 'legs'
            for j in range(start[1], start[1] + h):
                if not _chech_matrix(i, j, matrix):
                    return False
        else:
            j = edge  # fill the 'roof'
            if not _chech_matrix(i, j, matrix):
                return False
    return True


def _packing_arc(start: T_start, index_poly: int, poly: T_poly, rotate: int, arc_polyominos: list[T_poly],
                 matrix: np.ndarray) -> bool:
    """Trying to put this arc-poly with this rotation on matrix"""
    (h, w), count = poly
    result = False
    if rotate == 0:
        result = _rotate_arc_hor(start, poly, matrix, edge=start[0] - h + 1)
    elif rotate == 2:
        result = _rotate_arc_hor(start, poly, matrix, edge=start[0])
    elif rotate == 1:
        result = _rotate_arc_ver(start, poly, matrix, edge=start[1])
    elif rotate == 3:
        result = _rotate_arc_ver(start, poly, matrix, edge=start[1] + h - 1)
    else:
        assert 0  # can't be here
    if not result:
        return False
    # delete this poly
    if count - 1 > 0:
        poly = (h, w), count - 1
        arc_polyominos[index_poly] = poly
    else:
        arc_polyominos.pop(index_poly)
    return True


def _check_poly_arc(start: T_start, polyominos: list[T_poly], matrix: np.ndarray, rec_polyominos: list[T_poly]) -> bool:
    """Checking arc-polies what hadn't been packed"""
    for j, poly in enumerate(polyominos):
        for rotate in range(4):  # 0, 90, 180, 270 degrees
            cur_polyominos = copy(polyominos)
            cur_rec_polyominos = copy(rec_polyominos)
            cur_matrix = copy(matrix)
            if _packing_arc(start, j, poly, rotate, cur_polyominos, cur_matrix):
                # trying to search left polies in matrix with new-packed-poly
                result = _search(start, cur_matrix, cur_rec_polyominos, cur_polyominos)
                if result:
                    return True
    return False


def _check_poly_rec(start, polyominos, matrix, arc_polyominos) -> bool:
    """Checking rec-polies what hadn't been packed"""
    for j, poly in enumerate(polyominos):
        for rotate in range(2):  # horizontal + vertical
            cur_polyominos = copy(polyominos)
            cur_arc_polyominos = copy(arc_polyominos)
            cur_matrix = copy(matrix)
            if _packing_rec(start, j, poly, rotate, cur_polyominos, cur_matrix):
                # trying to search left polies in matrix with new-packed-poly
                result = _search(start, cur_matrix, cur_polyominos, cur_arc_polyominos)
                if result:
                    return True
    return False


def _check_polies(start: T_start, matrix: np.ndarray, rec: list[T_poly], arc: list[T_poly]) -> bool:
    """Checking rec- and arc- polies what hadn't been packed"""
    result = _check_poly_rec(start, rec, matrix, arc)
    if result:
        return True
    result = _check_poly_arc(start, arc, matrix, rec)
    if result:
        return True
    return False


def _search(start: T_start, matrix: np.ndarray, rec: list[T_poly], arc: list[T_poly]) -> bool:
    """Searching for start coordinates for every packed poly"""
    if not rec and not arc:  # exit when all poly is packed
        return True
    start_index = start[1]
    for i in range(start[0], -1, -1):
        for j in range(start_index, N):
            if matrix[i, j]: continue
            result = _check_polies((i, j), matrix, rec, arc)  # try to put next poly
            if result:
                return True
        start_index = 0
    return False


def search(d: tuple[int, int], rec_polyominos: list[T_poly], arc_polyominos: list[T_poly]) -> bool:
    global N, M
    N, M = d
    matrix = np.zeros(shape=(M, N), dtype=bool)
    result = _search((M - 1, 0), matrix, rec_polyominos, arc_polyominos)  # find first place from left bottom
    if result:
        return True
    return False


if __name__ == '__main__':
    by_shell = True
    answer = search(*input_value(by_shell))
    print('Result:', answer)
