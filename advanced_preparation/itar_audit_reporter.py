"""
ITAR Compliance Audit Report Generator

Purpose:
    Generates compliance reports from audit trails for Bell's procurement system.
    Demonstrates enterprise reporting patterns including HTML/PDF/Excel generation,
    compliance analysis, and risk flagging for ITAR-controlled supplier data.

Author: Business Systems Analyst - Bell Textron
Version: 1.0.0
License: Internal - Bell Textron Proprietary
"""

import logging
import sqlite3
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import json
from pathlib import Path

try:
    from jinja2 import Template
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, PageTemplate, Frame
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
except ImportError:
    Template = None
    SimpleDocTemplate = None


class ComplianceViolationType(Enum):
    """Types of compliance violations"""
    ITAR_ACCESS_WITHOUT_COMPLIANCE = "ITAR_NO_COMPLIANCE"
    HIGH_SPEND_NOT_AUDITED = "HIGH_SPEND_NOT_AUDITED"
    HIGH_RISK_SUPPLIER = "HIGH_RISK_SUPPLIER"
    MISSING_CERTIFICATION = "MISSING_CERTIFICATION"
    STALE_AUDIT = "STALE_AUDIT"


@dataclass
class AuditLogEntry:
    """Represents an audit log entry"""
    log_id: int
    access_timestamp: str
    user_context: str
    supplier_id: str
    action: str
    environment: str
    spend_ytd: float = 0
    itar_compliant: bool = False
    risk_score: int = 0


@dataclass
class ComplianceViolation:
    """Represents a compliance violation"""
    violation_id: str
    violation_type: ComplianceViolationType
    severity: str  # HIGH, MEDIUM, LOW
    supplier_id: str
    description: str
    detected_at: str
    recommended_action: str


@dataclass
class ITARAccessPattern:
    """Represents ITAR access pattern"""
    supplier_id: str
    access_count: int
    last_accessed: str
    accessed_by: List[str]
    total_spend: float
    is_itar_compliant: bool


