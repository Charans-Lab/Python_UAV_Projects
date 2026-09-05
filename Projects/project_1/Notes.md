# Notes — Project 1

## 1. `input()`

- `input()` is a built-in Python function used to take input from the user.
- It pauses the program and waits until the user types something and presses Enter.
- It **always returns a string**, even when the user types a number.
- To use the value as a number, convert it explicitly with `int()` or `float()`.

```python
name = input("Enter your name: ")        # returns a string
age = int(input("Enter your age: "))     # converted to an integer
```

---

## 2. Lists

- A list stores **heterogeneous data** — integers, strings, floats can all sit in the same list.
- A list is written inside square brackets `[ ]`, with items separated by commas.

```python
ex_list = [1, "sai", 96.020]
```

- `ex_list` is the name of the list; `1`, `"sai"` and `96.020` are the **items** (or elements) of the list.
- Quotes are required only for **strings**. Numbers are written without quotes.
- Lists are ordered and indexed from `0`:

```python
ex_list[0]    # 1
ex_list[1]    # 'sai'
```

---

## 3. `.split()`

- `.split()` is a **string method**.
- It splits one string into a **list of substrings**, using whitespace as the separator by default.
- A different separator can be passed as an argument, e.g. `.split(",")`.

```python
"1 47.398 8.546 9".split()
# → ['1', '47.398', '8.546', '9']
```

- Note that every item in the result is still a **string**, not a number.

---

## 4. `.append()`

- `.append()` is a **list method**. It adds **one item** to the end of a list.
- It modifies the list in place and returns `None`.
- If the item being appended is itself a list, it is added as a **single nested item** — not merged.

```python
a = ['sai', 'charan', 'drone']
b = ['raju']

b.append(a)
print(b)
# → ['raju', ['sai', 'charan', 'drone']]
```

- To merge the contents of one list into another instead of nesting, use `.extend()`:

```python
b = ['raju']
b.extend(a)
print(b)
# → ['raju', 'sai', 'charan', 'drone']
```

---

## 5. Functions

Syntax:

```python
def function_name():
    # body
    return value
```

Example:

```python
def function_name():
    m = 1
    c = 5
    y = m + c * c
    return y
```

- The `return` statement must be **inside** the function body — i.e. indented to the same level as the rest of the body.
- Defining a function does **not** run it. The body executes only when the function is **called**.
- The simplest way to call it:

```python
result = function_name()
print(result)    # → 26
```

---

## 6. Global variables

- **Reading** a global variable inside a function needs no declaration.
- The `global` keyword is needed only when **reassigning** the global variable from inside a function.

```python
count = 0

def read_it():
    print(count)        # works fine, no `global` needed

def change_it():
    global count        # needed, because we are reassigning
    count = count + 8
```

- Without the `global` line, `count = count + 8` would create a **new local variable** inside the function, and Python would raise an `UnboundLocalError`.

---

## 7. Where a function should be defined

- In the first version of this project I defined `haversine()` **inside a `for` loop**, and later **inside `Missionplan_summary()`**.
- Both versions run, but both are wrong. A function belongs at **module level** — defined once, at the top of the file, outside every loop and every other function.

Why nesting is worse as a program grows:

- **Not reusable** — a nested function is invisible outside its parent, so nothing else in the file can call it. `haversine()` is generally useful, so burying it means copy-pasting it later.
- **Re-created on every call** — the function object is rebuilt each time the parent runs. Pointless work.
- **Not self-contained** — it can silently capture variables from the enclosing scope, so its behaviour starts depending on invisible state.
- **Not testable** — it can't be imported or called in isolation.

```python
# wrong — redefined on every iteration
for wp in waypoints:
    def haversine(lat1, lon1, lat2, lon2):
        ...
    d = haversine(...)

# correct — defined once, at module level
def haversine(lat1, lon1, lat2, lon2):
    ...

for wp in waypoints:
    d = haversine(...)
```

- Modularity comes from **flat, independent, reusable units**, not from physical nesting. A flat structure makes the flow of a large program visible; nesting hides it.