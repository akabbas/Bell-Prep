"""
Bell Textron Procurement Automation System

Purpose: 
    Simulate downloading supplier performance data from SAP Ariba API,
    clean/transform it, and load it to a SQL Server database with
    defense/aerospace-specific compliance requirements (ITAR, AS9100).

Author: Business Systems Analyst - Bell Textron
Version: 1.0.0
License: Internal - Bell Textron Proprietary
"""

import os
import sys
import json
import logging
import configparser
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import time
import random
import sqlite3
from dataclasses import dataclass, asdict
from enum import Enum

import requests
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# ============================================================================
# CONFIGURATION AND CONSTANTS
# ============================================================================

class Environment(Enum):
    """Application environment types"""
    DEV = "development"
    TEST = "testing"
    PROD = "production"


# Bell-specific compliance thresholds
ITAR_THRESHOLD_SPEND = 50000  # Transactions above $50k require ITAR compliance
HIGH_RISK_SPEND_THRESHOLD = 100000
HIGH_RISK_SCORE_THRESHOLD = 3
DUNS_LENGTH = 9

# Aerospace quality standards
REQUIRED_CERTIFICATIONS = {
    "AS9100": "AS9100 Certification (Aerospace Quality Standard)",
    "ITAR": "ITAR Compliance (International Traffic in Arms Regulations)"
}


# ============================================================================
# LOGGING SETUP
# ============================================================================

def setup_logging(config: configparser.ConfigParser, env: str) -> logging.Logger:
    """
    Configure logging with environment-specific settings and ITAR compliance.
    
    For ITAR-sensitive operations, we log:
    - Who accessed the data
    - What data was accessed
    - When it was accessed
    - From which system
    """
    log_level = config.get("DEFAULT", "LOG_LEVEL")
    log_file = config.get(env.upper(), "LOG_FILE")
    
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    logger = logging.getLogger("bell_procurement")
    logger.setLevel(getattr(logging, log_level))
    
    # File handler with ITAR-compliant format
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(getattr(logging, log_level))
    
    # Format includes timestamp, level, and user context for compliance audit trail
    formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | [%(funcName)s] | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class SupplierPerformanceData:
    """
    Represents supplier performance metrics from Ariba.
    
    ITAR Note: Some fields (ITAR_compliant, AS9100_certified) are export-controlled
    and must be logged for compliance audit trail.
    """
    supplier_id: str
    supplier_name: str
    duns_number: str
    on_time_delivery_rate: float  # Percentage
    quality_rejection_rate: float  # Percentage
    lead_time_days: float
    cost_reduction_score: float  # 1-10 scale
    as9100_certified: bool  # Aerospace quality standard
    itar_compliant: bool  # Export control compliance
    last_audit_date: str  # ISO format
    risk_score: int  # 1-5 scale
    spend_ytd: float  # Year-to-date spend in USD
    created_at: str = None  # Timestamp of record creation
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow().isoformat()


@dataclass
class AuditTrail:
    """Bell-specific audit trail for compliance and governance"""
    import_id: str
    environment: str
    import_timestamp: str
    imported_by: str  # User context
    total_records: int
    records_inserted: int
    records_updated: int
    records_skipped: int
    errors_encountered: int
    itar_records_processed: int  # For export control tracking
    validation_status: str  # SUCCESS, PARTIAL_SUCCESS, FAILED


# ============================================================================
# ARIBA API SIMULATION
# ============================================================================

