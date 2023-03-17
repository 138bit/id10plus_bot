class mesh_gen:

    def __init__(self, grid, N: int, radius: float, default: int, weight: int = 1) -> None:

    # def __init__(self, N: int, radius: float, default: int, weight: int = 1) -> None:
        self._N = N
        self._size = self._N * self._N
        yy = [ 0 ] * self._size
        xx = [ 0 ] * self._size
        self._matrix = grid
        cy = my = -(self._N // 2)
        rad = (radius * radius)
        """
        In example: self._size = 11*11, radius = (n/2)
        xx =
            -5  -4  -3  -2  -1   0   1   2   3   4   5
            -5  -4  -3  -2  -1   0   1   2   3   4   5
            -5  -4  -3  -2  -1   0   1   2   3   4   5
            -5  -4  -3  -2  -1   0   1   2   3   4   5
            -5  -4  -3  -2  -1   0   1   2   3   4   5
            -5  -4  -3  -2  -1   0   1   2   3   4   5
            -5  -4  -3  -2  -1   0   1   2   3   4   5
            -5  -4  -3  -2  -1   0   1   2   3   4   5
            -5  -4  -3  -2  -1   0   1   2   3   4   5
            -5  -4  -3  -2  -1   0   1   2   3   4   5
            -5  -4  -3  -2  -1   0   1   2   3   4   5

        yy =
            -5  -5  -5  -5  -5  -5  -5  -5  -5  -5  -5
            -4  -4  -4  -4  -4  -4  -4  -4  -4  -4  -4
            -3  -3  -3  -3  -3  -3  -3  -3  -3  -3  -3
            -2  -2  -2  -2  -2  -2  -2  -2  -2  -2  -2
            -1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1
             0   0   0   0   0   0   0   0   0   0   0
             1   1   1   1   1   1   1   1   1   1   1
             2   2   2   2   2   2   2   2   2   2   2
             3   3   3   3   3   3   3   3   3   3   3
             4   4   4   4   4   4   4   4   4   4   4
             5   5   5   5   5   5   5   5   5   5   5
        """

        for i in range(0, self._N):
            cx = my
            for j in range(i * self._N, (i + 1) * self._N):
                xx[j] = cx
                yy[j] = cy
                cx += 1
            cy += 1

        # self.print(xx)
        # self.print(yy)
        """
        In example: rad = 30, weight = -1
        xx.^2+yy.^2 =
            50   41   34   29   26   25   26   29   34   41   50
            41   32   25   20   17   16   17   20   25   32   41
            34   25   18   13   10    9   10   13   18   25   34
            29   20   13    8    5    4    5    8   13   20   29
            26   17   10    5    2    1    2    5   10   17   26
            25   16    9    4    1    0    1    4    9   16   25
            26   17   10    5    2    1    2    5   10   17   26
            29   20   13    8    5    4    5    8   13   20   29
            34   25   18   13   10    9   10   13   18   25   34
            41   32   25   20   17   16   17   20   25   32   41
            50   41   34   29   26   25   26   29   34   41   50

        (xx.^2+yy.^2)<a^2 = 
            0   0   1   1   1   1   1   1   1   0   0
            0   1   1   1   1   1   1   1   1   1   0
            1   1   1   1   1   1   1   1   1   1   1
            1   1   1   1   1   1   1   1   1   1   1
            1   1   1   1   1   1   1   1   1   1   1
            1   1   1   1   1   1   1   1   1   1   1
            1   1   1   1   1   1   1   1   1   1   1
            1   1   1   1   1   1   1   1   1   1   1
            1   1   1   1   1   1   1   1   1   1   1
            0   1   1   1   1   1   1   1   1   1   0
            0   0   1   1   1   1   1   1   1   0   0
        """

        for i in range(0, self._size):
            yy[i] = (xx[i] * xx[i]) + (yy[i] * yy[i])
            yy[i] = (yy[i] < rad) * weight

        # self.print(yy)
        
        for i in range(0, self._N):
            for j in range(i * self._N, (i + 1) * self._N):
                self._matrix[j] += yy[j] + default

    def print(self, matrix):
        for i in range(0, self._N):
            for j in range(i * self._N, (i + 1) * self._N):
                print("{:2d}".format(matrix[j]), end=' ')
            print("")
        print("")


if __name__ == "__main__":
    N = 11
    matrix = [ 10 ] * (N *N)
    mg = mesh_gen(matrix, N, N/3, -1, +1)
    mg.print(mg._matrix)
