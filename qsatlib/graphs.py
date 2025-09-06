from .qsatlib import *


class DirectedGraph(Variable):
    def __init__(self, num_vertices, allow_self_loops=False):
        super().__init__([None] * num_vertices ** 2)
        self.num_vertices = num_vertices
        if not allow_self_loops:
            self.constraint = Node.conj(*[~self._has_edge(i, i) for i in range(num_vertices)])

    @operation
    def __eq__(self, other):
        assert self.num_vertices == other.num_vertices
        result = Boolean()
        result.constraint = (result.node ==
                             Node.conj(*[self.get(i) == other.get(i) for i in range(self.num_vertices ** 2)]))
        return result

    @operation
    def __and__(self, other):
        assert self.num_vertices == other.num_vertices
        intersection = DirectedGraph(num_vertices=self.num_vertices)
        conditions = []
        for i in range(self.num_vertices):
            for j in range(self.num_vertices):
                conditions.append(intersection._has_edge(i, j) == self._has_edge(i, j) & other._has_edge(i, j))
        intersection.constraint &= Node.conj(*conditions)
        return intersection

    @operation
    def __or__(self, other):
        assert self.num_vertices == other.num_vertices
        union = DirectedGraph(num_vertices=self.num_vertices)
        conditions = []
        for i in range(self.num_vertices):
            for j in range(self.num_vertices):
                conditions.append(union._has_edge(i, j) == self._has_edge(i, j) | other._has_edge(i, j))
        union.constraint &= Node.conj(*conditions)
        return union

    def _has_edge(self, i, j):
        return self.get(self.num_vertices * i + j)

    @operation
    def has_edge(self, i, j):
        result = Boolean()
        result.constraint = (result.node == self.get(self.num_vertices * i + j))
        return result


class UndirectedGraph(DirectedGraph):
    def __init__(self, num_vertices, allow_self_loops=False):
        super().__init__(num_vertices=num_vertices,
                         allow_self_loops=allow_self_loops)
        self.constraint &= Node.conj(*[self._has_edge(i, j) == self._has_edge(j, i)
                                       for i in range(self.num_vertices) for j in range(i)])