class AribaAPIClient:
    """
    Simulates SAP Ariba Supplier Performance API with realistic behaviors:
    - Authentication with Bearer tokens
    - Rate limiting (429 responses)
    - Pagination
    - Error responses (500, 503)
    - Network delays
    """
    
    def __init__(
        self,
        base_url: str,
        api_key: str,
        rate_limit_calls: int = 100,
        rate_limit_period: int = 60,
        logger: logging.Logger = None
    ):
        self.base_url = base_url
        self.api_key = api_key
        self.rate_limit_calls = rate_limit_calls
        self.rate_limit_period = rate_limit_period
        self.logger = logger or logging.getLogger(__name__)
        
        # Rate limiting tracking
        self.request_times: List[float] = []
        
        # Session with retry strategy
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        """Create session with retry strategy for transient failures"""
        session = requests.Session()
        
        # Retry strategy: retry on 429 (rate limit), 500, 502, 503, 504
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def _check_rate_limit(self) -> None:
        """
        Check and enforce rate limiting.
        Defense APIs often have strict rate limits for security.
        """
        now = time.time()
        
        # Remove old requests outside the rate limit period
        self.request_times = [
            req_time for req_time in self.request_times
            if now - req_time < self.rate_limit_period
        ]
        
        if len(self.request_times) >= self.rate_limit_calls:
            sleep_time = self.rate_limit_period - (now - self.request_times[0])
            self.logger.warning(
                f"Rate limit reached. Sleeping for {sleep_time:.2f} seconds"
            )
            time.sleep(sleep_time)
            self.request_times.clear()
        
        self.request_times.append(now)
    
    def _add_network_delay(self) -> None:
        """Simulate realistic network delay for API calls"""
        delay = random.uniform(0.1, 0.5)
        time.sleep(delay)
    
    def get_suppliers(self, page: int = 1, page_size: int = 100) -> Dict:
        """
        Fetch supplier performance data with pagination.
        
        Args:
            page: Page number (1-indexed)
            page_size: Number of records per page
            
        Returns:
            API response with supplier data and pagination info
        """
        self._check_rate_limit()
        self._add_network_delay()
        
        # Simulate API call
        url = f"{self.base_url}/suppliers"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        params = {
            "page": page,
            "pageSize": page_size
        }
        
        self.logger.info(
            f"Fetching suppliers - Page: {page}, PageSize: {page_size}"
        )
        
        try:
            # For demo, we'll mock the response instead of actual API
            response = self._mock_api_response(page, page_size)
            return response
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed: {str(e)}")
            raise
    
    def _mock_api_response(self, page: int, page_size: int) -> Dict:
        """
        Mock Ariba API response with realistic supplier data.
        In production, this would be replaced with actual API calls.
        """
        # Generate mock suppliers
        total_suppliers = 250
        suppliers = []
        
        # Create deterministic mock data based on page
        start_id = (page - 1) * page_size + 1
        end_id = min(start_id + page_size, total_suppliers + 1)
        
        for i in range(start_id, end_id):
            supplier = {
                "supplier_id": f"SUPP-{i:05d}",
                "supplier_name": self._generate_supplier_name(i),
                "duns_number": f"{100000000 + i:09d}",
                "on_time_delivery_rate": round(
                    random.uniform(85, 99.5), 2
                ),
                "quality_rejection_rate": round(
                    random.uniform(0.1, 5), 2
                ),
                "lead_time_days": round(
                    random.uniform(5, 90), 1
                ),
                "cost_reduction_score": round(
                    random.uniform(1, 10), 2
                ),
                "as9100_certified": random.choice([True, False, True]),
                "itar_compliant": random.choice([True, False, True]),
                "last_audit_date": (
                    datetime.utcnow() - timedelta(days=random.randint(1, 365))
                ).date().isoformat(),
                "risk_score": random.randint(1, 5),
                "spend_ytd": round(
                    random.uniform(10000, 500000), 2
                )
            }
            suppliers.append(supplier)
        
        # Simulate occasional API errors (5% chance per request)
        if random.random() < 0.05:
            self.logger.warning("Simulating API error response")
            return {
                "error": True,
                "status_code": random.choice([429, 500, 503]),
                "message": "Simulated API error"
            }
        
        # Return successful response
        total_pages = (total_suppliers + page_size - 1) // page_size
        
        return {
            "error": False,
            "status_code": 200,
            "data": suppliers,
            "pagination": {
                "current_page": page,
                "page_size": page_size,
                "total_records": total_suppliers,
                "total_pages": total_pages,
                "has_next": page < total_pages
            },
            "metadata": {
                "fetch_timestamp": datetime.utcnow().isoformat(),
                "api_version": "1.0"
            }
        }
    
    def _generate_supplier_name(self, supplier_id: int) -> str:
        """Generate realistic aerospace supplier names"""
        prefixes = [
            "Boeing", "Lockheed Martin", "General Dynamics",
            "RTX", "Northrop Grumman", "L3Harris", "Raytheon",
            "Honeywell", "Collins", "Spirit AeroSystems",
            "Precision", "Advanced", "Strategic", "Integrated"
        ]
        
        suffixes = [
            "Corp", "Company", "Industries", "Systems",
            "Manufacturing", "Solutions", "Technologies",
            "Defense", "Aerospace", "Supply"
        ]
        
        prefix = random.choice(prefixes)
        suffix = random.choice(suffixes)
        
        # Add variation to test name standardization
        variations = [
            f"{prefix} {suffix}",
            f"{prefix} {suffix} Inc.",
            f"{prefix} {suffix}, Inc.",
            f"{prefix} {suffix} Corporation"
        ]
        
        return random.choice(variations)


