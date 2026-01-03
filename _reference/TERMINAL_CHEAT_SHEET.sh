#!/bin/bash

# BELL PROCUREMENT AUTOMATION - TERMINAL CHEAT SHEET
# Quick reference for ALL commands you'll use at Bell
# Print this out or save it! This has EVERYTHING.

# ═════════════════════════════════════════════════════════════════════════════
# 🎯 DO THIS FIRST - EVERY TIME
# ═════════════════════════════════════════════════════════════════════════════

# 1. Navigate to project
cd "/Users/ammrabbasher/Bell Prep"

# 2. Check which environment you're in
python -m environment_cli info

# 3. Verify everything works
python -m environment_cli check


# ═════════════════════════════════════════════════════════════════════════════
# 🔄 ENVIRONMENT MANAGEMENT - DAILY WORK
# ═════════════════════════════════════════════════════════════════════════════

# Set environment variable (determines which database you use)
export BELL_ENVIRONMENT=dev        # Development (local, safe)
export BELL_ENVIRONMENT=test       # Testing (more strict)
export BELL_ENVIRONMENT=prod       # Production (REAL DATA - careful!)

# Check current environment
python -m environment_cli info              # See banner with colored environment

# Get all configuration
python -m environment_cli status            # Full configuration details
python -m environment_cli status --json     # As JSON (for scripts)

# Get help
python -m environment_cli help              # See all available commands


# ═════════════════════════════════════════════════════════════════════════════
# ✅ VERIFICATION COMMANDS - RUN BEFORE STARTING WORK
# ═════════════════════════════════════════════════════════════════════════════

# Run comprehensive health checks (should show all ✅)
python -m environment_cli check

# Run health checks with detailed output
python -m environment_cli check --verbose

# Get health checks as JSON (for monitoring)
python -m environment_cli check --json


# ═════════════════════════════════════════════════════════════════════════════
# 📊 INSPECTION COMMANDS - UNDERSTAND YOUR ENVIRONMENT
# ═════════════════════════════════════════════════════════════════════════════

# Which database are you using?
python -m environment_cli database

# What's the API configuration?
python -m environment_cli api

# Are compliance controls enabled? (ITAR, audit trail)
python -m environment_cli compliance

# Compare environments (run each separately, notice the differences)
export BELL_ENVIRONMENT=dev && python -m environment_cli database
export BELL_ENVIRONMENT=test && python -m environment_cli database
export BELL_ENVIRONMENT=prod && python -m environment_cli database


# ═════════════════════════════════════════════════════════════════════════════
# 🚀 RUNNING THE APPLICATION
# ═════════════════════════════════════════════════════════════════════════════

# Development (local database, safe to break things)
export BELL_ENVIRONMENT=dev
python procurement_automation.py dev config.ini

# Testing (test database, closer to production rules)
export BELL_ENVIRONMENT=test
python procurement_automation.py test config.ini

# Production (REAL DATA - only after validation!)
export BELL_ENVIRONMENT=prod
python -m environment_cli validate      # ⚠️ MUST PASS
python -m environment_cli compliance    # ⚠️ Check ITAR enabled
python procurement_automation.py prod config.ini


# ═════════════════════════════════════════════════════════════════════════════
# 🔍 TROUBLESHOOTING COMMANDS - WHEN SOMETHING GOES WRONG
# ═════════════════════════════════════════════════════════════════════════════

# Where am I in the file system?
pwd

# What files/folders are here?
ls                               # Simple list
ls -la                          # Detailed list
ls -lh                          # With human-readable sizes

# Does this file exist?
ls -l procurement_automation.py
ls -l config.ini
ls -l data/bell_procurement_dev.db

# Show me what's in a file
cat config.ini
head -20 config.ini             # First 20 lines
tail -20 config.ini             # Last 20 lines

# Search for something in files
grep "DEVELOPMENT" config.ini
grep "ERROR" logs/bell_procurement_dev.log

# Show recent log entries
tail -50 logs/bell_procurement_dev.log

# Count lines in a file
wc -l logs/bell_procurement_dev.log

# Clear cluttered screen
clear


# ═════════════════════════════════════════════════════════════════════════════
# ⚠️ PRODUCTION DEPLOYMENT - STEP BY STEP (REQUIRED PROCEDURE)
# ═════════════════════════════════════════════════════════════════════════════

# DO NOT SKIP ANY STEPS!

# Step 1: Navigate
cd "/Users/ammrabbasher/Bell Prep"

# Step 2: Set production
export BELL_ENVIRONMENT=prod

# Step 3: See production banner (should be 🔴 PRODUCTION)
python -m environment_cli info

# Step 4: Run health checks (must all be ✅)
python -m environment_cli check

