# PostgreSQL Setup Guide for Windows

## Step 1: Download & Install PostgreSQL

### Option A: Official Installer (Recommended)
1. Visit: https://www.postgresql.org/download/windows/
2. Download **PostgreSQL 15 or 16**
3. Run installer:
   - Choose installation directory (default: `C:\Program Files\PostgreSQL\16`)
   - Username: `postgres`
   - **Password: IMPORTANT - Remember this!** (e.g., `postgres`)
   - Port: `5432` (default)
   - Locale: Leave as default
4. Finish installation

### Option B: Windows Package Manager
```powershell
winget install PostgreSQL.PostgreSQL
```

---

## Step 2: Verify Installation

Open **PowerShell** and test:

```powershell
# Check PostgreSQL version
psql --version
# Output: psql (PostgreSQL) 16.x

# Login to PostgreSQL
psql -U postgres -h localhost
# Enter password when prompted
# If successful, you'll see: postgres=#
```

---

## Step 3: Add PostgreSQL to PATH (Optional but Recommended)

Make PostgreSQL commands available globally:

```powershell
# Open PowerShell as Administrator

# Add to current session
$env:Path += ";C:\Program Files\PostgreSQL\16\bin"

# Make permanent (also as Admin):
[Environment]::SetEnvironmentVariable(
    "Path",
    $env:Path + ";C:\Program Files\PostgreSQL\16\bin",
    "User"
)
```

Verify:
```powershell
psql --version  # Should work from anywhere
```

---

## Step 4: Create Test Database

```powershell
# Login as postgres user
psql -U postgres -h localhost

# Or use this shortcut to run commands directly:
psql -U postgres -h localhost -c "CREATE DATABASE contention_lab;"
```

Inside psql:
```sql
-- Create the contention_lab database
CREATE DATABASE contention_lab;

-- List databases
\l

-- Connect to it
\c contention_lab

-- Create test table
CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    balance DECIMAL(10, 2),
    version INT DEFAULT 0
);

-- Insert sample data
INSERT INTO accounts (name, balance) VALUES ('Alice', 1000.00);
INSERT INTO accounts (name, balance) VALUES ('Bob', 1500.00);

-- Verify
SELECT * FROM accounts;

-- Exit
\q
```

---

## Step 5: Install Python PostgreSQL Driver

```powershell
# Install psycopg2 (PostgreSQL adapter for Python)
pip install psycopg2-binary

# Or with pip3
pip3 install psycopg2-binary
```

Verify:
```powershell
python -c "import psycopg2; print(psycopg2.__version__)"
```

---

## Step 6: Test Connection from Python

Create `test_postgres_connection.py`:

```python
import psycopg2

try:
    conn = psycopg2.connect(
        dbname="contention_lab",
        user="postgres",
        password="postgres",  # Change if you used different password
        host="localhost",
        port=5432
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM accounts")
    print("Connected! Accounts:")
    for row in cur.fetchall():
        print(row)
    cur.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
```

Run:
```powershell
python test_postgres_connection.py
```

Expected output:
```
Connected! Accounts:
(1, 'Alice', Decimal('1000.00'), 0)
(2, 'Bob', Decimal('1500.00'), 0)
```

---

## Step 7: Run the Learning Scripts

Update the `DB_CONFIG` in each script with your credentials:

```python
DB_CONFIG = {
    'dbname': 'contention_lab',
    'user': 'postgres',
    'password': 'postgres',  # YOUR PASSWORD HERE
    'host': 'localhost',
    'port': 5432
}
```

Then run:

```powershell
# Race condition demo
python postgres_race_condition.py

# Isolation levels demo
python postgres_isolation_levels.py

# Deadlocks and advisory locks
python postgres_deadlocks_advisory_locks.py
```

---

## Step 8: Manual Testing with psql

Create two PowerShell windows side-by-side:

**Window 1:** Transaction A
```powershell
psql -U postgres -d contention_lab

BEGIN;
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
SELECT * FROM accounts WHERE id = 1;
-- Keep window open, don't commit yet
```

