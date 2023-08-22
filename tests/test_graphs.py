from qsatlib.graphs import *
from qsatlib.solver import BruteForceSolver


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


def test_vertices():
    solver = BruteForceSolver()
    g = UndirectedGraph(num_vertices=2)
    u, v = g.vertex(), g.vertex()
    formula = forall(u, v, (u == v) | (u != v))
    assert solver.solve(formula)
    g = UndirectedGraph(num_vertices=2)
    u, v = g.vertex(), g.vertex()
    formula = forall(u, v, (u == v) | g.has_edge(u, v))
    assert not solver.solve(formula)
    g = UndirectedGraph(num_vertices=2)
    u, v = g.vertex(), g.vertex()
    formula = forall(u, v, g.has_edge(u, v) | ~g.has_edge(u, v))
    assert solver.solve(formula)
