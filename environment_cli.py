"""
Bell Textron Environment CLI Utilities

Purpose:
    Command-line interface utilities for environment inspection, status checking,
    and common operational tasks. These tools help developers and administrators
    verify which environment they're working with before running operations.

Author: Business Systems Analyst - Bell Textron
Version: 1.0.0
License: Internal - Bell Textron Proprietary
"""

import sys
import json
import logging
from typing import Optional
from pathlib import Path

from environment_config import EnvironmentConfig, validate_environment_safety
from environment_health_check import EnvironmentHealthChecker, HealthStatus


def setup_cli_logging(verbose: bool = False) -> logging.Logger:
    """Setup logging for CLI operations"""
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(levelname)s: %(message)s'
    )
    return logging.getLogger("bell_procurement_cli")


def cmd_status(args) -> int:
    """
    Display current environment status.
    
    Usage: bell-env status [--json] [--config CONFIG_FILE]
    """
    try:
        env = EnvironmentConfig(config_file=args.config)
        
        if args.json:
            print(json.dumps(env.get_all_settings(), indent=2))
        else:
            print(env.status_report())
        
        return 0
    
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


def cmd_check(args) -> int:
    """
    Run comprehensive health checks.
    
    Usage: bell-env check [--json] [--config CONFIG_FILE] [--verbose]
    """
    logger = setup_cli_logging(args.verbose)
    
    try:
        checker = EnvironmentHealthChecker(logger=logger)
        checker.run_all_checks()
        
        if args.json:
            print(checker.get_json_report())
        else:
            checker.print_report()
        
        # Exit with error if critical issues found
        summary = checker.get_summary()
        if summary['errors'] > 0:
            return 1
        
        return 0
    
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


def cmd_validate(args) -> int:
    """
    Validate environment safety (especially for production).
    
    Usage: bell-env validate [--config CONFIG_FILE]
    """
    logger = setup_cli_logging(args.verbose)
    
    try:
        env = EnvironmentConfig(config_file=args.config)
        validate_environment_safety()
        
        print(f"✓ Environment validation passed: {env.env_display}")
        logger.info(f"Environment {env.env_display} passed safety validation")
        
        return 0
    
    except RuntimeError as e:
        print(f"CRITICAL: {e}", file=sys.stderr)
        logger.critical(f"Environment validation failed: {e}")
        return 1
    
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


def cmd_info(args) -> int:
    """
    Display current environment in banner format.
    
    Usage: bell-env info [--config CONFIG_FILE]
    """
    try:
        env = EnvironmentConfig(config_file=args.config)
        logger = logging.getLogger("bell_procurement")
        env.print_startup_banner(logger)
        
        return 0
    
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


def cmd_database(args) -> int:
    """
    Display database information for current environment.
    
    Usage: bell-env database [--config CONFIG_FILE]
    """
    try:
        env = EnvironmentConfig(config_file=args.config)
        db_url = env.database_url
        
        print(f"\nDatabase Information ({env.env_display})")
        print("=" * 60)
        print(f"Connection URL: {db_url}")
        
        if "sqlite" in db_url.lower():
            db_path = db_url.replace('sqlite:///', '')
            print(f"Database Type: SQLite")
            print(f"Database Path: {db_path}")
            
            import os
            if os.path.exists(db_path):
                size_mb = os.path.getsize(db_path) / (1024 * 1024)
                print(f"File Size: {size_mb:.2f} MB")
                
                # Try to show table count
                import sqlite3
                try:
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
                    table_count = cursor.fetchone()[0]
                    conn.close()
                    print(f"Tables: {table_count}")
                except:
                    pass
            else:
                print(f"Status: Database file not found (will be created on first run)")
        
        elif "mssql" in db_url.lower():
            print(f"Database Type: SQL Server")
            print(f"Status: Connection deferred to runtime")
        
        print("=" * 60 + "\n")
        
        return 0
    
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


