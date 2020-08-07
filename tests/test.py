import sys
sys.path.append("../")
from wdict import Dict as dict
import numpy as np
from logging import basicConfig, DEBUG
basicConfig(level=DEBUG)


def test_extract_child():
    a = dict({
        "a": {
            "1": {
                "2": {
                    "3": "A",
                    "33": "A"
                }
            }
        },
        "b": {
            "1": {
                "2": {
                    "3": "A",
                    "33": "A"
                }
            }
        },
        "c": {
            "1": {
                "2c": {
                    "3": "C",
                    "33": "A"
                }
            }
        },
        "d": {
            "1": {
                "2d": {
                    "3": "D",
                    "33": "A"
                }
            }
        }
    })
    # print(a.extract_child("1/2/3"))
    assert len([key for key in a.extract_child("1/2/3").keys()
                if key in ["a", "b"]]) == 2
    assert len([key for key in a.extract_child("1/*/3").keys()
                if key in ["a", "b", "c", "d"]]) == 4


def test_get_keys():
    a = dict({
        "a": {
            "1": {
                "2": {
                    "3": "A"
                }
            }
        },
        "b": {
            "1": {
                "2": {
                    "3": "A"
                }
            }
        },
        "c": {
            "1": {
                "2": {
                    "3": "C"
                }
            }
        },
        "d": {
            "1": {
                "22": {
                    "33": "D"
                }
            }
        }
    })
    assert len(list(a.get_child_keys("1/2/3"))) == 0
    assert list(a.get_child_keys("1/2")) == ["3"]
    assert list(a.get_child_keys("1")) == ["2", "22"] or \
           list(a.get_child_keys("1")) == ["2", "22"][::-1]
    assert list(a.get_child_keys()) == ["1"]


def test_drop():
    a = dict({
        "a": {
            "1": {
                "2": {
                    "3": "A"
                }
            }
        },
        "b": {
            "1": {
                "2": {
                    "3": "A"
                }
            }
        },
        "c": {
            "1": {
                "2": {
                    "3": "C"
                }
            }
        }
    })
    b = a.drop(0)
    assert b["1"]["2"]["3"] == ["A", "A", "C"]
    b = a.drop(1)
    b = b.where("2/3", "in", ["A"])
    assert len([key for key in b.keys() if key in ["a", "b"]]) == 2
    b = a.drop(2)
    b = b.where("1/3", "in", ["C"])
    assert len(b.keys()) == 1
    assert list(b.keys())[0] == "c"
    a = dict({
        "a": {
            "1": {
                "2": {
                    "3": "A"
                }
            }
        },
        "b": {
            "1": {
                "2": {
                    "3": "A"
                }
            },
            "11": {
                "2": {
                    "3": "A"
                }
            }
        },
        "c": {
            "1": {
                "2": {
                    "3": "C"
                }
            }
        }
    })
    b = a.drop(1)
    b = b.where("2/3", "has", "A")
    assert len([key for key in b.keys() if key in ["a", "b"]]) == 2


def test_has_child():
    a = dict({"a": {"child": 1}, "b": {"son": 1},
              "c": {
                  "daughter": {
                      "g_daughter": {
                            "gg_daughter": 1
                        }}}})
    b = a.has_child("son")
    assert len(b.keys()) == 1
    assert list(b.keys())[0] == "b"

    b = a.has_child("*/g_daughter/gg_daughter")
    assert len(b.keys()) == 1
    assert list(b.keys())[0] == "c"

    b = a.has_child("*/*/*")
    assert len(b.keys()) == 1
    assert list(b.keys())[0] == "c"

    b = a.has_child("daughter/g_daughter/gg_daughter")
    assert len(b.keys()) == 1
    assert list(b.keys())[0] == "c"

    a = dict({"a": {"child": 1}, "b": {"son": 1}})
    b = a.has_child("*")
    assert len(b.keys()) == 2
    assert len([key for key in b.keys() if key in ["a", "b"]]) == 2

    a = dict({
        "a": {"child": {"g_child": 1}},
        "b": {"son": {"g_daughter": {"gg_son": 1}}},
        "c": {"daughter": {"g_daughter": {"gg_daughter": 1}}}
    })

    b = a.has_child("*")
    assert len(b.keys()) == 3

    b = a.has_child("*/g_daughter")
    assert len(b.keys()) == 2
    assert len([key for key in b.keys() if key in ["b", "c"]]) == 2

    b = a.has_child("*/*/gg_son")
    assert len(b.keys()) == 1
    assert list(b.keys())[0] == "b"




def test_exclude():
    a = dict({"a": 2, "b": 2, "c": 2})
    a = a.exclude(["b"])
    assert len(a.keys()) == 2
    assert len([key for key in a.keys() if key in ["a", "c"]]) == 2

    a = a.exclude(["F"])
    assert len(a.keys()) == 2
    assert len([key for key in a.keys() if key in ["a", "c"]]) == 2

    a = dict({"a": 2, "b": 2, "c": 2})
    a = a.exclude(["b", "c"])
    assert len(a.keys()) == 1
    assert list(a.keys())[0] == "a"


def test_extract():
    a = dict({"a": 2, "b": 2, "c": 2})
    a = a.extract(["a", "c"])
    assert len(a.keys()) == 2
    assert len([key for key in a.keys() if key in ["a", "c"]]) == 2

    a = dict({"a": 2, "b": 2, "c": 2})
    a = a.extract(["a"])
    assert len(a.keys()) == 1
    assert list(a.keys())[0] == "a"


