from qsatlib.numbers import *
from qsatlib.solver import BruteForceSolver


def test_unary_add():
    n = 2
    solver = BruteForceSolver()

    # Uniqueness
    a = UIntUnary(num_bits=n)
    b = UIntUnary(num_bits=n)
    c = UIntUnary(num_bits=2 * n)
    formula = forall(a, b, exist_unique(c, c == a + b))
    assert solver.solve(formula)

    # Odd numbers
    a = UIntUnary(num_bits=n)
    b = UIntUnary(num_bits=n)
    formula = forall(a, exist(b, a == b + b))
    assert not solver.solve(formula)

    # a + a == b + b for b = a
    a = UIntUnary(num_bits=n)
    b = UIntUnary(num_bits=n)
    formula = forall(a, exist(b, a + a == b + b))
    assert solver.solve(formula)

    # Commutativity
    a = UIntUnary(num_bits=n)
    b = UIntUnary(num_bits=n)
    formula = forall(a, b, a + b == b + a)
    assert solver.solve(formula)

    # Associativity
    a = UIntUnary(num_bits=n)
    b = UIntUnary(num_bits=n)
    c = UIntUnary(num_bits=n)
    formula = forall(a, b, c, (a + b) + c == a + (b + c))
    assert solver.solve(formula)


def test_unary_mul():
    n = 2
    solver = BruteForceSolver()

    # Uniqueness
    a = UIntUnary(num_bits=n)
    b = UIntUnary(num_bits=n)
    c = UIntUnary(num_bits=n * n)
    formula = forall(a, b, exist_unique(c, c == a * b))
    assert solver.solve(formula)

    # Non-perfect squares
    a = UIntUnary(num_bits=n)
    b = UIntUnary(num_bits=n)
    formula = forall(a, exist(b, a == b * b))
    assert not solver.solve(formula)

    # a * a == b * b for b = a
    a = UIntUnary(num_bits=n)
    b = UIntUnary(num_bits=n)
    formula = forall(a, exist(b, a * a == b * b))
    assert solver.solve(formula)

    # Commutativity
    a = UIntUnary(num_bits=n)
    b = UIntUnary(num_bits=n)
    formula = forall(a, b, a * b == b * a)
    assert solver.solve(formula)

    # Associativity
    a = UIntUnary(num_bits=n)
    b = UIntUnary(num_bits=n)
    c = UIntUnary(num_bits=n)
    formula = forall(a, b, c, (a * b) * c == a * (b * c))
    assert solver.solve(formula)


