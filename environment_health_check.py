"""
Bell Textron Environment Health Check Utilities

Purpose:
    Provides health check and status verification functions for the procurement
    automation system. These utilities help diagnose environment issues and
    verify that critical systems are operational before processing data.

Author: Business Systems Analyst - Bell Textron
Version: 1.0.0
License: Internal - Bell Textron Proprietary
"""

import os
import sys
import logging
import sqlite3
import json
from typing import Dict, Any, Tuple, Optional
from datetime import datetime
from pathlib import Path
from enum import Enum

from environment_config import EnvironmentConfig


class HealthStatus(Enum):
    """Health check result status"""
    HEALTHY = "HEALTHY"
    WARNING = "WARNING"
    ERROR = "ERROR"
    UNKNOWN = "UNKNOWN"


class HealthCheckResult:
    """Encapsulates results of a health check"""
    
    def __init__(self, name: str, status: HealthStatus, message: str = "", details: Dict[str, Any] = None):
        self.name = name
        self.status = status
        self.message = message
        self.details = details or {}
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'status': self.status.value,
            'message': self.message,
            'details': self.details,
            'timestamp': self.timestamp.isoformat()
        }
    
    def __str__(self) -> str:
        icon = {
            HealthStatus.HEALTHY: "✅",
            HealthStatus.WARNING: "⚠️ ",
            HealthStatus.ERROR: "❌",
            HealthStatus.UNKNOWN: "❓",
        }.get(self.status, "•")
        
        result = f"{icon} {self.name}: {self.status.value}"
        if self.message:
            result += f" - {self.message}"
        return result


