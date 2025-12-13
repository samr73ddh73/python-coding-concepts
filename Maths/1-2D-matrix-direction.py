"""
================================================================================
PATTERN: 2D Direction Rotation - Robot Bounded in Circle
================================================================================
https://leetcode.com/problems/robot-bounded-in-circle/

CONCEPT:
Robot starts at (0,0) facing NORTH. Given instructions (G=go forward, L=left, R=right),
determine if robot is bounded in a circle.

KEY INSIGHT:
Robot is bounded if EITHER:
1. Returns to origin (0,0) after one cycle
2. Not facing NORTH after one cycle (will eventually return after 2/4 cycles)

Why? If direction changes, robot creates a circular path:
- 90° turn  → Square (4 cycles to return)
- 180° turn → Line back and forth (2 cycles)
- 270° turn → Square (4 cycles)

TIME: O(n), SPACE: O(1)
"""

class Solution:
    def isRobotBounded(self, instructions: str) -> bool:
        x, y, dx, dy = 0, 0, 0, 1  # Start at (0,0) facing NORTH (0,1)

        for i in instructions:
            if i == 'L':
                dx, dy = -dy, dx   # Rotate 90° counter-clockwise
            if i == 'R':
                dx, dy = dy, -dx   # Rotate 90° clockwise
            if i == 'G':
                x += dx
                y += dy

        # Bounded if: back at origin OR direction changed
        return (x, y) == (0, 0) or (dx, dy) != (0, 1)


"""
================================================================================
CORE CONCEPT: Direction Vectors & Rotation
================================================================================

DIRECTION REPRESENTATION:
Use (dx, dy) to represent direction in 2D grid

Direction | (dx, dy) | Meaning
----------|----------|--------
NORTH     | (0, 1)   | Move up
EAST      | (1, 0)   | Move right
SOUTH     | (0, -1)  | Move down
WEST      | (-1, 0)  | Move left

ROTATION FORMULAS:
Left (90° counter-clockwise):  (dx, dy) → (-dy, dx)
Right (90° clockwise):         (dx, dy) → (dy, -dx)

VISUAL:
         NORTH (0,1)
             ↑
             |
WEST ←------+------→ EAST
(-1,0)      |      (1,0)
            |
            ↓
        SOUTH (0,-1)

LEFT rotation from NORTH (0,1):
  (-dy, dx) = (-1, 0) = WEST ✓

RIGHT rotation from NORTH (0,1):
  (dy, -dx) = (1, 0) = EAST ✓
"""


"""
================================================================================
TRACE EXAMPLE
================================================================================

Instructions: "GL"

Initial: x=0, y=0, dx=0, dy=1 (facing NORTH)

Step 1: 'G'
  x += dx → x=0
  y += dy → y=1
  Position: (0,1), Direction: NORTH (0,1)

Step 2: 'L'
  dx, dy = -dy, dx = (-1, 0)
  Position: (0,1), Direction: WEST (-1,0)

After 1 cycle:
  Position: (0,1) ≠ (0,0)
  Direction: (-1,0) ≠ (0,1) → Direction changed!

Return: True (bounded) ✓

Why bounded?
After 4 cycles, robot completes a square:
Cycle 1: (0,1) facing WEST
Cycle 2: (-1,1) facing SOUTH
Cycle 3: (-1,0) facing EAST
Cycle 4: (0,0) facing NORTH → Back to start!
"""


"""
================================================================================
WHY DIRECTION CHANGE = BOUNDED?
================================================================================

Case 1: Direction = NORTH after 1 cycle
- Robot will repeat exact same path forever
- Only bounded if already at origin

Case 2: Direction ≠ NORTH after 1 cycle
- Robot facing different direction
- After k cycles (k ≤ 4), will return to origin

Proof:
- 4 directions total (N, E, S, W)
- Each cycle rotates by some angle
- After at most 4 cycles, robot faces NORTH again
- Since relative path is same each cycle, returns to origin

Example: "GR" (go forward, turn right)
Cycle 1: (0,1) facing EAST
Cycle 2: (1,1) facing SOUTH
Cycle 3: (1,0) facing WEST
Cycle 4: (0,0) facing NORTH → Bounded! ✓
"""


