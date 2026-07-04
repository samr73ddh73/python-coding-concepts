/**
 * build-notes.js — Auto-generates notes-data.js from all .md files in the repo
 *
 * Usage:
 *   node website/build-notes.js
 *
 * Run this whenever you add or edit a .md file.
 * It scans the repo, reads every .md file, and writes notes-data.js.
 */

'use strict';

const fs   = require('fs');
const path = require('path');

// ── Config: which files to include and how to label them ─────────
// Files are relative to the REPO ROOT (one level up from website/).
// Edit this list to add/remove notes. Order = sidebar order.

const NOTE_SOURCES = [
  // ── Python ──────────────────────────────────────────────────────
  {
    id:       'python-notes',
    title:    'Python Quick Reference',
    emoji:    '🐍',
    category: 'Python',
    file:     'notes.md',
  },
  {
    id:       'python-imports',
    title:    'Common Imports',
    emoji:    '📦',
    category: 'Python',
    file:     'imports.md',
  },
  {
    id:       'python-strings',
    title:    'String Operations',
    emoji:    '📝',
    category: 'Python',
    file:     'Strings/notes.md',
  },
  {
    id:       'python-maps',
    title:    'Maps / Dictionaries',
    emoji:    '🗂️',
    category: 'Python',
    file:     'Maps/notes.md',
  },

  // ── Concepts ─────────────────────────────────────────────────────
  {
    id:       'time-complexity',
    title:    'Time Complexity Guide',
    emoji:    '⏱️',
    category: 'Concepts',
    file:     'timecomplexity.md',
  },
  {
    id:       'dp-complexity',
    title:    'DP Complexity Guide',
    emoji:    '🧮',
    category: 'Concepts',
    file:     'DP/TIME_COMPLEXITY_GUIDE.md',
  },
  {
    id:       'recursion-theory',
    title:    'Recursion Theory',
    emoji:    '🔄',
    category: 'Concepts',
    file:     'Recursion/01-theory.md',
  },

  // ── Data Structures ───────────────────────────────────────────────
  {
    id:       'trees-theory',
    title:    'Trees Theory',
    emoji:    '🌳',
    category: 'Data Structures',
    file:     'Trees/0-1.Theory.md',
  },
  {
    id:       'bit-manipulation',
    title:    'Bit Manipulation',
    emoji:    '⚙️',
    category: 'Data Structures',
    file:     'BitManipulation/resources.md',
  },

  // ── Patterns ──────────────────────────────────────────────────────
  {
    id:       'two-pointer-code',
    title:    'Two-Pointer Code Patterns',
    emoji:    '👈👉',
    category: 'Code Patterns',
    file:     'Array/two-pointer-pattern.md',
  },
  {
    id:       'binary-search-code',
    title:    'Binary Search Code Patterns',
    emoji:    '🔍',
    category: 'Code Patterns',
    file:     'BinarySearch/binary-search-code-pattern.md',
  },
  {
    id:       'bfs-code',
    title:    'BFS Code Patterns',
    emoji:    '🌊',
    category: 'Code Patterns',
    file:     'Graph/BFS-pattern.md',
  },
  {
    id:       'dfs-code',
    title:    'DFS Code Patterns',
    emoji:    '⬇️',
    category: 'Code Patterns',
    file:     'Graph/DFS-pattern.md',
  },
  {
    id:       'binary-search-patterns',
    title:    'Binary Search Patterns',
    emoji:    '🔍',
    category: 'Patterns',
    file:     'BinarySearch/0-patterns.md',
  },
  {
    id:       'general-patterns',
    title:    'General Patterns',
    emoji:    '🗺️',
    category: 'Patterns',
    file:     'patterns.md',
  },
  {
    id:       'backtracking-pattern',
    title:    'Backtracking Pattern',
    emoji:    '🔙',
    category: 'Patterns',
    file:     'Backtracking/pattern.md',
  },
  {
    id:       'sliding-window-pattern',
    title:    'Sliding Window Pattern',
    emoji:    '🪟',
    category: 'Patterns',
    file:     'Sliding window/pattern.md',
  },
  {
    id:       'tree-patterns',
    title:    'Tree Patterns',
    emoji:    '🌳',
    category: 'Patterns',
    file:     'Trees/0-patterns-cheatsheet.md',
  },
  {
    id:       'tree-pattern-old',
    title:    'Tree Pattern Reference',
    emoji:    '🎯',
    category: 'Patterns',
    file:     'Trees/pattern.md',
  },
  {
    id:       'graph-patterns',
    title:    'Graph Patterns',
    emoji:    '🕸️',
    category: 'Patterns',
    file:     'Graph/patterns.md',
  },
  {
    id:       'graph-dsu',
    title:    'Disjoint Set Union (DSU)',
    emoji:    '🔗',
    category: 'Patterns',
    file:     'Graph/0-DSU-notes.md',
  },
  {
    id:       'graph-bfs-dfs',
    title:    'When BFS vs DFS',
    emoji:    '↔️',
    category: 'Patterns',
    file:     'Graph/20-when-to-use-bfs-dfs.md',
  },
  {
    id:       'merge-intervals',
    title:    'Merge Intervals Patterns',
    emoji:    '📏',
    category: 'Patterns',
    file:     'MergeIntervals/concept.md',
  },
  {
    id:       'cyclic-sort',
    title:    'Cyclic Sort Pattern',
    emoji:    '🔃',
    category: 'Patterns',
    file:     'Cyclic Sort/when-to-use.md',
  },
  {
    id:       'lcs-guide',
    title:    'LCS Variations',
    emoji:    '🧵',
    category: 'Patterns',
    file:     'DP/3-LCS/README.md',
  },
  {
    id:       'lcs-concept',
    title:    'LCS vs Substring',
    emoji:    '🔀',
    category: 'Patterns',
    file:     'DP/3-LCS/2-lcs-concept.md',
  },
  {
    id:       'scs-guide',
    title:    'Shortest Common Supersequence',
    emoji:    '📐',
    category: 'Patterns',
    file:     'DP/3-LCS/SHORTEST_COMMON_SUPERSEQUENCE.md',
  },
  {
    id:       'unbounded-knapsack',
    title:    'Unbounded Knapsack',
    emoji:    '♾️',
    category: 'Patterns',
    file:     'DP/2-Unbounded-Knapsack/theory.md',
  },
  {
    id:       'mcm-concept',
    title:    'Matrix Chain Mult. (Interval DP)',
    emoji:    '🔢',
    category: 'Patterns',
    file:     'DP/4-MCM/concept.md',
  },
  {
    id:       'binary-search-bounds',
    title:    'Binary Search Bounds',
    emoji:    '🔍',
    category: 'Patterns',
    file:     'binary-search-bounds.py',   // this one is a Python file with a guide
  },
  {
    id:       'range-query-bit',
    title:    'Binary Indexed Tree',
    emoji:    '🌲',
    category: 'Patterns',
    file:     'Range-Query/02-binary-index-tree.md',
  },
  {
    id:       'insert-delete-getrandom',
    title:    'Insert Delete GetRandom O(1)',
    emoji:    '🎲',
    category: 'Patterns',
    file:     'google/insert-delete-o(1).md',
  },
];

