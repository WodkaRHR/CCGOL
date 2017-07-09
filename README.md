This is an extension to Conway's Game Of Life, called Continuous Conway's Game Of Life.

The main difference is that instead of discrete transition functions everything now is defined on a
continouous number scale which causes a higher computation time for an iteration.

A cell can now store any number from the intervall [0; 1] and thus every cell creates a continuous field
depending on its own intensity. At any point x', y' in the cell the field created by the cell x, y
with an intensity of i equals i / sqrt((x-x')^2 + (y - y')^2) which simply is - like many scalar fields
in our world proportional to 1/d^2 where d equals the distance between two points. Thus all cells create
a scalar field that is spread over the entire grid and simply can be summed since the principle of
superposition is applied to CCGOL. However - for the sake of lower computation time - only a certain
range of cells is taken under consideration when calculating the field at any position x, y. This range
can be modified and equals by default 2 in any direction. This is justified since the field induced by
cells further away almost has no significance for the value of a scalar field f.

To iterate the entire grid from generation n to generation n+1 each cell is iterated independently. The
state of a cell at x,y at generation n+1 depends on the magnitude fn of the scalar field f at x,y at
generation n as well as the value of the cell cn at generation n. The state of the cell cn+1 at generation
n+1 can then be described by this formula: cn+1 = 1 / ( 1 + ( cn * d(fn) + (1 - cn) * b(fn) ) )
d(f) represents a function that describes the durability or ability of a cell with a value near to 1
to survive, so that when d(f) = 0 the cell survives best (meaning its value will converge towards 1) and the 
greater d(f) the less more near the value of the cell will converge to 0. Analogously b(f) describes the ability
of a cell with a value near to 0 to be born so that b(f) = 0 induces a high magnitude near 1 for the cell.
These functions can be interpreted as the birth and survival rules of Conway's Game of Life: A dead cell
(meaning its value is near 0) can be born when it has excactly 3 neighbours or in the case of CCGOL has a field
with magnitude near 3. A living cell (meaning its value is near 1) only survives when it has exaclty 2 or 3
living neighbours or in case of CCGOL has a field with magnitude near 2 or 3. Considering this defintion the
roots of the functions should describe the amount of neighbours a cell needs to be born or to survive.
Each function is of this form: A * ( B(f, r1) * B(f, r2) * ... * B (f, rn) ) where r1, r2, ..., rn
are all roots of the function. A defines a spectrum of values the function will take for more or less variety in
the cell values. B(f, ri) is defined as 1 - 1 / ( 1 + (f - ri)^P ) so that it produces a root for f = ri. P
can be identified as the exponent of each root so that for higher values of P the continuous functions for
b and d tend to become more and more like their discrete inspirations.