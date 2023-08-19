from solver import *


def test_m_plus_m_equals_n():
    n = UnaryUnsigned(num_bits=4)
    m = UnaryUnsigned(num_bits=4)
    formula = forall(n, exists(m, UnaryUnsigned.a_plus_b_is_c(m, m, n)))
    assert brute_force_solve(formula) is False


def test_
