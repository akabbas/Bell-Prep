"""
Bell Textron Environment Configuration Manager

Purpose:
    Provides enterprise-grade environment detection and configuration management
    with audit logging compliance for defense/aerospace procurement systems.
    
    This module ensures clarity about which environment (dev/test/prod) the system
    is running in, prevents accidental cross-environment operations, and maintains
    audit trails required by ITAR and AS9100 standards.

Author: Business Systems Analyst - Bell Textron
Version: 1.0.0
License: Internal - Bell Textron Proprietary
"""

import os
import sys
import logging
import configparser
from typing import Optional, Dict, Any
from enum import Enum
from datetime import datetime
from pathlib import Path


class EnvironmentType(Enum):
    """Valid environment types for Bell Procurement System"""
    DEV = "development"
    TEST = "testing"
    PROD = "production"
    
    @classmethod
    def from_string(cls, value: str) -> "EnvironmentType":
        """Convert string to EnvironmentType with error handling"""
        if not value:
            raise ValueError("Environment cannot be empty")
        
        value = value.lower().strip()
        
        # Handle both short and long forms
        mapping = {
            'dev': cls.DEV,
            'development': cls.DEV,
            'test': cls.TEST,
            'testing': cls.TEST,
            'prod': cls.PROD,
            'production': cls.PROD,
        }
        
        if value not in mapping:
            valid = ', '.join(mapping.keys())
            raise ValueError(
                f"Invalid environment '{value}'. "
                f"Valid options: {valid}"
            )
        
        return mapping[value]
    
    def is_production(self) -> bool:
        """Check if this is production environment"""
        return self == EnvironmentType.PROD
    
    def is_development(self) -> bool:
        """Check if this is development environment"""
        return self == EnvironmentType.DEV
    
    def is_testing(self) -> bool:
        """Check if this is testing environment"""
        return self == EnvironmentType.TEST


