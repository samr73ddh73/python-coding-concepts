# Python Conventions for LLD (Low-Level Design)

## What Changed and Why

### 1. Method Naming: camelCase → snake_case

**Before (Java style):**
```python
def isExpired(self):
def getCode(self):
def markOccupied(self):
```

**After (Python style - PEP 8):**
```python
def is_expired(self) -> bool:
def get_code(self) -> str:
def mark_occupied(self) -> None:
```

✅ Python convention is `snake_case` for methods and variables  
✅ More readable in Python ecosystem  
✅ Consistent with standard library (`str.is_digit()`, `dict.get_value()`)

---

### 2. Type Hints - Added Throughout

**Before:**
```python
def __init__(self, code, expiry, compartment):
```

**After:**
```python
def __init__(self, code: str, expiry: datetime, compartment: Compartment) -> None:
```

✅ Makes code self-documenting  
✅ IDE can provide better autocomplete  
✅ Enables static type checking with mypy  
✅ Helps catch bugs early

---

### 3. Imports - Proper Organization

**Before:**
```python
class AccessToken:
    def isExpired(self):
        currentTime = Date.now()  # ❌ Date doesn't exist
```

**After:**
```python
from datetime import datetime

def is_expired(self) -> bool:
    return datetime.now() > self.expiry  # ✅ Correct
```

---

### 4. Docstrings - Added for Clarity

**Before:**
```python
def book(self, packageSize: Size):
    if packageSize != self.size:
        return False
```

**After:**
```python
def book(self, package_size: Size) -> bool:
    """
    Book the compartment for a package

    Args:
        package_size: Size of the package to store

    Returns:
        True if booking successful, False otherwise
    """
    if not self.can_fit_package(package_size):
        return False
    if self.status != LockerStatus.AVAILABLE:
        return False
    self.status = LockerStatus.RESERVED
    return True
```

✅ Explains what, why, and how  
✅ Shows arguments and return values  
✅ IDE displays docstrings on hover

---

### 5. Logic Fixes

#### Compartment.book() - Was incomplete

**Before:**
```python
def book(self, packageSize: Size):
    if packageSize != self.size:
        return False
    # Missing: return True! ❌
```

**After:**
```python
def book(self, package_size: Size) -> bool:
    if not self.can_fit_package(package_size):
        return False
    if self.status != LockerStatus.AVAILABLE:
        return False
    self.status = LockerStatus.RESERVED
    return True
```

---

#### AccessToken.isExpired() - Was incorrect

**Before:**
```python
def isExpired(self):
    currentTime = Date.now()  # ❌ Date is Java, not Python
    if self.expiry < currentTime:
        return True
    return False
```

**After:**
```python
def is_expired(self) -> bool:
    return datetime.now() > self.expiry  # ✅ Correct + concise
```

---

### 6. Variable Naming: camelCase → snake_case

**Before:**
```python
currentTime = Date.now()
packageSize = Size.SMALL
compartmentByID = {}
```

**After:**
```python
current_time = datetime.now()
package_size = Size.SMALL
compartment_by_id = {}
```

✅ Consistent with Python style  
✅ More readable

---

## Key Python Conventions (PEP 8)

### Naming Standards

| Item | Convention | Example |
|------|-----------|---------|
| Classes | PascalCase | `class AccessToken` |
| Methods | snake_case | `def is_expired(self)` |
| Variables | snake_case | `access_code = "ABC123"` |
| Constants | UPPER_CASE | `MAX_RETRIES = 3` |
| Private methods | _leading_underscore | `def _validate()` |
| Protected methods | _leading_underscore | `def _internal_setup()` |

### Type Hints

```python
# Function arguments and return type
def deliver_package(self, package_size: Size) -> Optional[AccessToken]:
    pass

# Variable type hints
compartments: List[Compartment] = []
status_count: Dict[str, int] = {}

# With Optional
token: Optional[AccessToken] = None
```

### Docstring Format

```python
def book(self, package_size: Size) -> bool:
    """One-line summary.

    Longer description if needed. Explain what this does
    and why someone would use it.

    Args:
        package_size: Description of argument

    Returns:
        Description of return value

    Raises:
        ValueError: When something is invalid
    """
    pass
```

---

## Complete Example: Before vs After

### BEFORE (Java-style):
```python
class Compartment:
    def __init__(self, size):
        self.size = size
        self.status = LockerStatus.AVAILABLE
    
    def book(self, packageSize):
        if packageSize != self.size:
            return False
        # ❌ Missing return True!

    def getStatus(self):
        return self.status
    
    def markOccupied(self):
        self.status = LockerStatus.OCCUPIED
```

### AFTER (Pythonic):
```python
class Compartment:
    """A single compartment in a locker"""

    def __init__(self, size: Size):
        """
        Args:
            size: Size of the compartment
        """
        self.size = size
        self.status = LockerStatus.AVAILABLE

    def can_fit_package(self, package_size: Size) -> bool:
        """Check if package size matches compartment size"""
        return package_size == self.size

    def book(self, package_size: Size) -> bool:
        """Book the compartment for a package.
        
        Args:
            package_size: Size of the package to store

        Returns:
            True if booking successful, False otherwise
        """
        if not self.can_fit_package(package_size):
            return False
        if self.status != LockerStatus.AVAILABLE:
            return False
        self.status = LockerStatus.RESERVED
        return True

    def get_status(self) -> LockerStatus:
        """Get compartment status"""
        return self.status

    def mark_occupied(self) -> None:
        """Mark compartment as occupied (package inside)"""
        self.status = LockerStatus.OCCUPIED
```

---

## Why These Changes Matter

### 1. **Readability**
- Python developers expect `snake_case` methods
- Takes less time to understand code
- Reduces cognitive load

### 2. **Type Safety**
- Type hints catch errors at IDE time, not runtime
- Better IDE autocomplete
- Easier to refactor with confidence

### 3. **Consistency**
- All Python code follows PEP 8
- Easier to collaborate with other Python developers
- Matches standard library style

### 4. **Correctness**
- Fixed logical bugs (missing return statements)
- Used actual Python datetime, not Java Date
- Proper enum values

### 5. **Maintainability**
- Docstrings help future developers
- Clear what each function expects and returns
- Easier to debug and extend

---

## Quick Reference Checklist

When writing Python LLD code:

- [ ] Methods use `snake_case` (not `camelCase`)
- [ ] Variables use `snake_case` (not `camelCase`)
- [ ] Add type hints to all function arguments and returns
- [ ] Write docstrings for public methods
- [ ] Import from standard library correctly (`datetime`, not `Date`)
- [ ] Use `Optional[T]` for nullable types
- [ ] Use `List[T]`, `Dict[K, V]` for collections
- [ ] Return `None` explicitly (not `return` alone)
- [ ] Use `is` and `is not` for None checks
- [ ] Use list comprehensions for filtering

---

## Running the Code

```bash
# Run the demo
python Locker.py

# Expected output:
# Locker created: Locker(id=LOC-001, compartments=10, available=10)
# Status: {'AVAILABLE': 10}
# 
# Delivering packages:
#   Package 1 (SMALL): ABC123
#   Package 2 (LARGE): DEF456
# 
# Status after delivery: {'AVAILABLE': 8, 'OCCUPIED': 2}
# Pickup packages:
#   Pickup 1: Success
#   Pickup 2: Success
# 
# Final status: {'AVAILABLE': 10}
```

---

## References

- [PEP 8 - Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)
- [PEP 257 - Docstring Conventions](https://www.python.org/dev/peps/pep-0257/)
- [Type Hints - Python Docs](https://docs.python.org/3/library/typing.html)
