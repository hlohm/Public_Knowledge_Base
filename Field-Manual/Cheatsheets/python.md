---
type: cheatsheet
area: "Programming Languages"
aliases: [python3, py]
tags: [python, programming, scripting, data]
status: working
---

# Python

> **Area:** [[Programming Languages]]

The 80% you reach for daily. Python 3.10+. See the stdlib at `python3 -m pydoc <module>` or `help(<obj>)` at the REPL.

---

## 1. Built-in types

```python
# Strings — immutable, iterable
s = "hello"
s.upper(), s.lower(), s.strip(), s.lstrip(" "), s.rstrip()
s.split(",")                    # list of parts
",".join(["a", "b", "c"])       # "a,b,c"
s.startswith("he"), s.endswith("lo")
s.replace("l", "r")
s.find("ell")                   # index or -1
f"Value is {x:.2f}"            # f-string (preferred over .format())
f"{value!r}"                    # repr() in f-string
f"{n:04d}"                      # zero-padded integer

# Lists — mutable, ordered
lst = [1, 2, 3]
lst.append(4)           # [1, 2, 3, 4]
lst.extend([5, 6])      # [1, 2, 3, 4, 5, 6]
lst.insert(0, 0)        # insert at index
lst.remove(3)           # remove first occurrence
lst.pop()               # remove and return last
lst.pop(0)              # remove and return index 0
lst.sort(key=str.lower, reverse=True)
sorted(lst)             # returns new list
lst.index(2)            # index of value
3 in lst                # membership test

# Slicing (works on strings, lists, tuples)
lst[1:4]                # elements 1, 2, 3
lst[::2]                # every other element
lst[::-1]               # reversed

# Dicts — insertion-ordered (3.7+)
d = {"a": 1, "b": 2}
d["a"]                  # 1  (KeyError if missing)
d.get("c", 0)           # 0  (default if missing)
d.setdefault("c", []).append(1)   # insert if missing, then use
d.items()               # view of (key, value) pairs
d.keys(), d.values()
d.pop("a")              # remove and return
d.update({"c": 3})      # merge in
{**d, "extra": 4}       # merge with spread (3.9+: d | {"extra": 4})
"a" in d                # key membership

# Sets
s = {1, 2, 3}
s.add(4); s.discard(4)  # add; discard (no error if missing)
s & {2, 3, 4}           # intersection
s | {4, 5}              # union
s - {2}                 # difference
s ^ {3, 4}              # symmetric difference

# Tuples — immutable
t = (1, 2, 3)
a, b, c = t             # unpack
a, *rest = t            # rest = [2, 3]
```

## 2. Comprehensions

```python
# List comprehension
squares = [x**2 for x in range(10)]
evens   = [x for x in range(20) if x % 2 == 0]

# Dict comprehension
inv = {v: k for k, v in d.items()}

# Set comprehension
unique_lengths = {len(word) for word in words}

# Generator expression (lazy — does not build a list)
total = sum(x**2 for x in range(1000))
first = next(x for x in items if x > 10)
```

## 3. Control flow

```python
# Ternary
result = "yes" if condition else "no"

# match (3.10+) — structural pattern matching
match command:
    case "quit":
        exit()
    case "go" | "move":
        move()
    case {"action": action, "target": target}:
        do(action, target)
    case _:
        print("unknown")

# for / else (else runs when loop completes without break)
for item in items:
    if found(item):
        break
else:
    print("not found")

# walrus operator (3.8+)
while chunk := f.read(4096):
    process(chunk)
```

## 4. Functions

```python
def process(data, *, output=None, verbose=False):
    """Docstring."""
    ...

# * forces keyword-only args after it
# / forces positional-only args before it

# *args and **kwargs
def log(*args, **kwargs):
    print(args, kwargs)

# Type hints (optional but useful for linting/documentation)
def greet(name: str, count: int = 1) -> str:
    return (name + " ") * count

# Lambda (for short callbacks only)
sorted(items, key=lambda x: x.age)
```

## 5. Classes

```python
class Animal:
    species = "Unknown"              # class variable

    def __init__(self, name: str):
        self.name = name             # instance variable

    def speak(self) -> str:
        return f"{self.name} says something"

    @classmethod
    def create(cls, name: str) -> "Animal":
        return cls(name)

    @staticmethod
    def is_animal(obj) -> bool:
        return isinstance(obj, Animal)

    def __repr__(self) -> str:
        return f"Animal(name={self.name!r})"

    def __str__(self) -> str:
        return self.name


class Dog(Animal):
    def speak(self) -> str:
        return f"{self.name} barks"

    def __init__(self, name: str, breed: str):
        super().__init__(name)
        self.breed = breed

# Dataclasses (3.7+) — auto-generate __init__, __repr__, __eq__
from dataclasses import dataclass, field

@dataclass
class Point:
    x: float
    y: float
    tags: list = field(default_factory=list)  # mutable default
```

