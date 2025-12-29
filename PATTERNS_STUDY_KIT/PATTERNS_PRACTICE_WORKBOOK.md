# Coding Patterns Practice Workbook

**Your interactive guide to mastering Bell's 10 most common patterns**

Complete the exercises in this workbook as you study each pattern.

---

## Exercise 1: Identify Patterns in procurement_automation.py

### Task: Find Configuration Reading Patterns (Pattern 1)

Find these lines in your code and explain what they do:

**Location:** Lines 71-72
```python
log_level = config.get("DEFAULT", "LOG_LEVEL")
log_file = config.get(env.upper(), "LOG_FILE")
```

What's being read?
- From: _______________
- Keys being read: _______________
- Why not hardcode? _______________

**Find 2 more config.get() calls in the code and document them below:**

Config Reading #2:
- Location: Line ____
- Code: _______________
- Purpose: _______________

Config Reading #3:
- Location: Line ____
- Code: _______________
- Purpose: _______________

---

### Task: Find Validation Patterns (Pattern 2)

Go to the `_validate_duns_number()` function (lines 517-540).

List all the validation checks:

1. Check: _______________
   - If fails: _______________
   - Why important: _______________

2. Check: _______________
   - If fails: _______________
   - Why important: _______________

3. Check: _______________
   - If fails: _______________
   - Why important: _______________

4. Check: _______________
   - If fails: _______________
   - Why important: _______________

**Find 1 other validation function and document it:**

Function Name: _______________
Location: Line ____
What it validates: _______________
Validation checks (list them):
- _______________
- _______________
- _______________

---

### Task: Find Loop and Transform Patterns (Pattern 3)

Go to the `clean_suppliers()` function (lines 387-419).

**What's the loop doing?**

Input: _______________
Process: _______________
Output: _______________

**How would you rewrite this as a list comprehension?**

```python
# Original (lines 387-419):
cleaned = []
for supplier_data in suppliers:
    try:
        cleaned_record = self._clean_record(supplier_data)
        cleaned.append(cleaned_record)
    except ValueError as e:
        errors.append({...})

# As comprehension (try below):
# (Hint: with try/except, comprehensions are harder, so traditional loop is fine)
```

**Find 2 more loop patterns:**

Loop #1:
- Location: Line ____
- What's being looped: _______________
- What transformation: _______________

Loop #2:
- Location: Line ____
- What's being looped: _______________
- What transformation: _______________

---

### Task: Find Error Handling Patterns (Pattern 4)

Find the try/except block in `upsert_suppliers()` (around lines 806-957).

**What could go wrong?**

Error type being caught: _______________
What causes it: _______________
How it's handled: _______________

**Find 2 more error handling patterns:**

Error Handling #1:
- Location: Line ____
- Error caught: _______________
- Handler: _______________

Error Handling #2:
- Location: Line ____
- Error caught: _______________
- Handler: _______________

---

### Task: Find Create/Configure/Return Pattern (Pattern 5)

The `setup_logging()` function (lines 61-99) is a perfect example.

**Map each step:**

Step 1 (Create):
- What's created: _______________
- Line: ____

Step 2 (Configure):
- What's configured: _______________
- Lines: ____-____

Step 3 (Configure More):
- What else: _______________
- Lines: ____-____

Step 4 (Return):
- What's returned: _______________
- Line: ____

---

## Exercise 2: Write Your Own Pattern Examples

### Pattern 1: Configuration Reading

Write code that reads a setting from config.ini:

```python
# Read the API timeout from config
# (Hint: Look for API_TIMEOUT or similar in config.ini)

# Your code:
api_timeout = config.get("DEFAULT", "API_TIMEOUT_SECONDS")
```

Now write your own:
- Read the log file location for PROD environment

```python
# Your answer:
prod_log_file = _________________________________
```

---

### Pattern 2: Validation

Write a validation function for supplier spend:

Requirements:
- Check if spend is provided (not empty)
- Check if it's a positive number
- Check if it's not more than $10 million
- Raise ValueError with helpful message

