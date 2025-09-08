import subprocess
import sys
from copy import copy
from enum import Enum
from typing import Iterable, Optional, Dict

sys.setrecursionlimit(10 ** 7)


class QuantifierType(Enum):
    EXISTS = '∃'
    FORALL = '∀'


class OperationType(Enum):
    NOT = '¬'
    AND = '∧'
    OR = '∨'
    XOR = '⊕'
    EQ = '='


class Node:
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

    def implies(self, other):
        return ~self | other

    @staticmethod
    def conj(*nodes):
        res = ConstantNode(True)
        for node in nodes:
            res = res & node
        return res

    @staticmethod
    def disj(*nodes):
        res = ConstantNode(False)
        for node in nodes:
            res = res | node
        return res

    @staticmethod
    def xor(*nodes):
        res = ConstantNode(False)
        for node in nodes:
            res = res ^ node
        return res

    def rename(self, replacements: Dict):
        if isinstance(self, BitNode):
            return replacements[self] if self in replacements.keys() else self
        if isinstance(self, ConstantNode):
            return self
        if isinstance(self, QuantifierNode):
            res = copy(self)
            res.child = self.child.rename(replacements)
            return res
        if isinstance(self, OperationNode):
            res = copy(self)
            res.children = [child.rename(replacements) for child in self.children]
            return res
        raise ValueError('Unknown node')

    def pnf(self):
        if isinstance(self, BitNode) or isinstance(self, ConstantNode):
            return PNF([], self)
        if isinstance(self, QuantifierNode):
            child_pnf = self.child.pnf()
            quantifiers = [(self.quantifier, x) for x in self.variables]
            quantifiers += child_pnf.quantifiers
            return PNF(quantifiers, child_pnf.node)
        if isinstance(self, OperationNode):
            if self.op_type == OperationType.NOT:
                return ~self.children[0].pnf()
            child1_pnf = self.children[0].pnf()
            child2_pnf = self.children[1].pnf()
            if self.op_type == OperationType.AND:
                return child1_pnf & child2_pnf
            if self.op_type == OperationType.OR:
                return child1_pnf | child2_pnf
            if self.op_type == OperationType.XOR:
                return child1_pnf ^ child2_pnf
            if self.op_type == OperationType.EQ:
                return child1_pnf == child2_pnf
            raise ValueError('Unknown operation')
        raise ValueError('Unknown node')

    def simplify(self):
        if isinstance(self, BitNode) or isinstance(self, ConstantNode):
            return self
        if isinstance(self, OperationNode):
            if self.op_type == OperationType.NOT:
                child = self.children[0]
                if isinstance(child, BitNode):
                    return self
                if isinstance(child, ConstantNode):
                    return ConstantNode(not child.value)
                if isinstance(child, OperationNode):
                    if child.op_type == OperationType.NOT:
                        return child.children[0].simplify()
                    if child.op_type == OperationType.AND:
                        child1 = OperationNode(OperationType.NOT, child.children[0])
                        child2 = OperationNode(OperationType.NOT, child.children[1])
                        return OperationNode(OperationType.OR, child1, child2).simplify()
                    if child.op_type == OperationType.OR:
                        child1 = OperationNode(OperationType.NOT, child.children[0])
                        child2 = OperationNode(OperationType.NOT, child.children[1])
                        return OperationNode(OperationType.AND, child1, child2).simplify()
                    if child.op_type == OperationType.XOR:
                        return OperationNode(OperationType.EQ, *child.children).simplify()
                    if child.op_type == OperationType.EQ:
                        return OperationNode(OperationType.XOR, *child.children).simplify()
                    raise ValueError('Unknown child operation')
                raise ValueError('Unknown child node')
            if self.op_type == OperationType.AND:
                child1, child2 = self.children[0].simplify(), self.children[1].simplify()
                if isinstance(child1, ConstantNode):
                    return child2 if child1.value else ConstantNode(False)
                if isinstance(child2, ConstantNode):
                    return child1 if child2.value else ConstantNode(False)
                if isinstance(child1, BitNode) and isinstance(child2, BitNode) and child1.id == child2.id:
                    return child1
                if (isinstance(child1, BitNode) and isinstance(child2, OperationNode) and
                        child2.op_type == OperationType.NOT and isinstance(child2.children[0], BitNode) and
                        child1.id == child2.children[0].id):
                    return ConstantNode(False)
                if (isinstance(child2, BitNode) and isinstance(child1, OperationNode) and
                        child1.op_type == OperationType.NOT and isinstance(child1.children[0], BitNode) and
                        child2.id == child1.children[0].id):
                    return ConstantNode(False)
                return OperationNode(OperationType.AND, child1, child2)
            if self.op_type == OperationType.OR:
                child1, child2 = self.children[0].simplify(), self.children[1].simplify()
                if isinstance(child1, ConstantNode):
                    return child2 if not child1.value else ConstantNode(True)
                if isinstance(child2, ConstantNode):
                    return child1 if not child2.value else ConstantNode(True)
                if isinstance(child1, BitNode) and isinstance(child2, BitNode) and child1.id == child2.id:
                    return child1
                if (isinstance(child1, BitNode) and isinstance(child2, OperationNode) and
                        child2.op_type == OperationType.NOT and isinstance(child2.children[0], BitNode) and
                        child1.id == child2.children[0].id):
                    return ConstantNode(True)
                if (isinstance(child2, BitNode) and isinstance(child1, OperationNode) and
                        child1.op_type == OperationType.NOT and isinstance(child1.children[0], BitNode) and
                        child2.id == child1.children[0].id):
                    return ConstantNode(True)
                return OperationNode(OperationType.OR, child1, child2)
            if self.op_type == OperationType.XOR:
                child1, child2 = self.children[0].simplify(), self.children[1].simplify()
                if isinstance(child1, ConstantNode):
                    return child2 if not child1.value else OperationNode(OperationType.NOT, child2).simplify()
                if isinstance(child2, ConstantNode):
                    return child1 if not child2.value else OperationNode(OperationType.NOT, child1).simplify()
                if isinstance(child1, BitNode) and isinstance(child2, BitNode) and child1.id == child2.id:
                    return ConstantNode(False)
                if (isinstance(child1, BitNode) and isinstance(child2, OperationNode) and
                        child2.op_type == OperationType.NOT and isinstance(child2.children[0], BitNode) and
                        child1.id == child2.children[0].id):
                    return ConstantNode(True)
                if (isinstance(child2, BitNode) and isinstance(child1, OperationNode) and
                        child1.op_type == OperationType.NOT and isinstance(child1.children[0], BitNode) and
                        child2.id == child1.children[0].id):
                    return ConstantNode(True)
                return OperationNode(OperationType.XOR, child1, child2)
            if self.op_type == OperationType.EQ:
                child1, child2 = self.children[0].simplify(), self.children[1].simplify()
                if isinstance(child1, ConstantNode):
                    return child2 if child1.value else OperationNode(OperationType.NOT, child2).simplify()
                if isinstance(child2, ConstantNode):
                    return child1 if child2.value else OperationNode(OperationType.NOT, child1).simplify()
                if isinstance(child1, BitNode) and isinstance(child2, BitNode) and child1.id == child2.id:
                    return ConstantNode(True)
                if (isinstance(child1, BitNode) and isinstance(child2, OperationNode) and
                        child2.op_type == OperationType.NOT and isinstance(child2.children[0], BitNode) and
                        child1.id == child2.children[0].id):
                    return ConstantNode(False)
                if (isinstance(child2, BitNode) and isinstance(child1, OperationNode) and
                        child1.op_type == OperationType.NOT and isinstance(child1.children[0], BitNode) and
                        child2.id == child1.children[0].id):
                    return ConstantNode(False)
                return OperationNode(OperationType.EQ, child1, child2)
            raise ValueError('Unknown operation')
        raise ValueError('Unknown node')

    def eval(self):
        return self.pnf().pcnf().check().eval()