"""
================================================================================
ROTATION MATRIX EXPLANATION
================================================================================

LEFT (counter-clockwise 90°):
Rotation matrix:
  | 0  -1 |   |dx|   |-dy|
  | 1   0 | × |dy| = |dx |

RIGHT (clockwise 90°):
Rotation matrix:
  | 0   1 |   |dx|   |dy |
  |-1   0 | × |dy| = |-dx|

PATTERN:
(dx, dy) → (-dy, dx)  Left rotation
(dx, dy) → (dy, -dx)  Right rotation

MEMORY TRICK:
LEFT:  Put NEGATIVE on first → (-dy, dx)
RIGHT: Put POSITIVE on first → (dy, -dx)
"""


"""
================================================================================
ALL 4 ROTATIONS FROM EACH DIRECTION
================================================================================

Starting from NORTH (0, 1):
  Left  → (-1, 0) WEST
  Right → (1, 0)  EAST

Starting from EAST (1, 0):
  Left  → (0, 1)  NORTH
  Right → (0, -1) SOUTH

Starting from SOUTH (0, -1):
  Left  → (1, 0)  EAST
  Right → (-1, 0) WEST

Starting from WEST (-1, 0):
  Left  → (0, -1) SOUTH
  Right → (0, 1)  NORTH

VERIFY FORMULA:
NORTH (0,1) + LEFT = (-1,0) = (-dy, dx) = (-1, 0) ✓
NORTH (0,1) + RIGHT = (1,0) = (dy, -dx) = (1, 0) ✓
"""


"""
================================================================================
ALTERNATIVE: Using Direction Index
================================================================================

def isRobotBounded(instructions):
    directions = [(0,1), (1,0), (0,-1), (-1,0)]  # N, E, S, W
    x, y, d = 0, 0, 0  # d = direction index

    for i in instructions:
        if i == 'L':
            d = (d - 1) % 4  # Counter-clockwise
        elif i == 'R':
            d = (d + 1) % 4  # Clockwise
        else:
            dx, dy = directions[d]
            x += dx
            y += dy

    return (x, y) == (0, 0) or d != 0

COMPARISON:
✓ Direction vector (dx,dy): Cleaner, no array needed
✗ Direction index: More intuitive but uses extra array
"""


"""
================================================================================
COMMON PATTERNS WITH DIRECTIONS
================================================================================

1. GRID TRAVERSAL (4 directions):
directions = [(0,1), (1,0), (0,-1), (-1,0)]  # N, E, S, W

2. GRID TRAVERSAL (8 directions):
directions = [(-1,-1), (-1,0), (-1,1), (0,-1),
              (0,1), (1,-1), (1,0), (1,1)]

3. ROTATION WITH (dx, dy):
Left:  dx, dy = -dy, dx
Right: dx, dy = dy, -dx

4. ROTATION WITH INDEX:
Left:  d = (d - 1) % 4
Right: d = (d + 1) % 4

5. MOVE IN CURRENT DIRECTION:
x += dx
y += dy
"""


"""
================================================================================
RELATED PROBLEMS
================================================================================

1. Robot Bounded in Circle (LC 1041) - This problem
2. Walking Robot Simulation (LC 874) - Similar direction tracking
3. Spiral Matrix (LC 54) - Direction change on boundary
4. Robot Room Cleaner (LC 489) - Track position and direction

KEY SKILL: 2D direction vectors + rotation formulas
"""


"""
================================================================================
FANG INTERVIEW TIPS
================================================================================

1. "Use (dx,dy) for direction - cleaner than direction index"

2. "Left rotation: (-dy, dx), Right rotation: (dy, -dx)"

3. "Robot bounded if returns to origin OR direction changes"

4. "Direction change means circular path in at most 4 cycles"

5. "Time O(n), Space O(1) - process instructions once"

6. "Alternative: Track direction index with (d±1)%4 for rotation"

================================================================================
COMPLEXITY
================================================================================

TIME: O(n) - Process each instruction once
SPACE: O(1) - Only track (x,y,dx,dy)

No need to simulate multiple cycles!
"""


# Test examples
if __name__ == "__main__":
    sol = Solution()

    print(sol.isRobotBounded("GGLLGG"))  # True - returns to origin
    print(sol.isRobotBounded("GG"))      # False - goes to (0,2), still facing N
    print(sol.isRobotBounded("GL"))      # True - direction changes
    print(sol.isRobotBounded("GLGLGGLGL"))  # False
