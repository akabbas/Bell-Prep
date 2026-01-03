"""
Unit tests for ITAR Compliance Audit Reporter

Tests cover:
- Compliance violation detection
- Access pattern extraction
- Report formatting
- HTML/JSON output generation
"""

import pytest
import logging
import json
from datetime import datetime, timedelta
from advanced_preparation.itar_audit_reporter import (
    ComplianceAnalyzer,
    ReportFormatter,
    ComplianceViolationType,
)


@pytest.fixture
def compliance_analyzer():
    """Create compliance analyzer instance"""
    return ComplianceAnalyzer(logger=logging.getLogger(__name__))


@pytest.fixture
def report_formatter():
    """Create report formatter instance"""
    return ReportFormatter(logger=logging.getLogger(__name__))


@pytest.fixture
def sample_audit_logs():
    """Create sample audit logs for testing"""
    return [
        {
            'supplier_id': 'SUPP-001',
            'user_context': 'user1',
            'access_timestamp': datetime.now().isoformat(),
            'spend_ytd': 150000,
            'itar_compliant': True,
            'risk_score': 2
        },
        {
            'supplier_id': 'SUPP-002',
            'user_context': 'user2',
            'access_timestamp': (datetime.now() - timedelta(days=120)).isoformat(),
            'spend_ytd': 200000,
            'itar_compliant': False,  # Will trigger violation
            'risk_score': 4
        }
    ]


class TestComplianceAnalyzer:
    """Test compliance analysis logic"""
    
    def test_analyzer_initialization(self, compliance_analyzer):
        """Test analyzer initializes correctly"""
        assert compliance_analyzer.ITAR_THRESHOLD_SPEND == 50000
        assert compliance_analyzer.HIGH_RISK_SCORE == 3
        assert compliance_analyzer.HIGH_SPEND == 100000
    
    def test_analyze_audit_logs(self, compliance_analyzer, sample_audit_logs):
        """Test audit log analysis"""
        violations = compliance_analyzer.analyze_audit_logs(sample_audit_logs)
        
        # Should detect ITAR violation for SUPP-002
        assert len(violations) > 0
        itar_violations = [v for v in violations if v.violation_type == ComplianceViolationType.ITAR_ACCESS_WITHOUT_COMPLIANCE]
        assert len(itar_violations) >= 1
    
    def test_access_patterns_extraction(self, compliance_analyzer, sample_audit_logs):
        """Test ITAR access pattern extraction"""
        patterns = compliance_analyzer.get_itar_access_patterns(sample_audit_logs)
        
        # Should extract only ITAR-compliant suppliers
        assert len(patterns) >= 1
        assert all(p.is_itar_compliant for p in patterns)


class TestReportFormatter:
    """Test report formatting"""
    
    def test_html_format(self, report_formatter, sample_audit_logs):
        """Test HTML report formatting"""
        violations = []
        patterns = []
        
        html = report_formatter.format_html(violations, patterns, "2025-01-01", "2025-01-31")
        
        assert "<!DOCTYPE html>" in html
        assert "ITAR Compliance Report" in html
        assert "2025-01-01" in html
        assert "2025-01-31" in html
    
    def test_json_format(self, report_formatter):
        """Test JSON report formatting"""
        violations = []
        patterns = []
        
        json_str = report_formatter.format_json(violations, patterns, "2025-01-01", "2025-01-31")
        
        # Should be valid JSON
        data = json.loads(json_str)
        assert 'metadata' in data
        assert 'violations' in data
        assert 'access_patterns' in data
        assert data['metadata']['report_type'] == 'ITAR_COMPLIANCE'


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


