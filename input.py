
T_poly = tuple[tuple[int, int], int]
T_start = tuple[int, int]


def _input_value_by_shell() -> tuple[T_start, list[T_poly], list[T_poly]]:
    print('Input NxM: ', end='')
    N, M = map(int, input().split())

    print('Input count of different rectangular polyominos: ', end='')
    count_rec = int(input())
    rec_polyominos = []
    for _ in range(count_rec):
        print('Input rectangular polyominos (height, weight, count): ', end='')
        h, w, count = map(int, input().split())
        rec_polyominos.append(((h, w), count))

    print('Input count of different П-polyominos: ', end='')
    count_arc = int(input())
    arc_polyominos = []
    for _ in range(count_arc):
        print('Input П-polyominos (height, weight, count): ', end='')
        h, w, count = map(int, input().split())
        arc_polyominos.append(((h, w), count))

    return (N, M), rec_polyominos, arc_polyominos


def input_value(by_shell: bool) -> tuple[T_start, list[T_poly], list[T_poly]]:
    if by_shell:
        return _input_value_by_shell()
    else:
        (N, M) = (4, 6)
        rec_polyominos = [((3, 2), 1), ((1, 1), 1)]
        arc_polyominos = [((3, 4), 2)]
        return (N, M), rec_polyominos, arc_polyominos
