# Contention Practice Problems

## Problem 1: Bank Account Transfer Race Condition

**Scenario:**
```
Two customers simultaneously withdraw from same account
T1: Withdraw $50 from Account A (balance $100)
T2: Withdraw $30 from Account A (balance $100)
Without locking: Final balance could be $100, $50, or $70
```

**Problem:**
Write a concurrent system that demonstrates this race condition, then fix it.

**Solution Approach:**
```python
# UNSAFE - Race condition
def withdraw(account_id, amount):
    balance = get_balance(account_id)
    time.sleep(0.1)  # Simulate processing
    set_balance(account_id, balance - amount)

# SAFE - Option 1: Pessimistic locking
def withdraw_pessimistic(account_id, amount):
    conn.execute("SELECT balance FROM accounts WHERE id = ? FOR UPDATE", (account_id,))
    balance = get_balance(account_id)
    set_balance(account_id, balance - amount)

# SAFE - Option 2: Optimistic locking (version column)
def withdraw_optimistic(account_id, amount):
    balance, version = get_balance_and_version(account_id)
    success = update_if_version_matches(account_id, balance - amount, version)
    if not success:
        retry_withdraw(account_id, amount)
```

**Key Concepts:**
- Race conditions
- Read-Modify-Write atomicity
- Pessimistic vs optimistic locking

---

## Problem 2: Lost Update in Inventory Management

**Scenario:**
```
Product has 10 units in stock
Simultaneously:
  Order 1 checks stock (10) and orders 8 units
  Order 2 checks stock (10) and orders 5 units
Result: Both succeed, inventory goes to -3 units!
```

**Problem:**
How would you prevent overselling inventory with concurrent orders?

**Solution:**
1. **Pessimistic:** Lock row before checking
   ```sql
   SELECT stock FROM products WHERE id = ? FOR UPDATE
   IF stock >= order_qty THEN UPDATE
   ```

2. **Optimistic:** Use CAS (Compare-and-Swap)
   ```sql
   UPDATE products SET stock = stock - ?
   WHERE id = ? AND stock >= ?
   ```

3. **Distributed:** Use distributed counter with atomic operations

---

## Problem 3: Phantom Read in Analytics

**Scenario:**
```
Transaction 1: Count total products
SELECT COUNT(*) FROM products → 100

Meanwhile...
Transaction 2: Insert new product
INSERT INTO products VALUES (...)

Transaction 1: Count again
SELECT COUNT(*) FROM products → 101 (phantom read!)
```

**Problem:**
Why is this problematic? How to fix?

**Solution:**
- Use SERIALIZABLE isolation level
- This ensures phantom reads don't occur
- Trade-off: Lower throughput

```sql
BEGIN ISOLATION LEVEL SERIALIZABLE;
SELECT COUNT(*) FROM products;
-- ... do more reads/writes ...
COMMIT;  -- Atomic with respect to other transactions
```

---

## Problem 4: Deadlock in Multi-Account Transfer

**Scenario:**
```
Thread 1: Transfer from Account A → Account B
  Lock Account A
  Wait for Account B lock
  (blocked by Thread 2)

Thread 2: Transfer from Account B → Account A
  Lock Account B
  Wait for Account A lock
  (blocked by Thread 1)

DEADLOCK! Both waiting indefinitely
```

**Problem:**
Design a deadlock-free transfer system.

**Solutions:**

1. **Ordered Locking:** Always lock in consistent order
   ```python
   accounts = sorted([from_id, to_id])
   lock(accounts[0])
   lock(accounts[1])
   # Transfer
   unlock(accounts[1])
   unlock(accounts[0])
   ```

2. **Timeout & Retry:**
   ```python
   try:
       transfer_with_timeout(from_id, to_id, timeout=1)
   except DeadlockError:
       sleep(random(0.1, 1.0))
       retry_transfer(from_id, to_id)
   ```

3. **Single Lock per Transfer:**
   ```python
   lock(min(from_id, to_id))  # Consistent order
   # Access both accounts while holding one lock
   ```

---

## Problem 5: Double-Booking in Reservation System

**Scenario:**
```
Hotel has 1 room available
Guest 1: Check availability → 1 room
Guest 2: Check availability → 1 room
Guest 1: Book room → Success
Guest 2: Book room → Success (should fail!)
```

**Problem:**
Implement a reservation system that prevents double-booking.

**Solution:**

