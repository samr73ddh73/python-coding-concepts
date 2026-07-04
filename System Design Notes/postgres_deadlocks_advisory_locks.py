"""
PostgreSQL Deadlocks & Advisory Locks Demo
"""

import psycopg2
import threading
import time
from psycopg2 import OperationalError

DB_CONFIG = {
    'dbname': 'contention_lab',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost'
}

def init_transfer_table():
    """Create accounts table for deadlock demo"""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    try:
        cur.execute("DROP TABLE IF EXISTS bank_accounts CASCADE")
    except:
        pass

    cur.execute("""
    CREATE TABLE bank_accounts (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        balance DECIMAL(10, 2)
    )
    """)

    cur.execute("INSERT INTO bank_accounts (name, balance) VALUES ('Account A', 1000.00)")
    cur.execute("INSERT INTO bank_accounts (name, balance) VALUES ('Account B', 1000.00)")

    conn.commit()
    cur.close()
    conn.close()
    print("✓ Transfer table initialized")

def demo_deadlock_circular_locks():
    """
    Deadlock Demo: Circular lock dependencies
    T1: Lock A → Lock B
    T2: Lock B → Lock A
    Result: DEADLOCK
    """
    print("\n" + "="*60)
    print("DEMO: Circular Locks → DEADLOCK")
    print("="*60)

    results = {'t1_status': None, 't2_status': None}
    lock = threading.Lock()

    def transfer_a_to_b():
        """T1: Transfer from A to B"""
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cur = conn.cursor()

            print("[T1] BEGIN - Will lock A, then B")
            cur.execute("BEGIN")

            print("[T1] Locking Account A (FOR UPDATE)...")
            cur.execute("SELECT balance FROM bank_accounts WHERE id = 1 FOR UPDATE")
            print("[T1] ✓ Locked A")

            time.sleep(1)  # Wait for T2 to lock B

            print("[T1] Trying to lock Account B...")
            cur.execute("SELECT balance FROM bank_accounts WHERE id = 2 FOR UPDATE")
            print("[T1] ✓ Locked B (this shouldn't happen due to deadlock)")

            # If we get here, no deadlock
            cur.execute("UPDATE bank_accounts SET balance = balance - 100 WHERE id = 1")
            cur.execute("UPDATE bank_accounts SET balance = balance + 100 WHERE id = 2")
            cur.execute("COMMIT")
            print("[T1] ✓ Committed")

            with lock:
                results['t1_status'] = 'SUCCESS'

        except OperationalError as e:
            if 'deadlock' in str(e).lower():
                print(f"[T1] ✗ DEADLOCK DETECTED: {str(e)[:50]}...")
                with lock:
                    results['t1_status'] = 'DEADLOCK'
            else:
                print(f"[T1] ✗ Other error: {e}")
                with lock:
                    results['t1_status'] = 'ERROR'
        finally:
            try:
                cur.close()
                conn.close()
            except:
                pass

    def transfer_b_to_a():
        """T2: Transfer from B to A (opposite order)"""
        try:
            time.sleep(0.5)  # Let T1 start first
            conn = psycopg2.connect(**DB_CONFIG)
            cur = conn.cursor()

            print("[T2] BEGIN - Will lock B, then A")
            cur.execute("BEGIN")

            print("[T2] Locking Account B (FOR UPDATE)...")
            cur.execute("SELECT balance FROM bank_accounts WHERE id = 2 FOR UPDATE")
            print("[T2] ✓ Locked B")

            print("[T2] Trying to lock Account A...")
            cur.execute("SELECT balance FROM bank_accounts WHERE id = 1 FOR UPDATE")
            print("[T2] ✓ Locked A (this shouldn't happen due to deadlock)")

            cur.execute("UPDATE bank_accounts SET balance = balance - 50 WHERE id = 2")
            cur.execute("UPDATE bank_accounts SET balance = balance + 50 WHERE id = 1")
            cur.execute("COMMIT")
            print("[T2] ✓ Committed")

            with lock:
                results['t2_status'] = 'SUCCESS'

        except OperationalError as e:
            if 'deadlock' in str(e).lower():
                print(f"[T2] ✗ DEADLOCK DETECTED: {str(e)[:50]}...")
                with lock:
                    results['t2_status'] = 'DEADLOCK'
            else:
                print(f"[T2] ✗ Other error: {e}")
                with lock:
                    results['t2_status'] = 'ERROR'
        finally:
            try:
                cur.close()
                conn.close()
            except:
                pass

    init_transfer_table()

    t1 = threading.Thread(target=transfer_a_to_b, name="T1")
    t2 = threading.Thread(target=transfer_b_to_a, name="T2")

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    print(f"\nResults:")
    print(f"  T1: {results['t1_status']}")
    print(f"  T2: {results['t2_status']}")

