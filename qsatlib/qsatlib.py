import subprocess
import sys
from copy import deepcopy
from enum import Enum
from typing import Sequence, Tuple, Dict

sys.setrecursionlimit(10 ** 8)


class QuantifierType(Enum):
    EXISTS = '∃'
    FORALL = '∀'
    EXISTS_UNIQUE = '∃!'


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

    def __ne__(self, other):
        return ~(self == other)

    def pnf(self):
        return formula2pnf(self)

    def pcnf(self):
        return pnf2pcnf(formula2pnf(self))


_VAR_CNT = 0


class BitNode(Formula):
    def __init__(self):
        super().__init__()
        global _VAR_CNT
        _VAR_CNT += 1
        self.id = _VAR_CNT

    def __str__(self):
        return f'x{self.id}'

    def __hash__(self):
        return self.id


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


class Variable:
    def __init__(self, num_bits):
        self.bits = [BitNode() for _ in range(num_bits)]
        self.constraint = ConstantNode(True)
        self.aux_bits = set()

    def size(self):
        return len(self.bits)

    def get(self, item):
        if not 0 <= item < len(self.bits):
            raise ValueError(f'Index {item} is outside [0; {len(self.bits) - 1}]')
        return self.bits[item]

    def get_or(self, item, default=ConstantNode(False)):
        return self.bits[item] if 0 <= item < len(self.bits) else default


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


def extract_bits_constraint(variables):
    bits, constraint = [], ConstantNode(True)
    for variable in variables:
        if isinstance(variable, Variable):
            bits += variable.bits
            constraint &= variable.constraint
        elif isinstance(variable, BitNode):
            bits += [variable]
    return bits, constraint


def exist(*variables_and_formula):
    variables, formula = list(variables_and_formula[:-1]), variables_and_formula[-1]
    bits, constraint = extract_bits_constraint(variables)
    return QuantifierNode(QuantifierType.EXISTS, bits, constraint & formula)


def forall(*variables_and_formula):
    variables, formula = list(variables_and_formula[:-1]), variables_and_formula[-1]
    bits, constraint = extract_bits_constraint(variables)
    return QuantifierNode(QuantifierType.FORALL, bits, implies(constraint, formula))


def exist_unique(*variables_and_formula):
    variables, formula = list(variables_and_formula[:-1]), variables_and_formula[-1]
    bits, constraint = extract_bits_constraint(variables)
    return QuantifierNode(QuantifierType.EXISTS_UNIQUE, bits, constraint & formula)


def operation(func):
    def inner(*args, **kwargs):
        aux_bits = set()
        constraint = ConstantNode(True)
        for var in args + tuple(kwargs.values()):
            if not isinstance(var, Variable):
                continue
            aux_bits |= var.aux_bits
            constraint &= var.constraint
            var.aux_bits.clear()
        result = func(*args, **kwargs)
        result.aux_bits |= aux_bits | set(result.bits)
        result.constraint &= constraint
        return result

    return inner


def relation(func):
    def inner(*args, **kwargs):
        aux_bits = set()
        constraint = ConstantNode(True)
        for var in args + tuple(kwargs.values()):
            if not isinstance(var, Variable):
                continue
            aux_bits |= var.aux_bits
            constraint &= var.constraint
            var.aux_bits.clear()
        formula = func(*args, **kwargs)
        if aux_bits:
            formula = exist(*aux_bits, constraint & formula)
        return formula

    return inner


class PNF:
    def __init__(self, quantifiers, formula):
        self.quantifiers = quantifiers
        self.formula = formula

    def __str__(self):
        return ' '.join([q.value + str(q_var) for q, q_var in self.quantifiers]) + ' ' + str(self.formula)


def def_pnf(formula: PNF) -> Tuple[PNF, BitNode]:
    x = BitNode()
    if not formula.quantifiers:
        return PNF([], x == formula.formula), x
    q = formula.quantifiers[0][0]
    r = 0
    while r < len(formula.quantifiers) and formula.quantifiers[r][0] == q:
        r += 1
    ais = [BitNode() for _ in range(r)]
    bis = [formula.quantifiers[i][1] for i in range(r)]
    child_pnf, y = def_pnf(PNF(formula.quantifiers[r:], formula.formula))
    child_pnf = negate_pnf(child_pnf)
    quantifiers = [(QuantifierType.EXISTS, a) for a in ais]
    quantifiers += [(QuantifierType.FORALL, b) for b in bis]
    quantifiers += [(QuantifierType.FORALL, y)]
    quantifiers += child_pnf.quantifiers
    neq = disj(*[a != b for a, b in zip(ais, bis)])
    if q == QuantifierType.EXISTS:
        return PNF(quantifiers, child_pnf.formula | ((neq | ~x | y) & (x | ~y))), x
        # return PNF(quantifiers, child_pnf.formula | ((neq | ~x | ~y) & (x | y))), x
    else:
        return PNF(quantifiers, child_pnf.formula | ((neq | x | ~y) & (~x | y))), x
        # return PNF(quantifiers, child_pnf.formula | ((neq | x | y) & (~x | ~y))), x


