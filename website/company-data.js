// Company-wise LeetCode Questions Data
// Source: https://github.com/snehasishroy/leetcode-companywise-interview-questions

const companyQuestions = {
    google: {
        name: "Google",
        color: "#4285f4",
        topQuestions: [
            { id: 1, title: "Two Sum", number: 1, difficulty: "Easy", category: "Array", frequency: "Very High" },
            { id: 2, title: "Add Two Numbers", number: 2, difficulty: "Medium", category: "LinkedList", frequency: "High" },
            { id: 3, title: "Longest Substring Without Repeating Characters", number: 3, difficulty: "Medium", category: "String", frequency: "Very High" },
            { id: 4, title: "Median of Two Sorted Arrays", number: 4, difficulty: "Hard", category: "Array", frequency: "High" },
            { id: 5, title: "Longest Palindromic Substring", number: 5, difficulty: "Medium", category: "String", frequency: "High" },
            { id: 6, title: "Regular Expression Matching", number: 10, difficulty: "Hard", category: "DP", frequency: "Medium" },
            { id: 7, title: "Container With Most Water", number: 11, difficulty: "Medium", category: "Array", frequency: "Very High" },
            { id: 8, title: "3Sum", number: 15, difficulty: "Medium", category: "Array", frequency: "Very High" },
            { id: 9, title: "Letter Combinations of a Phone Number", number: 17, difficulty: "Medium", category: "Backtracking", frequency: "High" },
            { id: 10, title: "Remove Nth Node From End of List", number: 19, difficulty: "Medium", category: "LinkedList", frequency: "High" },
        ]
    },
    amazon: {
        name: "Amazon",
        color: "#FF9900",
        topQuestions: [
            { id: 11, title: "Two Sum", number: 1, difficulty: "Easy", category: "Array", frequency: "Very High" },
            { id: 12, title: "Reverse Integer", number: 7, difficulty: "Easy", category: "Math", frequency: "High" },
            { id: 13, title: "Longest Substring Without Repeating Characters", number: 3, difficulty: "Medium", category: "String", frequency: "Very High" },
            { id: 14, title: "Container With Most Water", number: 11, difficulty: "Medium", category: "Array", frequency: "Very High" },
            { id: 15, title: "Binary Tree Level Order Traversal", number: 102, difficulty: "Medium", category: "Tree", frequency: "Very High" },
            { id: 16, title: "Merge K Sorted Lists", number: 23, difficulty: "Hard", category: "LinkedList", frequency: "High" },
            { id: 17, title: "LRU Cache", number: 146, difficulty: "Hard", category: "Design", frequency: "Very High" },
            { id: 18, title: "Number of Islands", number: 200, difficulty: "Medium", category: "Graph", frequency: "Very High" },
            { id: 19, title: "Longest Increasing Subsequence", number: 300, difficulty: "Medium", category: "DP", frequency: "High" },
            { id: 20, title: "Coin Change", number: 322, difficulty: "Medium", category: "DP", frequency: "Very High" },
        ]
    },
    microsoft: {
        name: "Microsoft",
        color: "#00A4EF",
        topQuestions: [
            { id: 21, title: "Two Sum", number: 1, difficulty: "Easy", category: "Array", frequency: "Very High" },
            { id: 22, title: "Reverse String", number: 344, difficulty: "Easy", category: "String", frequency: "High" },
            { id: 23, title: "Merge Two Sorted Lists", number: 21, difficulty: "Easy", category: "LinkedList", frequency: "Very High" },
            { id: 24, title: "Binary Tree Level Order Traversal", number: 102, difficulty: "Medium", category: "Tree", frequency: "Very High" },
            { id: 25, title: "Longest Palindromic Substring", number: 5, difficulty: "Medium", category: "String", frequency: "High" },
            { id: 26, title: "LRU Cache", number: 146, difficulty: "Hard", category: "Design", frequency: "Very High" },
            { id: 27, title: "Binary Search Tree to Greater Sum Tree", number: 1038, difficulty: "Medium", category: "Tree", frequency: "High" },
            { id: 28, title: "Word Ladder II", number: 126, difficulty: "Hard", category: "Graph", frequency: "Medium" },
            { id: 29, title: "Trapping Rain Water", number: 42, difficulty: "Hard", category: "Array", frequency: "High" },
            { id: 30, title: "Median of Two Sorted Arrays", number: 4, difficulty: "Hard", category: "Array", frequency: "High" },
        ]
    },
    meta: {
        name: "Meta",
        color: "#1877F2",
        topQuestions: [
            { id: 31, title: "Two Sum", number: 1, difficulty: "Easy", category: "Array", frequency: "Very High" },
            { id: 32, title: "Longest Substring Without Repeating Characters", number: 3, difficulty: "Medium", category: "String", frequency: "Very High" },
            { id: 33, title: "Container With Most Water", number: 11, difficulty: "Medium", category: "Array", frequency: "Very High" },
            { id: 34, title: "Number of Islands", number: 200, difficulty: "Medium", category: "Graph", frequency: "Very High" },
            { id: 35, title: "BinaryTree Maximum Path Sum", number: 124, difficulty: "Hard", category: "Tree", frequency: "High" },
            { id: 36, title: "Word Ladder", number: 127, difficulty: "Hard", category: "Graph", frequency: "High" },
            { id: 37, title: "LRU Cache", number: 146, difficulty: "Hard", category: "Design", frequency: "Very High" },
            { id: 38, title: "Merge K Sorted Lists", number: 23, difficulty: "Hard", category: "LinkedList", frequency: "High" },
            { id: 39, title: "Median of Two Sorted Arrays", number: 4, difficulty: "Hard", category: "Array", frequency: "Medium" },
            { id: 40, title: "Trapping Rain Water", number: 42, difficulty: "Hard", category: "Array", frequency: "High" },
        ]
    },
    uber: {
        name: "Uber",
        color: "#000000",
        topQuestions: [
            { id: 41, title: "Two Sum", number: 1, difficulty: "Easy", category: "Array", frequency: "Very High" },
            { id: 42, title: "Add Two Numbers", number: 2, difficulty: "Medium", category: "LinkedList", frequency: "High" },
            { id: 43, title: "Longest Substring Without Repeating Characters", number: 3, difficulty: "Medium", category: "String", frequency: "Very High" },
            { id: 44, title: "Best Time to Buy and Sell Stock", number: 121, difficulty: "Easy", category: "Array", frequency: "Very High" },
            { id: 45, title: "Number of Islands", number: 200, difficulty: "Medium", category: "Graph", frequency: "Very High" },
            { id: 46, title: "Course Schedule II", number: 210, difficulty: "Medium", category: "Graph", frequency: "High" },
            { id: 47, title: "LRU Cache", number: 146, difficulty: "Hard", category: "Design", frequency: "Very High" },
            { id: 48, title: "Merge K Sorted Lists", number: 23, difficulty: "Hard", category: "LinkedList", frequency: "High" },
            { id: 49, title: "Median of Two Sorted Arrays", number: 4, difficulty: "Hard", category: "Array", frequency: "Medium" },
            { id: 50, title: "Binary Tree Maximum Path Sum", number: 124, difficulty: "Hard", category: "Tree", frequency: "High" },
        ]
    },
    linkedin: {
        name: "LinkedIn",
        color: "#0A66C2",
        topQuestions: [
            { id: 51, title: "Two Sum", number: 1, difficulty: "Easy", category: "Array", frequency: "Very High" },
            { id: 52, title: "Reverse Linked List", number: 206, difficulty: "Easy", category: "LinkedList", frequency: "Very High" },
            { id: 53, title: "Merge Two Sorted Lists", number: 21, difficulty: "Easy", category: "LinkedList", frequency: "Very High" },
            { id: 54, title: "Longest Substring Without Repeating Characters", number: 3, difficulty: "Medium", category: "String", frequency: "Very High" },
            { id: 55, title: "Number of Islands", number: 200, difficulty: "Medium", category: "Graph", frequency: "Very High" },
            { id: 56, title: "Sort List", number: 148, difficulty: "Medium", category: "LinkedList", frequency: "High" },
            { id: 57, title: "LRU Cache", number: 146, difficulty: "Hard", category: "Design", frequency: "Very High" },
            { id: 58, title: "Word Ladder II", number: 126, difficulty: "Hard", category: "Graph", frequency: "High" },
            { id: 59, title: "Merge K Sorted Lists", number: 23, difficulty: "Hard", category: "LinkedList", frequency: "Very High" },
            { id: 60, title: "Binary Search Tree Iterator", number: 173, difficulty: "Hard", category: "Tree", frequency: "High" },
        ]
    },
    atlassian: {
        name: "Atlassian",
        color: "#0052CC",
        topQuestions: [
            { id: 61, title: "Two Sum", number: 1, difficulty: "Easy", category: "Array", frequency: "Very High" },
            { id: 62, title: "Valid Parentheses", number: 20, difficulty: "Easy", category: "Stack", frequency: "Very High" },
            { id: 63, title: "Merge Two Sorted Lists", number: 21, difficulty: "Easy", category: "LinkedList", frequency: "Very High" },
            { id: 64, title: "Longest Substring Without Repeating Characters", number: 3, difficulty: "Medium", category: "String", frequency: "Very High" },
            { id: 65, title: "Number of Islands", number: 200, difficulty: "Medium", category: "Graph", frequency: "Very High" },
            { id: 66, title: "LRU Cache", number: 146, difficulty: "Hard", category: "Design", frequency: "Very High" },
            { id: 67, title: "Word Ladder", number: 127, difficulty: "Hard", category: "Graph", frequency: "High" },
            { id: 68, title: "Merge K Sorted Lists", number: 23, difficulty: "Hard", category: "LinkedList", frequency: "High" },
            { id: 69, title: "Median of Two Sorted Arrays", number: 4, difficulty: "Hard", category: "Array", frequency: "Medium" },
            { id: 70, title: "Trapping Rain Water", number: 42, difficulty: "Hard", category: "Array", frequency: "High" },
        ]
    },
    salesforce: {
        name: "Salesforce",
        color: "#00A1E0",
        topQuestions: [
            { id: 71, title: "Two Sum", number: 1, difficulty: "Easy", category: "Array", frequency: "Very High" },
            { id: 72, title: "Reverse String", number: 344, difficulty: "Easy", category: "String", frequency: "High" },
            { id: 73, title: "Merge Two Sorted Lists", number: 21, difficulty: "Easy", category: "LinkedList", frequency: "Very High" },
            { id: 74, title: "Longest Substring Without Repeating Characters", number: 3, difficulty: "Medium", category: "String", frequency: "Very High" },
            { id: 75, title: "Number of Islands", number: 200, difficulty: "Medium", category: "Graph", frequency: "Very High" },
            { id: 76, title: "Coin Change", number: 322, difficulty: "Medium", category: "DP", frequency: "High" },
            { id: 77, title: "LRU Cache", number: 146, difficulty: "Hard", category: "Design", frequency: "Very High" },
            { id: 78, title: "Word Ladder II", number: 126, difficulty: "Hard", category: "Graph", frequency: "High" },
            { id: 79, title: "Binary Search Tree Iterator", number: 173, difficulty: "Hard", category: "Tree", frequency: "High" },
            { id: 80, title: "Trapping Rain Water", number: 42, difficulty: "Hard", category: "Array", frequency: "High" },
        ]
    },
    apple: {
        name: "Apple",
        color: "#555555",
        topQuestions: [
            { id: 81, title: "Two Sum", number: 1, difficulty: "Easy", category: "Array", frequency: "Very High" },
            { id: 82, title: "Reverse Linked List", number: 206, difficulty: "Easy", category: "LinkedList", frequency: "Very High" },
            { id: 83, title: "Longest Substring Without Repeating Characters", number: 3, difficulty: "Medium", category: "String", frequency: "Very High" },
            { id: 84, title: "Container With Most Water", number: 11, difficulty: "Medium", category: "Array", frequency: "Very High" },
            { id: 85, title: "Lowest Common Ancestor of a Binary Tree", number: 236, difficulty: "Medium", category: "Tree", frequency: "Very High" },
            { id: 86, title: "LRU Cache", number: 146, difficulty: "Hard", category: "Design", frequency: "Very High" },
            { id: 87, title: "Merge K Sorted Lists", number: 23, difficulty: "Hard", category: "LinkedList", frequency: "High" },
            { id: 88, title: "Binary Tree Maximum Path Sum", number: 124, difficulty: "Hard", category: "Tree", frequency: "High" },
            { id: 89, title: "Median of Two Sorted Arrays", number: 4, difficulty: "Hard", category: "Array", frequency: "Medium" },
            { id: 90, title: "Word Ladder II", number: 126, difficulty: "Hard", category: "Graph", frequency: "High" },
        ]
    },
    netflix: {
        name: "Netflix",
        color: "#E50914",
        topQuestions: [
            { id: 91, title: "Two Sum", number: 1, difficulty: "Easy", category: "Array", frequency: "Very High" },
            { id: 92, title: "Valid Parentheses", number: 20, difficulty: "Easy", category: "Stack", frequency: "Very High" },
            { id: 93, title: "Longest Substring Without Repeating Characters", number: 3, difficulty: "Medium", category: "String", frequency: "Very High" },
            { id: 94, title: "Number of Islands", number: 200, difficulty: "Medium", category: "Graph", frequency: "Very High" },
            { id: 95, title: "Course Schedule II", number: 210, difficulty: "Medium", category: "Graph", frequency: "High" },
            { id: 96, title: "LRU Cache", number: 146, difficulty: "Hard", category: "Design", frequency: "Very High" },
            { id: 97, title: "Merge K Sorted Lists", number: 23, difficulty: "Hard", category: "LinkedList", frequency: "High" },
            { id: 98, title: "Median of Two Sorted Arrays", number: 4, difficulty: "Hard", category: "Array", frequency: "High" },
            { id: 99, title: "Trapping Rain Water", number: 42, difficulty: "Hard", category: "Array", frequency: "High" },
            { id: 100, title: "Binary Tree Maximum Path Sum", number: 124, difficulty: "Hard", category: "Tree", frequency: "High" },
        ]
    },
    airbnb: {
        name: "Airbnb",
        color: "#FF5A5F",
        topQuestions: [
            { id: 101, title: "Two Sum", number: 1, difficulty: "Easy", category: "Array", frequency: "Very High" },
            { id: 102, title: "Merge Two Sorted Lists", number: 21, difficulty: "Easy", category: "LinkedList", frequency: "Very High" },
            { id: 103, title: "Longest Substring Without Repeating Characters", number: 3, difficulty: "Medium", category: "String", frequency: "Very High" },
            { id: 104, title: "Number of Islands", number: 200, difficulty: "Medium", category: "Graph", frequency: "Very High" },
            { id: 105, title: "Course Schedule", number: 207, difficulty: "Medium", category: "Graph", frequency: "High" },
            { id: 106, title: "LRU Cache", number: 146, difficulty: "Hard", category: "Design", frequency: "Very High" },
            { id: 107, title: "Word Ladder", number: 127, difficulty: "Hard", category: "Graph", frequency: "High" },
            { id: 108, title: "Merge K Sorted Lists", number: 23, difficulty: "Hard", category: "LinkedList", frequency: "High" },
            { id: 109, title: "Median of Two Sorted Arrays", number: 4, difficulty: "Hard", category: "Array", frequency: "Medium" },
            { id: 110, title: "Trapping Rain Water", number: 42, difficulty: "Hard", category: "Array", frequency: "High" },
        ]
    },
};

