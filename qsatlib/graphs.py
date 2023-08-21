from qsatlib.qsatlib import *


class DirectedGraph(Variable):
    def __getitem__(self, i):
        return self.bits[i * self.num_vertices:(i + 1) * self.num_vertices]

    def __init__(self, num_vertices):
        self.num_vertices = num_vertices
        num_bits = self.num_vertices * self.num_vertices
        super().__init__([BitNode() for _ in range(num_bits)])
        self.constraint = conj(*[~self[i][i] for i in range(num_vertices)])  # no self-loops

    @operation
    def __and__(self, other):  # graph intersection
        assert self.num_vertices == other.num_vertices
        intersection = DirectedGraph(num_vertices=self.num_vertices)
        conditions = []
        for i in range(self.num_vertices):
            for j in range(self.num_vertices):
                conditions.append(intersection[i][j] == self[i][j] & other[i][j])
        intersection.constraint = conj(intersection.constraint, *conditions)
        return intersection

    @operation
    def __or__(self, other):  # graph union
        assert self.num_vertices == other.num_vertices
        union = DirectedGraph(num_vertices=self.num_vertices)
        conditions = []
        for i in range(self.num_vertices):
            for j in range(self.num_vertices):
                conditions.append(union[i][j] == self[i][j] | other[i][j])
        union.constraint = conj(union.constraint, *conditions)
        return union

    @relation
    def has_edge(self, i, j):
        return self[i][j]
