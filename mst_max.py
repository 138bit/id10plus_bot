from edge_list import edge_list, directed_edge
from mesh_gen import mesh_gen
import heapq
import math

class priority_queue:
    def __init__(self) -> None:
        self._queue = []
        heapq.heapify(self._queue)

    def get(self) -> directed_edge:
        entry = heapq.heappop(self._queue)
        return entry[1]

    def put(self, item: directed_edge) -> None:
        entry = [item._w, item]
        heapq.heappush(self._queue, entry)

    def print(self):
        x = 0
        for i in self._queue:
            print("       {0} -> ( {1} )".format(x, i[1]))
            x += 1
    
    def empty(self):
        return len(self._queue) == 0


class mst_max():
    """
        vertex 
    """
    def _visit(self, el: edge_list, u: int):
        for e in el._matrix[u]:
            v = e._v

            # print("    visit {0} {1} ({2})".format(u, v, e._w))
            # for min: use <
            if e._w > self._dist_to[v]:
                self._edge_to[v] = e
                self._dist_to[v] = e._w
                self._pq.put(e)

    def __init__(self, el: edge_list, s: int) -> None:
        self._pq = priority_queue()
        self._s = s
        self._Nm = el.size()

        self._edge_to = [ directed_edge ] * self._Nm

        # for min: use math.inf
        self._dist_to = [ -math.inf ] * self._Nm

         # Nothing goes to 0, because I'm already here
        self._edge_to[0] = directed_edge(0, 0, 0)

        self._visit(el, s)
        while not self._pq.empty():
            e = self._pq.get()
            v = e._v

            self._visit(el, v)

    def print(self) -> None:
        for i in self._edge_to:
            print(i)
    
    def __iter__(self):
        self._i = 1
        return self

    def __next__(self):
        if self._i >= self._Nm:
            raise StopIteration
        e = self._edge_to[self._i]
        self._i += 1
        return e


if __name__ == "__main__":
    matrix = [
        [    # 0
            directed_edge(0, 1,  4),
            directed_edge(0, 7,  8)
        ], [ # 1
            directed_edge(1, 2,  8),
            directed_edge(1, 7, 11)
        ], [ # 2
            directed_edge(2, 3,  7),
            directed_edge(2, 5,  4),
            directed_edge(2, 8,  2)
        ], [ # 3
            directed_edge(3, 4,  9),
            directed_edge(3, 5, 14)
        ], [ # 4
            directed_edge(4, 5, 10)
        ], [ # 5
            directed_edge(5, 6,  2)
        ], [ # 6
            directed_edge(6, 7,  1),
            directed_edge(6, 8,  6)
        ], [ # 7
            directed_edge(7, 8,  7)
        ], [ # 8

        ]
    ]

    el = edge_list(matrix)
    # el.print(el._matrix)
    el._matrix = matrix
    # el.print(el._matrix)
    pm = mst_max(el, 0)

    for e in pm:
        if e._u == 0:
            break
    print(e)