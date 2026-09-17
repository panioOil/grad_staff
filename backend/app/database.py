import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. กำหนด URL สำหรับเชื่อมต่อ PostgreSQL
# ในการใช้งานจริง แนะนำให้ตั้งค่าผ่าน Environment Variable (.env)
# รูปแบบ: postgresql://[user]:[password]@[host]:[port]/[database_name]
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:gradmfu@localhost:5432/graduflow_v2"
)

# 2. สร้าง Engine สำหรับจัดการการเชื่อมต่อฐานข้อมูล
# การตั้งค่า pool_size และ max_overflow จะช่วยรองรับการเชื่อมต่อพร้อมๆ กันจำนวนมากได้ดีขึ้น
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=20,
    max_overflow=10
)

# 3. สร้าง Session Factory 
# autocommit=False เพื่อให้เราสามารถควบคุมการบันทึก (commit) หรือยกเลิก (rollback) ข้อมูลได้เองใน API
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. สร้าง Base Class เพื่อให้ไฟล์ models.py นำไปใช้สืบทอดสร้างตาราง
Base = declarative_base()

# 5. Dependency Function สำหรับแจกจ่าย Database Session ให้กับ API แต่ละเส้น
# เมื่อ API ทำงานเสร็จ จะทำการปิด (close) การเชื่อมต่อให้ทันทีเพื่อไม่ให้ Connection ค้าง
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()