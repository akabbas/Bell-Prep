"""
Data Validation Rules Engine Example - How to use the validation system

This example demonstrates:
- Creating validation rules
- Running validation on supplier data
- Interpreting validation reports
- Data quality scoring
- Custom validation rules
"""

import logging
from advanced_preparation.validation_rules_engine import (
    ValidationRulesEngine,
    ValidationRule,
    ValidationResult,
    ValidationSeverity
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def example_basic_validation():
    """Example 1: Basic validation"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Validation")
    print("="*70)
    
    # Create validation engine
    engine = ValidationRulesEngine(logger=logger)
    
    # Valid supplier data
    valid_supplier = {
        'supplier_id': 'SUPP-001',
        'supplier_name': 'Boeing Corporation',
        'duns_number': '123456789',
        'on_time_delivery_rate': 95.5,
        'quality_rejection_rate': 2.3,
        'lead_time_days': 14,
        'cost_reduction_score': 8.5,
        'spend_ytd': 150000,
        'itar_compliant': True,
        'as9100_certified': True,
        'risk_score': 2
    }
    
    report = engine.validate_supplier(valid_supplier)
    
    print(f"Validation Result: {'✓ PASS' if report.all_passed else '✗ FAIL'}")
    print(f"Quality Score: {report.quality_score.score:.1f}/100")
    print(f"Rules Passed: {report.quality_score.passed_rules}")
    print(f"Rules Failed: {report.quality_score.failed_rules}")


def example_invalid_data():
    """Example 2: Validation with invalid data"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Validation with Invalid Data")
    print("="*70)
    
    engine = ValidationRulesEngine(logger=logger)
    
    # Invalid supplier data
    invalid_supplier = {
        'supplier_id': 'SUPP-002',
        'supplier_name': 'Bad',  # Too short
        'duns_number': '12345',  # Wrong length
        'on_time_delivery_rate': 150,  # > 100
        'quality_rejection_rate': -5,  # Negative
        'lead_time_days': 14,
        'cost_reduction_score': 8.5,
        'spend_ytd': 150000,
        'itar_compliant': False,  # High spend without ITAR!
        'as9100_certified': False,  # High spend without AS9100
        'risk_score': 3
    }
    
    report = engine.validate_supplier(invalid_supplier)
    
    print(f"Validation Result: {'✓ PASS' if report.all_passed else '✗ FAIL'}")
    print(f"Quality Score: {report.quality_score.score:.1f}/100")
    print(f"Confidence: {report.quality_score.confidence_level}")
    
    # Show failed rules
    if report.failed_rules:
        print(f"\nFailed Validations ({len(report.failed_rules)}):")
        for failed in report.failed_rules:
            severity_icon = "✗" if failed.severity == ValidationSeverity.ERROR else "⚠"
            print(f"  {severity_icon} {failed.rule_name}: {failed.message}")


