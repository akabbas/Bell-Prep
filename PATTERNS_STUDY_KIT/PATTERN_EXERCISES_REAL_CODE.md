# Pattern Recognition Exercises: Real Code Examples

**This document shows you REAL code snippets from Bell Textron systems and related work.**
**Your job: Identify which pattern(s) are used in each snippet.**

---

## Exercise Set 1: Real Procurement Code Examples

### Example 1.1: Reading Configuration

```python
def initialize_api_client(config):
    api_url = config.get("PROD", "API_BASE_URL")
    api_key = config.get("PROD", "API_KEY")
    timeout = config.getint("PROD", "API_TIMEOUT_SECONDS")
    
    client = APIClient(api_url, api_key, timeout)
    return client
```

**Questions:**
1. What pattern appears in lines 2-4?
   Answer: _______________

2. What's being read from where?
   Answer: _______________

3. Why not hardcode these values?
   Answer: _______________

4. What pattern appears in lines 6-7?
   Answer: _______________

---

### Example 1.2: Supplier Data Processing

```python
def process_suppliers(suppliers):
    cleaned = []
    errors = []
    
    for supplier in suppliers:
        try:
            # Validate DUNS
            if not supplier.get('duns'):
                raise ValueError("DUNS missing")
            
            duns = supplier['duns'].replace('-', '').strip()
            if len(duns) != 9:
                raise ValueError("Invalid DUNS length")
            
            if not duns.isdigit():
                raise ValueError("Non-numeric DUNS")
            
            supplier['duns'] = duns
            cleaned.append(supplier)
        
        except ValueError as e:
            errors.append({
                'supplier_id': supplier.get('id'),
                'error': str(e)
            })
    
    return cleaned, errors
```

**Questions:**
1. What pattern is used in line 5 (`for supplier in suppliers:`)?
   Answer: _______________

2. What patterns are used in lines 8-16?
   Answer: _______________ and _______________

3. What pattern is used in lines 18-24?
   Answer: _______________

4. How many different checks are validating the DUNS?
   Answer: _____ (list them)
   - _____________________
   - _____________________
   - _____________________

---

### Example 1.3: Logging Setup

```python
def setup_audit_logger(log_dir, environment):
    # Create logger
    audit_logger = logging.getLogger("bell_audit")
    audit_logger.setLevel(logging.INFO)
    
    # Configure file handler
    log_file = f"{log_dir}/audit_{environment}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(
        logging.Formatter('%(asctime)s | %(message)s')
    )
    
    # Add handler
    audit_logger.addHandler(file_handler)
    
    # Return configured logger
    return audit_logger
```

**Questions:**
1. What pattern is this entire function?
   Answer: _______________

2. Map the steps:
   - Create (line ___): _______________
   - Configure (lines ___-___): _______________
   - Return (line ___): _______________

3. What pattern in line 6?
   Answer: _______________

---

## Exercise Set 2: Decision Making Code

### Example 2.1: Conditional Processing

```python
def process_supplier(supplier, environment):
    # Read config
    high_risk_threshold = config.getint(environment, "HIGH_RISK_THRESHOLD")
    
    # Make decision
    if supplier['spend'] > high_risk_threshold:
        if supplier['risk_score'] > 3:
            flag_for_compliance_review(supplier)
        else:
            add_to_high_spend_list(supplier)
    else:
        add_to_normal_list(supplier)
```

**Questions:**
1. What pattern is in line 3?
   Answer: _______________

2. What pattern is in lines 6-11?
   Answer: _______________

3. How many decisions are being made?
   Answer: _____

4. Rewrite lines 6-11 using a different structure (bonus):
   Answer: _______________

---

### Example 2.2: Data Access and Conditional

```python
def validate_itar_status(supplier):
    # Safely get value
    is_itar = supplier.get('itar_compliant', False)
    
    # Make decision based on value
    if is_itar:
        log_itar_access(supplier)
        return True
    else:
        log_warning(f"Non-ITAR supplier: {supplier.get('name', 'Unknown')}")
        return False
```

**Questions:**
1. What pattern is in line 3?
   Answer: _______________

2. What pattern is in line 9?
   Answer: _______________

3. Why use `.get()` instead of direct access?
   Answer: _______________

4. What patterns appear in lines 6-11?
   Answer: _______________ and _______________

---

## Exercise Set 3: Data Transformation

### Example 3.1: List Transformation

