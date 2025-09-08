from qsatlib.integers import *
import time

p, q = UInt(25), UInt(25)
n = 368986894403417
# n = 243948295914941
formula = exist(p, q, (p > 1) & (q > 1) & (p * q == n))

t0 = time.time()
print(formula.eval())
t1 = time.time()
print(f'elapsed time: {t1 - t0:.2f} sec')
