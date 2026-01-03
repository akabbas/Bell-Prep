"""
Unit tests for Error Recovery Patterns

Tests cover:
- Retry logic and strategies
- Circuit breaker state management
- Error classification
- Partial failure handling
"""

import pytest
import logging
import time
from advanced_preparation.error_recovery_patterns import (
    ErrorRecoveryManager,
    CircuitBreaker,
    ErrorClassification,
    RetryStrategy,
    PartialFailureHandler,
)


@pytest.fixture
def error_recovery_manager():
    """Create error recovery manager"""
    return ErrorRecoveryManager(
        max_retries=3,
        retry_strategy=RetryStrategy.EXPONENTIAL_BACKOFF,
        initial_delay=0.1,
        logger=logging.getLogger(__name__)
    )


@pytest.fixture
def circuit_breaker():
    """Create circuit breaker"""
    return CircuitBreaker(
        failure_threshold=3,
        recovery_timeout=2,
        logger=logging.getLogger(__name__)
    )


class TestErrorClassification:
    """Test error classification"""
    
    def test_classify_transient_errors(self, error_recovery_manager):
        """Test transient error classification"""
        errors = [
            TimeoutError("timeout"),
            ConnectionError("connection"),
            OSError("os error")
        ]
        
        for error in errors:
            classification = error_recovery_manager.classify_error(error)
            assert classification == ErrorClassification.TRANSIENT
    
    def test_classify_permanent_errors(self, error_recovery_manager):
        """Test permanent error classification"""
        errors = [
            ValueError("value error"),
            TypeError("type error"),
            KeyError("key error")
        ]
        
        for error in errors:
            classification = error_recovery_manager.classify_error(error)
            assert classification == ErrorClassification.PERMANENT


class TestCircuitBreaker:
    """Test circuit breaker pattern"""
    
    def test_initial_state(self, circuit_breaker):
        """Test initial state is CLOSED"""
        assert circuit_breaker.state == "CLOSED"
        assert circuit_breaker.failure_count == 0
    
    def test_circuit_opens_on_threshold(self, circuit_breaker):
        """Test circuit opens after failure threshold"""
        for i in range(3):
            circuit_breaker.record_failure()
        
        assert circuit_breaker.state == "OPEN"
        assert circuit_breaker.failure_count == 3
    
    def test_can_execute_when_closed(self, circuit_breaker):
        """Test execution allowed when CLOSED"""
        assert circuit_breaker.can_execute() is True
    
    def test_cannot_execute_when_open(self, circuit_breaker):
        """Test execution blocked when OPEN"""
        for i in range(3):
            circuit_breaker.record_failure()
        
        assert circuit_breaker.can_execute() is False


class TestRetryStrategies:
    """Test different retry strategies"""
    
    def test_exponential_backoff(self):
        """Test exponential backoff calculation"""
        manager = ErrorRecoveryManager(
            initial_delay=1,
            retry_strategy=RetryStrategy.EXPONENTIAL_BACKOFF
        )
        
        assert manager.calculate_delay(0) == 1
        assert manager.calculate_delay(1) == 2
        assert manager.calculate_delay(2) == 4
    
    def test_linear_backoff(self):
        """Test linear backoff calculation"""
        manager = ErrorRecoveryManager(
            initial_delay=1,
            retry_strategy=RetryStrategy.LINEAR_BACKOFF
        )
        
        assert manager.calculate_delay(0) == 1
        assert manager.calculate_delay(1) == 2
        assert manager.calculate_delay(2) == 3


class TestPartialFailureHandler:
    """Test partial failure handling"""
    
    def test_record_success_and_failure(self):
        """Test recording successes and failures"""
        handler = PartialFailureHandler()
        
        handler.record_success("item1")
        handler.record_failure("item2", ValueError("error"))
        
        assert len(handler.succeeded_items) == 1
        assert len(handler.failed_items) == 1
    
    def test_summary_generation(self):
        """Test summary generation"""
        handler = PartialFailureHandler()
        
        for i in range(3):
            handler.record_success(f"item{i}")
        
        handler.record_failure("item_bad", ValueError("error"))
        
        summary = handler.get_summary()
        
        assert summary['total_items'] == 4
        assert summary['succeeded'] == 3
        assert summary['failed'] == 1
        assert "75.0%" in summary['success_rate']


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


