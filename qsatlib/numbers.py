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
        super().__init__(width)

    @staticmethod
    @operation
    def value(val, width=None):
        if not isinstance(val, int):
            raise ValueError('Unsupported value type')
        if val < 0:
            raise ValueError('Negative values are not allowed')
        if width is None:
            width = max(1, val.bit_length())
        var = UInt(width)
        var.constraint = conj(*[var.get(i) if (val >> i) & 1 else ~var.get(i) for i in range(width)])
        return var

    @staticmethod
    def zero(width):
        return UInt.value(0, width=width)

    @staticmethod
    def one(width):
        return UInt.value(1, width=width)

    @operation
    def resize(self, width):
        res = UInt(width)
        res.constraint = conj(*[res.get(i) == self.get_or(i) for i in range(width)])
        return res

    @staticmethod
    def convert_scalars(func):
        def inner(*args):
            new_args = (UInt.value(arg) if isinstance(arg, int) else arg for arg in args)
            return func(*new_args)
        return inner

    @convert_scalars
    @relation
    def __eq__(self, other):
        return conj(*[self.get_or(i) == other.get_or(i) for i in range(max(self.size(), other.size()))])

    @convert_scalars
    @relation
    def __ne__(self, other):
        return ~(self == other)

    @convert_scalars
    @relation
    def __le__(self, other):
        return (self < other) | (self == other)

    @convert_scalars
    @relation
    def __lt__(self, other):
        options = []
        n = max(self.size(), other.size())
        for i in range(n):
            options.append(conj(~self.get_or(i), other.get_or(i),
                                *[self.get_or(j) == other.get_or(j) for j in range(i + 1, n)]))
        return disj(*options)

    @convert_scalars
    @relation
    def __ge__(self, other):
        return (self > other) | (self == other)

    @convert_scalars
    @relation
    def __gt__(self, other):
        return other < self

    @staticmethod
    def _bit_sum_is(a, b, c, s0, s1):  # a + b + c == 2 * s1 + s0
        return conj(s0 == xor(a, b, c),
                    s1 == disj(a & b, b & c, a & c))

    @staticmethod
    def _sum_is(a, b, c):
        n = c.size()
        carry = Variable(n + 1)
        conditions = [~carry.get(0)]
        for k in range(n):
            conditions.append(UInt._bit_sum_is(
                a.get_or(k), b.get_or(k), carry.get(k), c.get(k), carry.get(k + 1)))
        return exist(carry, conj(*conditions))

    @convert_scalars
    @operation
    def __add__(self, other):
        result = UInt(max(self.size(), other.size()) + 1)
        result.constraint &= self._sum_is(self, other, result)
        return result

    @convert_scalars
    @operation
    def __radd__(self, other):
        return self + other

    @convert_scalars
    @operation
    def __iadd__(self, other):
        result = UInt(self.size())
        result.constraint &= self._sum_is(self, other, result)
        return result

    @staticmethod
    def _prod_is(a, b, c):
        n = c.size()
        conditions = []
        r = [UInt(n) for _ in range(n)]
        for i in range(n):
            for j in range(i):
                conditions.append(~r[i].get(j))
            for j in range(i, n):
                conditions.append(r[i].get(j) == (a.get_or(j - i) & b.get_or(i)))
        s = r[0]
        for elem in r[1:]:
            s += elem
        return exist(*r, conj(*conditions, s == c))

    @convert_scalars
    @operation
    def __mul__(self, other):
        result = UInt(self.size() + other.size())
        result.constraint &= self._prod_is(self, other, result)
        return result

    @convert_scalars
    @operation
    def __rmul__(self, other):
        return self * other

    @convert_scalars
    @operation
    def __imul__(self, other):
        result = UInt(self.size())
        result.constraint &= self._prod_is(self, other, result)
        return result

    @convert_scalars
    @operation
    def __and__(self, other):
        n = min(self.size(), other.size())
        result = UInt(n)
        result.constraint &= conj(*[result.get(i) == (self.get(i) & other.get(i)) for i in range(n)])
        return result

    @convert_scalars
    @operation
    def __or__(self, other):
        n = max(self.size(), other.size())
        result = UInt(n)
        result.constraint &= conj(*[result.get(i) == (self.get_or(i) | other.get_or(i)) for i in range(n)])
        return result

    @operation
    def __invert__(self):
        n = self.size()
        result = UInt(n)
        result.constraint &= conj(*[result.get(i) == ~self.get(i) for i in range(n)])
        return result
