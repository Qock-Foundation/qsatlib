from qsatlib.qsatlib import *


class DirectedGraph(Variable):
    def __init__(self, num_vertices, allow_self_loops=False):
        self.num_vertices = num_vertices
        super().__init__([BitNode() for _ in range(num_vertices ** 2)])
        if not allow_self_loops:
            self.constraint = conj(*[~self.outgoing(i)[i] for i in range(num_vertices)])

    @operation
    def __and__(self, other):  # graph intersection
        assert self.num_vertices == other.num_vertices
        intersection = DirectedGraph(num_vertices=self.num_vertices)
        conditions = []
        for i in range(self.num_vertices):
            for j in range(self.num_vertices):
                conditions.append(intersection.outgoing(i)[j] == self.outgoing(i)[j] & other.outgoing(i)[j])
        intersection.constraint &= conj(*conditions)
        return intersection

    @operation
    def __or__(self, other):  # graph union
        assert self.num_vertices == other.num_vertices
        union = DirectedGraph(num_vertices=self.num_vertices)
        conditions = []
        for i in range(self.num_vertices):
            for j in range(self.num_vertices):
                conditions.append(union.outgoing(i)[j] == self.outgoing(i)[j] | other.outgoing(i)[j])
        union.constraint &= conj(*conditions)
        return union

    @operation
    def ingoing(self, i):
        return self.bits[i::self.num_vertices]

    @operation
    def outgoing(self, i):
        return self.bits[i * self.num_vertices:(i + 1) * self.num_vertices]

    @relation
    def has_edge(self, i, j):
        return self.outgoing(i)[j]


class UndirectedGraph(DirectedGraph):
    def __init__(self, num_vertices):
        super().__init__(num_vertices)
        self.constraint &= conj(*[self.outgoing(i)[j] == self.ingoing(i)[j]
                                  for i in range(self.num_vertices) for j in range(i)])
