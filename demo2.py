from qsatlib.numbers import *
import time


p, q = UInt(25), UInt(25)
n = 243948295914941
formula = exist(p, q, (p > 1) & (q > 1) & (p * q == n))
t0 = time.time()
print(formula.pcnf().eval())
t1 = time.time()
print(f'elapsed time: {t1 - t0:.2f} sec')

# formula = forall(a, b, exist_unique(c, c == a * b))
# # formula = forall(c, c == c + c) != exist(a, a == a + a)
# # formula = exist_unique(c, c == 2 * c)
# # print(len(formula.pcnf().quantifiers))
# print(formula)
# pnf = formula.pnf()
# print(pnf)
# print(pnf2pcnf(pnf))
# assert formula.pcnf().eval()
