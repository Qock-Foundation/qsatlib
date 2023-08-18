from enum import Enum
from typing import Sequence


# n = Integer(num_bits=4)
# k = Integer(num_bits=4)

# Forall(n, Exists(k, n == k + k))

#            q = Forall x1..10: (x2 => x1 AND x3 => x2 AND ...) =>                                    Forall(...)
#                    Exists x11..x20: (x12 => x11 AND x13 => x12 AND ...) AND                         Exists(...)
#                    (Exists x21..x30:                                                                k + k
#                       (x22 => x21 AND x23 => x22 AND ...) AND                                       k + k
#                       (x21 == (x11 AND x11) AND x22 == (x11 AND x12 OR x12 AND x11) AND ...) AND    k + k
#
#                       (x1 == x21 AND x2 == x22 AND ...)                                             n == k + k
#                    )


class QuantifierType(Enum):
    EXISTS = '∃'
    FORALL = '∀'


class UnaryOperationType(Enum):
    ID = ''
    NOT = '¬'


class BinaryOperationType(Enum):
    AND = '∧'
    OR = '∨'
    XOR = '⊕'
    EQ = '='


class AbstractNode:
    def __invert__(self):
        return UnaryOperationNode(UnaryOperationType.NOT, self)

    def __and__(self, other):
        return BinaryOperationNode(BinaryOperationType.AND, self, other)

    def __or__(self, other):
        return BinaryOperationNode(BinaryOperationType.OR, self, other)

    def __xor__(self, other):
        return BinaryOperationNode(BinaryOperationType.XOR, self, other)

    def __eq__(self, other):
        return BinaryOperationNode(BinaryOperationType.EQ, self, other)


def implies(left: AbstractNode, right: AbstractNode):
    return ~left | right


def conj(seq: Sequence[AbstractNode]):
    if not seq:
        return ConstantNode(True)
    if len(seq) == 1:
        return seq[0]
    return seq[0] & conj(seq[1:])


def disj(seq: Sequence[AbstractNode]):
    if not seq:
        return ConstantNode(False)
    if len(seq) == 1:
        return seq[0]
    return seq[0] | disj(seq[1:])


def eq(seq: Sequence[AbstractNode]):
    if len(seq) <= 1:
        return ConstantNode(True)
    if len(seq) == 2:
        return seq[0] == seq[1]
    return (seq[0] == seq[1]) & eq(seq[1:])


# def eq(left: AbstractNode, right: AbstractNode):
#     return eq([left, right])


class Datatype:
    def __init__(self, num_bits):
        self.bits = [BitNode() for _ in range(num_bits)]

    def is_valid(self):
        return ConstantNode(True)


def exists(variable: Datatype, condition: AbstractNode):
    return QuantifierNode(QuantifierType.EXISTS, variable.bits, variable.is_valid() & condition)


def forall(variable: Datatype, condition: AbstractNode):
    return QuantifierNode(QuantifierType.FORALL, variable.bits, implies(variable.is_valid(), condition))


# just to make sure that you suck
# QuantifierTypeType = class


counter = 0


class BitNode(AbstractNode):
    def __init__(self):
        super().__init__()
        global counter
        counter += 1
        self.id = counter

    def __str__(self):
        return f'x{self.id}'


class ConstantNode(AbstractNode):
    def __init__(self, value: bool):
        super().__init__()
        self.value = value

    def __str__(self):
        return str(int(self.value))


class QuantifierNode(AbstractNode):
    def __init__(self, quantifier: QuantifierType, variables: Sequence[BitNode], child: AbstractNode):
        super().__init__()
        self.quantifier = quantifier
        self.variables = variables
        self.child = child

    def __str__(self):
        return f'{self.quantifier.value}{",".join(map(str, self.variables))} {self.child}'


class UnaryOperationNode(AbstractNode):
    def __init__(self, op_type: UnaryOperationType, child: AbstractNode):
        super().__init__()
        self.op_type = op_type
        self.child = child

    def __str__(self):
        return f'{self.op_type.value}{self.child}'


class BinaryOperationNode(AbstractNode):
    def __init__(self, op_type: BinaryOperationType, child1: AbstractNode, child2: AbstractNode):
        super().__init__()
        self.op_type = op_type
        self.child1 = child1
        self.child2 = child2

    def __str__(self):
        return f'({self.child1} {self.op_type.value} {self.child2})'


class UnaryUnsigned(Datatype):
    def __init__(self, num_bits):
        super().__init__(num_bits)

    def get_bit(self, k):
        return self.bits[k] if 0 <= k < len(self.bits) else ConstantNode(False)

    @staticmethod
    def a_plus_b_is_c(a, b, c):
        conditions = []
        for k in range(1, len(c.bits)):
            # c.(k-1) <=> b.(k-1) or (a.0 and b.(k-2)) or (a.1 and b.(k-3)) or ... or (a.(k-2) and b.0) or a.(k-1)
            conditions.append(eq([c.bits[k - 1], disj([b.get_bit(k - 1)] +
                                                      [a.get_bit(i) & b.get_bit(k - 2 - i) for i in range(k - 1)] +
                                                      [a.get_bit(k - 1)])]))
        return conj(conditions)

    # def __add__(self, other):
    #     tmp = UnaryUnsigned(len(self.bits) + len(other.bits))
    #     return exists(tmp, self.a_plus_b_is_c(self, other, tmp))

    # def __eq__(self, other):
    #     conditions = []
    #     for k in range(max(len(self.bits), len(other.bits))):
    #         conditions.append(eq([self._get_bit(k), other._get_bit(k)]))
    #     return conj(conditions)

    def is_valid(self):
        return conj([implies(self.bits[i], self.bits[i - 1]) for i in range(1, len(self.bits))])

    def __str__(self):
        result = '[unary number'
        for k in range(len(self.bits)):
            result += f' {self.bits[k]}'
        result += ']'
        return result


if __name__ == '__main__':
    n = UnaryUnsigned(num_bits=4)
    m = UnaryUnsigned(num_bits=4)
    res = forall(n, exists(m, UnaryUnsigned.a_plus_b_is_c(m, m, n)))
    print(res)
