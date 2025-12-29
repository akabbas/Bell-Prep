# 10 Coding Patterns: Quick Visual Reference

**Print this out or bookmark it. You'll refer to this constantly.**

---

## The 10 Patterns at a Glance

```
┌─────────────────────────────────────────────────────────────┐
│  PATTERN 1: Configuration Reading                           │
├─────────────────────────────────────────────────────────────┤
│  Look For: config.get()                                     │
│  Purpose:  Read settings from file instead of hardcoding    │
│  Where:    Initialization, startup, setup functions        │
│  Example:  log_level = config.get("DEFAULT", "LOG_LEVEL")  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  PATTERN 2: Validation                                       │
├─────────────────────────────────────────────────────────────┤
│  Look For: if not, if x <, if x >, raise ValueError         │
│  Purpose:  Check if data is valid before using it           │
│  Where:    Data cleaning, input validation, before inserts  │
│  Example:  if len(duns) != 9: raise ValueError("Invalid")   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  PATTERN 3: Loop and Transform                              │
├─────────────────────────────────────────────────────────────┤
│  Look For: for x in, append(), list comprehensions          │
│  Purpose:  Process each item in a list                      │
│  Where:    Data cleaning, batch processing                  │
│  Example:  [transform(x) for x in data]                     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  PATTERN 4: Error Handling (Try/Except)                     │
├─────────────────────────────────────────────────────────────┤
│  Look For: try:, except:, finally:                          │
│  Purpose:  Handle failures gracefully                       │
│  Where:    API calls, database ops, risky operations        │
│  Example:  try: db.save() except Error: handle()            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  PATTERN 5: Create/Configure/Return                         │
├─────────────────────────────────────────────────────────────┤
│  Look For: Create → Configure → Return flow                 │
│  Purpose:  Build and configure complex objects              │
│  Where:    Setup functions, factories, init code            │
│  Example:  obj = X(); obj.set(y); return obj                │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  PATTERN 6: If/Else Conditional                             │
├─────────────────────────────────────────────────────────────┤
│  Look For: if, elif, else                                   │
│  Purpose:  Make decisions based on conditions               │
│  Where:    Decision logic, branching                        │
│  Example:  if x: do_a() else: do_b()                        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  PATTERN 7: Dictionary/Object Access                        │
├─────────────────────────────────────────────────────────────┤
│  Look For: .get(), ["key"], .attribute                      │
│  Purpose:  Retrieve values from objects/dicts               │
│  Where:    Data access, field retrieval                     │
│  Example:  value = obj.get("field", default)                │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  PATTERN 8: String Formatting                               │
├─────────────────────────────────────────────────────────────┤
│  Look For: f"...", {variable}, .format()                    │
│  Purpose:  Build strings with variables                     │
│  Where:    Error messages, logging, reporting               │
│  Example:  f"Error: {error_msg} at {time}"                  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  PATTERN 9: List/Dict Comprehension                         │
├─────────────────────────────────────────────────────────────┤
│  Look For: [... for ... in ...], {... for ...}              │
│  Purpose:  Transform/filter lists in one line               │
│  Where:    Data filtering, extraction                       │
│  Example:  [s.name for s in suppliers if s.risk > 3]        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  PATTERN 10: Function with Return Value                     │
├─────────────────────────────────────────────────────────────┤
│  Look For: def, return                                      │
│  Purpose:  Reusable code that returns a result              │
│  Where:    Calculations, transformations, utility funcs     │
│  Example:  def calc(x): return x * 2                        │
└─────────────────────────────────────────────────────────────┘
```

---

## Pattern Recognition Flowchart

```
┌─ Reading from config file?
│  └─> PATTERN 1: Configuration Reading
│
├─ Checking if data is valid?
│  └─> PATTERN 2: Validation
│
├─ Looping over items and processing each one?
│  └─> PATTERN 3: Loop and Transform
│
├─ Handling errors gracefully?
│  └─> PATTERN 4: Error Handling
│
├─ Building an object step by step?
│  └─> PATTERN 5: Create/Configure/Return
│
├─ Making a decision (if/else)?
│  └─> PATTERN 6: Conditional
│
├─ Getting a value from an object/dict?
│  └─> PATTERN 7: Dictionary/Object Access
│
├─ Building a string with variables?
│  └─> PATTERN 8: String Formatting
│
├─ Filtering/transforming a list in one line?
│  └─> PATTERN 9: List/Dict Comprehension
│
└─ Calculating something and returning it?
   └─> PATTERN 10: Function with Return Value
```

---

## Bell Textron Pattern Priority

### CRITICAL (Start Here)
1. **Configuration Reading** - Every app uses it
2. **Validation** - Prevents bad data
3. **Loop and Transform** - Process 250+ suppliers

### IMPORTANT (Learn Next)
4. **Error Handling** - When things go wrong
5. **Create/Configure/Return** - Setup code

### USEFUL (Learn After)
6. **Conditional** - Make decisions
7. **Dict/Object Access** - Get data
8. **String Formatting** - Build messages
9. **Comprehension** - Transform data
10. **Return Value** - Functions

---

## Pattern Complexity Levels

```
EASIEST (Start Here):
├─ String Formatting (just adding variables to text)
├─ Dictionary Access (just getting values)
└─ Conditional (simple if/else)

MODERATE (Next):
├─ Configuration Reading (understanding config files)
├─ Validation (multiple checks)
├─ Return Value (functions)
└─ Loop and Transform (for loops)

HARDER (Later):
├─ Error Handling (try/except logic)
├─ Create/Configure/Return (multi-step process)
└─ Comprehension (one-liner thinking)
```

