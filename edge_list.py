import math
from mesh_gen import mesh_gen


class directed_edge:
    pass


class directed_edge:
    def __init__(self, u, v, w) -> None:
        self._u = u # from
        self._v = v # to
        self._w = w # weight

    def __lt__(self, other: directed_edge):
        return (self._w < other._w)
    
    def _gt_(self, other: directed_edge):
        return (self._w > other._w)

    def __le__(self, other: directed_edge):
        return self._w <= other._w

    def __ge__(self, other: directed_edge):
        return self._w >= other._w

    def __str__(self) -> str:
        return "{0:2d} -> {1:2d} = {2:2d}".format(self._u, self._v, self._w)
        # return "{0}".format(self._v)


class edge_list:
    def __init__(self, matrix: list = None) -> None:
        self._Nm = len(matrix)
        self._Nr = int(math.sqrt(self._Nm))
        self._matrix = [ [ directed_edge ] * 0 ] * self._Nm

        # print(self._matrix, self._Nm, self._Nr)

        for i in range(0, self._Nm):
            t = i - self._Nr
            b = i + self._Nr
            l = i - 1
            r = i + 1

            self._matrix[i] = []

            # if i == 1:
            #     print(t, b, l, r)
            #     print(
            #         t >= 0,
            #         b < self._Nm,
            #         (l % self._Nr) != 0 and l >= 0 or l == 0,
            #         (i % self._Nr) != 0 and r < self._Nm)

            if t >= 0:
                self._matrix[i].append(directed_edge(i, t, matrix[t]))

            if b < self._Nm:
                self._matrix[i].append(directed_edge(i, b, matrix[b]))

            if (i % self._Nr) != 0 and l >= 0 or l == 0:
                self._matrix[i].append(directed_edge(i, l, matrix[l]))

            if (r % self._Nr) != 0 and r < self._Nm:
                self._matrix[i].append(directed_edge(i, r, matrix[r]))
            
    def size(self) -> int:
        return self._Nm

    def print(self, matrix):
        for i in range(0, self._Nm):
            array = matrix[i]

            print("----------{:2d}: ".format(i), end=' ')
            for a in array:
                print("{0}".format(a), end=' ')
            print("")


if __name__ == "__main__":
    N = 11
    matrix = [ 10 ] * (N *N)
    mg = mesh_gen(matrix, N, N/3, -1, +1)
    mg.print(mg._matrix)
    el = edge_list(mg._matrix)
    el.print(el._matrix)  