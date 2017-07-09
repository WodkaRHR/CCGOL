import math, random
import numpy as np

A = 10
P = 4
_B = [3]
_D = [2, 3]
<<<<<<< HEAD
=======
DISTANCE = "euclid"
_distances = {
    "euclid" : (lambda x0, y0, x1, y1: math.sqrt(math.pow(x0 - x1, 2) + math.pow(y0 - y1, 2))),
    "average" : (lambda x0, y0, x1, y1: (abs(x0 - x1) + abs(y0 - y1)) / 2),
    "max" : (lambda x0, y0, x1, y1: max(abs(x0 - x1), abs(y0 - y1))) 
}

>>>>>>> 42bca687494647403ca3e87d2b452d881be3620d

def polynomial_functor(roots):
    """ Functor to create a pol. function a*(1-(1/(1 + (x-ri))))"""
    def f(x):
        r = A
        for root in roots:
            r *= 1 - 1 / (1 + math.pow(x - root, P))
        return r
    return f

<<<<<<< HEAD
1   def _b(f):
=======
def _b(f):
>>>>>>> 42bca687494647403ca3e87d2b452d881be3620d
    """ Best birth rate at field = 3 """
    return polynomial_functor(_B)(f)

def _d(f):
    """ Cell survives best at 2 or 3 neighbours """
    return polynomial_functor(_D)(f)

class CGrid:
    """ Continuous grid"""
<<<<<<< HEAD
    def __init__(self, width, height, b=_b, d=_d, f=None, xrange=2, yrange=2):
        """ b(f) (birth rate) and d(f) (durability function) are polynomial
        functions depending on the strength of the surrounding field
        xrange, yrange defines how many neighbours are creating a field for a cell"""
        if not f: f = self._field
        self.width = width
        self.height = height
        self.reset()
        self.f = f #default field function
=======
    def __init__(self, width, height, b=_b, d=_d, xrange=2, yrange=2):
        """ b(f) (birth rate) and d(f) (durability function) are polynomial
        functions depending on the strength of the surrounding field
        xrange, yrange defines how many neighbours are creating a field for a cell"""
        self.width = width
        self.height = height
        self.reset()
>>>>>>> 42bca687494647403ca3e87d2b452d881be3620d
        self.b = b
        self.d = d
        self.xrange = xrange
        self.yrange = yrange
        self.CONST = 1 / (xrange + yrange) 

    def reset(self):
        """ Resets the cells to 0.0 """
        self.cells = [[0 for x in range(self.width)] for y in range(self.height)]

    def random(self):
        """ Creates a random cell distribution"""
        self.cells = [[random.uniform(0, 1) for x in range(self.width)] for y in range(self.height)]

    def _distance(self, x0, y0, x1, y1):
        """ Calculates the distance between two points"""
<<<<<<< HEAD
        dx, dy = x1 - x0, y1 - y0
        return math.sqrt(dx*dx + dy*dy)
=======
        return _distances[DISTANCE](x0, y0, x1, y1)
>>>>>>> 42bca687494647403ca3e87d2b452d881be3620d


    def _iter_field(self):
        """ O(n^2 * xrange * yrange) iteration of the entire field """
        self.field = [[0 for x in range(self.width)] for y in range(self.height)]
        for y, x, j, i in np.ndindex(self.height, self.width, 1 + self.yrange * 2, 1 + self.xrange * 2):
            dx = i - self.xrange
            dy = j - self.yrange
            x1 = x - dx
            y1 = y - dy
            if dx == 0 and dy == 0: continue #Cell does not induce its own field
            if x1 in range(self.width) and y1 in range(self.height):
                d = self._distance(x, y, x1, y1)
                self.field[y][x] += self.cells[y1][x1] / math.pow(d, 2)# * self.CONST

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

    def iter_cells(self):
        """ Iterate all cells """
        self._iter_field()
        for y in range(self.height):
            for x in range(self.width):
                c_last = self.cells[y][x]
                f = self.field[y][x]
                self.cells[y][x] = 1 / (1 + self.b(f) * math.pow(1 - c_last, 1) + self.d(f) * math.pow(c_last, 1))

<<<<<<< HEAD
=======
    def set_DISTANCE(self, distance):
        """ Changes the distance method """
        global DISTANCE
        DISTANCE = distance

>>>>>>> 42bca687494647403ca3e87d2b452d881be3620d

        