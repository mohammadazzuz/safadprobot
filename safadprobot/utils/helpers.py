# Utility functions
from safadprobot.db.database import Base, engine, test_db_connection
from sqlalchemy import inspect
from safadprobot.db import models  # مهم لتعريف الجداول

def init_db():
    print("📦 [helpers.py] Initializing database...")
    
    # اختبار الاتصال
    test_db_connection()
    
    # إنشاء الجداول (إذا لم تكن موجودة)
    Base.metadata.create_all(bind=engine)
    print("✅ [helpers.py] Tables created (if not existing).")


def init_db():
    try:
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()

        required_tables = Base.metadata.tables.keys()

        print("📦 [init_db] Existing tables:", existing_tables)
        print("🧱 [init_db] Required tables:", list(required_tables))

        missing_tables = [t for t in required_tables if t not in existing_tables]

        if missing_tables:
            print(f"⚙️ [init_db] Creating missing tables: {missing_tables}")
            Base.metadata.create_all(bind=engine)
            print("✅ [init_db] Tables created successfully.")
        else:
            print("✅ [init_db] All required tables already exist.")

    except Exception as e:
        print(f"❌ [init_db] Failed to initialize database: {e}")

