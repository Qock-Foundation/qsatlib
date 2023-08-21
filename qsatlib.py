from enum import Enum
from typing import Sequence, Any


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
    def __init__(self, bits: Sequence[BitNode]):
        self.bits = bits
        self.constraint = ConstantNode(True)
        self.auxiliary = False

    def __len__(self):
        return len(self.bits)

    def __getitem__(self, item):
        return self.bits[item] if 0 <= item < len(self.bits) else ConstantNode(False)


def exist_seq(variables: Sequence[Variable], formula: Formula):
    return QuantifierNode(QuantifierType.EXISTS, sum([variable.bits for variable in variables], []),
                          conj(*[variable.constraint for variable in variables], formula))

def exist(*variables_and_formula):
    if len(variables_and_formula) == 2 and isinstance(variables_and_formula[0], list):
        return exist_seq(variables_and_formula[0], variables_and_formula[1])
    else:
        return exist_seq(list(variables_and_formula[:-1]), variables_and_formula[-1])

exists = exist

def forall_seq(variables: Sequence[Variable], formula: Formula):
    return QuantifierNode(QuantifierType.FORALL, sum([variable.bits for variable in variables], []),
                          implies(conj(*[variable.constraint for variable in variables]), formula))

def forall(*variables_and_formula):
    if len(variables_and_formula) == 2 and isinstance(variables_and_formula[0], list):
        return forall_seq(variables_and_formula[0], variables_and_formula[1])
    else:
        return forall_seq(list(variables_and_formula[:-1]), variables_and_formula[-1])


# def wrap_auxiliary(variables: Sequence[Variable], formula: Formula):
#     auxiliary_variables = [variable for variable in variables if variable.auxiliary]
#     return exist(auxiliary_variables, formula) if auxiliary_variables else formula


def operation(func):
    def inner(*variables: Variable):
        aux_vars = [variable for variable in variables if variable.auxiliary]
        result = func(*variables)
        result.auxiliary = True
        if aux_vars:
            result.constraint = exist(aux_vars, result.constraint)
        return result

    return inner


def relation(func):
    def inner(*variables: Variable):
        aux_vars = [variable for variable in variables if variable.auxiliary]
        formula = func(*variables)
        if aux_vars:
            formula = exist(aux_vars, formula)
        return formula

    return inner
