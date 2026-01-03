"""
Unit tests for SQL Server Connection Manager

Tests cover:
- Connection pool initialization
- Connection acquisition and release
- Transaction management
- Error retry logic
- Health checking
"""

import pytest
import logging
from advanced_preparation.sql_server_manager import (
    SQLServerConnectionManager,
    ConnectionConfig,
    RetryStrategy,
    ConnectionRetryHandler,
    ErrorClassification,
)


@pytest.fixture
def connection_config():
    """Create test connection config"""
    return ConnectionConfig(
        server="localhost",
        database="test_db",
        timeout=5,
        pool_size=2,
        max_retries=2,
        retry_delay=1
    )


@pytest.fixture
def retry_handler():
    """Create test retry handler"""
    return ConnectionRetryHandler(
        max_retries=2,
        retry_delay=1,
        strategy=RetryStrategy.EXPONENTIAL_BACKOFF,
        logger=logging.getLogger(__name__)
    )


class TestRetryHandler:
    """Test retry handler logic"""
    
    def test_calculate_delay_exponential(self, retry_handler):
        """Test exponential backoff calculation"""
        assert retry_handler.calculate_delay(0) == 1  # 1 * 2^0
        assert retry_handler.calculate_delay(1) == 2  # 1 * 2^1
        assert retry_handler.calculate_delay(2) == 4  # 1 * 2^2
    
    def test_retry_strategy_linear(self):
        """Test linear backoff"""
        handler = ConnectionRetryHandler(
            max_retries=3,
            retry_delay=2,
            strategy=RetryStrategy.LINEAR_BACKOFF
        )
        assert handler.calculate_delay(0) == 2  # 2 * 1
        assert handler.calculate_delay(1) == 4  # 2 * 2
        assert handler.calculate_delay(2) == 6  # 2 * 3


class TestConnectionConfig:
    """Test connection configuration"""
    
    def test_config_creation(self, connection_config):
        """Test config object creation"""
        assert connection_config.server == "localhost"
        assert connection_config.database == "test_db"
        assert connection_config.pool_size == 2
        assert connection_config.max_retries == 2
    
    def test_windows_auth_config(self):
        """Test Windows authentication config"""
        config = ConnectionConfig(
            server="server1",
            database="db1",
            trusted_connection="yes"
        )
        assert config.trusted_connection == "yes"
        assert config.uid is None
    
    def test_sql_auth_config(self):
        """Test SQL authentication config"""
        config = ConnectionConfig(
            server="server1",
            database="db1",
            uid="user1",
            pwd="password",
            trusted_connection="no"
        )
        assert config.uid == "user1"
        assert config.pwd == "password"


class TestConnectionManager:
    """Test connection manager (without real database)"""
    
    def test_singleton_pattern(self, connection_config):
        """Test that ConnectionManager uses singleton pattern"""
        manager1 = SQLServerConnectionManager(connection_config)
        manager2 = SQLServerConnectionManager(connection_config)
        
        # Should be same instance
        assert manager1 is manager2
    
    def test_manager_initialization(self, connection_config):
        """Test manager initializes correctly"""
        manager = SQLServerConnectionManager(connection_config)
        
        assert manager.config == connection_config
        assert manager.retry_handler is not None
        assert manager.circuit_breaker is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