```python
def reserve_room_optimistic(room_id, guest_id, version):
    """Version-based optimistic locking"""
    success = db.execute("""
        UPDATE rooms 
        SET booked_by = ?, version = version + 1
        WHERE id = ? AND version = ? AND booked_by IS NULL
    """, (guest_id, room_id, version))
    
    if success.rows_affected == 0:
        raise ReservationConflict("Room unavailable or version mismatch")

def reserve_room_pessimistic(room_id, guest_id):
    """Row lock before checking"""
    with db.transaction():
        row = db.execute("""
            SELECT * FROM rooms 
            WHERE id = ? FOR UPDATE
        """, (room_id,))
        
        if row.booked_by is None:
            db.execute("""
                UPDATE rooms SET booked_by = ? WHERE id = ?
            """, (guest_id, room_id))
            return True
        return False
```

---

## Problem 6: Write Skew - Concurrent Modifications

**Scenario:**
```
Doctor availability tracking
Doctor on call with minimum 2 required at hospital

Session 1: Check count (2 doctors on call)
Session 2: Check count (2 doctors on call)
Session 1: Remove self → count becomes 1
Session 2: Remove self → count becomes 0 (VIOLATION!)
```

**Problem:**
Constraint violated even though both sessions saw it was satisfied.

**Solution:**
- Use SERIALIZABLE isolation
- Explicit constraint checks with pessimistic locks
- Append-only ledger for immutable audit trail

```sql
-- SERIALIZABLE prevents write skew
BEGIN ISOLATION LEVEL SERIALIZABLE;
SELECT COUNT(*) FROM doctors_on_call WHERE available = true;
-- Must be >= 2

-- Then can safely do update
UPDATE doctors_on_call SET available = false WHERE id = ?;
COMMIT;
```

---

## Problem 7: MVCC & Snapshot Consistency

**Scenario:**
```
Account totals consistency check:
  All accounts should sum to exactly $10,000
  
T1: Read account A (sees $3000)
T2: Transfer $1000 from A to B
T1: Read account B (sees $2000 after transfer)
T1: Read account C...
T1: Total = $5000 (inconsistent!)
```

**Problem:**
How to ensure consistent reads across multiple rows?

**Solution:**

```python
# Read entire dataset in one transaction (snapshot)
def get_consistent_account_totals():
    with db.transaction(isolation=REPEATABLE_READ):
        accounts = db.query("""
            SELECT * FROM accounts
            ORDER BY id
        """)
        # All reads see same snapshot, total will be consistent
        total = sum(a.balance for a in accounts)
        return total

# Or use explicit lock if writing
def transfer_consistent(from_id, to_id, amount):
    with db.transaction(isolation=SERIALIZABLE):
        from_acc = db.query(
            "SELECT * FROM accounts WHERE id = ? FOR UPDATE",
            (from_id,)
        )
        to_acc = db.query(
            "SELECT * FROM accounts WHERE id = ? FOR UPDATE",
            (to_id,)
        )
        
        if from_acc.balance >= amount:
            db.execute(
                "UPDATE accounts SET balance = balance - ? WHERE id = ?",
                (amount, from_id)
            )
            db.execute(
                "UPDATE accounts SET balance = balance + ? WHERE id = ?",
                (amount, to_id)
            )
```

---

## Problem 8: Distributed Locking Across Services

**Scenario:**
```
Microservice architecture:
- Service A: User microservice
- Service B: Order microservice
Both need to coordinate on resource

Service A: Lock user for update
Service B: Also needs to lock same user
Challenge: How to synchronize across services?
```

**Solution:**

```python
# Option 1: Distributed lock in shared database
def lock_user_distributed(user_id, service_id):
    """Use PostgreSQL advisory lock"""
    db.execute("SELECT pg_advisory_lock(?)", (user_id,))
    try:
        # Critical section
        update_user(user_id)
    finally:
        db.execute("SELECT pg_advisory_unlock(?)", (user_id,))

# Option 2: Distributed lock with Redis
def lock_user_redis(user_id, service_id):
    """SETNX for distributed locking"""
    lock_key = f"user:{user_id}:lock"
    lock_id = uuid4()
    
    # Try to acquire lock (30s timeout)
    acquired = redis.set(
        lock_key,
        lock_id,
        nx=True,  # Only set if not exists
        ex=30     # Expire after 30s
    )
    
    if acquired:
        try:
            update_user(user_id)
        finally:
            # Only release if still ours
            if redis.get(lock_key) == lock_id:
                redis.delete(lock_key)
    else:
        raise LockNotAcquired()

# Option 3: Consensus with etcd/Zookeeper
# More complex but handles network partitions
```

