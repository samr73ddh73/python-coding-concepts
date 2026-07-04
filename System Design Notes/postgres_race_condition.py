"""
PostgreSQL Race Condition Demo
Run this to see unsafe concurrent updates (READ COMMITTED level)
"""

import psycopg2
import threading
import time
from typing import Dict

# Connection parameters - UPDATE THESE!
DB_CONFIG = {
    'dbname': 'contention_lab',
    'user': 'postgres',
    'password': 'postgres',  # Change to your password
    'host': 'localhost',
    'port': 5432
}

def init_db():
    """Create test table and reset data"""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    try:
        cur.execute("DROP TABLE IF EXISTS accounts CASCADE")
    except:
        pass

    cur.execute("""
    CREATE TABLE accounts (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        balance DECIMAL(10, 2),
        version INT DEFAULT 0
    )
    """)

    cur.execute("INSERT INTO accounts (name, balance) VALUES ('Alice', 1000.00)")
    cur.execute("INSERT INTO accounts (name, balance) VALUES ('Bob', 1500.00)")

    conn.commit()
    cur.close()
    conn.close()
    print("✓ Database initialized")

def get_balance(account_id: int) -> float:
    """Get current balance"""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT balance FROM accounts WHERE id = %s", (account_id,))
    balance = cur.fetchone()[0]
    cur.close()
    conn.close()
    return float(balance)

def transfer_unsafe(account_id: int, amount: float, delay: float = 0.05):
    """
    UNSAFE: Race condition demo
    Two concurrent transfers can lose money
    """
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # Read-Modify-Write without locking
    cur.execute("SET TRANSACTION ISOLATION LEVEL READ COMMITTED")
    cur.execute("SELECT balance FROM accounts WHERE id = %s", (account_id,))
    balance = cur.fetchone()[0]

    time.sleep(delay)  # Simulate processing delay

    new_balance = float(balance) - amount
    cur.execute("UPDATE accounts SET balance = %s WHERE id = %s",
                (new_balance, account_id))

    conn.commit()
    cur.close()
    conn.close()

def transfer_pessimistic(account_id: int, amount: float, delay: float = 0.05):
    """
    SAFE: Lock row before reading
    FOR UPDATE prevents other transactions from accessing
    """
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("BEGIN")
    cur.execute("SET TRANSACTION ISOLATION LEVEL READ COMMITTED")

    # Lock row immediately with FOR UPDATE
    cur.execute("SELECT balance FROM accounts WHERE id = %s FOR UPDATE",
                (account_id,))
    balance = cur.fetchone()[0]

    time.sleep(delay)  # Simulate processing delay

    new_balance = float(balance) - amount
    cur.execute("UPDATE accounts SET balance = %s WHERE id = %s",
                (new_balance, account_id))

    conn.commit()
    cur.close()
    conn.close()

def transfer_optimistic(account_id: int, amount: float, delay: float = 0.05, max_retries: int = 3):
    """
    SAFE: Use version column to detect conflicts
    Retry on conflict
    """
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    for attempt in range(max_retries):
        cur.execute("BEGIN")
        cur.execute("SET TRANSACTION ISOLATION LEVEL READ COMMITTED")

        # Read balance and version
        cur.execute("SELECT balance, version FROM accounts WHERE id = %s",
                    (account_id,))
        result = cur.fetchone()
        if result is None:
            conn.rollback()
            return False

        balance, version = result

        time.sleep(delay)  # Simulate processing delay

        new_balance = float(balance) - amount

        # Only update if version hasn't changed
        cur.execute("""
            UPDATE accounts
            SET balance = %s, version = version + 1
            WHERE id = %s AND version = %s
        """, (new_balance, account_id, version))

        conn.commit()

        if cur.rowcount > 0:
            cur.close()
            conn.close()
            return True  # Success!

        conn.rollback()
        print(f"  Version conflict on attempt {attempt + 1}, retrying...")

    cur.close()
    conn.close()
    return False

def run_test(method_name: str, transfer_func, num_transfers: int = 10, amount: float = 10):
    """Run concurrent transfers and check result"""
    print(f"\n{'='*60}")
    print(f"Testing: {method_name}")
    print(f"{'='*60}")

    init_db()
    initial = get_balance(1)
    print(f"Initial balance: ${initial}")

    # Run concurrent transfers
    threads = []
    start_time = time.time()

    for i in range(num_transfers):
        t = threading.Thread(
            target=transfer_func,
            args=(1, amount),
            name=f"Transfer-{i}"
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    elapsed = time.time() - start_time

    # Check result
    final = get_balance(1)
    expected = initial - (num_transfers * amount)
    error = final - expected

    print(f"\nAfter {num_transfers} transfers of ${amount} each:")
    print(f"  Expected:     ${expected:.2f}")
    print(f"  Actual:       ${final:.2f}")
    print(f"  Error:        ${error:.2f}")
    print(f"  Time elapsed: {elapsed:.3f}s")

    if abs(error) < 0.01:
        print(f"  ✓ SAFE - No lost updates")
    else:
        print(f"  ✗ UNSAFE - Lost ${-error:.2f}!")

    return final, expected, error

if __name__ == "__main__":
    print("PostgreSQL Race Condition & Locking Demo")
    print("Make sure 'contention_lab' database exists!")

    try:
        # Test 1: Unsafe (Race Condition)
        print("\n[TEST 1] UNSAFE - Race Condition (READ COMMITTED)")
        run_test(
            "Unsafe Read-Modify-Write",
            transfer_unsafe,
            num_transfers=10,
            amount=10
        )

        # Test 2: Pessimistic Locking
        print("\n[TEST 2] SAFE - Pessimistic Locking (FOR UPDATE)")
        run_test(
            "Pessimistic Locking",
            transfer_pessimistic,
            num_transfers=10,
            amount=10
        )

        # Test 3: Optimistic Locking
        print("\n[TEST 3] SAFE - Optimistic Locking (Version Column)")
        run_test(
            "Optimistic Locking",
            transfer_optimistic,
            num_transfers=10,
            amount=10
        )

        print("\n" + "="*60)
        print("Summary:")
        print("  Unsafe: Shows lost updates due to race conditions")
        print("  Pessimistic: Uses locks, slower but guaranteed safe")
        print("  Optimistic: Detects conflicts, retries if needed")

    except psycopg2.Error as e:
        print(f"\n✗ Database error: {e}")
        print("\nSetup:")
        print("  1. Install PostgreSQL: https://www.postgresql.org/download/windows/")
        print("  2. Create database: psql -U postgres -c 'CREATE DATABASE contention_lab'")
        print("  3. Update DB_CONFIG in this script with your password")
