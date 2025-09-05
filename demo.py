import itertools

import numpy as np

from qsatlib.numbers import UIntBinary, IntBinary


def vectorise(x):
    return sum([2 ** i * x[i] for i in range(len(x))])


def check_clifford(state: np.ndarray):
    n = state.ndim
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    y_ids = list(range(len(pairs)))
    a_ids = list(range(len(pairs), len(pairs) + n))
    b_ids = list(range(len(pairs) + n, len(pairs) + 2 * n))
    c_ids = list(range(len(pairs) + 2 * n, len(pairs) + 3 * n))
    d_ids = list(range(len(pairs) + 3 * n, len(pairs) + 4 * n))
    state_terms = [[([], [])] for _ in range(2 ** n)]
    for e, (i, j) in enumerate(pairs):
        for x in itertools.product(range(2), repeat=n):
            if x[i] == x[j] == 1:
                state_terms[vectorise(x)][0][1].append((2, y_ids[e]))

    for gate, ids in [('S', a_ids), ('H', b_ids), ('S', c_ids), ('H', d_ids)]:
        for i in range(n):
            if gate == 'S':
                for x in itertools.product(range(2), repeat=n):
                    for amp, phase in state_terms[vectorise(x)]:
                        if x[i] == 1:
                            phase.append((1, ids[i]))
            elif gate == 'H':
                new_state_terms = [[] for _ in range(2 ** n)]
                for x in itertools.product(range(2), repeat=n):
                    x1 = list(x)
                    x1[i] = 1 - x1[i]
                    for amp, phase in state_terms[vectorise(x1)]:
                        new_state_terms[vectorise(x)].append((amp + [ids[i]], phase.copy()))
                for x in itertools.product(range(2), repeat=n):
                    for amp, phase in state_terms[vectorise(x)]:
                        if x[i] == 1:
                            phase.append((2, ids[i]))
                    state_terms[vectorise(x)] += new_state_terms[vectorise(x)]

    y_vars = [UIntBinary(1) for _ in range(len(y_ids))]
    a_vars = [UIntBinary(2) for _ in range(len(a_ids))]
    b_vars = [UIntBinary(1) for _ in range(len(b_ids))]
    c_vars = [UIntBinary(2) for _ in range(len(c_ids))]
    d_vars = [UIntBinary(1) for _ in range(len(d_ids))]
    for x in itertools.product(range(2), repeat=n):
        elem_real = IntBinary(5).value(0)
        elem_imag = IntBinary(5).value(0)
        for amp, phase in state_terms[vectorise(x)]:
            total_amp = UIntBinary(1).value(1)
            for var_id in amp:
                if var_id in b_ids:
                    total_amp = total_amp & b_vars[b_ids.index(var_id)]
                elif var_id in d_ids:
                    total_amp = total_amp & d_vars[d_ids.index(var_id)]
                else:
                    raise ValueError(f'Unknown amplitude variable {var_id}')
            total_phase = UIntBinary(2).value(0)
            for coef, var_id in phase:
                if var_id in y_ids:
                    total_phase = total_phase + y_vars[y_ids.index(var_id)] * coef
                elif var_id in a_ids:
                    total_phase = total_phase + a_vars[a_ids.index(var_id)] * coef
                elif var_id in b_ids:
                    total_phase = total_phase + b_vars[b_ids.index(var_id)] * coef
                elif var_id in c_ids:
                    total_phase = total_phase + c_vars[c_ids.index(var_id)] * coef
                elif var_id in d_ids:
                    total_phase = total_phase + d_vars[d_ids.index(var_id)] * coef
                else:
                    raise ValueError(f'Unknown phase variable {var_id}')
            elem_real = elem_real + ~(total_phase & 1) * total_amp * (1 - total_phase & 2)
            elem_imag = elem_imag + (total_phase & 1) * total_amp * (1 - total_phase & 2)
            scale_factor_sq = 2 ** (n + sum(b_vars, UIntBinary(4).value(0)) + sum(d_vars, UIntBinary(4).value(0)))


    return state_terms


