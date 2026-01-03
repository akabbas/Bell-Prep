# Terminal Commands - Step-by-Step Visual Examples

A visual guide showing exactly what you'll see when you run commands. This is what your screen will look like!

---

## Example 1: Your First Morning (Basic Setup)

### Step 1: Open Terminal
- On Mac: Press `Cmd + Space`, type "Terminal", press Enter
- On Windows: Press `Win + R`, type "powershell", press Enter

You'll see something like:
```
Last login: Sun Dec 28 14:39:14 on ttys003
ammrabbasher@Ammrs-MacBook-Air-2 ~ %
```

**What this means:**
- `ammrabbasher` = your username
- `@Ammrs-MacBook-Air-2` = your computer name
- `~` = you're in home directory
- `%` = ready for commands (prompt)

---

### Step 2: Navigate to Project

**Type this:**
```bash
cd "/Users/ammrabbasher/Bell Prep"
```

**You see:**
```
ammrabbasher@Ammrs-MacBook-Air-2 Bell Prep %
```

**What changed:**
- `Bell Prep` = now you're in that folder
- Prompt is ready for next command

---

### Step 3: Check Which Environment

**Type this:**
```bash
python -m environment_cli info
```

**You see:**
```
╔═══════════════════════════════════════════════════════════════════════╗
║ 🟢 DEVELOPMENT                                                         ║
║                                                                       ║
║ Database:       sqlite:///./data/bell_procurement_dev.db             ║
║ API:            http://localhost:8000/ariba-mock                     ║
║ Log Level:      INFO                                                 ║
║ ITAR Logging:   ENABLED                                              ║
║                                                                       ║
║ ℹ️  Development environment, relaxed limits                           ║
║ Initialized:    2025-12-28 15:11:37 UTC                              ║
╚═══════════════════════════════════════════════════════════════════════╝

ammrabbasher@Ammrs-MacBook-Air-2 Bell Prep %
```

**What you learned:**
- 🟢 You're in DEVELOPMENT (safe)
- Database is local SQLite
- API is localhost (not real)
- ITAR logging is enabled
- Ready to work!

---

### Step 4: Verify Everything Works

**Type this:**
```bash
python -m environment_cli check
```

**You see:**
```
INFO: Starting comprehensive health check suite

======================================================================
HEALTH CHECK REPORT
======================================================================
Environment: DEVELOPMENT
Overall Status: HEALTHY
Timestamp: 2025-12-28T15:13:40.012001
----------------------------------------------------------------------
✅ Configuration: HEALTHY - Environment: DEVELOPMENT
✅ Environment Variables: HEALTHY - Environment variables configured
✅ Database Connectivity: HEALTHY - SQLite database accessible
✅ Database Schema: HEALTHY - All required tables present (4)
✅ Log Directory: HEALTHY - Log directory writable
✅ Data Directory: HEALTHY - Data directory writable
✅ API Configuration: HEALTHY - API configured
✅ Compliance Settings: HEALTHY - Compliance settings configured for DEVELOPMENT
----------------------------------------------------------------------
Summary: 8 healthy, 0 warnings, 0 errors
======================================================================

INFO: Health check complete: 8 checks performed

ammrabbasher@Ammrs-MacBook-Air-2 Bell Prep %
```

**What you learned:**
- ✅ All 8 checks passed
- Database is working
- Files/directories are writable
- Everything is ready to go!

**If you see ❌ ERROR:** Stop and fix the issue before continuing.

---

## Example 2: Switching Environments

### Current: Development → Switch to Testing

**Type this:**
```bash
export BELL_ENVIRONMENT=test
```

**You see:**
```
ammrabbasher@Ammrs-MacBook-Air-2 Bell Prep %
```

**What happened:** Nothing visible yet. The environment is now set to TEST, but you need another command to see it.

---

### Verify You Switched

**Type this:**
```bash
python -m environment_cli info
```

**You see:**
```
╔═══════════════════════════════════════════════════════════════════════╗
║ 🟡 TEST                                                                ║
║                                                                       ║
║ Database:       sqlite:///./data/bell_procurement_test.db            ║
║ API:            http://localhost:8000/ariba-mock                     ║
║ Log Level:      INFO                                                 ║
║ ITAR Logging:   ENABLED                                              ║
║                                                                       ║
║ ℹ️  Test environment with full audit trail                            ║
║ Initialized:    2025-12-28 15:13:47 UTC                              ║
╚═══════════════════════════════════════════════════════════════════════╝

ammrabbasher@Ammrs-MacBook-Air-2 Bell Prep %
```

**What changed:**
- 🟡 Now showing TEST (instead of 🟢 DEVELOPMENT)
- Database path changed (test instead of dev)
- Everything else same

