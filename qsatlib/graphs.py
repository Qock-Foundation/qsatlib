from qsatlib.qsatlib import *


class DirectedGraph(Variable):
    def __init__(self, num_vertices, allow_self_loops=False):
        super().__init__(num_vertices ** 2)
        self.num_vertices = num_vertices
        if not allow_self_loops:
            self.constraint = conj(*[~self.has_edge(i, i) for i in range(num_vertices)])

    @operation
    def __and__(self, other):
        assert self.num_vertices == other.num_vertices
        intersection = DirectedGraph(num_vertices=self.num_vertices)
        conditions = []
        for i in range(self.num_vertices):
            for j in range(self.num_vertices):
                conditions.append(intersection.has_edge(i, j) == self.has_edge(i, j) & other.has_edge(i, j))
        intersection.constraint &= conj(*conditions)
        return intersection

    @operation
    def __or__(self, other):
        assert self.num_vertices == other.num_vertices
        union = DirectedGraph(num_vertices=self.num_vertices)
        conditions = []
        for i in range(self.num_vertices):
            for j in range(self.num_vertices):
                conditions.append(union.has_edge(i, j) == self.has_edge(i, j) | other.has_edge(i, j))
        union.constraint &= conj(*conditions)
        return union

    @relation
    def has_edge(self, i, j):
        return self[self.num_vertices * i + j]


class UndirectedGraph(DirectedGraph):
    def __init__(self, num_vertices, allow_self_loops=False):
        super().__init__(num_vertices=num_vertices,
                         allow_self_loops=allow_self_loops)
        self.constraint &= conj(*[self.has_edge(i, j) == self.has_edge(j, i)
                                  for i in range(self.num_vertices) for j in range(i)])
