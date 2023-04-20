from qsatlib import Forall, Exists, And, Or, Not, Exist
from qsatlib import UndirectedGraph, DirectedGraph
from qsatlib import Bitstring, DeterministicBooleanCircuit, NondeterministicBooleanCircuit
from qsatlib import STConnAlgorithm
from qsatlib import RubiksCube2x2x2, RubiksCube2x2x2Move

# 1. by elexunix
g = UndirectedGraph(2)
h = UndirectedGraph(2)
Forall(g, Exists(h, g != h))  # True

# 2. by elexunix
nbc = NondeterministicBooleanCircuit(e_vars=3, i_vars=5, o_vars=1, complexity=10)
dbc = DeterministicBooleanCircuit(i_vars=5, o_vars=1, complexity=20)
x = Bitstring(5)
Forall(nbc, Exists(dbc, Forall(x, nbc(x) == dbc(x))))  # Interesting

# 3. by elexunix & cookiedoth
g = DirectedGraph(5)
s, t = g.Vertex(0), g.Vertex(4)
algos = STConnAlgorithm(states=20, graph=g)
Exists(algos, Forall(g, algos(g) == g.reachable(s, t)))

# 4. by elexunix
c = RubiksCube2x2x2()
solution = [RubiksCube2x2x2Move() for i in range(11)]
Forall(c, Exists(solution, c(solution).solved()))

# 5. by fedroidus
g = UndirectedGraph(6)
v1, v2, v3 = g.Vertex(), g.Vertex(), g.Vertex()
Forall(g, Exist(v1, v2, v3, g.HasEdge(v1, v2) and g.HasEdge(v2, v3) and g.HasEdge(v3, v1) or not g.HasEdge(v1, v2) and not g.HasEdge(v2, v3) and not g.HasEdge(v3, v1)))

# 6. by cookiedoth
dbc1 = DeterministicBooleanCircuit(i_vars=2, o_vars=1, complexity=5)
dbc2 = DeterministicBooleanCircuit(i_vars=2, o_vars=1, complexity=5)
x = Bitstring(2)
Forall(dbc1, Exists(dbc2, Forall(x, dbc1(x) != dbc2(x))))

# 7. by cookiedoth
dbc = DeterministicBooleanCircuit(i_vars=2, o_vars=1)
x = Bitstring(2)
Forall(dbc, Forall(x, dbc(x)) or Exists(x, not dbc(x)))
