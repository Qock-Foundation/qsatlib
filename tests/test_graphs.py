from qsatlib.graphs import *
from qsatlib.solver import BruteForceSolver


def test_digraph_equality():
    n = 2
    solver = BruteForceSolver()

    # Uniqueness for ==
    a = DirectedGraph(num_vertices=n)
    b = DirectedGraph(num_vertices=n)
    formula = forall(a, exist_unique(b, b == a))
    assert solver.solve(formula)

    # Commutativity of ==
    a = DirectedGraph(num_vertices=n)
    b = DirectedGraph(num_vertices=n)
    formula = forall(a, b, implies(a == b, b == a))
    assert solver.solve(formula)

    # Transitivity of ==
    a = DirectedGraph(num_vertices=n)
    b = DirectedGraph(num_vertices=n)
    c = DirectedGraph(num_vertices=n)
    formula = forall(a, b, c, implies((a == b) & (b == c), a == c))
    assert solver.solve(formula)

    # Non-uniqueness for !=
    a = DirectedGraph(num_vertices=n)
    b = DirectedGraph(num_vertices=n)
    formula = forall(a, exist_unique(b, b != a))
    assert not solver.solve(formula)

    # Commutativity of !=
    a = DirectedGraph(num_vertices=n)
    b = DirectedGraph(num_vertices=n)
    formula = forall(a, b, implies(a != b, b != a))
    assert solver.solve(formula)

    # Non-transitivity of !=
    a = DirectedGraph(num_vertices=n)
    b = DirectedGraph(num_vertices=n)
    c = DirectedGraph(num_vertices=n)
    formula = forall(a, b, c, implies((a != b) & (b != c), a != c))
    assert not solver.solve(formula)

    # (a == b) & (b != c) => (a != c)
    a = DirectedGraph(num_vertices=n)
    b = DirectedGraph(num_vertices=n)
    c = DirectedGraph(num_vertices=n)
    formula = forall(a, b, c, implies((a == b) & (b != c), a != c))
    assert solver.solve(formula)


def test_digraph_set_operations():
    n = 2
    solver = BruteForceSolver()

    # definition of intersection
    for i in range(n):
        for j in range(n):
            a = DirectedGraph(num_vertices=n)
            b = DirectedGraph(num_vertices=n)
            formula = forall(a, b, (a & b).has_edge(i, j) == a.has_edge(i, j) & b.has_edge(i, j))
            assert solver.solve(formula)

    # commutativity of intersection
    a = DirectedGraph(num_vertices=n)
    b = DirectedGraph(num_vertices=n)
    formula = forall(a, b, (a & b) == (b & a))
    assert solver.solve(formula)

    # associativity of intersection
    a = DirectedGraph(num_vertices=n)
    b = DirectedGraph(num_vertices=n)
    c = DirectedGraph(num_vertices=n)
    formula = forall(a, b, c, ((a & b) & c) == (a & (b & c)))
    assert solver.solve(formula)

    # definition of union
    for i in range(n):
        for j in range(n):
            a = DirectedGraph(num_vertices=n)
            b = DirectedGraph(num_vertices=n)
            formula = forall(a, b, (a | b).has_edge(i, j) == a.has_edge(i, j) | b.has_edge(i, j))
            assert solver.solve(formula)

    # commutativity of union
    a = DirectedGraph(num_vertices=n)
    b = DirectedGraph(num_vertices=n)
    formula = forall(a, b, (a | b) == (b | a))
    assert solver.solve(formula)

    # associativity of union
    a = DirectedGraph(num_vertices=n)
    b = DirectedGraph(num_vertices=n)
    c = DirectedGraph(num_vertices=n)
    formula = forall(a, b, c, ((a | b) | c) == (a | (b | c)))
    assert solver.solve(formula)

    # (a | b) & c == (a & c) | (b & c)
    a = DirectedGraph(num_vertices=n)
    b = DirectedGraph(num_vertices=n)
    c = DirectedGraph(num_vertices=n)
    formula = forall(a, b, c, ((a | b) & c) == ((a & c) | (b & c)))
    assert solver.solve(formula)

    # (a & b) | c == (a | c) & (b | c)
    a = DirectedGraph(num_vertices=n)
    b = DirectedGraph(num_vertices=n)
    c = DirectedGraph(num_vertices=n)
    formula = forall(a, b, c, ((a & b) | c) == ((a | c) & (b | c)))
    assert solver.solve(formula)