---

## Pattern Frequency in Bell Code

```
How often you'll see each pattern:

PATTERN 1: Config Reading        ████████░░ 80%
PATTERN 2: Validation            ███████░░░ 70%
PATTERN 3: Loop Transform        ███████░░░ 70%
PATTERN 4: Error Handling        ██████░░░░ 60%
PATTERN 5: Create/Configure      █████░░░░░ 50%
PATTERN 6: Conditional           ███████░░░ 70%
PATTERN 7: Dict Access           ████████░░ 80%
PATTERN 8: String Format         ██████░░░░ 60%
PATTERN 9: Comprehension         ████░░░░░░ 40%
PATTERN 10: Return Value         ██████░░░░ 60%
```

**Interpretation:** Patterns 1, 2, 3, 6, 7 are EVERYWHERE. Master those first.

---

## Quick Decision Matrix

**When you see code and need to understand it, ask:**

| Question | Pattern |
|----------|---------|
| "Where is this value coming from?" | 1 or 7 |
| "Why does this fail here?" | 2 or 4 |
| "What happens to each item?" | 3 or 9 |
| "How is the error handled?" | 4 |
| "How is this object set up?" | 5 |
| "Which path does this take?" | 6 |
| "How is this text built?" | 8 |
| "What does this function return?" | 10 |

---

## "I'm Confused" Troubleshooting Guide

**"I don't understand this code"**

Step 1: Identify the pattern (use flowchart above)
Step 2: Look up that pattern in CODING_PATTERNS_GUIDE.md
Step 3: Find an example of that pattern in your code
Step 4: Compare the example to the confusing code
Step 5: Now you understand

**Works 90% of the time.**

---

## Study Recommendation

### If You Have 1 Week
Focus on: 1, 2, 3, 6, 7

### If You Have 2 Weeks
Focus on: 1, 2, 3, 4, 5, 6, 7

### If You Have 3 Weeks
Focus on: All 10 patterns

### If You Have 4+ Weeks
Focus on: All 10 patterns + practice writing them

---

## Red Flags: Patterns You're Struggling With

**If you don't understand Pattern 1:**
- Read config.ini file directly
- Trace a config.get() call step by step
- Run the code with print statements

**If you don't understand Pattern 2:**
- Find validation in your code
- List each check
- Ask "what happens if this fails?"

**If you don't understand Pattern 3:**
- Compare traditional loop vs comprehension
- Start with traditional loops first
- Learn comprehensions later

**If you don't understand Pattern 4:**
- Understand what "risky" means (API calls, DB inserts)
- Understand what errors it's catching
- Ask "what's the fallback?"

**If you don't understand Pattern 5:**
- Trace through setup_logging() line by line
- See: Create → Configure → Return
- Map each line to a step

---

## Your Pattern Learning Checklist

As you study each pattern, check off:

### Pattern 1: Configuration Reading
- [ ] I can recognize this pattern
- [ ] I understand why it's used
- [ ] I found examples in my code
- [ ] I could explain it to someone
- [ ] I could write a simple example
- [ ] Ready to move on: Y/N

### Pattern 2: Validation
- [ ] I can recognize this pattern
- [ ] I understand why it's used
- [ ] I found examples in my code
- [ ] I could explain it to someone
- [ ] I could write a simple example
- [ ] Ready to move on: Y/N

### Pattern 3: Loop and Transform
- [ ] I can recognize this pattern
- [ ] I understand why it's used
- [ ] I found examples in my code
- [ ] I could explain it to someone
- [ ] I could write a simple example
- [ ] Ready to move on: Y/N

**[Repeat for Patterns 4-10]**

---

## Things to Remember

✅ **DO:**
- Start with patterns 1-3
- Find examples in your code
- Write your own small examples
- Ask for help if confused

❌ **DON'T:**
- Try to memorize syntax
- Skip patterns
- Try to learn all 10 at once
- Feel bad if it takes time

---

## Success Indicators

**You're ready when you can:**
- ✅ Point to code and say "that's Pattern 3"
- ✅ Explain what each pattern does
- ✅ Find 3 examples of each pattern
- ✅ Write basic code using patterns
- ✅ Read uncommented code without panicking

**You're REALLY ready when you:**
- ✅ See new code and instantly recognize patterns
- ✅ Know why that pattern was chosen
- ✅ Can modify it confidently
- ✅ Understand edge cases

---

## Next Steps

1. **Today:** Read patterns 1-3 in CODING_PATTERNS_GUIDE.md
2. **Tomorrow:** Complete exercises for patterns 1-3 in PATTERNS_PRACTICE_WORKBOOK.md
3. **Next:** Find each pattern in your actual code
4. **Then:** Read patterns 4-5
5. **After:** Read patterns 6-10
6. **Finally:** Practice recognition quiz daily

**Timeline: Complete by Jan 12**

---

## Emergency Reference

**Stuck on a pattern? Quick lookup:**

```
Pattern 1? → See lines 71-72 in procurement_automation.py
Pattern 2? → See lines 517-540 in procurement_automation.py
Pattern 3? → See lines 387-419 in procurement_automation.py
Pattern 4? → See lines 806-957 in procurement_automation.py
Pattern 5? → See lines 61-99 in procurement_automation.py
```

---

**You've got this. Start with pattern 1. You'll be fluent by Jan 12.**

