# Your 50/50 Job Prep Guide

**Tech + Business. Everything you need.**

---

## The Job: 50% Technology, 50% Business

Your role bridges two worlds. You need to understand both.

---

## 🔧 Technical Skills (50%)

### Week 1: Master the 10 Patterns
**File:** `PATTERNS_STUDY_KIT/PATTERNS_UNDERSTANDING_PRACTICE.md`  
**Time:** 8-10 hours total

**Patterns you'll see every day:**
1. **Configuration Reading** - Systems know where to connect
2. **Validation** - Making sure data is correct
3. **Loop & Transform** - Process many suppliers at once
4. **Error Handling** - What happens when things break
5. **Create/Configure/Return** - Build objects properly
6-10. **Support patterns** - Less common but still important

**Why:** You'll write code using these patterns. Understanding them = writing better code faster.

### Week 2: Get Comfortable with Tools
**Terminal, Python, APIs, Databases**
- `TERMINAL_COMMANDS_GUIDE.md` (1-2 hrs)
- Run `procurement_automation.py` yourself
- See the flow: fetch → clean → validate → store

**Why:** Day 1, someone will ask "Can you run the import?" You need to be comfortable.

---

## 💼 Business Skills (50%)

### Before Week 1: Understand the Context
**File:** `JOB_DESCRIPTION.md`  
**Time:** 15 minutes

**What you're actually doing:**
- Bringing supplier data from SAP Ariba into Bell's system
- Cleaning it so it's trustworthy
- Checking compliance (ITAR, AS9100)
- Flagging risky suppliers
- Recording everything for audit

### Throughout Your Study: Business Concepts

**DUNS Number** (Unique supplier ID)
- You'll validate these in Pattern 2 (Validation)
- Must be exactly 9 digits
- Suppliers without it = can't do business

**ITAR Compliance** (Export Control)
- Bell is defense/aerospace = export control matters
- Some suppliers can't sell to certain countries
- You'll LOG every access to these suppliers
- Government audits this

**AS9100 Certification** (Aerospace Quality)
- Defense contractors must have this
- Missing it = red flag
- You'll check for this and flag if missing

**Risk Scoring** (Which Suppliers Matter)
- High spend + high risk = needs attention
- Old audits (90+ days) = might need fresh review
- Pattern 3 (Loop & Transform) will calculate these

**Performance Scoring** (How They Perform)
- On-time delivery: 40% weight
- Quality: 30% weight
- Cost: 20% weight
- Risk: 10% weight
- You'll calculate this in Pattern 5

### Day-to-Day Business Work

**You'll be asked:**
- "How many ITAR-compliant suppliers do we have?" (You'll query the database)
- "Which suppliers are high-risk?" (Pattern 3 logic)
- "Can we use this supplier?" (Check DUNS, ITAR, AS9100, risk)
- "Why did that import fail?" (Error handling, Pattern 4)
- "Show me the audit trail" (You logged it!)

---

## 🎯 How to Study (Tech + Business Together)

### Pattern 1: Configuration Reading

**Technical:** How systems connect to API  
**Business:** You're reading the SAP Ariba API configuration

**Real scenario:** "The import ran but no data came in"  
→ First check: Configuration correct? (Tech) + API creds valid? (Business/security)

### Pattern 2: Validation

**Technical:** Checking if data meets rules  
**Business:** You're validating supplier data per Bell's standards

**Real scenario:** "I got supplier XYZ but the DUNS looks wrong"  
→ Use Pattern 2: validate DUNS (9 digits, check digit) before storing

### Pattern 3: Loop & Transform

**Technical:** Processing many items  
**Business:** Cleaning data from 250 suppliers, calculating performance scores

**Real scenario:** "I need performance scores for all suppliers"  
→ Pattern 3: Loop through suppliers, calculate weighted score

### Pattern 4: Error Handling

**Technical:** Catching and fixing problems  
**Business:** Import fails halfway - what do you do?

**Real scenario:** "Supplier 50 of 250 failed validation, but 49 succeeded"  
→ Pattern 4: Skip the bad one, continue, log it, report at end

### Pattern 5: Create/Configure/Return

**Technical:** Building complex objects  
**Business:** Creating a "SupplierRecord" with all the data

**Real scenario:** "I need to store this supplier in the database"  
→ Create a proper supplier object with all fields, configured correctly, return it

---

## 📖 How to Use the Code

`procurement_automation.py` demonstrates EVERYTHING:

**Lines 1-100:** Configuration (Pattern 1)  
**Lines 200-300:** Validation (Pattern 2)  
**Lines 400-500:** Loop & clean (Pattern 3)  
**Lines 600-700:** Error handling (Pattern 4)  
**Lines 800-900:** Complex functions (Pattern 5)  

**As you learn patterns:**
1. Read the pattern explanation
2. Look at the code lines shown
3. See how business logic uses the pattern
4. Practice with the exercise

---

## ✅ Your Study Checklist

**Technical Prep:**
- [ ] Learn all 10 patterns (PATTERNS_UNDERSTANDING_PRACTICE.md)
- [ ] Run the code yourself
- [ ] Understand what each line does
- [ ] Practice terminal commands
- [ ] Be comfortable with error messages

**Business Prep:**
- [ ] Know what ITAR means (export control)
- [ ] Know what AS9100 is (aerospace quality)
- [ ] Understand DUNS validation
- [ ] Know what risk scoring is
- [ ] Know what performance scoring is
- [ ] Understand the 5-step import flow

**Ready for Day 1:**
- [ ] Can explain any pattern in 2 minutes
- [ ] Can run the import and read output
- [ ] Know why each check matters
- [ ] Understand procurement basics
- [ ] Know what to ask when stuck

---

## 🎓 The Meta-Skill: Bridging Tech & Business

Your real job skill = **translating between engineers and business people.**

- Business says: "We need to know which suppliers are risky"
- You think: "I'll use Pattern 3 to loop through suppliers and calculate risk scores"
- Code does: Process, validate, score, store
- You report: "We have 8 high-risk suppliers needing attention"

**That's your job.**

You'll spend:
- 50% writing/understanding code (patterns)
- 50% talking to people about what that code means (business)

This prep covers both.

---

## 📍 Next Steps

1. **Today:** Read this file (you just did!)
2. **Tomorrow:** Open `PATTERNS_STUDY_KIT/PATTERNS_UNDERSTANDING_PRACTICE.md`, start Pattern 1
3. **Week 1:** Learn patterns, run code, see business concepts
4. **Week 2:** Practice, terminal commands, build confidence
5. **Day 1:** Walk in ready

**You've got this.** 💪

