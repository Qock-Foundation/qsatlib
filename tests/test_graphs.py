from qsatlib.graphs import *


def test_digraph_set_operations():
    n = 5
    a = DirectedGraph(num_vertices=n)
    b = DirectedGraph(num_vertices=n)
    c = DirectedGraph(num_vertices=n)

    # definition of intersection
    for i in range(n):
        for j in range(n):
            formula = forall(a, b, (a & b).has_edge(i, j) == a.has_edge(i, j) & b.has_edge(i, j))
            assert formula.eval()

    # commutativity of intersection
    formula = forall(a, b, (a & b) == (b & a))
    assert formula.eval()

    # associativity of intersection
    formula = forall(a, b, c, ((a & b) & c) == (a & (b & c)))
    assert formula.eval()

    # definition of union
    for i in range(n):
        for j in range(n):
            formula = forall(a, b, (a | b).has_edge(i, j) == a.has_edge(i, j) | b.has_edge(i, j))
            assert formula.eval()

    # commutativity of union
    formula = forall(a, b, (a | b) == (b | a))
    assert formula.eval()

    # associativity of union
    formula = forall(a, b, c, ((a | b) | c) == (a | (b | c)))
    assert formula.eval()

    # (a | b) & c == (a & c) | (b & c)
    formula = forall(a, b, c, ((a | b) & c) == ((a & c) | (b & c)))
    assert formula.eval()

    # (a & b) | c == (a | c) & (b | c)
    formula = forall(a, b, c, ((a & b) | c) == ((a | c) & (b | c)))
    assert formula.eval()


def test_graph_set_operations():
    n = 5
    a = UndirectedGraph(num_vertices=n)
    b = UndirectedGraph(num_vertices=n)
    c = UndirectedGraph(num_vertices=n)

    # definition of intersection
    for i in range(n):
        for j in range(n):
            formula = forall(a, b, (a & b).has_edge(i, j) == a.has_edge(i, j) & b.has_edge(i, j))
            assert formula.eval()

    # commutativity of intersection
    formula = forall(a, b, (a & b) == (b & a))
    assert formula.eval()

    # associativity of intersection
    formula = forall(a, b, c, ((a & b) & c) == (a & (b & c)))
    assert formula.eval()

    # definition of union
    for i in range(n):
        for j in range(n):
            formula = forall(a, b, (a | b).has_edge(i, j) == a.has_edge(i, j) | b.has_edge(i, j))
            assert formula.eval()

    # commutativity of union
    formula = forall(a, b, (a | b) == (b | a))
    assert formula.eval()

    # associativity of union
    formula = forall(a, b, c, ((a | b) | c) == (a | (b | c)))
    assert formula.eval()

    # (a | b) & c == (a & c) | (b & c)
    formula = forall(a, b, c, ((a | b) & c) == ((a & c) | (b & c)))
    assert formula.eval()

    # (a & b) | c == (a | c) & (b | c)
    formula = forall(a, b, c, ((a & b) | c) == ((a | c) & (b | c)))
    assert formula.eval()