# Step 5: Validate production safety (must pass)
python -m environment_cli validate

# Step 6: Verify compliance (ITAR must be ENABLED)
python -m environment_cli compliance

# Step 7: See what you're about to do
python -m environment_cli status

# Step 8: DEPLOY (only after manager approval!)
python procurement_automation.py prod config.ini

# Step 9: Check it worked
tail logs/bell_procurement_prod.log


# ═════════════════════════════════════════════════════════════════════════════
# 🎯 YOUR DAILY MORNING ROUTINE (Copy & paste this block)
# ═════════════════════════════════════════════════════════════════════════════

cd "/Users/ammrabbasher/Bell Prep"
python -m environment_cli info
python -m environment_cli check
python -m environment_cli status

# Expected: 🟢 DEVELOPMENT environment, all ✅ healthy, ready to work


# ═════════════════════════════════════════════════════════════════════════════
# 💡 PRO TIPS FOR TERMINAL POWER USERS
# ═════════════════════════════════════════════════════════════════════════════

# Run two commands in sequence (second runs only if first succeeds)
export BELL_ENVIRONMENT=dev && python -m environment_cli check

# Use arrow keys to repeat last command
# (Just press ↑ arrow key, then Enter)

# Use Tab to auto-complete
cd "/Users/ammra<TAB>"    # Auto-completes to /Users/ammrabbasher
ls bell_proc<TAB>         # Auto-completes to bell_procurement_dev.db

# Search command history
history | grep "environment"


# ═════════════════════════════════════════════════════════════════════════════
# ❌ COMMON MISTAKES & FIXES
# ═════════════════════════════════════════════════════════════════════════════

# MISTAKE 1: "File not found" error
# ❌ WRONG (you're in wrong directory)
python procurement_automation.py dev config.ini

# ✅ RIGHT (navigate first)
cd "/Users/ammrabbasher/Bell Prep"
python procurement_automation.py dev config.ini


# MISTAKE 2: Forgetting to set environment
# ❌ WRONG (environment not set)
python procurement_automation.py dev config.ini

# ✅ RIGHT (set it first)
export BELL_ENVIRONMENT=dev
python procurement_automation.py dev config.ini


# MISTAKE 3: Deploying to production without validation
# ❌ WRONG (skipping critical checks)
export BELL_ENVIRONMENT=prod
python procurement_automation.py prod config.ini

# ✅ RIGHT (verify first!)
export BELL_ENVIRONMENT=prod
python -m environment_cli validate
python -m environment_cli compliance
python procurement_automation.py prod config.ini


# MISTAKE 4: Path with spaces needs quotes
# ❌ WRONG
cd /Users/ammrabbasher/Bell Prep

# ✅ RIGHT
cd "/Users/ammrabbasher/Bell Prep"


# ═════════════════════════════════════════════════════════════════════════════
# 📋 QUICK COMMAND SUMMARY (For fast lookup)
# ═════════════════════════════════════════════════════════════════════════════

# Command                                    | What It Does
# ────────────────────────────────────────────────────────────────────────
# cd "/Users/ammrabbasher/Bell Prep"        | Go to project
# python -m environment_cli info             | Show environment
# python -m environment_cli check            | Health checks
# python -m environment_cli status           | Full config
# python -m environment_cli database         | Database info
# python -m environment_cli api              | API info
# python -m environment_cli compliance       | ITAR & audit status
# python -m environment_cli validate         | Production safety check
# python -m environment_cli help             | All commands
# export BELL_ENVIRONMENT=dev                | Set environment
# python procurement_automation.py dev config.ini | Run in dev
# tail logs/bell_procurement_dev.log         | See logs
# grep "ERROR" logs/*.log                    | Find errors


# ═════════════════════════════════════════════════════════════════════════════
# 🆘 IF YOU'RE STUCK
# ═════════════════════════════════════════════════════════════════════════════

# Get help on all commands
python -m environment_cli help

# Check where you are
pwd

# Check which environment
python -m environment_cli info

# Check if files exist
ls

# Look for errors in logs
tail logs/bell_procurement_dev.log | grep ERROR

# Read the comprehensive guide
# TERMINAL_COMMANDS_GUIDE.md has everything explained


# ═════════════════════════════════════════════════════════════════════════════
# ✨ YOU'VE GOT THIS! 💪
# ═════════════════════════════════════════════════════════════════════════════

# 1. Navigate first (cd)
# 2. Check environment (info)
# 3. Verify health (check)
# 4. Run code (python)
# 5. Check results (tail logs)

# This is exactly what you'll do at Bell. You're ready! 🚀

# ═════════════════════════════════════════════════════════════════════════════
# ⚡ MOST IMPORTANT - DO THIS FIRST EVERY TIME
# ═════════════════════════════════════════════════════════════════════════════