```python
# Get high-risk suppliers
all_suppliers = fetch_suppliers()
high_risk = [s for s in all_suppliers if s['risk_score'] > 3]

# Extract names
names = [s['name'] for s in high_risk]

# Create lookup dict
lookup = {s['id']: s['name'] for s in high_risk}

# Filter and transform
critical_suppliers = [
    {
        'name': s['name'],
        'duns': s['duns'],
        'risk': s['risk_score']
    }
    for s in all_suppliers
    if s['spend_ytd'] > 500000
]
```

**Questions:**
1. What pattern is used in line 3?
   Answer: _______________

2. What pattern is used in line 6?
   Answer: _______________

3. What pattern is used in line 9?
   Answer: _______________

4. What patterns are used in lines 11-19?
   Answer: _______________ and _______________

---

### Example 3.2: Loop with Transformation and Error Handling

```python
def clean_and_save_suppliers(suppliers, db):
    results = {
        'saved': 0,
        'skipped': 0,
        'errors': []
    }
    
    for supplier in suppliers:
        try:
            # Validate
            if not supplier.get('duns'):
                raise ValueError("DUNS required")
            
            # Transform
            clean = {
                'duns': supplier['duns'].upper(),
                'name': supplier['name'].title(),
                'spend': float(supplier.get('spend', 0))
            }
            
            # Save
            db.insert(clean)
            results['saved'] += 1
        
        except ValueError as e:
            results['errors'].append(str(e))
            results['skipped'] += 1
    
    return results
```

**Questions:**
1. What pattern is in line 8?
   Answer: _______________

2. What pattern is in lines 10-12?
   Answer: _______________

3. What pattern is in lines 14-18?
   Answer: _______________

4. What pattern is in lines 25-27?
   Answer: _______________

5. Name ALL patterns used in this function:
   Answer: _______________, _______________, _______________, _______________

---

## Exercise Set 4: Bell-Specific Scenarios

### Example 4.1: ITAR Compliance Logging

```python
def log_itar_transaction(supplier, action):
    timestamp = datetime.now()
    
    log_entry = f"""
    ITAR Access Log
    ===============
    Supplier: {supplier['name']}
    DUNS: {supplier['duns']}
    Action: {action}
    Timestamp: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}
    """
    
    itar_logger.info(log_entry)
    
    try:
        itar_db.insert({
            'supplier_id': supplier['id'],
            'action': action,
            'timestamp': timestamp
        })
    except Exception as e:
        itar_logger.error(f"Failed to log ITAR: {str(e)}")
```

**Questions:**
1. What pattern is in lines 4-11?
   Answer: _______________

2. What pattern is in lines 14-20?
   Answer: _______________

3. Name all patterns in this function:
   Answer: _______________, _______________, _______________

---

### Example 4.2: Supplier Risk Assessment

```python
def assess_supplier_risk(supplier, config):
    # Read thresholds
    high_spend = config.getint("RISK", "HIGH_SPEND_THRESHOLD")
    high_risk_score = config.getint("RISK", "HIGH_RISK_SCORE")
    
    # Get supplier data safely
    spend = supplier.get('spend_ytd', 0)
    risk_score = supplier.get('risk_score', 0)
    is_itar = supplier.get('itar_compliant', False)
    
    # Assess risk
    if risk_score >= high_risk_score and spend > high_spend:
        risk_level = "CRITICAL"
    elif risk_score >= high_risk_score or spend > high_spend:
        risk_level = "HIGH"
    elif is_itar and spend > high_spend * 0.5:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"
    
    return risk_level
```

**Questions:**
1. What pattern is in lines 3-4?
   Answer: _______________

2. What pattern is in lines 7-9?
   Answer: _______________

3. What pattern is in lines 12-19?
   Answer: _______________

4. How many decision paths are there?
   Answer: _____

5. Name all patterns:
   Answer: _______________, _______________, _______________

---

## Exercise Set 5: API Integration

### Example 5.1: API Call with Error Handling

```python
def fetch_supplier_data(api_client, page=1):
    try:
        # Make API call
        endpoint = f"/suppliers?page={page}&size=50"
        response = api_client.get(endpoint)
        
        # Check response
        if response.status_code != 200:
            raise ValueError(f"API error: {response.status_code}")
        
        # Parse and return
        data = response.json()
        return data.get('suppliers', [])
    
    except requests.ConnectionError as e:
        logger.error(f"Connection failed: {str(e)}")
        return []
    
    except Exception as e:
        logger.critical(f"Unexpected error: {str(e)}")
        raise
```