_VAR_CNT = 0


class BitNode(Node):
    def __init__(self):
        super().__init__()
        global _VAR_CNT
        _VAR_CNT += 1
        self.id = _VAR_CNT

    def __str__(self):
        return f'x{self.id}'

    def __hash__(self):
        return self.id


class ConstantNode(Node):
    def __init__(self, value: bool):
        super().__init__()
        self.value = value

    def __str__(self):
        return str(int(self.value))


class QuantifierNode(Node):
    def __init__(self, quantifier: QuantifierType, variables: Iterable[BitNode], child: Node):
        super().__init__()
        self.quantifier = quantifier
        self.variables = variables
        self.child = child

    def __str__(self):
        return f'{self.quantifier.value}{",".join(map(str, self.variables))} {self.child}'


class OperationNode(Node):
    def __init__(self, op_type: OperationType, *children: Node):
        super().__init__()
        assert (op_type == OperationType.NOT and len(children) == 1) or len(children) == 2
        self.op_type = op_type
        self.children = children

    def __str__(self):
        if self.op_type == OperationType.NOT:
            return f'{self.op_type.value}{self.children[0]}'
        return '(' + f' {self.op_type.value} '.join(map(str, self.children)) + ')'


class Variable:
    def __init__(self, var_nodes: Iterable[Optional[BitNode]], constraint=ConstantNode(True), aux_nodes=None):
        self.var_nodes = [BitNode() if node is None else node for node in var_nodes]
        self.constraint = constraint
        self.aux_nodes = set() if aux_nodes is None else aux_nodes

    def size(self):
        return len(self.var_nodes)

    def get(self, idx: int):
        if not 0 <= idx < self.size():
            raise ValueError(f'Index {idx} is outside [0; {self.size() - 1}]')
        return self.var_nodes[idx]

    def get_or(self, idx: int, default=ConstantNode(False)):
        return self.var_nodes[idx] if 0 <= idx < self.size() else default


