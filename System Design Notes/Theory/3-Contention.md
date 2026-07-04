I need to learn postgres concepts of MVCC
Isolation levels
Types of locking

how to handle contention etc. 




# Database Contention & Isolation Levels - PostgreSQL Hands-On Guide

## Part 1: Installation & Setup

### Windows PostgreSQL Installation

1. **Download PostgreSQL 15/16**
   - Visit: https://www.postgresql.org/download/windows/
   - Download PostgreSQL installer
   - Run installer, set password for `postgres` user (remember this!)
   - Choose port 5432 (default)
   - Install pgAdmin4 (optional, GUI tool)

2. **Add PostgreSQL to PATH**
   ```powershell
   # Open PowerShell as Admin
   $env:Path += ";C:\Program Files\PostgreSQL\16\bin"
   ```

3. **Verify Installation**
   ```powershell
   psql --version
   psql -U postgres -h localhost
   # Enter password when prompted
   ```

4. **Create Test Database**
   ```sql
   CREATE DATABASE contention_lab;
   \c contention_lab
   CREATE TABLE accounts (
       id SERIAL PRIMARY KEY,
       name VARCHAR(100),
       balance DECIMAL(10, 2),
       version INT DEFAULT 0
   );
   INSERT INTO accounts (name, balance) VALUES ('Alice', 1000.00);
   INSERT INTO accounts (name, balance) VALUES ('Bob', 1000.00);
   ```

---

## Part 2: Core Concepts

### 1. RACE CONDITIONS
**Problem:** Two transactions modify the same data simultaneously, losing updates.

```
T1: Read balance = $100
T2: Read balance = $100
T1: Writes balance = $90 (T1 deducts $10)
T2: Writes balance = $95 (T2 deducts $5)
Result: Lost $10 from T1's update!
```

### 2. POSTGRESQL ISOLATION LEVELS (Strongest to Weakest)

| Level | Dirty Read | Non-Repeatable Read | Phantom Read | Lost Update |
|-------|-----------|-------------------|--------------|-------------|
| **SERIALIZABLE** | ❌ | ❌ | ❌ | ❌ |
| **REPEATABLE READ** | ❌ | ❌ | ❌* | ❌ |
| **READ COMMITTED** | ❌ | ⚠️ | ⚠️ | ⚠️ |
| **READ UNCOMMITTED** | ⚠️ | ⚠️ | ⚠️ | ⚠️ |

*PostgreSQL REPEATABLE READ prevents phantoms via MVCC

### 3. LOCKING MECHANISMS

**Pessimistic Locking:**
- Lock row before reading/writing
- Prevents other txns from accessing
- Blocks other transactions
- Safe but slower (deadlock risk)

**Optimistic Locking:**
- Use version numbers
- No locks during transaction
- Detect conflicts at commit
- Faster, allows more concurrency

**MVCC (Multi-Version Concurrency Control):**
- PostgreSQL default
- Each txn sees snapshot of data
- No read locks needed
- Writers get exclusive locks on rows

### 4. DISTRIBUTED LOCKING
- For cross-database coordination
- Use advisory locks: `pg_advisory_lock(key)`
- Redis SETNX for distributed systems
- Explicit lock management needed

---

## Part 3: Hands-On Examples

