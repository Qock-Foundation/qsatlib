from qsatlib.qsatlib import *
from qsatlib.error import *


class BruteForceSolver:
    def solve(self, formula: Formula, assignments=None):
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
                    result |= self.solve(formula.child, assignments)
                    for variable in formula.variables:
                        del assignments[variable.id]
                    if result:
                        break
                return result
            if formula.quantifier == QuantifierType.FORALL:
                result = True
                for mask in range(2 ** len(formula.variables)):
                    for i, variable in enumerate(formula.variables):
                        if variable.id in assignments:
                            raise SuckError(f'detected nested quantifiers by {variable}')
                        assignments[variable.id] = bool((mask >> i) & 1)
                    result &= self.solve(formula.child, assignments)
                    for variable in formula.variables:
                        del assignments[variable.id]
                    if not result:
                        break
                return result
            raise SuckError(f'Unknown quantifier type {formula.quantifier}')

        if isinstance(formula, OperationNode):
            if formula.op_type == OperationType.NOT:
                return not self.solve(formula.children[0], assignments)
            if formula.op_type == OperationType.AND:
                result = True
                for child in formula.children:
                    result &= self.solve(child, assignments)
                    if not result:
                        break
                return result
            if formula.op_type == OperationType.OR:
                result = False
                for child in formula.children:
                    result |= self.solve(child, assignments)
                    if result:
                        break
                return result
            if formula.op_type == OperationType.XOR:
                result = False
                for child in formula.children:
                    result ^= self.solve(child, assignments)
                return result
            if formula.op_type == OperationType.EQ:
                return self.solve(formula.children[0], assignments) == \
                    self.solve(formula.children[1], assignments)
            raise SuckError(f'Unknown operation type {formula.op_type}')

        raise SuckError(f'Unknown node type {type(formula)}')