// ── Helpers ──────────────────────────────────────────────────────
const REPO_ROOT   = path.resolve(__dirname, '..');
const OUTPUT_FILE = path.join(__dirname, 'notes-data.js');

function readFile(relPath) {
  const abs = path.join(REPO_ROOT, relPath);
  if (!fs.existsSync(abs)) {
    console.warn(`  ⚠  File not found, skipping: ${relPath}`);
    return null;
  }
  return fs.readFileSync(abs, 'utf8');
}

// Escape backticks and template-literal placeholders so content can
// be safely embedded in a JS template literal string.
function escapeForTemplateLiteral(str) {
  return str
    .replace(/\\/g, '\\\\')       // backslashes first
    .replace(/`/g, '\\`')         // backticks
    .replace(/\$\{/g, '\\${');    // ${...} interpolations
}

// ── Build ─────────────────────────────────────────────────────────
console.log('Building notes-data.js from markdown files...\n');

const entries = [];
let skipped = 0;

for (const source of NOTE_SOURCES) {
  const raw = readFile(source.file);
  if (raw === null) { skipped++; continue; }

  const escaped = escapeForTemplateLiteral(raw.trim());
  entries.push({ ...source, content: escaped });
  console.log(`  ✓  ${source.file.padEnd(50)} → "${source.title}"`);
}

// ── Write output ──────────────────────────────────────────────────
const lines = [
  '/* AUTO-GENERATED by build-notes.js — do not edit manually.',
  ' * Run:  node website/build-notes.js',
  ` * Generated: ${new Date().toISOString()}`,
  ' */',
  '',
  'const NOTES = [',
];

for (const e of entries) {
  lines.push('  {');
  lines.push(`    id:       ${JSON.stringify(e.id)},`);
  lines.push(`    title:    ${JSON.stringify(e.title)},`);
  lines.push(`    emoji:    ${JSON.stringify(e.emoji)},`);
  lines.push(`    category: ${JSON.stringify(e.category)},`);
  lines.push(`    file:     ${JSON.stringify(e.file)},`);
  lines.push(`    content: \`${e.content}\`,`);
  lines.push('  },');
  lines.push('');
}

lines.push('];');
lines.push('');

fs.writeFileSync(OUTPUT_FILE, lines.join('\n'), 'utf8');

console.log(`\n✅  Done — ${entries.length} notes written, ${skipped} skipped.`);
console.log(`   Output: ${OUTPUT_FILE}`);
