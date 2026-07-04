-- PostgreSQL Isolation Levels Manual Testing
-- Run these commands in separate psql sessions to see isolation behavior

-- ============================================================
-- SETUP: Create test tables
-- ============================================================

CREATE TABLE IF NOT EXISTS isolation_test (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    value INT
);

INSERT INTO isolation_test (name, value) VALUES ('Counter', 0);

-- ============================================================
-- TEST 1: READ COMMITTED - Non-Repeatable Read
-- ============================================================
-- Window A: Reader at READ COMMITTED
-- Window B: Writer
-- Shows how same query returns different results

-- WINDOW A - Start here first:
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
BEGIN;
SELECT value FROM isolation_test WHERE id = 1;  -- Read 0

-- WINDOW B - Run while A is waiting:
UPDATE isolation_test SET value = 100 WHERE id = 1;
COMMIT;

-- WINDOW A - Back to reader, uncomment next:
-- SELECT value FROM isolation_test WHERE id = 1;  -- Reads 100 (non-repeatable!)
-- COMMIT;


-- ============================================================
-- TEST 2: REPEATABLE READ - Snapshot Isolation
-- ============================================================
-- Window A: Reader at REPEATABLE READ
-- Window B: Writer
-- Reader should see consistent snapshot

-- WINDOW A - Start here first:
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
BEGIN;
SELECT value FROM isolation_test WHERE id = 1;  -- Reads 100

-- WINDOW B - Run while A is waiting:
UPDATE isolation_test SET value = 200 WHERE id = 1;
COMMIT;

-- WINDOW A - Back to reader:
-- SELECT value FROM isolation_test WHERE id = 1;  -- Still reads 100 (repeatable!)
-- COMMIT;


-- ============================================================
-- TEST 3: Phantom Read Detection
-- ============================================================

-- WINDOW A - Start here:
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
BEGIN;
SELECT COUNT(*) FROM isolation_test;  -- Count rows

-- WINDOW B - Insert while A is running:
INSERT INTO isolation_test (name, value) VALUES ('Phantom', 999);
COMMIT;

-- WINDOW A - Back to reader:
-- SELECT COUNT(*) FROM isolation_test;  -- Counts phantom (one more row)
-- COMMIT;


-- ============================================================
-- TEST 4: Dirty Reads (READ UNCOMMITTED in other DBs)
-- Note: PostgreSQL doesn't allow true dirty reads, minimal issue
-- ============================================================

-- WINDOW A - Start here:
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
BEGIN;
SELECT value FROM isolation_test WHERE id = 1;

