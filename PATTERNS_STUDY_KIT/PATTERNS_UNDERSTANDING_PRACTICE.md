# 🎓 Coding Patterns: Understanding & Practice Guide

**How to use this guide:**
1. Read the **UNDERSTAND** section
2. Study the **GUIDED EXAMPLE**
3. Try the **PRACTICE PROBLEM** (with help)
4. **SPOT IT** in real code
5. **YOUR JOB** - what you'll do at Bell

No explanations required. Everything has answers.

---

# PATTERN 1: CONFIGURATION READING

## UNDERSTAND IT

**What It Does:**
Instead of writing values directly in code (`database = "localhost"`), you read values from a config file (`config.ini`). This lets you change settings without touching code.

**Why Bell Uses It:**
- Dev team uses dev database (localhost)
- Production uses real database (prod.server.com)
- **Same code, different settings**
- If Bell changes business rule (approval amount), edit config file, done

**The Problem Without This Pattern:**
```python
# ❌ HARDCODED - Won't work in production
database = "localhost"
api_key = "secret-key-12345"
approval_threshold = 50000
```

If you hardcode "localhost", production will crash (can't connect to real database).

**The Solution:**
```python
# ✅ FROM CONFIG - Works everywhere
database = config.get("DATABASE", "URL")
api_key = os.environ.get("API_KEY")
approval_threshold = config.getint("BUSINESS", "APPROVAL_THRESHOLD")
```

Now:
- Dev: `config.get()` reads "localhost"
- Prod: `config.get()` reads "prod.server.com"
- **Same code, different output**

---

## GUIDED EXAMPLE

**Real code from procurement_automation.py (lines 71-72):**

```python
log_level = config.get("DEFAULT", "LOG_LEVEL")
log_file = config.get(env.upper(), "LOG_FILE")
```

**What's happening step-by-step:**

Step 1: `config.get("DEFAULT", "LOG_LEVEL")`
- Opens config.ini file
- Finds section: `[DEFAULT]`
- Finds key: `LOG_LEVEL`
- Returns value: `"INFO"` or `"DEBUG"`
- Stores in: `log_level` variable

Step 2: `env.upper()`
- `env` might be "dev" or "prod"
- `.upper()` converts to "DEV" or "PROD"
- So `config.get(env.upper(), "LOG_FILE")` becomes `config.get("PROD", "LOG_FILE")`

Step 3: Result
- Dev environment: reads `[DEV]` section
- Prod environment: reads `[PROD]` section
- **Same code, different settings**

**config.ini looks like:**
```ini
[DEFAULT]
LOG_LEVEL = INFO

[DEV]
LOG_FILE = /tmp/dev.log

[PROD]
LOG_FILE = /var/log/prod.log
```

---

## PRACTICE PROBLEM

**Your task:** 
Write code to read the database URL from config (Section: "DATABASE", Key: "URL")

```python
# Fill in the blank:
database_url = ???
```

**Answer:**
```python
database_url = config.get("DATABASE", "URL")
```

**Why this works:**
- Same pattern as line 71
- Section is "DATABASE" (matches [DATABASE] in config.ini)
- Key is "URL" (matches URL = ... in config.ini)
- Returns the value, stores in database_url

---

## SPOT IT IN REAL CODE

**Find these in procurement_automation.py:**

1. **Line 71:** `log_level = config.get("DEFAULT", "LOG_LEVEL")`
   - Reading: Log level setting
   - Why config: Dev uses DEBUG, Prod uses INFO

2. **Line 72:** `log_file = config.get(env.upper(), "LOG_FILE")`
   - Reading: Log file location
   - Why config: Dev writes to /tmp, Prod writes to /var/log

3. **Line 110-120:** Database connection config
   - Reading: database URL, port, name
   - Why config: Dev is localhost, Prod is real server

---

## YOUR JOB AT BELL

**Day 1 Scenario:**
Your manager says: "Deploy to staging. Update config.ini to use the staging database."

**What you do:**
1. Open config.ini
2. Find `[STAGING]` section (or create it)
3. Update: `URL = staging.db.bell.textron.com`
4. Save file
5. Deploy code (NO CODE CHANGES NEEDED)

**Why this matters:**
- Same code works in dev/test/staging/prod
- Only config changes
- Fast deployments
- Safe (no code modifications)

---

# PATTERN 2: VALIDATION

## UNDERSTAND IT

**What It Does:**
Checks that data is correct BEFORE using it. If data is bad, stop and report error.

**Why Bell Uses It:**
- Suppliers come from external sources (Ariba, user input, etc.)
- External data can't be trusted
- A bad DUNS number would corrupt supplier database
- Validate EVERYTHING from outside sources

**The Problem Without This Pattern:**
```python
# ❌ NO VALIDATION
duns = user_input  # Could be anything!
insert_supplier(duns=duns)  # Saves bad data to database
# Later: Reports are wrong because database has junk
```

**The Solution:**
```python
# ✅ WITH VALIDATION
duns = user_input  # Could be anything
if len(duns) != 9:
    raise ValueError("DUNS must be 9 digits")
if not duns.isdigit():
    raise ValueError("DUNS must be numbers only")
# Only if validation passes:
insert_supplier(duns=duns)  # Database stays clean
```

---

## GUIDED EXAMPLE

**Real code from procurement_automation.py (lines 517-540):**

```python
def _validate_duns_number(duns: str) -> str:
    # Check 1: Is it empty?
    if not duns:
        raise ValueError("DUNS number cannot be empty")
    
    # Check 2: Clean it (remove spaces, dashes)
    duns_clean = str(duns).replace("-", "").replace(" ", "").strip()
    
    # Check 3: Is it only numbers?
    if not duns_clean.isdigit():
        raise ValueError(f"DUNS number contains non-numeric characters: {duns}")
    
    # Check 4: Is it exactly 9 digits?
    if len(duns_clean) != 9:
        raise ValueError(f"DUNS number must be 9 digits, got {len(duns_clean)}")
    
    # All checks passed! Return cleaned value
    return duns_clean
```

**What's happening:**

**Check 1: Is it empty?**
- Input: "" (empty string)
- Check: `if not duns:` (is it empty?)
- Action: Raise error with message
- Why: Can't use empty supplier ID

**Check 2: Clean it**
- Input: "123-456-789" or "123 456 789"
- Action: Remove dashes and spaces
- Result: "123456789"
- Why: Users sometimes type with formatting

**Check 3: Only numbers?**
- Input: "12345678A" (has letter A)
- Check: `duns_clean.isdigit()` (are all characters 0-9?)
- Action: Raise error if not all numbers
- Why: DUNS is numbers only

**Check 4: Exactly 9 digits?**
- Input: "12345678" (only 8)
- Check: `len(duns_clean) != 9` (is length 9?)
- Action: Raise error if not 9
- Why: DUNS industry standard is 9 digits

**If all checks pass:**
- Return: "123456789" (cleaned, validated)
- Now safe to use

---

## PRACTICE PROBLEM

**Your task:**
Write validation for approval amount (must be positive number)

```python
def validate_approval_amount(amount):
    # Check 1: Is it empty?
    if ???:
        raise ValueError("Amount required")
    
    # Check 2: Can we convert to number?
    try:
        amount_num = float(amount)
    except ValueError:
        raise ValueError("Amount must be numeric")
    
    # Check 3: Is it positive?
    if ???:
        raise ValueError("Amount must be greater than zero")
    
    # All checks passed
    return amount_num
```

**Answers:**
```python
def validate_approval_amount(amount):
    # Check 1: Is it empty?
    if not amount:
        raise ValueError("Amount required")
    
    # Check 2: Can we convert to number?
    try:
        amount_num = float(amount)
    except ValueError:
        raise ValueError("Amount must be numeric")
    
    # Check 3: Is it positive?
    if amount_num <= 0:
        raise ValueError("Amount must be greater than zero")
    
    # All checks passed
    return amount_num
```

**Why these checks:**
- Check 1: `if not amount:` catches None, empty string, 0
- Check 3: `if amount_num <= 0:` catches negative or zero (must be positive)

---

## SPOT IT IN REAL CODE

**Find these validations in procurement_automation.py:**

1. **Lines 517-540:** `_validate_duns_number()`
   - What's validated: DUNS format
   - Checks: Empty? Numbers only? Exactly 9 digits?

2. **Lines 545-560:** Other validation functions
   - Search for `if not` and `raise ValueError`
   - Each one checks something different

3. **Lines 387-419:** Validation in `clean_suppliers()`
   - Calls `_validate_duns_number()`
   - Catches errors and logs them

---

## YOUR JOB AT BELL

**Day 1 Scenario:**
Manager: "We're importing 500 suppliers from CSV. Make sure bad data doesn't get into the database."

**What you do:**
1. Find the validation functions (already written)
2. Call validation before inserting
3. If validation fails, log error and skip supplier
4. If validation passes, insert supplier
5. Report: "500 imported, 3 skipped (bad data)"

**Why this matters:**
- Bad data corrupts reports
- Validation prevents garbage in, garbage out
- Bell's data stays clean

---

# PATTERN 3: LOOP AND TRANSFORM

## UNDERSTAND IT

**What It Does:**
Process multiple items one at a time, change each one, collect results.

**Why Bell Uses It:**
- Ariba returns 250 suppliers
- Each supplier needs cleaning
- Need to process all 250 (not manually one by one)
- Loop: Go through each supplier
- Transform: Clean it
- Collect: Save cleaned versions

**The Problem Without This Pattern:**
```python
# ❌ MANUAL - Process one at a time
supplier1 = clean_supplier(supplier1)
supplier2 = clean_supplier(supplier2)
supplier3 = clean_supplier(supplier3)
# ... this would take 250 lines!
```

**The Solution:**
```python
# ✅ LOOP - Process all at once
cleaned_suppliers = []
for supplier in suppliers:
    cleaned = clean_supplier(supplier)
    cleaned_suppliers.append(cleaned)
# One loop handles all 250
```

---

## GUIDED EXAMPLE

**Real code from procurement_automation.py (lines 387-419):**

```python
cleaned = []
errors = []

for supplier_data in suppliers:  # ← LOOP: Go through each supplier
    try:
        cleaned_record = self._clean_record(supplier_data)  # ← TRANSFORM: Clean it
        cleaned.append(cleaned_record)  # ← COLLECT: Save the cleaned version
    except ValueError as e:
        errors.append({"data": supplier_data, "error": str(e)})  # ← COLLECT errors

return cleaned, errors
```

**What's happening:**

**Setup:**
- `cleaned = []` - Empty list to collect results
- `errors = []` - Empty list to collect errors

**Loop iteration (repeat for each supplier):**
- `for supplier_data in suppliers:` - Get one supplier
- `cleaned_record = self._clean_record(supplier_data)` - Transform: clean this supplier
- `cleaned.append(cleaned_record)` - Add to results list
- If error occurs, add to error list

**Result:**
- `cleaned` = List of 240-250 clean suppliers (some were too bad)
- `errors` = List of 0-10 that had problems

**Step-by-step example with 3 suppliers:**
```
Input: [
    {"name": " BOEING ", "duns": "123-456-789"},
    {"name": "airbus", "duns": "invalid"},
    {"name": "LOCKHEED", "duns": "987654321"}
]

Loop iteration 1:
  Input: {"name": " BOEING ", "duns": "123-456-789"}
  Transform: Clean name → "BOEING", Clean DUNS → "123456789"
  Result: {"name": "BOEING", "duns": "123456789"}
  Add to cleaned list

Loop iteration 2:
  Input: {"name": "airbus", "duns": "invalid"}
  Transform: Tries to clean, DUNS validation fails
  Result: Error! Add to errors list

Loop iteration 3:
  Input: {"name": "LOCKHEED", "duns": "987654321"}
  Transform: Clean name → "LOCKHEED", DUNS is good
  Result: {"name": "LOCKHEED", "duns": "987654321"}
  Add to cleaned list

Output:
  cleaned = [
    {"name": "BOEING", "duns": "123456789"},
    {"name": "LOCKHEED", "duns": "987654321"}
  ]
  errors = [
    {"data": {"name": "airbus", "duns": "invalid"}, "error": "DUNS invalid"}
  ]
```

---

## PRACTICE PROBLEM

**Your task:**
Extract supplier names from a list of supplier objects

```python
suppliers = [
    {"name": "Boeing", "duns": "123456789"},
    {"name": "Airbus", "duns": "987654321"},
    {"name": "Lockheed", "duns": "555666777"}
]

# Get just the names: ["Boeing", "Airbus", "Lockheed"]

# Method 1: Traditional loop
supplier_names = []
for ??? in ???:
    ???
print(supplier_names)

# Method 2: List comprehension (shorter)
supplier_names = [??? for ??? in ???]
print(supplier_names)
```

**Answers:**

**Method 1: Traditional loop**
```python
supplier_names = []
for supplier in suppliers:
    supplier_names.append(supplier["name"])
print(supplier_names)  # ["Boeing", "Airbus", "Lockheed"]
```

**Method 2: List comprehension**
```python
supplier_names = [supplier["name"] for supplier in suppliers]
print(supplier_names)  # ["Boeing", "Airbus", "Lockheed"]
```

**Why these work:**
- `for supplier in suppliers:` - Loop through each supplier
- `supplier["name"]` - Get the name field
- `.append()` - Add to list
- List comprehension does same thing in one line

---

## SPOT IT IN REAL CODE

**Find these in procurement_automation.py:**

1. **Lines 387-419:** `clean_suppliers()` function
   - Loop: `for supplier_data in suppliers:`
   - Transform: `self._clean_record(supplier_data)`
   - Collect: `cleaned.append(cleaned_record)`

2. **Lines 400-450:** Other loops
   - Search for `for ??? in ???:`
   - Find what's being transformed
   - Find what's being collected

---

## YOUR JOB AT BELL

**Day 1 Scenario:**
Manager: "Import 250 suppliers from Ariba. Clean each one. Report how many succeeded and failed."

**What you do:**
1. Get all 250 suppliers from Ariba API
2. Loop through each supplier
3. Transform: Clean name, validate DUNS, check ITAR status
4. Collect: Good ones go to database, bad ones go to error list
5. Report: "248 imported successfully, 2 had errors"

**Why this matters:**
- Manual processing = impossible (250 items)
- Loop + transform = process all at once
- Collect results and errors separately

---

# PATTERN 4: ERROR HANDLING (TRY/EXCEPT)

## UNDERSTAND IT

**What It Does:**
Attempts something risky. If it fails, handle the failure gracefully (don't crash).

**Why Bell Uses It:**
- Ariba API might be slow or down
- Database might have integrity constraint
- File might not exist
- Any risky operation might fail
- System shouldn't crash on one failure
- Continue processing, skip the bad one, log the error

**The Problem Without This Pattern:**
```python
# ❌ NO ERROR HANDLING
for supplier in suppliers:
    save_to_database(supplier)  # If one fails, CRASHES - rest never processed
# Only 100 of 250 saved before crash
```

**The Solution:**
```python
# ✅ WITH ERROR HANDLING
for supplier in suppliers:
    try:
        save_to_database(supplier)  # Attempt risky operation
    except DatabaseError:
        log_error(supplier)  # If fails, log it
        continue  # Skip this one, continue with next
# All 250 attempted, bad ones logged
```

---

## GUIDED EXAMPLE

**Real code from procurement_automation.py (lines 806-957):**

```python
for supplier in suppliers:
    try:
        # Risky operation: insert into database
        cursor.execute("""INSERT INTO suppliers (name, duns) VALUES (?, ?)""",
                      (supplier["name"], supplier["duns"]))
        database.commit()  # Save to database
        inserted += 1
        
    except sqlite3.IntegrityError as e:
        # Catch if this specific error occurs
        skipped += 1
        self.logger.warning(f"Integrity error for supplier {supplier['duns']}: {str(e)}")
        database.rollback()  # Undo partial changes
        
    except Exception as e:
        # Catch any other error
        skipped += 1
        self.logger.error(f"Unexpected error: {str(e)}")
        database.rollback()
```

**What's happening:**

**Try block (lines 1-5):**
- Attempt: Insert supplier into database
- `cursor.execute()` - Run SQL command
- `database.commit()` - Save changes
- If all works: `inserted += 1`

**Except block - IntegrityError (lines 7-11):**
- If constraint violation occurs (like duplicate DUNS)
- Catch it (don't crash)
- Log warning: "This supplier couldn't be inserted"
- Rollback: Undo partial changes
- `skipped += 1` - Count skipped

**Except block - Any other error (lines 13-16):**
- If unexpected error occurs
- Log error: "Something else went wrong"
- Rollback: Undo partial changes

**Result:**
- Tried to insert 250 suppliers
- Maybe 248 succeeded, 2 had errors
- Program didn't crash
- Errors were logged for investigation

---

## PRACTICE PROBLEM

**Your task:**
Write error handling for calling an external API

```python
try:
    # Attempt risky operation: call external API
    response = ariba_api.get_suppliers()
    suppliers = response["data"]
    
except ??? as e:
    # If API returns invalid response
    self.logger.error(f"API error: {str(e)}")
    suppliers = []

except ??? as e:
    # If network is down
    self.logger.error(f"Network error: {str(e)}")
    suppliers = []

# Continue processing
for supplier in suppliers:
    # process supplier
    pass
```

**Answers:**
```python
try:
    response = ariba_api.get_suppliers()
    suppliers = response["data"]
    
except KeyError as e:
    # If API returns invalid response (missing "data" key)
    self.logger.error(f"API error: {str(e)}")
    suppliers = []

except ConnectionError as e:
    # If network is down
    self.logger.error(f"Network error: {str(e)}")
    suppliers = []

# Continue processing
for supplier in suppliers:
    pass
```

**Why these work:**
- `KeyError` - Catches when API response missing expected field
- `ConnectionError` - Catches network failures
- Both set `suppliers = []` so loop still runs (just with no items)
- Program continues instead of crashing

---

## SPOT IT IN REAL CODE

**Find these in procurement_automation.py:**

1. **Lines 806-957:** Large try/except block
   - Try: Database insert/update operations
   - Except: IntegrityError (constraint violation)
   - Except: Any other error

2. **Lines 250-280:** API call error handling
   - Try: Call Ariba API
   - Except: Network or format errors

---

## YOUR JOB AT BELL

**Day 1 Scenario:**
Manager: "Import from Ariba. If API is slow, skip it but don't crash. Log everything."

**What you do:**
1. Try to connect to Ariba API
2. If fails: Log the error, continue with local data
3. Try to insert suppliers
4. If one fails: Log it, skip it, process next
5. At end: Report "500 processed, 2 had errors - see logs"

**Why this matters:**
- Systems fail sometimes (networks, databases)
- Code shouldn't crash on failures
- Log everything for debugging
- User sees "2 errors" not "Program crashed"

---

# PATTERN 5: CREATE/CONFIGURE/RETURN

## UNDERSTAND IT

**What It Does:**
Create an object → Set its properties → Return it ready to use.

**Why Bell Uses It:**
- Setup is complex (logging, database, API clients)
- Don't want setup code scattered everywhere
- Create one function that does all setup
- Call function once at startup
- Get back something ready to use

**The Problem Without This Pattern:**
```python
# ❌ Setup scattered everywhere
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
formatter = logging.Formatter(...)
handler = logging.FileHandler("app.log")
handler.setFormatter(formatter)
logger.addHandler(handler)
# ... this code appears in 5 different files!
```

**The Solution:**
```python
# ✅ Setup in one function
def setup_logger():
    logger = logging.getLogger("app")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(...)
    handler = logging.FileHandler("app.log")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

# Use it
logger = setup_logger()  # One line, ready to use
```

---

## GUIDED EXAMPLE

**Real code from procurement_automation.py (lines 61-99):**

```python
def setup_logging(config, env):
    # STEP 1: CREATE logger object
    logger = logging.getLogger("bell_procurement")
    
    # STEP 2: CONFIGURE - Set log level
    log_level = config.get("DEFAULT", "LOG_LEVEL")
    logger.setLevel(getattr(logging, log_level))
    
    # STEP 3: CONFIGURE - Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # STEP 4: CREATE and CONFIGURE file handler
    log_file = config.get(env.upper(), "LOG_FILE")
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(getattr(logging, log_level))
    file_handler.setFormatter(formatter)
    
    # STEP 5: CREATE and CONFIGURE console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # STEP 6: CONFIGURE - Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # STEP 7: RETURN - Ready to use
    return logger
```

**What's happening:**

**Create (Step 1):**
```python
logger = logging.getLogger("bell_procurement")
```
- Create new logger object named "bell_procurement"

**Configure (Steps 2-6):**
```python
logger.setLevel(getattr(logging, log_level))
# Set: How verbose should logging be?
# INFO = show info messages, DEBUG = show more, WARNING = show less

formatter = logging.Formatter(...)
# Set: What should log message look like?

file_handler = logging.FileHandler(log_file)
# Set: Write logs to file at path log_file

console_handler = logging.StreamHandler(sys.stdout)
# Set: Also write logs to console (terminal)

logger.addHandler(file_handler)
logger.addHandler(console_handler)
# Set: Use both file and console handlers
```

**Return (Step 7):**
```python
return logger
```
- Return the fully configured logger
- Now ready to use: `logger.info("Message")`

---

## PRACTICE PROBLEM

**Your task:**
Write a setup function for database connection

```python
def setup_database(config, env):
    # STEP 1: CREATE database object
    db = Database()
    
    # STEP 2: CONFIGURE - Set connection string
    db_url = config.get("DATABASE", "URL")
    db.???  # Set the URL
    
    # STEP 3: CONFIGURE - Set timeout
    timeout = config.getint("DATABASE", "TIMEOUT")
    db.???  # Set timeout
    
    # STEP 4: CONFIGURE - Connect
    db.???  # Actually connect
    
    # STEP 5: RETURN
    return db
```

**Answer:**
```python
def setup_database(config, env):
    # STEP 1: CREATE database object
    db = Database()
    
    # STEP 2: CONFIGURE - Set connection string
    db_url = config.get("DATABASE", "URL")
    db.set_url(db_url)  # or db.url = db_url
    
    # STEP 3: CONFIGURE - Set timeout
    timeout = config.getint("DATABASE", "TIMEOUT")
    db.set_timeout(timeout)  # or db.timeout = timeout
    
    # STEP 4: CONFIGURE - Connect
    db.connect()  # Actually connect
    
    # STEP 5: RETURN
    return db
```

**Why this works:**
- Create object first (empty)
- Configure each part (add properties)
- Connect/finalize
- Return when ready
- Caller gets ready-to-use object

---

## SPOT IT IN REAL CODE

**Find these in procurement_automation.py:**

1. **Lines 61-99:** `setup_logging()` function
   - Create: Logger object
   - Configure: Level, formatter, handlers
   - Return: Configured logger

2. **Lines 100-150:** Other setup functions
   - Search for `def setup_` or `def create_`
   - Pattern: Create → Configure → Return

---

## YOUR JOB AT BELL

**Day 1 Scenario:**
Manager: "Make sure logger is set up before main code runs. Log to both file and console."

**What you do:**
1. Call `setup_logging(config, env)` at startup
2. Get back logger that's ready to use
3. Use throughout code: `logger.info("Message")`
4. Log goes to both file and console automatically

**Why this matters:**
- Setup happens once at startup
- Rest of code doesn't worry about setup
- Logger works correctly everywhere
- Easy to change setup in future (one function)

---

# PATTERNS 6-10: QUICK REFERENCE

## PATTERN 6: IF/ELSE CONDITIONAL

**What It Does:**
Make decisions: if condition is true, do A; else do B.

**Simple Example:**
```python
if supplier.risk_score > 70:
    flag_for_manual_review(supplier)
else:
    auto_approve(supplier)
```

**Your Job at Bell:**
Check supplier data, make different decisions based on values.

---

## PATTERN 7: DICTIONARY/OBJECT ACCESS

**What It Does:**
Get values from dictionaries or objects.

**Safe vs Risky:**
```python
# SAFE: Returns None if key missing
name = supplier.get("name")

# RISKY: Crashes if key missing
name = supplier["name"]
```

**Your Job at Bell:**
Access supplier fields like DUNS, risk score, spend.

---

## PATTERN 8: STRING FORMATTING

**What It Does:**
Build strings by putting values into templates.

**Modern Way:**
```python
message = f"Supplier {name} has risk score {risk_score}"
```

**Your Job at Bell:**
Create error messages, log messages, reports.

---

## PATTERN 9: LIST/DICT COMPREHENSION

**What It Does:**
Create new list/dict by transforming existing one (one line).

**Comprehension:**
```python
supplier_names = [s["name"] for s in suppliers]
```

**vs Traditional Loop:**
```python
supplier_names = []
for s in suppliers:
    supplier_names.append(s["name"])
```

**Your Job at Bell:**
Extract fields, filter suppliers, create lookup dictionaries.

---

## PATTERN 10: FUNCTION WITH RETURN VALUE

**What It Does:**
Function does work, returns result.

**Example:**
```python
def calculate_risk_score(supplier):
    score = supplier["rating"] * 10
    return score

risk = calculate_risk_score(supplier)  # Returns number
```

**Your Job at Bell:**
Calculate scores, validate data, transform information.

---

# FINAL TIPS

## When You're Confused

**If you don't understand a pattern:**

1. **Re-read the UNDERSTAND section**
   - Read slowly, sentence by sentence
   - Understand WHY before HOW

2. **Study the GUIDED EXAMPLE**
   - See how it works in real code
   - Understand each step

3. **Try the PRACTICE PROBLEM**
   - Fill in blanks
   - Compare your answer
   - Do you understand why it works?

4. **SPOT IT in real code**
   - Find actual examples
   - See it in context
   - Connect to your job

## Remember

**Your job is NOT to be a Python expert.**

Your job is to:
- ✅ Recognize patterns
- ✅ Understand what they do
- ✅ Know when to use them
- ✅ Know where they are in code

**That's enough to do your job at Bell.**

---

# QUICK REFERENCE: ALL 10 PATTERNS

| Pattern | What It Does | Where in Code | Your Job |
|---------|---|---|---|
| 1. Configuration | Read settings from file | Lines 71-120 | Deploy to different environments |
| 2. Validation | Check data is correct | Lines 517-560 | Keep bad data out of database |
| 3. Loop/Transform | Process multiple items | Lines 387-419 | Clean 250 suppliers |
| 4. Error Handling | Handle failures gracefully | Lines 806-957 | Don't crash on one bad supplier |
| 5. Create/Configure | Setup complex objects | Lines 61-99 | Set up logger, database at startup |
| 6. Conditional | Make decisions | Throughout | Different actions for high-risk suppliers |
| 7. Dict Access | Get values from objects | Throughout | Read supplier fields safely |
| 8. String Format | Build strings | Throughout | Create error/log messages |
| 9. Comprehension | Transform lists (short) | Throughout | Extract fields, filter data |
| 10. Return Value | Function returns result | Throughout | Reusable functions everywhere |

---

**Now you understand how patterns work. The rest is recognition and practice.**

Go find these patterns in your code. You've got this. 🚀