def example_detailed_report():
    """Example 3: Detailed validation report"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Detailed Validation Report")
    print("="*70)
    
    engine = ValidationRulesEngine(logger=logger)
    
    supplier = {
        'supplier_id': 'SUPP-003',
        'supplier_name': 'Raytheon Technologies',
        'duns_number': '123456789',
        'on_time_delivery_rate': 92.0,
        'quality_rejection_rate': 3.5,
        'lead_time_days': 21,
        'cost_reduction_score': 7.0,
        'spend_ytd': 250000,
        'itar_compliant': False,  # This will fail validation
        'as9100_certified': True,
        'risk_score': 4
    }
    
    report = engine.validate_supplier(supplier)
    
    # Print detailed report
    print(report.get_detailed_report())


def example_custom_rule():
    """Example 4: Adding custom validation rules"""
    print("\n" + "="*70)
    print("EXAMPLE 4: Custom Validation Rules")
    print("="*70)
    
    # Create custom rule
    class LeadTimeRule(ValidationRule):
        """Validates reasonable lead times"""
        
        def __init__(self, logger=None):
            super().__init__(
                "LEAD_TIME_VALIDATION",
                ValidationSeverity.WARNING,
                logger
            )
        
        def validate(self, data):
            lead_time = data.get('lead_time_days', 0)
            
            # Flag if lead time is unusually long
            if lead_time > 90:
                return ValidationResult(
                    passed=False,
                    rule_name=self.name,
                    severity=self.severity,
                    message=f"Lead time {lead_time} days is unusually long",
                    value=lead_time
                )
            
            return ValidationResult(
                passed=True,
                rule_name=self.name,
                severity=self.severity,
                message="Lead time is reasonable",
                value=lead_time
            )
    
    # Create engine and add custom rule
    engine = ValidationRulesEngine(logger=logger)
    engine.add_rule(LeadTimeRule(logger))
    
    # Test with long lead time
    supplier = {
        'supplier_id': 'SUPP-004',
        'supplier_name': 'Slow Supplier',
        'duns_number': '123456789',
        'on_time_delivery_rate': 80.0,
        'quality_rejection_rate': 5.0,
        'lead_time_days': 120,  # Very long!
        'cost_reduction_score': 5.0,
        'spend_ytd': 50000,
        'itar_compliant': False,
        'as9100_certified': False,
        'risk_score': 3
    }
    
    report = engine.validate_supplier(supplier)
    
    print(f"Quality Score: {report.quality_score.score:.1f}/100")
    print(f"\nCustom Rule Status:")
    for result in report.results:
        if result.rule_name == "LEAD_TIME_VALIDATION":
            status = "✓ PASS" if result.passed else "✗ FAIL"
            print(f"  {status}: {result.message}")


def example_quality_scores():
    """Example 5: Comparing quality scores"""
    print("\n" + "="*70)
    print("EXAMPLE 5: Quality Score Comparison")
    print("="*70)
    
    engine = ValidationRulesEngine(logger=logger)
    
    # Test different suppliers
    suppliers = {
        'high_quality': {
            'supplier_name': 'High Quality Supplier',
            'duns_number': '111111111',
            'on_time_delivery_rate': 98.0,
            'quality_rejection_rate': 1.0,
            'lead_time_days': 7,
            'spend_ytd': 50000,
            'itar_compliant': True,
            'as9100_certified': True,
        },
        'medium_quality': {
            'supplier_name': 'Medium Quality Supplier',
            'duns_number': '222222222',
            'on_time_delivery_rate': 85.0,
            'quality_rejection_rate': 5.0,
            'lead_time_days': 30,
            'spend_ytd': 75000,
            'itar_compliant': True,
            'as9100_certified': False,
        },
        'low_quality': {
            'supplier_name': 'Low Quality Supplier',
            'duns_number': '333333333',
            'on_time_delivery_rate': 70.0,
            'quality_rejection_rate': 10.0,
            'lead_time_days': 60,
            'spend_ytd': 100000,
            'itar_compliant': False,
            'as9100_certified': False,
        }
    }
    
    print(f"{'Supplier':<25} {'Score':<10} {'Confidence':<15} {'Status':<10}")
    print("-" * 60)
    
    for name, supplier_data in suppliers.items():
        report = engine.validate_supplier(supplier_data)
        score = report.quality_score
        status = "✓ PASS" if report.all_passed else "✗ FAIL"
        
        supplier_name = supplier_data['supplier_name'][:20]
        print(f"{supplier_name:<25} {score.score:<10.1f} {score.confidence_level:<15} {status:<10}")


if __name__ == "__main__":
    print("\n" + "╔" + "="*68 + "╗")
    print("║ Data Validation Rules Engine Examples".ljust(69) + "║")
    print("╚" + "="*68 + "╝")
    
    # Run examples
    try:
        example_basic_validation()
        example_invalid_data()
        example_detailed_report()
        example_custom_rule()
        example_quality_scores()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n✓ Examples complete!")


