"""
Error Recovery Patterns - Production-Grade Error Handling

Purpose:
    Demonstrates enterprise error handling patterns including retry logic,
    circuit breakers, and partial failure recovery. These patterns ensure
    that procurement systems gracefully handle failures at Bell.

Author: Business Systems Analyst - Bell Textron
Version: 1.0.0
License: Internal - Bell Textron Proprietary
"""

import logging
import time
from typing import Callable, Any, List, Optional, Dict
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta
from contextlib import contextmanager
from functools import wraps


class ErrorClassification(Enum):
    """Classification of errors"""
    TRANSIENT = "transient"  # Retry-able (network timeout, rate limit)
    PERMANENT = "permanent"   # Don't retry (invalid data, auth failure)
    UNKNOWN = "unknown"       # Unknown, be cautious


class RetryStrategy(Enum):
    """Retry strategies"""
    EXPONENTIAL_BACKOFF = "exponential"
    LINEAR_BACKOFF = "linear"
    FIXED_DELAY = "fixed"


@dataclass
class ErrorContext:
    """Context about an error"""
    error: Exception
    classification: ErrorClassification
    attempt_number: int
    timestamp: datetime
    message: str


@dataclass
class RecoveryAction:
    """Action to take for recovery"""
    action_type: str  # skip, retry, alert, log
    description: str
    timestamp: datetime