def cmd_api(args) -> int:
    """
    Display API configuration for current environment.
    
    Usage: bell-env api [--config CONFIG_FILE]
    """
    try:
        env = EnvironmentConfig(config_file=args.config)
        
        print(f"\nAPI Configuration ({env.env_display})")
        print("=" * 60)
        print(f"Base URL:        {env.api_base_url}")
        print(f"Rate Limit:      {env.api_rate_limit_calls} calls")
        print(f"Period:          {env.api_rate_limit_period} seconds")
        print(f"Timeout:         30 seconds")
        print(f"Calculated Rate: {env.api_rate_limit_calls / env.api_rate_limit_period:.2f} calls/sec")
        print("=" * 60 + "\n")
        
        return 0
    
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


def cmd_compliance(args) -> int:
    """
    Display compliance settings for current environment.
    
    Usage: bell-env compliance [--config CONFIG_FILE]
    """
    try:
        env = EnvironmentConfig(config_file=args.config)
        
        print(f"\nCompliance Configuration ({env.env_display})")
        print("=" * 60)
        print(f"Environment:              {env.env_display}")
        print(f"ITAR Logging:             {env.enable_itar_logging}")
        print(f"ITAR Validation Required: {env.require_itar_validation}")
        print(f"Audit Trail Enabled:      {env.audit_enabled}")
        print(f"Log Level:                {env.log_level}")
        print(f"Log File:                 {env.log_file}")
        
        # Warn if production settings are not strict
        if env.is_production:
            print("\n⚠️  PRODUCTION ENVIRONMENT DETECTED")
            print("=" * 60)
            issues = []
            if not env.enable_itar_logging:
                issues.append("ITAR logging is DISABLED in production")
            if not env.audit_enabled:
                issues.append("Audit trail is DISABLED in production")
            if env.log_level == "DEBUG":
                issues.append("Log level set to DEBUG in production")
            
            if issues:
                print("CRITICAL ISSUES FOUND:")
                for issue in issues:
                    print(f"  ❌ {issue}")
                print("=" * 60)
                return 1
            else:
                print("All production compliance controls are ENABLED ✓")
        
        print("=" * 60 + "\n")
        
        return 0
    
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


def cmd_set_environment(args) -> int:
    """
    Print shell command to set environment variable.
    
    Usage: bell-env set DEV|TEST|PROD
    """
    env_map = {
        'dev': 'dev',
        'development': 'dev',
        'test': 'test',
        'testing': 'test',
        'prod': 'prod',
        'production': 'prod',
    }
    
    env_requested = args.environment.lower()
    
    if env_requested not in env_map:
        print(f"ERROR: Unknown environment '{args.environment}'", file=sys.stderr)
        print(f"Valid options: dev, development, test, testing, prod, production", file=sys.stderr)
        return 1
    
    env_value = env_map[env_requested]
    
    print(f"# To set environment to {env_value}, run:")
    print(f"export BELL_ENVIRONMENT={env_value}")
    print(f"\n# Or in one command:")
    print(f"export BELL_ENVIRONMENT={env_value} && python procurement_automation.py {env_value} config.ini")
    
    return 0


