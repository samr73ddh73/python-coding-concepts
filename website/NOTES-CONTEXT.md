# DSA Hub - Notes Organization Context

This file explains how to structure and add notes to the DSA Hub website.

## Directory Structure for Notes

```
Topics/
├── fundamentals/
│   ├── time-complexity.md
│   ├── data-structures.md
│   ├── python-basics.md
│   └── imports.md
│
├── array/
│   ├── theory.md
│   ├── patterns.md
│   ├── questions.md
│   └── tricks.md
│
├── graphs/
│   ├── theory.md
│   ├── patterns.md
│   ├── bfs-pattern.md
│   ├── dfs-pattern.md
│   ├── questions.md
│   └── tricks.md
│
├── trees/
│   ├── theory.md
│   ├── patterns.md
│   ├── questions.md
│   └── tricks.md
│
├── dp/
│   ├── theory.md
│   ├── patterns.md
│   ├── questions.md
│   └── tricks.md
│
├── binary-search/
│   ├── theory.md
│   ├── patterns.md
│   ├── questions.md
│   └── tricks.md
│
├── linked-lists/
│   ├── theory.md
│   ├── patterns.md
│   ├── questions.md
│   └── tricks.md
│
├── strings/
│   ├── theory.md
│   ├── patterns.md
│   ├── questions.md
│   └── tricks.md
│
├── backtracking/
│   ├── theory.md
│   ├── patterns.md
│   ├── questions.md
│   └── tricks.md
│
├── heap/
│   ├── theory.md
│   ├── patterns.md
│   ├── questions.md
│   └── tricks.md
│
└── [other-topics]/
    └── Same pattern...
```

## File Format

### theory.md
```markdown
# [Topic] Theory

## Core Concepts
- Explain concepts in your own words
- Include diagrams/descriptions
- Use Hindi if helpful

## Time Complexity
| Operation | Complexity | Notes |
| --- | --- | --- |
| ... | O(...) | ... |

## Key Points
- Point 1
- Point 2

## When to Use
- Condition 1
- Condition 2
```

### patterns.md
```markdown
# [Topic] Patterns

## Pattern 1: [Name]

**When to use:** Brief description

**Code:**
```python
# Your code here
```

**Complexity:** O(...) time, O(...) space

**Tips:**
- Tip 1
- Tip 2

---

## Pattern 2: [Name]
...
```

### questions.md
```markdown
# [Topic] Practice Questions

## Easy
- LC 1: [Problem Name] - `pattern/approach`
- LC 2: [Problem Name] - `pattern/approach`

## Medium
- LC 3: [Problem Name] - `pattern/approach`

## Hard
- LC 4: [Problem Name] - `pattern/approach`
```

### tricks.md
```markdown
# [Topic] Tricks & Gotchas

## Trick 1: [Name]
**Trap:** What goes wrong
**Solution:** How to fix it
**Example:** Code example

---

## Trick 2: [Name]
...
```

## How Website Loads Notes

The website will:
1. Read all .md files from `topics/` directory
2. Parse markdown into structured data
3. Display with proper formatting
4. Support code blocks, tables, lists

## To Add a New Note

1. Create file: `topics/[topic-name]/[file-type].md`
2. Follow format above
3. Website auto-loads on refresh
4. No code changes needed!

## Current Mapping of Your Notes

### ✅ Already Have
- Trees: `Trees/0-1.Theory.md`, `Trees/pattern.md`, `Trees/0-patterns-cheatsheet.md`
- Graphs: `Graph/00-MASTER-PATTERNS.md`, `Graph/BFS-pattern.md`, `Graph/DFS-pattern.md`, `Graph/0-DSU-notes.md`
- DP: `DP/TIME_COMPLEXITY_GUIDE.md`, `DP/**/theory.md`
- Binary Search: `BinarySearch/0-patterns.md`, `BinarySearch/binary-search-code-pattern.md`
- Arrays: `Array/two-pointer-pattern.md`
- Backtracking: `Backtracking/pattern.md`
- Others: Strings, Maps, Recursion, etc.

### ❌ Need Organization
1. Move all theory files to `topics/[topic]/theory.md`
2. Move all pattern files to `topics/[topic]/patterns.md`
3. Create questions.md with LeetCode problem lists
4. Create tricks.md with gotchas for each topic
5. Clean up unnecessary files

## Files to Delete (Bloat)

- `website/revision-app.html` - old version
- `website/revision-hub.html` - old version
- `REVISION-APP-GUIDE.md` - old guide
- `REVISION-HUB-COMPLETE.md` - old guide
- `PROJECT-SUMMARY.md` - old summary
- Old guides and redundant files

## Process to Implement

1. **Phase 1:** Create `topics/` directory structure
2. **Phase 2:** Migrate your .md files to new structure
3. **Phase 3:** Update website to load from `topics/`
4. **Phase 4:** Display with proper formatting (markdown parser)
5. **Phase 5:** Add flashcard generation from notes
6. **Phase 6:** Clean up old files