def operation(func):
    def inner(*args, **kwargs):
        aux_nodes = set()
        constraint = ConstantNode(True)
        for var in args + tuple(kwargs.values()):
            if not isinstance(var, Variable):
                continue
            aux_nodes |= var.aux_nodes
            constraint &= var.constraint
            var.aux_nodes.clear()
            var.constraint = ConstantNode(True)
        result: Variable = func(*args, **kwargs)
        result.aux_nodes |= aux_nodes | set(result.var_nodes)
        result.constraint &= constraint
        return result

    return inner


class Boolean(Variable):
    def __init__(self, node=None, has_var=True):
        self.node = node or BitNode()
        self.has_var = has_var
        super().__init__([self.node] if has_var else [])

    @staticmethod
    def false():
        res = Boolean(ConstantNode(False), has_var=False)
        return res

    @staticmethod
    def true():
        res = Boolean(ConstantNode(True), has_var=False)
        return res

    @operation
    def __invert__(self):
        if not self.has_var:
            return Boolean(~self.node, has_var=False)
        res = Boolean()
        res.constraint = (res.node ^ self.node)
        return res

    @operation
    def __and__(self, other):
        if not self.has_var or not other.has_var:
            return Boolean(self.node & other.node, has_var=False)
        res = Boolean()
        res.constraint = (res.node == (self.node & other.node))
        return res

    @operation
    def __or__(self, other):
        if not self.has_var or not other.has_var:
            return Boolean(self.node | other.node, has_var=False)
        res = Boolean()
        res.constraint = (res.node == (self.node | other.node))
        return res

    @operation
    def __xor__(self, other):
        if not self.has_var or not other.has_var:
            return Boolean(self.node ^ other.node, has_var=False)
        res = Boolean()
        res.constraint = (res.node == (self.node ^ other.node))
        return res

    @operation
    def __eq__(self, other):
        if not self.has_var or not other.has_var:
            return Boolean(self.node == other.node, has_var=False)
        res = Boolean()
        res.constraint = (res.node == (self.node == other.node))
        return res

    @operation
    def __ne__(self, other):
        if not self.has_var or not other.has_var:
            return Boolean(self.node != other.node, has_var=False)
        res = Boolean()
        res.constraint = (res.node == (self.node != other.node))
        return res

    @operation
    def implies(self, other):
        return ~self | other

    @staticmethod
    @operation
    def conj(*bools):
        res = Boolean.true()
        for b in bools:
            res = res & b
        return res

    @staticmethod
    @operation
    def disj(*bools):
        res = Boolean.false()
        for b in bools:
            res = res | b
        return res

    @staticmethod
    @operation
    def xor(*bools):
        res = Boolean.false()
        for b in bools:
            res = res ^ b
        return res

    def get_node(self):
        return self.node if not self.has_var else QuantifierNode(
            QuantifierType.EXISTS, self.aux_nodes, self.constraint & self.node)

    def eval(self):
        return self.get_node().eval()


