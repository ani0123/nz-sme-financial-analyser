# ══════════════════════════════════════════════════════
#  db_connection.py
#  Handles all PostgreSQL database connections
#  Used by every other module in the project
# ══════════════════════════════════════════════════════

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import psycopg2

# Load environment variables from .env file
load_dotenv()

def get_engine():
    """
    Creates and returns a SQLAlchemy engine.
    Used for pandas read/write operations.
    """
    db_url = (
        f"postgresql+psycopg2://"
        f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
        f"/{os.getenv('DB_NAME')}"
    )
    engine = create_engine(db_url)
    return engine


def get_connection():
    """
    Creates and returns a raw psycopg2 connection.
    Used for direct SQL queries and inserts.
    """
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    return conn


def test_connection():
    """
    Tests the database connection and prints the result.
    Run this file directly to verify everything is working.
    """
    try:
        engine = get_engine()
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM businesses"))
            count = result.scalar()
            print("✓ Database connected successfully")
            print(f"✓ Found {count} businesses in the database")
    except Exception as e:
        print(f"✗ Connection failed: {e}")


# Run test when this file is executed directly
if __name__ == "__main__":
    test_connection()