// Decision Making Patterns - When to use which technique
const decisionPatterns = {
    array: {
        title: "Array Problems - Decision Tree",
        flowchart: `
Does it involve finding pairs/subarrays?
├─ YES, need O(1) lookups?
│  └─ Use HashMap/Set (Two Sum, Anagrams)
├─ YES, need contiguous elements?
│  └─ Use Sliding Window (Max subarray, substring problems)
└─ Rearranging elements in range [0, n)?
   └─ Use Indexing as HashMap (Find duplicates, missing number)

Does it need maximum/minimum value in range?
└─ Use Binary Search or Monotonic Stack

Does it involve merging intervals?
└─ Sort by start, then check overlaps (Two pointers)

Does it need O(1) space without modifying array?
└─ Use Two-pointer technique
        `
    },
    graph: {
        title: "Graph Problems - Decision Tree",
        flowchart: `
Need shortest path?
├─ Unweighted → Use BFS
└─ Weighted → Use Dijkstra

Need cycle detection?
├─ Undirected → DFS with parent check OR DSU
└─ Directed → DFS with pathVisited (3-color)

Need topological sort?
├─ Verify it's a DAG first!
└─ Use Kahn's algorithm OR DFS post-order

Connected components?
├─ DFS/BFS from each unvisited
└─ OR Union-Find (DSU)

Matrix/Grid problem?
├─ Multi-source? → Add all sources, then BFS
└─ Single source → DFS for all paths OR BFS for shortest
        `
    },
    tree: {
        title: "Tree Problems - Decision Tree",
        flowchart: `
Path problems (root to leaf)?
├─ Use DFS Pre-order (TOP-DOWN)
└─ Track path as you go down

Need info from children first (heights, counts)?
├─ Use DFS Post-order (BOTTOM-UP)
└─ LCA, balanced tree, diameter

Level-wise information needed?
├─ Use BFS (Queue)
└─ Level order, width, first occurrence

Construction from traversals?
├─ Preorder + Inorder → Find root, split left/right
└─ Postorder + Inorder → Find root, split left/right

Iterative traversal (no recursion)?
└─ Use explicit Stack for DFS
        `
    },
    dp: {
        title: "DP Problems - Decision Tree",
        flowchart: `
Optimization problem (maximize/minimize)?
└─ Check if has optimal substructure

Counting problem (count ways)?
└─ Check if overlapping subproblems exist

Is it a sequence problem (LCS, LIS)?
├─ 2D DP: O(m × n)
└─ Space optimize: O(min(m, n))

Is it a knapsack variant?
├─ 0/1 Knapsack → iterate capacity backward
├─ Unbounded → iterate capacity forward
└─ Partition → check feasibility with weights

Is it multi-dimensional?
├─ Grid DP → 2D array
├─ Interval DP → 2D array (MCM, palindrome partition)
└─ String DP → depends on problem (edit distance, regex)

Can't find recurrence?
└─ Might not be DP! Try Greedy or other approach
        `
    },
    binarySearch: {
        title: "Binary Search - Decision Tree",
        flowchart: `
Search in sorted array?
├─ Find exact match → Standard BS
├─ Find position to insert → Lower bound
├─ Find first > target → Upper bound
└─ Rotated sorted → Modified BS

Search in answer space?
├─ Can define bounds [low, high]?
├─ Monotonic predicate? (more capacity → always true)
└─ Use BS on answer (capacity to ship, koko bananas)

Peak/Valley finding?
├─ Peak element → Check middle neighbors
└─ Find rotation point → Compare with end

Search in matrix?
├─ Treat as 1D sorted array
└─ Binary search on row, then column

Can't use BS?
└─ Usually array is not sorted or no monotonic property
        `
    },
    greedy: {
        title: "Greedy Problems - Decision Tree",
        flowchart: `
Can I solve with local optimal choice?
├─ YES → Might be greedy
└─ NO → Probably DP

Does greedy choice not block future choices?
├─ YES → Verify with examples/proof
└─ NO → Use DP instead

Activity selection / Interval problems?
├─ Sort by end time, greedily pick non-overlapping
└─ Check for contradiction first

Job sequencing / Deadlines?
├─ Sort by profit (or time), pick greedily
└─ Check feasibility

Change making / Coins?
├─ Local optimal ≠ global → TRAP! Use DP
└─ Only works for specific coin systems

Jumping game / Fuel / Steps?
├─ Greedy: always pick maximum reach
└─ Verify it reaches end

When greedy FAILS (TRAP):
└─ Coin change (arbitrary coin system)
└─ Cannot be split into groups
└─ Future decisions depend on current
        `
    }
};
