from qsatlib.integers import *
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns
import time

def factorise_naive(r):
    p = 2
    while p * p <= r:
        if r % p == 0:
            return True
        p += 1
    return False

rs = [11, 47, 163, 349, 1811, 7649, 15973, 77513, 768811,
      1097321, 4319563, 53808061, 223798567, 846927583,
      1725033083, 5246251471, 34019378677, 167651825359, 976960715333,
      3722859635531, 7345868902831, 52567644508517, 205580802858421, 632484200566909]
# rs = [9, 35, 143, 713, 1219, 5141, 45113, 155011, 511493,
#       2375959, 13651849, 34611131, 116109443, 502627757,
#       1606978957, 6108426551, 28646845079, 101444118511, 255937255061]
ns = range(2, 26)
data_qsatlib = {'log N': [], 'time': []}
data_naive = {'log N': [], 'time': []}
for n in tqdm(ns):
    p, q = UInt(n), UInt(n)
    r = rs[n - 2]
    for _ in range(1):
        t0 = time.time()
        if exist(p, q, (p > 1) & (q > 1) & (p * q == r)).eval():
            print(n)
            assert False
        t1 = time.time()
        data_qsatlib['log N'].append(2 * n)
        data_qsatlib['time'].append(t1 - t0)
    t0 = time.time()
    assert not factorise_naive(r)
    t1 = time.time()
    data_naive['log N'].append(2 * n)
    data_naive['time'].append(t1 - t0)

sns.pointplot(data_qsatlib, x='log N', y='time', label='qsatlib', log_scale=True)
sns.pointplot(data_naive, x='log N', y='time', label='naive', color='black', log_scale=True)
plt.legend()
plt.show()