# ============================================================================
# DATA CLEANING AND TRANSFORMATION
# ============================================================================

class DataCleaner:
    """
    Cleans and validates supplier performance data.
    
    Bell-specific logic:
    - Validates DUNS numbers (critical for supplier identification)
    - Standardizes supplier names (multiple formats in legacy systems)
    - Validates ITAR and AS9100 compliance flags
    - Flags high-risk suppliers
    - Handles missing values strategically
    """
    
    def __init__(self, logger: logging.Logger = None):
        self.logger = logger or logging.getLogger(__name__)
        self.validation_errors: List[Dict] = []
    
    def clean_suppliers(
        self,
        suppliers: List[Dict]
    ) -> Tuple[List[SupplierPerformanceData], List[Dict]]:
        """
        Clean and validate supplier data.
        
        Returns:
            Tuple of (cleaned_suppliers, error_records)
        """
        cleaned = []
        errors = []
        
        self.logger.info(f"Cleaning {len(suppliers)} supplier records")
        
        for supplier_data in suppliers:
            try:
                cleaned_record = self._clean_record(supplier_data)
                cleaned.append(cleaned_record)
            except ValueError as e:
                self.logger.warning(
                    f"Record rejected: {supplier_data.get('supplier_id')} - {str(e)}"
                )
                errors.append({
                    "supplier_id": supplier_data.get("supplier_id"),
                    "error": str(e),
                    "timestamp": datetime.utcnow().isoformat()
                })
        
        self.logger.info(
            f"Cleaned {len(cleaned)} records, {len(errors)} errors"
        )
        return cleaned, errors
    
    def _clean_record(self, record: Dict) -> SupplierPerformanceData:
        """Clean a single supplier record"""
        
        # Validate required fields
        required_fields = [
            "supplier_id", "supplier_name", "duns_number",
            "on_time_delivery_rate", "quality_rejection_rate",
            "lead_time_days", "cost_reduction_score",
            "as9100_certified", "itar_compliant",
            "risk_score", "spend_ytd"
        ]
        
        for field in required_fields:
            if field not in record or record[field] is None:
                raise ValueError(f"Missing required field: {field}")
        
        # Clean DUNS number
        duns = self._validate_duns_number(record["duns_number"])
        
        # Standardize supplier name
        supplier_name = self._standardize_supplier_name(
            record["supplier_name"]
        )
        
        # Validate and clean numeric fields
        on_time_rate = self._validate_percentage(
            record["on_time_delivery_rate"],
            "on_time_delivery_rate"
        )
        
        quality_rate = self._validate_percentage(
            record["quality_rejection_rate"],
            "quality_rejection_rate"
        )
        
        lead_time = self._validate_positive_number(
            record["lead_time_days"],
            "lead_time_days"
        )
        
        cost_score = self._validate_range(
            record["cost_reduction_score"],
            1, 10,
            "cost_reduction_score"
        )
        
        risk_score = self._validate_range(
            record["risk_score"],
            1, 5,
            "risk_score"
        )
        
        spend = self._validate_positive_number(
            record["spend_ytd"],
            "spend_ytd"
        )
        
        # Validate last audit date (should be recent for aerospace)
        last_audit = record.get("last_audit_date")
        if not last_audit:
            # Use 30 days ago if missing
            last_audit = (
                datetime.utcnow() - timedelta(days=30)
            ).date().isoformat()
            self.logger.warning(
                f"Missing audit date for {record['supplier_id']}, "
                f"using {last_audit}"
            )
        
        # ITAR compliance checks (CRITICAL FOR DEFENSE)
        if not isinstance(record.get("itar_compliant"), bool):
            raise ValueError(
                f"ITAR compliance flag must be boolean for {record['supplier_id']}"
            )
        
        if not isinstance(record.get("as9100_certified"), bool):
            raise ValueError(
                f"AS9100 certification flag must be boolean for {record['supplier_id']}"
            )
        
        # Create cleaned record
        return SupplierPerformanceData(
            supplier_id=record["supplier_id"],
            supplier_name=supplier_name,
            duns_number=duns,
            on_time_delivery_rate=on_time_rate,
            quality_rejection_rate=quality_rate,
            lead_time_days=lead_time,
            cost_reduction_score=cost_score,
            as9100_certified=record["as9100_certified"],
            itar_compliant=record["itar_compliant"],
            last_audit_date=last_audit,
            risk_score=risk_score,
            spend_ytd=spend
        )
    
    def _validate_duns_number(self, duns: str) -> str:
        """
        Validate DUNS number (9 digits with check digit).
        
        DUNS numbers are critical for supplier identification in defense
        procurement and must be validated before database insertion.
        """
        if not duns:
            raise ValueError("DUNS number cannot be empty")
        
        # Remove spaces and hyphens first
        duns_clean = str(duns).replace("-", "").replace(" ", "").strip()
        
        if not duns_clean.isdigit():
            raise ValueError(f"DUNS number contains non-numeric characters: {duns}")
        
        if len(duns_clean) != DUNS_LENGTH:
            raise ValueError(
                f"DUNS number must be {DUNS_LENGTH} digits, got {len(duns_clean)}"
            )
        
        return duns_clean
    
    def _standardize_supplier_name(self, name: str) -> str:
        """
        Standardize supplier names for consistent matching.
        
        Legacy systems often have variations like:
        - "Boeing Co." vs "Boeing Company"
        - "RTX Corp" vs "Raytheon Technologies"
        """
        if not name:
            raise ValueError("Supplier name cannot be empty")
        
        name = name.strip().upper()
        
        # Common replacements
        replacements = {
            " INC.": " INC",
            " INC,": " INC",
            " CORP.": " CORP",
            " CORPORATION": " CORP",
            " CO.": " CO",
            " COMPANY": " CO",
            " LLC": " LLC",
            " L.L.C.": " LLC",
        }
        
        for old, new in replacements.items():
            name = name.replace(old, new)
        
        return name
    
    def _validate_percentage(self, value: float, field_name: str) -> float:
        """Validate that value is a valid percentage (0-100)"""
        try:
            num = float(value)
            if not 0 <= num <= 100:
                raise ValueError(
                    f"{field_name} must be between 0 and 100, got {num}"
                )
            return round(num, 2)
        except (ValueError, TypeError):
            raise ValueError(f"{field_name} must be a number, got {value}")
    
    def _validate_positive_number(
        self, value: float, field_name: str
    ) -> float:
        """Validate that value is a positive number"""
        try:
            num = float(value)
            if num < 0:
                raise ValueError(
                    f"{field_name} must be positive, got {num}"
                )
            return round(num, 2)
        except (ValueError, TypeError):
            raise ValueError(f"{field_name} must be a number, got {value}")
    
    def _validate_range(
        self, value: float, min_val: float, max_val: float, field_name: str
    ) -> int:
        """Validate that value is within a specific range"""
        try:
            num = int(float(value))
            if not min_val <= num <= max_val:
                raise ValueError(
                    f"{field_name} must be between {min_val} and {max_val}, "
                    f"got {num}"
                )
            return num
        except (ValueError, TypeError):
            raise ValueError(f"{field_name} must be a number, got {value}")
    
    def flag_high_risk_suppliers(
        self,
        suppliers: List[SupplierPerformanceData]
    ) -> List[Dict]:
        """
        Flag suppliers that meet high-risk criteria.
        
        High-risk definition for Bell:
        - risk_score > 3 AND spend_ytd > $100,000
        - Missing recent audit (> 90 days old)
        - Not ITAR compliant but receiving defense work
        - AS9100 certification missing
        """
        high_risk = []
        
        for supplier in suppliers:
            risk_flags = []
            
            # Check risk score + spend combination
            if (supplier.risk_score > HIGH_RISK_SCORE_THRESHOLD and
                supplier.spend_ytd > HIGH_RISK_SPEND_THRESHOLD):
                risk_flags.append(
                    f"High risk score ({supplier.risk_score}) with "
                    f"high spend (${supplier.spend_ytd:,.0f})"
                )
            
            # Check audit recency
            audit_date = datetime.fromisoformat(supplier.last_audit_date)
            days_since_audit = (datetime.utcnow() - audit_date).days
            if days_since_audit > 90:
                risk_flags.append(
                    f"Audit outdated ({days_since_audit} days old)"
                )
            
            # Check ITAR compliance for high-spend suppliers
            if supplier.spend_ytd > ITAR_THRESHOLD_SPEND and \
               not supplier.itar_compliant:
                risk_flags.append(
                    f"ITAR non-compliant with spend ${supplier.spend_ytd:,.0f}"
                )
            
            # Check AS9100 certification
            if not supplier.as9100_certified:
                risk_flags.append("AS9100 certification missing")
            
            if risk_flags:
                high_risk.append({
                    "supplier_id": supplier.supplier_id,
                    "supplier_name": supplier.supplier_name,
                    "risk_flags": risk_flags,
                    "identified_at": datetime.utcnow().isoformat()
                })
        
        if high_risk:
            self.logger.warning(
                f"Identified {len(high_risk)} high-risk suppliers"
            )
        
        return high_risk
    
    def calculate_performance_score(
        self,
        supplier: SupplierPerformanceData
    ) -> float:
        """
        Calculate composite performance score for supplier.
        
        Weights:
        - On-time delivery: 40% (most important for aerospace)
        - Quality: 30% (critical for safety-critical parts)
        - Cost reduction: 20% (business efficiency)
        - Risk score: 10% (negative weight - lower is better)
        
        Scale: 0-100
        """
        score = (
            (supplier.on_time_delivery_rate * 0.40) +
            ((100 - supplier.quality_rejection_rate) * 0.30) +
            (supplier.cost_reduction_score * 2 * 0.20) +  # Scale to 0-100
            ((5 - supplier.risk_score) * 20 * 0.10)  # Inverse: lower risk = higher score
        )
        
        return round(min(100, max(0, score)), 2)