class EnvironmentHealthChecker:
    """
    Comprehensive health check suite for Bell Procurement System.
    
    Verifies that all critical systems are operational and properly configured
    for the current environment.
    """
    
    def __init__(self, logger: logging.Logger = None):
        self.env = EnvironmentConfig()
        self.logger = logger or logging.getLogger("bell_procurement")
        self.results: Dict[str, HealthCheckResult] = {}
    
    def run_all_checks(self) -> Dict[str, HealthCheckResult]:
        """
        Run all health checks and return results.
        
        Returns:
            Dictionary of check name -> HealthCheckResult
        """
        self.logger.info("Starting comprehensive health check suite")
        
        # Configuration checks
        self._check_environment_config()
        self._check_environment_variables()
        
        # Database checks
        self._check_database_connectivity()
        self._check_database_schema()
        
        # File system checks
        self._check_log_directory()
        self._check_data_directory()
        
        # API checks (simulation)
        self._check_api_configuration()
        
        # Compliance checks
        self._check_compliance_settings()
        
        self.logger.info(f"Health check complete: {len(self.results)} checks performed")
        
        return self.results
    
    def _check_environment_config(self) -> None:
        """Verify environment configuration is valid"""
        check_name = "Configuration"
        try:
            env_display = self.env.env_display
            self.results[check_name] = HealthCheckResult(
                check_name,
                HealthStatus.HEALTHY,
                f"Environment: {env_display}",
                {
                    'environment': env_display,
                    'environment_short': self.env.env_string,
                    'is_production': self.env.is_production,
                }
            )
            self.logger.debug(f"✓ Configuration check passed: {env_display}")
        except Exception as e:
            self.results[check_name] = HealthCheckResult(
                check_name,
                HealthStatus.ERROR,
                f"Configuration error: {str(e)}"
            )
            self.logger.error(f"✗ Configuration check failed: {e}")
    
    def _check_environment_variables(self) -> None:
        """Check required environment variables"""
        check_name = "Environment Variables"
        try:
            bell_env = os.environ.get('BELL_ENVIRONMENT')
            details = {
                'BELL_ENVIRONMENT': bell_env or "(not set - using default)",
                'BELL_CONFIG_FILE': os.environ.get('BELL_CONFIG_FILE', "(not set)"),
            }
            
            # This is OK if not set (we have defaults)
            self.results[check_name] = HealthCheckResult(
                check_name,
                HealthStatus.HEALTHY,
                "Environment variables configured",
                details
            )
            self.logger.debug(f"✓ Environment variables check passed")
        except Exception as e:
            self.results[check_name] = HealthCheckResult(
                check_name,
                HealthStatus.WARNING,
                f"Environment variables check: {str(e)}",
                details
            )
            self.logger.warning(f"⚠ Environment variables check: {e}")
    
    def _check_database_connectivity(self) -> None:
        """Check database is accessible"""
        check_name = "Database Connectivity"
        try:
            db_url = self.env.database_url
            
            # Check SQLite connectivity
            if "sqlite" in db_url.lower():
                db_path = db_url.replace('sqlite:///', '')
                if os.path.exists(db_path):
                    # Try to connect
                    conn = sqlite3.connect(db_path)
                    conn.execute("SELECT 1")
                    conn.close()
                    
                    file_size = os.path.getsize(db_path) / 1024
                    self.results[check_name] = HealthCheckResult(
                        check_name,
                        HealthStatus.HEALTHY,
                        f"SQLite database accessible",
                        {
                            'database_path': db_path,
                            'file_size_kb': f"{file_size:.2f}",
                        }
                    )
                    self.logger.debug(f"✓ Database connectivity check passed")
                else:
                    self.results[check_name] = HealthCheckResult(
                        check_name,
                        HealthStatus.WARNING,
                        f"SQLite database not found (will be created on first run)",
                        {'database_path': db_path}
                    )
                    self.logger.warning(f"⚠ Database not found: {db_path}")
            
            # SQL Server connectivity (production)
            elif "mssql" in db_url.lower():
                self.results[check_name] = HealthCheckResult(
                    check_name,
                    HealthStatus.WARNING,
                    "SQL Server connectivity check skipped (requires runtime setup)",
                    {'database_type': 'SQL Server', 'connection_string': db_url[:50] + "..."}
                )
                self.logger.warning(f"⚠ SQL Server connectivity deferred to runtime")
            
        except Exception as e:
            self.results[check_name] = HealthCheckResult(
                check_name,
                HealthStatus.ERROR,
                f"Database connectivity error: {str(e)}"
            )
            self.logger.error(f"✗ Database connectivity check failed: {e}")
    
    def _check_database_schema(self) -> None:
        """Check if database schema is initialized"""
        check_name = "Database Schema"
        try:
            db_url = self.env.database_url
            
            if "sqlite" in db_url.lower():
                db_path = db_url.replace('sqlite:///', '')
                if os.path.exists(db_path):
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    
                    # Check for required tables
                    cursor.execute(
                        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
                    )
                    tables = cursor.fetchall()
                    conn.close()
                    
                    table_names = [t[0] for t in tables]
                    required_tables = {'suppliers', 'audit_trail', 'itar_access_log', 'data_quality_issues'}
                    
                    if required_tables.issubset(set(table_names)):
                        self.results[check_name] = HealthCheckResult(
                            check_name,
                            HealthStatus.HEALTHY,
                            f"All required tables present ({len(required_tables)})",
                            {'tables': sorted(table_names)}
                        )
                        self.logger.debug(f"✓ Database schema check passed")
                    else:
                        missing = required_tables - set(table_names)
                        self.results[check_name] = HealthCheckResult(
                            check_name,
                            HealthStatus.WARNING,
                            f"Schema not initialized (missing tables: {', '.join(missing)})",
                            {'tables_found': len(table_names), 'missing_tables': list(missing)}
                        )
                        self.logger.warning(f"⚠ Missing database tables: {missing}")
                else:
                    self.results[check_name] = HealthCheckResult(
                        check_name,
                        HealthStatus.WARNING,
                        "Database not created yet"
                    )
            else:
                self.results[check_name] = HealthCheckResult(
                    check_name,
                    HealthStatus.UNKNOWN,
                    "Schema check deferred for non-SQLite databases"
                )
        
        except Exception as e:
            self.results[check_name] = HealthCheckResult(
                check_name,
                HealthStatus.WARNING,
                f"Schema check: {str(e)}"
            )
            self.logger.warning(f"⚠ Database schema check: {e}")
    
    def _check_log_directory(self) -> None:
        """Check log directory exists and is writable"""
        check_name = "Log Directory"
        try:
            log_file = self.env.log_file
            log_dir = os.path.dirname(log_file) or '.'
            
            if not os.path.exists(log_dir):
                os.makedirs(log_dir, exist_ok=True)
            
            # Try to write
            if os.access(log_dir, os.W_OK):
                self.results[check_name] = HealthCheckResult(
                    check_name,
                    HealthStatus.HEALTHY,
                    f"Log directory writable",
                    {'log_directory': os.path.abspath(log_dir)}
                )
                self.logger.debug(f"✓ Log directory check passed")
            else:
                self.results[check_name] = HealthCheckResult(
                    check_name,
                    HealthStatus.ERROR,
                    f"Log directory not writable: {log_dir}"
                )
                self.logger.error(f"✗ Log directory not writable: {log_dir}")
        
        except Exception as e:
            self.results[check_name] = HealthCheckResult(
                check_name,
                HealthStatus.ERROR,
                f"Log directory check failed: {str(e)}"
            )
            self.logger.error(f"✗ Log directory check: {e}")
    
    def _check_data_directory(self) -> None:
        """Check data directory exists and is writable"""
        check_name = "Data Directory"
        try:
            data_dir = 'data'
            
            if not os.path.exists(data_dir):
                os.makedirs(data_dir, exist_ok=True)
            
            if os.access(data_dir, os.W_OK):
                # Count database files
                db_files = list(Path(data_dir).glob('*.db'))
                self.results[check_name] = HealthCheckResult(
                    check_name,
                    HealthStatus.HEALTHY,
                    f"Data directory writable",
                    {
                        'data_directory': os.path.abspath(data_dir),
                        'database_files': len(db_files),
                        'files': [f.name for f in db_files]
                    }
                )
                self.logger.debug(f"✓ Data directory check passed")
            else:
                self.results[check_name] = HealthCheckResult(
                    check_name,
                    HealthStatus.ERROR,
                    f"Data directory not writable"
                )
                self.logger.error(f"✗ Data directory not writable")
        
        except Exception as e:
            self.results[check_name] = HealthCheckResult(
                check_name,
                HealthStatus.ERROR,
                f"Data directory check failed: {str(e)}"
            )
            self.logger.error(f"✗ Data directory check: {e}")
    
    def _check_api_configuration(self) -> None:
        """Verify API configuration"""
        check_name = "API Configuration"
        try:
            api_url = self.env.api_base_url
            rate_limit_calls = self.env.api_rate_limit_calls
            rate_limit_period = self.env.api_rate_limit_period
            
            self.results[check_name] = HealthCheckResult(
                check_name,
                HealthStatus.HEALTHY,
                f"API configured",
                {
                    'api_url': api_url,
                    'rate_limit': f"{rate_limit_calls} calls per {rate_limit_period}s",
                    'timeout_seconds': 30
                }
            )
            self.logger.debug(f"✓ API configuration check passed")
        
        except Exception as e:
            self.results[check_name] = HealthCheckResult(
                check_name,
                HealthStatus.ERROR,
                f"API configuration error: {str(e)}"
            )
            self.logger.error(f"✗ API configuration check: {e}")
    
    def _check_compliance_settings(self) -> None:
        """Check compliance-related settings (ITAR, AS9100, audit)"""
        check_name = "Compliance Settings"
        try:
            is_prod = self.env.is_production
            itar_logging = self.env.enable_itar_logging
            audit_enabled = self.env.audit_enabled
            require_itar_validation = self.env.require_itar_validation
            
            # Production safety checks
            if is_prod:
                errors = []
                if not itar_logging:
                    errors.append("ITAR logging disabled in production")
                if not audit_enabled:
                    errors.append("Audit trail disabled in production")
                if "sqlite" in self.env.database_url.lower():
                    errors.append("SQLite used in production (should be SQL Server)")
                
                if errors:
                    self.results[check_name] = HealthCheckResult(
                        check_name,
                        HealthStatus.ERROR,
                        f"Production compliance issues: {'; '.join(errors)}",
                        {
                            'itar_logging': itar_logging,
                            'audit_enabled': audit_enabled,
                            'require_itar_validation': require_itar_validation,
                            'errors': errors
                        }
                    )
                    self.logger.error(f"✗ Production compliance issues: {errors}")
                else:
                    self.results[check_name] = HealthCheckResult(
                        check_name,
                        HealthStatus.HEALTHY,
                        "All compliance controls enabled for production",
                        {
                            'itar_logging': itar_logging,
                            'audit_enabled': audit_enabled,
                            'require_itar_validation': require_itar_validation,
                        }
                    )
                    self.logger.debug(f"✓ Compliance settings check passed")
            else:
                # Dev/Test
                self.results[check_name] = HealthCheckResult(
                    check_name,
                    HealthStatus.HEALTHY,
                    f"Compliance settings configured for {self.env.env_display}",
                    {
                        'itar_logging': itar_logging,
                        'audit_enabled': audit_enabled,
                        'require_itar_validation': require_itar_validation,
                    }
                )
                self.logger.debug(f"✓ Compliance settings check passed")
        
        except Exception as e:
            self.results[check_name] = HealthCheckResult(
                check_name,
                HealthStatus.ERROR,
                f"Compliance settings check failed: {str(e)}"
            )
            self.logger.error(f"✗ Compliance settings check: {e}")
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of health check results"""
        if not self.results:
            return {}
        
        status_counts = {s: 0 for s in HealthStatus}
        for result in self.results.values():
            status_counts[result.status] += 1
        
        overall_status = HealthStatus.HEALTHY
        if status_counts[HealthStatus.ERROR] > 0:
            overall_status = HealthStatus.ERROR
        elif status_counts[HealthStatus.WARNING] > 0:
            overall_status = HealthStatus.WARNING
        
        return {
            'overall_status': overall_status.value,
            'total_checks': len(self.results),
            'healthy': status_counts[HealthStatus.HEALTHY],
            'warnings': status_counts[HealthStatus.WARNING],
            'errors': status_counts[HealthStatus.ERROR],
            'unknown': status_counts[HealthStatus.UNKNOWN],
            'timestamp': datetime.now().isoformat(),
        }
    
    def print_report(self) -> None:
        """Print formatted health check report"""
        if not self.results:
            print("No health checks have been run")
            return
        
        summary = self.get_summary()
        
        print("\n" + "=" * 70)
        print("HEALTH CHECK REPORT")
        print("=" * 70)
        print(f"Environment: {self.env.env_display}")
        print(f"Overall Status: {summary['overall_status']}")
        print(f"Timestamp: {summary['timestamp']}")
        print("-" * 70)
        
        for name, result in self.results.items():
            print(str(result))
        
        print("-" * 70)
        print(f"Summary: {summary['healthy']} healthy, {summary['warnings']} warnings, {summary['errors']} errors")
        print("=" * 70 + "\n")
    
    def get_json_report(self) -> str:
        """Get health check results as JSON"""
        if not self.results:
            return json.dumps({})
        
        return json.dumps({
            'summary': self.get_summary(),
            'checks': {name: result.to_dict() for name, result in self.results.items()},
            'environment': self.env.get_all_settings()
        }, indent=2)


if __name__ == "__main__":
    # CLI usage: python environment_health_check.py [--json] [--verbose]
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Bell Procurement System - Health Check Utility"
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help="Output results as JSON"
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help="Verbose logging output"
    )
    parser.add_argument(
        '--config',
        default='config.ini',
        help="Path to config.ini file"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s | %(name)s | %(levelname)s | %(message)s'
    )
    logger = logging.getLogger("bell_procurement")
    
    try:
        checker = EnvironmentHealthChecker(logger=logger)
        checker.run_all_checks()
        
        if args.json:
            print(checker.get_json_report())
        else:
            checker.print_report()
        
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