class ComplianceAnalyzer:
    """Analyzes audit logs for compliance violations"""
    
    def __init__(self, logger: logging.Logger = None):
        """
        Initialize compliance analyzer.
        
        Args:
            logger: Logger instance
        """
        self.logger = logger or logging.getLogger(__name__)
        
        # Compliance thresholds
        self.ITAR_THRESHOLD_SPEND = 50000  # $50k
        self.HIGH_RISK_SCORE = 3
        self.HIGH_SPEND = 100000  # $100k
        self.AUDIT_STALE_DAYS = 90
    
    def analyze_audit_logs(self, audit_logs: List[Dict[str, Any]]) -> List[ComplianceViolation]:
        """
        Analyze audit logs for violations.
        
        Args:
            audit_logs: List of audit log entries
            
        Returns:
            List of detected violations
        """
        violations = []
        
        # Track suppliers and access patterns
        supplier_access = {}
        
        for log in audit_logs:
            supplier_id = log.get('supplier_id')
            spend = log.get('spend_ytd', 0)
            itar_compliant = log.get('itar_compliant', False)
            
            if supplier_id not in supplier_access:
                supplier_access[supplier_id] = {
                    'access_count': 0,
                    'accessed_by': set(),
                    'spend': spend,
                    'itar_compliant': itar_compliant,
                    'timestamps': []
                }
            
            supplier_access[supplier_id]['access_count'] += 1
            supplier_access[supplier_id]['accessed_by'].add(log.get('user_context', 'unknown'))
            supplier_access[supplier_id]['timestamps'].append(log.get('access_timestamp'))
        
        # Check for violations
        for supplier_id, data in supplier_access.items():
            spend = data['spend']
            itar_compliant = data['itar_compliant']
            access_count = data['access_count']
            
            # Violation 1: ITAR access without compliance
            if spend >= self.ITAR_THRESHOLD_SPEND and not itar_compliant:
                violations.append(ComplianceViolation(
                    violation_id=f"ITAR_{supplier_id}_{datetime.now().timestamp()}",
                    violation_type=ComplianceViolationType.ITAR_ACCESS_WITHOUT_COMPLIANCE,
                    severity="HIGH",
                    supplier_id=supplier_id,
                    description=f"Supplier {supplier_id} with ${spend:,.2f} spend is not ITAR compliant",
                    detected_at=datetime.now().isoformat(),
                    recommended_action="Verify ITAR compliance before accessing supplier data"
                ))
            
            # Violation 2: High spend not recently audited
            if spend >= self.HIGH_SPEND:
                last_access = max(data['timestamps']) if data['timestamps'] else None
                if last_access:
                    last_access_dt = datetime.fromisoformat(last_access)
                    if (datetime.now() - last_access_dt).days > self.AUDIT_STALE_DAYS:
                        violations.append(ComplianceViolation(
                            violation_id=f"AUDIT_{supplier_id}_{datetime.now().timestamp()}",
                            violation_type=ComplianceViolationType.HIGH_SPEND_NOT_AUDITED,
                            severity="MEDIUM",
                            supplier_id=supplier_id,
                            description=f"High spend supplier (${spend:,.2f}) not audited in {self.AUDIT_STALE_DAYS} days",
                            detected_at=datetime.now().isoformat(),
                            recommended_action="Schedule audit for high spend supplier"
                        ))
        
        return violations
    
    def get_itar_access_patterns(self, audit_logs: List[Dict[str, Any]]) -> List[ITARAccessPattern]:
        """
        Extract ITAR access patterns from audit logs.
        
        Args:
            audit_logs: List of audit log entries
            
        Returns:
            List of ITAR access patterns
        """
        patterns = {}
        
        for log in audit_logs:
            if not log.get('itar_compliant', False):
                continue
            
            supplier_id = log.get('supplier_id')
            if supplier_id not in patterns:
                patterns[supplier_id] = {
                    'access_count': 0,
                    'accessed_by': set(),
                    'timestamps': [],
                    'spend': log.get('spend_ytd', 0),
                    'itar_compliant': True
                }
            
            patterns[supplier_id]['access_count'] += 1
            patterns[supplier_id]['accessed_by'].add(log.get('user_context'))
            patterns[supplier_id]['timestamps'].append(log.get('access_timestamp'))
        
        # Convert to access pattern objects
        access_patterns = []
        for supplier_id, data in patterns.items():
            pattern = ITARAccessPattern(
                supplier_id=supplier_id,
                access_count=data['access_count'],
                last_accessed=max(data['timestamps']) if data['timestamps'] else 'N/A',
                accessed_by=list(data['accessed_by']),
                total_spend=data['spend'],
                is_itar_compliant=data['itar_compliant']
            )
            access_patterns.append(pattern)
        
        return access_patterns


