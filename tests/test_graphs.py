from qsatlib.graphs import *
from qsatlib.solver import BruteForceSolver


def test_digraph_equality():
    n = 2
    solver = BruteForceSolver()

    # Commutativity of ==
    a = DirectedGraph(num_vertices=n)
    b = DirectedGraph(num_vertices=n)
    formula = forall(a, b, implies(a == b, b == a))
    assert solver.solve(formula)

    # Commutativity of !=
    a = DirectedGraph(num_vertices=n)
    b = DirectedGraph(num_vertices=n)
    formula = forall(a, b, implies(a != b, b != a))
    assert solver.solve(formula)

    # Transitivity of ==
    a = DirectedGraph(num_vertices=n)
    b = DirectedGraph(num_vertices=n)
    c = DirectedGraph(num_vertices=n)
    formula = forall(a, b, c, implies((a == b) & (b == c), a == c))
    assert solver.solve(formula)

    # Non-transitivity of !=
    a = DirectedGraph(num_vertices=n)
    b = DirectedGraph(num_vertices=n)
    c = DirectedGraph(num_vertices=n)
    formula = forall(a, b, c, implies((a != b) & (b != c), a != c))
    assert not solver.solve(formula)

    # Now together
    a = DirectedGraph(num_vertices=n)
    b = DirectedGraph(num_vertices=n)
    c = DirectedGraph(num_vertices=n)
    formula = forall(a, b, c, implies((a == b) & (b != c), a != c))
    assert solver.solve(formula)


def test_digraph_intersection():
    n = 2
    solver = BruteForceSolver()

    # definition
    for i in range(n):
        for j in range(n):
            a = DirectedGraph(num_vertices=n)
            b = DirectedGraph(num_vertices=n)
            formula = forall(a, b, (a & b).has_edge(i, j) == a.has_edge(i, j) & b.has_edge(i, j))
            assert solver.solve(formula)

    # commutativity
    a = DirectedGraph(num_vertices=n)
    b = DirectedGraph(num_vertices=n)
    formula = forall(a, b, (a & b) == (b & a))
    assert solver.solve(formula)

    # associativity
    a = DirectedGraph(num_vertices=n)
    b = DirectedGraph(num_vertices=n)
    c = DirectedGraph(num_vertices=n)
    formula = forall(a, b, c, ((a & b) & c) == (a & (b & c)))
    assert solver.solve(formula)


def test_digraph_union():
    n = 2
    solver = BruteForceSolver()

    # definition
    for i in range(n):
        for j in range(n):
            a = DirectedGraph(num_vertices=n)
            b = DirectedGraph(num_vertices=n)
            formula = forall(a, b, (a | b).has_edge(i, j) == a.has_edge(i, j) | b.has_edge(i, j))
            assert solver.solve(formula)

    # commutativity
    a = DirectedGraph(num_vertices=n)
    b = DirectedGraph(num_vertices=n)
    formula = forall(a, b, (a | b) == (b | a))
    assert solver.solve(formula)

    # associativity
    a = DirectedGraph(num_vertices=n)
    b = DirectedGraph(num_vertices=n)
    c = DirectedGraph(num_vertices=n)
    formula = forall(a, b, c, ((a | b) | c) == (a | (b | c)))
    assert solver.solve(formula)


def test_digraph_intersection_and_union():
    n = 2
    solver = BruteForceSolver()

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

    # Commutativity of ==
    a = UndirectedGraph(num_vertices=n)
    b = UndirectedGraph(num_vertices=n)
    formula = forall(a, b, implies(a == b, b == a))
    assert solver.solve(formula)

    # Commutativity of !=
    a = UndirectedGraph(num_vertices=n)
    b = UndirectedGraph(num_vertices=n)
    formula = forall(a, b, implies(a != b, b != a))
    assert solver.solve(formula)

    # Transitivity of ==
    a = UndirectedGraph(num_vertices=n)
    b = UndirectedGraph(num_vertices=n)
    c = UndirectedGraph(num_vertices=n)
    formula = forall(a, b, c, implies((a == b) & (b == c), a == c))
    assert solver.solve(formula)

    # Non-transitivity of !=
    a = UndirectedGraph(num_vertices=n)
    b = UndirectedGraph(num_vertices=n)
    c = UndirectedGraph(num_vertices=n)
    formula = forall(a, b, c, implies((a != b) & (b != c), a != c))
    assert not solver.solve(formula)

    # now together
    a = UndirectedGraph(num_vertices=n)
    b = UndirectedGraph(num_vertices=n)
    c = UndirectedGraph(num_vertices=n)
    formula = forall(a, b, c, implies((a == b) & (b != c), a != c))
    assert solver.solve(formula)


def test_graph_intersection():
    n = 2
    solver = BruteForceSolver()

    # definition
    for i in range(n):
        for j in range(n):
            a = UndirectedGraph(num_vertices=n)
            b = UndirectedGraph(num_vertices=n)
            formula = forall(a, b, (a & b).has_edge(i, j) == a.has_edge(i, j) & b.has_edge(i, j))
            assert solver.solve(formula)

    # commutativity
    a = UndirectedGraph(num_vertices=n)
    b = UndirectedGraph(num_vertices=n)
    formula = forall(a, b, (a & b) == (b & a))
    assert solver.solve(formula)

    # associativity
    a = UndirectedGraph(num_vertices=n)
    b = UndirectedGraph(num_vertices=n)
    c = UndirectedGraph(num_vertices=n)
    formula = forall(a, b, c, ((a & b) & c) == (a & (b & c)))
    assert solver.solve(formula)


def test_graph_union():
    n = 2
    solver = BruteForceSolver()

    # definition
    for i in range(n):
        for j in range(n):
            a = UndirectedGraph(num_vertices=n)
            b = UndirectedGraph(num_vertices=n)
            formula = forall(a, b, (a | b).has_edge(i, j) == a.has_edge(i, j) | b.has_edge(i, j))
            assert solver.solve(formula)

    # commutativity
    a = UndirectedGraph(num_vertices=n)
    b = UndirectedGraph(num_vertices=n)
    formula = forall(a, b, (a | b) == (b | a))
    assert solver.solve(formula)

    # associativity
    a = UndirectedGraph(num_vertices=n)
    b = UndirectedGraph(num_vertices=n)
    c = UndirectedGraph(num_vertices=n)
    formula = forall(a, b, c, ((a | b) | c) == (a | (b | c)))
    assert solver.solve(formula)


def test_graph_intersection_and_union():
    n = 2
    solver = BruteForceSolver()

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
