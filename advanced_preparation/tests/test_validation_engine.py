"""
Unit tests for Data Validation Rules Engine

Tests cover:
- Rule validation
- Data quality scoring
- Custom rule creation
- Validation reporting
"""

import pytest
import logging
from advanced_preparation.validation_rules_engine import (
    ValidationRulesEngine,
    ValidationRule,
    ValidationResult,
    ValidationSeverity,
    DUNSNumberRule,
    SupplierNameRule,
    PercentageRule,
    ITARComplianceRule,
)


@pytest.fixture
def validation_engine():
    """Create validation engine"""
    return ValidationRulesEngine(logger=logging.getLogger(__name__))


@pytest.fixture
def valid_supplier():
    """Create valid supplier data"""
    return {
        'supplier_id': 'SUPP-001',
        'supplier_name': 'Valid Supplier Inc',
        'duns_number': '123456789',
        'on_time_delivery_rate': 95.0,
        'quality_rejection_rate': 2.0,
        'lead_time_days': 14,
        'spend_ytd': 50000,
        'itar_compliant': True,
        'as9100_certified': True,
        'risk_score': 2
    }


@pytest.fixture
def invalid_supplier():
    """Create invalid supplier data"""
    return {
        'supplier_id': 'SUPP-002',
        'supplier_name': 'X',  # Too short
        'duns_number': '12345',  # Wrong length
        'on_time_delivery_rate': 150,  # > 100
        'quality_rejection_rate': -5,  # Negative
        'lead_time_days': 14,
        'spend_ytd': 150000,
        'itar_compliant': False,  # High spend without ITAR!
        'as9100_certified': False,
        'risk_score': 4
    }


class TestDUNSValidation:
    """Test DUNS number validation"""
    
    def test_valid_duns(self):
        """Test valid DUNS number"""
        rule = DUNSNumberRule()
        result = rule.validate({'duns_number': '123456789'})
        assert result.passed is True
    
    def test_invalid_duns_length(self):
        """Test invalid DUNS length"""
        rule = DUNSNumberRule()
        result = rule.validate({'duns_number': '12345'})
        assert result.passed is False
        assert "9 digits" in result.message
    
    def test_invalid_duns_non_numeric(self):
        """Test DUNS with non-numeric characters"""
        rule = DUNSNumberRule()
        result = rule.validate({'duns_number': '12345678A'})
        assert result.passed is False


class TestPercentageValidation:
    """Test percentage field validation"""
    
    def test_valid_percentage(self):
        """Test valid percentage"""
        rule = PercentageRule('on_time_delivery_rate')
        result = rule.validate({'on_time_delivery_rate': 95.5})
        assert result.passed is True
    
    def test_percentage_out_of_range(self):
        """Test percentage > 100"""
        rule = PercentageRule('on_time_delivery_rate')
        result = rule.validate({'on_time_delivery_rate': 150})
        assert result.passed is False
        assert "between 0 and 100" in result.message


class TestITARCompliance:
    """Test ITAR compliance validation"""
    
    def test_high_spend_with_itar(self):
        """Test high spend WITH ITAR compliance"""
        rule = ITARComplianceRule()
        result = rule.validate({
            'spend_ytd': 150000,
            'itar_compliant': True
        })
        assert result.passed is True
    
    def test_high_spend_without_itar(self):
        """Test high spend WITHOUT ITAR compliance"""
        rule = ITARComplianceRule()
        result = rule.validate({
            'spend_ytd': 150000,
            'itar_compliant': False
        })
        assert result.passed is False
        assert "ITAR compliance" in result.message


class TestValidationEngine:
    """Test validation engine"""
    
    def test_validate_valid_supplier(self, validation_engine, valid_supplier):
        """Test validation of valid supplier"""
        report = validation_engine.validate_supplier(valid_supplier)
        
        assert report.all_passed is True
        assert len(report.error_rules) == 0
    
    def test_validate_invalid_supplier(self, validation_engine, invalid_supplier):
        """Test validation of invalid supplier"""
        report = validation_engine.validate_supplier(invalid_supplier)
        
        assert report.all_passed is False
        assert len(report.error_rules) > 0
    
    def test_quality_score_calculation(self, validation_engine, valid_supplier):
        """Test quality score calculation"""
        report = validation_engine.validate_supplier(valid_supplier)
        qs = report.quality_score
        
        assert 0 <= qs.score <= 100
        assert qs.confidence_level in ["HIGH", "MEDIUM", "LOW"]
    
    def test_add_custom_rule(self, validation_engine):
        """Test adding custom rule"""
        class CustomRule(ValidationRule):
            def validate(self, data):
                return ValidationResult(
                    passed=True,
                    rule_name="custom",
                    severity=ValidationSeverity.INFO
                )
        
        validation_engine.add_rule(CustomRule("CUSTOM"))
        
        # Rule should be in engine
        rule_names = [r.name for r in validation_engine.rules]
        assert "CUSTOM" in rule_names


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

