from qsatlib.qsatlib import *
from qsatlib.solver import BruteForceSolver


def test_variable_equality():
    n = 5
    solver = BruteForceSolver()

    # Uniqueness for ==
    a = Variable(num_bits=n)
    b = Variable(num_bits=n)
    formula = forall(a, exist_unique(b, b == a))
    assert solver.solve(formula)

    # Commutativity of ==
    a = Variable(num_bits=n)
    b = Variable(num_bits=n)
    formula = forall(a, b, implies(a == b, b == a))
    assert solver.solve(formula)

    # Transitivity of ==
    a = Variable(num_bits=n)
    b = Variable(num_bits=n)
    c = Variable(num_bits=n)
    formula = forall(a, b, c, implies((a == b) & (b == c), a == c))
    assert solver.solve(formula)

    # Non-uniqueness for !=
    a = Variable(num_bits=n)
    b = Variable(num_bits=n)
    formula = forall(a, exist_unique(b, b != a))
    assert not solver.solve(formula)

    # Commutativity of !=
    a = Variable(num_bits=n)
    b = Variable(num_bits=n)
    formula = forall(a, b, implies(a != b, b != a))
    assert solver.solve(formula)

    # Non-transitivity of !=
    a = Variable(num_bits=n)
    b = Variable(num_bits=n)
    c = Variable(num_bits=n)
    formula = forall(a, b, c, implies((a != b) & (b != c), a != c))
    assert not solver.solve(formula)

    # (a == b) & (b != c) => (a != c)
    a = Variable(num_bits=n)
    b = Variable(num_bits=n)
    c = Variable(num_bits=n)
    formula = forall(a, b, c, implies((a == b) & (b != c), a != c))
    assert solver.solve(formula)
