"""
SQL Server Manager Example - How to use the SQL Server Connection Manager

This example demonstrates:
- Creating a connection manager
- Getting connections from the pool
- Executing queries with retry logic
- Using transactions
- Health checking
"""

import logging
from advanced_preparation.sql_server_manager import (
    SQLServerConnectionManager,
    ConnectionConfig,
    RetryStrategy,
    create_connection_manager
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def example_basic_connection():
    """Example 1: Basic connection usage"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Connection Usage")
    print("="*70)
    
    # Create manager with Windows Authentication (for test/dev)
    config = ConnectionConfig(
        server="localhost",
        database="bell_procurement",
        trusted_connection="yes"  # Windows Auth
    )
    
    manager = SQLServerConnectionManager(config, logger)
    
    # Get connection and execute query
    try:
        with manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM suppliers")
            result = cursor.fetchone()
            print(f"✓ Query successful: {result[0]} suppliers in database")
    except Exception as e:
        print(f"✗ Error: {e}")


def example_transaction():
    """Example 2: Transaction management"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Transaction Management")
    print("="*70)
    
    config = ConnectionConfig(
        server="localhost",
        database="bell_procurement"
    )
    
    manager = SQLServerConnectionManager(config, logger)
    
    try:
        with manager.transaction() as cursor:
            # Multiple operations in one transaction
            cursor.execute(
                "INSERT INTO suppliers (supplier_id, supplier_name) VALUES (?, ?)",
                ("SUPP-TEST-001", "Test Supplier")
            )
            cursor.execute(
                "UPDATE audit_trail SET import_status = 'COMPLETED' WHERE import_id = ?"
            )
            print("✓ Transaction executed (auto-commit on success)")
    except Exception as e:
        print(f"✗ Transaction rolled back due to error: {e}")


def example_health_check():
    """Example 3: Health checking"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Health Checking")
    print("="*70)
    
    config = ConnectionConfig(
        server="localhost",
        database="bell_procurement"
    )
    
    manager = SQLServerConnectionManager(config, logger)
    
    health = manager.health_check()
    print(f"Status: {health['status']}")
    print(f"Response Time: {health.get('response_time_ms', 'N/A')} ms")
    if 'error' in health:
        print(f"Error: {health['error']}")


def example_from_config_file():
    """Example 4: Load from config file"""
    print("\n" + "="*70)
    print("EXAMPLE 4: Loading from Config File")
    print("="*70)
    
    # Create manager from config.ini (requires proper config structure)
    try:
        manager = SQLServerConnectionManager.from_config(
            'config.ini',
            'PROD'  # Environment
        )
        print("✓ Connection manager created from config file")
        
        health = manager.health_check()
        print(f"✓ Database status: {health['status']}")
    except Exception as e:
        print(f"✗ Error loading from config: {e}")


def example_retry_strategy():
    """Example 5: Using different retry strategies"""
    print("\n" + "="*70)
    print("EXAMPLE 5: Retry Strategies")
    print("="*70)
    
    config = ConnectionConfig(
        server="localhost",
        database="bell_procurement",
        max_retries=3,
        retry_delay=1
    )
    
    # Try exponential backoff (default)
    manager = SQLServerConnectionManager(
        config,
        logger,
        retry_strategy=RetryStrategy.EXPONENTIAL_BACKOFF
    )
    print("✓ Manager created with exponential backoff strategy")
    
    # Exponential: 1s, 2s, 4s delays
    # Linear: 1s, 2s, 3s delays
    print("  Exponential backoff: 1s, 2s, 4s...")
    print("  Linear backoff: 1s, 2s, 3s...")


if __name__ == "__main__":
    print("\n" + "╔" + "="*68 + "╗")
    print("║ SQL Server Connection Manager Examples".ljust(69) + "║")
    print("╚" + "="*68 + "╝")
    
    print("\nNote: These examples demonstrate the patterns. In production,")
    print("you'll need actual SQL Server connections and proper credentials.")
    
    # Run examples (comment out those that need actual DB access)
    # example_basic_connection()
    # example_transaction()
    # example_health_check()
    # example_from_config_file()
    example_retry_strategy()
    
    print("\n✓ Examples complete!")

