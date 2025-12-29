# Bell Textron Procurement Automation System

## 📚 Documentation Guide

**Start here based on your needs:**

| Your Question | Read This | Time |
|---|---|---|
| "What is this project?" | **README.md** (this file) | 10 min |
| "How does this prepare me for Bell?" | **ENVIRONMENT_AT_BELL.md** | 20 min |
| "How do I use the terminal?" | **TERMINAL_COMMANDS_GUIDE.md** | 20 min |
| "What should I see when I run this?" | **TERMINAL_VISUAL_EXAMPLES.md** | 15 min |
| "What's the quick command?" | **TERMINAL_CHEAT_SHEET.sh** | 2 min |
| "How is it built?" | **ENVIRONMENT_IMPLEMENTATION_SUMMARY.md** | 15 min |

---

## Overview

A production-ready Python application that simulates downloading supplier performance data from SAP Ariba API, cleans and transforms it, and loads it to a SQL Server database. Built specifically for Bell Textron's defense/aerospace procurement environment with ITAR compliance, AS9100 certification validation, and comprehensive audit trails.

**Version:** 1.0.0  
**Environment:** Python 3.8+  
**Database:** SQLite (development/testing) / SQL Server (production)

---

## Features

### 1. **SAP Ariba API Simulation**
- Realistic API authentication with Bearer tokens
- Rate limiting enforcement (429 responses)
- Pagination support for large supplier lists
- Network delay simulation
- Retry logic for transient failures (500, 502, 503, 504)
- Deterministic mock data generation

### 2. **Data Cleaning & Validation**
- **DUNS Number Validation**: 9-digit check-digit validation (critical for supplier identification)
- **Supplier Name Standardization**: Converts variations ("Boeing Co." → "BOEING CO")
- **Numeric Validation**: Ensures percentages (0-100), lead times, cost scores are valid
- **ITAR/AS9100 Compliance Flags**: Validates export-control and aerospace quality certifications
- **Missing Data Handling**: Strategic approach (default audit dates, etc.)
- **Composite Performance Scoring**: Weighted metrics (on-time: 40%, quality: 30%, cost: 20%, risk: 10%)

### 3. **High-Risk Supplier Detection**
Flags suppliers meeting Bell's risk criteria:
- Risk score > 3 AND spend YTD > $100,000
- Audit date > 90 days old
- ITAR non-compliant with defense work (spend > $50K)
- Missing AS9100 certification

### 4. **Database Operations**
- **Upsert Logic**: Insert new suppliers, update existing (by DUNS number)
- **Audit Trail**: Complete import tracking (who, what, when, how many)
- **ITAR Access Logging**: Export-control compliance tracking (who accessed what)
- **Transaction Management**: Rollback on errors
- **Performance Score**: Calculated and stored for each supplier

### 5. **Bell-Specific Compliance**
- ✅ ITAR compliance logging (export-controlled supplier tracking)
- ✅ AS9100 certification validation (aerospace quality standard)
- ✅ Risk scoring for defense contractors
- ✅ Audit trail for governance requirements
- ✅ Environment-specific configuration (dev/test/prod)
- ✅ Comprehensive error handling and logging

### 6. **Environment Management**
```
DEV:   SQLite database, relaxed rate limits, verbose logging
TEST:  SQLite database, test rate limits, full audit trail
PROD:  SQL Server, strict rate limits, ITAR enforcement
```

### 7. **Enterprise-Grade Configuration Management**
- ✅ Centralized `EnvironmentConfig` singleton for single source of truth
- ✅ Type-safe configuration properties with IDE autocomplete
- ✅ Environment variable support (`BELL_ENVIRONMENT`)
- ✅ Comprehensive health check suite with detailed reporting
- ✅ Production safety validation (ITAR enforcement, SQL Server requirement)
- ✅ CLI utilities for environment inspection and status checking
- ✅ Startup banner logging for audit trails and compliance

---

## Environment Management

### Understanding Environments

Bell Procurement System supports three distinct environments, each optimized for its purpose:

| Feature | Development | Testing | Production |
|---------|-------------|---------|-----------|
| **Database** | SQLite (local) | SQLite (local) | SQL Server (enterprise) |
| **API Endpoint** | localhost:8000 | localhost:8000 | api.ariba.com |
| **Rate Limiting** | 100 calls/60s | 50 calls/60s | 500 calls/60s |
| **ITAR Logging** | Enabled | Enabled | **Required** |
| **Audit Trail** | Enabled | Enabled | **Required** |
| **ITAR Validation** | Optional | Optional | **Mandatory** |
| **Log Level** | INFO (configurable) | INFO | WARNING |

