from wdict import Dict as dict
import numpy as np
from logging import basicConfig, DEBUG
basicConfig(level=DEBUG)


def test_int_int():
    a = dict({"a": 1})
    b = dict({"a": 2, "b": 2})
    c = a + b
    assert c["a"] == [1, 2]
    assert c["b"] == 2
    assert c.a == [1, 2]
    assert c.b == 2


def test_float_float():
    a = dict({"a": 1.0})
    b = dict({"a": 2.0, "b": 2.0})
    c = a + b
    assert c["a"] == [1.0, 2.0]
    assert c["b"] == 2.0
    assert c.a == [1.0, 2.0]
    assert c.b == 2.0



def test_float_int():
    a = dict({"a": 1.0})
    b = dict({"a": 2, "b": 2})
    c = a + b
    assert c["a"] == [1.0, 2]
    assert c["b"] == 2
    assert c.a == [1.0, 2]
    assert c.b == 2


def test_str_str():
    a = dict({"a": "str_a"})
    b = dict({"a": "str_b", "b": "str_b2"})
    c = a + b
    assert c["a"] == ["str_a", "str_b"]
    assert c["b"] == "str_b2"
    assert c.a == ["str_a", "str_b"]
    assert c.b == "str_b2"


def test_dict_dict():
    a = dict({"a": {"k": "1a"}})
    b = dict({"a": {"k": "1b"}, "b": {"c": {"d": 1}}})
    c = a + b
    assert c["a"]["k"] == ["1a", "1b"]
    assert c["b"]["c"]["d"] == 1
    assert c.a.k == ["1a", "1b"]
    assert c.b.c.d == 1


def test_dict_int():
    a = dict({"a": {"k": "1a"}})
    b = dict({"a": 1, "b": {"c": {"d": 1}}})
    c = a + b
    assert c["a"][0]["k"] == "1a"
    assert c["a"][1] == 1
    assert c["b"]["c"]["d"] == 1
    assert c.a[0].k == "1a"
    assert c.a[1] == 1
    assert c.b.c.d == 1


def test_npy_npy():
    a = dict({"a": np.zeros(3, dtype=int)})
    b = dict({"a": np.ones(3, dtype=float), "b": {"c": {"d": 1}}})
    c = a + b
    assert c["a"] == [0, 0, 0, 1.0, 1.0, 1.0]
    assert c["b"]["c"]["d"] == 1
    assert c.a == [0, 0, 0, 1.0, 1.0, 1.0]
    assert c.b.c.d == 1


def test_npy_list():
    a = dict({"a": np.zeros(3, dtype=int)})
    b = dict({"a": [2.0, 2.0, 2.0], "b": {"c": {"d": 1}}})
    c = a + b
    assert c["a"] == [0, 0, 0, 2.0, 2.0, 2.0]
    assert c["b"]["c"]["d"] == 1
    assert c.a == [0, 0, 0, 2.0, 2.0, 2.0]
    assert c.b.c.d == 1


def test_list_list():
    a = dict({"a": [1, 1, 1]})
    b = dict({"a": [3.0, 3.0, 3.0], "b": {"c": {"d": 1}}})
    c = a + b
    assert c["a"] == [1, 1, 1, 3.0, 3.0, 3.0]
    assert c["b"]["c"]["d"] == 1
    assert c.a == [1, 1, 1, 3.0, 3.0, 3.0]
    assert c.b.c.d == 1


def test_list_str():
    a = dict({"a": [1, 1, 1]})
    b = dict({"a": "str b", "b": {"c": {"d": 1}}})
    c = a + b
    assert c["a"] == [1, 1, 1, "str b"]
    assert c["b"]["c"]["d"] == 1
    assert c.a == [1, 1, 1, "str b"]
    assert c.b.c.d == 1


def test_list_int():
    a = dict({"a": [1, 1, 1]})
    b = dict({"a": 7, "b": {"c": {"d": 1}}})
    c = a + b
    assert c["a"] == [1, 1, 1, 7]
    assert c["b"]["c"]["d"] == 1
    assert c.a == [1, 1, 1, 7]
    assert c.b.c.d == 1


def test_str_int_list():
    a = dict({"a": "str 0"})
    b = dict({"a": 8, "b": {"c": {"d": 1}}})
    c = dict({"a": [9, 0]})
    d = a + b + c
    assert d["a"] == ["str 0", 8, 9, 0]
    assert d["b"]["c"]["d"] == 1
    assert d.a == ["str 0", 8, 9, 0]
    assert d.b.c.d == 1


def test_str_int_list_del():
    a = dict({"a": "str 0"})
    b = dict({"a": 8, "b": {"c": {"d": 1}}})
    c = dict({"a": [9, 0]})
    d = a + b + c
    del a
    del b
    del c
    assert d["a"] == ["str 0", 8, 9, 0]
    assert d["b"]["c"]["d"] == 1
    assert d.a == ["str 0", 8, 9, 0]
    assert d.b.c.d == 1


def test_str_int_list_update():
    a = dict({"a": "str 0"})
    b = dict({"a": 8, "b": {"c": {"d": 1}}})
    c = dict({"a": [9, 0]})
    d = a + b + c
    b["b"] = None
    a["a"] = None
    c["a"] = "None"
    assert d["a"] == ["str 0", 8, 9, 0]
    assert d["b"]["c"]["d"] == 1
    assert d.a == ["str 0", 8, 9, 0]
    assert d.b.c.d == 1

