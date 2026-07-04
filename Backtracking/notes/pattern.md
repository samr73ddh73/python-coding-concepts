# Backtracking Patterns

## Mutable vs Immutable

In recursion, you must understand whether your data structure is mutable or immutable to know if you need to backtrack.

### Immutable (string, tuple, number)
- No undo needed
- Just pass a new value to recursion
- String concatenation creates new string

### Mutable (list, dict, set)
- Must undo changes after recursion
- Use pop(), del, or reassignment
- Pattern: Add → Explore → Remove (A-E-R)

See the Python documentation for specific examples.