### Knowing Which Environment You're In

Bell uses an **enterprise-grade environment detection system** that prevents ambiguity:

#### 1. **Check Environment Status**

```bash
# Display current environment configuration
python -m environment_cli status

# Output as JSON for programmatic use
python -m environment_cli status --json

# Show in banner format
python -m environment_cli info
```

#### 2. **Set Your Environment**

```bash
# Via environment variable (recommended for production)
export BELL_ENVIRONMENT=prod
python procurement_automation.py prod config.ini

# Or use the CLI to see the command
python -m environment_cli set prod

# Development (default)
python -m environment_cli set dev
```

#### 3. **Verify Environment Configuration**

```bash
# Run comprehensive health checks
python -m environment_cli check

# Validate production safety requirements
python -m environment_cli validate

# View specific configurations
python -m environment_cli database    # Database settings
python -m environment_cli api          # API configuration
python -m environment_cli compliance  # ITAR & audit settings
```

### Programmatic Environment Access

From within Python code:

```python
from environment_config import EnvironmentConfig

# Get configuration (singleton pattern - initialized once)
env = EnvironmentConfig()

# Check environment
if env.is_production:
    print("Running in PRODUCTION - strict validation enabled")
elif env.is_development:
    print("Running in DEVELOPMENT - relaxed settings")

# Access configuration values
db_url = env.database_url
api_endpoint = env.api_base_url
is_prod = env.is_production

# Get all settings as dictionary
all_settings = env.get_all_settings()

# Print formatted status report
print(env.status_report())
```

### Health Check and Validation

```python
from environment_health_check import EnvironmentHealthChecker

# Run health checks
checker = EnvironmentHealthChecker()
results = checker.run_all_checks()

# Print formatted report
checker.print_report()

# Get JSON results
json_report = checker.get_json_report()

# Check specific component
if results['Database Connectivity'].status.value == 'HEALTHY':
    print("Database is accessible")
```

### Environment Variables

The system respects these environment variables:

```bash
# Explicitly set environment (dev, test, prod)
export BELL_ENVIRONMENT=prod

# Optional: Override config file location
export BELL_CONFIG_FILE=/etc/bell/config.ini
```

If not set, the system defaults to `dev` and looks for `config.ini` in the current directory.

### Production Requirements

**Before deploying to production, verify:**

```bash
# 1. Set production environment
export BELL_ENVIRONMENT=prod

# 2. Display environment (should show PRODUCTION)
python -m environment_cli info

# 3. Run health checks (must all be GREEN)
python -m environment_cli check

# 4. Validate safety requirements (ITAR, SQL Server, audit)
python -m environment_cli validate

# 5. Review compliance settings
python -m environment_cli compliance
```

All checks must pass before running in production.

---

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone/Navigate to project directory:**
```bash
cd "/Users/ammrabbasher/Bell Prep"
```

2. **Create virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Create required directories:**
```bash
mkdir -p logs data
```

### Running the Application

#### Development Environment (Default)
```bash
python procurement_automation.py dev config.ini
```

#### Test Environment
```bash
python procurement_automation.py test config.ini
```

#### Production Environment (requires SQL Server setup)
```bash
python procurement_automation.py prod config.ini
```

### Expected Output

```
===========================================================================
PROCUREMENT AUTOMATION SUMMARY
===========================================================================
{
  "import_id": "IMP-20231215120345",
  "environment": "dev",
  "status": "SUCCESS",
  "duration_seconds": 4.32,
  "records": {
    "total_fetched": 250,
    "cleaned": 248,
    "inserted": 150,
    "updated": 98,
    "skipped": 0,
    "errors": 2
  },
  "compliance": {
    "itar_compliant_suppliers": 145,
    "high_risk_suppliers": 8
  }
}
===========================================================================
```

---

## Configuration

### config.ini Structure

```ini
[DEFAULT]
LOG_LEVEL = INFO              # CRITICAL, ERROR, WARNING, INFO, DEBUG
API_TIMEOUT_SECONDS = 30      # API call timeout

[DEV]
ENVIRONMENT = development
DATABASE_URL = sqlite:///./data/bell_procurement_dev.db
API_BASE_URL = http://localhost:8000/ariba-mock
API_RATE_LIMIT_CALLS = 100    # Calls per period
API_RATE_LIMIT_PERIOD = 60    # Seconds
ENABLE_ITAR_LOGGING = true
LOG_FILE = logs/bell_procurement_dev.log
AUDIT_ENABLED = true

[PROD]
ENVIRONMENT = production
DATABASE_URL = mssql+pyodbc://user:pass@server/bell_procurement?driver=ODBC+Driver+17+for+SQL+Server
API_BASE_URL = https://api.ariba.com/v1
API_RATE_LIMIT_CALLS = 500
API_RATE_LIMIT_PERIOD = 60
ENABLE_ITAR_LOGGING = true
REQUIRE_ITAR_VALIDATION = true
```

