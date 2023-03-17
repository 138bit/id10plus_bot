import random
import numpy as np
from ..bot_control import Move

import math
import heapq

class mesh_gen:

    def __init__(self, grid, N: int, radius: float, default: int, weight: int = 1) -> None:
        # print("{} {} {} {}".format(N, radius, default, weight))

        self._N = N
        self._size = self._N * self._N
        yy = [ 0 ] * self._size
        xx = [ 0 ] * self._size
        self._matrix = grid
        cy = my = -(self._N // 2)
        rad = (radius * radius)

        for i in range(0, self._N):
            cx = my
            for j in range(i * self._N, (i + 1) * self._N):
                xx[j] = cx
                yy[j] = cy
                cx += 1
            cy += 1

        for i in range(0, self._size):
            yy[i] = (xx[i] * xx[i]) + (yy[i] * yy[i])
            yy[i] = (yy[i] < rad) * weight

        for i in range(0, self._N):
            for j in range(i * self._N, (i + 1) * self._N):
                self._matrix[j] += yy[j] + default
        
    def __str__(self):
        s = ""
        for i in range(0, self._N):
            for j in range(i * self._N, (i + 1) * self._N):
                s += "{:2d} ".format(self._matrix[j])
            s += "\n"
        return s


class directed_edge:
    pass


class directed_edge:
    def __init__(self, u, v, w) -> None:
        # print("{} {} {}".format(u, v, w))
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
    
    def __str__(self,):
        s = ""
        for i in range(0, self._Nm):
            array = self._matrix[i]

            s += "----------{:2d}: ".format(i)
            for a in array:
                s += "{0} ".format(a)
            s += "\n"
        return s


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
            if e._w < self._dist_to[v]:
                self._edge_to[v] = e
                self._dist_to[v] = e._w
                self._pq.put(e)

    def __init__(self, el: edge_list, s: int) -> None:
        self._pq = priority_queue()
        self._s = s
        self._Nm = el.size()

        self._edge_to = [ directed_edge ] * self._Nm

        # for min: use math.inf
        self._dist_to = [ math.inf ] * self._Nm

         # Nothing goes to 0, because I'm already here
        self._edge_to[0] = directed_edge(0, 0, 0)

        self._visit(el, s)
        while not self._pq.empty():
            e = self._pq.get()
            v = e._v

            self._visit(el, v)

    def __str__(self) -> str:
        s = ""
        for i in self._edge_to:
            s += str(i) + "\n"
        return s
    
    def __iter__(self):
        self._i = 1
        return self

    def __next__(self):
        if self._i >= self._Nm:
            raise StopIteration
        e = self._edge_to[self._i]
        self._i += 1
        return e


"""
Notes:
    grid = [
        [0 0 0 0 0 0 0 0]
        [0 0 0 0 0 0 0 0]
        [0 0 0 0 0 0 0 0]
        [0 0 0 0 0 0 0 0]
        [0 0 0 0 0 0 0 0]
        [0 0 0 0 0 0 0 0]
        [0 0 0 0 0 0 0 0]
        [0 0 0 0 0 0 0 0]
    ]

"""

class id10plus_bot:

    def __init__(self):
        self.target = None
        self.last_edge = None

    def get_name(self):
        return "ID10+ BOT"

    def get_contributor(self):
        return "Nobleo"

    def determine_next_move(self, grid, enemies, game_info):
        x = self.position[0]
        y = self.position[1]

        # print(x, y, game_info.grid_size)
        # print(grid)
        # print(enemies)
        # print(game_info)
        # exit(0)

        p = x + (y * game_info.grid_size)

        # Copy grid due to different matrix implementation
        # g = np.copy(grid[0])
        l = len(grid[0])
        g = [ 0 ] * int(math.pow(l, 2))
        for y in range(0, l):
            for x in range(0, l):
                g[(y * l) + x] = grid[y][x]
                i = (y * l) + x
                # print(self.last_edge)
                if self.last_edge is not None and self.last_edge._u == i:
                    # print(self.last_edge, i)
                    g[i] = 99
 
        # mg = mesh_gen(g, game_info.grid_size, game_info.grid_size / 3, 1, -1)
        mg = mesh_gen(g, game_info.grid_size, game_info.grid_size / 3, -1, +1)
        el = edge_list(mg._matrix)
        mm = mst_max(el, p)

        for e in mm:
            if e._u == p:
                self.last_edge = e
                break
        
        # MST says "use e". How to anticipate on...

        if p - game_info.grid_size == e._v:
            move = Move.DOWN # UP in my graph
        if p + game_info.grid_size == e._v:
            move = Move.UP # Down in my graph
        if p - 1 == e._v:
            move = Move.LEFT
        if p + 1 == e._v:
            move = Move.RIGHT

        # move = Move.STAY

        if game_info.current_round == game_info.number_of_rounds:
            print(mg)
            # print(mm)
            print(enemies)
            t = len(str(p))
            for y in range(0, l):
                for x in range(0, l):
                    s = "{:0" + str(t) + "d}"
                    print(s.format((y * l) + x), end=' ')
                print("\n")

        print(move, p, e, self.position, grid.shape[0], game_info.grid_size)
        return move