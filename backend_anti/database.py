"""
Database configuration and connection
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Database URL - can be SQLite for development or PostgreSQL for production
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./anti_drowning.db")

# Create engine
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables
def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")

# Dependency to get database session
def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database
def init_database():
    """Initialize database with default data"""
    create_tables()
    
    # Create default admin user if not exists
    db = SessionLocal()
    try:
        from models import User
        from simple_auth import simple_hash_password
        
        admin_user = db.query(User).filter(User.phone == "admin").first()
        if not admin_user:
            # Use simple password hashing
            admin_password = "admin123"
            admin_user = User(
                name="System Administrator",
                phone="admin",
                password_hash=simple_hash_password(admin_password),
                role="admin"
            )
            db.add(admin_user)
            db.commit()
            print("✅ Default admin user created (phone: admin, password: admin123)")
        
        # No sample devices - only real ESP32 devices will be created when data arrives
        print("✅ Database initialized - devices will be auto-created from real ESP32 data")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()