# 14-Day Coding Patterns Study Plan

**Your countdown to Bell Textron. Complete this by January 12.**

---

## Overview

- **Total Days:** 14 days until January 12
- **Study Time:** 1-2 hours per day
- **Goal:** Master 10 coding patterns
- **Outcome:** Understand 80% of Bell's codebase

---

## Days 1-3: Pattern 1 (Configuration Reading)

### Day 1: Learn Pattern 1

**Time:** 45 minutes

**Tasks:**
1. Read: CODING_PATTERNS_GUIDE.md → Pattern 1 section (15 min)
2. Understand: What config.get() does
3. Find: 3 examples in procurement_automation.py
4. Record: Write line numbers and what each reads

**What to do:**
- Open procurement_automation.py
- Search for "config.get"
- For each one found:
  - Note the line number
  - Note what value is being read
  - Note why (what's it used for)

**Success:** Can you explain what config.get() does? Y/N

---

### Day 2: Practice Pattern 1

**Time:** 45 minutes

**Tasks:**
1. Complete: Exercise 1, Task 1 in PATTERNS_PRACTICE_WORKBOOK.md
2. Write: Your own config.get() examples
3. Find: 3 more config.get() calls if they exist
4. Test: Can you find where config.ini is used?

**Hands-on:**
- Open config.ini
- Look at the [DEFAULT], [DEV], [PROD] sections
- Understand: Different configs for different environments
- Trace: Find where these are read in procurement_automation.py

**Success:** Can you read a value from config? Y/N

---

### Day 3: Master Pattern 1

**Time:** 30 minutes

**Tasks:**
1. Review: Pattern 1 section in PATTERNS_QUICK_REFERENCE.md
2. Quiz: Check yourself - can you spot Pattern 1?
3. Connect: Why does Bell use configuration instead of hardcoding?
4. Ready: Move on? Y/N

**Deeper Thinking:**
- Why would Bell need different settings for dev/test/prod?
- What would happen if database URL was hardcoded?
- How does config help with security?

**Success:** Ready to move to Pattern 2? Y/N

---

## Days 4-6: Pattern 2 (Validation)

### Day 4: Learn Pattern 2

**Time:** 1 hour

**Tasks:**
1. Read: CODING_PATTERNS_GUIDE.md → Pattern 2 section (20 min)
2. Study: The _validate_duns_number() function (lines 517-540)
3. Trace: Each validation check step by step
4. Record: What each check does

**What to understand:**
- First check: Is DUNS empty?
- Second check: Does it contain only numbers?
- Third check: Is it exactly 9 digits?
- Fourth check: Return cleaned version

**Success:** Can you list all 4 validation checks? Y/N

---

### Day 5: Practice Pattern 2

**Time:** 1 hour

**Tasks:**
1. Complete: Exercise 1, Task 2 in PATTERNS_PRACTICE_WORKBOOK.md
2. Find: 3 more validation patterns in your code
3. Understand: Why each validation is important
4. Write: Your own simple validation function

**Write your own:**
```python
def validate_percentage(value):
    # Check if value is numeric
    # Check if value is between 0 and 100
    # Return cleaned value or raise error
    pass
```

**Success:** Can you write a validation function? Y/N

---

### Day 6: Master Pattern 2

**Time:** 30 minutes

**Tasks:**
1. Review: Pattern 2 in PATTERNS_QUICK_REFERENCE.md
2. Quiz: Identify 3 validation patterns in your code
3. Connect: Why is DUNS validation important for Bell?
4. Ready: Move on? Y/N

**Real Bell Connection:**
- DUNS numbers identify suppliers
- Wrong DUNS = wrong supplier = wrong contract
- Validation prevents disasters

**Success:** Ready for Pattern 3? Y/N

---

## Days 7-9: Pattern 3 (Loop and Transform)

### Day 7: Learn Pattern 3

**Time:** 1 hour

**Tasks:**
1. Read: CODING_PATTERNS_GUIDE.md → Pattern 3 section
2. Study: clean_suppliers() function (lines 387-419)
3. Understand: What's being looped? What's the output?
4. Trace: Each supplier through the cleaning process

**Key concepts:**
- Input: Raw 250 suppliers from API
- Loop: For each supplier...
- Transform: Clean and validate it
- Output: Cleaned list + error list

**Success:** Can you trace one supplier through cleaning? Y/N

---

### Day 8: Practice Pattern 3

**Time:** 1 hour

**Tasks:**
1. Complete: Exercise 1, Task 3 in PATTERNS_PRACTICE_WORKBOOK.md
2. Find: 2 more loop patterns in your code
3. Learn: List comprehensions (simpler version of loops)
4. Compare: Traditional loop vs comprehension

**Traditional loop:**
```python
names = []
for s in suppliers:
    names.append(s.name)
```

**Comprehension:**
```python
names = [s.name for s in suppliers]
```

**Both do the same thing. Comprehension is shorter.**

**Success:** Can you write both styles? Y/N

---

### Day 9: Master Pattern 3

**Time:** 45 minutes

**Tasks:**
1. Review: Pattern 3 in PATTERNS_QUICK_REFERENCE.md
2. Quiz: Spot 3 loop patterns in your code
3. Connect: How would Bell process 250 suppliers without loops?
4. Ready: Move on? Y/N

**Real scenario:**
- Bell gets 250 suppliers from Ariba
- Each needs cleaning and validation
- Loop processes all 250 automatically

**Success:** Ready for Pattern 4? Y/N

---

## Days 10-11: Pattern 4 (Error Handling)

### Day 10: Learn Pattern 4

**Time:** 1 hour

**Tasks:**
1. Read: CODING_PATTERNS_GUIDE.md → Pattern 4 section
2. Study: Error handling in upsert_suppliers() (lines 806-957)
3. Understand: What could go wrong? What catches it?
4. Trace: What happens when IntegrityError occurs?

**Key concepts:**
- try: The risky operation (insert/update)
- except: What to do if it fails
- Continue: Process next supplier instead of crashing

**Success:** Can you trace an error through handling? Y/N

---

### Day 11: Practice Pattern 4

**Time:** 1 hour

**Tasks:**
1. Complete: Exercise 1, Task 4 in PATTERNS_PRACTICE_WORKBOOK.md
2. Find: 2 more error handling patterns
3. Write: Your own try/except example
4. Understand: Why we don't want crashes

**Your scenario:**
- What if 1 of 250 suppliers has bad data?
- Without try/except: Program crashes, nothing is saved
- With try/except: Log error, skip that one, continue

**Success:** Ready for Pattern 5? Y/N

---

## Days 12-13: Pattern 5 (Create/Configure/Return)

### Day 12: Learn Pattern 5

**Time:** 1 hour

**Tasks:**
1. Read: CODING_PATTERNS_GUIDE.md → Pattern 5 section
2. Study: setup_logging() (lines 61-99) - this is the PERFECT example
3. Map: Each step of the setup
4. Trace: From creation to return

**The pattern:**
- Create: New logger object
- Configure: Add handlers, set formatter
- Configure: Add console handler
- Configure: Add file handler
- Return: Logger ready to use

**Success:** Can you map all steps? Y/N

---

### Day 13: Practice Pattern 5

**Time:** 1 hour

**Tasks:**
1. Complete: Exercise 1, Task 5 in PATTERNS_PRACTICE_WORKBOOK.md
2. Find: 1 other setup function in code
3. Map: Its steps (create, configure, return)
4. Write: Simple setup function

**Your scenario:**
```python
def setup_database():
    # Create
    db = Database()
    
    # Configure
    db.host = "localhost"
    db.port = 5432
    db.timeout = 30
    
    # Return
    return db
```

**Success:** Ready for Patterns 6-10? Y/N

---

## Days 14-17: Patterns 6-9 (Quick Learning)

### Day 14: Patterns 6 & 7

**Time:** 1 hour total

**Pattern 6 (Conditional):**
- Learn: if/else/elif
- Find: 5 examples in your code
- Key: Making decisions based on conditions

**Pattern 7 (Dict/Object Access):**
- Learn: .get() vs ["key"]
- Find: 5 examples in your code
- Key: Getting values safely

**Success:** Can you spot both? Y/N

---

### Day 15: Patterns 8 & 9

**Time:** 1 hour total

**Pattern 8 (String Formatting):**
- Learn: f-strings and .format()
- Find: 3 examples in your code
- Write: 2 of your own

**Pattern 9 (List Comprehension):**
- Learn: [x for x in list if condition]
- Find: 3 examples in your code
- Write: 2 of your own

**Success:** Can you use f-strings? Y/N

---

### Day 16: Pattern 10 & Review

**Time:** 1 hour

**Pattern 10 (Return Value):**
- Learn: Functions that return results
- Find: 5 examples in your code
- Key: Reusable code

**Review: Patterns 1-10**
- Can you name all 10? Y/N
- Can you recognize each in code? Y/N

**Success:** Ready for consolidation? Y/N

---

### Day 17: Recognition Quiz

**Time:** 1 hour

**Tasks:**
1. Complete: "Pattern Recognition Quiz" in PATTERNS_PRACTICE_WORKBOOK.md
2. Score: ___/10
3. Retake: Any you got wrong
4. Goal: 10/10

**Quiz again:**
For each code snippet, name the pattern.

**Success:** Score 10/10? Y/N

---

## Days 18-19: Final Consolidation

### Day 18: Real Bell Scenarios

**Time:** 1 hour

**Tasks:**
1. Complete: "Real Bell Scenarios" in PATTERNS_PRACTICE_WORKBOOK.md
2. For each scenario:
   - Identify the pattern needed
   - Write the code
   - Understand why that pattern
3. Consolidate learning

**Scenarios practiced:**
1. Reading configuration
2. Validating ITAR compliance
3. Processing 250 suppliers
4. Handling database insert errors
5. Setting up audit logging

**Success:** Can you code all 5 scenarios? Y/N

---

### Day 19: Final Review & Confidence Check

**Time:** 1 hour

**Tasks:**
1. Review: All 10 patterns one more time
2. Check: Can you recognize them in procurement_automation.py?
3. Self-assess: How confident are you? 1-10
4. Celebrate: You're ready for Bell!

**Self-Assessment:**
- [ ] I can recognize all 10 patterns
- [ ] I understand what each does
- [ ] I found examples of each
- [ ] I could write basic code using patterns
- [ ] I'm ready for Bell

**Confidence Level (1-10):** ___

---

## Daily Study Routine

### Each day, do this:

**Morning (15 min):**
1. Review yesterday's patterns
2. Spot patterns in your code from yesterday
3. Mental preparation for today

**Main Study (45-60 min):**
1. Read the pattern explanation
2. Find examples in your code
3. Complete exercises
4. Write your own examples

**Evening (15 min):**
1. Review what you learned
2. Check: Did you understand?
3. Prepare: What's tomorrow?

**Optional (15-30 min):**
1. Extra practice
2. Re-read confusing parts
3. Find more examples

---

## What to Study With

**Have open:**
- CODING_PATTERNS_GUIDE.md (reference)
- PATTERNS_QUICK_REFERENCE.md (quick lookup)
- PATTERNS_PRACTICE_WORKBOOK.md (exercises)
- procurement_automation.py (real examples)

**Keep nearby:**
- Notebook for notes
- Pen for writing
- Water

---

## Checkpoints

### End of Day 3
- [ ] Understand Pattern 1
- [ ] Can find config.get() calls
- [ ] Know why configuration matters

### End of Day 6
- [ ] Understand Pattern 2
- [ ] Can find validation patterns
- [ ] Know why validation matters

### End of Day 9
- [ ] Understand Pattern 3
- [ ] Can find loop patterns
- [ ] Know why loops matter

### End of Day 13
- [ ] Understand Patterns 4-5
- [ ] Can find error handling
- [ ] Can identify setup patterns

### End of Day 17
- [ ] Understand Patterns 6-10
- [ ] Can recognize all patterns
- [ ] Score 10/10 on recognition quiz

### End of Day 19
- [ ] Can recognize all patterns
- [ ] Can explain all patterns
- [ ] Feel confident for Bell
- [ ] Score ___/10 self-confidence

---

## Troubleshooting

**If a pattern is confusing:**
1. Re-read that section of CODING_PATTERNS_GUIDE.md
2. Find 3 real examples in your code
3. Trace through each example step-by-step
4. Write your own simple version
5. Ask for help if stuck

**If you're falling behind:**
1. Focus on patterns 1-5 first
2. Skip patterns 6-10 for now
3. Come back to them after
4. Better to understand 5 well than 10 poorly

**If you're ahead:**
1. Write more examples
2. Find more patterns in your code
3. Write real Bell scenarios
4. Help someone else learn

---

## Final Note

**January 12 is your deadline, but:**
- This isn't a race
- Understanding matters more than speed
- Better to spend 2 hours on 1 pattern than 10 minutes on 10
- You can continue learning after Jan 12

**Your goal:**
✅ Recognize patterns
✅ Understand them
✅ Apply them to your job

**You've got 19 days. You can do this.**

---

## Success Stories

**By the end of day 19, you'll be able to:**

✅ Open any Bell code and understand 80% immediately
✅ Recognize what's happening without comments
✅ Know which pattern to use for any problem
✅ Write code that follows Bell's style
✅ Debug code by understanding patterns
✅ Learn new code 10x faster

**That's the power of pattern recognition.**

---

## Celebrate These Wins

- **Day 3:** "I understand configuration!"
- **Day 6:** "I can write validation!"
- **Day 9:** "I can transform lists!"
- **Day 13:** "I can set up complex systems!"
- **Day 17:** "I recognize all patterns!"
- **Day 19:** "I'm ready for Bell!"

**You got this.** 🚀