# ============================================================================
# DATABASE OPERATIONS
# ============================================================================

class ProcurementDatabase:
    """
    Handle database operations for supplier performance data.
    
    Features:
    - Upsert logic (update existing, insert new)
    - Audit trail logging
    - ITAR compliance tracking
    - Data validation before commit
    - Transaction management
    """
    
    def __init__(
        self,
        database_url: str,
        logger: logging.Logger = None,
        environment: str = "dev"
    ):
        self.database_url = database_url
        self.logger = logger or logging.getLogger(__name__)
        self.environment = environment
        
        # Initialize database if needed
        self._initialize_database()
    
    def _initialize_database(self) -> None:
        """Create database tables if they don't exist"""
        
        # For SQLite simulation of SQL Server
        conn = sqlite3.connect(self.database_url.replace("sqlite:///", ""))
        cursor = conn.cursor()
        
        try:
            # Suppliers table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS suppliers (
                    supplier_id TEXT PRIMARY KEY,
                    supplier_name TEXT NOT NULL,
                    duns_number TEXT UNIQUE NOT NULL,
                    on_time_delivery_rate REAL,
                    quality_rejection_rate REAL,
                    lead_time_days REAL,
                    cost_reduction_score REAL,
                    performance_score REAL,
                    as9100_certified INTEGER,
                    itar_compliant INTEGER,
                    last_audit_date TEXT,
                    risk_score INTEGER,
                    spend_ytd REAL,
                    created_at TEXT,
                    updated_at TEXT,
                    is_high_risk INTEGER DEFAULT 0
                )
            """)
            
            # Audit trail table (for compliance)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS audit_trail (
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
                )
            """)
            
            # ITAR access log (export control compliance)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS itar_access_log (
                    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    access_timestamp TEXT,
                    user_context TEXT,
                    supplier_id TEXT,
                    action TEXT,
                    environment TEXT,
                    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
                )
            """)
            
            # Data quality issues tracking
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS data_quality_issues (
                    issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    supplier_id TEXT,
                    issue_type TEXT,
                    issue_description TEXT,
                    identified_at TEXT,
                    resolved_at TEXT
                )
            """)
            
            conn.commit()
            self.logger.info("Database initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Database initialization failed: {str(e)}")
            raise
        finally:
            conn.close()
    
    def upsert_suppliers(
        self,
        suppliers: List[SupplierPerformanceData],
        high_risk_suppliers: List[Dict],
        import_id: str,
        user_context: str = "system"
    ) -> Tuple[int, int, int]:
        """
        Upsert supplier records (insert new, update existing).
        
        Returns:
            Tuple of (inserted, updated, skipped) counts
        """
        conn = sqlite3.connect(self.database_url.replace("sqlite:///", ""))
        cursor = conn.cursor()
        
        inserted = 0
        updated = 0
        skipped = 0
        now = datetime.utcnow().isoformat()
        
        try:
            for supplier in suppliers:
                try:
                    # Check if supplier exists
                    cursor.execute(
                        "SELECT supplier_id FROM suppliers WHERE duns_number = ?",
                        (supplier.duns_number,)
                    )
                    existing = cursor.fetchone()
                    
                    # Check if high-risk
                    is_high_risk = any(
                        h["supplier_id"] == supplier.supplier_id
                        for h in high_risk_suppliers
                    )
                    
                    # Calculate performance score
                    cleaner = DataCleaner()
                    performance_score = cleaner.calculate_performance_score(
                        supplier
                    )
                    
                    if existing:
                        # Update existing record
                        cursor.execute("""
                            UPDATE suppliers SET
                                supplier_name = ?,
                                on_time_delivery_rate = ?,
                                quality_rejection_rate = ?,
                                lead_time_days = ?,
                                cost_reduction_score = ?,
                                performance_score = ?,
                                as9100_certified = ?,
                                itar_compliant = ?,
                                last_audit_date = ?,
                                risk_score = ?,
                                spend_ytd = ?,
                                updated_at = ?,
                                is_high_risk = ?
                            WHERE supplier_id = ?
                        """, (
                            supplier.supplier_name,
                            supplier.on_time_delivery_rate,
                            supplier.quality_rejection_rate,
                            supplier.lead_time_days,
                            supplier.cost_reduction_score,
                            performance_score,
                            supplier.as9100_certified,
                            supplier.itar_compliant,
                            supplier.last_audit_date,
                            supplier.risk_score,
                            supplier.spend_ytd,
                            now,
                            1 if is_high_risk else 0,
                            supplier.supplier_id
                        ))
                        updated += 1
                        
                        # Log ITAR access if applicable
                        if supplier.itar_compliant:
                            self._log_itar_access(
                                cursor, user_context, supplier.supplier_id,
                                "UPDATE", import_id
                            )
                        
                        self.logger.debug(
                            f"Updated supplier: {supplier.supplier_id}"
                        )
                    else:
                        # Insert new record
                        cursor.execute("""
                            INSERT INTO suppliers (
                                supplier_id, supplier_name, duns_number,
                                on_time_delivery_rate, quality_rejection_rate,
                                lead_time_days, cost_reduction_score,
                                performance_score, as9100_certified,
                                itar_compliant, last_audit_date,
                                risk_score, spend_ytd,
                                created_at, updated_at, is_high_risk
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            supplier.supplier_id,
                            supplier.supplier_name,
                            supplier.duns_number,
                            supplier.on_time_delivery_rate,
                            supplier.quality_rejection_rate,
                            supplier.lead_time_days,
                            supplier.cost_reduction_score,
                            performance_score,
                            supplier.as9100_certified,
                            supplier.itar_compliant,
                            supplier.last_audit_date,
                            supplier.risk_score,
                            supplier.spend_ytd,
                            now,
                            now,
                            1 if is_high_risk else 0
                        ))
                        inserted += 1
                        
                        # Log ITAR access if applicable
                        if supplier.itar_compliant:
                            self._log_itar_access(
                                cursor, user_context, supplier.supplier_id,
                                "INSERT", import_id
                            )
                        
                        self.logger.debug(
                            f"Inserted supplier: {supplier.supplier_id}"
                        )
                
                except sqlite3.IntegrityError as e:
                    skipped += 1
                    self.logger.warning(
                        f"Integrity error for {supplier.supplier_id}: {str(e)}"
                    )
            
            conn.commit()
            self.logger.info(
                f"Upsert complete: {inserted} inserted, {updated} updated, "
                f"{skipped} skipped"
            )
            
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Upsert failed: {str(e)}")
            raise
        finally:
            conn.close()
        
        return inserted, updated, skipped
    
    def _log_itar_access(
        self,
        cursor: sqlite3.Cursor,
        user_context: str,
        supplier_id: str,
        action: str,
        import_id: str
    ) -> None:
        """
        Log ITAR-compliant supplier access for audit trail.
        
        ITAR regulations require tracking who accessed export-controlled
        supplier data and when.
        """
        cursor.execute("""
            INSERT INTO itar_access_log (
                access_timestamp, user_context, supplier_id, action, environment
            ) VALUES (?, ?, ?, ?, ?)
        """, (
            datetime.utcnow().isoformat(),
            user_context,
            supplier_id,
            action,
            self.environment
        ))
        
        self.logger.info(
            f"ITAR access logged: {user_context} performed {action} on "
            f"{supplier_id}"
        )
    
    def record_audit_trail(
        self,
        audit_trail: AuditTrail
    ) -> None:
        """Record audit trail for governance and compliance"""
        conn = sqlite3.connect(self.database_url.replace("sqlite:///", ""))
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO audit_trail (
                    import_id, environment, import_timestamp,
                    imported_by, total_records, records_inserted,
                    records_updated, records_skipped, errors_encountered,
                    itar_records_processed, validation_status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                audit_trail.import_id,
                audit_trail.environment,
                audit_trail.import_timestamp,
                audit_trail.imported_by,
                audit_trail.total_records,
                audit_trail.records_inserted,
                audit_trail.records_updated,
                audit_trail.records_skipped,
                audit_trail.errors_encountered,
                audit_trail.itar_records_processed,
                audit_trail.validation_status
            ))
            
            conn.commit()
            self.logger.info(
                f"Audit trail recorded: {audit_trail.import_id} - "
                f"{audit_trail.validation_status}"
            )
            
        finally:
            conn.close()
    
    def get_high_risk_suppliers(self) -> List[Dict]:
        """Query high-risk suppliers from database"""
        conn = sqlite3.connect(self.database_url.replace("sqlite:///", ""))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT supplier_id, supplier_name, risk_score,
                       spend_ytd, as9100_certified, itar_compliant
                FROM suppliers
                WHERE is_high_risk = 1
                ORDER BY risk_score DESC, spend_ytd DESC
            """)
            
            results = [dict(row) for row in cursor.fetchall()]
            return results
            
        finally:
            conn.close()


