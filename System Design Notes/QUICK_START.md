# Contention Learning Quick Start

## 📋 Your Learning Path

### Phase 1: Setup (30 minutes)
- [ ] Install PostgreSQL from https://www.postgresql.org/download/windows/
- [ ] Create `contention_lab` database
- [ ] Install Python driver: `pip install psycopg2-binary`
- [ ] Test connection with sample script
- **Guide:** `POSTGRES_SETUP_WINDOWS.md`

### Phase 2: Theory (45 minutes)
- [ ] Read: Race conditions, isolation levels, locking strategies
- [ ] Understand: MVCC, pessimistic vs optimistic locking
- [ ] Know: SERIALIZABLE, REPEATABLE READ, READ COMMITTED
- **Guide:** `Theory/3-Contention.md` (Parts 1-2)

### Phase 3: Hands-On Demos (60 minutes)
- [ ] Run: `postgres_race_condition.py` - See unsafe operations
- [ ] Run: `postgres_isolation_levels.py` - See snapshot isolation
- [ ] Run: `postgres_deadlocks_advisory_locks.py` - See deadlock scenarios
- [ ] Experiment: Modify scripts, see different outcomes
- **Guides:** Examples in `Theory/3-Contention.md` (Parts 3-7)

### Phase 4: Manual Testing (45 minutes)
- [ ] Open two psql terminals side-by-side
- [ ] Test READ COMMITTED vs REPEATABLE READ
- [ ] Trigger non-repeatable reads
- [ ] Observe phantom reads
- [ ] Test FOR UPDATE locking
- **Guide:** `isolation_levels_manual_tests.sql`

### Phase 5: Practice Problems (90 minutes)
- [ ] Solve 12 practice problems
- [ ] Implement solutions in Python
- [ ] Test with PostgreSQL
- [ ] Understand trade-offs
- **Guide:** `Theory/Contention-Practice-Problems.md`

---

## 🚀 30-Second Setup

```powershell
# 1. Install PostgreSQL
winget install PostgreSQL.PostgreSQL

# 2. Create database
psql -U postgres -c "CREATE DATABASE contention_lab;"

# 3. Install Python driver
pip install psycopg2-binary

# 4. Run first demo
python postgres_race_condition.py
```

---

## 📚 Files Created

### Theory & Concepts
- **3-Contention.md** — Complete theory guide with examples
- **Contention-Practice-Problems.md** — 12 real-world problems with solutions

### Hands-On Scripts
- **postgres_race_condition.py** — Demo unsafe operations + fixes
- **postgres_isolation_levels.py** — Test different isolation levels
- **postgres_deadlocks_advisory_locks.py** — Deadlock scenarios + solutions
- **isolation_levels_manual_tests.sql** — Manual SQL tests with psql

### Setup Guides
- **POSTGRES_SETUP_WINDOWS.md** — Detailed Windows installation
- **QUICK_START.md** — This file!

---

## 🔑 Key Concepts Map

```
CONTENTION
├── Race Conditions
│   ├── Read-Modify-Write problem
│   ├── Lost updates
│   └── Solutions: Locking, CAS, Transactions
│
├── Isolation Levels (Weakest → Strongest)
│   ├── READ UNCOMMITTED (dirty reads possible)
│   ├── READ COMMITTED (default, non-repeatable reads possible)
│   ├── REPEATABLE READ (phantom reads possible in some DBs)
│   └── SERIALIZABLE (safest, slowest)
│
├── MVCC (Multi-Version Concurrency Control)
│   ├── PostgreSQL default mechanism
│   ├── Each txn sees consistent snapshot
│   ├── No read locks needed
│   └── Writers get exclusive locks only
│
├── Pessimistic Locking
│   ├── Lock immediately before access
│   ├── FOR UPDATE clause
│   ├── Blocks concurrent access
│   └── Prevents race conditions
│
├── Optimistic Locking
│   ├── Use version numbers
│   ├── Check version at commit
│   ├── Retry on conflict
│   └── Higher concurrency, lower throughput
│
└── Distributed Locking
    ├── PostgreSQL advisory locks
    ├── Redis SETNX
    ├── Zookeeper/etcd
    └── Cross-service coordination
```

---

## 💡 Quick Decision Guide

When should you use what?

| Scenario | Solution | Why |
|----------|----------|-----|
| High-frequency counter increments | `UPDATE SET col = col + 1` | Atomic at SQL level |
| Bank transfers between accounts | Pessimistic + ordered locks | Prevent deadlocks, ensure consistency |
| Product inventory decrement | Conditional update + version | Prevent overselling |
| User profile updates | Optimistic with version | High concurrency, rare conflicts |
| Critical consistency | SERIALIZABLE isolation | Safety > performance |
| Multi-row aggregates | REPEATABLE READ + manual locks | Consistent snapshot |
| Cross-service coordination | Distributed locks (Redis) | Language/DB agnostic |
| Real-time counting | Cache + eventual consistency | Accept slight staleness |

---

## 🧪 Expected Experiment Results