def test_where_in():
    a = dict({"a": {"child": 1},
              "b": {"child": [0, 1, 2]},
              "c": {"child": "A"}
              })
    b = a.where("child", "in", ["A", 1])
    assert len(b.keys()) == 2
    assert len([key for key in b.keys() if key in ["a", "c"]]) == 2

    a = dict({"a": {"child": 1},
              "b": {"child": [0, 1, 2]},
              "c": {"child": "A"}
              })
    b = a.where("child", "in", "A")
    assert len(b.keys()) == 1
    assert len([key for key in b.keys() if key in ["c"]]) == 1


def test_where_not_in():
    a = dict({"a": {"child": 1},
              "b": {"child": [0, 1, 2]},
              "c": {"child": "A"}
              })
    b = a.where("child", "not in", ["A", 1])
    assert len(b.keys()) == 1
    assert len([key for key in b.keys() if key in ["b"]]) == 1

    a = dict({"a": {"child": 1},
              "b": {"child": [0, 1, 2]},
              "c": {"child": "A"}
              })
    b = a.where("child", "not in", "A")
    assert len(b.keys()) == 2
    assert len([key for key in b.keys() if key in ["a", "b"]]) == 2

    a = dict({"a": {"child": 1},
              "b": {"child": [0, 1, 2]},
              "c": {"child": "A"}
              })
    b = a.where("child", "not in", [1])
    assert len(b.keys()) == 2
    assert len([key for key in b.keys() if key in ["b", "c"]]) == 2


def test_where_does_not_have():
    a = dict({"a": {"child": 1},
              "b": {"child": [0, 1, 2]},
              "c": {"child": "1"}
              })
    b = a.where("child", "does not have", 1)
    assert len(b.keys()) == 2
    assert len([key for key in b.keys() if key in ["a", "c"]]) == 2

    a = dict({"a": {"child1": "1"},
              "b": {"child2": {"g_child": [0]}},
              "bb": {"child2": {"g_child": [5]}},
              "c": {"child3": [5]},
              })
    b = a.where("*/g_child", "does not have", 5)
    assert len(b.keys()) == 1
    assert len([key for key in b.keys() if key in ["b"]]) == 1


def test_where_has():
    a = dict({"a": 1, "b": {"child": [0, 1, 2]}})
    b = a.where("child", "has", 1)
    assert len(b.keys()) == 1
    assert list(b.keys())[0] == "b"

    a = dict({"a": 1,
              "b": {"child": [0, 1, 2, 5]},
              "bb": {"child": [0, 1, 2]}
              })
    b = a.where("child", "has", 5)
    assert len(b.keys()) == 1
    assert list(b.keys())[0] == "b"


def test_where_has_any():
    a = dict({"a": 1, "b": {"child": {"a": 1, "b": 2, "c": 3}}})
    b = a.where("child", "has any", ["a", "d"])
    assert len(b.keys()) == 1
    assert list(b.keys())[0] == "b"

    a = dict({"a": 1,
              "b": {"child": {"a": 1, "b": 2, "c": 3}},
              "bb": {"child": {"e": 1, "f": 2, "g": 3}}
              })
    b = a.where("child", "has any", ["a", "d"])
    assert len(b.keys()) == 1
    assert list(b.keys())[0] == "b"


def test_where_does_not_have_any():
    a = dict({"a": 1, "b": {"child": {"a": 1, "b": 2, "c": 3}}})
    b = a.where("child", "does not have any", ["a", "d"])
    assert len(b.keys()) == 0

    a = dict({"a": 1,
              "b": {"child": {"a": 1, "b": 2, "c": 3}},
              "c": {"child": {"e": 1, "f": 2, "g": 3}}
              })
    b = a.where("child", "does not have any", ["a", "d"])
    assert len(b.keys()) == 1
    assert list(b.keys())[0] == "c"

    a = dict({"a": 1,
              "b": {"child": {"a": 1, "b": 2, "c": 3}},
              "bb": {"child": {"a": 1, "b": 2, "d": 3}}
              })
    b = a.where("child", "does not have any", ["a", "d"])
    assert len(b.keys()) == 0


def test_where_has_all():
    a = dict({"a": 1, "b": {"child": {"a": 1, "b": 2, "c": 3}}})
    b = a.where("child", "has all", ["a", "d"])
    assert len(b.keys()) == 0

    a = dict({"a": 1,
              "b": {"child": {"a": 1, "b": 2, "c": 3}},
              "bb": {"child": {"e": 1, "f": 2, "g": 3}}
              })
    b = a.where("child", "has all", ["a", "c"])
    assert len(b.keys()) == 1
    assert list(b.keys())[0] == "b"


def test_where_does_not_have_all():
    a = dict({"a": 1, "b": {"child": {"a": 1, "b": 2, "c": 3}}})
    b = a.where("child", "does not have all", ["a", "d"])
    assert len(b.keys()) == 1
    assert list(b.keys())[0] == "b"

    a = dict({"a": 1, "b": {"child": {"a": 1, "b": 2, "c": 3, "d": 4}}})
    b = a.where("child", "does not have all", ["a", "d"])
    assert len(b.keys()) == 0

    a = dict({"a": 1,
              "b": {"child": {"a": 1, "b": 2, "c": 3}},
              "bb": {"child": {"e": 1, "f": 2, "g": 3}}
              })
    b = a.where("child", "does not have all", ["a", "c"])
    assert len(b.keys()) == 1
    assert list(b.keys())[0] == "bb"


def test_where_eq():
    a = dict({
        "a": 1,
        "b": {"child": {"gchild": 1, "a": 1}, "son": {"gchild": 0}},
        "c": {"child": 1}})
    b = a.where("*/gchild", "==", 1)
    print(b)
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
    a = dict({"a": 1, "b": {"child": 1, "son": 1}})
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
