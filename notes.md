You got it! Here's the **entire thing in pure Markdown format**, ready to copy and paste:

---

## 🐍 Python Notes Summary

### 🧩 `defaultdict` from `collections`

- **Syntax:** `defaultdict(list)`
- Automatically initializes missing keys with an empty list
- Useful for grouping or counting without needing `if key not in dict`
- Other common initializers:
  - `defaultdict(int)` → default is `0`
  - `defaultdict(set)` → default is an empty set

---

### 🔡 Sorting Strings in Python

```python
sorted_string = ''.join(sorted(s))
```

- `sorted(s)` returns a list of characters in sorted order
- `''.join(...)` combines the sorted characters back into a string
- Used to create a consistent key for grouping anagrams

---

### 🔣 `ord()` Function

```python
ord('a')        # returns 97
ord('c') - ord('a')  # returns 2 (useful for index mapping)
```

- Converts a character to its ASCII integer value
- Common in problems involving frequency arrays

---

### 📦 Tuples in Python

- **Syntax:** `(1, 2, 3)`
- Immutable and ordered
- Can be used as **dictionary keys** (unlike lists)
- Convert from list: `tuple(my_list)`
- **Single-element tuple:** `(1,)` → the comma is necessary

---

### 📚 `dict.values()` vs `dict.values`

```python
list(my_dict.values())  # ✅ correct
my_dict.values          # ⚠️ just a method reference, not the result
```

- `.values()` must be called to get the actual data
- Use `list()` to convert it to a list of values

---

### 🔁 Tuple Unpacking

```python
a, b = (1, 2)
# a = 1, b = 2
```

- Splits a tuple into individual variables


```markdown
# 🐍 Python Strings: Cheatsheet for Coding & Interviews

---

## 🔤 1. String Basics

```python
s = "hello"
s2 = 'world'
s3 = "hello 'again'"  # mixed quotes allowed
```

- Strings are immutable
- Indexable: `s[0] == 'h'`
- Slicing: `s[1:4] == 'ell'`
- Reverse: `s[::-1]`

---

## 🧰 2. Common String Methods

| Method               | Use                                      |
|----------------------|------------------------------------------|
| `s.upper()`          | `'hi'.upper() → 'HI'`                    |
| `s.lower()`          | `'HI'.lower() → 'hi'`                    |
| `s.capitalize()`     | `'hello'.capitalize() → 'Hello'`         |
| `s.strip()`          | `'  hi  '.strip() → 'hi'`                |
| `s.lstrip()`         | `'  hi'.lstrip() → 'hi'`                 |
| `s.rstrip()`         | `'hi  '.rstrip() → 'hi'`                 |
| `s.replace(a, b)`    | `'hi hi'.replace('hi','ho') → 'ho ho'`   |
| `s.split()`          | `'a b c'.split() → ['a','b','c']`        |
| `'sep'.join(list)`   | `' '.join(['a','b']) → 'a b'`            |
| `s.find(x)`          | `'abcde'.find('c') → 2`                  |
| `s.index(x)`         | `'abcde'.index('c') → 2`                 |
| `s.count(x)`         | `'aaa'.count('a') → 3`                   |
| `s.startswith(x)`    | `'hello'.startswith('he') → True`        |
| `s.endswith(x)`      | `'hello'.endswith('lo') → True`          |

---

## 🪄 3. String Formatting

```python
name = "Sam"
age = 25

f"Hello {name}, you are {age}"     # ✅ Preferred
"Hello {}, you are {}".format(name, age)
"Hello %s, you are %d" % (name, age)
```

---

## 🔢 4. Character <-> ASCII

```python
ord('a')   # → 97
chr(97)    # → 'a'
```

Use `ord()` when mapping characters to indexes (like in anagrams).

---

## 🔁 5. Loops and Checks

```python
for ch in s:
    print(ch)

if 'h' in s:
    print("yes")

s.isdigit()     # '123' → True
s.isalpha()     # 'abc' → True
s.isalnum()     # 'abc123' → True
s.islower(), s.isupper()
```

---

## 🧠 6. Tips & Tricks

- Strings are **immutable**. To change them, make a new string.
- `''.join()` is faster than repeated `+` for concatenation in loops.
- Always prefer `in` over `.find()` for presence checks:
  ```python
  if 'a' in s:
      ...
  ```

---

## 🧪 Practice

Try understanding outputs:
```python
s = "hello world"
print(s[::2])       # 'hlowrd'
print(s[-1])        # 'd'
print(s.split())    # ['hello', 'world']
print("-".join(s))  # h-e-l-l-o- -w-o-r-l-d
```
```

---

Let me know when you're ready and I can do the same for **lists**, **dicts**, or **loops/conditionals** too!