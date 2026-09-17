# file โครงสร้างฐานข้อมูล
import uuid
from sqlalchemy import Column, Integer, String, Boolean, Text, Numeric, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column, declarative_base
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, date
from app.database import Base
from typing import Optional
    
Base = declarative_base()

class MstAttendanceType(Base):
    __tablename__ = "mst_attendance_type"
    
    type_id = Column(Integer, primary_key=True, index=True)
    type_name = Column(String)
    is_attend = Column(Boolean)
    require_remark = Column(String)

class GradStudent(Base):
    __tablename__ = "grad_students"
    
    id = Column(Integer, primary_key=True, index=True)
    acadyear = Column(Integer)
    studentcode = Column(String(20), unique=True, index=True)
    levelid = Column(String(50))
    levelname = Column(String)
    levelnameeng = Column(String)
    facultyid = Column(String(50))
    facultyname = Column(String)
    facultynameeng = Column(String)
    departmentid = Column(String(50))
    departmentname = Column(String)
    departmentnameeng = Column(String)
    programid = Column(String(50))
    programname = Column(String)
    programnameeng = Column(String)
    prefixname = Column(Text)
    prefixnameeng = Column(Text)
    studentname = Column(Text)
    studentnameeng = Column(Text)
    studentsurname = Column(Text)
    studentsurnameeng = Column(Text)
    email = Column(String)
    mobile = Column(String(20))
    orderno = Column(Integer)
    
    # Relationship กลับไปยังตาราง graduations (1 นักศึกษา มี 1 การแจ้งความประสงค์)
    graduation_info = relationship("Graduation", back_populates="student", uselist=False)

class Graduation(Base):
    __tablename__ = "graduations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(Integer, ForeignKey("grad_students.id"))
    is_attending = Column(Integer, ForeignKey("mst_attendance_type.type_id"))
    food_type = Column(String)
    food_allergy = Column(Text)
    face_image_url = Column(Text)
    survey_completed = Column(Boolean, default=False)
    status = Column(String)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    pregnancy_month = Column(Integer, nullable=True)
    reason = Column(String, nullable=True)

    # Relationships
    student = relationship("GradStudent", back_populates="graduation_info")
    attendance_type = relationship("MstAttendanceType")
    delivery_info = relationship("Delivery", back_populates="graduation", uselist=False)

class Delivery(Base):
    __tablename__ = "deliveries"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    graduation_id = Column(UUID(as_uuid=True), ForeignKey("graduations.id"))
    shipping_address = Column(Text)
    shipping_method = Column(Integer)
    shipping_cost = Column(Numeric(10, 2))
    payment_status = Column(String)
    tracking_number = Column(String) # รอรับค่าจาก API ขนส่ง
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    graduation = relationship("Graduation", back_populates="delivery_info")

class MstEventSchedule(Base):
    __tablename__ = "mst_event_schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    academic_year = Column(Integer)
    event_name: Mapped[str] = mapped_column(String(255))
    event_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    
    #  rehearsal_start_date = Column(DateTime)
    # rehearsal_end_date = Column(DateTime)
    # graduation_start_date = Column(DateTime)
    # graduation_end_date = Column(DateTime)
    is_active = Column(Boolean, default=False)  # ระบุว่ารอบนี้เปิดให้เช็คชื่ออยู่หรือไม่

class AttendanceLog(Base):
    __tablename__ = "attendance_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    schedule_id = Column(Integer, ForeignKey("mst_event_schedules.id"))
    student_id = Column(Integer, ForeignKey("grad_students.id"))
    scan_method = Column(String) 
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow)
    scanned_by = Column(String)  # อนาคตสามารถผูกกับชื่อบัญชีเจ้าหน้าที่ได้
    checkin_point = Column(Integer, default=1)
    
    # Relationship
    student = relationship("GradStudent")

class SystemSetting(Base):
    __tablename__ = "system_settings"

    setting_key = Column(String, primary_key=True, index=True)
    setting_value = Column(String, nullable=True)
    description = Column(String, nullable=True)

class Faculty(Base):
    __tablename__ = "faculty"

    facultyid = Column(Integer, primary_key=True, index=True)
    facultyname = Column(String)
    facultynameeng = Column(String)

class Department(Base):
    __tablename__ = "department"

    facultyid = Column(Integer, primary_key=True, index=True)
    departmentid = Column(Integer, primary_key=True, index=True)
    departmentname = Column(String)
    departmentnameeng = Column(String)