def negate_pnf(formula: PNF) -> PNF:
    quantifiers = []
    for q, q_var in formula.quantifiers:
        q_neg = QuantifierType.FORALL if q == QuantifierType.EXISTS else QuantifierType.EXISTS
        quantifiers.append((q_neg, q_var))
    return PNF(quantifiers, ~formula.formula)


def conj_pnf(formula1: PNF, formula2: PNF) -> PNF:
    return PNF(formula1.quantifiers + formula2.quantifiers, formula1.formula & formula2.formula)


def disj_pnf(formula1: PNF, formula2: PNF) -> PNF:
    return PNF(formula1.quantifiers + formula2.quantifiers, formula1.formula | formula2.formula)


def xor_pnf(formula1: PNF, formula2: PNF) -> PNF:
    if not formula1.quantifiers and not formula2.quantifiers:
        return PNF([], formula1.formula ^ formula2.formula)

    # formula1_neg = negate_pnf(clone_pnf(formula1, {}))
    # formula2_neg = negate_pnf(clone_pnf(formula2, {}))
    # quantifiers = formula1.quantifiers + formula1_neg.quantifiers + formula2.quantifiers + formula2_neg.quantifiers
    # formula = (formula1.formula | formula2.formula) & (formula1_neg.formula | formula2_neg.formula)
    # formula = (formula1_neg.formula & formula2.formula) | (formula1.formula & formula2_neg.formula)

    formula1, x1 = def_pnf(formula1)
    formula2, x2 = def_pnf(formula2)
    quantifiers = [(QuantifierType.EXISTS, x1), (QuantifierType.EXISTS, x2)]
    quantifiers += formula1.quantifiers + formula2.quantifiers
    formula = formula1.formula & formula2.formula & (x1 ^ x2)
    return PNF(quantifiers, formula)


def eq_pnf(formula1: PNF, formula2: PNF) -> PNF:
    if not formula1.quantifiers and not formula2.quantifiers:
        return PNF([], formula1.formula == formula2.formula)

    # formula1_neg = negate_pnf(clone_pnf(formula1, {}))
    # formula2_neg = negate_pnf(clone_pnf(formula2, {}))
    # quantifiers = formula1.quantifiers + formula1_neg.quantifiers + formula2.quantifiers + formula2_neg.quantifiers
    # formula = (formula1_neg.formula | formula2.formula) & (formula1.formula | formula2_neg.formula)
    # formula = (formula1.formula & formula2.formula) | (formula1_neg.formula & formula2_neg.formula)

    formula1, x1 = def_pnf(formula1)
    formula2, x2 = def_pnf(formula2)
    quantifiers = [(QuantifierType.EXISTS, x1), (QuantifierType.EXISTS, x2)]
    quantifiers += formula1.quantifiers + formula2.quantifiers
    formula = formula1.formula & formula2.formula & (x1 == x2)
    return PNF(quantifiers, formula)


def clone_pnf(orig: PNF, replacements: Dict[BitNode, BitNode]):
    quantifiers = []
    for q_type, q_var in orig.quantifiers:
        if q_var not in replacements.keys():
            replacements[q_var] = BitNode()
        quantifiers.append((q_type, replacements[q_var]))
    formula = rename_formula(orig.formula, replacements)
    return PNF(quantifiers, formula)


def rename_formula(formula: Formula, replacements: Dict[BitNode, BitNode]) -> Formula:
    if isinstance(formula, BitNode):
        return replacements[formula] if formula in replacements.keys() else formula

    if isinstance(formula, ConstantNode):
        return formula

    if isinstance(formula, OperationNode):
        new_formula = deepcopy(formula)
        new_formula.children = [rename_formula(child, replacements) for child in formula.children]
        return new_formula

    raise ValueError('Node not recognised')