# ============================================================================
# MAIN ORCHESTRATION
# ============================================================================

class ProcurementAutomation:
    """
    Main orchestrator for the procurement automation pipeline.
    
    Process:
    1. Authenticate with Ariba API
    2. Fetch supplier performance data (with pagination)
    3. Clean and transform data
    4. Flag high-risk suppliers
    5. Load to database with upsert logic
    6. Record audit trail for compliance
    """
    
    def __init__(
        self,
        config_file: str,
        environment: str = "dev",
        api_key: str = None
    ):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        
        self.environment = environment.upper()
        self.api_key = api_key or "mock-api-key-12345"
        
        # Setup logging
        self.logger = setup_logging(self.config, environment)
        
        # Initialize components
        self.api_client = self._initialize_api_client()
        self.data_cleaner = DataCleaner(logger=self.logger)
        self.database = ProcurementDatabase(
            database_url=self.config.get(
                self.environment, "DATABASE_URL"
            ),
            logger=self.logger,
            environment=environment
        )
        
        self.logger.info(
            f"Procurement Automation initialized for {environment}"
        )
    
    def _initialize_api_client(self) -> AribaAPIClient:
        """Initialize Ariba API client with config"""
        return AribaAPIClient(
            base_url=self.config.get(
                self.environment, "API_BASE_URL"
            ),
            api_key=self.api_key,
            rate_limit_calls=self.config.getint(
                self.environment, "API_RATE_LIMIT_CALLS"
            ),
            rate_limit_period=self.config.getint(
                self.environment, "API_RATE_LIMIT_PERIOD"
            ),
            logger=self.logger
        )
    
    def run_full_pipeline(self) -> Dict:
        """
        Execute the complete procurement automation pipeline.
        
        Returns:
            Dictionary with execution summary
        """
        import_id = f"IMP-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        self.logger.info(f"Starting procurement import: {import_id}")
        
        start_time = time.time()
        
        # Initialize tracking
        total_records = 0
        all_suppliers = []
        all_errors = []
        itar_count = 0
        validation_status = "SUCCESS"
        
        try:
            # Step 1: Fetch data from Ariba API
            self.logger.info("Step 1: Fetching supplier data from Ariba API")
            page = 1
            max_pages = 5  # Limit for demo
            
            while page <= max_pages:
                try:
                    response = self.api_client.get_suppliers(
                        page=page,
                        page_size=50
                    )
                    
                    if response.get("error"):
                        self.logger.error(
                            f"API error on page {page}: "
                            f"{response.get('message')}"
                        )
                        if response.get("status_code") == 429:
                            # Rate limited, wait and retry
                            self.logger.warning("Rate limited, retrying...")
                            time.sleep(5)
                            continue
                        else:
                            validation_status = "PARTIAL_SUCCESS"
                            break
                    
                    suppliers = response.get("data", [])
                    total_records += len(suppliers)
                    all_suppliers.extend(suppliers)
                    
                    self.logger.info(
                        f"Fetched page {page}: {len(suppliers)} suppliers"
                    )
                    
                    # Check if there are more pages
                    has_next = response.get("pagination", {}).get("has_next")
                    if not has_next:
                        break
                    
                    page += 1
                    
                except Exception as e:
                    self.logger.error(f"Failed to fetch page {page}: {str(e)}")
                    validation_status = "PARTIAL_SUCCESS"
                    break
            
            self.logger.info(
                f"Fetched {total_records} total supplier records from API"
            )
            
            # Step 2: Clean and transform data
            self.logger.info("Step 2: Cleaning and transforming data")
            cleaned_suppliers, errors = self.data_cleaner.clean_suppliers(
                all_suppliers
            )
            all_errors.extend(errors)
            
            # Count ITAR-compliant suppliers
            itar_count = sum(
                1 for s in cleaned_suppliers if s.itar_compliant
            )
            
            self.logger.info(
                f"Cleaned {len(cleaned_suppliers)} suppliers, "
                f"{itar_count} ITAR-compliant"
            )
            
            # Step 3: Flag high-risk suppliers
            self.logger.info("Step 3: Identifying high-risk suppliers")
            high_risk = self.data_cleaner.flag_high_risk_suppliers(
                cleaned_suppliers
            )
            self.logger.info(f"Flagged {len(high_risk)} high-risk suppliers")
            
            # Step 4: Load to database
            self.logger.info("Step 4: Loading data to database")
            inserted, updated, skipped = self.database.upsert_suppliers(
                cleaned_suppliers,
                high_risk,
                import_id,
                user_context="automation_service"
            )
            
            # Step 5: Record audit trail
            self.logger.info("Step 5: Recording audit trail")
            audit_trail = AuditTrail(
                import_id=import_id,
                environment=self.environment.lower(),
                import_timestamp=datetime.utcnow().isoformat(),
                imported_by="automation_service",
                total_records=len(cleaned_suppliers),
                records_inserted=inserted,
                records_updated=updated,
                records_skipped=skipped,
                errors_encountered=len(all_errors),
                itar_records_processed=itar_count,
                validation_status=validation_status
            )
            
            self.database.record_audit_trail(audit_trail)
            
        except Exception as e:
            self.logger.error(f"Pipeline execution failed: {str(e)}")
            validation_status = "FAILED"
            raise
        
        # Generate summary
        duration = time.time() - start_time
        
        summary = {
            "import_id": import_id,
            "environment": self.environment.lower(),
            "status": validation_status,
            "duration_seconds": round(duration, 2),
            "records": {
                "total_fetched": total_records,
                "cleaned": len(cleaned_suppliers),
                "inserted": inserted,
                "updated": updated,
                "skipped": skipped,
                "errors": len(all_errors)
            },
            "compliance": {
                "itar_compliant_suppliers": itar_count,
                "high_risk_suppliers": len(high_risk)
            }
        }
        
        self.logger.info(f"Pipeline complete: {json.dumps(summary, indent=2)}")
        
        return summary


# ============================================================================
# ENTRY POINT
# ============================================================================

def main():
    """Main entry point"""
    import sys
    
    # Get environment from command line or default to dev
    environment = sys.argv[1] if len(sys.argv) > 1 else "dev"
    
    # Get config file path
    config_file = sys.argv[2] if len(sys.argv) > 2 else "config.ini"
    
    try:
        # Initialize automation system
        automation = ProcurementAutomation(
            config_file=config_file,
            environment=environment
        )
        
        # Run the full pipeline
        summary = automation.run_full_pipeline()
        
        # Print summary
        print("\n" + "=" * 70)
        print("PROCUREMENT AUTOMATION SUMMARY")
        print("=" * 70)
        print(json.dumps(summary, indent=2))
        print("=" * 70)
        
        # Return success
        return 0
        
    except Exception as e:
        print(f"FATAL ERROR: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

