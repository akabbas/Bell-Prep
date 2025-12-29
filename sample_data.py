"""
Sample test data for procurement automation pipeline.
This file provides realistic supplier data for testing without API calls.
"""

import json
from datetime import datetime, timedelta

# Sample supplier data that simulates Ariba API response
SAMPLE_SUPPLIER_DATA = [
    {
        "supplier_id": "SUPP-00001",
        "supplier_name": "Boeing Company Inc.",
        "duns_number": "100000001",
        "on_time_delivery_rate": 94.5,
        "quality_rejection_rate": 0.8,
        "lead_time_days": 45.0,
        "cost_reduction_score": 8.5,
        "as9100_certified": True,
        "itar_compliant": True,
        "last_audit_date": (datetime.utcnow() - timedelta(days=30)).date().isoformat(),
        "risk_score": 1,
        "spend_ytd": 250000.00
    },
    {
        "supplier_id": "SUPP-00002",
        "supplier_name": "Lockheed Martin Corp.",
        "duns_number": "100000002",
        "on_time_delivery_rate": 91.2,
        "quality_rejection_rate": 1.5,
        "lead_time_days": 60.0,
        "cost_reduction_score": 7.2,
        "as9100_certified": True,
        "itar_compliant": True,
        "last_audit_date": (datetime.utcnow() - timedelta(days=45)).date().isoformat(),
        "risk_score": 2,
        "spend_ytd": 180000.00
    },
    {
        "supplier_id": "SUPP-00003",
        "supplier_name": "General Dynamics",
        "duns_number": "100000003",
        "on_time_delivery_rate": 87.3,
        "quality_rejection_rate": 3.2,
        "lead_time_days": 75.0,
        "cost_reduction_score": 5.8,
        "as9100_certified": False,  # Missing critical certification
        "itar_compliant": True,
        "last_audit_date": (datetime.utcnow() - timedelta(days=120)).date().isoformat(),
        "risk_score": 4,  # High risk
        "spend_ytd": 120000.00  # High spend
    },
    {
        "supplier_id": "SUPP-00004",
        "supplier_name": "Honeywell Inc.",
        "duns_number": "100000004",
        "on_time_delivery_rate": 96.1,
        "quality_rejection_rate": 0.5,
        "lead_time_days": 35.0,
        "cost_reduction_score": 9.1,
        "as9100_certified": True,
        "itar_compliant": False,  # Non-ITAR compliant
        "last_audit_date": (datetime.utcnow() - timedelta(days=15)).date().isoformat(),
        "risk_score": 1,
        "spend_ytd": 85000.00
    },
    {
        "supplier_id": "SUPP-00005",
        "supplier_name": "RTX Corporation",
        "duns_number": "100000005",
        "on_time_delivery_rate": 89.7,
        "quality_rejection_rate": 2.1,
        "lead_time_days": 50.0,
        "cost_reduction_score": 7.9,
        "as9100_certified": True,
        "itar_compliant": True,
        "last_audit_date": (datetime.utcnow() - timedelta(days=60)).date().isoformat(),
        "risk_score": 3,
        "spend_ytd": 200000.00
    }
]


def load_sample_data():
    """Return sample supplier data for testing"""
    return SAMPLE_SUPPLIER_DATA


def save_sample_data_to_json(filepath: str):
    """Save sample data to JSON file for reference"""
    with open(filepath, 'w') as f:
        json.dump(SAMPLE_SUPPLIER_DATA, f, indent=2)
    print(f"Sample data saved to {filepath}")


if __name__ == "__main__":
    save_sample_data_to_json("sample_suppliers.json")

