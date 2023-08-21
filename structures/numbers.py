from qsatlib import *

class UIntUnary(Variable):
    def __init__(self, num_bits):
        super().__init__([BitNode() for _ in range(num_bits)])
        self.constraint = conj(*[implies(self[i], self[i - 1]) for i in range(1, num_bits)])

    @operation
    def __add__(self, other):
        result = UIntUnary(num_bits=len(self) + len(other))
        conditions = []
        for i in range(len(self)):
            for j in range(len(other)):
                conditions.append(implies(self[i] & other[j], result[i + j + 1]))
                conditions.append(implies(~self[i] & ~other[j], ~result[i + j]))
        result.constraint = conj(*conditions)
        return result

    @operation
    def __mul__(self, other):
        result = UIntUnary(num_bits=len(self) * len(other))
        conditions = []
        for i in range(len(self)):
            for j in range(len(other)):
                conditions.append(implies(self[i] & other[j], result[i * j + i + j]))
                conditions.append(implies(~self[i] & ~other[j], ~result[i * j]))
        result.constraint = conj(*conditions)
        return result

    @relation
    def __eq__(self, other):
        return conj(*[self[i] == other[i] for i in range(max(len(self), len(other)))])

    @relation
    def __le__(self, other):
        return conj(*[implies(other[i], self[i]) for i in range(max(len(self), len(other)))])

    @relation
    def __ge__(self, other):
        return conj(*[implies(self[i], other[i]) for i in range(max(len(self), len(other)))])


class UIntBinary(Variable):
    def __init__(self, num_bits):
        super().__init__([BitNode() for _ in range(num_bits)])

    @staticmethod
    def _bit_sum_is(a, b, c, s0, s1):  # a + b + c == 2 * s1 + s0
        return conj(s0 == xor(a, b, c),
                    s1 == disj(a & b, b & c, a & c))

    @operation
    def __add__(self, other):
        assert len(self) == len(other)
        n = len(self)
        result = UIntBinary(num_bits=n)
        carry = UIntBinary(num_bits=n + 1)
        conditions = [~carry[0]]
        for k in range(n):
            conditions.append(UIntBinary._bit_sum_is(self[k], other[k], carry[k], result[k], carry[k + 1]))
        result.constraint = exist(carry, conj(*conditions))
        return result

    @operation
    def __mul__(self, other):
        assert len(self) == len(other)
        n = len(self)
        conditions = []
        r = [UIntBinary(num_bits=n) for _ in range(n)]
        for i in range(n):
            for j in range(i):
                conditions.append(~r[i][j])
            for j in range(i, n):
                conditions.append(r[i][j] == (self[j - i] & other[i]))
        s = r[0]
        for i in range(1, n):
            s = s + r[i]  # Concise
        result = UIntBinary(num_bits=n)
        result.constraint = exist(r, conj(*conditions, result == s))
        return result

    @relation
    def __eq__(self, other):
        assert len(self) == len(other)
        return conj(*[self[i] == other[i] for i in range(len(self))])

    @relation
    def __le__(self, other):
        assert len(self) == len(other)
        options = [self == other]
        for i in range(len(self)):
            options.append(conj(~self[i], other[i],
                                *[self[j] == other[j] for j in range(i + 1, len(self))]))
        return disj(*options)

    @relation
    def __ge__(self, other):
        assert len(self) == len(other)
        options = [self == other]
        for i in range(len(self)):
            options.append(conj(self[i], ~other[i],
                                *[self[j] == other[j] for j in range(i + 1, len(self))]))
        return disj(*options)