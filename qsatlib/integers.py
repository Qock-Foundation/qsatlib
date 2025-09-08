from .qsatlib import *


# class UIntUnary(Variable):
#     def __init__(self, num_bits):
#         super().__init__(num_bits)
#         self.constraint = conj(*[implies(self[i], self[i - 1]) for i in range(1, num_bits)])
#
#     @operation
#     def __add__(self, other):
#         result = UIntUnary(num_bits=len(self) + len(other))
#         conditions = []
#         for i in range(-1, len(self) + 1):
#             for j in range(-1, len(other) + 1):
#                 conditions.append(implies(self[i] & other[j], result[i + j + 1]))
#                 conditions.append(implies(~self[i] & ~other[j], ~result[i + j]))
#         result.constraint &= conj(*conditions)
#         return result
#
#     @operation
#     def __mul__(self, other):
#         result = UIntUnary(num_bits=len(self) * len(other))
#         conditions = []
#         for i in range(-1, len(self) + 1):
#             for j in range(-1, len(other) + 1):
#                 conditions.append(implies(self[i] & other[j], result[i * j + i + j]))
#                 conditions.append(implies(~self[i] & ~other[j], ~result[i * j]))
#         result.constraint &= conj(*conditions)
#         return result
#
#     @relation
#     def __getitem__(self, item):
#         if 0 <= item < len(self.bits):
#             return self.bits[item]
#         return ConstantNode(item < 0)
#
#     @relation
#     def __le__(self, other):
#         return conj(*[implies(other[i], self[i]) for i in range(max(len(self), len(other)))])
#
#     @relation
#     def __lt__(self, other):
#         return (self <= other) & (self != other)
#
#     @relation
#     def __ge__(self, other):
#         return other <= self
#
#     @relation
#     def __gt__(self, other):
#         return other < self