**Window 2:** Transaction B
```powershell
psql -U postgres -d contention_lab

UPDATE accounts SET balance = 2000 WHERE id = 1;
COMMIT;
```

**Back to Window 1:**
```sql
SELECT * FROM accounts WHERE id = 1;  -- See change from B!
COMMIT;
```

---

## Troubleshooting

### "psql: command not found"
- PostgreSQL not in PATH
- **Fix:** Add to PATH (see Step 3) or restart PowerShell

### "psql: FATAL: Ident authentication failed"
- Username issue
- **Fix:** Use `-U postgres` explicitly

### "psql: ERROR: database does not exist"
- Database not created
- **Fix:** Run `psql -U postgres -c "CREATE DATABASE contention_lab;"`

### Connection refused (port 5432)
- PostgreSQL service not running
- **Fix:** Restart PostgreSQL service:
  ```powershell
  # As Administrator
  net start postgresql-x64-16  # Check actual service name
  # Or via Services app: Press Win+R → services.msc
  ```

### "password authentication failed"
- Wrong password
- **Fix:** 
  - Update `DB_CONFIG` in Python scripts
  - Or reset PostgreSQL password:
    ```powershell
    psql -U postgres -c "ALTER USER postgres PASSWORD 'newpassword';"
    ```

### "permission denied" on connecting
- PostgreSQL not accepting connections
- **Fix:** Check `pg_hba.conf`:
  ```
  C:\Program Files\PostgreSQL\16\data\pg_hba.conf
  
  Change:
    local   all      all     trust
    host    all      all     127.0.0.1/32   trust
  ```

---

## Useful PostgreSQL Commands

```powershell
# Login
psql -U postgres -h localhost -d contention_lab

# Run SQL file
psql -U postgres -d contention_lab -f script.sql

# Run single command
psql -U postgres -c "SELECT version();"

# Backup database
pg_dump -U postgres contention_lab > backup.sql

# Restore database
psql -U postgres -d contention_lab < backup.sql

# Monitor active connections
psql -U postgres -d contention_lab -c "SELECT * FROM pg_stat_activity;"
```

---

## Inside psql (Interactive)

```sql
\l              -- List databases
\c dbname       -- Connect to database
\d              -- List tables
\d tablename    -- Describe table
\q              -- Quit
\h              -- Help on SQL commands
SELECT version(); -- Check PostgreSQL version
```

---

## Setting Up pgAdmin (GUI - Optional)

pgAdmin was installed with PostgreSQL. To use it:

```powershell
# Launch pgAdmin (usually starts automatically)
# Or go to: C:\Program Files\PostgreSQL\16\pgAdmin 4\bin\pgAdmin4.exe
# Access at: http://localhost:5050
```

Create server:
1. **Name:** LocalPG
2. **Host:** localhost
3. **Port:** 5432
4. **Username:** postgres
5. **Password:** (your password)

---

## What's Next?

1. ✅ Run `postgres_race_condition.py` - See unsafe operations
2. ✅ Fix with pessimistic locking - See FOR UPDATE work
3. ✅ Test optimistic locking - See version columns work
4. ✅ Run isolation level demo - See REPEATABLE READ
5. ✅ Test deadlock scenario - See circular lock problem
6. ✅ Solve with ordered locks - See deadlock prevention
7. ✅ Work through practice problems

---

## Quick Reference: Configuration

```python
# Always update this in scripts:
DB_CONFIG = {
    'dbname': 'contention_lab',
    'user': 'postgres',
    'password': 'YOUR_PASSWORD',  # ← Change here
    'host': 'localhost',
    'port': 5432
}
```

---

## Next Steps

After setup, follow the learning path in `3-Contention.md`:
1. Learn core concepts (race conditions, isolation levels)
2. Run Python demos (race condition, optimistic/pessimistic locking)
3. Test isolation levels manually with psql
4. Trigger and resolve deadlocks
5. Implement distributed locks with advisory locks
6. Work through practice problems