---

## Example 3: Checking Database Information

### Development Database

**Type this:**
```bash
export BELL_ENVIRONMENT=dev
python -m environment_cli database
```

**You see:**
```

Database Information (DEVELOPMENT)
============================================================
Connection URL: sqlite:///./data/bell_procurement_dev.db
Database Type: SQLite
Database Path: ./data/bell_procurement_dev.db
File Size: 2.45 MB
Tables: 4
============================================================

ammrabbasher@Ammrs-MacBook-Air-2 Bell Prep %
```

### Production Database

**Type this:**
```bash
export BELL_ENVIRONMENT=prod
python -m environment_cli database
```

**You see:**
```

Database Information (PRODUCTION)
============================================================
Connection URL: mssql+pyodbc://user:password@server/bell_procurement?driver=ODBC+Driver+17+for+SQL+Server
Database Type: SQL Server
Status: Connection deferred to runtime
============================================================

ammrabbasher@Ammrs-MacBook-Air-2 Bell Prep %
```

**Key difference:**
- DEV: Local SQLite file you can see
- PROD: SQL Server on network (Bell's servers)

---

## Example 4: Checking API Configuration

**Type this:**
```bash
export BELL_ENVIRONMENT=dev
python -m environment_cli api
```

**You see:**
```

API Configuration (DEVELOPMENT)
============================================================
Base URL:        http://localhost:8000/ariba-mock
Rate Limit:      100 calls
Period:          60 seconds
Timeout:         30 seconds
Calculated Rate: 1.67 calls/sec
============================================================

ammrabbasher@Ammrs-MacBook-Air-2 Bell Prep %
```

**Now check production:**

```bash
export BELL_ENVIRONMENT=prod
python -m environment_cli api
```

**You see:**
```

API Configuration (PRODUCTION)
============================================================
Base URL:        https://api.ariba.com/v1
Rate Limit:      500 calls
Period:          60 seconds
Timeout:         30 seconds
Calculated Rate: 8.33 calls/sec
============================================================

ammrabbasher@Ammrs-MacBook-Air-2 Bell Prep %
```

**Key differences:**
- DEV: 100 calls/min, localhost
- PROD: 500 calls/min, real API (https://api.ariba.com)

---

## Example 5: Checking Compliance (Important!)

### Development

**Type this:**
```bash
export BELL_ENVIRONMENT=dev
python -m environment_cli compliance
```

**You see:**
```

Compliance Configuration (DEVELOPMENT)
============================================================
Environment:              DEVELOPMENT
ITAR Logging:             True
ITAR Validation Required: False
Audit Trail Enabled:      True
Log Level:                INFO
Log File:                 logs/bell_procurement_dev.log
============================================================

ammrabbasher@Ammrs-MacBook-Air-2 Bell Prep %
```

### Production

**Type this:**
```bash
export BELL_ENVIRONMENT=prod
python -m environment_cli compliance
```

**You see:**
```

Compliance Configuration (PRODUCTION)
============================================================
Environment:              PRODUCTION
ITAR Logging:             True
ITAR Validation Required: True
Audit Trail Enabled:      True
Log Level:                WARNING
Log File:                 logs/bell_procurement_prod.log

⚠️  PRODUCTION ENVIRONMENT DETECTED
============================================================
All production compliance controls are ENABLED ✓
============================================================

ammrabdasher@Ammrs-MacBook-Air-2 Bell Prep %
```

**Key differences:**
- PROD requires ITAR validation
- PROD log level is WARNING (less verbose)
- Everything else ENABLED

---

## Example 6: Production Deployment (Step-by-Step)

### Step 1: Set to Production

**Type this:**
```bash
export BELL_ENVIRONMENT=prod
```

**You see:**
```
ammrabbasher@Ammrs-MacBook-Air-2 Bell Prep %
```

---

### Step 2: See Production Banner

**Type this:**
```bash
python -m environment_cli info
```

**You see:**
```
╔═══════════════════════════════════════════════════════════════════════╗
║ 🔴 PRODUCTION                                                          ║
║                                                                       ║
║ Database:       mssql+pyodbc://user:password@server/bell_procurement?driver=ODBC+Driver+17+for+SQL+Server║
║ API:            https://api.ariba.com/v1                             ║
║ Log Level:      WARNING                                              ║
║ ITAR Logging:   ENABLED                                              ║
║                                                                       ║
║ ⚠️  STRICT VALIDATION AND AUDIT LOGGING ENABLED                       ║
║ Initialized:    2025-12-28 15:13:32 UTC                              ║
╚═══════════════════════════════════════════════════════════════════════╝

ammrabbasher@Ammrs-MacBook-Air-2 Bell Prep %
```

**What you learned:** This is PRODUCTION - the big red banner is a warning!

---

### Step 3: Run Health Checks

**Type this:**
```bash
python -m environment_cli check
```

**You see:**
```
INFO: Starting comprehensive health check suite

======================================================================
HEALTH CHECK REPORT
======================================================================
Environment: PRODUCTION
Overall Status: HEALTHY
Timestamp: 2025-12-28T15:13:32.577869
----------------------------------------------------------------------
✅ Configuration: HEALTHY - Environment: PRODUCTION
✅ Environment Variables: HEALTHY - Environment variables configured
⚠️  Database Connectivity: WARNING - SQL Server connectivity check skipped
✅ API Configuration: HEALTHY - API configured
✅ Compliance Settings: HEALTHY - All compliance controls enabled
...
Summary: 7 healthy, 1 warnings, 0 errors
======================================================================

ammrabbasher@Ammrs-MacBook-Air-2 Bell Prep %
```

**What you learned:**
- Most checks pass ✅
- SQL Server check is skipped (normal - will connect at runtime)
- Overall status is HEALTHY (safe to proceed)

---

### Step 4: Validate Safety

**Type this:**
```bash
python -m environment_cli validate
```

**You see:**
```
INFO: Environment PRODUCTION passed safety validation
✓ Environment validation passed: PRODUCTION

ammrabbasher@Ammrs-MacBook-Air-2 Bell Prep %
```

**What you learned:** Production safety checks passed - ITAR is enabled, audit trail is on, everything is secure.

---

### Step 5: Check Compliance

**Type this:**
```bash
python -m environment_cli compliance
```

**You see:** (Same as before - all controls ENABLED)

---

### Step 6: Deploy

**Type this:**
```bash
python procurement_automation.py prod config.ini
```

**You see:**
```
===========================================================================
PROCUREMENT AUTOMATION SUMMARY
===========================================================================
{
  "import_id": "IMP-20251228151432",
  "environment": "prod",
  "status": "SUCCESS",
  "duration_seconds": 12.45,
  "records": {
    "total_fetched": 500,
    "cleaned": 498,
    "inserted": 250,
    "updated": 248,
    "skipped": 0,
    "errors": 2
  },
  "compliance": {
    "itar_compliant_suppliers": 480,
    "high_risk_suppliers": 15
  }
}
===========================================================================

ammrabbasher@Ammrs-MacBook-Air-2 Bell Prep %
```

**What you learned:** 
- Import succeeded ✅
- 500 suppliers processed
- 498 cleaned successfully
- 250 new, 248 updated
- Audit trail logged this action
- ITAR-compliant suppliers tracked

---

## Example 7: Troubleshooting - "File not found" Error

### The Problem

**You type this (without navigating first):**
```bash
python procurement_automation.py dev config.ini
```

**You see:**
```
/Library/Developer/CommandLineTools/usr/bin/python3: can't open file '/Users/ammrabbasher/procurement_automation.py': [Errno 2] No such file or directory
ammrabbasher@Ammrs-MacBook-Air-2 ~ %
```

**What went wrong:**
- You're in home directory (`~`)
- Python is looking for file there, but it's in `/Users/ammrabbasher/Bell Prep`

### The Solution

**Type this:**
```bash
cd "/Users/ammrabbasher/Bell Prep"
python procurement_automation.py dev config.ini
```

**Now you see:**
```
(Application runs successfully)

ammrabbasher@Ammrs-MacBook-Air-2 Bell Prep %
```

---

## Example 8: Viewing Logs to See What Happened

### View Last 20 Lines

**Type this:**
```bash
tail -20 logs/bell_procurement_dev.log
```

**You see:**
```
2025-12-28 15:10:30 | bell_procurement | INFO | [_initialize_api_client] | Procurement Automation initialized for dev
2025-12-28 15:10:31 | bell_procurement | INFO | [get_suppliers] | Fetching suppliers - Page: 1, PageSize: 50
2025-12-28 15:10:32 | bell_procurement | INFO | [_clean_suppliers] | Cleaned 48 suppliers, 2 validation errors
2025-12-28 15:10:33 | bell_procurement | INFO | [_upsert_suppliers] | Inserted 25 new suppliers
2025-12-28 15:10:33 | bell_procurement | INFO | [_upsert_suppliers] | Updated 23 existing suppliers
2025-12-28 15:10:34 | bell_procurement | INFO | [_log_itar_access] | ITAR access logged: automation_service performed INSERT on SUPP-00142
2025-12-28 15:10:35 | bell_procurement | INFO | [record_audit_trail] | Audit trail recorded: IMP-20251228151030 - SUCCESS

ammrabbasher@Ammrs-MacBook-Air-2 Bell Prep %
```

**What you learned:**
- Import succeeded
- 48 suppliers cleaned
- 25 new suppliers added
- 23 updated
- ITAR access was logged
- Audit trail was recorded

---

### Search for Errors

**Type this:**
```bash
grep "ERROR" logs/bell_procurement_dev.log
```

**You see (if there are errors):**
```
2025-12-28 15:10:32 | bell_procurement | ERROR | [_validate_duns_number] | DUNS number validation failed for supplier SUPP-00089
2025-12-28 15:10:32 | bell_procurement | ERROR | [_validate_duns_number] | DUNS number validation failed for supplier SUPP-00156

ammrabbasher@Ammrs-MacBook-Air-2 Bell Prep %
```

**What you learned:** Two suppliers had validation errors (DUNS numbers invalid)

---

## Example 9: Quick Status Check

**Type this (everything in one command):**
```bash
cd "/Users/ammrabbasher/Bell Prep" && export BELL_ENVIRONMENT=dev && python -m environment_cli info
```

**You see:**
```
╔═══════════════════════════════════════════════════════════════════════╗
║ 🟢 DEVELOPMENT                                                         ║
║                                                                       ║
║ Database:       sqlite:///./data/bell_procurement_dev.db             ║
║ API:            http://localhost:8000/ariba-mock                     ║
║ Log Level:      INFO                                                 ║
║ ITAR Logging:   ENABLED                                              ║
║                                                                       ║
║ ℹ️  Development environment, relaxed limits                           ║
║ Initialized:    2025-12-28 15:11:37 UTC                              ║
╚═══════════════════════════════════════════════════════════════════════╝

ammrabbasher@Ammrs-MacBook-Air-2 Bell Prep %
```

**What this does:** Navigate + set environment + show banner in one command using `&&` (do next command if previous succeeded)

---

## Example 10: Listing Files

### Simple List

**Type this:**
```bash
ls
```

**You see:**
```
README.md                              config.ini
config.ini.save                        data
environment_cli.py                     environment_config.py
environment_health_check.py            logs
procurement_automation.py              requirements.txt
sample_data.py                         utils.py
test_pipeline.py                       TERMINAL_COMMANDS_GUIDE.md

ammrabbasher@Ammrs-MacBook-Air-2 Bell Prep %
```

### Detailed List

**Type this:**
```bash
ls -la
```

**You see:**
```
total 1048
drwxr-xr-x  16 ammrabbasher  staff    512 Dec 28 15:13 .
drwxr-xr-x   4 ammrabbasher  staff    128 Dec 28 14:00 ..
-rw-r--r--   1 ammrabbasher  staff   1024 Dec 28 15:10 README.md
-rw-r--r--   1 ammrabbasher  staff    982 Dec 28 15:10 config.ini
drwxr-xr-x   3 ammrabbasher  staff     96 Dec 28 15:10 data
drwxr-xr-x   3 ammrabbasher  staff     96 Dec 28 15:10 logs
-rw-r--r--   1 ammrabbasher  staff  15000 Dec 28 15:04 environment_cli.py

ammrabbasher@Ammrs-MacBook-Air-2 Bell Prep %
```

**What you see:**
- First column: permissions (rwx = read/write/execute)
- Size (in bytes)
- Date/time modified
- File name

---

## What to Do If You See These Prompts

### Prompt: `>`

```
Python 3.9.0 (default, Oct  5 2020, 17:52:40) 
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

**What this means:** You're inside Python interactive shell (not what we want)

**Fix:** Type `exit()` to go back to terminal

```bash
>>> exit()
ammrabbasher@Ammrs-MacBook-Air-2 Bell Prep %
```

---

### Prompt: `quote>`

```
> export BELL_ENVIRONMENT=test   # Now it's TEST
quote> python -m environment_cli info
```

**What this means:** You accidentally included a line break in middle of command

**Fix:** Press `Ctrl + C` to cancel, then try again separately

```bash
^C
ammrabbasher@Ammrs-MacBook-Air-2 Bell Prep %
export BELL_ENVIRONMENT=test
ammrabbasher@Ammrs-MacBook-Air-2 Bell Prep %
python -m environment_cli info
```

---

## Summary

Now you understand:
- ✅ How to navigate with `cd`
- ✅ How to set environment with `export`
- ✅ How to check environment with `info`
- ✅ How to verify health with `check`
- ✅ How to see logs with `tail`
- ✅ What errors look like
- ✅ How to fix mistakes

**You're ready to use the terminal like a pro!** 🚀

Print this out for reference during your first week at Bell!