def exist(*vars_cond):
    variables = list(vars_cond[:-1])
    condition = vars_cond[-1]
    if any(variable.aux_nodes for variable in variables):
        raise ValueError('Quantifying over auxiliary variables is not allowed')

    var_nodes = sum([variable.var_nodes for variable in variables], [])
    aux_nodes = list(condition.aux_nodes)
    constraint = Node.conj(*[variable.constraint for variable in variables]) & condition.constraint
    return Boolean(QuantifierNode(QuantifierType.EXISTS, var_nodes + aux_nodes, constraint & condition.node),
                   has_var=False)


def forall(*vars_cond):
    variables = list(vars_cond[:-1])
    condition = vars_cond[-1]
    if any(variable.aux_nodes for variable in variables):
        raise ValueError('Quantifying over auxiliary variables is not allowed')

    var_nodes = sum([variable.var_nodes for variable in variables], [])
    aux_nodes = list(condition.aux_nodes)
    constraint = Node.conj(*[variable.constraint for variable in variables]) & condition.constraint
    return Boolean(QuantifierNode(QuantifierType.FORALL, var_nodes + aux_nodes, constraint.implies(condition.node)),
                   has_var=False)


def exist_unique(*vars_cond):
    variables = list(vars_cond[:-1])
    condition = vars_cond[-1]
    if any(variable.aux_nodes for variable in variables):
        raise ValueError('Quantifying over auxiliary variables is not allowed')

    var_nodes = sum([variable.var_nodes for variable in variables], [])
    new_nodes = [BitNode() for _ in range(len(var_nodes))]
    aux_nodes = list(condition.aux_nodes)
    new_constraint = Node.conj(*[variable.constraint for variable in variables]).rename(
        {var_node: new_node for var_node, new_node in zip(var_nodes, new_nodes)})
    constraint = Node.conj(*[variable.constraint for variable in variables]) & condition.constraint
    eq = Node.conj(*[var_node == new_node for var_node, new_node in zip(var_nodes, new_nodes)])
    return Boolean(QuantifierNode(QuantifierType.EXISTS, new_nodes,
                                  QuantifierNode(QuantifierType.FORALL, var_nodes + aux_nodes,
                                                 new_constraint & constraint.implies(condition.node == eq))),
                   has_var=False)


