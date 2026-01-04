# Pattern 3: Loop & Transform - Practice Variations

**Learn by doing. Write, test, and master Pattern 3 with these 5 variations.**

Master loops by practicing different transformations on the same data.

---

## 📊 Base Data (Use for All Variations)

```python
suppliers = [
    {"name": "Boeing", "duns": "123456789", "risk": 2},
    {"name": "Airbus", "duns": "987654321", "risk": 1},
    {"name": "Lockheed", "duns": "555666777", "risk": 3},
    {"name": "Raytheon", "duns": "111222333", "risk": 2},
    {"name": "Northrop", "duns": "444555666", "risk": 4}
]
```

---

## 🎯 Variation 1: Extract Single Field (Names)

**What it does:** Get just the names  
**Goal:** `["Boeing", "Airbus", "Lockheed", "Raytheon", "Northrop"]`

**Your code:**
```python
# Method 1: Traditional loop
supplier_names = []
for s in suppliers:
    # YOUR CODE HERE
    pass

print(supplier_names)

# Method 2: List comprehension
supplier_names = [??? for ??? in ???]
print(supplier_names)
```

**Test it:** Run your code. Do you get the expected list?

---

## 🎯 Variation 2: Transform Field (Uppercase Names)

**What it does:** Get names but uppercase them  
**Goal:** `["BOEING", "AIRBUS", "LOCKHEED", "RAYTHEON", "NORTHROP"]`

**Your code:**
```python
# Method 1: Traditional loop
supplier_names_upper = []
for s in suppliers:
    # YOUR CODE HERE
    pass

print(supplier_names_upper)

# Method 2: List comprehension
supplier_names_upper = [??? for ??? in ???]
print(supplier_names_upper)
```

**Test it:** Run your code. Are all names uppercase?

---

## 🎯 Variation 3: Extract Multiple Fields as Tuples

**What it does:** Get name and duns as tuples  
**Goal:** `[("Boeing", "123456789"), ("Airbus", "987654321"), ...]`

**Your code:**
```python
# Method 1: Traditional loop
supplier_pairs = []
for s in suppliers:
    # YOUR CODE HERE
    pass

print(supplier_pairs)

# Method 2: List comprehension
supplier_pairs = [??? for ??? in ???]
print(supplier_pairs)
```

**Hint:** You can create tuples with `(value1, value2)`

**Test it:** Run your code. Do you get name-duns pairs?

---

## 🎯 Variation 4: Filter and Transform (High-Risk Suppliers)

**What it does:** Get names of suppliers with risk > 2  
**Goal:** `["Lockheed", "Northrop"]`

**Your code:**
```python
# Method 1: Traditional loop
high_risk_names = []
for s in suppliers:
    # Check if risk > 2
    # If yes, append the name
    # YOUR CODE HERE
    pass

print(high_risk_names)

# Method 2: List comprehension (with if)
high_risk_names = [??? for ??? in ??? if ???]
print(high_risk_names)
```

**Hint:** In list comprehensions, you can add `if condition` at the end

**Test it:** Run your code. Do you only get high-risk suppliers?

---

## 🎯 Variation 5: Complex Transform (Format for Report)

**What it does:** Create formatted strings for a report  
**Goal:** `["Boeing (123456789) - Risk: 2", "Airbus (987654321) - Risk: 1", ...]`

**Your code:**
```python
# Method 1: Traditional loop
report_lines = []
for s in suppliers:
    # Create formatted string like: "Name (duns) - Risk: X"
    # YOUR CODE HERE
    pass

print(report_lines)

# Method 2: List comprehension
report_lines = [f"??? (???) - Risk: ???" for ??? in ???]
print(report_lines)
```

**Hint:** Use f-strings: `f"Name: {value}"`

**Test it:** Run your code. Do you get formatted report lines?

---

## 📝 Study Guide

### For Each Variation:

1. **Read the description** - What are we transforming?
2. **Look at the goal** - What should the output be?
3. **Write Method 1** - Traditional loop (easier to understand)
4. **Test it** - Run and verify it works
5. **Write Method 2** - List comprehension (same result, one line)
6. **Test it** - Run and verify it works
7. **Compare** - Do both methods produce the same result?

### Progressive Difficulty:

- ✅ **Variation 1:** Basic extraction (easiest)
- ✅ **Variation 2:** Add method chaining (`.upper()`)
- ✅ **Variation 3:** Multiple fields at once
- ✅ **Variation 4:** Add filtering logic (if statement)
- ✅ **Variation 5:** Format complex strings (f-strings)

---

## 🧪 How to Test Your Code

**Quick test in terminal:**

```bash
# Create a file: test_variations.py
# Paste one variation into it
# Run it:
python test_variations.py

# You should see output like:
# ['Boeing', 'Airbus', 'Lockheed', 'Raytheon', 'Northrop']
```

---

## 💡 Tips

1. **Don't skip Method 1** - It teaches you how loops work
2. **Test after each variation** - See if it works
3. **If it breaks, read the error** - Errors tell you what's wrong
4. **Try to break it** - What if you change the data? What if risk is 2.5?
5. **Compare with classmates** - Different ways to write the same thing

---

## ✅ Success Checklist

- [ ] Variation 1 works (both methods)
- [ ] Variation 2 works (both methods)
- [ ] Variation 3 works (both methods)
- [ ] Variation 4 works (both methods)
- [ ] Variation 5 works (both methods)
- [ ] You understand why Method 1 and 2 produce same result
- [ ] You could write a new variation on your own

**If all checked:** You've mastered Pattern 3 ✅

---

## 📖 Reference

**Related sections in main guide:**
- [`PATTERNS_UNDERSTANDING_PRACTICE.md`](PATTERNS_UNDERSTANDING_PRACTICE.md) - Pattern 3 explanation
- [`procurement_automation.py`](../procurement_automation.py) - Real code examples (lines 387-419)

---

**Ready to practice?** Start with Variation 1. Test it. Then move to Variation 2. You've got this! 💪