---

## Problem 9: Lost Update with Concurrent Incrementing

**Scenario:**
```
Page view counter
Initial: views = 1000
T1: Read 1000 → Increment → Write 1001
T2: Read 1000 → Increment → Write 1001
Final: 1001 (should be 1002!)
```

**Problem:**
Fix the counter without explicit locks.

**Solutions:**

```python
# WRONG - Race condition
def increment_counter():
    count = get_counter()
    set_counter(count + 1)

# Solution 1: Atomic increment
db.execute("UPDATE counters SET count = count + 1 WHERE id = ?")

# Solution 2: Version-based retry
def increment_counter_optimistic(max_retries=3):
    for attempt in range(max_retries):
        count, version = get_counter_and_version()
        success = db.execute(
            "UPDATE counters SET count = ?, version = version + 1 WHERE id = ? AND version = ?",
            (count + 1, counter_id, version)
        )
        if success:
            return
        # Retry

# Solution 3: Lock-free with MVCC
db.execute("UPDATE counters SET count = count + 1 WHERE id = ?")
# PostgreSQL handles serialization automatically
```

---

## Problem 10: Phantom Update During Range Scan

**Scenario:**
```
Monthly billing report on accounts balance > $1000

T1: SELECT * FROM accounts WHERE balance > 1000
    → Sees 5 accounts, total = $6000

Meanwhile...
T2: INSERT INTO accounts (balance) VALUES (1500)

T1: Calculates billing
    → Phantom row was inserted!
    → Lost revenue from new account
```

**Problem:**
How to ensure range queries are stable?

**Solution:**

```python
def calculate_billing_consistent():
    """SERIALIZABLE prevents phantoms"""
    with db.transaction(isolation=SERIALIZABLE):
        accounts = db.query("""
            SELECT * FROM accounts 
            WHERE balance > 1000
            ORDER BY id
        """)
        
        total = 0
        for account in accounts:
            billing = account.balance * 0.1
            total += billing
        
        # Record billing
        db.execute("""
            INSERT INTO billing_records (month, total)
            VALUES (?, ?)
        """, (current_month(), total))

# Without SERIALIZABLE, new rows could appear
# With SERIALIZABLE, transaction sees snapshot before T1
```

---

## Problem 11: Consistency Check Under Load

**Scenario:**
```
Constraint: sum(account_a) + sum(account_b) == system_total

Concurrent transfers within each type:
  Can final state violate constraint?
```

**Solution:**

```python
def maintain_consistency():
    """Two-phase commit or SERIALIZABLE"""
    with db.transaction(isolation=SERIALIZABLE):
        total_a = db.query("SELECT SUM(balance) FROM accounts WHERE type = 'A'")[0]
        total_b = db.query("SELECT SUM(balance) FROM accounts WHERE type = 'B'")[0]
        
        assert total_a + total_b == expected_total, "Constraint violated!"
        
        # Safe to update
        transfer_between_accounts()

# SERIALIZABLE ensures atomicity with constraint check
```

---

## Problem 12: Monitoring & Debugging Contentio

**Task:** Build monitoring for contention

```python
def monitor_lock_contention():
    """Track lock wait times"""
    stats = db.query("""
        SELECT
            COUNT(*) as blocked_txns,
            MAX(EXTRACT(EPOCH FROM (now() - query_start))) as longest_wait_s
        FROM pg_stat_activity
        WHERE waiting = true
    """)
    return stats

def detect_deadlocks():
    """Alert on deadlock patterns"""
    stats = db.query("""
        SELECT
            query,
            COUNT(*) as deadlock_count
        FROM pg_stat_statements
        WHERE query LIKE '%UPDATE%'
        GROUP BY query
        HAVING COUNT(*) > 100
    """)
    # Alert if deadlock_count is high
```

---

## Summary: Choosing the Right Strategy

| Problem | Best Solution |
|---------|---------------|
| High-frequency increments | Atomic SQL: `UPDATE SET col = col + 1` |
| Account transfers | Ordered pessimistic locking |
| Inventory management | CAS updates with constraints |
| Analytics consistency | SERIALIZABLE isolation |
| Cross-service coordination | Distributed locks (Redis/Consul) |
| Real-time updates | Optimistic locking with version |
| Double-booking prevention | Pessimistic lock before insert |
| Constraint checking | SERIALIZABLE + explicit check |

