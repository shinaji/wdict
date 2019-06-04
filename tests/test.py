import sys
sys.path.append("../")
from wdict import Dict as dict
import numpy as np
from logging import basicConfig, DEBUG
basicConfig(level=DEBUG)


def test_where_in():
    a = dict({"a": 1, "b": {"child": [0, 1, 2]}})
    b = a.where("child", "in", 1)
    assert len(b.keys()) == 1
    assert list(b.keys())[0] == "b"


def test_where_in():
    a = dict({"a": 1, "b": {"child": [0, 1, 2]}})
    b = a.where("child", "not in", 5)
    assert len(b.keys()) == 1
    assert list(b.keys())[0] == "b"


def test_where_eq():
    a = dict({"a": 1, "b": {"child": 1}})
    b = a.where("child", "==", 1)
    assert len(b.keys()) == 1
    assert list(b.keys())[0] == "b"


def test_where_neq():
    a = dict({"a": 1, "b": {"child": 1}})
    b = a.where("child", "!=", 1)
    assert len(b.keys()) == 0

    a = dict({"a": 1, "b": {"child": 1}})
    b = a.where("child", "!=", 0)
    assert len(b.keys()) == 1
    assert list(b.keys())[0] == "b"


def test_where_gt():
    a = dict({"a": 1, "b": {"child": 1}})
    b = a.where("child", ">", 0)
    assert len(b.keys()) == 1
    assert list(b.keys())[0] == "b"

    a = dict({"a": 1, "b": {"child": 1}})
    b = a.where("child", ">", 1)
    assert len(b.keys()) == 0


def test_where_lt():
    a = dict({"a": 1, "b": {"child": 1}})
    b = a.where("child", "<", 2)
    assert len(b.keys()) == 1
    assert list(b.keys())[0] == "b"

    a = dict({"a": 1, "b": {"child": 1}})
    b = a.where("child", "<", 1)
    assert len(b.keys()) == 0


def test_where_gteq():
    a = dict({"a": 1, "b": {"child": 1}})
    b = a.where("child", ">=", 1)
    b = b.where("child", ">=", 0)
    assert len(b.keys()) == 1
    assert list(b.keys())[0] == "b"


def test_where_lteq():
    a = dict({"a": 1, "b": {"child": 1}})
    b = a.where("child", "<=", 1)
    b = b.where("child", "<=", 2)
    assert len(b.keys()) == 1
    assert list(b.keys())[0] == "b"


def test_mul():
    a = dict({"a": 1})
    b = list(a * 2)
    assert b[0]["a"] == 1
    assert b[0].a == 1
    assert b[1]["a"] == 1
    assert b[1].a == 1


def test_sum():
    a = dict({"a": 1})
    b = dict({"a": 2, "b": 2})
    c = sum([a, b])
    assert c["a"] == [1, 2]
    assert c["b"] == 2
    assert c.a == [1, 2]
    assert c.b == 2


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


def test_list_to_ndarray():
    a = dict(a=[0, 1])
    a.list_to_ndarray()
    b = dict(a=[0, 1], force_ndarray=True)
    assert a.a.tolist() == [0, 1]
    assert a["a"].tolist() == [0, 1]
    assert b.a.tolist() == [0, 1]
    assert b["a"].tolist() == [0, 1]


def test_ndarray_to_list():
    a = dict(a=np.array([0, 1]))
    a.ndarray_to_list()
    b = dict(a=[0, 1], force_ndarray=True)
    b.ndarray_to_list()
    assert isinstance(a.a, list)
    assert isinstance(a["a"], list)
    assert isinstance(b.a, list)
    assert isinstance(b["a"], list)
    assert a.a == [0, 1]
    assert a["a"] == [0, 1]
    assert b.a == [0, 1]
    assert b["a"] == [0, 1]
