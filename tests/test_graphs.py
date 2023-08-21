from qsatlib.graphs import *
from qsatlib.solver import BruteForceSolver


def test_digraph_intersection():
    n = 2
    for i in range(n):
        for j in range(n):
            a = DirectedGraph(num_vertices=n)
            b = DirectedGraph(num_vertices=n)
            formula = forall(a, b, (a & b).has_edge(i, j) == a.has_edge(i, j) & b.has_edge(i, j))
            assert BruteForceSolver().solve(formula)


def test_digraph_union():
    n = 2
    for i in range(n):
        for j in range(n):
            a = DirectedGraph(num_vertices=n)
            b = DirectedGraph(num_vertices=n)
            formula = forall(a, b, (a | b).has_edge(i, j) == a.has_edge(i, j) | b.has_edge(i, j))
            assert BruteForceSolver().solve(formula)
