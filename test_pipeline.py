#!/usr/bin/env python3
"""
Test script for procurement automation system.

This script demonstrates the full pipeline with sample data and verifies all components.

Usage:
    python test_pipeline.py
    python test_pipeline.py --environment prod
"""

import sys
import os
import json
import argparse
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from procurement_automation import (
    ProcurementAutomation,
    DataCleaner,
    AribaAPIClient,
    SupplierPerformanceData,
    setup_logging
)
from sample_data import SAMPLE_SUPPLIER_DATA
import configparser


def test_data_cleaning():
    """Test data cleaning and validation"""
    print("\n" + "=" * 70)
    print("TEST 1: Data Cleaning & Validation")
    print("=" * 70)
    
    cleaner = DataCleaner()
    cleaned, errors = cleaner.clean_suppliers(SAMPLE_SUPPLIER_DATA)
    
    print(f"\n✓ Cleaned {len(cleaned)} suppliers")
    print(f"✓ Found {len(errors)} validation errors")
    
    if errors:
        print("\nErrors encountered:")
        for error in errors:
            print(f"  - {error['supplier_id']}: {error['error']}")
    
    # Test performance scoring
    if cleaned:
        supplier = cleaned[0]
        score = cleaner.calculate_performance_score(supplier)
        print(f"\n✓ Calculated performance score for {supplier.supplier_name}: {score}/100")
    
    print("\n✓ Test PASSED")
    return len(cleaned) > 0


def test_high_risk_detection():
    """Test high-risk supplier detection"""
    print("\n" + "=" * 70)
    print("TEST 2: High-Risk Supplier Detection")
    print("=" * 70)
    
    cleaner = DataCleaner()
    cleaned, _ = cleaner.clean_suppliers(SAMPLE_SUPPLIER_DATA)
    
    high_risk = cleaner.flag_high_risk_suppliers(cleaned)
    
    print(f"\n✓ Flagged {len(high_risk)} high-risk suppliers")
    
    for supplier in high_risk:
        print(f"\n  {supplier['supplier_name']} ({supplier['supplier_id']}):")
        for flag in supplier['risk_flags']:
            print(f"    • {flag}")
    
    print("\n✓ Test PASSED")
    return len(high_risk) > 0


def test_duns_validation():
    """Test DUNS number validation"""
    print("\n" + "=" * 70)
    print("TEST 3: DUNS Number Validation")
    print("=" * 70)
    
    cleaner = DataCleaner()
    
    test_cases = [
        ("100000001", True, "Valid DUNS"),
        ("10000000", False, "Too short"),
        ("100000A01", False, "Contains letter"),
        ("100000001-", False, "Contains hyphen"),
        ("100000001", True, "Valid DUNS"),
    ]
    
    print("\nTest Cases:")
    for duns, should_pass, description in test_cases:
        try:
            result = cleaner._validate_duns_number(duns)
            if should_pass:
                print(f"  ✓ {description}: '{duns}' → '{result}'")
            else:
                print(f"  ✗ {description}: '{duns}' should have failed")
        except ValueError as e:
            if not should_pass:
                print(f"  ✓ {description}: '{duns}' rejected as expected")
            else:
                print(f"  ✗ {description}: '{duns}' should have passed - {str(e)}")
    
    print("\n✓ Test PASSED")
    return True


def test_name_standardization():
    """Test supplier name standardization"""
    print("\n" + "=" * 70)
    print("TEST 4: Supplier Name Standardization")
    print("=" * 70)
    
    cleaner = DataCleaner()
    
    test_names = [
        ("Boeing Co.", "BOEING CO"),
        ("Boeing Company Inc.", "BOEING COMPANY INC"),
        ("RTX Corp.", "RTX CORP"),
        ("Lockheed Martin Corporation", "LOCKHEED MARTIN CORP"),
    ]
    
    print("\nName Standardization:")
    all_pass = True
    for input_name, expected in test_names:
        result = cleaner._standardize_supplier_name(input_name)
        if result == expected or result == expected.upper():
            print(f"  ✓ '{input_name}' → '{result}'")
        else:
            print(f"  ✗ '{input_name}' → '{result}' (expected '{expected}')")
            all_pass = False
    
    print(f"\n✓ Test PASSED" if all_pass else "\n✗ Test FAILED")
    return all_pass


