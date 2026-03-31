"""
Test database connection and create tables
"""
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from database import Base, engine, get_db
from models import Alert

def test_connection():
    """Test database connection"""
    print("Testing Supabase database connection...")
    
    try:
        # Test basic connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"✅ Database connected successfully!")
            print(f"PostgreSQL version: {version}")
            
        # Test session creation
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Test a simple query
        result = db.execute(text("SELECT current_database(), current_user;"))
        db_info = result.fetchone()
        print(f"Database: {db_info[0]}")
        print(f"User: {db_info[1]}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        return False

def create_tables():
    """Create all tables"""
    print("\nCreating database tables...")
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created successfully!")
        
        # Verify table creation
        with engine.connect() as connection:
            result = connection.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_type = 'BASE TABLE';
            """))
            
            tables = result.fetchall()
            print(f"Tables in database: {[table[0] for table in tables]}")
            
        return True
        
    except Exception as e:
        print(f"❌ Table creation failed: {str(e)}")
        return False

def test_crud_operations():
    """Test basic CRUD operations"""
    print("\nTesting CRUD operations...")
    
    try:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Create a test alert
        test_alert = Alert(
            device_id="test_device_001",
            danger=True,
            latitude=18.5204,
            longitude=73.8567
        )
        
        db.add(test_alert)
        db.commit()
        db.refresh(test_alert)
        
        print(f"✅ Created test alert with ID: {test_alert.id}")
        
        # Read the alert
        retrieved_alert = db.query(Alert).filter(Alert.id == test_alert.id).first()
        print(f"✅ Retrieved alert: {retrieved_alert.device_id} - Danger: {retrieved_alert.danger}")
        
        # Update the alert
        retrieved_alert.danger = False
        db.commit()
        print("✅ Updated alert danger status to False")
        
        # Count total alerts
        total_alerts = db.query(Alert).count()
        print(f"✅ Total alerts in database: {total_alerts}")
        
        # Clean up - delete test alert
        db.delete(retrieved_alert)
        db.commit()
        print("✅ Deleted test alert")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ CRUD operations failed: {str(e)}")
        return False

def check_table_structure():
    """Check the alerts table structure"""
    print("\nChecking table structure...")
    
    try:
        with engine.connect() as connection:
            result = connection.execute(text("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_name = 'alerts'
                ORDER BY ordinal_position;
            """))
            
            columns = result.fetchall()
            print("Alerts table structure:")
            print("-" * 60)
            print(f"{'Column':<15} {'Type':<20} {'Nullable':<10} {'Default'}")
            print("-" * 60)
            
            for col in columns:
                print(f"{col[0]:<15} {col[1]:<20} {col[2]:<10} {col[3] or 'None'}")
            
        return True
        
    except Exception as e:
        print(f"❌ Table structure check failed: {str(e)}")
        return False

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    print("🚀 Supabase Database Connection Test")
    print("=" * 50)
    
    # Test connection
    if not test_connection():
        exit(1)
    
    # Create tables
    if not create_tables():
        exit(1)
    
    # Check table structure
    if not check_table_structure():
        exit(1)
    
    # Test CRUD operations
    if not test_crud_operations():
        exit(1)
    
    print("\n🎉 All database tests passed successfully!")
    print("Your Supabase database is ready for the IoT Alert System!")