class UInt(Variable):
    def __init__(self, width):
        super().__init__([None] * width)

    @staticmethod
    @operation
    def value(val: int, width=None):
        if val < 0:
            raise ValueError('Negative values are not allowed')
        if width is None:
            width = max(1, val.bit_length())
        var = UInt(width)
        var.constraint = Node.conj(*[var.get(i) if (val >> i) & 1 else ~var.get(i) for i in range(width)])
        return var

    @staticmethod
    def zero(width):
        return UInt.value(0, width=width)

    @staticmethod
    def one(width):
        return UInt.value(1, width=width)

    @operation
    def resize(self, width):
        result = deepcopy(self)
        if width <= self.size():
            result.var_nodes = self.var_nodes[:width]
        else:
            new_nodes = [BitNode() for _ in range(width - self.size())]
            result.var_nodes += new_nodes
            result.constraint &= Node.conj(*[~node for node in new_nodes])
        return result

    @staticmethod
    def convert_scalars(func):
        def inner(*args):
            new_args = (UInt.value(arg) if isinstance(arg, int) else arg for arg in args)
            return func(*new_args)

        return inner

    @operation
    def __invert__(self):
        n = self.size()
        result = UInt(n)
        result.constraint &= Node.conj(*[result.get(i) == ~self.get(i) for i in range(n)])
        return result

    @convert_scalars
    @operation
    def __and__(self, other):
        n = min(self.size(), other.size())
        result = UInt(n)
        result.constraint &= Node.conj(*[result.get(i) == self.get(i) & other.get(i) for i in range(n)])
        return result

    @convert_scalars
    @operation
    def __or__(self, other):
        n = max(self.size(), other.size())
        result = UInt(n)
        result.constraint &= Node.conj(*[result.get(i) == self.get_or(i) | other.get_or(i) for i in range(n)])
        return result

    @convert_scalars
    @operation
    def __xor__(self, other):
        n = max(self.size(), other.size())
        result = UInt(n)
        result.constraint &= Node.conj(*[result.get(i) == self.get_or(i) ^ other.get_or(i) for i in range(n)])
        return result

    @convert_scalars
    @operation
    def __eq__(self, other):
        n = max(self.size(), other.size())
        result = Boolean()
        result.constraint = (result.node == Node.conj(*[self.get_or(i) == other.get_or(i) for i in range(n)]))
        return result

    @convert_scalars
    @operation
    def __ne__(self, other):
        return ~(self == other)

    @convert_scalars
    @operation
    def __le__(self, other):
        return (self < other) | (self == other)

    @convert_scalars
    @operation
    def __lt__(self, other):
        n = max(self.size(), other.size())
        result = Boolean()
        options = []
        for i in range(n):
            options.append(Node.conj(~self.get_or(i), other.get_or(i),
                                     *[self.get_or(j) == other.get_or(j) for j in range(i + 1, n)]))
        result.constraint = (result.node == Node.disj(*options))
        return result

    @convert_scalars
    @operation
    def __ge__(self, other):
        return (self > other) | (self == other)

    @convert_scalars
    @operation
    def __gt__(self, other):
        return other < self

    @staticmethod
    def _bit_sum_is(a, b, c, s0, s1=None):  # a + b + c == 2 * s1 + s0
        if s1 is None:
            return s0 == (a ^ b ^ c)
        return (s0 == (a ^ b ^ c)) & (s1 == ((a & b) | (b & c) | (a & c)))

    @staticmethod
    def _sum_is(a, b, c):
        n, m, k = a.size(), b.size(), c.size()
        carry = Variable([None] * min(k, max(n, m) + 1))
        aux_nodes = set(carry.var_nodes)
        constraint = ~carry.get(0)
        for i in range(k):
            if i < carry.size():
                constraint &= UInt._bit_sum_is(
                    a.get_or(i), b.get_or(i), carry.get(i), c.get(i),
                    carry.get(i + 1) if i < carry.size() - 1 else None)
            else:
                constraint &= ~c.get(i)
        return aux_nodes, constraint

    @convert_scalars
    @operation
    def __add__(self, other):
        result = UInt(max(self.size(), other.size()) + 1)
        aux_nodes, constraint = self._sum_is(self, other, result)
        result.aux_nodes |= aux_nodes
        result.constraint &= constraint
        return result

    @convert_scalars
    @operation
    def __radd__(self, other):
        return self + other

    @convert_scalars
    @operation
    def __iadd__(self, other):
        result = UInt(self.size())
        aux_nodes, constraint = self._sum_is(self, other, result)
        result.aux_nodes |= aux_nodes
        result.constraint &= constraint
        return result

    @convert_scalars
    @operation
    def __sub__(self, other):
        result = UInt(self.size())
        cmp = (other + result == self)
        result.aux_nodes |= cmp.aux_nodes
        result.constraint &= cmp.constraint & cmp.node
        return result

    @convert_scalars
    @operation
    def __rsub__(self, other):
        return other - self

    @convert_scalars
    @operation
    def __isub__(self, other):
        result = UInt(self.size())
        cur = result
        cur += other
        cmp = (cur == self)
        result.aux_nodes |= cmp.aux_nodes
        result.constraint &= cmp.constraint & cmp.node
        return result

    @staticmethod
    def _prod_is(a, b, c):
        n, m, k = a.size(), b.size(), c.size()
        aux_nodes = set()
        constraint = ConstantNode(True)
        rs = []
        for i in range(min(m, k)):
            r = UInt(min(k, n + i))
            aux_nodes |= set(r.var_nodes)
            for j in range(i):
                constraint &= ~r.get(j)
            for j in range(i, r.size()):
                constraint &= r.get(j) == (a.get(j - i) & b.get(i))
            rs.append(r)
        s = rs[0]
        for r in rs[1:]:
            s = s + r
            if s.size() > k:
                s = s.resize(k)
        aux_nodes |= s.aux_nodes
        constraint &= s.constraint
        constraint &= Node.conj(*[c.get(i) == s.get_or(i) for i in range(k)])
        return aux_nodes, constraint

    @convert_scalars
    @operation
    def __mul__(self, other):
        result = UInt(self.size() + other.size())
        aux_nodes, constraint = self._prod_is(self, other, result)
        result.aux_nodes |= aux_nodes
        result.constraint &= constraint
        return result

    @convert_scalars
    @operation
    def __rmul__(self, other):
        return self * other

    @convert_scalars
    @operation
    def __imul__(self, other):
        result = UInt(self.size())
        aux_nodes, constraint = self._prod_is(self, other, result)
        result.aux_nodes |= aux_nodes
        result.constraint &= constraint
        return result

    @convert_scalars
    @operation
    def __divmod__(self, other):
        div = UInt(self.size())
        mod = UInt(other.size())
        cmp = (other * div + mod == self) & (mod < other)
        div.aux_nodes |= cmp.aux_nodes
        div.constraint &= cmp.constraint & cmp.node
        mod.aux_nodes |= cmp.aux_nodes
        mod.constraint &= cmp.constraint & cmp.node
        return div, mod

    @convert_scalars
    @operation
    def __floordiv__(self, other):
        return divmod(self, other)[0]

    @convert_scalars
    @operation
    def __mod__(self, other):
        return divmod(self, other)[1]
