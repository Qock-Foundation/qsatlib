from qsatlib.numbers import *


# def test_unary_add():
#     n = 2
#     solver = BruteForceSolver()
#
#     # Uniqueness
#     a = UIntUnary(num_bits=n)
#     b = UIntUnary(num_bits=n)
#     c = UIntUnary(num_bits=2 * n)
#     formula = forall(a, b, exist_unique(c, c == a + b))
#     assert solver.solve(formula)
#
#     # Odd numbers
#     a = UIntUnary(num_bits=n)
#     b = UIntUnary(num_bits=n)
#     formula = forall(a, exist(b, a == b + b))
#     assert not solver.solve(formula)
#
#     # a + a == b + b for b = a
#     a = UIntUnary(num_bits=n)
#     b = UIntUnary(num_bits=n)
#     formula = forall(a, exist(b, a + a == b + b))
#     assert solver.solve(formula)
#
#     # Commutativity
#     a = UIntUnary(num_bits=n)
#     b = UIntUnary(num_bits=n)
#     formula = forall(a, b, a + b == b + a)
#     assert solver.solve(formula)
#
#     # Associativity
#     a = UIntUnary(num_bits=n)
#     b = UIntUnary(num_bits=n)
#     c = UIntUnary(num_bits=n)
#     formula = forall(a, b, c, (a + b) + c == a + (b + c))
#     assert solver.solve(formula)


