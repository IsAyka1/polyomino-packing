import numpy as np
from copy import copy

(N, M) = (0, 0)

def input_value_by_shell():
    print('Input NxM: ', end='')
    global N, M
    N, M = map(int, input().split())
    print('Input count of rectangular polyominos: ', end='')
    count_rec = int(input())
    print('Input rectangular polyominos (height, weight, count) : ', end='')
    rec_polyominos = []
    for _ in range(count_rec):
        h, w, count = map(int, input().split())
        rec_polyominos.append(((h, w), count))
    print('Input count of П-polyominos: ', end='')
    count_arc = int(input())
    print('Input П-polyominos (height, weight, count) : ', end='')
    arc_polyominos = []
    for _ in range(count_arc):
        h, w, count = map(int, input().split())
        arc_polyominos.append(((h, w), count))
    return (N, M), rec_polyominos, arc_polyominos


def input_value(by_shell):
    if by_shell:
        return input_value_by_shell()
    else:
        global N, M
        (N, M) = (4, 6)
        rec_polyominos = [((3, 2), 1), ((1, 1), 1)]
        arc_polyominos = [((3, 4), 2)]
        return rec_polyominos, arc_polyominos


def _packing_rec(start, index_poly, poly: tuple, rotate, rec_polyominos, matrix):
    (h, w), count = poly
    if rotate == 1:
        h, w = w, h
    if start[0] - h + 1 < 0 or start[1] + w - 1 >= N:
        return False
    for i in range(start[0], start[0] - h, -1):
        for j in range(start[1], start[1] + w):
            if not matrix[i, j]:
                matrix[i, j] = 1  # TODO True
            else:
                return False
    if count - 1 > 0:
        poly = (h, w), count - 1
        rec_polyominos[index_poly] = poly
    else:
        rec_polyominos.pop(index_poly)
    return True


def _rotate_arc_hor(start, poly: tuple, matrix, edge):
    (h, w), count = poly
    if start[0] - h + 1 < 0 or start[1] + w - 1 >= N:
        return False
    for i in range(start[0], start[0] - h, -1):
        if i == edge:
            for j in range(start[1], start[1] + w):
                if not matrix[i, j]:
                    matrix[i, j] = 2  # TODO True
                else:
                    return False
        else:
            for j in (start[1], start[1] + w - 1):
                if not matrix[i, j]:
                    matrix[i, j] = 2  # TODO True
                else:
                    return False
    return True

def _rotate_arc_ver(start, poly: tuple, matrix, edge):
    (h, w), count = poly
    if start[0] - w + 1 < 0 or start[1] + h - 1 >= N:
        return False
    for i in range(start[0], start[0] - w, -1):
        if i in (start[0], start[0] - w + 1):
            for j in range(start[1], start[1] + h):
                if not matrix[i, j]:
                    matrix[i, j] = 2  # TODO True
                else:
                    return False
        else:
            j = edge
            if not matrix[i, j]:
                matrix[i, j] = 2  # TODO True
            else:
                return False
    return True



def _packing_arc(start, index_poly, poly: tuple, rotate, arc_polyominos, matrix):
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
        assert 0
    if not result:
        return False
    if count - 1 > 0:
        poly = (h, w), count - 1
        arc_polyominos[index_poly] = poly
    else:
        arc_polyominos.pop(index_poly)
    return True


def _check_poly_arc(start, polyominos, matrix, rec_polyominos):
    for j, poly in enumerate(polyominos):
        for rotate in range(4):
            cur_polyominos = copy(polyominos)
            cur_rec_polyominos = copy(rec_polyominos)
            cur_matrix = copy(matrix)
            if _packing_arc(start, j, poly, rotate, cur_polyominos, cur_matrix):
                new_start = (start[0], start[1] + 1) if start[1] < N else (start[0] - 1, 0)
                result = _search(new_start, cur_matrix, cur_rec_polyominos, cur_polyominos)
                if result:
                    return True
    return False

def _check_poly_rec(start, polyominos, matrix, arc_polyominos):
    for j, poly in enumerate(polyominos):
        for rotate in range(2):
            cur_polyominos = copy(polyominos)
            cur_arc_polyominos = copy(arc_polyominos)
            cur_matrix = copy(matrix)
            if _packing_rec(start, j, poly, rotate, cur_polyominos, cur_matrix):
                new_start = (start[0], start[1] + 1) if start[1] < N else (start[0] - 1, 0)
                result = _search(new_start, cur_matrix, cur_polyominos, cur_arc_polyominos)
                if result:
                    return True
    return False

def _check_polies(start, matrix, rec, arc):
    result = _check_poly_rec(start, rec, matrix, arc)
    if result:
        return True
    result = _check_poly_arc(start, arc, matrix, rec)
    if result:
        return True
    return False


def _search(start, matrix, rec, arc):
    if not rec and not arc:
        print(matrix)
        return True
    if start[0] < 0:
        return False
    start_index = start[1]
    for i in range(start[0], -1, -1):
        for j in range(start_index, N):
            if matrix[i, j]: continue
            result = _check_polies((i, j), matrix, rec, arc)
            if result:
                return True
        start_index = 0
    return False


def search(rec_polyominos, arc_polyominos):
    matrix = np.zeros(shape=(M, N), dtype=int)
    for i in range(M - 1, -1, -1):  # go from bottom
        for j in range(N):
            result = _search((i, j), matrix, rec_polyominos, arc_polyominos)
            if result:
                return True
    return False



if __name__ == '__main__':
    by_shell = False
    rec, arc = input_value(by_shell)
    answer = search(rec, arc)
    print(answer)
