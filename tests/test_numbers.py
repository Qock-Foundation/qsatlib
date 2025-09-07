from qsatlib.numbers import *


def test_uint_add_unique():
    a, b, c = UInt(5), UInt(5), UInt(6)
    assert forall(a, b, exist_unique(c, c == a + b)).eval()


def test_uint_add_overflow():
    a, b, c = UInt(5), UInt(5), UInt(5)
    assert not forall(a, b, exist(c, c == a + b)).eval()


def test_uint_add_inplace():
    a, b = UInt(5), UInt(5)
    c = a
    c += b
    assert exist(a, b, (a > 0) & (b > 0) & (c == 0)).eval()


def test_uint_add_zero():
    a = UInt(5)
    assert forall(a, a + 0 == a).eval()


def test_uint_add_commutativity():
    a, b = UInt(5), UInt(5)
    assert forall(a, b, a + b == b + a).eval()


def test_uint_add_associativity():
    a, b, c = UInt(5), UInt(5), UInt(5)
    assert forall(a, b, c, (a + b) + c == a + (b + c)).eval()


def test_uint_add_misc():
    a, b, c = UInt(5), UInt(5), UInt(5)
    assert forall(a, b, (a < b) | exist_unique(c, a == b + c)).eval()


def test_uint_add_parity():
    a, b = UInt(5), UInt(5)
    assert forall(a, exist_unique(b, (a == b + b) | (a == b + b + 1))).eval()


def test_uint_mul_unique():
    a, b, c = UInt(3), UInt(3), UInt(6)
    assert forall(a, b, exist_unique(c, c == a * b)).eval()


def test_uint_mul_overflow():
    a, b, c = UInt(3), UInt(3), UInt(5)
    assert not forall(a, b, exist(c, c == a * b)).eval()


def test_uint_mul_inplace():
    a, b = UInt(5), UInt(5)
    c = a
    c *= b
    assert exist(a, b, (a > 0) & (b > 0) & (c == 0)).eval()


def test_uint_mul_zero():
    a = UInt(5)
    assert forall(a, a * 0 == 0).eval()


def test_uint_mul_one():
    a = UInt(5)
    assert forall(a, a * 1 == a).eval()


def test_uint_mul_commutativity():
    a, b = UInt(5), UInt(5)
    assert forall(a, b, a * b == b * a).eval()


def test_uint_mul_associativity():
    a, b, c = UInt(3), UInt(3), UInt(3)
    assert forall(a, b, c, (a * b) * c == a * (b * c)).eval()


def test_uint_factorise():
    a, b = UInt(5), UInt(5)
    assert exist(a, b, (a > 1) & (b > 1) & (a * b == 899)).eval()


def test_uint_remainder():
    a, b, c = UInt(5), UInt(5), UInt(5)
    assert forall(a, b, (b == 0) | exist_unique(c, (b * c <= a) & (b * (c + 1) > a))).eval()


def test_uint_sum_squares():
    a, b = UInt(4), UInt(4)
    assert exist(a, b, (a < b) & (a * a + b * b == 65)).eval()
    assert not exist_unique(a, b, (a < b) & (a * a + b * b == 65)).eval()


def test_uint_add_mul_dist():
    a, b, c = UInt(4), UInt(4), UInt(4)
    assert forall(a, b, c, (a + b) * c == a * c + b * c).eval()


def test_uint_leq_transitivity():
    a, b, c = UInt(5), UInt(5), UInt(5)
    assert forall(a, b, c, ((a <= b) & (b <= c)).implies(a <= c)).eval()


def test_uint_lt_transitivity():
    a, b, c = UInt(5), UInt(5), UInt(5)
    assert forall(a, b, c, ((a < b) & (b < c)).implies(a < c)).eval()


def test_uint_geq_transitivity():
    a, b, c = UInt(5), UInt(5), UInt(5)
    assert forall(a, b, c, ((a >= b) & (b >= c)).implies(a >= c)).eval()


def test_uint_gt_transitivity():
    a, b, c = UInt(5), UInt(5), UInt(5)
    assert forall(a, b, c, ((a > b) & (b > c)).implies(a > c)).eval()


def test_uint_non_transitivity():
    a, b, c = UInt(5), UInt(5), UInt(5)
    assert not forall(a, b, c, ((a <= b) & (b <= c)).implies(a < c)).eval()


def test_uint_leq_geq_linearity():
    a, b = UInt(5), UInt(5)
    assert forall(a, b, (a <= b) | (a >= b)).eval()


def test_uint_lt_gt_linearity():
    a, b = UInt(5), UInt(5)
    assert forall(a, b, (a < b) | (a > b) | (a == b)).eval()


def test_uint_minimum():
    a, b, c = UInt(5), UInt(5), UInt(5)
    assert forall(a, b, exist_unique(c, (c <= a) & (c <= b) & ((c == a) | (c == b)))).eval()


def test_uint_ge_add_dist():
    a, b, c, d = UInt(4), UInt(4), UInt(4), UInt(4)
    assert forall(a, b, c, d, ((a >= c) & (b >= d)).implies(a + b >= c + d)).eval()


def test_uint_ge_mul_dist():
    a, b, c, d = UInt(4), UInt(4), UInt(4), UInt(4)
    assert forall(a, b, c, d, ((a >= c) & (b >= d)).implies(a * b >= c * d)).eval()


def test_uint_and_unique():
    a, b, c = UInt(5), UInt(5), UInt(5)
    assert forall(a, b, exist_unique(c, c == a & b)).eval()


def test_uint_and_zero():
    a = UInt(5)
    assert forall(a, a & 0 == 0).eval()


def test_uint_and_commutativity():
    a, b = UInt(5), UInt(5)
    assert forall(a, b, a & b == b & a).eval()


def test_uint_and_associativity():
    a, b, c = UInt(5), UInt(5), UInt(5)
    assert forall(a, b, c, (a & b) & c == a & (b & c)).eval()


def test_uint_and_monotonicity():
    a, b = UInt(5), UInt(5)
    assert forall(a, b, ((a & b) <= a) & ((a & b) <= b)).eval()


def test_uint_or_unique():
    a, b, c = UInt(5), UInt(5), UInt(5)
    assert forall(a, b, exist_unique(c, c == a | b)).eval()


def test_uint_or_zero():
    a = UInt(5)
    assert forall(a, a | 0 == a).eval()


def test_uint_or_commutativity():
    a, b = UInt(5), UInt(5)
    assert forall(a, b, a | b == b | a).eval()


def test_uint_or_associativity():
    a, b, c = UInt(5), UInt(5), UInt(5)
    assert forall(a, b, c, (a | b) | c == a | (b | c)).eval()


def test_uint_or_monotonicity():
    a, b = UInt(5), UInt(5)
    assert forall(a, b, ((a | b) >= a) & ((a | b) >= b)).eval()


def test_uint_not_and():
    a, b = UInt(5), UInt(5)
    assert forall(a, b, ~(a & b) == ~a | ~b).eval()


def test_uint_not_or():
    a, b = UInt(5), UInt(5)
    assert forall(a, b, ~(a | b) == ~a & ~b).eval()


def test_uint_and_or_dist():
    a, b, c = UInt(5), UInt(5), UInt(5)
    assert forall(a, b, c, (a & b) | c == (a | c) & (b | c)).eval()


def test_uint_or_and_dist():
    a, b, c = UInt(5), UInt(5), UInt(5)
    assert forall(a, b, c, (a | b) & c == (a & c) | (b & c)).eval()