# def test_unary_mul():
#     n = 2
#     solver = BruteForceSolver()
#
#     # Uniqueness
#     a = UIntUnary(num_bits=n)
#     b = UIntUnary(num_bits=n)
#     c = UIntUnary(num_bits=n * n)
#     formula = forall(a, b, exist_unique(c, c == a * b))
#     assert solver.solve(formula)
#
#     # Non-perfect squares
#     a = UIntUnary(num_bits=n)
#     b = UIntUnary(num_bits=n)
#     formula = forall(a, exist(b, a == b * b))
#     assert not solver.solve(formula)
#
#     # a * a == b * b for b = a
#     a = UIntUnary(num_bits=n)
#     b = UIntUnary(num_bits=n)
#     formula = forall(a, exist(b, a * a == b * b))
#     assert solver.solve(formula)
#
#     # Commutativity
#     a = UIntUnary(num_bits=n)
#     b = UIntUnary(num_bits=n)
#     formula = forall(a, b, a * b == b * a)
#     assert solver.solve(formula)
#
#     # Associativity
#     a = UIntUnary(num_bits=n)
#     b = UIntUnary(num_bits=n)
#     c = UIntUnary(num_bits=n)
#     formula = forall(a, b, c, (a * b) * c == a * (b * c))
#     assert solver.solve(formula)
#
#
# def test_unary_order():
#     n = 3
#     solver = BruteForceSolver()
#
#     # Transitivity of <=
#     a = UIntUnary(num_bits=n)
#     b = UIntUnary(num_bits=n)
#     c = UIntUnary(num_bits=n)
#     formula = forall(a, b, c, implies((a <= b) & (b <= c), a <= c))
#     assert solver.solve(formula)
#
#     # Transitivity of <
#     a = UIntUnary(num_bits=n)
#     b = UIntUnary(num_bits=n)
#     c = UIntUnary(num_bits=n)
#     formula = forall(a, b, c, implies((a < b) & (b < c), a < c))
#     assert solver.solve(formula)
#
#     # Transitivity of < and <=
#     a = UIntUnary(num_bits=n)
#     b = UIntUnary(num_bits=n)
#     c = UIntUnary(num_bits=n)
#     formula = forall(a, b, c, implies((a < b) & (b <= c), a < c))
#     assert solver.solve(formula)
#
#     # (a <= b) & (b <= c) !=> (a < c)
#     a = UIntUnary(num_bits=n)
#     b = UIntUnary(num_bits=n)
#     c = UIntUnary(num_bits=n)
#     formula = forall(a, b, c, implies((a <= b) & (b <= c), a < c))
#     assert not solver.solve(formula)
#
#     # Transitivity of >=
#     a = UIntUnary(num_bits=n)
#     b = UIntUnary(num_bits=n)
#     c = UIntUnary(num_bits=n)
#     formula = forall(a, b, c, implies((a >= b) & (b >= c), a >= c))
#     assert solver.solve(formula)
#
#     # Transitivity of >
#     a = UIntUnary(num_bits=n)
#     b = UIntUnary(num_bits=n)
#     c = UIntUnary(num_bits=n)
#     formula = forall(a, b, c, implies((a > b) & (b > c), a > c))
#     assert solver.solve(formula)
#
#     # Transitivity of > and >=
#     a = UIntUnary(num_bits=n)
#     b = UIntUnary(num_bits=n)
#     c = UIntUnary(num_bits=n)
#     formula = forall(a, b, c, implies((a > b) & (b >= c), a > c))
#     assert solver.solve(formula)
#
#     # (a >= b) & (b >= c) !=> (a > c)
#     a = UIntUnary(num_bits=n)
#     b = UIntUnary(num_bits=n)
#     c = UIntUnary(num_bits=n)
#     formula = forall(a, b, c, implies((a >= b) & (b >= c), a > c))
#     assert not solver.solve(formula)
#
#     # Linearity of <=
#     a = UIntUnary(num_bits=n)
#     b = UIntUnary(num_bits=n)
#     formula = forall(a, b, (a <= b) | (a >= b))
#     assert solver.solve(formula)
#
#     # Non-linearity of <
#     a = UIntUnary(num_bits=n)
#     b = UIntUnary(num_bits=n)
#     formula = forall(a, b, (a < b) | (a > b))
#     assert not solver.solve(formula)
#
#     # Linearity of < (for !=)
#     a = UIntUnary(num_bits=n)
#     b = UIntUnary(num_bits=n)
#     formula = forall(a, b, (a < b) | (a > b) | (a == b))
#     assert solver.solve(formula)
#
#     # (a <= b) <=> (b >= a)
#     a = UIntUnary(num_bits=n)
#     b = UIntUnary(num_bits=n)
#     formula = forall(a, b, (a <= b) == (b >= a))
#     assert solver.solve(formula)
#
#     # (a <= b) & (b <= a) => (a == b)
#     a = UIntUnary(num_bits=n)
#     b = UIntUnary(num_bits=n)
#     formula = forall(a, b, implies((a <= b) & (b <= a), a == b))
#     assert solver.solve(formula)
#
#     # (a <= c) & (b <= c) !=> (a <= b)
#     a = UIntUnary(num_bits=n)
#     b = UIntUnary(num_bits=n)
#     c = UIntUnary(num_bits=n)
#     formula = forall(a, b, c, implies((a <= c) & (b <= c), a <= b))
#     assert not solver.solve(formula)
#
#     # Minimum
#     a = UIntUnary(num_bits=n)
#     b = UIntUnary(num_bits=n)
#     formula = exist(a, forall(b, b >= a))
#     assert solver.solve(formula)
#
#
# def test_unary_dist():
#     n = 2
#     solver = BruteForceSolver()
#
#     # (a + b) * c == a * c + b * c
#     a = UIntUnary(num_bits=n)
#     b = UIntUnary(num_bits=n)
#     c = UIntUnary(num_bits=n)
#     formula = forall(a, b, c, (a + b) * c == a * c + b * c)
#     assert solver.solve(formula)
#
#     # (a >= c) & (b >= d) => a + b >= c + d
#     a = UIntUnary(num_bits=n)
#     b = UIntUnary(num_bits=n)
#     c = UIntUnary(num_bits=n)
#     d = UIntUnary(num_bits=n)
#     formula = forall(a, b, c, d, implies((a >= c) & (b >= d), a + b >= c + d))
#     assert solver.solve(formula)
#
#     # (a >= c) & (b >= d) => a * b >= c * d
#     a = UIntUnary(num_bits=n)
#     b = UIntUnary(num_bits=n)
#     c = UIntUnary(num_bits=n)
#     d = UIntUnary(num_bits=n)
#     formula = forall(a, b, c, d, implies((a >= c) & (b >= d), a * b >= c * d))
#     assert solver.solve(formula)


def test_uint_add():
    n = 5
    a, b, c = UInt(n), UInt(n), UInt(n + 1)

    # Uniqueness
    formula = forall(a, b, exist_unique(c, c == a + b))
    assert formula.eval()

    # Odd numbers
    formula = forall(a, exist(b, a == b + b))
    assert not formula.eval()

    # a + a == b + b for b = a
    formula = forall(a, exist(b, a + a == b + b))
    assert formula.eval()

    # Commutativity
    formula = forall(a, b, a + b == b + a)
    assert formula.eval()

    # Associativity
    formula = forall(a, b, c, (a + b) + c == a + (b + c))
    assert formula.eval()


def test_uint_mul():
    n = 3
    a, b, c = UInt(n), UInt(n), UInt(2 * n)

    # Uniqueness
    formula = forall(a, b, exist_unique(c, c == a * b))
    assert formula.eval()

    # Non-perfect squares
    formula = forall(a, exist(b, a == b * b))
    assert not formula.eval()

    # a * a == b * b for b = a
    formula = forall(a, exist(b, a * a == b * b))
    assert formula.eval()

    # Commutativity
    formula = forall(a, b, a * b == b * a)
    assert formula.eval()

    # Associativity
    formula = forall(a, b, c, (a * b) * c == a * (b * c))
    assert formula.eval()


