from solver import *


def test_2m_equals_n_unary():
    n = UIntUnary(num_bits=4)
    m = UIntUnary(num_bits=4)
    formula = forall([n], exist([m], n == m + m))
    assert not BruteForceSolver().solve(formula)


def test_2m_equals_2n_unary():
    n = UIntUnary(num_bits=4)
    m = UIntUnary(num_bits=4)
    formula = forall([n], exist([m], n + n == m + m))
    assert BruteForceSolver().solve(formula)


def test_add_commutativity_unary():
    a = UIntUnary(num_bits=4)
    b = UIntUnary(num_bits=4)
    formula = forall([a, b], a + b == b + a)
    assert BruteForceSolver().solve(formula)


def test_m2_equals_n_unary():
    n = UIntUnary(num_bits=4)
    m = UIntUnary(num_bits=4)
    formula = forall([n], exist([m], n == m * m))
    assert not BruteForceSolver().solve(formula)


def test_m2_equals_n2_unary():
    n = UIntUnary(num_bits=3)
    m = UIntUnary(num_bits=3)
    formula = forall([n], exist([m], n * n == m * m))
    assert BruteForceSolver().solve(formula)


def test_mul_commutativity_unary():
    n = UIntUnary(num_bits=3)
    m = UIntUnary(num_bits=3)
    formula = forall([n, m], n * m == m * n)
    assert BruteForceSolver().solve(formula)


def test_le_transitivity_unary():
    a = UIntUnary(num_bits=4)
    b = UIntUnary(num_bits=4)
    c = UIntUnary(num_bits=4)
    formula = forall([a, b, c], implies((a <= b) & (b <= c), a <= c))
    assert BruteForceSolver().solve(formula)


def test_ge_transitivity_unary():
    a = UIntUnary(num_bits=4)
    b = UIntUnary(num_bits=4)
    c = UIntUnary(num_bits=4)
    formula = forall([a, b, c], implies((a >= b) & (b >= c), a >= c))
    assert BruteForceSolver().solve(formula)


def test_2m_equals_n_binary():
    n = UIntBinary(num_bits=4)
    m = UIntBinary(num_bits=4)
    formula = forall([n], exist([m], n == m + m))
    assert not BruteForceSolver().solve(formula)


def test_2m_equals_2n_binary():
    n = UIntBinary(num_bits=4)
    m = UIntBinary(num_bits=4)
    formula = forall([n], exist([m], n + n == m + m))
    assert BruteForceSolver().solve(formula)


def test_add_commutativity_binary():
    a = UIntBinary(num_bits=4)
    b = UIntBinary(num_bits=4)
    formula = forall([a, b], a + b == b + a)
    assert BruteForceSolver().solve(formula)


def test_m2_equals_n_binary():
    n = UIntBinary(num_bits=2)
    m = UIntBinary(num_bits=2)
    formula = forall([n], exist([m], n == m * m))
    print(formula)
    assert not BruteForceSolver().solve(formula)


def test_m2_equals_n2_binary():
    n = UIntBinary(num_bits=3)
    m = UIntBinary(num_bits=3)
    formula = forall([n], exist([m], n * n == m * m))
    assert BruteForceSolver().solve(formula)


def test_mul_commutativity_binary():
    n = UIntBinary(num_bits=3)
    m = UIntBinary(num_bits=3)
    formula = forall([n, m], n * m == m * n)
    assert BruteForceSolver().solve(formula)


def test_le_transitivity_binary():
    a = UIntBinary(num_bits=4)
    b = UIntBinary(num_bits=4)
    c = UIntBinary(num_bits=4)
    formula = forall([a, b, c], implies((a <= b) & (b <= c), a <= c))
    assert BruteForceSolver().solve(formula)


def test_ge_transitivity_binary():
    a = UIntBinary(num_bits=4)
    b = UIntBinary(num_bits=4)
    c = UIntBinary(num_bits=4)
    formula = forall([a, b, c], implies((a >= b) & (b >= c), a >= c))
    assert BruteForceSolver().solve(formula)
