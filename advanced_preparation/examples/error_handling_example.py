"""
Error Recovery Patterns Example - How to use error handling and recovery

This example demonstrates:
- Retry decorator
- Circuit breaker pattern
- Partial failure handling
- Error classification and recovery
"""

import logging
import time
from advanced_preparation.error_recovery_patterns import (
    ErrorRecoveryManager,
    CircuitBreaker,
    RetryStrategy,
    GracefulDegradation,
    retry_with_backoff,
    handle_partial_failure
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def example_retry_decorator():
    """Example 1: Using retry decorator"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Retry Decorator")
    print("="*70)
    
    recovery = ErrorRecoveryManager(
        max_retries=3,
        retry_strategy=RetryStrategy.EXPONENTIAL_BACKOFF,
        initial_delay=1,
        logger=logger
    )
    
    attempt_count = 0
    
    @recovery.retry_on_failure
    def unstable_api_call():
        nonlocal attempt_count
        attempt_count += 1
        
        if attempt_count < 2:
            print(f"  Attempt {attempt_count}: Simulating transient failure")
            raise TimeoutError("API timeout")
        
        print(f"  Attempt {attempt_count}: Success!")
        return "API Response Data"
    
    try:
        result = unstable_api_call()
        print(f"✓ Result: {result}")
    except Exception as e:
        print(f"✗ Failed: {e}")


def example_circuit_breaker():
    """Example 2: Circuit breaker pattern"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Circuit Breaker Pattern")
    print("="*70)
    
    breaker = CircuitBreaker(
        failure_threshold=3,
        recovery_timeout=5,
        logger=logger
    )
    
    print("Initial state: CLOSED (requests allowed)")
    print(f"State: {breaker.state}\n")
    
    # Simulate failures
    for i in range(1, 5):
        if breaker.can_execute():
            print(f"Attempt {i}: Executing request")
            breaker.record_failure()
            print(f"  State: {breaker.state}, Failures: {breaker.failure_count}")
        else:
            print(f"Attempt {i}: Circuit OPEN - request rejected")


def example_partial_failure():
    """Example 3: Partial failure handling"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Partial Failure Handling")
    print("="*70)
    
    suppliers = [
        {'id': 'SUPP-001', 'name': 'Boeing'},
        {'id': 'SUPP-002', 'name': 'Raytheon'},
        {'id': 'SUPP-003', 'name': 'Invalid'},  # Will fail
        {'id': 'SUPP-004', 'name': 'Honeywell'},
    ]
    
    recovery = ErrorRecoveryManager(logger=logger)
    
    def process_supplier(supplier):
        """Process supplier - will fail for specific ones"""
        if supplier['name'] == 'Invalid':
            raise ValueError("Invalid supplier data")
        print(f"  Processing: {supplier['name']}")
        time.sleep(0.1)
    
    with recovery.partial_failure_handler() as handler:
        for supplier in suppliers:
            try:
                process_supplier(supplier)
                handler.record_success(supplier['id'])
            except Exception as e:
                handler.record_failure(supplier['id'], e)
    
    # Show summary
    summary = handler.get_summary()
    print(f"\n✓ Processing complete:")
    print(f"  Succeeded: {summary['succeeded']}")
    print(f"  Failed: {summary['failed']}")
    print(f"  Success Rate: {summary['success_rate']}")


def example_graceful_degradation():
    """Example 4: Graceful degradation"""
    print("\n" + "="*70)
    print("EXAMPLE 4: Graceful Degradation")
    print("="*70)
    
    degradation = GracefulDegradation(logger=logger)
    
    print("Initial status: Full service available")
    print(f"Status: {degradation.get_status()}\n")
    
    # Simulate service issues
    print("Simulating database connectivity issue...")
    degradation.disable_feature(
        'supplier_audit_logging',
        "Database connection timeout"
    )
    
    print("Simulating API rate limit...")
    degradation.disable_feature(
        'ariba_api_sync',
        "Rate limit exceeded"
    )
    
    # Check feature availability
    print(f"\n✓ Service Status:")
    status = degradation.get_status()
    print(f"  Full Service Available: {status['full_service_available']}")
    print(f"  Disabled Features: {status['disabled_features']}")
    print(f"  Degradation Mode: {status['degradation_mode']}")
    
    # Check specific features
    print(f"\nFeature Availability:")
    print(f"  supplier_audit_logging: {degradation.is_feature_enabled('supplier_audit_logging')}")
    print(f"  procurement_validation: {degradation.is_feature_enabled('procurement_validation')}")


def example_error_classification():
    """Example 5: Error classification and recovery"""
    print("\n" + "="*70)
    print("EXAMPLE 5: Error Classification")
    print("="*70)
    
    recovery = ErrorRecoveryManager(logger=logger)
    
    # Test different error types
    errors = [
        TimeoutError("Connection timeout"),
        ValueError("Invalid data"),
        ConnectionError("Network error"),
        KeyError("Missing field"),
    ]
    
    print("Error Classifications:\n")
    for error in errors:
        classification = recovery.classify_error(error)
        retryable = "✓ Will retry" if classification.value == "transient" else "✗ Won't retry"
        print(f"{error.__class__.__name__:<20} → {classification.value:<12} ({retryable})")


def example_error_report():
    """Example 6: Error reporting"""
    print("\n" + "="*70)
    print("EXAMPLE 6: Error Report")
    print("="*70)
    
    recovery = ErrorRecoveryManager(
        max_retries=2,
        logger=logger
    )
    
    # Generate some errors
    for i in range(1, 4):
        try:
            if i == 1:
                raise TimeoutError("API timeout")
            elif i == 2:
                raise ValueError("Invalid data")
            else:
                raise ConnectionError("Network error")
        except Exception as e:
            classification = recovery.classify_error(e)
            # Just classifying, not retrying in this example
    
    # Get error report
    report = recovery.get_error_report()
    print(f"✓ Error Report:")
    print(f"  Total Errors: {report['total_errors']}")
    print(f"  Transient: {report['transient_errors']}")
    print(f"  Permanent: {report['permanent_errors']}")
    print(f"  Circuit State: {report['circuit_breaker_state']}")


if __name__ == "__main__":
    print("\n" + "╔" + "="*68 + "╗")
    print("║ Error Recovery Patterns Examples".ljust(69) + "║")
    print("╚" + "="*68 + "╝")
    
    # Run examples
    try:
        example_retry_decorator()
        example_circuit_breaker()
        example_partial_failure()
        example_graceful_degradation()
        example_error_classification()
        example_error_report()
    except Exception as e:
        print(f"\n✗ Error: {e}")
    
    print("\n✓ Examples complete!")