class CircuitBreaker:
    """
    Circuit breaker pattern to prevent cascading failures.
    
    States:
    - CLOSED: Normal operation, requests pass through
    - OPEN: Too many failures, requests rejected
    - HALF_OPEN: Testing if service recovered
    """
    
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        logger: logging.Logger = None
    ):
        """
        Initialize circuit breaker.
        
        Args:
            failure_threshold: Failures before opening circuit
            recovery_timeout: Seconds before attempting recovery
            logger: Logger instance
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.logger = logger or logging.getLogger(__name__)
        
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    def record_failure(self):
        """Record a failure"""
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            self.logger.warning(
                f"Circuit breaker opened after {self.failure_count} failures"
            )
    
    def record_success(self):
        """Record a success"""
        if self.state == "HALF_OPEN":
            self.state = "CLOSED"
            self.failure_count = 0
            self.logger.info("Circuit breaker closed - service recovered")
    
    def can_execute(self) -> bool:
        """Check if execution is allowed"""
        if self.state == "CLOSED":
            return True
        
        if self.state == "OPEN":
            # Check if recovery timeout has passed
            if self.last_failure_time:
                elapsed = (datetime.now() - self.last_failure_time).seconds
                if elapsed >= self.recovery_timeout:
                    self.state = "HALF_OPEN"
                    self.logger.info("Circuit breaker half-open - testing recovery")
                    return True
            return False
        
        # HALF_OPEN - allow one request to test
        return True


class PartialFailureHandler:
    """Handles operations with partial failures"""
    
    def __init__(self, logger: logging.Logger = None):
        """
        Initialize partial failure handler.
        
        Args:
            logger: Logger instance
        """
        self.logger = logger or logging.getLogger(__name__)
        self.failed_items = []
        self.succeeded_items = []
        self.errors = []
    
    def record_success(self, item: Any):
        """Record successful item"""
        self.succeeded_items.append(item)
    
    def record_failure(self, item: Any, error: Exception):
        """Record failed item"""
        self.failed_items.append(item)
        self.errors.append({
            'item': item,
            'error': str(error),
            'timestamp': datetime.now().isoformat()
        })
    
    def get_summary(self) -> Dict[str, Any]:
        """Get failure summary"""
        total = len(self.succeeded_items) + len(self.failed_items)
        success_rate = (len(self.succeeded_items) / total * 100) if total > 0 else 0
        
        return {
            'total_items': total,
            'succeeded': len(self.succeeded_items),
            'failed': len(self.failed_items),
            'success_rate': f"{success_rate:.1f}%",
            'errors': self.errors
        }
    
    def should_continue(self) -> bool:
        """Determine if processing should continue"""
        # Continue if success rate is above 50%
        total = len(self.succeeded_items) + len(self.failed_items)
        if total == 0:
            return True
        
        success_rate = len(self.succeeded_items) / total
        return success_rate >= 0.5


class ErrorRecoveryManager:
    """
    Centralized error recovery manager for production systems.
    
    Provides retry logic, circuit breakers, partial failure handling,
    and intelligent error classification.
    """
    
    # Transient errors that should be retried
    TRANSIENT_ERRORS = (
        TimeoutError,
        ConnectionError,
        OSError,
    )
    
    # Permanent errors that shouldn't be retried
    PERMANENT_ERRORS = (
        ValueError,
        TypeError,
        KeyError,
    )
    
    def __init__(
        self,
        max_retries: int = 3,
        retry_strategy: RetryStrategy = RetryStrategy.EXPONENTIAL_BACKOFF,
        initial_delay: int = 1,
        circuit_breaker: Optional[CircuitBreaker] = None,
        logger: logging.Logger = None
    ):
        """
        Initialize error recovery manager.
        
        Args:
            max_retries: Maximum retry attempts
            retry_strategy: Strategy for retry delays
            initial_delay: Initial delay in seconds
            circuit_breaker: Circuit breaker instance
            logger: Logger instance
        """
        self.max_retries = max_retries
        self.retry_strategy = retry_strategy
        self.initial_delay = initial_delay
        self.circuit_breaker = circuit_breaker or CircuitBreaker()
        self.logger = logger or logging.getLogger(__name__)
        
        self.error_history = []
    
    def classify_error(self, error: Exception) -> ErrorClassification:
        """
        Classify error as transient or permanent.
        
        Args:
            error: Exception to classify
            
        Returns:
            ErrorClassification enum
        """
        if isinstance(error, self.TRANSIENT_ERRORS):
            return ErrorClassification.TRANSIENT
        elif isinstance(error, self.PERMANENT_ERRORS):
            return ErrorClassification.PERMANENT
        else:
            return ErrorClassification.UNKNOWN
    
    def calculate_delay(self, attempt: int) -> int:
        """Calculate delay for retry attempt"""
        if self.retry_strategy == RetryStrategy.EXPONENTIAL_BACKOFF:
            return self.initial_delay * (2 ** attempt)
        elif self.retry_strategy == RetryStrategy.LINEAR_BACKOFF:
            return self.initial_delay * attempt
        else:  # FIXED_DELAY
            return self.initial_delay
    
    def retry_on_failure(self, func: Callable) -> Callable:
        """
        Decorator to retry function on failure.
        
        Usage:
            @recovery.retry_on_failure
            def risky_operation():
                pass
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            
            for attempt in range(self.max_retries):
                try:
                    if not self.circuit_breaker.can_execute():
                        raise ConnectionError("Circuit breaker is open")
                    
                    result = func(*args, **kwargs)
                    self.circuit_breaker.record_success()
                    return result
                    
                except Exception as e:
                    last_error = e
                    classification = self.classify_error(e)
                    
                    # Record error
                    error_context = ErrorContext(
                        error=e,
                        classification=classification,
                        attempt_number=attempt + 1,
                        timestamp=datetime.now(),
                        message=str(e)
                    )
                    self.error_history.append(error_context)
                    
                    # Don't retry permanent errors
                    if classification == ErrorClassification.PERMANENT:
                        self.logger.error(
                            f"Permanent error (not retrying): {e}"
                        )
                        self.circuit_breaker.record_failure()
                        raise
                    
                    # Retry transient errors
                    if attempt < self.max_retries - 1:
                        delay = self.calculate_delay(attempt)
                        self.logger.warning(
                            f"Attempt {attempt + 1} failed: {e}. "
                            f"Retrying in {delay}s..."
                        )
                        time.sleep(delay)
                    else:
                        self.circuit_breaker.record_failure()
                        self.logger.error(
                            f"All {self.max_retries} attempts failed: {e}"
                        )
            
            raise last_error if last_error else RuntimeError("Unknown error")
        
        return wrapper
    
    @contextmanager
    def partial_failure_handler(self):
        """
        Context manager for partial failure handling.
        
        Usage:
            with recovery.partial_failure_handler() as handler:
                for item in items:
                    try:
                        process(item)
                        handler.record_success(item)
                    except Exception as e:
                        handler.record_failure(item, e)
        """
        handler = PartialFailureHandler(self.logger)
        yield handler
        
        # Log summary
        summary = handler.get_summary()
        self.logger.info(
            f"Partial failure summary: {summary['succeeded']} succeeded, "
            f"{summary['failed']} failed, {summary['success_rate']} success rate"
        )
    
    def handle_partial_failure(
        self,
        item: Any,
        error: Exception
    ) -> RecoveryAction:
        """
        Handle partial failure for a single item.
        
        Args:
            item: Item that failed
            error: Exception raised
            
        Returns:
            Recovery action taken
        """
        classification = self.classify_error(error)
        
        if classification == ErrorClassification.TRANSIENT:
            action = RecoveryAction(
                action_type="skip_with_logging",
                description=f"Skipped transient error: {error}",
                timestamp=datetime.now()
            )
            self.logger.warning(f"Transient error for item {item}: {error}")
        else:
            action = RecoveryAction(
                action_type="alert",
                description=f"Permanent error for item {item}: {error}",
                timestamp=datetime.now()
            )
            self.logger.error(f"Permanent error for item {item}: {error}")
        
        return action
    
    def get_error_report(self) -> Dict[str, Any]:
        """
        Get detailed error report.
        
        Returns:
            Error statistics and history
        """
        transient_errors = [
            e for e in self.error_history 
            if e.classification == ErrorClassification.TRANSIENT
        ]
        permanent_errors = [
            e for e in self.error_history 
            if e.classification == ErrorClassification.PERMANENT
        ]
        
        return {
            'total_errors': len(self.error_history),
            'transient_errors': len(transient_errors),
            'permanent_errors': len(permanent_errors),
            'circuit_breaker_state': self.circuit_breaker.state,
            'circuit_breaker_failures': self.circuit_breaker.failure_count,
            'error_history': [
                {
                    'timestamp': e.timestamp.isoformat(),
                    'classification': e.classification.value,
                    'attempt': e.attempt_number,
                    'message': e.message
                }
                for e in self.error_history[-10:]  # Last 10 errors
            ]
        }


