/**
 * Script to add 40 new problems to website/data.js
 * Organizes by topic and inserts into the problems array
 */

const fs = require('fs');
const path = require('path');

// New problems data extracted from files
const NEW_PROBLEMS = {
  'backtracking': [
    {
      name: 'Maximum Number with K Swaps',
      difficulty: 'Medium',
      leetcode: null,
      leetcodeNum: null,
      file: 'Backtracking/3-k-swaps.py',
      notes: 'Key insight: Greedily swap largest elements forward using backtracking. Algorithm: At each position, find max element from current to end, swap if greater, recurse with k-1 swaps. Time: O(n²·k) | Space: O(n)'
    },
    {
      name: 'Increasing Order Numbers',
      difficulty: 'Easy',
      leetcode: null,
      leetcodeNum: null,
      file: 'Backtracking/4-increasing-order-num.py',
      notes: 'Key insight: Generate all n-digit numbers with strictly increasing digits. Algorithm: Backtracking with start index constraint—each digit must be greater than previous. Time: O(2^n) | Space: O(n)'
    }
  ],
  'binary-search': [
    {
      name: 'Find Peak Element',
      difficulty: 'Medium',
      leetcode: 'https://leetcode.com/problems/find-peak-element/description/',
      leetcodeNum: 162,
      file: 'BinarySearch/8-peak-element.py',
      notes: 'Key insight: Follow ascending slope—go right if mid < mid+1 (slope up), go left if mid > mid+1 (slope down). Algorithm: Binary search always moves toward peak, guaranteed to find one. Time: O(log n) | Space: O(1)'
    },
    {
      name: 'Minimum Speed to Arrive On Time (Unbounded)',
      difficulty: 'Medium',
      leetcode: 'https://leetcode.com/problems/minimum-speed-to-arrive-on-time/description/',
      leetcodeNum: 1870,
      file: 'BinarySearch/9-unbounded-case.py',
      notes: 'Key insight: Right bound set to 10^7 (unbounded)—binary search on answer. Algorithm: Calculate time with candidate speed (using ceil for all but last segment), move boundary if feasible. Time: O(n log(max_speed)) | Space: O(1)'
    },
    {
      name: 'Binary Search on Answer: Eating Bananas',
      difficulty: 'Medium',
      leetcode: 'https://leetcode.com/problems/minimum-eating-speed/',
      leetcodeNum: 875,
      file: 'BinarySearch/10-bs-on-answers.py',
      notes: 'Key insight: Problem asks for minimum speed—binary search on answer space instead of array. Algorithm: Find minimum k where we can eat all piles in h hours by checking feasibility with math.ceil. Time: O(n log(max_pile)) | Space: O(1)'
    }
  ],
  'dp': [
    {
      name: '0/1 Knapsack (Top-Down Memoization)',
      difficulty: 'Medium',
      leetcode: null,
      leetcodeNum: null,
      file: 'DP/1-Knapsack/0-1-knapsack/top-down.py',
      notes: 'Key insight: For each item, choose to include (take profit, reduce capacity) or skip. Algorithm: Recursive with memoization on (capacity, item_index). Time: O(n·capacity) | Space: O(n·capacity) + call stack'
    },
    {
      name: 'Subset Sum (Recursion)',
      difficulty: 'Medium',
      leetcode: null,
      leetcodeNum: null,
      file: 'DP/1-Knapsack/1-subsets-sum/recursion.py',
      notes: 'Key insight: For each element, decide to include or exclude to form target sum. Algorithm: Backtracking—if current sum matches target, return true; try both choices. Time: O(2^n) | Space: O(n) call stack'
    },
    {
      name: 'Subset Sum (Top-Down DP)',
      difficulty: 'Medium',
      leetcode: null,
      leetcodeNum: null,
      file: 'DP/1-Knapsack/1-subsets-sum/top-down.py',
      notes: 'Key insight: Memoize on (sum, index) to avoid recomputation of same subproblems. Algorithm: DP table where dp[sum][n]=true if subset of first n elements makes sum. Time: O(sum·n) | Space: O(sum·n) + stack'
    },
    {
      name: 'Partition Equal Subset Sum',
      difficulty: 'Medium',
      leetcode: 'https://leetcode.com/problems/partition-equal-subset-sum/description/',
      leetcodeNum: 416,
      file: 'DP/1-Knapsack/2-subset-partition/top-down.py',
      notes: 'Key insight: Check if subset with sum = total_sum/2 exists (divides array into equal parts). Algorithm: Use subset sum DP with targetSum=total/2. Time: O(n·sum/2) | Space: O(n·sum) + stack'
    },
    {
      name: 'Count Subsets with Target Sum (Negative Numbers)',
      difficulty: 'Hard',
      leetcode: null,
      leetcodeNum: null,
      file: 'DP/1-Knapsack/3-count-of-subset-sum/top-down-negative.py',
      notes: 'Key insight: Count ways to form target sum with negative numbers—memoize on (n, targetSum). Algorithm: Include or exclude each element, accumulate count of valid combinations. Time: O(n·range) | Space: O(n·range) + stack'
    },
    {
      name: 'Rod Cutting (Bottom-Up Unbounded Knapsack)',
      difficulty: 'Medium',
      leetcode: null,
      leetcodeNum: null,
      file: 'DP/2-Unbounded-Knapsack/1-rod-cutting-bottomup.py',
      notes: 'Key insight: Cut rod into pieces to maximize profit (unbounded—can use same piece multiple times). Algorithm: Bottom-up DP where dp[length]=max(profit[piece]+dp[remaining_length]). Time: O(n²) | Space: O(n)'
    },
    {
      name: 'Print LCS (Longest Common Subsequence)',
      difficulty: 'Medium',
      leetcode: null,
      leetcodeNum: null,
      file: 'DP/3-LCS/3-print-lcs.py',
      notes: 'Key insight: Use DP to compute LCS length, then backtrack to reconstruct string. Algorithm: Build LCS length table; trace back matching characters. Time: O(m·n) table + O(m+n) reconstruction | Space: O(m·n)'
    },
    {
      name: 'Print LCS Practice',
      difficulty: 'Medium',
      leetcode: null,
      leetcodeNum: null,
      file: 'DP/3-LCS/print-lcs-practice.py',
      notes: 'Key insight: Two approaches—direct string concatenation (slow) vs length table + backtrack (fast). Algorithm: Store lengths in dp[n][m], backtrack to find LCS. Time: O(m·n) | Space: O(m·n)'
    },
    {
      name: 'Combination Sum (Unbounded Knapsack)',
      difficulty: 'Medium',
      leetcode: 'https://leetcode.com/problems/combination-sum/',
      leetcodeNum: 39,
      file: 'DP/Combination-sum.py',
      notes: 'Key insight: Find all combinations that sum to target (reuse candidates). Algorithm: Backtracking with decision to use same candidate multiple times. Time: O(N^T/M) where N=candidates, T=target, M=min value | Space: O(T/M)'
    }
  ],
  'graph': [
    {
      name: 'Graph Representation (Matrix & List)',
      difficulty: 'Easy',
      leetcode: null,
      leetcodeNum: null,
      file: 'Graph/1-representation.py',
      notes: 'Key insight: Matrix O(V²) space, List O(V+E)—choose based on density. Algorithm: Adjacency matrix vs list vs defaultdict implementations with trade-offs. Time: O(V²+E) matrix, O(V+E) list | Space: O(V²) vs O(V+E)'
    },
    {
      name: 'Depth-First Search (DFS)',
      difficulty: 'Medium',
      leetcode: null,
      leetcodeNum: null,
      file: 'Graph/4.dfs.py',
      notes: 'Key insight: Recursive or iterative DFS for topological sort, cycle detection, paths. Algorithm: Multiple DFS patterns—standard, with path, all paths, cycle detection. Time: O(V+E) | Space: O(V)'
    },
    {
      name: 'BFS Practice',
      difficulty: 'Medium',
      leetcode: null,
      leetcodeNum: null,
      file: 'Graph/3-bfs-practice.py',
      notes: 'Key insight: Multiple queue implementations with different complexities. Algorithm: Compare deque O(1), list index O(V+E), list.pop(0) O(V²+E). Only use deque for O(V+E). Time: O(V+E) optimal | Space: O(V)'
    },
    {
      name: 'Cycle Detection (Undirected, BFS)',
      difficulty: 'Medium',
      leetcode: null,
      leetcodeNum: null,
      file: 'Graph/8-detect-cycle-undirected-bfs.py',
      notes: 'Key insight: Track parent in BFS—cycle if reach visited node that\'s not parent. Algorithm: BFS with parent tracking, check neighbors; non-parent revisit = cycle. Time: O(V+E) | Space: O(V)'
    },
    {
      name: 'Cycle Detection (Undirected, DFS)',
      difficulty: 'Medium',
      leetcode: null,
      leetcodeNum: null,
      file: 'Graph/8-detect-cycle-undirected-dfs.py',
      notes: 'Key insight: Track parent in DFS—cycle exists if visited neighbor is not parent. Algorithm: Recursive DFS with parent parameter, return true if cycle found. Time: O(V+E) | Space: O(V)'
    },
    {
      name: 'Shortest Path in DAG (Topological Sort)',
      difficulty: 'Hard',
      leetcode: null,
      leetcodeNum: null,
      file: 'Graph/13.shortest-path-topo.py',
      notes: 'Key insight: Process DAG nodes in topological order—optimal O(V+E) unlike Dijkstra O(V log V). Handles negative weights. Algorithm: Topo sort via DFS, relax edges in order. Time: O(V+E) | Space: O(V)'
    },
    {
      name: 'Shortest Path in Binary Matrix (BFS)',
      difficulty: 'Medium',
      leetcode: null,
      leetcodeNum: null,
      file: 'Graph/14.shortest-path-bfs.py',
      notes: 'Key insight: Unweighted grid shortest path—use BFS with 8 directions. Early terminate on destination. Algorithm: BFS level-order with 8-directional movement, check boundary & obstacles. Time: O(n²) | Space: O(n²)'
    },
    {
      name: 'Dijkstra\'s Algorithm',
      difficulty: 'Hard',
      leetcode: null,
      leetcodeNum: null,
      file: 'Graph/16-djkstras.py',
      notes: 'Key insight: Greedy shortest path using min-heap for non-negative weights. Algorithm: Always process nearest unvisited node, relax edges. With path reconstruction via parent tracking. Time: O((V+E) log V) | Space: O(V)'
    },
    {
      name: 'Shortest Path Matrix (Floyd-Warshall)',
      difficulty: 'Hard',
      leetcode: null,
      leetcodeNum: null,
      file: 'Graph/17-shortestpath-matrix.py',
      notes: 'Key insight: All-pairs shortest path using intermediate nodes. Algorithm: Triple nested loop over intermediate node k, check if path through k is shorter. Time: O(V³) | Space: O(V²)'
    }
  ],
  'linked-list': [
    {
      name: 'Linked List Implementation',
      difficulty: 'Easy',
      leetcode: null,
      leetcodeNum: null,
      file: 'LinkedList/implement.py',
      notes: 'Key insight: Basic LinkedList and DoublyLinkedList operations—insert at beginning/end. Algorithm: Node creation, traversal, pointer manipulation. Time: O(n) for end insertion (traverse), O(1) for begin | Space: O(1)'
    }
  ],
  'trees': [
    {
      name: 'Binary Tree Level Order Traversal',
      difficulty: 'Medium',
      leetcode: 'https://leetcode.com/problems/binary-tree-level-order-traversal/',
      leetcodeNum: 102,
      file: 'Trees/3-level-order.py',
      notes: 'Key insight: BFS with queue size tracking for level boundaries. Algorithm: Process level by level using queue size to determine when level ends. Time: O(n) | Space: O(w) where w=width'
    },
    {
      name: 'Binary Tree Zigzag Level Order',
      difficulty: 'Medium',
      leetcode: 'https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/',
      leetcodeNum: 103,
      file: 'Trees/4-zig-zag.py',
      notes: 'Key insight: Alternate direction per level—reverse every other level. Algorithm: BFS with boolean flag, reverse level if flag false. Time: O(n) | Space: O(w)'
    },
    {
      name: 'Odd Even Level Order',
      difficulty: 'Medium',
      leetcode: null,
      leetcodeNum: null,
      file: 'Trees/5-odd-even.py',
      notes: 'Key insight: Separate processing of odd/even levels in traversal. Algorithm: BFS with level counter, distinct processing per level type. Time: O(n) | Space: O(w)'
    },
    {
      name: 'Construct Binary Tree from Inorder & Postorder',
      difficulty: 'Medium',
      leetcode: 'https://leetcode.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/',
      leetcodeNum: 106,
      file: 'Trees/6-tree-construction.py',
      notes: 'Key insight: Last element in postorder = root, find root in inorder to partition left/right. Algorithm: Recursive construction by finding root position and splitting arrays. Time: O(n²) | Space: O(h)'
    },
    {
      name: 'Construct Binary Tree from Preorder & Inorder',
      difficulty: 'Medium',
      leetcode: 'https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/',
      leetcodeNum: 105,
      file: 'Trees/7-build-tree-1.py',
      notes: 'Key insight: First element in preorder = root, find in inorder to partition left/right subtrees. Algorithm: Recursive construction with array slicing. Time: O(n²) worst case | Space: O(h)'
    },
    {
      name: 'Maximum Binary Tree',
      difficulty: 'Medium',
      leetcode: 'https://leetcode.com/problems/maximum-binary-tree/description/',
      leetcodeNum: 654,
      file: 'Trees/8-max-binary-tree.py',
      notes: 'Key insight: Root = max element, recursively construct left and right from subarrays. Algorithm: Find max, split array, recursive construction. Time: O(n²) worst case | Space: O(h)'
    },
    {
      name: 'Construct BST from Preorder',
      difficulty: 'Medium',
      leetcode: 'https://leetcode.com/problems/construct-binary-search-tree-from-preorder-traversal/',
      leetcodeNum: 1008,
      file: 'Trees/9-construct-bst.py',
      notes: 'Key insight: Sort preorder to get inorder, then use inorder+preorder construction algorithm. Algorithm: Create both sequences, build tree via partition. Time: O(n log n) | Space: O(h)'
    },
    {
      name: 'Maximum Depth of Binary Tree',
      difficulty: 'Easy',
      leetcode: 'https://leetcode.com/problems/maximum-depth-of-binary-tree/',
      leetcodeNum: 104,
      file: 'Trees/10-max-depth.py',
      notes: 'Key insight: Recursive—return 1 + max(left_depth, right_depth). Algorithm: DFS post-order traversal, compute height bottom-up. Time: O(n) | Space: O(h)'
    },
    {
      name: 'Balanced Binary Tree',
      difficulty: 'Easy',
      leetcode: 'https://leetcode.com/problems/balanced-binary-tree/',
      leetcodeNum: 110,
      file: 'Trees/11-check-balance-tree.py',
      notes: 'Key insight: Sentinel pattern—return -1 if unbalanced, else return height. Algorithm: DFS checking height difference ≤1 at each node. Time: O(n) | Space: O(h)'
    },
    {
      name: 'Binary Tree Diameter',
      difficulty: 'Medium',
      leetcode: 'https://leetcode.com/problems/diameter-of-binary-tree/',
      leetcodeNum: 543,
      file: 'Trees/12-diameter.py',
      notes: 'Key insight: Diameter = longest path between any two nodes = max(left_height + right_height). Algorithm: DFS post-order, track max sum at each node. Time: O(n) | Space: O(h)'
    },
    {
      name: 'Path Sum (Root to Leaf)',
      difficulty: 'Medium',
      leetcode: 'https://leetcode.com/problems/path-sum-ii/',
      leetcodeNum: 113,
      file: 'Trees/13-path-sum.py',
      notes: 'Key insight: Find all paths where sum = target, backtracking with path restoration. Algorithm: DFS with current path list, append at leaf if sum matches. Time: O(n·h) | Space: O(h)'
    },
    {
      name: 'Sum Root to Leaf Numbers',
      difficulty: 'Medium',
      leetcode: 'https://leetcode.com/problems/sum-root-to-leaf-numbers/',
      leetcodeNum: 129,
      file: 'Trees/14-sum-root-to-leaf.py',
      notes: 'Key insight: Treat each path as number—multiply by 10 and add current node value. Algorithm: DFS computing numbers top-down, sum leaf values. Time: O(n) | Space: O(h)'
    },
    {
      name: 'Insufficient Nodes in Root to Leaf Paths',
      difficulty: 'Medium',
      leetcode: 'https://leetcode.com/problems/insufficient-nodes-in-root-to-leaf-paths/description/',
      leetcodeNum: 1080,
      file: 'Trees/15-insufficient-nodes.py',
      notes: 'Key insight: Remove nodes whose path sum < limit. Algorithm: DFS returns None if insufficient, parent captures return value to update pointer. Time: O(n) | Space: O(h)'
    },
    {
      name: 'Lowest Common Ancestor',
      difficulty: 'Medium',
      leetcode: 'https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/',
      leetcodeNum: 236,
      file: 'Trees/16-LCA.py',
      notes: 'Key insight: Post-order DFS—LCA is first node where both p,q found in subtrees. Algorithm: If both subtrees have target, current is LCA; else return non-null side. Time: O(n) | Space: O(h)'
    },
    {
      name: 'Minimum Absolute Difference in BST',
      difficulty: 'Easy',
      leetcode: 'https://leetcode.com/problems/minimum-absolute-difference-in-bst/',
      leetcodeNum: 530,
      file: 'Trees/17-BST.py',
      notes: 'Key insight: Inorder traversal of BST = sorted array. Min diff = consecutive elements in sorted order. Time: O(n) | Space: O(h)'
    },
    {
      name: 'Maximum Difference Between Node and Ancestor',
      difficulty: 'Medium',
      leetcode: 'https://leetcode.com/problems/maximum-difference-between-node-and-ancestor/description/',
      leetcodeNum: 1026,
      file: 'Trees/17-maxDiff.py',
      notes: 'Key insight: Track min/max ancestor values top-down. Difference = max_ancestor - min_ancestor at each node. Algorithm: DFS passing min/max from ancestors. Time: O(n) | Space: O(h)'
    }
  ]
};