class EnvironmentConfig:
    """
    Centralized configuration manager for Bell Procurement System.
    
    This is the single source of truth for environment state. All code should
    reference this instance to determine behavior based on environment.
    
    Usage:
        env = EnvironmentConfig(config_file='config.ini')
        
        # Check environment
        if env.is_production:
            enable_strict_validation()
        
        # Get configuration values
        db_url = env.database_url
        api_endpoint = env.api_base_url
        
        # Status
        print(env.status_report())
    """
    
    _instance = None  # Singleton pattern
    
    def __new__(cls, *args, **kwargs):
        """Implement singleton pattern - only one config instance"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, config_file: str = "config.ini", environment: Optional[str] = None):
        """
        Initialize environment configuration.
        
        Args:
            config_file: Path to config.ini file
            environment: Override environment (defaults to BELL_ENVIRONMENT env var or 'dev')
        
        Raises:
            ValueError: If environment is invalid
            FileNotFoundError: If config file doesn't exist
        """
        # Prevent re-initialization of singleton
        if self._initialized:
            return
        
        self._config_file = config_file
        self._config = None
        self._environment = None
        self._initialization_time = datetime.now()
        self._initialized = True
        
        # Determine environment: explicit arg > env var > default
        if environment:
            env_value = environment
        else:
            env_value = os.environ.get('BELL_ENVIRONMENT', 'dev')
        
        try:
            self._environment = EnvironmentType.from_string(env_value)
        except ValueError as e:
            raise ValueError(f"Failed to initialize environment: {e}")
        
        # Load config file
        if not os.path.exists(config_file):
            raise FileNotFoundError(
                f"Configuration file not found: {config_file}\n"
                f"Expected at: {os.path.abspath(config_file)}"
            )
        
        self._config = configparser.ConfigParser()
        self._config.read(config_file)
        
        # Validate configuration section exists
        env_section = self._environment.name.upper()  # DEV, TEST, PROD
        if env_section not in self._config:
            raise ValueError(
                f"Environment section '[{env_section}]' not found in {config_file}"
            )
    
    @property
    def environment(self) -> EnvironmentType:
        """Get current environment type"""
        return self._environment
    
    @property
    def env_string(self) -> str:
        """Get environment as lowercase string (dev/test/prod)"""
        return self._environment.name.lower()
    
    @property
    def env_display(self) -> str:
        """Get environment for display (DEVELOPMENT/TESTING/PRODUCTION)"""
        return self._environment.value.upper()
    
    @property
    def is_production(self) -> bool:
        """Check if running in production"""
        return self._environment.is_production()
    
    @property
    def is_development(self) -> bool:
        """Check if running in development"""
        return self._environment.is_development()
    
    @property
    def is_testing(self) -> bool:
        """Check if running in testing"""
        return self._environment.is_testing()
    
    @property
    def database_url(self) -> str:
        """Get database connection URL"""
        env_section = self.env_string.upper()
        return self._config.get(env_section, "DATABASE_URL")
    
    @property
    def api_base_url(self) -> str:
        """Get API base URL"""
        env_section = self.env_string.upper()
        return self._config.get(env_section, "API_BASE_URL")
    
    @property
    def log_file(self) -> str:
        """Get log file path"""
        env_section = self.env_string.upper()
        return self._config.get(env_section, "LOG_FILE")
    
    @property
    def log_level(self) -> str:
        """Get log level"""
        return self._config.get("DEFAULT", "LOG_LEVEL")
    
    @property
    def api_rate_limit_calls(self) -> int:
        """Get API rate limit calls per period"""
        env_section = self.env_string.upper()
        return self._config.getint(env_section, "API_RATE_LIMIT_CALLS")
    
    @property
    def api_rate_limit_period(self) -> int:
        """Get API rate limit period in seconds"""
        env_section = self.env_string.upper()
        return self._config.getint(env_section, "API_RATE_LIMIT_PERIOD")
    
    @property
    def enable_itar_logging(self) -> bool:
        """Check if ITAR logging is enabled"""
        env_section = self.env_string.upper()
        return self._config.getboolean(env_section, "ENABLE_ITAR_LOGGING")
    
    @property
    def audit_enabled(self) -> bool:
        """Check if audit trail is enabled"""
        env_section = self.env_string.upper()
        return self._config.getboolean(env_section, "AUDIT_ENABLED")
    
    @property
    def require_itar_validation(self) -> bool:
        """Check if ITAR validation is required (prod only)"""
        env_section = self.env_string.upper()
        return self._config.getboolean(env_section, "REQUIRE_ITAR_VALIDATION", fallback=False)
    
    @property
    def initialization_time(self) -> datetime:
        """Get when this config was initialized"""
        return self._initialization_time
    
    def get_all_settings(self) -> Dict[str, Any]:
        """Get all current environment settings as dictionary"""
        return {
            'environment': self.env_display,
            'environment_short': self.env_string,
            'database_url': self.database_url,
            'api_base_url': self.api_base_url,
            'log_file': self.log_file,
            'log_level': self.log_level,
            'api_rate_limit_calls': self.api_rate_limit_calls,
            'api_rate_limit_period': self.api_rate_limit_period,
            'enable_itar_logging': self.enable_itar_logging,
            'audit_enabled': self.audit_enabled,
            'require_itar_validation': self.require_itar_validation,
            'is_production': self.is_production,
            'is_development': self.is_development,
            'is_testing': self.is_testing,
            'initialized_at': self.initialization_time.isoformat(),
        }
    
    def print_startup_banner(self, logger: logging.Logger):
        """
        Print formatted startup banner showing environment status.
        
        This should be called early in application initialization to ensure
        that the environment is clearly visible in logs and console output.
        
        Args:
            logger: Logger instance to use for logging
        """
        banner = self._build_banner()
        print("\n" + banner + "\n", file=sys.stdout)
        logger.info("=" * 73)
        logger.info(f"ENVIRONMENT: {self.env_display}")
        logger.info("=" * 73)
    
    def _build_banner(self) -> str:
        """Build formatted startup banner"""
        width = 73
        
        # Determine banner color/theme based on environment
        if self.is_production:
            status_icon = "🔴 PRODUCTION"
            warning = "⚠️  STRICT VALIDATION AND AUDIT LOGGING ENABLED"
        elif self.is_testing:
            status_icon = "🟡 TEST"
            warning = "ℹ️  Test environment with full audit trail"
        else:  # development
            status_icon = "🟢 DEVELOPMENT"
            warning = "ℹ️  Development environment, relaxed limits"
        
        # Build banner
        lines = [
            "╔" + "═" * (width - 2) + "╗",
            f"║ {status_icon:<{width - 3}}║",
            "║" + " " * (width - 2) + "║",
            f"║ Database:       {self.database_url:<{width - 20}}║",
            f"║ API:            {self.api_base_url:<{width - 20}}║",
            f"║ Log Level:      {self.log_level:<{width - 20}}║",
            f"║ ITAR Logging:   {'ENABLED' if self.enable_itar_logging else 'DISABLED':<{width - 20}}║",
            "║" + " " * (width - 2) + "║",
            f"║ {warning:<{width - 3}}║",
            f"║ Initialized:    {self.initialization_time.strftime('%Y-%m-%d %H:%M:%S UTC'):<{width - 20}}║",
            "╚" + "═" * (width - 2) + "╝",
        ]
        
        return "\n".join(lines)
    
    def status_report(self) -> str:
        """
        Generate a detailed status report of current environment configuration.
        
        Returns:
            Formatted string with all configuration details
        """
        lines = [
            "\n" + "=" * 70,
            "ENVIRONMENT STATUS REPORT",
            "=" * 70,
            f"Environment:              {self.env_display} ({self.env_string})",
            f"Production Mode:          {self.is_production}",
            f"Initialized:              {self.initialization_time.isoformat()}",
            "-" * 70,
            "DATABASE CONFIGURATION",
            "-" * 70,
            f"URL:                      {self.database_url}",
            "-" * 70,
            "API CONFIGURATION",
            "-" * 70,
            f"Base URL:                 {self.api_base_url}",
            f"Rate Limit:               {self.api_rate_limit_calls} calls per {self.api_rate_limit_period} seconds",
            "-" * 70,
            "COMPLIANCE & LOGGING",
            "-" * 70,
            f"Log File:                 {self.log_file}",
            f"Log Level:                {self.log_level}",
            f"ITAR Logging:             {self.enable_itar_logging}",
            f"ITAR Validation Required: {self.require_itar_validation}",
            f"Audit Trail Enabled:      {self.audit_enabled}",
            "=" * 70 + "\n",
        ]
        
        return "\n".join(lines)
    
    def __repr__(self) -> str:
        """String representation"""
        return f"<EnvironmentConfig: {self.env_display}>"
    
    def __str__(self) -> str:
        """User-friendly string representation"""
        return f"Bell Procurement System [{self.env_display}]"


def validate_environment_safety() -> None:
    """
    Perform safety checks before running application.
    
    This is especially important in production to prevent accidental
    data loss or compliance violations.
    
    Raises:
        RuntimeError: If critical safety checks fail
    """
    env = EnvironmentConfig()
    
    if env.is_production:
        # Production safety checks
        if not env.enable_itar_logging:
            raise RuntimeError(
                "CRITICAL: ITAR logging must be enabled in production environment"
            )
        
        if not env.audit_enabled:
            raise RuntimeError(
                "CRITICAL: Audit trail must be enabled in production environment"
            )
        
        # Check that database is SQL Server (not SQLite)
        if "sqlite" in env.database_url.lower():
            raise RuntimeError(
                "CRITICAL: Production environment must use SQL Server, not SQLite"
            )


def get_environment_config(config_file: str = "config.ini", 
                          environment: Optional[str] = None) -> EnvironmentConfig:
    """
    Convenience function to get or create EnvironmentConfig instance.
    
    Args:
        config_file: Path to config.ini
        environment: Override environment (optional)
    
    Returns:
        EnvironmentConfig instance
    """
    return EnvironmentConfig(config_file=config_file, environment=environment)


if __name__ == "__main__":
    # CLI usage: python environment_config.py [environment]
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Bell Procurement System - Environment Configuration"
    )
    parser.add_argument(
        'environment',
        nargs='?',
        default=None,
        help="Environment to check (dev/test/prod). Defaults to BELL_ENVIRONMENT env var or 'dev'"
    )
    parser.add_argument(
        '--config',
        default='config.ini',
        help="Path to config.ini file"
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help="Output status as JSON"
    )
    
    args = parser.parse_args()
    
    try:
        env = EnvironmentConfig(config_file=args.config, environment=args.environment)
        
        if args.json:
            import json
            print(json.dumps(env.get_all_settings(), indent=2))
        else:
            print(env.status_report())
            print(f"Current Configuration: {env}\n")
            
    except (ValueError, FileNotFoundError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