```python
def validate_spend(spend):
    # Your code here:
    if ________________:
        raise ValueError("_________")
    
    if ________________:
        raise ValueError("_________")
    
    if ________________:
        raise ValueError("_________")
    
    return spend
```

---

### Pattern 3: Loop and Transform

Write code to extract supplier names:

Given: A list of suppliers with `.name` attribute
Need: A list of just the names

**Traditional loop:**
```python
names = []
for supplier in suppliers:
    names.append(supplier.name)
```

**As comprehension:**
```python
names = _____________________________
```

**Bonus: With filter for high-risk only:**
```python
high_risk_names = _________________________________ if supplier.risk_score > 3
```

---

### Pattern 4: Error Handling

Write error handling for API calls:

```python
def fetch_from_api(url):
    try:
        # What to do:
        response = requests.get(url)
        return response.json()
    except ________________ as e:
        # Handle connection errors
        logger.warning(f"Connection failed: {str(e)}")
        return None
    except ________________ as e:
        # Handle other errors
        logger.error(f"API error: {str(e)}")
        raise
```

---

### Pattern 5: Create/Configure/Return

Write a setup function for a database connection:

```python
def setup_database(config, environment):
    # Step 1: Create
    db = Database()
    
    # Step 2: Configure
    _________________________
    _________________________
    _________________________
    
    # Step 3: Return
    return db
```

---

## Exercise 3: Pattern Recognition Quiz

For each code snippet, identify the pattern number (1-10):

**Quiz #1:**
```python
suppliers = [s for s in all_suppliers if s.risk_score < 3]
```
Pattern: ______

**Quiz #2:**
```python
if supplier.as9100_certified and supplier.itar_compliant:
    approve_supplier(supplier)
```
Pattern: ______

**Quiz #3:**
```python
def calculate_score(metrics):
    total = sum(metrics.values())
    return total / len(metrics)
```
Pattern: ______

**Quiz #4:**
```python
database_url = config.get("PROD", "DATABASE_URL")
api_key = os.environ.get("API_KEY")
```
Pattern: ______

**Quiz #5:**
```python
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
handler = logging.FileHandler("app.log")
logger.addHandler(handler)
return logger
```
Pattern: ______

**Quiz #6:**
```python
try:
    save_to_db(supplier)
except IntegrityError:
    skip_record()
except Exception as e:
    logger.error(f"Unexpected: {str(e)}")
    raise
```
Pattern: ______

**Quiz #7:**
```python
duns = duns.replace("-", "").strip()
if not duns.isdigit():
    raise ValueError("Invalid DUNS")
if len(duns) != 9:
    raise ValueError("Wrong length")
```
Pattern: ______

**Quiz #8:**
```python
error_msg = f"Supplier {name} failed with error: {error_code}"
```
Pattern: ______

**Quiz #9:**
```python
supplier_dict = {s.id: s.name for s in suppliers}
```
Pattern: ______

**Quiz #10:**
```python
value = supplier.get("field", "default_value")
```
Pattern: ______

**Answers:** (Check your answers against CODING_PATTERNS_GUIDE.md)
1. ___ 2. ___ 3. ___ 4. ___ 5. ___
6. ___ 7. ___ 8. ___ 9. ___ 10. ___

---

## Exercise 4: Real Bell Scenarios

### Scenario 1: Reading Configuration

**Situation:** You need to know if ITAR logging is enabled for the current environment.

**Solution Pattern:** Configuration Reading

**Code to write:**
```python
# Read from config.ini in the PROD section
itar_logging_enabled = _________________________________

# Use it
if itar_logging_enabled:
    log_itar_access(supplier)
```

---

### Scenario 2: Validating ITAR Compliance

**Situation:** You're importing suppliers and need to ensure ITAR flags are boolean.

**Solution Pattern:** Validation

**Code to write:**
```python
def validate_itar_flag(supplier):
    if not isinstance(supplier.get('itar_compliant'), bool):
        raise _________________________
    
    return supplier
```

---