# Open Terminal and navigate to the project
cd "/Users/ammrabbasher/Bell Prep"

# Verify which environment you're in
python -m environment_cli info

# ═════════════════════════════════════════════════════════════════════════════
# 🎯 DAILY ROUTINE
# ═════════════════════════════════════════════════════════════════════════════

# Morning checklist
cd "/Users/ammrabbasher/Bell Prep"
python -m environment_cli info              # Where am I?
python -m environment_cli check             # Is everything working?
python -m environment_cli status            # Show me the config


# ═════════════════════════════════════════════════════════════════════════════
# 🔄 ENVIRONMENT SWITCHING
# ═════════════════════════════════════════════════════════════════════════════

# Development (local, safe to break)
export BELL_ENVIRONMENT=dev
python -m environment_cli info

# Testing (like production, but safer)
export BELL_ENVIRONMENT=test
python -m environment_cli info

# Production (real data, be careful!)
export BELL_ENVIRONMENT=prod
python -m environment_cli info


# ═════════════════════════════════════════════════════════════════════════════
# ✅ ENVIRONMENT VERIFICATION COMMANDS
# ═════════════════════════════════════════════════════════════════════════════

# See the environment banner
python -m environment_cli info

# Run health checks (should show all green ✅)
python -m environment_cli check

# See full configuration
python -m environment_cli status

# See which database
python -m environment_cli database

# See API configuration and rate limits
python -m environment_cli api

# See ITAR and compliance settings
python -m environment_cli compliance

# Validate production is safe
python -m environment_cli validate

# Get help on all commands
python -m environment_cli help


# ═════════════════════════════════════════════════════════════════════════════
# ▶️ RUNNING THE APPLICATION
# ═════════════════════════════════════════════════════════════════════════════

# Run in development
export BELL_ENVIRONMENT=dev
python procurement_automation.py dev config.ini

# Run in testing
export BELL_ENVIRONMENT=test
python procurement_automation.py test config.ini

# Run in production (⚠️ requires validation first!)
export BELL_ENVIRONMENT=prod
python -m environment_cli validate
python -m environment_cli compliance
python procurement_automation.py prod config.ini


# ═════════════════════════════════════════════════════════════════════════════
# 🔍 TROUBLESHOOTING COMMANDS
# ═════════════════════════════════════════════════════════════════════════════

# Where am I in the file system?
pwd

# What files are here?
ls
ls -la                           # With details
ls -lh                           # With human-readable sizes

# Check if file exists
ls procurement_automation.py
ls config.ini
ls data/bell_procurement_dev.db

# View file contents
cat config.ini                   # Show entire file
head -20 config.ini             # First 20 lines
tail -20 config.ini             # Last 20 lines

# Search in files
grep "DEVELOPMENT" config.ini
grep "ERROR" logs/bell_procurement_dev.log

# View recent log entries
tail -50 logs/bell_procurement_dev.log

# Count lines in file
wc -l logs/bell_procurement_dev.log

# Check Python version
python --version

# Check Python packages
pip list


# ═════════════════════════════════════════════════════════════════════════════
# 🚀 PRODUCTION DEPLOYMENT (STEP-BY-STEP)
# ═════════════════════════════════════════════════════════════════════════════

# Step 1: Navigate
cd "/Users/ammrabbasher/Bell Prep"

# Step 2: Set to production
export BELL_ENVIRONMENT=prod

# Step 3: See production banner (should be 🔴 red)
python -m environment_cli info

# Step 4: Run health checks (must all be ✅)
python -m environment_cli check

# Step 5: Validate production safety (must pass)
python -m environment_cli validate

# Step 6: Check compliance (ITAR must be enabled)
python -m environment_cli compliance

# Step 7: See the configuration you're about to use
python -m environment_cli status

# Step 8: DEPLOY (do this only after manager approval)
python procurement_automation.py prod config.ini

# Step 9: Check what happened
tail logs/bell_procurement_prod.log


# ═════════════════════════════════════════════════════════════════════════════
# 📋 QUICK COMMAND REFERENCE
# ═════════════════════════════════════════════════════════════════════════════

# Abbreviation | Full Command                      | What It Does
# ─────────────────────────────────────────────────────────────────────
# pwd          | pwd                               | Show current folder
# ls           | ls -la                            | List files with details
# cd           | cd "/Users/ammrabbasher/Bell Prep"| Go to project folder
# cat          | cat config.ini                    | View file contents
# grep         | grep "ERROR" logs/*.log           | Search for text
# tail         | tail -50 logs/bell_procurement_dev.log | Show last 50 lines
# clear        | clear                             | Clear screen
# set env      | export BELL_ENVIRONMENT=dev       | Set environment
# check env    | python -m environment_cli info    | See environment
# verify       | python -m environment_cli check   | Health checks
# help         | python -m environment_cli help    | See all commands