### Experiment 1: Race Condition
```
Without locking (unsafe):
  Initial balance: $1000
  After 10x $10 transfers: $950-$990 (LOST MONEY!)

With pessimistic locking (safe):
  After 10x $10 transfers: $900 ✓

With optimistic locking (safe):
  After 10x $10 transfers: $900 ✓
```

### Experiment 2: Isolation Levels
```
READ COMMITTED:
  T1: Read → $1000
  T2: Update → $2000
  T1: Read again → $2000 (non-repeatable!)

REPEATABLE READ:
  T1: Read → $1000
  T2: Update → $2000
  T1: Read again → $1000 (repeatable!) ✓
```

### Experiment 3: Deadlock
```
Circular locks (deadlock):
  T1: Lock A → Lock B → BLOCKED
  T2: Lock B → Lock A → BLOCKED
  PostgreSQL: DEADLOCK ERROR!

Ordered locks (safe):
  T1: Lock min(A,B) → Lock max(A,B) → SUCCESS
  T2: Lock min(A,B) → waits → Lock max(A,B) → SUCCESS ✓
```

---

## 📖 Recommended Reading Order

1. **Start:** POSTGRES_SETUP_WINDOWS.md (get PostgreSQL running)
2. **Learn:** Theory/3-Contention.md Parts 1-2 (understand concepts)
3. **Code:** Examples in Theory/3-Contention.md Part 3 (see patterns)
4. **Run:** postgres_race_condition.py (observe problems)
5. **Test:** postgres_isolation_levels.py (test isolation levels)
6. **Debug:** postgres_deadlocks_advisory_locks.py (see deadlock handling)
7. **Practice:** Theory/Contention-Practice-Problems.md (solve problems)
8. **Explore:** isolation_levels_manual_tests.sql (manual testing)

---

## 🎯 Learning Outcomes

After completing this guide, you'll understand:

✅ What race conditions are and how they occur
✅ All PostgreSQL isolation levels and when to use them
✅ How MVCC works and why PostgreSQL doesn't need read locks
✅ Difference between pessimistic and optimistic locking
✅ How to prevent deadlocks with ordered lock acquisition
✅ When to use distributed locks (Redis, advisory locks)
✅ How to implement retry logic for transient failures
✅ How to monitor and debug lock contention
✅ Real-world patterns for inventory, banking, reservations
✅ Trade-offs between safety, performance, and complexity

---

## 🚨 Common Mistakes to Avoid

1. ❌ **Forgetting to lock both rows in transfers**
   - ✅ Always use `SELECT ... FOR UPDATE` for both accounts

2. ❌ **Locking rows in inconsistent order**
   - ✅ Always lock by ID order: `sorted([id1, id2])`

3. ❌ **Mixing READ COMMITTED with critical operations**
   - ✅ Use REPEATABLE READ or SERIALIZABLE for consistency

4. ❌ **Forgetting version checks in optimistic locking**
   - ✅ Always compare version at commit time

5. ❌ **Not releasing locks in exception handlers**
   - ✅ Use try-finally or context managers

6. ❌ **Assuming single-row updates are atomic**
   - ✅ They are, but multi-row operations need transactions

7. ❌ **Setting timeouts too short**
   - ✅ Account for network latency + processing

8. ❌ **Not handling deadlock retries**
   - ✅ Implement exponential backoff retry logic

---

## 💻 How to Run Demos

### Python Scripts
```powershell
# Each script has DB_CONFIG at top - UPDATE THE PASSWORD!
# Then:

# Demo 1: Race conditions
python postgres_race_condition.py

# Demo 2: Isolation levels  
python postgres_isolation_levels.py

# Demo 3: Deadlocks & advisory locks
python postgres_deadlocks_advisory_locks.py
```

### SQL Scripts
```powershell
# Open psql
psql -U postgres -d contention_lab

# Run commands from isolation_levels_manual_tests.sql manually
# Open 2 terminals and follow the comments for multi-terminal demos
```

---

## 🔍 Monitoring Commands

Watch what's happening in PostgreSQL:

```sql
-- Active connections
SELECT pid, usename, application_name, state, query
FROM pg_stat_activity WHERE state != 'idle';

-- Lock info
SELECT * FROM pg_locks WHERE NOT granted;

-- Waiting info
SELECT blocked_locks.pid, blocking_locks.pid
FROM pg_locks blocked_locks
JOIN pg_locks blocking_locks ON ...;
```

---

## 📞 Getting Help

Each file has:
- **Comments** explaining what's happening
- **Examples** you can modify
- **Expected output** to compare against

If stuck:
1. Check the relevant theory section in `3-Contention.md`
2. Read the comments in the Python scripts
3. Try the manual SQL tests to understand isolation
4. Review the practice problems for similar scenarios

---

## Next Steps After Learning

1. **Apply to your projects:** Use pessimistic locking for critical transfers
2. **Add monitoring:** Track lock wait times in production
3. **Test edge cases:** Deliberately trigger deadlocks to verify handling
4. **Optimize gradually:** Start safe (SERIALIZABLE), optimize where needed
5. **Document:** Add comments on why you chose specific isolation levels

Good luck! 🚀