def test_uint_order():
    n = 5
    a, b, c = UInt(n), UInt(n), UInt(n)

    # Transitivity of <=
    formula = forall(a, b, c, ((a <= b) & (b <= c)).implies(a <= c))
    assert formula.eval()

    # Transitivity of <
    formula = forall(a, b, c, ((a < b) & (b < c)).implies(a < c))
    assert formula.eval()

    # Transitivity of < and <=
    formula = forall(a, b, c, ((a < b) & (b <= c)).implies(a < c))
    assert formula.eval()

    # (a <= b) & (b <= c) !=> (a < c)
    formula = forall(a, b, c, ((a <= b) & (b <= c)).implies(a < c))
    assert not formula.eval()

    # Transitivity of >=
    formula = forall(a, b, c, ((a >= b) & (b >= c)).implies(a >= c))
    assert formula.eval()

    # Transitivity of >
    formula = forall(a, b, c, ((a > b) & (b > c)).implies(a > c))
    assert formula.eval()

    # Transitivity of > and >=
    formula = forall(a, b, c, ((a > b) & (b >= c)).implies(a > c))
    assert formula.eval()

    # (a >= b) & (b >= c) !=> (a > c)
    formula = forall(a, b, c, ((a >= b) & (b >= c)).implies(a > c))
    assert not formula.eval()

    # Linearity of <=
    formula = forall(a, b, (a <= b) | (a >= b))
    assert formula.eval()

    # Non-linearity of <
    formula = forall(a, b, (a < b) | (a > b))
    assert not formula.eval()

    # Linearity of < for unequal
    formula = forall(a, b, (a < b) | (a > b) | (a == b))
    assert formula.eval()

    # (a <= b) <=> (b >= a)
    formula = forall(a, b, (a <= b) == (b >= a))
    assert formula.eval()

    # (a <= b) & (b <= a) => (a == b)
    formula = forall(a, b, ((a <= b) & (b <= a)).implies(a == b))
    assert formula.eval()

    # (a <= c) & (b <= c) !=> (a <= b)
    formula = forall(a, b, c, ((a <= c) & (b <= c)).implies(a <= b))
    assert not formula.eval()

    # Minimum
    formula = exist(a, forall(b, b >= a))
    assert formula.eval()


def test_uint_dist():
    n = 4
    a, b, c, d = UInt(n), UInt(n), UInt(n), UInt(n)

    # (a + b) * c == a * c + b * c
    formula = forall(a, b, c, (a + b) * c == a * c + b * c)
    assert formula.eval()

    # (a >= c) & (b >= d) => a + b >= c + d
    formula = forall(a, b, c, d, ((a >= c) & (b >= d)).implies(a + b >= c + d))
    assert formula.eval()

    # (a >= c) & (b >= d) => a * b >= c * d
    formula = forall(a, b, c, d, ((a >= c) & (b >= d)).implies(a * b >= c * d))
    assert formula.eval()


def test_uint_bit():
    n = 5
    a, b, c = UInt(n), UInt(n), UInt(n)

    # Uniqueness of &
    formula = forall(a, b, exist_unique(c, c == (a & b)))
    assert formula.eval()

    # Commutativity of &
    formula = forall(a, b, (a & b) == (b & a))
    assert formula.eval()

    # Associativity of &
    formula = forall(a, b, c, ((a & b) & c) == (a & (b & c)))
    assert formula.eval()

    # Monotonicity of &
    formula = forall(a, b, ((a & b) <= a) & ((a & b) <= b))
    assert formula.eval()

    # Uniqueness of |
    formula = forall(a, b, exist_unique(c, c == (a | b)))
    assert formula.eval()

    # Commutativity of |
    formula = forall(a, b, (a | b) == (b | a))
    assert formula.eval()

    # Associativity of |
    formula = forall(a, b, c, ((a | b) | c) == (a | (b | c)))
    assert formula.eval()

    # Monotonicity of |
    formula = forall(a, b, (a <= (a | b)) & (b <= (a | b)))
    assert formula.eval()

    # ~(a & b) == (~a | ~b)
    formula = forall(a, b, ~(a & b) == (~a | ~b))
    assert formula.eval()

    # ~(a | b) == (~a & ~b)
    formula = forall(a, b, ~(a | b) == (~a & ~b))
    assert formula.eval()

    # a & (b | c) == (a & b) | (a & c)
    formula = forall(a, b, c, a & (b | c) == (a & b) | (a & c))
    assert formula.eval()

    # a | (b & c) == (a | b) & (a | c)
    formula = forall(a, b, c, a | (b & c) == (a | b) & (a | c))
    assert formula.eval()
