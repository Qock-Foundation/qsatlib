from cvc5.pythonic import *
# from z3 import *


x, y, z = Ints('x y z')
solve(x * x * x + y * y * y + z * z * z == 8)