-- WINDOW B - Update and rollback:
BEGIN;
UPDATE isolation_test SET value = 9999 WHERE id = 1;
-- (don't commit, just update)

-- WINDOW A - Still won't see uncommitted change in PostgreSQL
-- SELECT value FROM isolation_test WHERE id = 1;
-- COMMIT;


-- ============================================================
-- TEST 5: Lost Update Problem
-- ============================================================

-- WINDOW A & B both do this with READ COMMITTED:
-- This is the classic lost update scenario

-- Both windows - Window A first:
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
BEGIN;
SELECT value FROM isolation_test WHERE id = 1;
-- Get value X

-- Window B - Do same:
-- ... B also gets value X

-- Window A - Modify:
UPDATE isolation_test SET value = X + 10 WHERE id = 1;
COMMIT;

-- Window B - Modify (overwrites A's change):
UPDATE isolation_test SET value = X + 5 WHERE id = 1;
COMMIT;

-- Result: A's update lost! Final value is X+5 instead of both updates applied


-- ============================================================
-- TEST 6: Serialization Anomaly (SERIALIZABLE)
-- ============================================================

-- Create table for this test:
CREATE TABLE IF NOT EXISTS accounts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    balance DECIMAL(10, 2)
);

INSERT INTO accounts (name, balance) VALUES ('Account1', 100.00);
INSERT INTO accounts (name, balance) VALUES ('Account2', 100.00);

-- WINDOW A - Read total balance:
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
BEGIN;
SELECT SUM(balance) FROM accounts;  -- Should be 200

-- WINDOW B - Transfer between accounts:
BEGIN;
UPDATE accounts SET balance = balance - 10 WHERE id = 1;
UPDATE accounts SET balance = balance + 10 WHERE id = 2;
COMMIT;

-- WINDOW A - Check again:
-- SELECT SUM(balance) FROM accounts;  -- Should still be 200
-- COMMIT;

-- SERIALIZABLE ensures consistency even with concurrent changes


-- ============================================================
-- TEST 7: Row-Level Locking with FOR UPDATE
-- ============================================================

-- WINDOW A - Lock row:
BEGIN;
SELECT value FROM isolation_test WHERE id = 1 FOR UPDATE;

-- WINDOW B - Try to update (will block):
BEGIN;
UPDATE isolation_test SET value = 500 WHERE id = 1;
-- This will block until Window A releases lock

-- WINDOW A - Release lock:
-- COMMIT;

-- WINDOW B - Now succeeds:
-- (after A commits)


-- ============================================================
-- TEST 8: Deadlock Scenario
-- ============================================================

-- Create two rows:
INSERT INTO isolation_test (name, value) VALUES ('Row1', 1);
INSERT INTO isolation_test (name, value) VALUES ('Row2', 2);

-- WINDOW A - Lock row 1 then row 2:
BEGIN;
SELECT * FROM isolation_test WHERE id = 4 FOR UPDATE;  -- Lock row 1
-- Then try to lock row 2 (next)

-- WINDOW B - Lock row 2 then row 1:
BEGIN;
SELECT * FROM isolation_test WHERE id = 5 FOR UPDATE;  -- Lock row 2
-- Then try to lock row 1 (next)

-- This will deadlock! PostgreSQL will kill one transaction.


-- ============================================================
-- TEST 9: Advisory Locks for Cross-Session Coordination
-- ============================================================

-- WINDOW A - Acquire lock:
SELECT pg_advisory_lock(123456);  -- Acquire lock
-- Do work here
SELECT pg_advisory_unlock(123456);  -- Release

-- WINDOW B - Try to acquire same lock (will block):
-- SELECT pg_advisory_lock(123456);  -- Blocks until A releases


-- ============================================================
-- TEST 10: View Lock Info
-- ============================================================

-- See active locks in system:
SELECT pid, usename, application_name, state, query
FROM pg_stat_activity
WHERE state != 'idle';

-- See blocking relationships:
SELECT
    blocked_locks.pid AS blocked_pid,
    blocked_activity.usename AS blocked_user,
    blocking_locks.pid AS blocking_pid,
    blocking_activity.usename AS blocking_user,
    blocked_activity.query AS blocked_statement,
    blocking_activity.query AS blocking_statement
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks ON blocking_locks.locktype = blocked_locks.locktype
    AND blocking_locks.database IS NOT DISTINCT FROM blocked_locks.database
    AND blocking_locks.relation IS NOT DISTINCT FROM blocked_locks.relation
    AND blocking_locks.page IS NOT DISTINCT FROM blocked_locks.page
    AND blocking_locks.tuple IS NOT DISTINCT FROM blocked_locks.tuple
    AND blocking_locks.virtualxid IS NOT DISTINCT FROM blocked_locks.virtualxid
    AND blocking_locks.transactionid IS NOT DISTINCT FROM blocked_locks.transactionid
    AND blocking_locks.classid IS NOT DISTINCT FROM blocked_locks.classid
    AND blocking_locks.objid IS NOT DISTINCT FROM blocked_locks.objid
    AND blocking_locks.objsubid IS NOT DISTINCT FROM blocked_locks.objsubid
    AND blocking_locks.pid != blocked_locks.pid
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;


-- ============================================================
-- Cleanup
-- ============================================================

DROP TABLE IF EXISTS isolation_test CASCADE;
DROP TABLE IF EXISTS accounts CASCADE;
