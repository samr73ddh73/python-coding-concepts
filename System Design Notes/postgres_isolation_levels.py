"""
PostgreSQL Isolation Levels Demo
Demonstrates: Dirty Reads, Non-Repeatable Reads, Phantom Reads
Run with 2 terminal windows for full effect
"""

import psycopg2
import time
import threading

DB_CONFIG = {
    'dbname': 'contention_lab',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost'
}

def init_demo_table():
    """Create test table"""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    try:
        cur.execute("DROP TABLE IF EXISTS products CASCADE")
    except:
        pass

    cur.execute("""
    CREATE TABLE products (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        price DECIMAL(10, 2),
        stock INT
    )
    """)

    cur.execute("INSERT INTO products (name, price, stock) VALUES ('Laptop', 999.99, 5)")
    cur.execute("INSERT INTO products (name, price, stock) VALUES ('Mouse', 25.00, 100)")
    cur.execute("INSERT INTO products (name, price, stock) VALUES ('Keyboard', 75.00, 50)")

    conn.commit()
    cur.close()
    conn.close()
    print("✓ Demo table initialized")

def demo_non_repeatable_read():
    """
    Non-Repeatable Read Demo
    Same query returns different results within same transaction
    """
    print("\n" + "="*60)
    print("DEMO: Non-Repeatable Read (READ COMMITTED)")
    print("="*60)
    print("""
Instructions:
1. Terminal 1: Run this function (client 1)
2. Terminal 2: Run demo_write_for_nonrepeat() (writer)
3. Watch Terminal 1 see different values

Expected:
  READ COMMITTED: Second SELECT sees updated value
  REPEATABLE READ: Both SELECTs see same value (snapshot)
    """)

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    print("\n[Client 1] Starting transaction with READ COMMITTED...")
    cur.execute("SET TRANSACTION ISOLATION LEVEL READ COMMITTED")
    cur.execute("BEGIN")

    print("[Client 1] First SELECT at T1:")
    cur.execute("SELECT price FROM products WHERE id = 1")
    price1 = cur.fetchone()[0]
    print(f"  Price: ${price1}")

    print("[Client 1] Waiting for Client 2 to update...")
    time.sleep(3)

    print("[Client 1] Second SELECT at T3 (after update):")
    cur.execute("SELECT price FROM products WHERE id = 1")
    price2 = cur.fetchone()[0]
    print(f"  Price: ${price2}")

    if price1 != price2:
        print(f"✗ Non-Repeatable Read: Price changed from ${price1} → ${price2}")
    else:
        print(f"✓ Repeatable Read: Price stayed ${price1}")

    cur.execute("COMMIT")
    cur.close()
    conn.close()

def demo_write_for_nonrepeat():
    """Writer for non-repeatable read demo"""
    time.sleep(1.5)  # Wait for reader to start
    print("\n[Client 2] Updating price...")
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("UPDATE products SET price = 1299.99 WHERE id = 1")
    conn.commit()
    print("[Client 2] Update committed!")

    cur.close()
    conn.close()

def demo_phantom_read():
    """
    Phantom Read Demo
    New rows appear/disappear in result set within same transaction
    """
    print("\n" + "="*60)
    print("DEMO: Phantom Read (READ COMMITTED)")
    print("="*60)
    print("""
Instructions:
1. Terminal 1: Run this function
2. Terminal 2: Run demo_insert_for_phantom()
3. Watch count increase

Expected:
  READ COMMITTED: Second COUNT sees new row
  SERIALIZABLE: Both COUNTs see same count
    """)

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    print("\n[Client 1] Starting transaction with READ COMMITTED...")
    cur.execute("SET TRANSACTION ISOLATION LEVEL READ COMMITTED")
    cur.execute("BEGIN")

    print("[Client 1] First COUNT at T1:")
    cur.execute("SELECT COUNT(*) FROM products")
    count1 = cur.fetchone()[0]
    print(f"  Count: {count1} rows")

    print("[Client 1] Waiting for Client 2 to insert...")
    time.sleep(3)

    print("[Client 1] Second COUNT at T3 (after insert):")
    cur.execute("SELECT COUNT(*) FROM products")
    count2 = cur.fetchone()[0]
    print(f"  Count: {count2} rows")

    if count1 != count2:
        print(f"✗ Phantom Read: Count changed {count1} → {count2}")
    else:
        print(f"✓ No Phantom: Count stayed {count1}")

    cur.execute("COMMIT")
    cur.close()
    conn.close()