def fix_deadlock_ordered_locks():
    """
    Deadlock Fix: Always acquire locks in same order
    Both T1 and T2 lock A before B
    """
    print("\n" + "="*60)
    print("FIX: Ordered Lock Acquisition (NO DEADLOCK)")
    print("="*60)

    results = {'t1_status': None, 't2_status': None}
    lock = threading.Lock()

    def transfer_ordered(from_id, to_id, amount):
        """Acquire locks in consistent order (lower ID first)"""
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cur = conn.cursor()

            thread_name = threading.current_thread().name
            print(f"[{thread_name}] BEGIN")
            cur.execute("BEGIN")

            # Always lock in order: min ID first
            lock_order = sorted([from_id, to_id])
            print(f"[{thread_name}] Locking accounts {lock_order[0]}, {lock_order[1]} (ordered)")

            for acc_id in lock_order:
                cur.execute("SELECT balance FROM bank_accounts WHERE id = %s FOR UPDATE",
                           (acc_id,))

            print(f"[{thread_name}] ✓ All locks acquired")

            time.sleep(0.2)  # Simulate processing

            cur.execute("UPDATE bank_accounts SET balance = balance - %s WHERE id = %s",
                       (amount, from_id))
            cur.execute("UPDATE bank_accounts SET balance = balance + %s WHERE id = %s",
                       (amount, to_id))
            cur.execute("COMMIT")
            print(f"[{thread_name}] ✓ Committed")

            with lock:
                results[thread_name] = 'SUCCESS'

        except OperationalError as e:
            print(f"[{thread_name}] ✗ Error: {e}")
            with lock:
                results[thread_name] = 'ERROR'
        finally:
            try:
                cur.close()
                conn.close()
            except:
                pass

    init_transfer_table()

    t1 = threading.Thread(
        target=transfer_ordered,
        args=(1, 2, 100),
        name="T1-A→B"
    )
    t2 = threading.Thread(
        target=transfer_ordered,
        args=(2, 1, 50),
        name="T2-B→A"
    )

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    print(f"\nResults:")
    for name, status in results.items():
        print(f"  {name}: {status}")

def demo_advisory_locks():
    """
    Advisory Locks: Explicit application-level locks
    Useful for cross-service coordination
    """
    print("\n" + "="*60)
    print("DEMO: PostgreSQL Advisory Locks")
    print("="*60)

    results = {'t1': None, 't2': None}
    lock = threading.Lock()

    def process_with_advisory_lock(lock_id, thread_name):
        """Acquire advisory lock, do work, release"""
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cur = conn.cursor()

            print(f"[{thread_name}] Acquiring advisory lock({lock_id})...")
            cur.execute("SELECT pg_advisory_lock(%s)", (lock_id,))
            print(f"[{thread_name}] ✓ Lock acquired")

            time.sleep(1)  # Critical section

            print(f"[{thread_name}] Doing work in critical section...")

            cur.execute("SELECT pg_advisory_unlock(%s)", (lock_id,))
            print(f"[{thread_name}] ✓ Lock released")

            conn.commit()
            cur.close()
            conn.close()

            with lock:
                results[thread_name] = 'SUCCESS'

        except Exception as e:
            print(f"[{thread_name}] ✗ Error: {e}")
            with lock:
                results[thread_name] = 'ERROR'

    t1 = threading.Thread(
        target=process_with_advisory_lock,
        args=(12345, "T1"),
        name="T1"
    )
    t2 = threading.Thread(
        target=process_with_advisory_lock,
        args=(12345, "T2"),
        name="T2"
    )

    print("Starting two threads, both trying to acquire same advisory lock...")
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    print(f"\nResults:")
    for name, status in results.items():
        print(f"  {name}: {status}")
    print("\nNote: One thread had to wait for the other (serialized)")

def handle_deadlock_with_retry():
    """
    Deadlock Handling: Detect and retry with backoff
    """
    print("\n" + "="*60)
    print("DEMO: Deadlock Detection & Retry")
    print("="*60)

    def transfer_with_retry(from_id, to_id, amount, max_retries=3):
        """Retry on deadlock with exponential backoff"""
        for attempt in range(max_retries):
            try:
                conn = psycopg2.connect(**DB_CONFIG)
                cur = conn.cursor()

                cur.execute("BEGIN")
                cur.execute("SELECT balance FROM bank_accounts WHERE id = %s FOR UPDATE",
                           (from_id,))
                cur.execute("SELECT balance FROM bank_accounts WHERE id = %s FOR UPDATE",
                           (to_id,))

                time.sleep(0.1)

                cur.execute("UPDATE bank_accounts SET balance = balance - %s WHERE id = %s",
                           (amount, from_id))
                cur.execute("UPDATE bank_accounts SET balance = balance + %s WHERE id = %s",
                           (amount, to_id))
                cur.execute("COMMIT")

                print(f"✓ Transfer successful on attempt {attempt + 1}")
                cur.close()
                conn.close()
                return True

            except OperationalError as e:
                if 'deadlock' in str(e).lower():
                    wait_time = 0.1 * (2 ** attempt)  # Exponential backoff
                    print(f"✗ Deadlock on attempt {attempt + 1}, waiting {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    print(f"✗ Non-deadlock error: {e}")
                    return False
            finally:
                try:
                    cur.close()
                    conn.close()
                except:
                    pass

        print(f"✗ Failed after {max_retries} attempts")
        return False

    init_transfer_table()
    print("Running transfer with deadlock retry logic...")
    transfer_with_retry(1, 2, 100)

if __name__ == "__main__":
    print("PostgreSQL Deadlocks & Advisory Locks Demo\n")

    try:
        # Demo 1: Show deadlock problem
        print("[1] Demonstrating Deadlock Problem")
        demo_deadlock_circular_locks()

        # Demo 2: Show how to fix it
        print("\n[2] Fixed: Ordered Lock Acquisition")
        fix_deadlock_ordered_locks()

        # Demo 3: Advisory locks
        print("\n[3] Advisory Locks for Explicit Coordination")
        demo_advisory_locks()

        # Demo 4: Deadlock handling
        print("\n[4] Deadlock Handling with Retry")
        handle_deadlock_with_retry()

    except psycopg2.Error as e:
        print(f"\n✗ Database error: {e}")
        print("\nSetup:")
        print("  1. psql -U postgres -c 'CREATE DATABASE contention_lab'")
        print("  2. Update DB_CONFIG password in this script")
