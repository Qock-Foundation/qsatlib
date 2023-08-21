from qsatlib import *
from solver import BruteForceSolver
from structures.numbers import UIntUnary, UIntBinary
from structures.graphs import DirectedGraph


def test_2m_equals_n_unary():
    n = UIntUnary(num_bits=4)
    m = UIntUnary(num_bits=4)
    formula = forall(n, exist(m, n == m + m))
    assert not BruteForceSolver().solve(formula)


def test_2m_equals_2n_unary():
    n = UIntUnary(num_bits=4)
    m = UIntUnary(num_bits=4)
    formula = forall(n, exist(m, n + n == m + m))
    assert BruteForceSolver().solve(formula)


def test_add_commutativity_unary():
    a = UIntUnary(num_bits=4)
    b = UIntUnary(num_bits=4)
    formula = forall(a, b, a + b == b + a)
    assert BruteForceSolver().solve(formula)


def test_m2_equals_n_unary():
    n = UIntUnary(num_bits=4)
    m = UIntUnary(num_bits=4)
    formula = forall(n, exist(m, n == m * m))
    assert not BruteForceSolver().solve(formula)


def test_m2_equals_n2_unary():
    n = UIntUnary(num_bits=3)
    m = UIntUnary(num_bits=3)
    formula = forall(n, exist(m, n * n == m * m))
    assert BruteForceSolver().solve(formula)


def test_mul_commutativity_unary():
    n = UIntUnary(num_bits=3)
    m = UIntUnary(num_bits=3)
    formula = forall(n, m, n * m == m * n)
    assert BruteForceSolver().solve(formula)


def test_le_transitivity_unary():
    a = UIntUnary(num_bits=4)
    b = UIntUnary(num_bits=4)
    c = UIntUnary(num_bits=4)
    formula = forall(a, b, c, implies((a <= b) & (b <= c), a <= c))
    assert BruteForceSolver().solve(formula)


def test_ge_transitivity_unary():
    a = UIntUnary(num_bits=4)
    b = UIntUnary(num_bits=4)
    c = UIntUnary(num_bits=4)
    formula = forall(a, b, c, implies((a >= b) & (b >= c), a >= c))
    assert BruteForceSolver().solve(formula)


def test_2m_equals_n_binary():
    n = UIntBinary(num_bits=4)
    m = UIntBinary(num_bits=4)
    formula = forall(n, exist(m, n == m + m))
    assert not BruteForceSolver().solve(formula)


def test_2m_equals_2n_binary():
    n = UIntBinary(num_bits=4)
    m = UIntBinary(num_bits=4)
    formula = forall(n, exist(m, n + n == m + m))
    assert BruteForceSolver().solve(formula)


def test_add_commutativity_binary():
    a = UIntBinary(num_bits=4)
    b = UIntBinary(num_bits=4)
    formula = forall(a, b, a + b == b + a)
    assert BruteForceSolver().solve(formula)


def test_m2_equals_n_binary():
    n = UIntBinary(num_bits=3)
    m = UIntBinary(num_bits=3)
    formula = forall(n, exist(m, n == m * m))
    assert not BruteForceSolver().solve(formula)


def test_m2_equals_n2_binary():
    n = UIntBinary(num_bits=3)
    m = UIntBinary(num_bits=3)
    formula = forall(n, exist(m, n * n == m * m))
    assert BruteForceSolver().solve(formula)


def test_mul_commutativity_binary():
    n = UIntBinary(num_bits=3)
    m = UIntBinary(num_bits=3)
    formula = forall(n, m, n * m == m * n)
    assert BruteForceSolver().solve(formula)


def test_le_transitivity_binary():
    a = UIntBinary(num_bits=4)
    b = UIntBinary(num_bits=4)
    c = UIntBinary(num_bits=4)
    formula = forall(a, b, c, implies((a <= b) & (b <= c), a <= c))
    assert BruteForceSolver().solve(formula)


def test_ge_transitivity_binary():
    a = UIntBinary(num_bits=4)
    b = UIntBinary(num_bits=4)
    c = UIntBinary(num_bits=4)
    formula = forall(a, b, c, implies((a >= b) & (b >= c), a >= c))
    assert BruteForceSolver().solve(formula)


def test_digraph_intersection():
    for n in range(4):
        a = DirectedGraph(num_vertices=n)
        b = DirectedGraph(num_vertices=n)
        for i in range(n):
            for j in range(n):
                formula = forall(a, b, implies(a.has_edge(i, j) & b.has_edge(i, j), (a & b).has_edge(i, j)))
                assert BruteForceSolver().solve(formula)
                formula = forall(a, b, implies((a & b).has_edge(i, j), a.has_edge(i, j) & b.has_edge(i, j)))
                assert BruteForceSolver().solve(formula)