def test_unary_order():
    n = 3
    solver = BruteForceSolver()

    # Transitivity of <=
    a = UIntUnary(num_bits=n)
    b = UIntUnary(num_bits=n)
    c = UIntUnary(num_bits=n)
    formula = forall(a, b, c, implies((a <= b) & (b <= c), a <= c))
    assert solver.solve(formula)

    # Transitivity of <
    a = UIntUnary(num_bits=n)
    b = UIntUnary(num_bits=n)
    c = UIntUnary(num_bits=n)
    formula = forall(a, b, c, implies((a < b) & (b < c), a < c))
    assert solver.solve(formula)

    # Transitivity of < and <=
    a = UIntUnary(num_bits=n)
    b = UIntUnary(num_bits=n)
    c = UIntUnary(num_bits=n)
    formula = forall(a, b, c, implies((a < b) & (b <= c), a < c))
    assert solver.solve(formula)

    # (a <= b) & (b <= c) !=> (a < c)
    a = UIntUnary(num_bits=n)
    b = UIntUnary(num_bits=n)
    c = UIntUnary(num_bits=n)
    formula = forall(a, b, c, implies((a <= b) & (b <= c), a < c))
    assert not solver.solve(formula)

    # Transitivity of >=
    a = UIntUnary(num_bits=n)
    b = UIntUnary(num_bits=n)
    c = UIntUnary(num_bits=n)
    formula = forall(a, b, c, implies((a >= b) & (b >= c), a >= c))
    assert solver.solve(formula)

    # Transitivity of >
    a = UIntUnary(num_bits=n)
    b = UIntUnary(num_bits=n)
    c = UIntUnary(num_bits=n)
    formula = forall(a, b, c, implies((a > b) & (b > c), a > c))
    assert solver.solve(formula)

    # Transitivity of > and >=
    a = UIntUnary(num_bits=n)
    b = UIntUnary(num_bits=n)
    c = UIntUnary(num_bits=n)
    formula = forall(a, b, c, implies((a > b) & (b >= c), a > c))
    assert solver.solve(formula)

    # (a >= b) & (b >= c) !=> (a > c)
    a = UIntUnary(num_bits=n)
    b = UIntUnary(num_bits=n)
    c = UIntUnary(num_bits=n)
    formula = forall(a, b, c, implies((a >= b) & (b >= c), a > c))
    assert not solver.solve(formula)

    # Linearity of <=
    a = UIntUnary(num_bits=n)
    b = UIntUnary(num_bits=n)
    formula = forall(a, b, (a <= b) | (a >= b))
    assert solver.solve(formula)

    # Non-linearity of <
    a = UIntUnary(num_bits=n)
    b = UIntUnary(num_bits=n)
    formula = forall(a, b, (a < b) | (a > b))
    assert not solver.solve(formula)

    # Linearity of < (for !=)
    a = UIntUnary(num_bits=n)
    b = UIntUnary(num_bits=n)
    formula = forall(a, b, (a < b) | (a > b) | (a == b))
    assert solver.solve(formula)

    # (a <= b) <=> (b >= a)
    a = UIntUnary(num_bits=n)
    b = UIntUnary(num_bits=n)
    formula = forall(a, b, (a <= b) == (b >= a))
    assert solver.solve(formula)

    # (a <= b) & (b <= a) => (a == b)
    a = UIntUnary(num_bits=n)
    b = UIntUnary(num_bits=n)
    formula = forall(a, b, implies((a <= b) & (b <= a), a == b))
    assert solver.solve(formula)

    # (a <= c) & (b <= c) !=> (a <= b)
    a = UIntUnary(num_bits=n)
    b = UIntUnary(num_bits=n)
    c = UIntUnary(num_bits=n)
    formula = forall(a, b, c, implies((a <= c) & (b <= c), a <= b))
    assert not solver.solve(formula)

    # Minimum
    a = UIntUnary(num_bits=n)
    b = UIntUnary(num_bits=n)
    formula = exist(a, forall(b, b >= a))
    assert solver.solve(formula)


def test_unary_dist():
    n = 2
    solver = BruteForceSolver()

    # (a + b) * c == a * c + b * c
    a = UIntUnary(num_bits=n)
    b = UIntUnary(num_bits=n)
    c = UIntUnary(num_bits=n)
    formula = forall(a, b, c, (a + b) * c == a * c + b * c)
    assert solver.solve(formula)

    # (a >= c) & (b >= d) => a + b >= c + d
    a = UIntUnary(num_bits=n)
    b = UIntUnary(num_bits=n)
    c = UIntUnary(num_bits=n)
    d = UIntUnary(num_bits=n)
    formula = forall(a, b, c, d, implies((a >= c) & (b >= d), a + b >= c + d))
    assert solver.solve(formula)

    # (a >= c) & (b >= d) => a * b >= c * d
    a = UIntUnary(num_bits=n)
    b = UIntUnary(num_bits=n)
    c = UIntUnary(num_bits=n)
    d = UIntUnary(num_bits=n)
    formula = forall(a, b, c, d, implies((a >= c) & (b >= d), a * b >= c * d))
    assert solver.solve(formula)


def test_unary_comp_with_ints():
    solver = BruteForceSolver()
    for n in range(1, 4):
        for k in range(n, n + 4):
            a = UIntUnary(num_bits=n)
            formula = forall(a, a <= k)
            assert solver.solve(formula)

            a = UIntUnary(num_bits=n)
            formula = forall(a, a < k + 1)
            assert solver.solve(formula)

        for k in range(0, n):
            a = UIntUnary(num_bits=n)
            formula = exists(a, a >= k)
            assert solver.solve(formula)

        # Adding more similar tests

        # Test for a == k
        for k in range(0, n + 1):
            a = UIntUnary(num_bits=n)
            formula = exists(a, a == k)
            assert solver.solve(formula)

        # Test for a != k
        for k in range(0, n):
            a = UIntUnary(num_bits=n)
            formula = exists(a, a != k)
            assert solver.solve(formula)

        # Test for a > k
        for k in range(0, n - 1):
            a = UIntUnary(num_bits=n)
            formula = exists(a, a > k)
            assert solver.solve(formula)