**Questions:**
1. What pattern is in line 4?
   Answer: _______________

2. What pattern is in lines 2-20?
   Answer: _______________

3. How many error cases are handled?
   Answer: _____ (list them)
   - _____________________
   - _____________________

---

## Exercise Set 6: Spot the Pattern (Harder)

### Challenge 1: Complex Function

```python
def import_suppliers(config, environment):
    # Setup
    api_key = config.get(environment, "API_KEY")
    db = setup_database(config, environment)
    logger = setup_logger(config, environment)
    
    # Fetch
    logger.info("Fetching suppliers...")
    suppliers = fetch_from_api(api_key)
    
    # Clean and save
    for supplier in suppliers:
        try:
            if not validate_supplier(supplier):
                skip_supplier(supplier)
                continue
            
            cleaned = clean_supplier(supplier)
            db.save(cleaned)
            logger.info(f"Saved: {cleaned['name']}")
        
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            continue
    
    logger.info("Import complete")
    return db
```

**Pattern Count:**
- How many different patterns are used?
  Answer: _____

**Name them:**
1. _____________________
2. _____________________
3. _____________________
4. _____________________
5. _____________________

---

## Answer Key

**Example 1.1:**
1. Pattern 1 (Configuration Reading)
2. API_BASE_URL, API_KEY, API_TIMEOUT_SECONDS from PROD config
3. So settings can change without redeploying
4. Pattern 5 (Create/Configure/Return)

**Example 1.2:**
1. Pattern 3 (Loop and Transform)
2. Pattern 2 (Validation) and Pattern 6 (Conditional)
3. Pattern 4 (Error Handling)
4. Three checks: Empty check, Length check, Digit check

**Example 1.3:**
1. Pattern 5 (Create/Configure/Return)
2. Lines 3: logger creation; Lines 6-12: handler creation and configuration; Line 15: return
3. Pattern 8 (String Formatting)

**Example 2.1:**
1. Pattern 1 (Configuration Reading)
2. Pattern 6 (If/Else Conditional)
3. Multiple nested decisions

**Example 2.2:**
1. Pattern 7 (Dictionary/Object Access)
2. Pattern 8 (String Formatting)
3. Prevent crashes when key doesn't exist
4. Pattern 6 (Conditional) and Pattern 8 (String Formatting)

**Example 3.1:**
1. Pattern 9 (List/Dict Comprehension)
2. Pattern 9 (List/Dict Comprehension)
3. Pattern 9 (Dict Comprehension)
4. Pattern 9 (Comprehension with filtering) and Pattern 3 (Loop/Transform)

**Example 3.2:**
1. Pattern 3 (Loop and Transform)
2. Pattern 2 (Validation)
3. Pattern 3 (Loop/Transform) - transforming data
4. Pattern 4 (Error Handling)
5. All four: Loop, Validation, Transformation, Error Handling

**Example 4.1:**
1. Pattern 8 (String Formatting)
2. Pattern 4 (Error Handling)
3. Three: String Formatting, Error Handling, Dictionary/Object Access

**Example 4.2:**
1. Pattern 1 (Configuration Reading)
2. Pattern 7 (Dictionary/Object Access)
3. Pattern 6 (If/Else Conditional)
4. Four paths: CRITICAL, HIGH, MEDIUM, LOW
5. Three: Configuration Reading, Dictionary Access, Conditional

**Example 5.1:**
1. Pattern 8 (String Formatting)
2. Pattern 4 (Error Handling)
3. Two: ConnectionError, generic Exception

**Challenge 1:**
Count: 8 patterns
1. Configuration Reading
2. Create/Configure/Return (for db, logger)
3. Loop and Transform
4. Validation
5. Conditional
6. Error Handling
7. String Formatting
8. Dictionary/Object Access

---

## Self-Scoring

**Count your correct answers:**

- 20+ correct: Excellent! You're ready.
- 15-19 correct: Good! Almost there.
- 10-14 correct: Making progress. Keep studying.
- 5-9 correct: Keep going. Practice more.
- 0-4 correct: Review patterns 1-3 again.

---

## Next Steps

1. **Today:** Complete this exercise
2. **Score yourself**
3. **Re-read patterns you missed**
4. **Do exercises again** (answers second time don't count)
5. **You're ready when:** Score 20+

---

**This is exactly what you'll do at Bell.**

On your first day, your manager will show you code. You won't understand every line. But you WILL recognize patterns. That's enough to get started.

**You can do this.** 🚀

