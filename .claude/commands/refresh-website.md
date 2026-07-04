Refresh the DSA Practice Hub website to pick up any new notes, markdown files, and problems added to the repo since the last update.

## Steps to follow

### 1. Regenerate notes-data.js

Run the build script to pull in all markdown files:

```bash
node website/build-notes.js
```

Check the output. If any files were skipped (shown with ⚠), investigate why — the file may have been renamed or moved. Update `NOTE_SOURCES` in `website/build-notes.js` if needed.

### 2. Scan for new problem files

Check each topic directory for Python files that do NOT yet have a corresponding entry in `website/data.js`.

Directories to scan (map to topic IDs in data.js):
- `Array/` → topic id `array`
- `BinarySearch/` → topic id `binary-search`
- `LinkedList/` → topic id `linked-list`
- `Trees/` → topic id `trees`
- `Graph/` → topic id `graph`
- `DP/` (all subdirs) → topic id `dp`
- `Backtracking/` → topic id `backtracking`
- `Sliding window/` → topic id `sliding-window`
- `Strings/` → topic id `strings`
- `MergeIntervals/` → topic id `merge-intervals`
- `Range-Query/` → topic id `range-query`
- `Recursion/` → topic id `recursion`
- `Maths/` → topic id `maths`
- `BitManipulation/` → topic id `bit-manipulation`
- `Cyclic Sort/` → topic id `cyclic-sort`
- `prefixSum/` → topic id `prefix-sum`
- `sorting/` and `groupAnagram/` → topic id `sorting`
- `google/` → topic id `google`

For each `.py` file found, check if a problem with a matching `file` field already exists in the relevant topic's `problems` array in `website/data.js`. If not, it is a **new problem**.

### 3. Add new problems to data.js

For each new Python file found:

1. **Read the file** to understand what problem it solves (look at comments, function names, problem description at the top).
2. **Determine**: problem name, difficulty (Easy/Medium/Hard), LeetCode number and URL if applicable.
3. **Write algorithm notes** — a concise explanation of the approach: key insight, step-by-step algorithm, time/space complexity. Use the same format as existing problems in data.js (see the `notes` field — plain text with `\n` newlines, bullet points with `•`).
4. **Add the problem** to the correct topic's `problems` array in `website/data.js`, following the exact same object structure:

```js
{
  name: 'Problem Name',
  difficulty: 'Easy' | 'Medium' | 'Hard',
  leetcode: 'https://leetcode.com/problems/slug/',
  leetcodeNum: 123,          // null if no direct LC problem
  file: 'TopicDir/filename.py',
  notes: 'Key insight: ...\n\nAlgorithm:\n• Step 1\n• Step 2\n\nTime: O(...) | Space: O(...)',
},
```

### 4. Check for new markdown notes

List all `.md` files in the repo:

```bash
find . -name "*.md" -not -path "./website/*" -not -path "./.git/*"
```

Compare against the `NOTE_SOURCES` array in `website/build-notes.js`. For any `.md` file not already listed, decide whether it is worth adding (skip very small or auto-generated files). If yes, add an appropriate entry to `NOTE_SOURCES` and re-run `node website/build-notes.js`.

### 5. Validate

Run a quick sanity check:

```bash
node -e "
const fs = require('fs');
const fn = new Function(fs.readFileSync('website/data.js','utf8') + '; return TOPICS;');
const T = fn();
const fn2 = new Function(fs.readFileSync('website/notes-data.js','utf8') + '; return NOTES;');
const N = fn2();
console.log('Topics:', T.length, '| Problems:', T.reduce((s,t)=>s+t.problems.length,0));
console.log('Notes:', N.length);
"
```

### 6. Report what changed

Print a summary:
- How many new problems were added (and to which topics)
- How many notes were refreshed / any new notes added
- Any files that were skipped or need attention