### Example 1: Race Condition (READ COMMITTED - UNSAFE)
```python
import psycopg2
import threading
import time

conn_params = {
    'dbname': 'contention_lab',
    'user': 'postgres',
    'password': 'your_password',
    'host': 'localhost'
}

def transfer_unsafe(account_id, amount):
    """Without explicit locking - RACE CONDITION"""
    conn = psycopg2.connect(**conn_params)
    cur = conn.cursor()
    
    cur.execute("SELECT balance FROM accounts WHERE id = %s", (account_id,))
    balance = cur.fetchone()[0]
    time.sleep(0.1)  # Simulate network delay
    
    new_balance = balance - amount
    cur.execute("UPDATE accounts SET balance = %s WHERE id = %s", 
                (new_balance, account_id))
    conn.commit()
    cur.close()
    conn.close()

# Run 10 concurrent transfers of $10 each (should end at $900)
threads = []
for i in range(10):
    t = threading.Thread(target=transfer_unsafe, args=(1, 10))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

# Check balance - will be > $900 due to lost updates!
conn = psycopg2.connect(**conn_params)
cur = conn.cursor()
cur.execute("SELECT balance FROM accounts WHERE id = 1")
print(f"Balance after 10x$10 transfers: ${cur.fetchone()[0]}")  # Expected: $900
cur.close()
conn.close()
```

### Example 2: Pessimistic Locking (SAFE)
```python
def transfer_pessimistic(account_id, amount):
    """Lock row before reading - SAFE"""
    conn = psycopg2.connect(**conn_params)
    cur = conn.cursor()
    
    # Lock row immediately
    cur.execute("BEGIN")
    cur.execute("SELECT balance FROM accounts WHERE id = %s FOR UPDATE", 
                (account_id,))
    balance = cur.fetchone()[0]
    time.sleep(0.1)  # Simulate delay
    
    new_balance = balance - amount
    cur.execute("UPDATE accounts SET balance = %s WHERE id = %s", 
                (new_balance, account_id))
    conn.commit()
    cur.close()
    conn.close()
```

### Example 3: Optimistic Locking (VERSION COLUMN)
```python
def transfer_optimistic(account_id, amount):
    """Use version number to detect conflicts"""
    conn = psycopg2.connect(**conn_params)
    cur = conn.cursor()
    
    while True:
        cur.execute("SELECT balance, version FROM accounts WHERE id = %s", 
                    (account_id,))
        balance, version = cur.fetchone()
        time.sleep(0.1)  # Simulate delay
        
        new_balance = balance - amount
        
        # Only update if version hasn't changed
        cur.execute("""UPDATE accounts 
                      SET balance = %s, version = version + 1 
                      WHERE id = %s AND version = %s""", 
                    (new_balance, account_id, version))
        conn.commit()
        
        if cur.rowcount > 0:
            break  # Success!
        print(f"Conflict detected, retrying...")
        
    cur.close()
    conn.close()
```

### Example 4: ISOLATION LEVELS - Non-Repeatable Read
```python
# Terminal 1:
psql -U postgres -d contention_lab
BEGIN ISOLATION LEVEL READ COMMITTED;
SELECT balance FROM accounts WHERE id = 1;  -- Read $1000

# Terminal 2 (while T1 is open):
UPDATE accounts SET balance = 500 WHERE id = 1;
COMMIT;

# Back to Terminal 1:
SELECT balance FROM accounts WHERE id = 1;  -- Reads $500 (non-repeatable!)
COMMIT;
```

### Example 5: REPEATABLE READ (Fixes Non-Repeatable Reads)
```python
# Terminal 1:
BEGIN ISOLATION LEVEL REPEATABLE READ;
SELECT balance FROM accounts WHERE id = 1;  -- Snapshot at T1 start

# Terminal 2:
UPDATE accounts SET balance = 500 WHERE id = 1;
COMMIT;

# Back to Terminal 1:
SELECT balance FROM accounts WHERE id = 1;  -- Still $1000 (repeatable!)
COMMIT;
```

### Example 6: Distributed Advisory Lock
```python
def transfer_with_distributed_lock(account_id, amount):
    """Use PostgreSQL advisory locks for coordination"""
    conn = psycopg2.connect(**conn_params)
    cur = conn.cursor()
    
    # Acquire advisory lock (function takes any 64-bit ID)
    cur.execute("SELECT pg_advisory_lock(%s)", (account_id,))
    
    try:
        cur.execute("SELECT balance FROM accounts WHERE id = %s", (account_id,))
        balance = cur.fetchone()[0]
        time.sleep(0.1)
        
        new_balance = balance - amount
        cur.execute("UPDATE accounts SET balance = %s WHERE id = %s", 
                    (new_balance, account_id))
        conn.commit()
    finally:
        # Release advisory lock
        cur.execute("SELECT pg_advisory_unlock(%s)", (account_id,))
        conn.commit()
    
    cur.close()
    conn.close()
```

