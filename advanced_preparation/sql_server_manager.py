"""
SQL Server Connection Manager - Enterprise Database Patterns

Purpose:
    Demonstrates enterprise SQL Server connection management patterns that
    you'll use at Bell. Teaches connection pooling, retry logic, and transaction
    management with production-ready error handling.

Author: Business Systems Analyst - Bell Textron
Version: 1.0.0
License: Internal - Bell Textron Proprietary
"""

import logging
import time
from typing import Optional, Generator, Any, Dict
from dataclasses import dataclass
from enum import Enum
import configparser
from contextlib import contextmanager

try:
    import pyodbc
    from sqlalchemy import create_engine, pool
    from sqlalchemy.orm import sessionmaker, Session
except ImportError:
    pyodbc = None
    create_engine = None


class DatabaseError(Exception):
    """Base exception for database operations"""
    pass


class ConnectionPoolError(DatabaseError):
    """Exception raised when connection pool operation fails"""
    pass


class TransactionError(DatabaseError):
    """Exception raised during transaction operations"""
    pass


class RetryStrategy(Enum):
    """Retry strategies for transient failures"""
    EXPONENTIAL_BACKOFF = "exponential"
    LINEAR_BACKOFF = "linear"
    IMMEDIATE = "immediate"


@dataclass
class ConnectionConfig:
    """Configuration for database connection"""
    server: str
    database: str
    driver: str = "ODBC Driver 17 for SQL Server"
    uid: Optional[str] = None  # Username for SQL Auth
    pwd: Optional[str] = None  # Password for SQL Auth
    trusted_connection: str = "yes"  # For Windows Auth
    timeout: int = 30
    pool_size: int = 5
    max_overflow: int = 10
    max_retries: int = 3
    retry_delay: int = 1


class ConnectionRetryHandler:
    """Handles retry logic for transient failures"""
    
    def __init__(
        self,
        max_retries: int = 3,
        retry_delay: int = 1,
        strategy: RetryStrategy = RetryStrategy.EXPONENTIAL_BACKOFF,
        logger: logging.Logger = None
    ):
        """
        Initialize retry handler.
        
        Args:
            max_retries: Maximum number of retry attempts
            retry_delay: Initial retry delay in seconds
            strategy: Retry strategy to use
            logger: Logger instance
        """
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.strategy = strategy
        self.logger = logger or logging.getLogger(__name__)
    
    def calculate_delay(self, attempt: int) -> int:
        """Calculate delay for this retry attempt"""
        if self.strategy == RetryStrategy.EXPONENTIAL_BACKOFF:
            return self.retry_delay * (2 ** attempt)
        elif self.strategy == RetryStrategy.LINEAR_BACKOFF:
            return self.retry_delay * attempt
        else:  # IMMEDIATE
            return 0
    
    def execute_with_retry(self, func, *args, **kwargs):
        """
        Execute function with retry logic.
        
        Args:
            func: Function to execute
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Function result
            
        Raises:
            DatabaseError: If all retries fail
        """
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except (pyodbc.OperationalError, pyodbc.InterfaceError) as e:
                last_exception = e
                
                if attempt < self.max_retries - 1:
                    delay = self.calculate_delay(attempt)
                    self.logger.warning(
                        f"Attempt {attempt + 1} failed: {e}. "
                        f"Retrying in {delay}s..."
                    )
                    time.sleep(delay)
                else:
                    self.logger.error(
                        f"All {self.max_retries} retry attempts failed"
                    )
        
        raise DatabaseError(
            f"Failed after {self.max_retries} attempts: {last_exception}"
        )


