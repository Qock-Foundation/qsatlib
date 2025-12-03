from qsatlib.qsatlib import *


def test_bool_and_unique():
    a, b, c = Boolean(), Boolean(), Boolean()
    assert forall(a, b, exist_unique(c, c == a & b)).eval()


def test_bool_and_false():
    a = Boolean()
    assert forall(a, ~(a & Boolean.false())).eval()


def test_bool_and_true():
    a = Boolean()
    assert forall(a, a & Boolean.true() == a).eval()


def test_bool_and_commutativity():
    a, b = Boolean(), Boolean()
    assert forall(a, b, a & b == b & a).eval()


def test_bool_and_associativity():
    a, b, c = Boolean(), Boolean(), Boolean()
    assert forall(a, b, c, (a & b) & c == a & (b & c)).eval()


def test_bool_or_unique():
    a, b, c = Boolean(), Boolean(), Boolean()
    assert forall(a, b, exist_unique(c, c == a | b)).eval()


def test_bool_or_false():
    a = Boolean()
    assert forall(a, a | Boolean.false() == a).eval()


def test_bool_or_true():
    a = Boolean()
    assert forall(a, a | Boolean.true()).eval()


def test_bool_or_commutativity():
    a, b = Boolean(), Boolean()
    assert forall(a, b, a | b == b | a).eval()


def test_bool_or_associativity():
    a, b, c = Boolean(), Boolean(), Boolean()
    assert forall(a, b, c, (a | b) | c == a | (b | c)).eval()


def test_bool_xor_unique():
    a, b, c = Boolean(), Boolean(), Boolean()
    assert forall(a, b, exist_unique(c, c == a ^ b)).eval()


def test_bool_xor_false():
    a = Boolean()
    assert forall(a, a ^ Boolean.false() == a).eval()


def test_bool_xor_true():
    a = Boolean()
    assert forall(a, a ^ Boolean.true() != a).eval()


def test_bool_xor_commutativity():
    a, b = Boolean(), Boolean()
    assert forall(a, b, a ^ b == b ^ a).eval()


def test_bool_xor_associativity():
    a, b, c = Boolean(), Boolean(), Boolean()
    assert forall(a, b, c, (a ^ b) ^ c == a ^ (b ^ c)).eval()


def test_bool_not_and():
    a, b = Boolean(), Boolean()
    assert forall(a, b, ~(a & b) == ~a | ~b).eval()


def test_bool_not_or():
    a, b = Boolean(), Boolean()
    assert forall(a, b, ~(a | b) == ~a & ~b).eval()


def test_bool_not_xor():
    a, b = Boolean(), Boolean()
    assert forall(a, b, ~(a ^ b) == (a == b)).eval()


def test_bool_and_or_dist():
    a, b, c = Boolean(), Boolean(), Boolean()
    assert forall(a, b, c, (a & b) | c == (a | c) & (b | c)).eval()


def test_bool_or_and_dist():
    a, b, c = Boolean(), Boolean(), Boolean()
    assert forall(a, b, c, (a | b) & c == (a & c) | (b & c)).eval()


def test_bool_xor_and_dist():
    a, b, c = Boolean(), Boolean(), Boolean()
    assert forall(a, b, c, (a ^ b) & c == (a & c) ^ (b & c)).eval()


def test_not_quantifiers():
    a, b = Boolean(), Boolean()
    assert (~forall(a, b, a | b)).eval()


def test_and_quantifiers():
    a, b = Boolean(), Boolean()
    assert not (forall(a, a) & exist(b, b)).eval()


def test_or_quantifiers():
    a, b = Boolean(), Boolean()
    assert (forall(a, a) | exist(b, b)).eval()


def test_xor_quantifiers():
    a, b = Boolean(), Boolean()
    assert (forall(a, a) ^ exist(b, b)).eval()


def test_eq_quantifiers():
    a, b = Boolean(), Boolean()
    assert not (forall(a, a) == exist(b, b)).eval()


def test_forall_exist():
    a, b = Boolean(), Boolean()
    assert forall(a, exist(b, (a | b).implies(a & b))).eval()


def test_exist_unique():
    a, b, c = Boolean(), Boolean(), Boolean()
    assert exist_unique(a, exist_unique(b, (a & ~b) | exist(c, c != c))).eval()


def test_variable_reuse():
    a, b = Boolean(), Boolean()
    c = a | b
    assert exist_unique(a, b, ~c).eval()
    c = c & a & b
    assert exist_unique(a, b, c).eval()
    c = a ^ b
    assert not exist_unique(a, b, c).eval()