// Read current data.js
const dataPath = path.join(__dirname, 'data.js');
let dataContent = fs.readFileSync(dataPath, 'utf8');

// Load TOPICS array
const fn = new Function(dataContent + '; return TOPICS;');
const TOPICS = fn();

// Add new problems to each topic
Object.keys(NEW_PROBLEMS).forEach(topicId => {
  const topic = TOPICS.find(t => t.id === topicId);
  if (topic) {
    topic.problems.push(...NEW_PROBLEMS[topicId]);
    console.log(`✓ Added ${NEW_PROBLEMS[topicId].length} problems to ${topic.name}`);
  } else {
    console.warn(`⚠ Topic ${topicId} not found!`);
  }
});

// Generate updated data.js content
const lines = [
  'const TOPICS = [',
];

TOPICS.forEach((topic, topicIdx) => {
  lines.push(`  {`);
  lines.push(`    id: ${JSON.stringify(topic.id)},`);
  lines.push(`    name: ${JSON.stringify(topic.name)},`);
  lines.push(`    color: ${JSON.stringify(topic.color)},`);
  lines.push(`    emoji: ${JSON.stringify(topic.emoji)},`);
  lines.push(`    ring: ${JSON.stringify(topic.ring)},`);

  if (topic.tips) {
    lines.push(`    tips: [`);
    topic.tips.forEach(tip => {
      lines.push(`      ${JSON.stringify(tip)},`);
    });
    lines.push(`    ],`);
  }

  if (topic.problems) {
    lines.push(`    problems: [`);
    topic.problems.forEach(problem => {
      lines.push(`      {`);
      lines.push(`        name: ${JSON.stringify(problem.name)},`);
      lines.push(`        difficulty: ${JSON.stringify(problem.difficulty)},`);
      lines.push(`        leetcode: ${JSON.stringify(problem.leetcode)},`);
      lines.push(`        leetcodeNum: ${problem.leetcodeNum},`);
      lines.push(`        file: ${JSON.stringify(problem.file)},`);
      lines.push(`        notes: ${JSON.stringify(problem.notes)},`);
      lines.push(`      },`);
    });
    lines.push(`    ],`);
  }

  lines.push(`  },`);
  lines.push('');
});

lines.push('];');
lines.push('');

// Write updated data.js
fs.writeFileSync(dataPath, lines.join('\n'), 'utf8');
console.log(`\n✅ Updated ${dataPath}`);
console.log(`📊 Total topics: ${TOPICS.length}`);
console.log(`📝 Total problems: ${TOPICS.reduce((s, t) => s + (t.problems ? t.problems.length : 0), 0)}`);
