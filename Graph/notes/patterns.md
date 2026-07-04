1. if matrix me adjacent element movement ho, toh graph lagega, aise me directions move kro (like bfs)
2. agar matrix me aise traverse krna hai ki sare adjacent ek time pe like rotten oranges ya flood fil, toh we can use bfs
3. jaha bhi mujhe kuch states store krne ho while traversal, mai queue me hi as tuple add kr dungi, jaise ki level ya fir parent etc (dist vagera bhi)
4. edge cases me humesha disconnected graph ka bhi sochna
5. self loop, cycle etc sochna

═══════════════════════════════════════════════════════════
MISTAKE LOG - Shortest Path in Binary Matrix
═══════════════════════════════════════════════════════════

❌ MISTAKE: dist += 1 inside while loop (global counter)
Problem: Incrementing for EVERY node, not per distance level
Result: Multiple nodes at same level get different distances

✅ FIX 1 - Store distance in queue:
   queue.append((r, c, dist+1))

✅ FIX 2 - Level-order BFS:
   for _ in range(len(queue)):  # Process all current level
       dist += 1  # Increment once per level, not per node

KEY: Distance = steps to reach a node, NOT number of nodes processed
