"""
ITAR Audit Reporter Example - How to use the compliance report generator

This example demonstrates:
- Generating compliance reports from audit trails
- Analyzing ITAR violations
- Extracting access patterns
- Saving reports in different formats
"""

import logging
from datetime import datetime, timedelta
from advanced_preparation.itar_audit_reporter import (
    ITARAuditReporter,
    ComplianceViolationType
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def example_generate_html_report():
    """Example 1: Generate HTML compliance report"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Generate HTML Report")
    print("="*70)
    
    reporter = ITARAuditReporter(
        database_url='sqlite:///data/bell_procurement_dev.db',
        logger=logger
    )
    
    # Generate report for last 30 days
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    
    report = reporter.generate_compliance_report(
        start_date=start_date,
        end_date=end_date,
        format='html'
    )
    
    print(f"✓ Report generated: {len(report['violations'])} violations found")
    print(f"✓ {len(report['patterns'])} ITAR access patterns tracked")
    
    # Save report
    reporter.save_report(report, 'reports/itar_compliance.html')
    print("✓ Report saved to reports/itar_compliance.html")


def example_generate_json_report():
    """Example 2: Generate JSON compliance report"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Generate JSON Report")
    print("="*70)
    
    reporter = ITARAuditReporter(
        database_url='sqlite:///data/bell_procurement_dev.db',
        logger=logger
    )
    
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    report = reporter.generate_compliance_report(
        start_date=start_date,
        end_date=end_date,
        format='json'
    )
    
    print(f"✓ JSON report generated: {len(report['violations'])} violations")
    
    # Save JSON report
    reporter.save_report(report, 'reports/itar_compliance.json')
    print("✓ Report saved to reports/itar_compliance.json")


def example_analyze_violations():
    """Example 3: Analyze recent violations"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Analyze Recent Violations")
    print("="*70)
    
    reporter = ITARAuditReporter(
        database_url='sqlite:///data/bell_procurement_dev.db',
        logger=logger
    )
    
    # Get violations from last 30 days
    violations = reporter.analyze_violations()
    
    print(f"✓ Found {len(violations)} violations in last 30 days")
    
    # Group by severity
    high_severity = [v for v in violations if v.severity == 'HIGH']
    medium_severity = [v for v in violations if v.severity == 'MEDIUM']
    low_severity = [v for v in violations if v.severity == 'LOW']
    
    print(f"\n  HIGH severity:   {len(high_severity)}")
    print(f"  MEDIUM severity: {len(medium_severity)}")
    print(f"  LOW severity:    {len(low_severity)}")
    
    # Show first few violations
    if violations:
        print(f"\nFirst violation example:")
        v = violations[0]
        print(f"  Type: {v.violation_type.value}")
        print(f"  Supplier: {v.supplier_id}")
        print(f"  Description: {v.description}")
        print(f"  Recommended: {v.recommended_action}")


def example_get_high_risk_suppliers():
    """Example 4: Get high-risk suppliers"""
    print("\n" + "="*70)
    print("EXAMPLE 4: High-Risk Suppliers")
    print("="*70)
    
    reporter = ITARAuditReporter(
        database_url='sqlite:///data/bell_procurement_dev.db',
        logger=logger
    )
    
    high_risk = reporter.get_high_risk_suppliers(limit=5)
    
    print(f"✓ Found {len(high_risk)} high-risk suppliers\n")
    
    if high_risk:
        print(f"{'Supplier':<20} {'Risk Score':<12} {'Spend YTD':<15} {'ITAR':<6}")
        print("-" * 55)
        for supplier in high_risk:
            supplier_id = supplier.get('supplier_id', 'N/A')[:15]
            risk = supplier.get('risk_score', 0)
            spend = supplier.get('spend_ytd', 0)
            itar = "✓" if supplier.get('itar_compliant') else "✗"
            print(f"{supplier_id:<20} {risk:<12} ${spend:>13,.0f} {itar:<6}")


def example_itar_access_patterns():
    """Example 5: Extract ITAR access patterns"""
    print("\n" + "="*70)
    print("EXAMPLE 5: ITAR Access Patterns")
    print("="*70)
    
    reporter = ITARAuditReporter(
        database_url='sqlite:///data/bell_procurement_dev.db',
        logger=logger
    )
    
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    report = reporter.generate_compliance_report(
        start_date=start_date,
        end_date=end_date,
        format='json'
    )
    
    patterns = report['patterns']
    print(f"✓ Found {len(patterns)} ITAR access patterns\n")
    
    if patterns:
        print(f"{'Supplier':<20} {'Accesses':<10} {'Total Spend':<15}")
        print("-" * 45)
        for pattern in patterns[:5]:
            supplier_id = pattern.get('supplier_id', 'N/A')[:15]
            access_count = pattern.get('access_count', 0)
            spend = pattern.get('total_spend', 0)
            print(f"{supplier_id:<20} {access_count:<10} ${spend:>13,.0f}")


if __name__ == "__main__":
    print("\n" + "╔" + "="*68 + "╗")
    print("║ ITAR Audit Reporter Examples".ljust(69) + "║")
    print("╚" + "="*68 + "╝")
    
    print("\nNote: These examples use the dev database at data/bell_procurement_dev.db")
    print("Make sure the database exists with sample data.\n")
    
    # Run examples
    try:
        example_generate_html_report()
        example_generate_json_report()
        example_analyze_violations()
        example_get_high_risk_suppliers()
        example_itar_access_patterns()
    except FileNotFoundError as e:
        print(f"\n✗ Database file not found: {e}")
        print("  Make sure to run procurement_automation.py first to create sample data")
    except Exception as e:
        print(f"\n✗ Error: {e}")
    
    print("\n✓ Examples complete!")