### Scenario 3: Processing 250 Suppliers

**Situation:** You need to get all ITAR-compliant supplier names for a report.

**Solution Pattern:** Loop and Transform

**Code to write:**
```python
# Get names of ITAR-compliant suppliers
itar_suppliers = _________________________________

# Or if you need more than just names:
itar_info = _________________________________
```

---

### Scenario 4: Database Insert Error

**Situation:** Inserting 250 suppliers, but sometimes there's a duplicate. Don't crash, just skip it.

**Solution Pattern:** Error Handling

**Code to write:**
```python
for supplier in suppliers:
    try:
        _________________________________
    except _________________________:
        logger.warning(f"Duplicate: {supplier['id']}")
        continue
```

---

### Scenario 5: Setting Up Audit Logging

**Situation:** You need to create and configure an audit logger for ITAR transactions.

**Solution Pattern:** Create/Configure/Return

**Code to write:**
```python
def setup_itar_audit_logger(log_file):
    # Create
    audit_logger = logging.getLogger("bell_itar_audit")
    
    # Configure
    _________________________________
    _________________________________
    
    # Return
    return audit_logger
```

---

## Study Checklist

### Week 1
- [ ] Read all Pattern 1 material (Configuration Reading)
- [ ] Find 3 Pattern 1 examples in your code
- [ ] Complete Pattern 1 exercises
- [ ] Read all Pattern 2 material (Validation)
- [ ] Find 5 Pattern 2 examples in your code
- [ ] Complete Pattern 2 exercises
- [ ] Read all Pattern 3 material (Loop & Transform)
- [ ] Find 3 Pattern 3 examples in your code
- [ ] Complete Pattern 3 exercises

### Week 2
- [ ] Read Pattern 4 material (Error Handling)
- [ ] Find 2 Pattern 4 examples in your code
- [ ] Complete Pattern 4 exercises
- [ ] Read Pattern 5 material (Create/Configure/Return)
- [ ] Find 2 Pattern 5 examples in your code
- [ ] Complete Pattern 5 exercises

### Week 3
- [ ] Read Patterns 6-10 material
- [ ] Complete Patterns 6-10 exercises
- [ ] Complete Pattern Recognition Quiz
- [ ] Score: ___/10

### Week 4
- [ ] Complete Real Bell Scenarios exercises
- [ ] Write own examples for each pattern
- [ ] Can you recognize all patterns in your code? Y/N
- [ ] Ready for Bell? Y/N

---

## Notes & Reflections

**As you study, write your thoughts here:**

Pattern I found most useful: _______________
Why: _______________

Pattern I found confusing: _______________
Why: _______________

Real Bell scenario I'm now ready for: _______________

Questions I still have:
- _______________
- _______________
- _______________

---

## Your Pattern Recognition Score

Track your progress:

| Pattern | Understand? | Can Find It? | Can Write It? |
|---------|---|---|---|
| 1. Config | Y/N | Y/N | Y/N |
| 2. Validation | Y/N | Y/N | Y/N |
| 3. Loop/Transform | Y/N | Y/N | Y/N |
| 4. Error Handling | Y/N | Y/N | Y/N |
| 5. Create/Configure | Y/N | Y/N | Y/N |
| 6. Conditional | Y/N | Y/N | Y/N |
| 7. Dict/Object | Y/N | Y/N | Y/N |
| 8. String Format | Y/N | Y/N | Y/N |
| 9. Comprehension | Y/N | Y/N | Y/N |
| 10. Return Value | Y/N | Y/N | Y/N |

**Goal:** All "Y/N" answered "Y" before Jan 12.

---

## Final Checklist Before Jan 12

- [ ] I can recognize all 10 patterns in code
- [ ] I understand what each pattern does
- [ ] I could explain each pattern to someone
- [ ] I can find examples in my own code
- [ ] I could write basic examples
- [ ] I feel confident reading uncommented code
- [ ] I'm ready for Bell

**Confidence Level: 1-10 ___**

**Your Bell Readiness: 1-10 ___**

