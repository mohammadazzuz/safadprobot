# PostgreSQL connection and schema
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

DATABASE_URL = os.getenv("DATABASE_URL")

# إعداد المحرك
engine = create_engine(DATABASE_URL, echo=False)

# إعداد الجلسة
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# قاعدة ORM
Base = declarative_base()

# اختبار الاتصال (اختياري)
def test_db_connection():
    try:
        with engine.connect() as conn:
            print("✅ [database.py] Connected to database successfully.")
    except OperationalError as e:
        print("❌ [database.py] Failed to connect to database:", e)