### Example 7: Detect & Handle Deadlocks
```python
def transfer_with_deadlock_handling(account_id, amount, max_retries=3):
    """Handle deadlocks gracefully"""
    from psycopg2 import OperationalError
    
    for attempt in range(max_retries):
        try:
            conn = psycopg2.connect(**conn_params)
            cur = conn.cursor()
            
            cur.execute("SELECT balance FROM accounts WHERE id = %s FOR UPDATE", 
                        (account_id,))
            balance = cur.fetchone()[0]
            time.sleep(0.1)
            
            cur.execute("UPDATE accounts SET balance = %s WHERE id = %s", 
                        (balance - amount, account_id))
            conn.commit()
            cur.close()
            conn.close()
            return True
        except OperationalError as e:
            if 'deadlock' in str(e).lower():
                print(f"Deadlock detected, retry {attempt + 1}/{max_retries}")
                time.sleep(0.1 * (attempt + 1))
            else:
                raise
    return False
```

---

## Part 4: MVCC Demonstration

```sql
-- Terminal 1:
BEGIN;
SELECT * FROM accounts WHERE id = 1;  -- Sees snapshot

-- Terminal 2:
UPDATE accounts SET balance = 250 WHERE id = 1;
COMMIT;

-- Terminal 1 (still in same transaction):
SELECT * FROM accounts WHERE id = 1;  -- Still sees old value (MVCC!)
COMMIT;
```

---

## Part 5: Practical Problems

### Problem 1: Bank Transfer Race Condition
**Scenario:** Transfer $100 from Account A → Account B
```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
```
**Issue:** If T1 fails after first update, money disappears!
**Solution:** Use explicit transactions with proper isolation

### Problem 2: Lost Update in Concurrent Edits
**Scenario:** Two users edit same profile name simultaneously
**Solutions:**
1. Optimistic: Add `version` column, detect at commit
2. Pessimistic: `SELECT FOR UPDATE` before read
3. Last-write-wins: Accept concurrent updates (weakest)

### Problem 3: Phantom Reads
**Scenario:** Count rows → Insert row → Count again, different results
**Solution:** Use `SERIALIZABLE` isolation level

### Problem 4: Deadlock Between Circular Locks
**Scenario:** T1 locks A then B, T2 locks B then A
**Solution:** Always acquire locks in same order (consistent ordering)

### Problem 5: Distributed Locking Across Services
**Scenario:** Multiple microservices accessing same DB row
**Solutions:**
1. PostgreSQL advisory locks
2. Redis SETNX with TTL
3. Consensus (Zookeeper, etcd)

---

## Quick Reference: Choosing Your Locking Strategy

| Scenario | Best Strategy | Why |
|----------|---------------|-----|
| High concurrency reads, rare writes | MVCC + REPEATABLE READ | Fast reads, no locks |
| Critical financial transactions | Pessimistic + SERIALIZABLE | Safety over speed |
| Low contention, frequent conflicts | Optimistic + version | Detect conflicts early |
| Distributed systems | Advisory locks + Redis | Cross-service coordination |
| High contention, strict ordering | Pessimistic + explicit locks | Prevent deadlocks |

---

## Testing Your Understanding

1. ✅ Create race condition scenario (Example 1)
2. ✅ Fix with pessimistic locking (Example 2)
3. ✅ Fix with optimistic locking (Example 3)
4. ✅ Test READ COMMITTED vs REPEATABLE READ
5. ✅ Trigger and resolve a deadlock
6. ✅ Implement distributed lock with advisory locks