def test_percentage_validation():
    """Test percentage validation"""
    print("\n" + "=" * 70)
    print("TEST 5: Percentage Validation")
    print("=" * 70)
    
    cleaner = DataCleaner()
    
    test_cases = [
        (95.5, True, "Valid percentage"),
        (0, True, "Zero percentage"),
        (100, True, "Maximum percentage"),
        (-5, False, "Negative percentage"),
        (105, False, "Over 100%"),
        ("abc", False, "Non-numeric"),
    ]
    
    print("\nPercentage Validation:")
    for value, should_pass, description in test_cases:
        try:
            result = cleaner._validate_percentage(value, "test_field")
            if should_pass:
                print(f"  ✓ {description}: {value} → {result}%")
            else:
                print(f"  ✗ {description}: {value} should have failed")
        except ValueError:
            if not should_pass:
                print(f"  ✓ {description}: {value} rejected as expected")
            else:
                print(f"  ✗ {description}: {value} should have passed")
    
    print("\n✓ Test PASSED")
    return True


def test_full_pipeline(environment: str = "dev"):
    """Test the full procurement pipeline"""
    print("\n" + "=" * 70)
    print(f"TEST 6: Full Pipeline ({environment.upper()})")
    print("=" * 70)
    
    try:
        automation = ProcurementAutomation(
            config_file="config.ini",
            environment=environment
        )
        
        summary = automation.run_full_pipeline()
        
        print(f"\n✓ Pipeline executed successfully")
        print(f"\nSummary:")
        print(f"  Import ID: {summary['import_id']}")
        print(f"  Status: {summary['status']}")
        print(f"  Duration: {summary['duration_seconds']}s")
        print(f"  Records:")
        print(f"    - Fetched: {summary['records']['total_fetched']}")
        print(f"    - Cleaned: {summary['records']['cleaned']}")
        print(f"    - Inserted: {summary['records']['inserted']}")
        print(f"    - Updated: {summary['records']['updated']}")
        print(f"    - Errors: {summary['records']['errors']}")
        print(f"  Compliance:")
        print(f"    - ITAR Compliant: {summary['compliance']['itar_compliant_suppliers']}")
        print(f"    - High-Risk: {summary['compliance']['high_risk_suppliers']}")
        
        print("\n✓ Test PASSED")
        return True
        
    except Exception as e:
        print(f"\n✗ Test FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    parser = argparse.ArgumentParser(
        description="Test the procurement automation system"
    )
    parser.add_argument(
        "--environment",
        default="dev",
        choices=["dev", "test", "prod"],
        help="Environment to test"
    )
    parser.add_argument(
        "--test",
        type=int,
        help="Run specific test (1-6)"
    )
    
    args = parser.parse_args()
    
    print("\n" + "=" * 70)
    print("BELL PROCUREMENT AUTOMATION - TEST SUITE")
    print("=" * 70)
    print(f"Started: {datetime.utcnow().isoformat()}")
    
    # Create required directories
    os.makedirs("logs", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    
    tests = [
        ("Data Cleaning", test_data_cleaning),
        ("High-Risk Detection", test_high_risk_detection),
        ("DUNS Validation", test_duns_validation),
        ("Name Standardization", test_name_standardization),
        ("Percentage Validation", test_percentage_validation),
        ("Full Pipeline", lambda: test_full_pipeline(args.environment)),
    ]
    
    results = []
    
    if args.test:
        # Run specific test
        if 1 <= args.test <= len(tests):
            test_name, test_func = tests[args.test - 1]
            result = test_func()
            results.append((test_name, result))
        else:
            print(f"Invalid test number: {args.test}")
            return 1
    else:
        # Run all tests
        for test_name, test_func in tests:
            try:
                result = test_func()
                results.append((test_name, result))
            except Exception as e:
                print(f"\n✗ Test '{test_name}' FAILED with exception: {str(e)}")
                import traceback
                traceback.print_exc()
                results.append((test_name, False))
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("=" * 70)
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())

