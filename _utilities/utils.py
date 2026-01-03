"""
Utility script for testing, querying, and analyzing the procurement database.

Usage:
    python utils.py --help
"""

import sqlite3
import argparse
import json
from datetime import datetime
from typing import List, Dict

try:
    import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False


class DatabaseUtility:
    """Utility functions for procurement database operations"""
    
    def __init__(self, database_url: str):
        self.database_path = database_url.replace("sqlite:///", "")
    
    def query_suppliers(self, filters: Dict = None) -> List[Dict]:
        """Query suppliers with optional filters"""
        conn = sqlite3.connect(self.database_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            query = "SELECT * FROM suppliers WHERE 1=1"
            params = []
            
            if filters:
                if "high_risk_only" in filters and filters["high_risk_only"]:
                    query += " AND is_high_risk = 1"
                
                if "itar_only" in filters and filters["itar_only"]:
                    query += " AND itar_compliant = 1"
                
                if "min_spend" in filters:
                    query += " AND spend_ytd >= ?"
                    params.append(filters["min_spend"])
            
            query += " ORDER BY risk_score DESC, spend_ytd DESC"
            
            cursor.execute(query, params)
            results = [dict(row) for row in cursor.fetchall()]
            
            return results
            
        finally:
            conn.close()
    
    def get_high_risk_suppliers(self) -> List[Dict]:
        """Get all high-risk suppliers"""
        return self.query_suppliers({"high_risk_only": True})
    
    def get_itar_suppliers(self) -> List[Dict]:
        """Get all ITAR-compliant suppliers"""
        return self.query_suppliers({"itar_only": True})
    
    def get_performance_stats(self) -> Dict:
        """Get overall supplier performance statistics"""
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        try:
            stats = {}
            
            # Total suppliers
            cursor.execute("SELECT COUNT(*) FROM suppliers")
            stats["total_suppliers"] = cursor.fetchone()[0]
            
            # Average metrics
            cursor.execute("""
                SELECT 
                    ROUND(AVG(on_time_delivery_rate), 2) as avg_on_time,
                    ROUND(AVG(quality_rejection_rate), 2) as avg_rejection,
                    ROUND(AVG(lead_time_days), 2) as avg_lead_time,
                    ROUND(AVG(cost_reduction_score), 2) as avg_cost_score,
                    ROUND(AVG(performance_score), 2) as avg_performance
                FROM suppliers
            """)
            
            row = cursor.fetchone()
            stats["averages"] = {
                "on_time_delivery_rate": row[0],
                "quality_rejection_rate": row[1],
                "lead_time_days": row[2],
                "cost_reduction_score": row[3],
                "performance_score": row[4]
            }
            
            # Certification stats
            cursor.execute("""
                SELECT 
                    SUM(CASE WHEN as9100_certified = 1 THEN 1 ELSE 0 END) as as9100_count,
                    SUM(CASE WHEN itar_compliant = 1 THEN 1 ELSE 0 END) as itar_count,
                    SUM(CASE WHEN is_high_risk = 1 THEN 1 ELSE 0 END) as high_risk_count
                FROM suppliers
            """)
            
            row = cursor.fetchone()
            stats["certifications"] = {
                "as9100_certified": row[0] or 0,
                "itar_compliant": row[1] or 0,
                "high_risk": row[2] or 0
            }
            
            # Spend statistics
            cursor.execute("""
                SELECT 
                    ROUND(SUM(spend_ytd), 2) as total_spend,
                    ROUND(MIN(spend_ytd), 2) as min_spend,
                    ROUND(MAX(spend_ytd), 2) as max_spend,
                    ROUND(AVG(spend_ytd), 2) as avg_spend
                FROM suppliers
            """)
            
            row = cursor.fetchone()
            stats["spend"] = {
                "total_ytd": row[0] or 0,
                "min": row[1] or 0,
                "max": row[2] or 0,
                "average": row[3] or 0
            }
            
            return stats
            
        finally:
            conn.close()
    
    def get_audit_trail(self, limit: int = 10) -> List[Dict]:
        """Get recent import audit trails"""
        conn = sqlite3.connect(self.database_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT * FROM audit_trail
                ORDER BY import_timestamp DESC
                LIMIT ?
            """, (limit,))
            
            results = [dict(row) for row in cursor.fetchall()]
            return results
            
        finally:
            conn.close()
    
    def get_itar_access_log(self, limit: int = 20) -> List[Dict]:
        """Get ITAR access log for compliance audit"""
        conn = sqlite3.connect(self.database_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT * FROM itar_access_log
                ORDER BY access_timestamp DESC
                LIMIT ?
            """, (limit,))
            
            results = [dict(row) for row in cursor.fetchall()]
            return results
            
        finally:
            conn.close()
    
    def export_suppliers_csv(self, output_file: str, filters: Dict = None) -> None:
        """Export suppliers to CSV file"""
        import csv
        
        suppliers = self.query_suppliers(filters)
        
        if not suppliers:
            print("No suppliers to export")
            return
        
        fieldnames = suppliers[0].keys()
        
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(suppliers)
        
        print(f"Exported {len(suppliers)} suppliers to {output_file}")
    
    def print_suppliers_table(
        self,
        suppliers: List[Dict],
        columns: List[str] = None
    ) -> None:
        """Print suppliers as formatted table"""
        if not suppliers:
            print("No suppliers found")
            return
        
        if columns is None:
            columns = [
                "supplier_name", "duns_number", "on_time_delivery_rate",
                "quality_rejection_rate", "performance_score",
                "risk_score", "spend_ytd", "is_high_risk"
            ]
        
        # Filter columns to those that exist
        available_columns = columns if columns else list(suppliers[0].keys())
        
        # Prepare data
        data = []
        for supplier in suppliers:
            row = []
            for col in available_columns:
                value = supplier.get(col, "")
                
                # Format boolean values
                if isinstance(value, int) and col in ["is_high_risk", "as9100_certified", "itar_compliant"]:
                    value = "✓" if value else "✗"
                # Format currency
                elif col == "spend_ytd" and value:
                    value = f"${value:,.0f}"
                # Format percentages
                elif col in ["on_time_delivery_rate", "quality_rejection_rate"] and value:
                    value = f"{value}%"
                
                row.append(value)
            
            data.append(row)
        
        if HAS_TABULATE:
            print(tabulate.tabulate(
                data,
                headers=available_columns,
                tablefmt="grid",
                maxcolwidths=15
            ))
        else:
            # Fallback to simple text output if tabulate not available
            header = " | ".join(f"{col:20}" for col in available_columns)
            print(header)
            print("-" * len(header))
            for row in data:
                print(" | ".join(f"{str(val):20}" for val in row))
    
    def print_stats_summary(self, stats: Dict) -> None:
        """Print statistics summary"""
        print("\n" + "=" * 70)
        print("PROCUREMENT SUPPLIER STATISTICS SUMMARY")
        print("=" * 70)
        
        print(f"\nTotal Suppliers: {stats['total_suppliers']}")
        
        print("\nCertifications & Compliance:")
        print(f"  AS9100 Certified:     {stats['certifications']['as9100_certified']:>3}")
        print(f"  ITAR Compliant:       {stats['certifications']['itar_compliant']:>3}")
        print(f"  High-Risk:            {stats['certifications']['high_risk']:>3}")
        
        print("\nAverage Performance Metrics:")
        avg = stats['averages']
        print(f"  On-Time Delivery:     {avg['on_time_delivery_rate']:>6.2f}%")
        print(f"  Quality Rejection:    {avg['quality_rejection_rate']:>6.2f}%")
        print(f"  Lead Time:            {avg['lead_time_days']:>6.2f} days")
        print(f"  Cost Score:           {avg['cost_reduction_score']:>6.2f}/10")
        print(f"  Performance Score:    {avg['performance_score']:>6.2f}/100")
        
        print("\nYear-to-Date Spend:")
        spend = stats['spend']
        print(f"  Total:                ${spend['total_ytd']:>15,.2f}")
        print(f"  Average per Supplier: ${spend['average']:>15,.2f}")
        print(f"  Min - Max:            ${spend['min']:>15,.2f} - ${spend['max']:>15,.2f}")
        
        print("=" * 70 + "\n")


def main():
    """Main entry point for utility functions"""
    parser = argparse.ArgumentParser(
        description="Procurement database utility and analysis tool"
    )
    
    parser.add_argument(
        "--db",
        default="./data/bell_procurement_dev.db",
        help="Path to database (default: ./data/bell_procurement_dev.db)"
    )
    
    parser.add_argument(
        "--suppliers",
        action="store_true",
        help="List all suppliers"
    )
    
    parser.add_argument(
        "--high-risk",
        action="store_true",
        help="List high-risk suppliers"
    )
    
    parser.add_argument(
        "--itar",
        action="store_true",
        help="List ITAR-compliant suppliers"
    )
    
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show statistics summary"
    )
    
    parser.add_argument(
        "--audit-trail",
        type=int,
        const=10,
        nargs="?",
        help="Show audit trail (optional: number of records, default 10)"
    )
    
    parser.add_argument(
        "--itar-access-log",
        type=int,
        const=20,
        nargs="?",
        help="Show ITAR access log (optional: number of records, default 20)"
    )
    
    parser.add_argument(
        "--export",
        type=str,
        help="Export suppliers to CSV file"
    )
    
    parser.add_argument(
        "--export-high-risk",
        type=str,
        help="Export high-risk suppliers to CSV file"
    )
    
    parser.add_argument(
        "--min-spend",
        type=float,
        help="Filter suppliers by minimum spend (use with --suppliers)"
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )
    
    args = parser.parse_args()
    
    try:
        db_util = DatabaseUtility(f"sqlite:///{args.db}")
        
        # Show statistics
        if args.stats:
            stats = db_util.get_performance_stats()
            if args.json:
                print(json.dumps(stats, indent=2))
            else:
                db_util.print_stats_summary(stats)
        
        # Show suppliers
        elif args.suppliers:
            filters = {}
            if args.min_spend:
                filters["min_spend"] = args.min_spend
            
            suppliers = db_util.query_suppliers(filters)
            
            if args.json:
                print(json.dumps(suppliers, indent=2))
            else:
                db_util.print_suppliers_table(suppliers)
        
        # Show high-risk suppliers
        elif args.high_risk:
            suppliers = db_util.get_high_risk_suppliers()
            
            if args.json:
                print(json.dumps(suppliers, indent=2))
            else:
                print(f"\nHigh-Risk Suppliers ({len(suppliers)}):\n")
                db_util.print_suppliers_table(suppliers)
        
        # Show ITAR suppliers
        elif args.itar:
            suppliers = db_util.get_itar_suppliers()
            
            if args.json:
                print(json.dumps(suppliers, indent=2))
            else:
                print(f"\nITAR-Compliant Suppliers ({len(suppliers)}):\n")
                db_util.print_suppliers_table(suppliers)
        
        # Show audit trail
        elif args.audit_trail is not None:
            audit_trail = db_util.get_audit_trail(args.audit_trail)
            
            if args.json:
                print(json.dumps(audit_trail, indent=2))
            else:
                print(f"\nAudit Trail (last {args.audit_trail} imports):\n")
                for record in audit_trail:
                    print(f"Import ID: {record['import_id']}")
                    print(f"  Timestamp: {record['import_timestamp']}")
                    print(f"  Environment: {record['environment']}")
                    print(f"  Records: {record['records_inserted']} inserted, "
                          f"{record['records_updated']} updated, "
                          f"{record['records_skipped']} skipped")
                    print(f"  Status: {record['validation_status']}")
                    print()
        
        # Show ITAR access log
        elif args.itar_access_log is not None:
            access_log = db_util.get_itar_access_log(args.itar_access_log)
            
            if args.json:
                print(json.dumps(access_log, indent=2))
            else:
                print(f"\nITAR Access Log (last {args.itar_access_log} accesses):\n")
                for record in access_log:
                    print(f"[{record['access_timestamp']}] {record['action']:8} | "
                          f"{record['supplier_id']:12} | User: {record['user_context']}")
                print()
        
        # Export suppliers
        elif args.export:
            db_util.export_suppliers_csv(args.export)
        
        elif args.export_high_risk:
            db_util.export_suppliers_csv(
                args.export_high_risk,
                filters={"high_risk_only": True}
            )
        
        else:
            # Default: show stats
            stats = db_util.get_performance_stats()
            db_util.print_stats_summary(stats)
    
    except FileNotFoundError:
        print(f"Error: Database not found at {args.db}")
        print("Run the main script first to create the database.")
        return 1
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())