#def test_binary_comp_with_ints():
#    solver = BruteForceSolver()
#    for n in range(1, 4):
#        for k in range(2 ** n, 2 ** n + 4):
#            a = UIntBinary(num_bits=n)
#            formula = forall(a, a <= k)
#            assert solver.solve(formula)
#
#            a = UIntBinary(num_bits=n)
#            formula = forall(a, a < k + 1)
#            assert solver.solve(formula)
#
#        for k in range(0, 2 ** n):
#            a = UIntBinary(num_bits=n)
#            formula = exists(a, a >= k)
#            assert solver.solve(formula)
#
#        # Adding more similar tests
#
#        # Test for a == k
#        for k in range(0, 2 ** n + 1):
#            a = UIntBinary(num_bits=n)
#            formula = exists(a, a == k)
#            assert solver.solve(formula)
#
#        # Test for a != k
#        for k in range(0, 2 ** n):
#            a = UIntBinary(num_bits=n)
#            formula = exists(a, a != k)
#            assert solver.solve(formula)
#
#        # Test for a > k
#        for k in range(0, 2 ** n - 1):
#            a = UIntBinary(num_bits=n)
#            formula = exists(a, a > k)
#            assert solver.solve(formula)


def test_binary_add():
    n = 2
    solver = BruteForceSolver()

    # Uniqueness
    a = UIntBinary(num_bits=n)
    b = UIntBinary(num_bits=n)
    c = UIntBinary(num_bits=n)
    formula = forall(a, b, exist_unique(c, c == a + b))
    assert solver.solve(formula)

    # Odd numbers
    a = UIntBinary(num_bits=n)
    b = UIntBinary(num_bits=n)
    formula = forall(a, exist(b, a == b + b))
    assert not solver.solve(formula)

    # a + a == b + b for b = a
    a = UIntBinary(num_bits=n)
    b = UIntBinary(num_bits=n)
    formula = forall(a, exist(b, a + a == b + b))
    assert solver.solve(formula)

    # Commutativity
    a = UIntBinary(num_bits=n)
    b = UIntBinary(num_bits=n)
    formula = forall(a, b, a + b == b + a)
    assert solver.solve(formula)

    # Associativity
    a = UIntBinary(num_bits=n)
    b = UIntBinary(num_bits=n)
    c = UIntBinary(num_bits=n)
    formula = forall(a, b, c, (a + b) + c == a + (b + c))
    assert solver.solve(formula)


def test_binary_mul():
    n = 2
    solver = BruteForceSolver()

    # Uniqueness
    a = UIntBinary(num_bits=n)
    b = UIntBinary(num_bits=n)
    c = UIntBinary(num_bits=n)
    formula = forall(a, b, exist_unique(c, c == a * b))
    assert solver.solve(formula)

    # Non-perfect squares
    a = UIntBinary(num_bits=n)
    b = UIntBinary(num_bits=n)
    formula = forall(a, exist(b, a == b * b))
    assert not solver.solve(formula)

    # a * a == b * b for b = a
    a = UIntBinary(num_bits=n)
    b = UIntBinary(num_bits=n)
    formula = forall(a, exist(b, a * a == b * b))
    assert solver.solve(formula)

    # Commutativity
    a = UIntBinary(num_bits=n)
    b = UIntBinary(num_bits=n)
    formula = forall(a, b, a * b == b * a)
    assert solver.solve(formula)

    # Associativity
    a = UIntBinary(num_bits=n)
    b = UIntBinary(num_bits=n)
    c = UIntBinary(num_bits=n)
    formula = forall(a, b, c, (a * b) * c == a * (b * c))
    assert solver.solve(formula)


