from qsatlib.graphs import *
from qsatlib.solver import BruteForceSolver


def test_digraph_equality():
    n = 2
    # Commutativity of ==
    a = DirectedGraph(num_vertices=n)
    b = DirectedGraph(num_vertices=n)
    formula = forall(a, b, implies(a == b, b == a))
    assert BruteForceSolver().solve(formula)

    # Commutativity of !=
    a = DirectedGraph(num_vertices=n)
    b = DirectedGraph(num_vertices=n)
    formula = forall(a, b, implies(a != b, b != a))
    assert BruteForceSolver().solve(formula)

    # Transitivity of ==
    a = DirectedGraph(num_vertices=n)
    b = DirectedGraph(num_vertices=n)
    c = DirectedGraph(num_vertices=n)
    formula = forall(a, b, c, implies((a == b) & (b == c), a == c))
    assert BruteForceSolver().solve(formula)

    # Transitivity of !=
    a = DirectedGraph(num_vertices=n)
    b = DirectedGraph(num_vertices=n)
    c = DirectedGraph(num_vertices=n)
    formula = forall(a, b, c, implies((a != b) & (b != c), a != c))
    assert not BruteForceSolver().solve(formula)

    # now together
    a = DirectedGraph(num_vertices=n)
    b = DirectedGraph(num_vertices=n)
    c = DirectedGraph(num_vertices=n)
    formula = forall(a, b, c, implies((a == b) & (b != c), a != c))
    assert BruteForceSolver().solve(formula)


def test_digraph_intersection():
    n = 2
    # definition
    for i in range(n):
        for j in range(n):
            a = DirectedGraph(num_vertices=n)
            b = DirectedGraph(num_vertices=n)
            formula = forall(a, b, (a & b).has_edge(i, j) == a.has_edge(i, j) & b.has_edge(i, j))
            assert BruteForceSolver().solve(formula)
    # commutativity
    a = DirectedGraph(num_vertices=n)
    b = DirectedGraph(num_vertices=n)
    formula = forall(a, b, (a & b) == (b & a))
    assert BruteForceSolver().solve(formula)
    # associativity
    a = DirectedGraph(num_vertices=n)
    b = DirectedGraph(num_vertices=n)
    c = DirectedGraph(num_vertices=n)
    formula = forall(a, b, c, ((a & b) & c) == (a & (b & c)))
    assert BruteForceSolver().solve(formula)


def test_digraph_union():
    n = 2
    # definition
    for i in range(n):
        for j in range(n):
            a = DirectedGraph(num_vertices=n)
            b = DirectedGraph(num_vertices=n)
            formula = forall(a, b, (a | b).has_edge(i, j) == a.has_edge(i, j) | b.has_edge(i, j))
            assert BruteForceSolver().solve(formula)
    # commutativity
    a = DirectedGraph(num_vertices=n)
    b = DirectedGraph(num_vertices=n)
    formula = forall(a, b, (a | b) == (b | a))
    assert BruteForceSolver().solve(formula)
    # associativity
    a = DirectedGraph(num_vertices=n)
    b = DirectedGraph(num_vertices=n)
    c = DirectedGraph(num_vertices=n)
    formula = forall(a, b, c, ((a | b) | c) == (a | (b | c)))
    assert BruteForceSolver().solve(formula)

    
def test_digraph_intersection_and_union():
    n = 2
    # write a test for ((a | b) & c) == ((a & c) | (b & c))
    a = DirectedGraph(num_vertices=n)
    b = DirectedGraph(num_vertices=n)
    c = DirectedGraph(num_vertices=n)
    formula = forall(a, b, c, ((a | b) & c) == ((a & c) | (b & c)))
    assert BruteForceSolver().solve(formula)
    
    # write a test for ((a & b) | c) == ((a | c) & (b | c))
    a = DirectedGraph(num_vertices=n)
    b = DirectedGraph(num_vertices=n)
    c = DirectedGraph(num_vertices=n)
    formula = forall(a, b, c, ((a & b) | c) == ((a | c) & (b | c)))
    assert BruteForceSolver().solve(formula)
