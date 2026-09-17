# ไฟล์ ตัวคัดกรองข้อมูล

from unittest.mock import Base

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func

# --- Schemas สำหรับ MstAttendanceType ---
class AttendanceTypeBase(BaseModel):
    type_id: int
    type_name: str
    is_attend: Optional[bool] = None
    require_remark: Optional[str] = None

    class Config:
        from_attributes = True

# --- Schemas สำหรับ Delivery ---
class DeliveryBase(BaseModel):
    shipping_address: Optional[str] = None
    shipping_method: Optional[int] = None
    shipping_cost: Optional[float] = None
    payment_status: Optional[str] = None
    tracking_number: Optional[str] = None

class DeliveryCreate(DeliveryBase):
    graduation_id: UUID

class DeliveryResponse(DeliveryBase):
    id: UUID
    graduation_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- Schemas สำหรับ Graduation ---
class GraduationBase(BaseModel):
    is_attending: int
    food_type: Optional[str] = None
    food_allergy: Optional[str] = None
    face_image_url: Optional[str] = None
    survey_completed: bool = False
    status: Optional[str] = None
    pregnancy_month: Optional[int] = None
    reason: Optional[str] = None

class GraduationCreate(GraduationBase):
    student_id: int

class GraduationResponse(GraduationBase):
    id: UUID
    student_id: int
    created_at: datetime
    updated_at: datetime
    
    # ดึงข้อมูลการจัดส่งมาแสดงด้วย (ถ้ามี)
    delivery_info: Optional[DeliveryResponse] = None

    class Config:
        from_attributes = True

# --- Schemas สำหรับ GradStudent ---
class GradStudentBase(BaseModel):
    acadyear: int
    studentcode: str
    facultyname: str
    departmentname: str
    programname: str
    prefixname: Optional[str] = None
    studentname: Optional[str] = None
    studentsurname: Optional[str] = None
    email: Optional[str] = None
    mobile: Optional[str] = None
    orderno: Optional[int] = None

class GradStudentResponse(GradStudentBase):
    id: int
    
    # รวมข้อมูลการแจ้งความประสงค์เข้าไปใน Response ของนักศึกษาเลย
    graduation_info: Optional[GraduationResponse] = None

    class Config:
        from_attributes = True

# เพิ่ม class นี้ไว้ล่างสุดของไฟล์ backend/app/schemas.py
class PaginatedStudentResponse(BaseModel):
    total_items: int
    total_pages: int
    current_page: int
    limit: int
    data: List[GradStudentResponse]

    class Config:
        from_attributes = True

# 1. ตารางตั้งค่ารอบการซ้อม/รับจริง (รองรับความยืดหยุ่นในแต่ละปี)
class EventSchedule(Base):
    __tablename__ = "mst_event_schedules"

    id = Column(Integer, primary_key=True, index=True)
    academic_year = Column(String(4)) # เช่น "2568"
    event_name = Column(String) # เช่น "ซ้อมย่อยวันที่ 1", "ซ้อมใหญ่", "วันรับจริง"
    event_date = Column(Date)
    session_type = Column(String) # เช่น "morning" (เช้า), "afternoon" (บ่าย)
    
    # สำคัญมาก: ตัวควบคุมว่าตอนนี้เจ้าหน้าที่กำลังสแกนเช็คชื่อของรอบไหนอยู่
    is_active = Column(Boolean, default=False) 

# 2. ตารางเก็บประวัติการเช็คชื่อ
class AttendanceLog(Base):
    __tablename__ = "attendance_logs"

    id = Column(Integer, primary_key=True, index=True)
    schedule_id = Column(Integer, ForeignKey("mst_event_schedules.id"))
    student_id = Column(Integer, ForeignKey("grad_students.id"))
    checkin_point = Column(Integer)  # เช่น "Main Gate", "Building A", "Room 101"
    
    # เก็บว่าเช็คชื่อด้วยวิธีไหน: 'face', 'qr', 'barcode', 'manual'
    scan_method = Column(String(20)) 
    
    # วันเวลาที่สแกนสำเร็จ
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # รหัสเจ้าหน้าที่ (หรือชื่อ) ที่เป็นคนสแกน
    scanned_by = Column(String)

class FacultyResponse(BaseModel):
    facultyid: int    # <--- แก้จาก id เป็น facultyid
    facultyname: str
    facultynameeng: str

    class Config:
        from_attributes = True

class DepartmentResponse(BaseModel):
    departmentid: int # <--- ถ้าของสาขาใช้ departmentid ก็ต้องแก้ด้วยนะครับ (หรือถ้าเป็น id ก็ปล่อยไว้)
    departmentname: str
    departmentnameeng: str
    facultyid: int   # ฟิลด์นี้เอาไว้เชื่อมกับ faculty

    class Config:
        from_attributes = True
