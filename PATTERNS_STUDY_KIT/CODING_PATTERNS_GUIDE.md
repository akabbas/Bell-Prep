# Bell Textron Coding Patterns Study Guide

**Purpose:** Master the 10 most common coding patterns you'll encounter at Bell Textron.

**Goal:** By recognizing these patterns, you'll understand 80% of the codebase without needing to memorize syntax.

---

## Table of Contents

1. [Pattern 1: Configuration Reading](#pattern-1-configuration-reading)
2. [Pattern 2: Validation](#pattern-2-validation)
3. [Pattern 3: Loop and Transform](#pattern-3-loop-and-transform)
4. [Pattern 4: Error Handling (Try/Except)](#pattern-4-error-handling)
5. [Pattern 5: Create/Configure/Return](#pattern-5-createconfigurereturn)
6. [Pattern 6: If/Else Conditional](#pattern-6-ifelse-conditional)
7. [Pattern 7: Dictionary/Object Access](#pattern-7-dictionaryobject-access)
8. [Pattern 8: String Formatting](#pattern-8-string-formatting)
9. [Pattern 9: List/Dict Comprehension](#pattern-9-listdict-comprehension)
10. [Pattern 10: Function with Return Value](#pattern-10-function-with-return-value)
11. [Study Plan](#study-plan)
12. [Practice Exercises](#practice-exercises)

---

## PATTERN 1: Configuration Reading

### What It Does
Reads settings from a configuration file or environment variables instead of hardcoding values.

### How to Recognize It
```python
config.get("SECTION", "KEY")
os.environ.get("VARIABLE_NAME")
settings["key"]
```

### Real Example from Your Code
```python
# Lines 71-72 in procurement_automation.py
log_level = config.get("DEFAULT", "LOG_LEVEL")
log_file = config.get(env.upper(), "LOG_FILE")
```

### Why It Matters
- **Flexibility:** Change behavior without changing code
- **Environments:** Different settings for dev/test/prod
- **Security:** Don't hardcode passwords or API keys
- **Bell-specific:** Can update procurement rules without redeployment

### Variations You'll See

**Reading from config file:**
```python
import configparser
config = configparser.ConfigParser()
config.read("config.ini")
value = config.get("PROD", "DATABASE_URL")
```

**Reading from environment variables:**
```python
import os
api_key = os.environ.get("API_KEY")
database_url = os.environ.get("DATABASE_URL")
```

**Reading from dictionary:**
```python
settings = {"timeout": 30, "retries": 3}
timeout = settings.get("timeout", 30)  # Default to 30 if not found
```

### When You'll Use This at Bell
- Getting database connections
- API keys and authentication
- Rate limiting values
- Log file locations
- Feature toggles (on/off)

### Study Tip
**Look for:** `config.get()`, `os.environ`, `.read()`, `.get()`

---

## PATTERN 2: Validation

### What It Does
Checks if data is valid before using it. If invalid, raises an error.

### How to Recognize It
```python
if not value:
    raise ValueError("Error message")

if len(value) != expected:
    raise ValueError("Error message")

if not value.isdigit():
    raise ValueError("Error message")
```

### Real Example from Your Code
```python
# Lines 517-568 in procurement_automation.py
def _validate_duns_number(self, duns: str) -> str:
    if not duns:
        raise ValueError("DUNS number cannot be empty")
    
    duns_clean = str(duns).replace("-", "").replace(" ", "").strip()
    
    if not duns_clean.isdigit():
        raise ValueError(f"DUNS number contains non-numeric characters: {duns}")
    
    if len(duns_clean) != 9:
        raise ValueError(f"DUNS number must be 9 digits, got {len(duns_clean)}")
    
    return duns_clean
```

### Why It Matters
- **Prevention:** Bad data doesn't enter the system
- **Debugging:** Know exactly where data failed
- **Bell-specific:** DUNS numbers MUST be valid (supplier identification)
- **Compliance:** Ensures data quality for ITAR/AS9100

### Common Validation Checks

```python
# Check if value exists
if not value:
    raise ValueError("Value cannot be empty")

# Check type
if not isinstance(value, str):
    raise ValueError("Value must be string")

# Check length
if len(value) != 9:
    raise ValueError("Must be 9 characters")

# Check range
if value < 0 or value > 100:
    raise ValueError("Must be between 0 and 100")

# Check format
if not value.isdigit():
    raise ValueError("Must be numeric")

# Check membership
if value not in allowed_values:
    raise ValueError("Not an allowed value")
```

### When You'll Use This at Bell
- Validating DUNS numbers
- Checking percentages (0-100%)
- Verifying ITAR flags (true/false)
- Validating supplier names
- Checking risk scores (1-5)

### Study Tip
**Look for:** `if not`, `if x >`, `if x <`, `raise ValueError`

---

## PATTERN 3: Loop and Transform

### What It Does
Iterates through a list of items, does something to each one, and collects results.

### How to Recognize It

**Version 1: Traditional Loop**
```python
results = []
for item in data:
    processed = do_something(item)
    results.append(processed)
return results
```

**Version 2: List Comprehension (shorter)**
```python
results = [do_something(item) for item in data]
return results
```

### Real Example from Your Code
```python
# Lines 387-419 in procurement_automation.py
cleaned = []
errors = []

for supplier_data in suppliers:
    try:
        cleaned_record = self._clean_record(supplier_data)
        cleaned.append(cleaned_record)
    except ValueError as e:
        errors.append({"supplier_id": ..., "error": str(e)})

return cleaned, errors
```

### Why It Matters
- **Common pattern:** Used constantly for data processing
- **Efficiency:** Process multiple items without repeating code
- **Bell-specific:** Clean 250+ suppliers at once
- **Maintainability:** Easy to understand what's happening

### Variations

**Simple transformation:**
```python
supplier_names = [s.name for s in suppliers]
```

**Transformation with condition:**
```python
high_risk = [s for s in suppliers if s.risk_score > 3]
```

**Transformation with multiple outputs:**
```python
results = []
for item in data:
    if validate(item):
        results.append(transform(item))
return results
```

### When You'll Use This at Bell
- Cleaning 250 supplier records
- Filtering high-risk suppliers
- Extracting specific fields
- Converting data formats
- Calculating metrics

### Study Tip
**Look for:** `for x in`, `append()`, list comprehensions `[... for x in ...]`

---

## PATTERN 4: Error Handling (Try/Except)

### What It Does
Attempts risky operations and handles failures gracefully without crashing.

### How to Recognize It
```python
try:
    risky_operation()
except SpecificError as e:
    handle_error(e)
except Exception as e:
    handle_any_error(e)
finally:
    cleanup()
```

### Real Example from Your Code
```python
# Lines 806-957 in procurement_automation.py
try:
    cursor.execute("""UPDATE suppliers SET ...""")
    updated += 1
except sqlite3.IntegrityError as e:
    skipped += 1
    self.logger.warning(f"Integrity error: {str(e)}")
```

### Why It Matters
- **Resilience:** System doesn't crash on one bad record
- **Debugging:** Know what went wrong and where
- **Bell-specific:** 250+ suppliers, 1 bad one shouldn't stop everything
- **ITAR compliance:** Errors must be logged for audit trail

### Error Handling Strategies

**Strategy 1: Catch and Continue**
```python
for record in records:
    try:
        process(record)
    except ValueError:
        skip_record()
        continue
```

**Strategy 2: Catch and Log**
```python
try:
    operation()
except Exception as e:
    logger.error(f"Operation failed: {str(e)}")
```

**Strategy 3: Catch and Recover**
```python
try:
    connect_to_server()
except ConnectionError:
    use_backup_server()
```

**Strategy 4: Catch Multiple Types**
```python
try:
    operation()
except ValueError:
    handle_value_error()
except KeyError:
    handle_key_error()
except Exception:
    handle_unknown_error()
```

### When You'll Use This at Bell
- API calls (might fail temporarily)
- Database operations (integrity violations)
- File operations (permission issues)
- Data transformation (unexpected formats)

### Study Tip
**Look for:** `try:`, `except:`, `finally:`, `as e`

---

## PATTERN 5: Create/Configure/Return

### What It Does
Creates an object, configures its properties, then returns it ready to use.

### How to Recognize It
```python
def setup_something():
    obj = create_object()           # Create
    obj.property = value            # Configure
    obj.set_option(setting)         # Configure
    return obj                       # Return
```

### Real Example from Your Code
```python
# Lines 61-99 in procurement_automation.py
def setup_logging(config, env):
    logger = logging.getLogger("bell_procurement")          # Create
    logger.setLevel(getattr(logging, log_level))            # Configure
    
    formatter = logging.Formatter(...)                      # Create
    
    file_handler = logging.FileHandler(log_file)            # Create
    file_handler.setLevel(getattr(logging, log_level))      # Configure
    file_handler.setFormatter(formatter)                    # Configure
    
    console_handler = logging.StreamHandler(sys.stdout)     # Create
    console_handler.setLevel(logging.INFO)                  # Configure
    console_handler.setFormatter(formatter)                 # Configure
    
    logger.addHandler(file_handler)                         # Configure
    logger.addHandler(console_handler)                      # Configure
    
    return logger                                            # Return
```

### Why It Matters
- **Separation:** Setup logic stays organized
- **Reusability:** Return ready-to-use object
- **Testability:** Easy to test configuration
- **Bell-specific:** Set up database, API, logging once

### Variations

**Simple version:**
```python
def create_database():
    db = Database()
    db.connect("localhost")
    db.set_timeout(30)
    return db
```

**With parameters:**
```python
def create_logger(name, level):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger
```

**With builder pattern:**
```python
class APIClient:
    def __init__(self):
        self.base_url = None
        self.timeout = 30
    
    def set_url(self, url):
        self.base_url = url
        return self
    
    def set_timeout(self, timeout):
        self.timeout = timeout
        return self
    
    def build(self):
        return self

client = APIClient().set_url("https://api.example.com").set_timeout(60).build()
```

### When You'll Use This at Bell
- Setting up database connections
- Creating API clients
- Configuring loggers
- Initializing reporting tools
- Setting up compliance trackers

### Study Tip
**Look for:** Pattern of create → configure → return. Often in `setup_` or `create_` functions.

---

## PATTERN 6: If/Else Conditional

### What It Does
Makes decisions based on conditions and executes different code paths.

### How to Recognize It
```python
if condition:
    do_something()
elif other_condition:
    do_something_else()
else:
    do_default()
```

### Real Example from Your Code
```python
# Lines 387-419 in procurement_automation.py
if existing:
    # UPDATE existing record
    cursor.execute("""UPDATE suppliers SET...""")
    updated += 1
else:
    # INSERT new record
    cursor.execute("""INSERT INTO suppliers ...""")
    inserted += 1
```

### Why It Matters
- **Branching:** Different behavior for different situations
- **Logic:** Core of decision-making in code
- **Bell-specific:** Upsert (insert vs update), environment selection

### Variations

**Simple if:**
```python
if condition:
    do_something()
```

**If/else:**
```python
if condition:
    do_something()
else:
    do_something_else()
```

**Multiple conditions:**
```python
if condition1:
    do_a()
elif condition2:
    do_b()
elif condition3:
    do_c()
else:
    do_default()
```

**Ternary (one-liner):**
```python
result = value_if_true if condition else value_if_false
```

**Checking multiple conditions:**
```python
if condition1 and condition2:
    # Both must be true
    do_something()

if condition1 or condition2:
    # At least one must be true
    do_something()

if not condition:
    # Condition must be false
    do_something()
```

### When You'll Use This at Bell
- Checking environment (dev/test/prod)
- Upsert logic (insert vs update)
- Environment-specific config
- High-risk supplier decisions
- ITAR compliance checks

### Study Tip
**Look for:** `if`, `else`, `elif`

---

## PATTERN 7: Dictionary/Object Access

### What It Does
Retrieves values from dictionaries or objects.

### How to Recognize It
```python
# Safe access (returns None if key doesn't exist)
value = dictionary.get("key")
value = object.get("attribute")

# Direct access (crashes if key doesn't exist)
value = dictionary["key"]
value = object.attribute

# With default
value = dictionary.get("key", default_value)
```

### Real Example from Your Code
```python
# Lines 387-419 in procurement_automation.py
supplier.get("supplier_id")         # Safe - returns None if missing
supplier["duns_number"]             # Direct - crashes if missing
record.get("on_time_delivery_rate", 0)  # Safe with default
```

### Why It Matters
- **Safety:** `.get()` prevents crashes on missing keys
- **Readability:** Clear what data you're accessing
- **Bell-specific:** Accessing supplier fields like DUNS, risk score, spend

### Variations

**Dictionary access:**
```python
supplier = {"name": "Boeing", "duns": "100000001"}
name = supplier.get("name")           # Safe
name = supplier["name"]               # Direct

# With default
name = supplier.get("name", "Unknown")
```

**Object access:**
```python
supplier = SupplierData(name="Boeing", duns="100000001")
name = supplier.name                   # Direct
name = getattr(supplier, "name", "Unknown")  # Safe with default
```

**Nested access:**
```python
data = {"supplier": {"duns": "100000001"}}
duns = data.get("supplier", {}).get("duns")  # Safe nested access
```

### When You'll Use This at Bell
- Reading supplier fields
- Accessing config values
- Getting API response data
- Extracting database records

### Study Tip
**Look for:** `.get()`, `["key"]`, `.attribute`

---

## PATTERN 8: String Formatting

### What It Does
Builds strings by inserting variables into templates.

### How to Recognize It
```python
f"Text {variable} more text"              # f-string (modern)
"Text {} more".format(variable)            # .format() (older)
"Text " + variable + " more"               # Concatenation (rare)
```

### Real Example from Your Code
```python
# Lines 521-522 in procurement_automation.py
raise ValueError(f"DUNS number contains non-numeric characters: {duns}")
raise ValueError(f"DUNS number must be {DUNS_LENGTH} digits, got {len(duns_clean)}")

# Lines 254-255 in procurement_automation.py
self.logger.info(
    f"Fetching suppliers - Page: {page}, PageSize: {page_size}"
)
```

### Why It Matters
- **Readability:** Clear what's in the string
- **Debugging:** Easy to log what happened
- **Bell-specific:** Error messages, logging, reporting

### Variations

**Simple f-string:**
```python
name = "Boeing"
message = f"Supplier: {name}"
```

**With expressions:**
```python
count = 250
message = f"Processed {count} suppliers"
message = f"Total cost: ${total_cost * 1.1}"  # With calculation
```

**With formatting:**
```python
price = 1234.5
message = f"Price: ${price:.2f}"              # 2 decimal places
value = 42
message = f"Value: {value:09d}"               # 9 digits, padded with zeros
```

**Multi-line:**
```python
message = f"""
Supplier: {name}
DUNS: {duns}
Spend: ${spend:,.0f}
Risk: {risk_score}/5
"""
```

### When You'll Use This at Bell
- Building error messages
- Creating log messages
- Formatting database queries
- Building report text
- Creating email bodies

### Study Tip
**Look for:** `f"..."`, `{variable}`, `.format()`

---

## PATTERN 9: List/Dict Comprehension

### What It Does
Creates a new list or dictionary by transforming or filtering an existing one (in one line).

### How to Recognize It
```python
# List comprehension
new_list = [expression for item in list if condition]

# Dictionary comprehension
new_dict = {key: value for key, value in items}
```

### Real Examples

**Simple transformation:**
```python
# Traditional
supplier_names = []
for s in suppliers:
    supplier_names.append(s.name)

# Comprehension
supplier_names = [s.name for s in suppliers]
```

**With condition:**
```python
# Traditional
high_risk = []
for s in suppliers:
    if s.risk_score > 3:
        high_risk.append(s)

# Comprehension
high_risk = [s for s in suppliers if s.risk_score > 3]
```

**Dictionary comprehension:**
```python
# Traditional
supplier_dict = {}
for s in suppliers:
    supplier_dict[s.supplier_id] = s.name

# Comprehension
supplier_dict = {s.supplier_id: s.name for s in suppliers}
```

### Why It Matters
- **Concise:** One line instead of 3-4
- **Efficient:** Slightly faster than loops
- **Pythonic:** Professional Python style
- **Bell-specific:** Transform 250+ suppliers efficiently

### Variations

**Simple:**
```python
doubled = [x * 2 for x in numbers]
```

**With condition:**
```python
even = [x for x in numbers if x % 2 == 0]
```

**With transformation and condition:**
```python
names = [s.name for s in suppliers if s.risk_score < 3]
```

**Dictionary:**
```python
scores = {s.supplier_id: s.performance_score for s in suppliers}
```

### When You'll Use This at Bell
- Extracting supplier names
- Filtering high-risk suppliers
- Creating lookup dictionaries
- Converting data formats

### Study Tip
**Look for:** `[... for ... in ...]` pattern

---

## PATTERN 10: Function with Return Value

### What It Does
A function that performs calculations/operations and returns a result.

### How to Recognize It
```python
def function_name(parameters):
    result = do_something()
    return result

# Call it
output = function_name(input)
```

### Real Example from Your Code
```python
# Lines 671-694 in procurement_automation.py
def calculate_performance_score(self, supplier: SupplierPerformanceData) -> float:
    """Calculate composite performance score for supplier."""
    score = (
        (supplier.on_time_delivery_rate * 0.40) +
        ((100 - supplier.quality_rejection_rate) * 0.30) +
        (supplier.cost_reduction_score * 2 * 0.20) +
        ((5 - supplier.risk_score) * 20 * 0.10)
    )
    return round(min(100, max(0, score)), 2)
```

### Why It Matters
- **Reusability:** Use function many times
- **Modularity:** Breaks code into chunks
- **Testing:** Easy to test functions independently
- **Bell-specific:** Calculate scores, transform data, validate repeatedly

### Variations

**Simple return:**
```python
def get_name(supplier):
    return supplier.name
```

**Calculation and return:**
```python
def calculate_total_spend(suppliers):
    total = 0
    for s in suppliers:
        total += s.spend_ytd
    return total
```

**Conditional return:**
```python
def is_high_risk(supplier):
    if supplier.risk_score > 3 and supplier.spend_ytd > 100000:
        return True
    return False
```

**Multiple return values:**
```python
def validate_and_clean(duns):
    if len(duns) != 9:
        return False, None
    return True, duns.strip()

valid, cleaned = validate_and_clean(duns)
```

### When You'll Use This at Bell
- Calculating performance scores
- Validating supplier data
- Extracting and transforming data
- Risk scoring
- Any reusable operation

### Study Tip
**Look for:** `def function_name():`, `return value`

---

## Study Plan

### Week 1: Master Patterns 1-3
- **Pattern 1 (Configuration Reading):** 30 min
  - Read your config.ini
  - Understand how config.get() works
  - Find 3 config.get() calls in your code
  
- **Pattern 2 (Validation):** 1 hour
  - Understand validation flow
  - Find 5 validation patterns in your code
  - Write your own validation function
  
- **Pattern 3 (Loop and Transform):** 1 hour
  - Understand for loops
  - Practice list comprehensions
  - Find 3 loop patterns in your code

### Week 2: Master Patterns 4-5
- **Pattern 4 (Error Handling):** 1 hour
  - Understand try/except
  - Find error handling in your code
  - Practice writing try/except blocks
  
- **Pattern 5 (Create/Configure/Return):** 1 hour
  - Understand setup functions
  - Trace setup_logging() completely
  - Find other setup patterns

### Week 3: Learn Patterns 6-10
- **Pattern 6 (Conditionals):** 30 min
- **Pattern 7 (Dictionary Access):** 30 min
- **Pattern 8 (String Formatting):** 30 min
- **Pattern 9 (Comprehensions):** 30 min
- **Pattern 10 (Functions):** 30 min

### Week 4: Practice Recognition
- Spend 1 hour daily finding patterns in your code
- Write pattern identification notes
- Practice writing code using patterns

---

## Practice Exercises

### Exercise 1: Identify Patterns in Your Code

**Find and mark the following in `procurement_automation.py`:**

1. **Find 3 Configuration Reading patterns**
   - What values are being read?
   - Why use config instead of hardcoding?

2. **Find 5 Validation patterns**
   - What's being validated?
   - What errors can occur?

3. **Find 3 Loop and Transform patterns**
   - What's being transformed?
   - What's the output?

4. **Find 2 Error Handling patterns**
   - What errors are caught?
   - What happens when caught?

5. **Find 1 Create/Configure/Return pattern**
   - What's being created?
   - What properties are set?

### Exercise 2: Write Pattern Examples

Write your own examples of each pattern:

```python
# Pattern 1: Configuration Reading
# TODO: Write your own config.get() example

# Pattern 2: Validation
# TODO: Write your own validation function

# Pattern 3: Loop and Transform
# TODO: Write your own loop example

# Pattern 4: Error Handling
# TODO: Write your own try/except example

# Pattern 5: Create/Configure/Return
# TODO: Write your own setup function

# Patterns 6-10: Similar exercises
```

### Exercise 3: Spot the Pattern Game

For each code snippet, identify the pattern:

**Snippet 1:**
```python
if supplier.risk_score > 3 and supplier.spend_ytd > 100000:
    flag_for_review(supplier)
```
**Pattern:** _____________

**Snippet 2:**
```python
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
return logger
```
**Pattern:** _____________

**Snippet 3:**
```python
processed = [transform(item) for item in data if validate(item)]
```
**Pattern:** _____________

**Snippet 4:**
```python
try:
    save_to_database(record)
except IntegrityError:
    skip_record()
```
**Pattern:** _____________

**Snippet 5:**
```python
config.get("PROD", "DATABASE_URL")
```
**Pattern:** _____________

### Exercise 4: Real Bell Scenarios

**Scenario 1:** You need to read the API rate limit from config.ini
- What pattern would you use?
- Write the code

**Scenario 2:** You need to check if a supplier is valid before processing
- What pattern would you use?
- Write the code

**Scenario 3:** You need to clean 250 suppliers
- What pattern would you use?
- Write the code

**Scenario 4:** You need to handle a database error gracefully
- What pattern would you use?
- Write the code

**Scenario 5:** You need to calculate a performance score
- What pattern would you use?
- Write the code

---

## Key Takeaways

1. **Patterns are everywhere** - Once you recognize them, code becomes readable
2. **Patterns are reusable** - You'll use them again and again
3. **Patterns are teachable** - You can learn and master them
4. **Patterns show expertise** - Using right pattern = professional code
5. **Patterns at Bell** - These 10 patterns cover 80% of codebase

---

## Quick Reference Cheat Sheet

| Pattern | Recognize By | Example |
|---------|---|---|
| 1. Config Reading | `.get()` | `config.get("PROD", "URL")` |
| 2. Validation | `if not`, `raise` | `if len(x) != 9: raise ValueError()` |
| 3. Loop Transform | `for x in`, `append()` | `[transform(x) for x in data]` |
| 4. Error Handling | `try:`, `except:` | `try: op() except Error: handle()` |
| 5. Create/Configure | Setup pattern | Create → Configure → Return |
| 6. Conditional | `if`, `else` | `if x: do_a() else: do_b()` |
| 7. Dict/Object Access | `.get()`, `["key"]` | `obj.get("field", default)` |
| 8. String Format | `f"{}"` | `f"Total: ${amount:.2f}"` |
| 9. Comprehension | `[... for ... in ...]` | `[s.name for s in suppliers]` |
| 10. Return Value | `return` | `def calc(x): return x * 2` |

---

## Final Note

**Your job at Bell is NOT to write these patterns from scratch.**

Your job is to:
1. ✅ **Recognize** when a pattern is being used
2. ✅ **Understand** what the pattern does
3. ✅ **Apply** the pattern to similar situations
4. ✅ **Modify** the pattern for your needs

**That's it. You're ready.**