def print_help() -> None:
    """Print help message"""
    help_text = """
╔════════════════════════════════════════════════════════════════════╗
║    Bell Textron Procurement Automation - Environment CLI           ║
╚════════════════════════════════════════════════════════════════════╝

USAGE:
    python -m environment_cli <command> [options]
    
    or (after adding to PATH):
    
    bell-env <command> [options]

COMMANDS:

  status [--json] [--config FILE]
    Display current environment configuration and status
    
    Examples:
      python -m environment_cli status
      python -m environment_cli status --json
      python -m environment_cli status --config /path/to/config.ini

  check [--json] [--verbose] [--config FILE]
    Run comprehensive health checks on the environment
    
    Examples:
      python -m environment_cli check
      python -m environment_cli check --json
      python -m environment_cli check --verbose

  validate [--config FILE]
    Validate environment safety (especially for production)
    
    Examples:
      python -m environment_cli validate

  info [--config FILE]
    Display environment in large banner format
    
    Examples:
      python -m environment_cli info

  database [--config FILE]
    Show database configuration and status
    
    Examples:
      python -m environment_cli database

  api [--config FILE]
    Show API configuration and rate limits
    
    Examples:
      python -m environment_cli api

  compliance [--config FILE]
    Show compliance settings (ITAR, audit, etc.)
    
    Examples:
      python -m environment_cli compliance

  set <ENV>
    Print command to set environment variable
    
    Examples:
      python -m environment_cli set dev
      python -m environment_cli set prod

  help
    Show this help message

ENVIRONMENT VARIABLES:

  BELL_ENVIRONMENT
    Set the environment (dev, test, prod)
    Defaults to 'dev' if not set
    
    Example:
      export BELL_ENVIRONMENT=prod

  BELL_CONFIG_FILE
    Path to config.ini file
    Defaults to './config.ini'
    
    Example:
      export BELL_CONFIG_FILE=/etc/bell/config.ini

QUICK START:

  1. Check current environment:
     python -m environment_cli status

  2. Run health checks:
     python -m environment_cli check

  3. Switch to production:
     export BELL_ENVIRONMENT=prod
     python -m environment_cli info

  4. Validate production settings:
     python -m environment_cli validate

PRODUCTION REQUIREMENTS:

  Before running in production:
  
  1. Set environment: export BELL_ENVIRONMENT=prod
  2. Validate settings: python -m environment_cli validate
  3. Run health checks: python -m environment_cli check
  4. Review compliance: python -m environment_cli compliance

═════════════════════════════════════════════════════════════════════
"""
    print(help_text)


def main():
    """Main CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Bell Textron Procurement Automation - Environment Management CLI",
        add_help=False
    )
    
    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Show environment status')
    status_parser.add_argument('--json', action='store_true', help='Output as JSON')
    status_parser.add_argument('--config', default='config.ini', help='Config file path')
    status_parser.set_defaults(func=cmd_status)
    
    # Check command
    check_parser = subparsers.add_parser('check', help='Run health checks')
    check_parser.add_argument('--json', action='store_true', help='Output as JSON')
    check_parser.add_argument('--verbose', action='store_true', help='Verbose output')
    check_parser.add_argument('--config', default='config.ini', help='Config file path')
    check_parser.set_defaults(func=cmd_check)
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate environment safety')
    validate_parser.add_argument('--config', default='config.ini', help='Config file path')
    validate_parser.add_argument('--verbose', action='store_true', help='Verbose output')
    validate_parser.set_defaults(func=cmd_validate)
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Show environment banner')
    info_parser.add_argument('--config', default='config.ini', help='Config file path')
    info_parser.set_defaults(func=cmd_info)
    
    # Database command
    db_parser = subparsers.add_parser('database', help='Show database info')
    db_parser.add_argument('--config', default='config.ini', help='Config file path')
    db_parser.set_defaults(func=cmd_database)
    
    # API command
    api_parser = subparsers.add_parser('api', help='Show API configuration')
    api_parser.add_argument('--config', default='config.ini', help='Config file path')
    api_parser.set_defaults(func=cmd_api)
    
    # Compliance command
    compliance_parser = subparsers.add_parser('compliance', help='Show compliance settings')
    compliance_parser.add_argument('--config', default='config.ini', help='Config file path')
    compliance_parser.set_defaults(func=cmd_compliance)
    
    # Set environment command
    set_parser = subparsers.add_parser('set', help='Print environment variable command')
    set_parser.add_argument('environment', help='Environment to set (dev/test/prod)')
    set_parser.set_defaults(func=cmd_set_environment)
    
    # Help command
    help_parser = subparsers.add_parser('help', help='Show help message')
    help_parser.set_defaults(func=lambda x: (print_help(), 0)[1])
    
    # Parse arguments
    args = parser.parse_args()
    
    # Show help if no command
    if not args.command:
        print_help()
        return 0
    
    # Execute command
    if hasattr(args, 'func'):
        return args.func(args)
    else:
        print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())