---

## Data Model

### Supplier Performance Data Fields

| Field | Type | Description | Notes |
|-------|------|-------------|-------|
| `supplier_id` | STRING | Unique identifier | SUPP-00001 format |
| `supplier_name` | STRING | Standardized name | Converted to UPPERCASE |
| `duns_number` | STRING | DUNS identifier | 9 digits, unique key |
| `on_time_delivery_rate` | FLOAT | % on-time delivery | 0-100 range |
| `quality_rejection_rate` | FLOAT | % defects | 0-100 range |
| `lead_time_days` | FLOAT | Average lead time | In calendar days |
| `cost_reduction_score` | FLOAT | Cost savings rating | 1-10 scale |
| `as9100_certified` | BOOLEAN | Aerospace certification | Required for defense |
| `itar_compliant` | BOOLEAN | Export control | Export-controlled tracking |
| `last_audit_date` | STRING | Last quality audit | ISO format (YYYY-MM-DD) |
| `risk_score` | INT | Risk rating | 1-5 scale (5=highest risk) |
| `spend_ytd` | FLOAT | Year-to-date spend | USD amount |

### Database Schema

```sql
-- Suppliers table
CREATE TABLE suppliers (
    supplier_id TEXT PRIMARY KEY,
    supplier_name TEXT NOT NULL,
    duns_number TEXT UNIQUE NOT NULL,
    on_time_delivery_rate REAL,
    quality_rejection_rate REAL,
    lead_time_days REAL,
    cost_reduction_score REAL,
    performance_score REAL,          -- Calculated composite score
    as9100_certified INTEGER,
    itar_compliant INTEGER,
    last_audit_date TEXT,
    risk_score INTEGER,
    spend_ytd REAL,
    created_at TEXT,
    updated_at TEXT,
    is_high_risk INTEGER DEFAULT 0   -- Bell-specific flag
);

-- Audit trail (compliance tracking)
CREATE TABLE audit_trail (
    import_id TEXT PRIMARY KEY,
    environment TEXT,
    import_timestamp TEXT,
    imported_by TEXT,
    total_records INTEGER,
    records_inserted INTEGER,
    records_updated INTEGER,
    records_skipped INTEGER,
    errors_encountered INTEGER,
    itar_records_processed INTEGER,
    validation_status TEXT
);

-- ITAR access log (export control compliance)
CREATE TABLE itar_access_log (
    log_id INTEGER PRIMARY KEY,
    access_timestamp TEXT,
    user_context TEXT,
    supplier_id TEXT,
    action TEXT,                     -- INSERT, UPDATE, READ
    environment TEXT
);

-- Data quality issues tracking
CREATE TABLE data_quality_issues (
    issue_id INTEGER PRIMARY KEY,
    supplier_id TEXT,
    issue_type TEXT,
    issue_description TEXT,
    identified_at TEXT,
    resolved_at TEXT
);
```

---

## Processing Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│  1. AUTHENTICATE & FETCH                                        │
│  - Connect to Ariba API with Bearer token                       │
│  - Handle rate limiting (429 responses)                         │
│  - Paginate through supplier list                               │
│  - Retry on transient failures                                  │
└──────────────────┬──────────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────────┐
│  2. CLEAN & TRANSFORM                                           │
│  - Validate DUNS numbers (9-digit check digit)                  │
│  - Standardize supplier names                                   │
│  - Validate percentages and ranges                              │
│  - Check ITAR/AS9100 compliance flags                           │
│  - Handle missing values strategically                          │
│  - Flag validation errors                                       │
└──────────────────┬──────────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────────┐
│  3. IDENTIFY RISKS                                              │
│  - Flag high-risk suppliers                                     │
│  - Calculate composite performance score                        │
│  - Check audit recency                                          │
│  - Validate compliance for spend level                          │
└──────────────────┬──────────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────────┐
│  4. UPSERT TO DATABASE                                          │
│  - Check if supplier exists (by DUNS)                           │
│  - Insert new records                                           │
│  - Update existing records with new metrics                     │
│  - Log ITAR-compliant access                                    │
│  - Transaction rollback on error                                │
└──────────────────┬──────────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────────┐
│  5. RECORD COMPLIANCE AUDIT TRAIL                               │
│  - Who imported (user context)                                  │
│  - When imported (timestamp)                                    │
│  - How many records (inserted/updated/skipped)                  │
│  - Validation status                                            │
│  - ITAR records processed count                                 │
└──────────────────┬──────────────────────────────────────────────┘
                   │
                   ▼
            ✅ SUCCESS OR FAILURE