def formula2pnf(formula: Formula) -> PNF:
    if isinstance(formula, BitNode):
        return PNF([], formula)

    if isinstance(formula, ConstantNode):
        return PNF([], formula)

    if isinstance(formula, QuantifierNode):
        if formula.quantifier == QuantifierType.EXISTS_UNIQUE:
            ais = [BitNode() for _ in range(len(formula.variables))]
            bis = formula.variables
            # replacements = {b: a for a, b in zip(ais, bis)}
            # child = formula2pnf(formula.child)
            # new_child = clone_pnf(child, replacements)
            # neg_child = negate_pnf(child)
            # quantifiers = [(QuantifierType.EXISTS, a) for a in ais]
            # quantifiers += [(QuantifierType.FORALL, b) for b in bis]
            # quantifiers += new_child.quantifiers
            # quantifiers += neg_child.quantifiers
            # eq = conj(*[a == b for a, b in zip(ais, bis)])
            # return PNF(quantifiers, new_child.formula & (neg_child.formula | eq))

            child_pnf, y = def_pnf(formula2pnf(formula.child))
            child_pnf = negate_pnf(child_pnf)
            quantifiers = [(QuantifierType.EXISTS, a) for a in ais]
            quantifiers += [(QuantifierType.FORALL, b) for b in bis]
            quantifiers += [(QuantifierType.FORALL, y)]
            quantifiers += child_pnf.quantifiers
            eq = conj(*[a == b for a, b in zip(ais, bis)])
            return PNF(quantifiers, child_pnf.formula | (eq == y))

        child_pnf = formula2pnf(formula.child)
        quantifiers = [(formula.quantifier, x) for x in formula.variables]
        quantifiers += child_pnf.quantifiers
        return PNF(quantifiers, child_pnf.formula)

    if isinstance(formula, OperationNode):
        if formula.op_type == OperationType.NOT:
            child_pnf = formula2pnf(formula.children[0])
            return negate_pnf(child_pnf)

        op_pnf_dict = {
            OperationType.AND: conj_pnf,
            OperationType.OR: disj_pnf,
            OperationType.XOR: xor_pnf,
            OperationType.EQ: eq_pnf
        }
        op_pnf = op_pnf_dict[formula.op_type]
        children_pnf = [formula2pnf(child) for child in formula.children]
        result = children_pnf[0]
        for child_pnf in children_pnf[1:]:
            result = op_pnf(result, child_pnf)
        return result

    raise ValueError('Node not recognised')


class PCNF:
    def __init__(self, quantifiers, cnf):
        self.quantifiers = quantifiers
        self.cnf = cnf

    def __str__(self):
        return (' '.join([q.value + str(q_var) for q, q_var in self.quantifiers]) + ' ' +
                ' ∧ '.join(map(lambda term: '(' + ' ∨ '.join(map(str, term)) + ')', self.cnf)))

    def eval(self):
        return eval_pcnf(self)


def pnf2pcnf(formula: PNF) -> PCNF:
    quantifiers = formula.quantifiers
    cnf = []

    def compute_cnf(node) -> BitNode:
        if isinstance(node, BitNode):
            return node

        x = BitNode()
        quantifiers.append((QuantifierType.EXISTS, x))

        if isinstance(node, ConstantNode):
            cnf.append([x] if node.value else [~x])
            return x

        if isinstance(node, OperationNode):
            if node.op_type == OperationType.NOT:
                y = compute_cnf(node.children[0])
                cnf.extend([[x, y], [~x, ~y]])
            elif node.op_type == OperationType.AND:
                children_nodes = [compute_cnf(child) for child in node.children]
                cnf.extend([[~x, y] for y in children_nodes])
                cnf.append([x, *[~y for y in children_nodes]])
            elif node.op_type == OperationType.OR:
                children_nodes = [compute_cnf(child) for child in node.children]
                cnf.extend([[x, ~y] for y in children_nodes])
                cnf.append([~x, *[y for y in children_nodes]])
            elif node.op_type == OperationType.XOR:
                assert len(node.children) == 2
                y = compute_cnf(node.children[0])
                z = compute_cnf(node.children[1])
                cnf.extend([[~x, y, z], [~x, ~y, ~z], [x, ~y, z], [x, y, ~z]])
            elif node.op_type == OperationType.EQ:
                assert len(node.children) == 2
                y = compute_cnf(node.children[0])
                z = compute_cnf(node.children[1])
                cnf.extend([[x, y, z], [x, ~y, ~z], [~x, ~y, z], [~x, y, ~z]])
            else:
                raise ValueError('Operation not recognised')

            return x

        raise ValueError('Node not recognised')

    value = compute_cnf(formula.formula)
    cnf.append([value])
    return PCNF(quantifiers, cnf)


def eval_pcnf(formula: PCNF) -> bool:
    instance_filename = 'instance.qdimacs'
    caqe_filename = 'caqe/target/release/caqe'

    with open(instance_filename, 'w') as fout:
        print(f'p cnf {len(formula.quantifiers)} {len(formula.cnf)}', file=fout)
        for q_type, q_var in formula.quantifiers:
            ch = 'e' if q_type == QuantifierType.EXISTS else 'a'
            print(ch, q_var.id, 0, file=fout)
        for clause in formula.cnf:
            for elem in clause:
                var_id = -elem.children[0].id if isinstance(elem, OperationNode) else elem.id
                print(var_id, end=' ', file=fout)
            print(0, file=fout)

    cmd = [caqe_filename, instance_filename]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 10:
        return True
    if result.returncode == 20:
        return False
    raise ValueError(f'Caqe exited with code {result.returncode}')