class PNF:
    def __init__(self, quantifiers, node):
        self.quantifiers = quantifiers
        self.node = node

    def __str__(self):
        return ' '.join([q.value + str(q_var) for q, q_var in self.quantifiers]) + ' ' + str(self.node)

    def __invert__(self):
        quantifiers = []
        for q_type, q_var in self.quantifiers:
            q_neg = QuantifierType.FORALL if q_type == QuantifierType.EXISTS else QuantifierType.EXISTS
            quantifiers.append((q_neg, q_var))
        return PNF(quantifiers, ~self.node)

    def __and__(self, other):
        return PNF(self.quantifiers + other.quantifiers, self.node & other.node)

    def __or__(self, other):
        return PNF(self.quantifiers + other.quantifiers, self.node | other.node)

    def __xor__(self, other):
        if not self.quantifiers and not other.quantifiers:
            return PNF([], self.node ^ other.node)
        # formula1_neg = negate_pnf(clone_pnf(formula1, {}))
        # formula2_neg = negate_pnf(clone_pnf(formula2, {}))
        # quantifiers = formula1.quantifiers + formula1_neg.quantifiers + formula2.quantifiers + formula2_neg.quantifiers
        # formula = (formula1.formula | formula2.formula) & (formula1_neg.formula | formula2_neg.formula)
        # formula = (formula1_neg.formula & formula2.formula) | (formula1.formula & formula2_neg.formula)

        pnf1, x1 = self.def_form()
        pnf2, x2 = other.def_form()
        quantifiers = [(QuantifierType.EXISTS, x1), (QuantifierType.EXISTS, x2)]
        quantifiers += pnf1.quantifiers + pnf2.quantifiers
        node = pnf1.node & pnf2.node & (x1 ^ x2)
        return PNF(quantifiers, node)

    def __eq__(self, other):
        if not self.quantifiers and not other.quantifiers:
            return PNF([], self.node == other.node)
        # formula1_neg = negate_pnf(clone_pnf(formula1, {}))
        # formula2_neg = negate_pnf(clone_pnf(formula2, {}))
        # quantifiers = formula1.quantifiers + formula1_neg.quantifiers + formula2.quantifiers + formula2_neg.quantifiers
        # formula = (formula1_neg.formula | formula2.formula) & (formula1.formula | formula2_neg.formula)
        # formula = (formula1.formula & formula2.formula) | (formula1_neg.formula & formula2_neg.formula)

        pnf1, x1 = self.def_form()
        pnf2, x2 = other.def_form()
        quantifiers = [(QuantifierType.EXISTS, x1), (QuantifierType.EXISTS, x2)]
        quantifiers += pnf1.quantifiers + pnf2.quantifiers
        node = pnf1.node & pnf2.node & (x1 == x2)
        return PNF(quantifiers, node)

    def def_form(self):
        x = BitNode()
        if not self.quantifiers:
            return PNF([], x == self.node), x
        q = self.quantifiers[0][0]
        r = 0
        while r < len(self.quantifiers) and self.quantifiers[r][0] == q:
            r += 1
        ais = [BitNode() for _ in range(r)]
        bis = [self.quantifiers[i][1] for i in range(r)]
        child_pnf, y = PNF(self.quantifiers[r:], self.node).def_form()
        child_pnf = ~child_pnf
        quantifiers = [(QuantifierType.EXISTS, a) for a in ais]
        quantifiers += [(QuantifierType.FORALL, b) for b in bis]
        quantifiers += [(QuantifierType.FORALL, y)]
        quantifiers += child_pnf.quantifiers
        neq = Node.disj(*[a != b for a, b in zip(ais, bis)])
        if q == QuantifierType.EXISTS:
            return PNF(quantifiers, child_pnf.node | ((neq | ~x | y) & (x | ~y))), x
            # return PNF(quantifiers, child_pnf.formula | ((neq | ~x | ~y) & (x | y))), x
        else:
            return PNF(quantifiers, child_pnf.node | ((neq | x | ~y) & (~x | y))), x
            # return PNF(quantifiers, child_pnf.formula | ((neq | x | y) & (~x | ~y))), x

    def simplify(self):
        return PNF(self.quantifiers, self.node.simplify())

    def pcnf(self):
        if self.quantifiers and self.quantifiers[-1][0] == QuantifierType.FORALL:
            pnf = (~self).simplify()
            negated = True
        else:
            pnf = self.simplify()
            negated = False
        quantifiers = [(q_type, q_var.id) for q_type, q_var in pnf.quantifiers]
        result = PCNF(quantifiers, [], negated)

        def compute_cnf(node) -> int:
            if isinstance(node, BitNode):
                return node.id
            if isinstance(node, OperationNode) and node.op_type == OperationType.NOT:
                assert isinstance(node.children[0], BitNode)
                return -node.children[0].id
            x = BitNode().id
            result.quantifiers.append((QuantifierType.EXISTS, x))
            if isinstance(node, ConstantNode):
                result.cnf.append([x] if node.value else [-x])
                return x
            if isinstance(node, OperationNode):
                if node.op_type == OperationType.AND:
                    y = compute_cnf(node.children[0])
                    z = compute_cnf(node.children[1])
                    result.cnf.extend([[-x, y], [-x, z]])
                    result.cnf.append([x, -y, -z])
                elif node.op_type == OperationType.OR:
                    y = compute_cnf(node.children[0])
                    z = compute_cnf(node.children[1])
                    result.cnf.extend([[x, -y], [x, -z]])
                    result.cnf.append([-x, y, z])
                elif node.op_type == OperationType.XOR:
                    y = compute_cnf(node.children[0])
                    z = compute_cnf(node.children[1])
                    result.cnf.extend([[-x, y, z], [-x, -y, -z], [x, -y, z], [x, y, -z]])
                elif node.op_type == OperationType.EQ:
                    y = compute_cnf(node.children[0])
                    z = compute_cnf(node.children[1])
                    result.cnf.extend([[x, y, z], [x, -y, -z], [-x, -y, z], [-x, y, -z]])
                else:
                    raise ValueError('Unknown operation')
                return x
            raise ValueError('Unknown node')

        value = compute_cnf(pnf.node)
        result.cnf.append([value])
        return result