def demo_insert_for_phantom():
    """Writer for phantom read demo"""
    time.sleep(1.5)  # Wait for reader to start
    print("\n[Client 2] Inserting new product...")
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("INSERT INTO products (name, price, stock) VALUES ('Monitor', 299.99, 20)")
    conn.commit()
    print("[Client 2] Insert committed!")

    cur.close()
    conn.close()

def demo_repeatable_read_vs_read_committed():
    """Side-by-side comparison"""
    print("\n" + "="*60)
    print("COMPARISON: REPEATABLE READ vs READ COMMITTED")
    print("="*60)

    conn_read_committed = psycopg2.connect(**DB_CONFIG)
    conn_repeatable = psycopg2.connect(**DB_CONFIG)

    cur_rc = conn_read_committed.cursor()
    cur_rr = conn_repeatable.cursor()

    # Start transactions
    cur_rc.execute("SET TRANSACTION ISOLATION LEVEL READ COMMITTED")
    cur_rc.execute("BEGIN")
    cur_rr.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ")
    cur_rr.execute("BEGIN")

    # Both read same data
    cur_rc.execute("SELECT price FROM products WHERE id = 2")
    cur_rr.execute("SELECT price FROM products WHERE id = 2")
    price_rc_1 = cur_rc.fetchone()[0]
    price_rr_1 = cur_rr.fetchone()[0]

    print(f"\nT1 - Initial read (both see $25):")
    print(f"  READ COMMITTED: ${price_rc_1}")
    print(f"  REPEATABLE READ: ${price_rr_1}")

    # Update from outside
    conn_update = psycopg2.connect(**DB_CONFIG)
    cur_update = conn_update.cursor()
    cur_update.execute("UPDATE products SET price = 35.00 WHERE id = 2")
    conn_update.commit()
    cur_update.close()
    conn_update.close()
    print("\nT2 - External UPDATE committed (price → $35)")

    # Read again in both transactions
    cur_rc.execute("SELECT price FROM products WHERE id = 2")
    cur_rr.execute("SELECT price FROM products WHERE id = 2")
    price_rc_2 = cur_rc.fetchone()[0]
    price_rr_2 = cur_rr.fetchone()[0]

    print(f"\nT3 - Second read:")
    print(f"  READ COMMITTED: ${price_rc_2} (saw update!)")
    print(f"  REPEATABLE READ: ${price_rr_2} (still sees snapshot)")

    cur_rc.execute("COMMIT")
    cur_rr.execute("COMMIT")
    cur_rc.close()
    cur_rr.close()
    conn_read_committed.close()
    conn_repeatable.close()

def interactive_demo():
    """Manual isolation level testing"""
    print("\n" + "="*60)
    print("INTERACTIVE: Manual Isolation Testing")
    print("="*60)
    print("""
For maximum control, use psql directly:

Terminal 1 (Reader):
  psql -U postgres -d contention_lab
  SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
  BEGIN;
  SELECT price FROM products WHERE id = 1;

Terminal 2 (Writer):
  psql -U postgres -d contention_lab
  UPDATE products SET price = 1500.00 WHERE id = 1;
  COMMIT;

Terminal 1 (Back to reader):
  SELECT price FROM products WHERE id = 1;
  COMMIT;

Compare results with REPEATABLE READ instead!
    """)

if __name__ == "__main__":
    print("PostgreSQL Isolation Levels Demo")

    try:
        init_demo_table()

        # Single-threaded demos
        print("\n[1] Running READ COMMITTED vs REPEATABLE READ comparison...")
        demo_repeatable_read_vs_read_committed()

        # Interactive instructions
        print("\n[2] For interactive testing...")
        interactive_demo()

        # For two-terminal demos, uncomment:
        # print("\n[1] Non-Repeatable Read Demo")
        # thread1 = threading.Thread(target=demo_non_repeatable_read)
        # thread2 = threading.Thread(target=demo_write_for_nonrepeat)
        # thread1.start()
        # thread2.start()
        # thread1.join()
        # thread2.join()

    except psycopg2.Error as e:
        print(f"\n✗ Error: {e}")
        print("\nMake sure:")
        print("  1. PostgreSQL is running")
        print("  2. Database 'contention_lab' exists")
        print("  3. Update DB_CONFIG with correct credentials")
