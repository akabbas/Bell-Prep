# Bell Textron Procurement Automation - Your Prep Guide

**Real code. Real concepts. Real job preparation.**

---

## 📍 START HERE

| What | Where | Time | Why |
|------|-------|------|-----|
| **Learn patterns** | `PATTERNS_STUDY_KIT/PATTERNS_UNDERSTANDING_PRACTICE.md` | 8-10 hrs | Core technical skill |
| **Understand the job** | `JOB_DESCRIPTION.md` | 15 min | Know what you'll do |
| **Terminal commands** | `TERMINAL_COMMANDS_GUIDE.md` | 1-2 hrs | Daily work tool |
| **Real code** | `procurement_automation.py` | Reference | See patterns in action |
| **Study roadmap** | `PATTERNS_STUDY_KIT/00_START_HERE.md` | 10 min | How to use everything |

---

## 🎯 Your Job: 50/50 Tech & Business

### Technical Half (What We Cover Here)
- **10 coding patterns** - real Bell code uses these
- **Python fundamentals** - loops, functions, error handling
- **API integration** - how systems talk to each other
- **Database operations** - storing supplier data
- **Environment management** - dev/test/prod systems

### Business Half (What You'll See Day 1)
- **Procurement process** - how Bell buys from suppliers
- **Compliance requirements** - ITAR (export control), AS9100 (quality)
- **Risk assessment** - which suppliers matter most
- **Audit trails** - proving what happened when
- **DUNS validation** - supplier identification
- **Performance scoring** - which suppliers perform best

---

## 🚀 Quick Setup

```bash
cd "/Users/ammrabbasher/Bell Prep"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 📚 What This Project Is

A **realistic simulation** of Bell Textron's procurement automation system:
- Downloads supplier data from API (simulated)
- Cleans and validates it
- Stores it in database
- Tracks compliance and audit trails
- Flags high-risk suppliers

**This is production code.** Not a tutorial. You'll see patterns here that you'll use on Day 1.

---

## 🎓 Study Path (Your Focus)

**Week 1:** Learn the 10 patterns using `PATTERNS_UNDERSTANDING_PRACTICE.md`
- Pattern 1-5: Foundation (1.5 hrs each)
- Pattern 6-10: Reference (1 hr combined)

**Week 2:** Practice & apply
- Terminal commands
- Run the code yourself
- See output and understand flow

**Week 3:** Business context
- Read procurement concepts in comments
- Understand why each step matters
- Know what you'll discuss on Day 1

---

## 🔑 Core Concepts You'll Use

**Configuration Reading** - How systems know where to connect  
**Validation** - Making sure data is correct  
**Loop & Transform** - Processing many items at once  
**Error Handling** - What happens when things break  
**Create/Configure/Return** - Building objects properly  

Plus 5 more patterns in the same code.

---

## 💼 Business Concepts in the Code

**DUNS Number** - Unique supplier identifier (you'll validate these)  
**ITAR** - Export control rules (you'll check compliance)  
**AS9100** - Aerospace quality standard (defense requirement)  
**Risk Scoring** - Which suppliers need attention  
**Performance Score** - How well suppliers perform  

---

## 📖 Files You Actually Need

- `PATTERNS_STUDY_KIT/PATTERNS_UNDERSTANDING_PRACTICE.md` - How to learn (CORE)
- `procurement_automation.py` - The real code (REFERENCE)
- `JOB_DESCRIPTION.md` - What the job is (CONTEXT)
- `TERMINAL_COMMANDS_GUIDE.md` - How to work (ESSENTIAL)
- `PATTERNS_STUDY_KIT/00_START_HERE.md` - Study plan (GUIDE)
- `QUICK_REFERENCE.md` - Fast lookups (REFERENCE)

---

## ▶️ Run It

```bash
# Development environment (default)
python procurement_automation.py dev config.ini

# Expected output: Suppliers imported/updated with audit trail
```

---

## 🎯 Your Goal

**Master the patterns** → **Understand the business** → **Be ready Day 1**

Everything in this project teaches you those three things.

No fluff. Just what you need.