# def clone_pnf(pnf_orig: PNF, replacements: Dict[BitNode, BitNode]):
#     quantifiers = []
#     for q_type, q_var in pnf_orig.quantifiers:
#         if q_var not in replacements.keys():
#             replacements[q_var] = BitNode()
#         quantifiers.append((q_type, replacements[q_var]))
#     formula = rename_formula(pnf_orig.formula, replacements)
#     return PNF(quantifiers, formula)


class PCNF:
    def __init__(self, quantifiers, cnf, negated=False):
        self.quantifiers = quantifiers
        self.cnf = cnf
        self.negated = negated

    def __str__(self):
        return (' '.join([q.value + str(q_var) for q, q_var in self.quantifiers]) + ' ' +
                ' ∧ '.join(map(lambda term: '(' + ' ∨ '.join(map(str, term)) + ')', self.cnf)))

    def check(self):
        q_var_ids = {q_var_id for _, q_var_id in self.quantifiers}
        if len(q_var_ids) < len(self.quantifiers):
            raise ValueError('Duplicated quantifiers')
        for clause in self.cnf:
            for var_id in clause:
                if var_id not in q_var_ids and -var_id not in q_var_ids:
                    raise ValueError(f'Undefined variable {var_id} in clause {clause}')
        return self

    def eval(self):
        instance_filename = 'instance.qdimacs'
        caqe_filename = 'caqe/target/release/caqe'
        with open(instance_filename, 'w') as fout:
            print(f'p cnf {len(self.quantifiers)} {len(self.cnf)}', file=fout)
            for q_type, q_var_id in self.quantifiers:
                ch = 'e' if q_type == QuantifierType.EXISTS else 'a'
                print(ch, q_var_id, 0, file=fout)
            for clause in self.cnf:
                for var_id in clause:
                    print(var_id, end=' ', file=fout)
                print(0, file=fout)
        cmd = [caqe_filename, instance_filename]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 10:
            return True ^ self.negated
        if result.returncode == 20:
            return False ^ self.negated
        raise ValueError(f'Caqe exited with code {result.returncode}')