## 6. Exceptions

```python
try:
    result = risky_call()
except ValueError as e:
    print(f"bad value: {e}")
except (TypeError, KeyError):
    raise
except Exception as e:
    print(f"unexpected: {e}")
    raise                          # re-raise with original traceback
else:
    use(result)                    # runs only if no exception
finally:
    cleanup()                      # always runs

# Raise
raise ValueError("must be positive")
raise RuntimeError("failed") from original_exc   # chained exception

# Custom exception
class AppError(Exception):
    def __init__(self, msg: str, code: int = 0):
        super().__init__(msg)
        self.code = code
```

## 7. Context managers

```python
# Files
with open("file.txt") as f:
    data = f.read()

with open("out.txt", "w") as f:
    f.write("hello\n")

# Multiple resources
with open("in.txt") as src, open("out.txt", "w") as dst:
    dst.write(src.read())

# Custom context manager
from contextlib import contextmanager

@contextmanager
def managed_resource():
    resource = acquire()
    try:
        yield resource
    finally:
        resource.close()
```

## 8. stdlib highlights

```python
import os
os.path.join("a", "b")         # path join
os.path.exists("/etc/passwd")
os.path.basename("/a/b/c.txt") # "c.txt"
os.makedirs("/a/b", exist_ok=True)
os.getenv("HOME", "/tmp")
os.environ["KEY"]

from pathlib import Path        # modern alternative (3.4+)
p = Path("/etc/passwd")
p.exists(), p.is_file(), p.is_dir()
p.read_text(), p.write_text("data")
p.parent, p.name, p.stem, p.suffix
list(p.glob("*.conf"))         # matches files
list(p.rglob("*.py"))          # recursive

import json
data = json.loads('{"key": 1}')
json.dumps(data, indent=2)
with open("f.json") as f: data = json.load(f)

import subprocess
result = subprocess.run(["ls", "-la"], capture_output=True, text=True, check=True)
result.stdout, result.returncode

import sys
sys.argv[0]                     # script name
sys.exit(1)
print("error", file=sys.stderr)

import re
m = re.search(r"(\d+)", "abc123")
m.group(1)                      # "123"
re.findall(r"\d+", "1 and 2")  # ["1", "2"]
re.sub(r"\s+", " ", text)

from collections import defaultdict, Counter, deque
d = defaultdict(list)
d["key"].append(1)
c = Counter("aabbc")
c.most_common(3)                # [("a", 2), ("b", 2), ("c", 1)]

import itertools
itertools.chain([1, 2], [3, 4])
itertools.product("AB", repeat=2)
itertools.groupby(sorted_items, key=lambda x: x.group)

from functools import lru_cache, partial
@lru_cache(maxsize=128)
def fib(n): return n if n < 2 else fib(n-1) + fib(n-2)
double = partial(operator.mul, 2)
```

## 9. File I/O patterns

```python
# Read all lines
with open("f.txt") as f:
    lines = f.readlines()          # list of strings (with \n)
    # or: lines = f.read().splitlines()  # strips \n

# Stream large files
with open("big.txt") as f:
    for line in f:                  # line-by-line, no full load
        process(line.rstrip("\n"))

# Binary mode
with open("file.bin", "rb") as f:
    data = f.read()

# CSV
import csv
with open("data.csv") as f:
    for row in csv.DictReader(f):
        print(row["column"])

# Write CSV
with open("out.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["a", "b"])
    w.writeheader()
    w.writerow({"a": 1, "b": 2})
```

---

## Daily workflows

### "Sort a dict by value"
```python
sorted_items = sorted(d.items(), key=lambda kv: kv[1], reverse=True)
# Or as dict:
sorted_d = dict(sorted(d.items(), key=lambda kv: kv[1]))
```

### "Flatten a list of lists"
```python
flat = [x for sub in nested for x in sub]
# Or: list(itertools.chain.from_iterable(nested))
```

### "Group items by a property"
```python
from itertools import groupby
from collections import defaultdict

# defaultdict approach (no pre-sort needed)
groups = defaultdict(list)
for item in items:
    groups[item.category].append(item)
```

## Gotchas / Golden rules

1. **Mutable default arguments are shared across calls** — `def f(lst=[])` reuses the same list; use `def f(lst=None): lst = lst or []` instead.
2. **`is` checks identity, `==` checks equality** — `x is None` (correct); `x == None` (works but poor style); never use `is` to compare strings or integers beyond small ranges.
3. **`for x in dict` iterates over keys** — use `.items()` for key-value pairs.
4. **`+=` on a string inside a loop is O(n²)** — collect into a list and `"".join()` at the end.
5. **Implicit truthiness**: empty `""`, `[]`, `{}`, `0`, `None` are falsy — `if lst:` is cleaner than `if len(lst) > 0:`, but be explicit when `0` is a valid meaningful value.