# ═════════════════════════════════════════════════════════════════════════════
# ⚠️ COMMON MISTAKES
# ═════════════════════════════════════════════════════════════════════════════

# ❌ WRONG: Forgetting to navigate to project
python procurement_automation.py dev config.ini
# Error: can't open file

# ✅ RIGHT: Navigate first
cd "/Users/ammrabbasher/Bell Prep"
python procurement_automation.py dev config.ini


# ❌ WRONG: Forgetting to set environment
python procurement_automation.py dev config.ini

# ✅ RIGHT: Set environment first
export BELL_ENVIRONMENT=dev
python procurement_automation.py dev config.ini


# ❌ WRONG: Copying commands with comments
export BELL_ENVIRONMENT=dev   # This is development

# ✅ RIGHT: Remove comments or type separately
export BELL_ENVIRONMENT=dev
python -m environment_cli info


# ❌ WRONG: Deploying to production without checks
export BELL_ENVIRONMENT=prod
python procurement_automation.py prod config.ini

# ✅ RIGHT: Validate first
export BELL_ENVIRONMENT=prod
python -m environment_cli validate
python -m environment_cli compliance
python procurement_automation.py prod config.ini


# ═════════════════════════════════════════════════════════════════════════════
# 🎯 YOUR FIRST 5 MINUTES AT BELL (or every morning)
# ═════════════════════════════════════════════════════════════════════════════

# Copy and paste this entire block:

cd "/Users/ammrabbasher/Bell Prep"
python -m environment_cli info
python -m environment_cli check
python -m environment_cli status

# Expected output: Should see 🟢 DEVELOPMENT with all ✅ HEALTHY checks


# ═════════════════════════════════════════════════════════════════════════════
# 📊 COMPARING ENVIRONMENTS (understand the differences)
# ═════════════════════════════════════════════════════════════════════════════

# See development
export BELL_ENVIRONMENT=dev
python -m environment_cli database
python -m environment_cli api

# See testing
export BELL_ENVIRONMENT=test
python -m environment_cli database
python -m environment_cli api

# See production
export BELL_ENVIRONMENT=prod
python -m environment_cli database
python -m environment_cli api

# Output will show different databases, APIs, and rate limits


# ═════════════════════════════════════════════════════════════════════════════
# 🔐 PRODUCTION SAFETY CHECKLIST (PRINT THIS OUT!)
# ═════════════════════════════════════════════════════════════════════════════

# Before deploying to production, verify EACH item:

# ☐ 1. Correct environment?
export BELL_ENVIRONMENT=prod
python -m environment_cli info          # Should show 🔴 PRODUCTION

# ☐ 2. All systems healthy?
python -m environment_cli check         # Should show all ✅

# ☐ 3. Safety validation passes?
python -m environment_cli validate      # Should show "passed"

# ☐ 4. Compliance enabled?
python -m environment_cli compliance    # Should show ITAR ENABLED

# ☐ 5. Manager approved?
# (Not a command, but critical!)

# ☐ 6. THEN deploy
python procurement_automation.py prod config.ini

# DO NOT PROCEED IF ANY CHECK FAILS!


# ═════════════════════════════════════════════════════════════════════════════
# 💡 PRO TIPS
# ═════════════════════════════════════════════════════════════════════════════

# Combine commands with && (run second only if first succeeds)
export BELL_ENVIRONMENT=dev && python -m environment_cli check

# Use ↑ arrow key to repeat last command
# (Just press up arrow key, then Enter)

# Use Tab to auto-complete file names
cd "/Users/ammra<TAB>"    # Completes: /Users/ammrabbasher
ls bell_proc<TAB>         # Completes: bell_procurement_dev.db

# Clear screen when it gets messy
clear

# Check history of commands you typed
history
history | grep "environment"    # Find specific command


# ═════════════════════════════════════════════════════════════════════════════
# 🆘 IF YOU'RE STUCK
# ═════════════════════════════════════════════════════════════════════════════

# Get help
python -m environment_cli help

# Check where you are
pwd

# Check what environment you're in
python -m environment_cli info

# Check if files exist
ls

# Look for errors
tail logs/bell_procurement_dev.log | grep ERROR

# Read this guide again
# TERMINAL_COMMANDS_GUIDE.md has everything


# ═════════════════════════════════════════════════════════════════════════════
# 🎉 REMEMBER
# ═════════════════════════════════════════════════════════════════════════════

# 1. Navigate first (cd)
# 2. Check environment (info)
# 3. Verify health (check)
# 4. Run code (python)
# 5. Check results (tail logs)

# You've got this! 💪

