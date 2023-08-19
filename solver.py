from qsatlib import *
from error import *


def brute_force_solve(formula: AbstractNode, assignments=None):
    if assignments is None:
        assignments = dict()

    if isinstance(formula, BitNode):
        if formula.id not in assignments:
            raise SuckError(f'{formula} cannot be evaluated from assignments {assignments}')
        return assignments[formula.id]

    if isinstance(formula, ConstantNode):
        return formula.value

    if isinstance(formula, QuantifierNode):
        if formula.quantifier == QuantifierType.EXISTS:
            result = False
            for mask in range(2 ** len(formula.variables)):
                for i, variable in enumerate(formula.variables):
                    if variable.id in assignments:
                        raise SuckError(f'detected nested quantifiers by {variable}')
                    assignments[variable.id] = bool((mask >> i) & 1)
                cur_result = brute_force_solve(formula.child, assignments)
                for variable in formula.variables:
                    del assignments[variable.id]
                if cur_result:
                    result = True
                    break
            return result
        if formula.quantifier == QuantifierType.FORALL:
            result = True
            for mask in range(2 ** len(formula.variables)):
                for i, variable in enumerate(formula.variables):
                    if variable.id in assignments:
                        raise SuckError(f'detected nested quantifiers by {variable}')
                    assignments[variable.id] = bool((mask >> i) & 1)
                cur_result = brute_force_solve(formula.child, assignments)
                for variable in formula.variables:
                    del assignments[variable.id]
                if not cur_result:
                    result = False
                    break
            return result
        raise SuckError(f'Unknown quantifier type {formula.quantifier}')

    if isinstance(formula, UnaryOperationNode):
        if formula.op_type == UnaryOperationType.ID:
            return brute_force_solve(formula.child, assignments)
        if formula.op_type == UnaryOperationType.NOT:
            return not brute_force_solve(formula.child, assignments)
        raise SuckError(f'Unknown unary operation type {formula.op_type}')

    if isinstance(formula, BinaryOperationNode):
        value1 = brute_force_solve(formula.child1, assignments)
        value2 = brute_force_solve(formula.child2, assignments)
        if formula.op_type == BinaryOperationType.AND:
            return value1 and value2
        if formula.op_type == BinaryOperationType.OR:
            return value1 or value2
        if formula.op_type == BinaryOperationType.XOR:
            return value1 ^ value2
        if formula.op_type == BinaryOperationType.EQ:
            return value1 == value2
        raise SuckError(f'Unknown binary operation type {formula.op_type}')

    raise SuckError(f'Unknown node type {type(formula)}')


def solve(formula: AbstractNode):
    return brute_force_solve(formula)