def test_binary_order():
    n = 3
    solver = BruteForceSolver()

    # Transitivity of <=
    a = UIntBinary(num_bits=n)
    b = UIntBinary(num_bits=n)
    c = UIntBinary(num_bits=n)
    formula = forall(a, b, c, implies((a <= b) & (b <= c), a <= c))
    assert solver.solve(formula)

    # Transitivity of <
    a = UIntBinary(num_bits=n)
    b = UIntBinary(num_bits=n)
    c = UIntBinary(num_bits=n)
    formula = forall(a, b, c, implies((a < b) & (b < c), a < c))
    assert solver.solve(formula)

    # Transitivity of < and <=
    a = UIntBinary(num_bits=n)
    b = UIntBinary(num_bits=n)
    c = UIntBinary(num_bits=n)
    formula = forall(a, b, c, implies((a < b) & (b <= c), a < c))
    assert solver.solve(formula)

    # (a <= b) & (b <= c) !=> (a < c)
    a = UIntBinary(num_bits=n)
    b = UIntBinary(num_bits=n)
    c = UIntBinary(num_bits=n)
    formula = forall(a, b, c, implies((a <= b) & (b <= c), a < c))
    assert not solver.solve(formula)

    # Transitivity of >=
    a = UIntBinary(num_bits=n)
    b = UIntBinary(num_bits=n)
    c = UIntBinary(num_bits=n)
    formula = forall(a, b, c, implies((a >= b) & (b >= c), a >= c))
    assert solver.solve(formula)

    # Transitivity of >
    a = UIntBinary(num_bits=n)
    b = UIntBinary(num_bits=n)
    c = UIntBinary(num_bits=n)
    formula = forall(a, b, c, implies((a > b) & (b > c), a > c))
    assert solver.solve(formula)

    # Transitivity of > and >=
    a = UIntBinary(num_bits=n)
    b = UIntBinary(num_bits=n)
    c = UIntBinary(num_bits=n)
    formula = forall(a, b, c, implies((a > b) & (b >= c), a > c))
    assert solver.solve(formula)

    # (a >= b) & (b >= c) !=> (a > c)
    a = UIntBinary(num_bits=n)
    b = UIntBinary(num_bits=n)
    c = UIntBinary(num_bits=n)
    formula = forall(a, b, c, implies((a >= b) & (b >= c), a > c))
    assert not solver.solve(formula)

    # Linearity of <=
    a = UIntBinary(num_bits=n)
    b = UIntBinary(num_bits=n)
    formula = forall(a, b, (a <= b) | (a >= b))
    assert solver.solve(formula)

    # Non-linearity of <
    a = UIntBinary(num_bits=n)
    b = UIntBinary(num_bits=n)
    formula = forall(a, b, (a < b) | (a > b))
    assert not solver.solve(formula)

    # Linearity of < for unequal
    a = UIntBinary(num_bits=n)
    b = UIntBinary(num_bits=n)
    formula = forall(a, b, (a < b) | (a > b) | (a == b))
    assert solver.solve(formula)

    # (a <= b) <=> (b >= a)
    a = UIntBinary(num_bits=n)
    b = UIntBinary(num_bits=n)
    formula = forall(a, b, (a <= b) == (b >= a))
    assert solver.solve(formula)

    # (a <= b) & (b <= a) => (a == b)
    a = UIntBinary(num_bits=n)
    b = UIntBinary(num_bits=n)
    formula = forall(a, b, implies((a <= b) & (b <= a), a == b))
    assert solver.solve(formula)

    # (a <= c) & (b <= c) !=> (a <= b)
    a = UIntBinary(num_bits=n)
    b = UIntBinary(num_bits=n)
    c = UIntBinary(num_bits=n)
    formula = forall(a, b, c, implies((a <= c) & (b <= c), a <= b))
    assert not solver.solve(formula)

    # Minimum
    a = UIntBinary(num_bits=n)
    b = UIntBinary(num_bits=n)
    formula = exist(a, forall(b, b >= a))
    assert solver.solve(formula)