class GracefulDegradation:
    """
    Implements graceful degradation - continue with reduced functionality
    when full functionality isn't available.
    """
    
    def __init__(self, logger: logging.Logger = None):
        """Initialize graceful degradation handler"""
        self.logger = logger or logging.getLogger(__name__)
        self.degradation_mode = False
        self.disabled_features = []
    
    def enable_degradation_mode(self, reason: str):
        """Enable degradation mode"""
        self.degradation_mode = True
        self.logger.warning(f"Degradation mode enabled: {reason}")
    
    def disable_degradation_mode(self):
        """Disable degradation mode"""
        self.degradation_mode = False
        self.disabled_features = []
        self.logger.info("Degradation mode disabled - full functionality restored")
    
    def disable_feature(self, feature_name: str, reason: str):
        """Disable a specific feature"""
        if feature_name not in self.disabled_features:
            self.disabled_features.append(feature_name)
            self.logger.warning(f"Feature '{feature_name}' disabled: {reason}")
    
    def is_feature_enabled(self, feature_name: str) -> bool:
        """Check if feature is enabled"""
        return feature_name not in self.disabled_features
    
    def get_status(self) -> Dict[str, Any]:
        """Get degradation status"""
        return {
            'degradation_mode': self.degradation_mode,
            'disabled_features': self.disabled_features,
            'full_service_available': len(self.disabled_features) == 0
        }


# Convenience functions

def retry_with_backoff(
    func: Callable,
    *args,
    max_retries: int = 3,
    initial_delay: int = 1,
    **kwargs
) -> Any:
    """
    Execute function with exponential backoff retry.
    
    Args:
        func: Function to execute
        max_retries: Maximum retry attempts
        initial_delay: Initial delay in seconds
        *args: Positional arguments
        **kwargs: Keyword arguments
        
    Returns:
        Function result
    """
    recovery = ErrorRecoveryManager(
        max_retries=max_retries,
        initial_delay=initial_delay
    )
    
    @recovery.retry_on_failure
    def execute():
        return func(*args, **kwargs)
    
    return execute()


def handle_partial_failure(
    items: List[Any],
    processor: Callable,
    continue_on_partial_failure: bool = True
) -> Dict[str, Any]:
    """
    Process items with partial failure handling.
    
    Args:
        items: Items to process
        processor: Function to process each item
        continue_on_partial_failure: Continue if some items fail
        
    Returns:
        Processing summary
    """
    recovery = ErrorRecoveryManager()
    
    with recovery.partial_failure_handler() as handler:
        for item in items:
            try:
                processor(item)
                handler.record_success(item)
            except Exception as e:
                handler.record_failure(item, e)
                
                if not continue_on_partial_failure:
                    raise
    
    return handler.get_summary()


