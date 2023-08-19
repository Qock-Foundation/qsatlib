#from qsatlib import implies, conj, disj, eq, exists, forall
#from qsatlib import AbstractNode, BitNode, ConstantNode, QuantifierNode
from qsatlib import *

def brute_force_solve(formula: AbstractNode, assignments = {}):
  if isinstance(formula, BitNode):
    assert formula.id in assignments, f'{formula} cannot be evaluated from assignments {assignments}, and you suck'
    return assignments[formula.id]
  if isinstance(formula, ConstantNode):
    return formula.value
  if isinstance(formula, QuantifierNode):
    assert formula.variable not in assignments, f'detected nested quantifiers by {formula.variable}, and you suck'
    assignments[formula.variable] = False
    value_if_false = brute_force_solve(formula, assignments)
    assignments[formula.variable] = True
    value_if_true = brute_force_solve(formula, assignments)
    del assignments[formula.variable]
    if formula.quantifier == QuantifierType.EXISTS:
      return value_if_false or value_if_true
    if formula.quantifier == QuantifierType.FORALL:
      return value_if_false and value_if_true
    raise SuckError(f'Unknown quantifier type {formula.quantifier}, and you suck')
  if isinstance(formula, UnaryOperationNode):
    if formula.op_type == UnaryOperationType.ID:
      return brute_force_solve(formula.child, assignments)
    if formula.op_type == UnaryOperationType.NOT:
      return not brute_force_solve(formula.child, assignments)
    raise SuckError(f'Unknown unary operation type {formula.op_type}, and you suck')
  if isinstance(formula, BinaryOperationNode):
    value1 = brute_force_solve(formula.child1)
    value2 = brute_force_solve(formula.child2)
    if formula.op_type == BinaryOperationType.AND:
      return value1 and value2
    if formula.op_type == BinaryOperationType.OR:
      return value1 or value2
    if formula.op_type == BinaryOperationType.XOR:
      return value1 xor value2
    if formula.op_type == BinaryOperationType.EQ:
      return value1 == value2
    raise SuckError(f'Unknown binary operation type {formula.op_type}, and you suck')
  raise SuckError(f'Unknown node type {type(formula)}, and you suck')

def solve(formula: AbstractNode):
  return brute_force_solve(formula)
