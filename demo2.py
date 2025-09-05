from qsatlib.numbers import *
import time


p, q = UInt(20), UInt(20)
n = 368774110723
formula = exist(p, q, (p > 1) & (q > 1) & (p * q == n))
print(formula.pcnf().eval())
# print(f'elapsed time: {t1 - t0:.2f} sec')

# formula = forall(a, b, exist_unique(c, c == a * b))
# # formula = forall(c, c == c + c) != exist(a, a == a + a)
# # formula = exist_unique(c, c == 2 * c)
# # print(len(formula.pcnf().quantifiers))
# print(formula)
# pnf = formula.pnf()
# print(pnf)
# print(pnf2pcnf(pnf))
# assert formula.pcnf().eval()