```

---

## Key Features Explained

### 1. DUNS Number Validation

DUNS (Data Universal Numbering System) is critical for supplier identification in procurement. The system validates:
- Exactly 9 digits
- Numeric characters only
- Check digit algorithm compliance

```python
# Example
Valid:   "100000001"
Invalid: "10000000"  # Only 8 digits
Invalid: "100000A01"  # Contains letter
```

### 2. Supplier Name Standardization

Handles common variations across legacy systems:
```
Input Variations:
  - "Boeing Co."
  - "Boeing Company"
  - "Boeing Corp."
  - "Boeing Corporation"

Standardized Output:
  - "BOEING CO"
```

### 3. Rate Limiting

Defense APIs often have strict rate limits. The system:
- Tracks request timestamps
- Enforces configurable limits (e.g., 100 calls/60 seconds)
- Automatically backs off with `sleep()`
- Retries on 429 (Too Many Requests)

### 4. ITAR Compliance Logging

ITAR (International Traffic in Arms Regulations) controls export of defense technology. The system:
- Tracks all access to ITAR-compliant suppliers
- Records who accessed data and when
- Maintains audit trail in separate table
- Flags non-compliant suppliers with high spend

### 5. High-Risk Supplier Detection

Multi-factor risk assessment:
- **Financial Risk**: High spend + high risk score
- **Compliance Risk**: ITAR non-compliant with defense work
- **Quality Risk**: Missing AS9100 certification
- **Audit Risk**: Outdated audits (>90 days old)

### 6. Composite Performance Scoring

Weighted formula for overall supplier evaluation:
```
Score = (OnTimeRate × 0.40) +
         ((100 - RejectionRate) × 0.30) +
         (CostScore × 2 × 0.20) +
         ((5 - RiskScore) × 20 × 0.10)

Range: 0-100 (higher = better)
```

---

## Logging

### Log Levels

- **CRITICAL**: System failure, cannot continue
- **ERROR**: Operation failed, recovery attempted
- **WARNING**: Unexpected condition, operation continues
- **INFO**: Normal operation milestones
- **DEBUG**: Detailed diagnostic information

### Log Examples

```
2023-12-15 12:03:45 | bell_procurement | INFO | [_initialize_api_client] | Procurement Automation initialized for dev
2023-12-15 12:03:46 | bell_procurement | INFO | [get_suppliers] | Fetching suppliers - Page: 1, PageSize: 50
2023-12-15 12:03:47 | bell_procurement | WARNING | [_validate_duns_number] | Missing audit date for SUPP-00003, using 2023-11-15
2023-12-15 12:03:48 | bell_procurement | INFO | [_log_itar_access] | ITAR access logged: automation_service performed INSERT on SUPP-00001
2023-12-15 12:04:01 | bell_procurement | INFO | [record_audit_trail] | Audit trail recorded: IMP-20231215120345 - SUCCESS
```

---

## Error Handling

### Recoverable Errors

- **API Rate Limiting (429)**: Automatic retry with backoff
- **Transient Failures (500, 502, 503, 504)**: Retry strategy (3 attempts)
- **Validation Errors**: Record skipped, logged, import continues
- **Integrity Errors**: Skip duplicate record, continue

### Non-Recoverable Errors

- **Authentication Failure**: Full pipeline abort
- **Database Connection**: Full pipeline abort
- **Invalid Configuration**: Full pipeline abort

### Error Response Example

```json
{
  "error": true,
  "status_code": 429,
  "message": "Rate limit exceeded. Retry-After: 60 seconds"
}
```

---

## Sample Data

Use `sample_data.py` for testing:

```bash
python sample_data.py
```

This generates `sample_suppliers.json` with realistic test data including:
- High-performing suppliers (Boeing, Honeywell)
- Problem suppliers (missing certifications, high-risk)
- Various compliance statuses (ITAR/non-ITAR)

---

## Production Deployment

### SQL Server Setup

1. **Install ODBC Driver:**
```bash
# macOS
brew install msodbcsql17 mssql-tools

# Ubuntu
sudo apt-get install odbc-msodbcsql17

