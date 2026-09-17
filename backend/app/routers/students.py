from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_, asc
from typing import List
import math # เพิ่ม import math สำหรับหารปัดเศษขึ้น

from app import models, schemas
from app.database import get_db

router = APIRouter()

# เปลี่ยน response_model เป็น PaginatedStudentResponse ที่เราสร้างใหม่
@router.get("/search", response_model=schemas.PaginatedStudentResponse)
def search_students(
    q: str = "", 
    page: int = 1, 
    limit: int = 20, 
    db: Session = Depends(get_db)
):
    query = db.query(models.GradStudent)
    
    if q:
        search_format = f"%{q}%"
        query = query.filter(
            or_(
                models.GradStudent.studentcode.ilike(search_format),
                models.GradStudent.studentname.ilike(search_format),
                models.GradStudent.facultyname.ilike(search_format)
            )
        )
    
    # นับจำนวนข้อมูลทั้งหมดที่หาเจอ
    total_items = query.count()
    # คำนวณว่ามีทั้งหมดกี่หน้า
    total_pages = math.ceil(total_items / limit) if total_items > 0 else 1
    
    # ห้ามให้หน้าที่ขอมา เกินหน้าที่มีอยู่จริง
    if page < 1:
        page = 1
    elif page > total_pages and total_items > 0:
        page = total_pages
        
    # คำนวณจุดเริ่มต้น (Offset) สำหรับดึงข้อมูล
    offset = (page - 1) * limit
    
    # ดึงข้อมูลจริง และเรียงตามลำดับขึ้นรับ (orderno)
    students = query.order_by(models.GradStudent.orderno.asc().nulls_last())\
                    .offset(offset)\
                    .all()
    
    # ส่งข้อมูลพร้อมสถิติหน้ากลับไป
    return {
        "total_items": total_items,
        "total_pages": total_pages,
        "current_page": page,
        "limit": limit,
        "data": students
    }

@router.put("/{student_id}/attendance")
def update_attendance(student_id: int, is_attending: int, db: Session = Depends(get_db)):
    """
    API สำหรับอัปเดตสถานะการเข้ารับปริญญา (is_attending)
    """
    # ตรวจสอบว่ามีข้อมูลนักศึกษานี้ในระบบหรือไม่
    student = db.query(models.GradStudent).filter(models.GradStudent.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="ไม่พบข้อมูลบัณฑิต")

    # ค้นหาข้อมูลการแจ้งความประสงค์ในตาราง graduations
    grad_record = db.query(models.Graduation).filter(models.Graduation.student_id == student_id).first()
    
    if not grad_record:
        # หากยังไม่เคยมีเรคคอร์ด ให้สร้างใหม่ (Insert)
        grad_record = models.Graduation(student_id=student_id, is_attending=is_attending)
        db.add(grad_record)
    else:
        # หากมีอยู่แล้ว ให้อัปเดตข้อมูล (Update)
        grad_record.is_attending = is_attending
        
    db.commit()
    db.refresh(grad_record)
    
    return {"message": "อัปเดตสถานะสำเร็จ", "is_attending": is_attending}

@router.get("/attendance-types", response_model=List[schemas.AttendanceTypeBase])
def get_attendance_types(db: Session = Depends(get_db)):
    """
    API สำหรับดึงตัวเลือกสถานะการเข้ารับทั้งหมดจากตาราง mst_attendance_type
    """
    types = db.query(models.MstAttendanceType).order_by(models.MstAttendanceType.type_id).all()
    return types