class SQLServerTransaction:
    """Context manager for SQL Server transactions"""
    
    def __init__(self, connection, logger: logging.Logger = None):
        """
        Initialize transaction context.
        
        Args:
            connection: pyodbc connection
            logger: Logger instance
        """
        self.connection = connection
        self.logger = logger or logging.getLogger(__name__)
        self.in_transaction = False
    
    def __enter__(self):
        """Start transaction"""
        try:
            self.connection.execute("BEGIN TRANSACTION")
            self.in_transaction = True
            self.logger.debug("Transaction started")
            return self.connection.cursor()
        except Exception as e:
            self.logger.error(f"Failed to start transaction: {e}")
            raise TransactionError(f"Transaction start failed: {e}")
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Commit or rollback transaction"""
        if not self.in_transaction:
            return False
        
        try:
            if exc_type is None:
                self.connection.commit()
                self.logger.debug("Transaction committed")
            else:
                self.connection.rollback()
                self.logger.warning(
                    f"Transaction rolled back due to: {exc_type.__name__}: {exc_val}"
                )
            self.in_transaction = False
            return False  # Don't suppress exception
        except Exception as e:
            self.logger.error(f"Failed to finalize transaction: {e}")
            raise TransactionError(f"Transaction finalization failed: {e}")


class SQLServerConnectionManager:
    """
    Enterprise SQL Server connection manager with pooling and retry logic.
    
    This class demonstrates production-grade connection management patterns
    that Bell uses for their procurement systems.
    """
    
    _instance = None  # Singleton
    
    def __new__(cls, *args, **kwargs):
        """Implement singleton pattern"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(
        self,
        config: ConnectionConfig,
        logger: logging.Logger = None,
        retry_strategy: RetryStrategy = RetryStrategy.EXPONENTIAL_BACKOFF
    ):
        """
        Initialize SQL Server connection manager.
        
        Args:
            config: Connection configuration
            logger: Logger instance
            retry_strategy: Retry strategy for transient failures
        """
        if self._initialized:
            return
        
        self.config = config
        self.logger = logger or logging.getLogger(__name__)
        self._initialized = True
        
        # Initialize retry handler
        self.retry_handler = ConnectionRetryHandler(
            max_retries=config.max_retries,
            retry_delay=config.retry_delay,
            strategy=retry_strategy,
            logger=self.logger
        )
        
        # Connection pool
        self._pool = None
        self._initialize_pool()
    
    def _initialize_pool(self):
        """Initialize connection pool"""
        try:
            if pyodbc is None:
                raise ImportError("pyodbc is not installed")
            
            # Build connection string
            conn_string = self._build_connection_string()
            
            # Create engine with pooling
            engine = create_engine(
                f"mssql+pyodbc:///?odbc_connect={conn_string}",
                poolclass=pool.QueuePool,
                pool_size=self.config.pool_size,
                max_overflow=self.config.max_overflow,
                pool_recycle=3600,  # Recycle connections after 1 hour
                echo=False
            )
            
            self._pool = engine
            self.logger.info(
                f"Connection pool initialized: "
                f"pool_size={self.config.pool_size}, "
                f"max_overflow={self.config.max_overflow}"
            )
        except Exception as e:
            self.logger.error(f"Failed to initialize connection pool: {e}")
            raise ConnectionPoolError(f"Pool initialization failed: {e}")
    
    def _build_connection_string(self) -> str:
        """Build ODBC connection string"""
        parts = [
            f"Driver={{{self.config.driver}}}",
            f"Server={self.config.server}",
            f"Database={self.config.database}",
            f"Timeout={self.config.timeout}",
        ]
        
        if self.config.trusted_connection.lower() == "yes":
            # Windows Authentication
            parts.append("Trusted_Connection=yes")
        else:
            # SQL Authentication
            if self.config.uid:
                parts.append(f"UID={self.config.uid}")
            if self.config.pwd:
                parts.append(f"PWD={self.config.pwd}")
        
        return ";".join(parts)
    
    @classmethod
    def from_config(
        cls,
        config_file: str,
        environment: str,
        logger: logging.Logger = None
    ) -> "SQLServerConnectionManager":
        """
        Create manager from config file.
        
        Args:
            config_file: Path to config.ini
            environment: Environment section (DEV, TEST, PROD)
            logger: Logger instance
            
        Returns:
            SQLServerConnectionManager instance
        """
        config = configparser.ConfigParser()
        config.read(config_file)
        
        env_section = environment.upper()
        
        conn_config = ConnectionConfig(
            server=config.get(env_section, "DATABASE_SERVER"),
            database=config.get(env_section, "DATABASE_NAME"),
            driver=config.get(env_section, "DATABASE_DRIVER", fallback="ODBC Driver 17 for SQL Server"),
            uid=config.get(env_section, "DATABASE_UID", fallback=None),
            pwd=config.get(env_section, "DATABASE_PWD", fallback=None),
            timeout=config.getint("SQL_SERVER", "TIMEOUT_SECONDS", fallback=30),
            pool_size=config.getint("SQL_SERVER", "CONNECTION_POOL_SIZE", fallback=5),
            max_retries=config.getint("SQL_SERVER", "MAX_RETRIES", fallback=3),
            retry_delay=config.getint("SQL_SERVER", "RETRY_DELAY_SECONDS", fallback=1),
        )
        
        return cls(conn_config, logger)
    
    @contextmanager
    def get_connection(self):
        """
        Get connection from pool with retry logic.
        
        Yields:
            pyodbc connection
            
        Usage:
            with manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM suppliers")
        """
        def _get_conn():
            if self._pool is None:
                raise ConnectionPoolError("Connection pool not initialized")
            return self._pool.raw_connection()
        
        connection = None
        try:
            connection = self.retry_handler.execute_with_retry(_get_conn)
            self.logger.debug("Connection acquired from pool")
            yield connection
        except Exception as e:
            self.logger.error(f"Failed to get connection: {e}")
            raise
        finally:
            if connection:
                try:
                    connection.close()
                    self.logger.debug("Connection returned to pool")
                except Exception as e:
                    self.logger.error(f"Error closing connection: {e}")
    
    @contextmanager
    def transaction(self):
        """
        Get transaction context manager.
        
        Yields:
            Cursor for transaction execution
            
        Usage:
            with manager.transaction() as cursor:
                cursor.execute("INSERT INTO suppliers ...")
                cursor.execute("UPDATE audit_trail ...")
                # Auto-commits if no exception, auto-rollback on error
        """
        with self.get_connection() as conn:
            with SQLServerTransaction(conn, self.logger) as cursor:
                yield cursor
    
    def execute_query(
        self,
        query: str,
        params: tuple = None,
        fetch_all: bool = True
    ) -> Any:
        """
        Execute query with retry logic.
        
        Args:
            query: SQL query
            params: Query parameters
            fetch_all: Fetch all results or just first row
            
        Returns:
            Query results
        """
        def _execute():
            with self.get_connection() as conn:
                cursor = conn.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                if fetch_all:
                    return cursor.fetchall()
                else:
                    return cursor.fetchone()
        
        return self.retry_handler.execute_with_retry(_execute)
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check database connectivity and health.
        
        Returns:
            Dictionary with health status
        """
        try:
            start_time = time.time()
            result = self.execute_query("SELECT 1", fetch_all=False)
            elapsed = time.time() - start_time
            
            return {
                "status": "HEALTHY",
                "response_time_ms": int(elapsed * 1000),
                "message": "Database connection successful"
            }
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return {
                "status": "UNHEALTHY",
                "error": str(e),
                "message": "Database connection failed"
            }
    
    def close_pool(self):
        """Close connection pool gracefully"""
        try:
            if self._pool:
                self._pool.dispose()
                self.logger.info("Connection pool closed")
        except Exception as e:
            self.logger.error(f"Error closing connection pool: {e}")


# Convenience function for quick initialization
def create_connection_manager(
    server: str,
    database: str,
    driver: str = "ODBC Driver 17 for SQL Server",
    uid: Optional[str] = None,
    pwd: Optional[str] = None,
    logger: logging.Logger = None
) -> SQLServerConnectionManager:
    """
    Create SQL Server connection manager with minimal configuration.
    
    Args:
        server: SQL Server instance name
        database: Database name
        driver: ODBC driver name
        uid: Username (for SQL Auth)
        pwd: Password (for SQL Auth)
        logger: Logger instance
        
    Returns:
        SQLServerConnectionManager instance
    """
    config = ConnectionConfig(
        server=server,
        database=database,
        driver=driver,
        uid=uid,
        pwd=pwd,
        trusted_connection="no" if uid else "yes"
    )
    
    return SQLServerConnectionManager(config, logger)