def test_graph_equality():
    n = 2
    solver = BruteForceSolver()

    # Uniqueness for ==
    a = UndirectedGraph(num_vertices=n)
    b = UndirectedGraph(num_vertices=n)
    formula = forall(a, exist_unique(b, b == a))
    assert solver.solve(formula)

    # Commutativity of ==
    a = UndirectedGraph(num_vertices=n)
    b = UndirectedGraph(num_vertices=n)
    formula = forall(a, b, implies(a == b, b == a))
    assert solver.solve(formula)

    # Transitivity of ==
    a = UndirectedGraph(num_vertices=n)
    b = UndirectedGraph(num_vertices=n)
    c = UndirectedGraph(num_vertices=n)
    formula = forall(a, b, c, implies((a == b) & (b == c), a == c))
    assert solver.solve(formula)

    # Uniqueness for != (n = 2)
    a = UndirectedGraph(num_vertices=n)
    b = UndirectedGraph(num_vertices=n)
    formula = forall(a, exist_unique(b, b != a))
    assert solver.solve(formula)

    # Commutativity of !=
    a = UndirectedGraph(num_vertices=n)
    b = UndirectedGraph(num_vertices=n)
    formula = forall(a, b, implies(a != b, b != a))
    assert solver.solve(formula)

    # Non-transitivity of !=
    a = UndirectedGraph(num_vertices=n)
    b = UndirectedGraph(num_vertices=n)
    c = UndirectedGraph(num_vertices=n)
    formula = forall(a, b, c, implies((a != b) & (b != c), a != c))
    assert not solver.solve(formula)

    # (a == b) & (b != c) => (a != c)
    a = UndirectedGraph(num_vertices=n)
    b = UndirectedGraph(num_vertices=n)
    c = UndirectedGraph(num_vertices=n)
    formula = forall(a, b, c, implies((a == b) & (b != c), a != c))
    assert solver.solve(formula)


def test_graph_set_operations():
    n = 2
    solver = BruteForceSolver()

    # definition of intersection
    for i in range(n):
        for j in range(n):
            a = UndirectedGraph(num_vertices=n)
            b = UndirectedGraph(num_vertices=n)
            formula = forall(a, b, (a & b).has_edge(i, j) == a.has_edge(i, j) & b.has_edge(i, j))
            assert solver.solve(formula)

    # commutativity of intersection
    a = UndirectedGraph(num_vertices=n)
    b = UndirectedGraph(num_vertices=n)
    formula = forall(a, b, (a & b) == (b & a))
    assert solver.solve(formula)

    # associativity of intersection
    a = UndirectedGraph(num_vertices=n)
    b = UndirectedGraph(num_vertices=n)
    c = UndirectedGraph(num_vertices=n)
    formula = forall(a, b, c, ((a & b) & c) == (a & (b & c)))
    assert solver.solve(formula)

    # definition of union
    for i in range(n):
        for j in range(n):
            a = UndirectedGraph(num_vertices=n)
            b = UndirectedGraph(num_vertices=n)
            formula = forall(a, b, (a | b).has_edge(i, j) == a.has_edge(i, j) | b.has_edge(i, j))
            assert solver.solve(formula)

    # commutativity of union
    a = UndirectedGraph(num_vertices=n)
    b = UndirectedGraph(num_vertices=n)
    formula = forall(a, b, (a | b) == (b | a))
    assert solver.solve(formula)

    # associativity of union
    a = UndirectedGraph(num_vertices=n)
    b = UndirectedGraph(num_vertices=n)
    c = UndirectedGraph(num_vertices=n)
    formula = forall(a, b, c, ((a | b) | c) == (a | (b | c)))
    assert solver.solve(formula)

    # (a | b) & c == (a & c) | (b & c)
    a = UndirectedGraph(num_vertices=n)
    b = UndirectedGraph(num_vertices=n)
    c = UndirectedGraph(num_vertices=n)
    formula = forall(a, b, c, ((a | b) & c) == ((a & c) | (b & c)))
    assert solver.solve(formula)

    # (a & b) | c == (a | c) & (b | c)
    a = UndirectedGraph(num_vertices=n)
    b = UndirectedGraph(num_vertices=n)
    c = UndirectedGraph(num_vertices=n)
    formula = forall(a, b, c, ((a & b) | c) == ((a | c) & (b | c)))
    assert solver.solve(formula)
