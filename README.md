# wdict
The Dictionary class contains filtering methods.

# Install

```sh
pip install --upgrade wdict
```

# Features
* Filter dicts based on its child value by "where" method 
* Filter dicts based on its keys by "has_child"", "exclude" and "extract" method
* Support specific depth key dropping 
* Concatenate dicts with "+" operator
* Attribute-style access

## Operators for the "where" method
* "==", ">=", "<=", "!=", "<", ">"
* "in", "not in"
* "has", "does not have"
* "has any", "does not have any"
* "has all", "does not have all"
* "subset of"

# Usage
```
>>> from wdict import Dict as WD
```

# Examples
See the [test code](https://github.com/shinaji/wdict/blob/master/tests/test.py)

```
>>> a = WD({"a": 1}) 
>>> b = WD({"a": 2, "b": 2})
>>> a + b
Dict([('a', [1, 2]), ('b', 2)])
>>> (a + b).a
[1, 2]
>>> (a + b)["a"]
[1, 2]

>>> a = WD({"a": 1, "b": {"child": 1}}) 
>>> a.where("child", "==", 1)
Dict([('b', Dict([('child', 1)]))])

>>> a = WD({"a": 1, "b": {"child": 1}}) 
>>> a.exclude(["b"])
Dict([('a', 1)])

>>> a = WD({"a": {"c": 1}}) 
>>> b = WD({"a": {"d": 2}})
>>> print(a + b)
{"a": {"c": 1, "d": 2}}
>>> print(sum([a, b]))
{"a": {"c": 1, "d": 2}}

>>> a = WD({"a": 1}) 
>>> b = WD({"b": 2})
>>> a += b
>>>print(a)
{"a": 1, "b": 2}

>>> a = WD({"a": 1, "b": "str a"}) 
>>> b = WD({"a": [2, 3], "b": "str b"})
>>> (a + b).a
[1, [2, 3]]
>>> (a + b).b
['str a', 'str b']

>>> a = WD({"a": 1}) 
>>> b = WD({"a": {"b": 1}})
>>> (a + b).a
[1, Dict([('b', 1)])]
```