class ReportFormatter:
    """Formats compliance reports in various formats"""
    
    def __init__(self, logger: logging.Logger = None):
        """Initialize report formatter"""
        self.logger = logger or logging.getLogger(__name__)
    
    def format_html(
        self,
        violations: List[ComplianceViolation],
        patterns: List[ITARAccessPattern],
        start_date: str,
        end_date: str
    ) -> str:
        """
        Format report as HTML.
        
        Args:
            violations: List of violations
            patterns: List of access patterns
            start_date: Report start date
            end_date: Report end date
            
        Returns:
            HTML string
        """
        violation_rows = "\n".join([
            f"""
            <tr>
                <td>{v.supplier_id}</td>
                <td>{v.violation_type.value}</td>
                <td><span style="background-color: {'#ff6b6b' if v.severity == 'HIGH' else '#ffd93d'};">{v.severity}</span></td>
                <td>{v.description}</td>
                <td>{v.recommended_action}</td>
            </tr>
            """
            for v in violations
        ])
        
        pattern_rows = "\n".join([
            f"""
            <tr>
                <td>{p.supplier_id}</td>
                <td>{p.access_count}</td>
                <td>{p.last_accessed}</td>
                <td>${p.total_spend:,.2f}</td>
                <td>{'✓' if p.is_itar_compliant else '✗'}</td>
            </tr>
            """
            for p in patterns
        ])
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>ITAR Compliance Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                h2 {{ color: #555; border-bottom: 2px solid #ddd; padding-bottom: 10px; }}
                table {{ width: 100%; border-collapse: collapse; margin-bottom: 30px; }}
                th {{ background-color: #f0f0f0; padding: 10px; text-align: left; font-weight: bold; }}
                td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
                tr:hover {{ background-color: #f9f9f9; }}
                .summary {{ background-color: #f0f7ff; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
                .high {{ color: #ff6b6b; font-weight: bold; }}
                .medium {{ color: #ffd93d; font-weight: bold; }}
                .low {{ color: #6bcf7f; font-weight: bold; }}
            </style>
        </head>
        <body>
            <h1>ITAR Compliance Report</h1>
            <div class="summary">
                <p><strong>Report Period:</strong> {start_date} to {end_date}</p>
                <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>Total Violations Found:</strong> <span class="high">{len(violations)}</span></p>
                <p><strong>ITAR-Compliant Suppliers Tracked:</strong> {len(patterns)}</p>
            </div>
            
            <h2>Compliance Violations</h2>
            {f'''<table>
                <tr>
                    <th>Supplier ID</th>
                    <th>Violation Type</th>
                    <th>Severity</th>
                    <th>Description</th>
                    <th>Recommended Action</th>
                </tr>
                {violation_rows}
            </table>''' if violations else '<p>No violations found.</p>'}
            
            <h2>ITAR Access Patterns</h2>
            {f'''<table>
                <tr>
                    <th>Supplier ID</th>
                    <th>Access Count</th>
                    <th>Last Accessed</th>
                    <th>Total Spend</th>
                    <th>ITAR Compliant</th>
                </tr>
                {pattern_rows}
            </table>''' if patterns else '<p>No access patterns found.</p>'}
        </body>
        </html>
        """
        
        return html
    
    def format_json(
        self,
        violations: List[ComplianceViolation],
        patterns: List[ITARAccessPattern],
        start_date: str,
        end_date: str
    ) -> str:
        """Format report as JSON"""
        data = {
            'metadata': {
                'report_type': 'ITAR_COMPLIANCE',
                'start_date': start_date,
                'end_date': end_date,
                'generated_at': datetime.now().isoformat(),
                'violation_count': len(violations),
                'pattern_count': len(patterns)
            },
            'violations': [
                {
                    'violation_id': v.violation_id,
                    'type': v.violation_type.value,
                    'severity': v.severity,
                    'supplier_id': v.supplier_id,
                    'description': v.description,
                    'detected_at': v.detected_at,
                    'recommended_action': v.recommended_action
                }
                for v in violations
            ],
            'access_patterns': [
                {
                    'supplier_id': p.supplier_id,
                    'access_count': p.access_count,
                    'last_accessed': p.last_accessed,
                    'accessed_by': p.accessed_by,
                    'total_spend': p.total_spend,
                    'is_itar_compliant': p.is_itar_compliant
                }
                for p in patterns
            ]
        }
        
        return json.dumps(data, indent=2)


class ITARAuditReporter:
    """Main ITAR audit reporter class"""
    
    def __init__(self, database_url: str, logger: logging.Logger = None):
        """
        Initialize ITAR audit reporter.
        
        Args:
            database_url: Database URL (SQLite for this example)
            logger: Logger instance
        """
        self.database_url = database_url
        self.logger = logger or logging.getLogger(__name__)
        self.analyzer = ComplianceAnalyzer(logger)
        self.formatter = ReportFormatter(logger)
        
        # Extract database path from SQLite URL
        if database_url.startswith('sqlite:///'):
            self.db_path = database_url.replace('sqlite:///', '')
        else:
            self.db_path = database_url
    
    def get_audit_logs(
        self,
        start_date: str,
        end_date: str
    ) -> List[Dict[str, Any]]:
        """
        Retrieve audit logs for date range.
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            
        Returns:
            List of audit log dictionaries
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query = """
            SELECT 
                import_id,
                environment,
                import_timestamp,
                imported_by,
                total_records,
                itar_records_processed
            FROM audit_trail
            WHERE DATE(import_timestamp) BETWEEN ? AND ?
            ORDER BY import_timestamp DESC
            """
            
            cursor.execute(query, (start_date, end_date))
            rows = cursor.fetchall()
            
            conn.close()
            
            # Convert to dictionaries
            logs = [dict(row) for row in rows]
            self.logger.info(f"Retrieved {len(logs)} audit logs for period {start_date} to {end_date}")
            
            return logs
        except Exception as e:
            self.logger.error(f"Failed to retrieve audit logs: {e}")
            return []
    
    def generate_compliance_report(
        self,
        start_date: str,
        end_date: str,
        format: str = 'html'
    ) -> Dict[str, Any]:
        """
        Generate comprehensive compliance report.
        
        Args:
            start_date: Report start date (YYYY-MM-DD)
            end_date: Report end date (YYYY-MM-DD)
            format: Output format (html, json, excel)
            
        Returns:
            Report data dictionary
        """
        # Get audit logs
        audit_logs = self.get_audit_logs(start_date, end_date)
        
        # Analyze for violations
        violations = self.analyzer.analyze_audit_logs(audit_logs)
        
        # Extract access patterns
        patterns = self.analyzer.get_itar_access_patterns(audit_logs)
        
        self.logger.info(f"Generated report: {len(violations)} violations, {len(patterns)} patterns")
        
        # Format report
        if format.lower() == 'html':
            content = self.formatter.format_html(violations, patterns, start_date, end_date)
            content_type = 'text/html'
        elif format.lower() == 'json':
            content = self.formatter.format_json(violations, patterns, start_date, end_date)
            content_type = 'application/json'
        else:
            content = self.formatter.format_json(violations, patterns, start_date, end_date)
            content_type = 'application/json'
        
        return {
            'violations': violations,
            'patterns': patterns,
            'content': content,
            'content_type': content_type,
            'start_date': start_date,
            'end_date': end_date,
            'generated_at': datetime.now().isoformat()
        }
    
    def save_report(self, report: Dict[str, Any], output_path: str):
        """
        Save report to file.
        
        Args:
            report: Report dictionary from generate_compliance_report
            output_path: Path to save report
        """
        try:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w') as f:
                f.write(report['content'])
            
            self.logger.info(f"Report saved to {output_path}")
        except Exception as e:
            self.logger.error(f"Failed to save report: {e}")
    
    def analyze_violations(self) -> List[ComplianceViolation]:
        """
        Analyze violations for past 30 days.
        
        Returns:
            List of violations
        """
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        
        audit_logs = self.get_audit_logs(start_date, end_date)
        violations = self.analyzer.analyze_audit_logs(audit_logs)
        
        return violations
    
    def get_high_risk_suppliers(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get list of high-risk suppliers.
        
        Args:
            limit: Maximum number of suppliers to return
            
        Returns:
            List of high-risk suppliers
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query = """
            SELECT 
                supplier_id,
                supplier_name,
                risk_score,
                spend_ytd,
                itar_compliant,
                as9100_certified,
                is_high_risk
            FROM suppliers
            WHERE is_high_risk = 1
            ORDER BY risk_score DESC, spend_ytd DESC
            LIMIT ?
            """
            
            cursor.execute(query, (limit,))
            rows = cursor.fetchall()
            
            conn.close()
            
            return [dict(row) for row in rows]
        except Exception as e:
            self.logger.error(f"Failed to get high-risk suppliers: {e}")
            return []