# Windows
# Download from Microsoft
```

2. **Update config.ini:**
```ini
[PROD]
DATABASE_URL = mssql+pyodbc://username:password@server.domain.com/bell_procurement?driver=ODBC+Driver+17+for+SQL+Server
```

3. **Environment Variables:**
```bash
export BELL_ENVIRONMENT=prod
export BELL_API_KEY=your-ariba-api-key
export BELL_DB_USER=procurement_user
export BELL_DB_PASSWORD=secure-password
```

4. **Scheduling (Cron job):**
```bash
# Daily import at 2 AM
0 2 * * * /usr/bin/python3 /opt/bell/procurement_automation.py prod config.ini
```

### Security Considerations

- ✅ Never commit API keys or database credentials
- ✅ Use environment variables for sensitive data
- ✅ Enable SQL Server encryption (TDE)
- ✅ Restrict database user permissions (SELECT, INSERT, UPDATE only)
- ✅ Monitor ITAR access logs regularly
- ✅ Audit all supplier data access

---

## Troubleshooting

### Issue: "DUNS number validation failed"
- Check for leading/trailing spaces
- Verify exactly 9 digits
- Ensure no special characters

### Issue: "Rate limit exceeded"
- Check API rate limit configuration
- Monitor request frequency
- May need to increase RATE_LIMIT_PERIOD

### Issue: "Database connection failed"
- Verify database URL is correct
- Check SQL Server is running
- Confirm user permissions
- Check firewall rules

### Issue: "ITAR compliance flag must be boolean"
- Ensure API returns true/false, not "yes"/"no" or 1/0
- Check data cleaning logic

---

## Testing

### Unit Testing (Future Enhancement)

```python
pytest tests/
pytest tests/test_data_cleaner.py -v
pytest tests/test_api_client.py -v
```

### Integration Testing

```bash
# Test with sample data
python -c "
from procurement_automation import *
from sample_data import SAMPLE_SUPPLIER_DATA

cleaner = DataCleaner()
cleaned, errors = cleaner.clean_suppliers(SAMPLE_SUPPLIER_DATA)
print(f'Cleaned: {len(cleaned)}, Errors: {len(errors)}')
"
```

---

## Getting Started (First Time Users)

### Prerequisites
- Python 3.8 or higher
- macOS, Linux, or Windows (with Terminal/PowerShell)
- Git (optional, for version control)

### Installation & Setup

**Step 1: Navigate to project**
```bash
cd "/Users/ammrabbasher/Bell Prep"
```

**Step 2: Create virtual environment (optional but recommended)**
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows
```

**Step 3: Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 4: Verify setup**
```bash
python -m environment_cli info
# Should display 🟢 DEVELOPMENT environment
```

### Your First Run

```bash
# 1. Check which environment you're in
python -m environment_cli info

# 2. Verify everything is working
python -m environment_cli check

# 3. Run the application
export BELL_ENVIRONMENT=dev
python procurement_automation.py dev config.ini
```

**Expected output:** Summary showing suppliers imported/updated with audit trail

### Common Commands You'll Use Every Day

```bash
# Know your environment
python -m environment_cli info

# Verify health
python -m environment_cli check

# Check database
python -m environment_cli database

# Check compliance (important before production!)
python -m environment_cli compliance

# Run the application
python procurement_automation.py dev config.ini

# See recent logs
tail logs/bell_procurement_dev.log
```

**For detailed terminal guidance, see TERMINAL_COMMANDS_GUIDE.md**

### Understanding Your First Week

| Day | What You Do | Commands |
|-----|------------|----------|
| **Day 1** | Setup & explore | `cd`, `python -m environment_cli info`, `ls` |
| **Day 2-3** | Learn environment | `export BELL_ENVIRONMENT=test`, check all 3 environments |
| **Day 4-5** | Try production (approval only!) | `python -m environment_cli validate`, production deployment |
| **Week 2** | Comfortable with workflow | Daily routine with all commands |

---

## Support & Documentation

- **SAP Ariba API Docs**: https://developer.ariba.com/
- **ITAR Compliance**: https://www.pmddtc.state.gov/
- **AS9100 Standard**: https://en.wikipedia.org/wiki/AS9100
- **Python Logging**: https://docs.python.org/3/library/logging.html

---

## Changelog

### v1.0.0 (Initial Release)
- ✅ Ariba API simulation with realistic behaviors
- ✅ Comprehensive data cleaning and validation
- ✅ ITAR compliance logging
- ✅ High-risk supplier detection
- ✅ Database upsert operations
- ✅ Audit trail tracking
- ✅ Multi-environment support (dev/test/prod)

---

## License

Internal - Bell Textron Proprietary

---

## Contact

**Bell Textron Procurement Systems Team**  
For questions or issues, contact your Business Systems Analyst.

