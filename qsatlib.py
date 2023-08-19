from enum import Enum
from typing import Sequence


class QuantifierType(Enum):
    EXISTS = '∃'
    FORALL = '∀'


class OperationType(Enum):
    NOT = '¬'
    AND = '∧'
    OR = '∨'
    XOR = '⊕'
    EQ = '='


class Formula:
    def __invert__(self):
        return OperationNode(OperationType.NOT, self)

    def __and__(self, other):
        return OperationNode(OperationType.AND, self, other)

    def __or__(self, other):
        return OperationNode(OperationType.OR, self, other)

    def __xor__(self, other):
        return OperationNode(OperationType.XOR, self, other)

    def __eq__(self, other):
        return OperationNode(OperationType.EQ, self, other)


counter = 0


class BitNode(Formula):
    def __init__(self):
        super().__init__()
        global counter
        counter += 1
        self.id = counter

    def __str__(self):
        return f'x{self.id}'


class ConstantNode(Formula):
    def __init__(self, value: bool):
        super().__init__()
        self.value = value

    def __str__(self):
        return str(int(self.value))


class QuantifierNode(Formula):
    def __init__(self, quantifier: QuantifierType, variables: Sequence[BitNode], child: Formula):
        super().__init__()
        self.quantifier = quantifier
        self.variables = variables
        self.child = child

    def __str__(self):
        return f'{self.quantifier.value}{",".join(map(str, self.variables))} {self.child}'


class OperationNode(Formula):
    def __init__(self, op_type: OperationType, *children: Formula):
        super().__init__()
        self.op_type = op_type
        self.children = children

    def __str__(self):
        if self.op_type == OperationType.NOT:
            return f'{self.op_type.value}{self.children[0]}'
        if len(self.children) == 1:
            return str(self.children[0])
        return '(' + f' {self.op_type.value} '.join(map(str, self.children)) + ')'


def implies(left: Formula, right: Formula):
    return ~left | right


def conj(*formulas: Formula):
    if not formulas:
        return ConstantNode(True)
    return OperationNode(OperationType.AND, *formulas)


def disj(*formulas: Formula):
    if not formulas:
        return ConstantNode(False)
    return OperationNode(OperationType.OR, *formulas)


def xor(*formulas: Formula):
    if not formulas:
        return ConstantNode(False)
    return OperationNode(OperationType.XOR, *formulas)


def eq(*formulas: Formula):
    return conj(*[formulas[i] == formulas[0] for i in range(1, len(formulas))])


class Variable:
    def __init__(self, bits: Sequence[BitNode], auxiliary=False):
        self.bits = bits
        self.constraints = []
        self.auxiliary = auxiliary

    def __len__(self):
        return len(self.bits)

    def __getitem__(self, item):
        return self.bits[item] if 0 <= item < len(self.bits) else ConstantNode(False)

    def constraints_formula(self):
        return conj(*self.constraints)


def exist(variables: Sequence[Variable], formula: Formula):
    return QuantifierNode(QuantifierType.EXISTS, sum([variable.bits for variable in variables], []),
                          conj(*[variable.constraints_formula() for variable in variables], formula))


def forall(variables: Sequence[Variable], formula: Formula):
    return QuantifierNode(QuantifierType.FORALL, sum([variable.bits for variable in variables], []),
                          implies(conj(*[variable.constraints_formula() for variable in variables]), formula))


def wrap_auxiliary(variables: Sequence[Variable], formula: Formula):
    auxiliary_variables = [variable for variable in variables if variable.auxiliary]
    return exist(auxiliary_variables, formula) if auxiliary_variables else formula


class UIntUnary(Variable):
    def __init__(self, num_bits, auxiliary=False):
        super().__init__(bits=[BitNode() for _ in range(num_bits)],
                         auxiliary=auxiliary)
        for i in range(1, num_bits):
            self.constraints.append(implies(self[i], self[i - 1]))

    def __add__(self, other):
        result = UIntUnary(num_bits=len(self) + len(other), auxiliary=True)
        conditions = []
        for i in range(len(self)):
            for j in range(len(other)):
                conditions.append(implies(self[i] & other[j], result[i + j + 1]))
                conditions.append(implies(~self[i] & ~other[j], ~result[i + j]))
        result.constraints.append(wrap_auxiliary([self, other], conj(*conditions)))
        return result

    def __mul__(self, other):
        result = UIntUnary(num_bits=len(self) * len(other), auxiliary=True)
        conditions = []
        for i in range(len(self)):
            for j in range(len(other)):
                conditions.append(implies(self[i] & other[j], result[i * j + i + j]))
                conditions.append(implies(~self[i] & ~other[j], ~result[i * j]))
        result.constraints.append(wrap_auxiliary([self, other], conj(*conditions)))
        return result

    def __eq__(self, other):
        return wrap_auxiliary([self, other],
                              conj(*[self[i] == other[i] for i in range(max(len(self), len(other)))]))

    def __le__(self, other):
        return wrap_auxiliary([self, other],
                              conj(*[implies(other[i], self[i]) for i in range(max(len(self), len(other)))]))

    def __ge__(self, other):
        return other <= self


class UIntBinary(Variable):
    def __init__(self, num_bits, auxiliary=False):
        super().__init__(bits=[BitNode() for _ in range(num_bits)],
                         auxiliary=auxiliary)

    @staticmethod
    def _bit_sum_is(a, b, c, s0, s1):  # a + b + c == 2 * s1 + s0
        return conj(s0 == xor(a, b, c),
                    s1 == disj(a & b, b & c, a & c))

    def __add__(self, other):
        assert len(self) == len(other)
        n = len(self)
        result = UIntBinary(num_bits=n, auxiliary=True)
        carry = UIntBinary(num_bits=n + 1, auxiliary=True)
        conditions = [~carry[0]]
        for k in range(n):
            conditions.append(UIntBinary._bit_sum_is(self[k], other[k], carry[k], result[k], carry[k + 1]))
        result.constraints.append(wrap_auxiliary([self, other, carry], conj(*conditions)))
        return result

    def __mul__(self, other):
        assert len(self) == len(other)
        n = len(self)
        conditions = []
        r = [UIntBinary(num_bits=n, auxiliary=True) for _ in range(n)]
        for i in range(n):
            for j in range(i):
                conditions.append(~r[i][j])
            for j in range(i, n):
                conditions.append(r[i][j] == (self[j - i] & other[i]))
        result = r[0]
        for i in range(1, n):
            result = result + r[i]  # Really nice!
        result.constraints.append(wrap_auxiliary([self, other] + r, conj(*conditions)))
        return result

    def __eq__(self, other):
        assert len(self) == len(other)
        return wrap_auxiliary([self, other],
                              conj(*[self[i] == other[i] for i in range(len(self))]))

    def __le__(self, other):
        assert len(self) == len(other)
        options = [self == other]
        for i in range(len(self)):
            options.append(conj(~self[i], other[i],
                                *[self[j] == other[j] for j in range(i + 1, len(self))]))
        return wrap_auxiliary([self, other], disj(*options))

    def __ge__(self, other):
        return other <= self
