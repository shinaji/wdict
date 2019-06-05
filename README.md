# wdict
Python dictionary class with add method.

# Install

```sh
pip install --upgrade wdict
```

# Features
* Concatenate dicts with "+" operator
* Filter dicts based on its child value by "where" method 
* Filter dicts based on its keys by "has_child"", "exclude" and "extract" method
* Drop 
* Attribute-style access

# Usage
```
>>> from wdict import Dict as dict
```

# Example
```
>>> a = dict({"a": 1}) 
>>> b = dict({"a": 2, "b": 2})
>>> a + b
Dict([('a', [1, 2]), ('b', 2)])
>>> (a + b).a
[1, 2]
>>> (a + b)["a"]
[1, 2]

>>> a = dict({"a": 1, "b": {"child": 1}}) 
>>> a.where("child", "==", 1)
Dict([('b', Dict([('child', 1)]))])

>>> a = dict({"a": 1, "b": {"child": 1}}) 
>>> a.want(["a"])
Dict([('a', 1)])

>>> a = dict({"a": 1, "b": {"child": 1}}) 
>>> a.exclude(["b"])
Dict([('a', 1)])

>>> a = dict({"a": {"c": 1}}) 
>>> b = dict({"a": {"d": 2}})
>>> print(a + b)
{"a": {"c": 1, "d": 2}}
>>> print(sum([a, b]))
{"a": {"c": 1, "d": 2}}

>>> a = dict({"a": 1}) 
>>> b = dict({"b": 2})
>>> a += b
>>>print(a)
{"a": 1, "b": 2}

>>> a = dict({"a": 1, "b": "str a"}) 
>>> b = dict({"a": [2, 3], "b": "str b"})
>>> (a + b).a
[1, [2, 3]]
>>> (a + b).b
['str a', 'str b']

>>> a = dict({"a": 1}) 
>>> b = dict({"a": {"b": 1}})
>>> (a + b).a
[1, Dict([('b', 1)])]
```
