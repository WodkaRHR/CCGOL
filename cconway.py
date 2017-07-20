import math, random
import numpy as np

A = 10
P = 4
_B = [3]
_D = [2, 3]
DISTANCE = "euclid"
_distances = {
    "euclid" : (lambda x0, y0, x1, y1: math.sqrt(math.pow(x0 - x1, 2) + math.pow(y0 - y1, 2))),
    "average" : (lambda x0, y0, x1, y1: (abs(x0 - x1) + abs(y0 - y1)) / 2),
    "max" : (lambda x0, y0, x1, y1: max(abs(x0 - x1), abs(y0 - y1))) 
}


def polynomial_functor(roots):
    """ Functor to create a pol. function a*(1-(1/(1 + (x-ri))))"""
    def f(x):
        r = A
        for root in roots:
            r *= 1 - 1 / (1 + math.pow(abs(x - root), P))
        return r
    return f

def _b(f):
    """ Best birth rate at field = 3 """
    return polynomial_functor(_B)(f)

def _d(f):
    """ Cell survives best at 2 or 3 neighbours """
    return polynomial_functor(_D)(f)



class CGrid:
    """ Continuous grid"""
    def __init__(self, width, height, b=_b, d=_d, xrange=2, yrange=2, borders_connected=True):
        """ b(f) (birth rate) and d(f) (durability function) are polynomial
        functions depending on the strength of the surrounding field
        xrange, yrange defines how many neighbours are creating a field for a cell"""
        self.width = width
        self.height = height
        self.reset()
        self.b = b
        self.d = d
        self.xrange = xrange
        self.yrange = yrange
        self.borders_connected = borders_connected

    def reset(self):
        """ Resets the cells to 0.0 """
        self.cells = [[0 for x in range(self.width)] for y in range(self.height)]

    def random(self):
        """ Creates a random cell distribution"""
        self.cells = [[random.uniform(0, 1) for x in range(self.width)] for y in range(self.height)]

    def _distance(self, x0, y0, x1, y1):
        """ Calculates the distance between two points"""
        return _distances[DISTANCE](x0, y0, x1, y1)


    def _iter_field(self):
        """ O(n^2 * xrange * yrange) iteration of the entire field """
        self.field = [[0 for x in range(self.width)] for y in range(self.height)]
        for y, x, j, i in np.ndindex(self.height, self.width, 1 + self.yrange * 2, 1 + self.xrange * 2):
            dx = i - self.xrange
            dy = j - self.yrange
            x1 = x - dx
            y1 = y - dy
            if dx == 0 and dy == 0: continue #Cell does not induce its own field
            d = self._distance(x, y, x1, y1)
            self.field[y][x] += self.get_cell(x1, y1) / math.pow(d, 2)# * self.CONST

    def print_field(self):
        print(self.field)

    def set_A(self, a):
        """ Sets A to a value """
        global A
        A = a
    
    def set_P(self, p):
        """ Sets P to a value """
        global P
        P = p

    def get_cell(self, x, y):
        if self.borders_connected:
            x = x % self.width
            y = y % self.height
        if x in range(self.width) and y in range(self.height):
            return self.cells[y][x]
        return 0

    def iter_cells(self):
        """ Iterate all cells """
        self._iter_field()
        for y in range(self.height):
            for x in range(self.width):
                c_last = self.get_cell(x, y)
                f = self.field[y][x]
                self.cells[y][x] = 1 / (1 + self.b(f) * math.pow(1 - c_last, 1) + self.d(f) * math.pow(c_last, 1))


    def set_DISTANCE(self, distance):
        """ Changes the distance method """
        global DISTANCE
        DISTANCE = distance


        