def test_binary_dist():
    n = 2
    solver = BruteForceSolver()

    # (a + b) * c == a * c + b * c
    a = UIntBinary(num_bits=n)
    b = UIntBinary(num_bits=n)
    c = UIntBinary(num_bits=n)
    formula = forall(a, b, c, (a + b) * c == a * c + b * c)
    assert solver.solve(formula)

    # (a >= c) & (b >= d) !=> a + b >= c + d
    a = UIntBinary(num_bits=n)
    b = UIntBinary(num_bits=n)
    c = UIntBinary(num_bits=n)
    d = UIntBinary(num_bits=n)
    formula = forall(a, b, c, d, implies((a >= c) & (b >= d), a + b >= c + d))
    assert not solver.solve(formula)

    # (a >= c) & (b >= d) !=> a * b >= c * d
    a = UIntBinary(num_bits=n)
    b = UIntBinary(num_bits=n)
    c = UIntBinary(num_bits=n)
    d = UIntBinary(num_bits=n)
    formula = forall(a, b, c, d, implies((a >= c) & (b >= d), a * b >= c * d))
    assert not solver.solve(formula)


def test_binary_bit_and():
    n = 3
    solver = BruteForceSolver()

    # Uniqueness
    a = UIntBinary(num_bits=n)
    b = UIntBinary(num_bits=n)
    c = UIntBinary(num_bits=n)
    formula = forall(a, b, exist_unique(c, c == (a & b)))
    assert solver.solve(formula)

    # Commutativity
    a = UIntBinary(num_bits=n)
    b = UIntBinary(num_bits=n)
    formula = forall(a, b, (a & b) == (b & a))
    assert solver.solve(formula)

    # Associativity
    a = UIntBinary(num_bits=n)
    b = UIntBinary(num_bits=n)
    c = UIntBinary(num_bits=n)
    formula = forall(a, b, c, ((a & b) & c) == (a & (b & c)))
    assert solver.solve(formula)

    # Monotonicity
    a = UIntBinary(num_bits=n)
    b = UIntBinary(num_bits=n)
    formula = forall(a, b, ((a & b) <= a) & ((a & b) <= b))
    assert solver.solve(formula)


def test_binary_bit_or():
    n = 3
    solver = BruteForceSolver()

    # Uniqueness
    a = UIntBinary(num_bits=n)
    b = UIntBinary(num_bits=n)
    c = UIntBinary(num_bits=n)
    formula = forall(a, b, exist_unique(c, c == (a | b)))
    assert solver.solve(formula)

    # Commutativity
    a = UIntBinary(num_bits=n)
    b = UIntBinary(num_bits=n)
    formula = forall(a, b, (a | b) == (b | a))
    assert solver.solve(formula)

    # Associativity
    a = UIntBinary(num_bits=n)
    b = UIntBinary(num_bits=n)
    c = UIntBinary(num_bits=n)
    formula = forall(a, b, c, ((a | b) | c) == (a | (b | c)))
    assert solver.solve(formula)

    # Monotonicity
    a = UIntBinary(num_bits=n)
    b = UIntBinary(num_bits=n)
    formula = forall(a, b, (a <= (a | b)) & (b <= (a | b)))
    assert solver.solve(formula)


def test_binary_bit_dist():
    n = 3
    solver = BruteForceSolver()

    # ~(a & b) == (~a | ~b)
    a = UIntBinary(num_bits=n)
    b = UIntBinary(num_bits=n)
    formula = forall(a, b, ~(a & b) == (~a | ~b))
    assert solver.solve(formula)

    # ~(a | b) == (~a & ~b)
    a = UIntBinary(num_bits=n)
    b = UIntBinary(num_bits=n)
    formula = forall(a, b, ~(a | b) == (~a & ~b))
    assert solver.solve(formula)

    # a & (b | c) == (a & b) | (a & c)
    a = UIntBinary(num_bits=n)
    b = UIntBinary(num_bits=n)
    c = UIntBinary(num_bits=n)
    formula = forall(a, b, c, a & (b | c) == (a & b) | (a & c))
    assert solver.solve(formula)

    # a | (b & c) == (a | b) & (a | c)
    a = UIntBinary(num_bits=n)
    b = UIntBinary(num_bits=n)
    c = UIntBinary(num_bits=n)
    formula = forall(a, b, c, a | (b & c) == (a | b) & (a | c))
    assert solver.solve(formula)
