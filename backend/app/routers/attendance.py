from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from app import models
from app.database import get_db
from sqlalchemy import or_
import base64
import os

router = APIRouter()
# (prefix="/attendance", tags=["Attendance"])

# Schema สำหรับรับข้อมูลจาก Frontend
class CheckInRequest(BaseModel):
    student_code: str
    scan_method: str  # 'face', 'qr', 'barcode', 'manual'
    checkin_point: int

@router.post("/checkin")
def process_checkin(req: CheckInRequest, db: Session = Depends(get_db)):
    # 1. หารอบซ้อมที่กำลังเปิดอยู่ (is_active = True)
    active_schedule = db.query(models.MstEventSchedule).filter(models.MstEventSchedule.is_active == True).first()
    if not active_schedule:
        raise HTTPException(status_code=400, detail="ยังไม่มีการเปิดรอบเช็คชื่อ กรุณาเปิดรอบในตั้งค่าก่อน")
    
    # 2. ค้นหาข้อมูลบัณฑิต
    # ⚠️ หมายเหตุ: หากคอลัมน์รหัสนักศึกษาในตาราง grad_students ของคุณชื่ออื่น (เช่น student_id) ให้แก้ตรงบรรทัดนี้นะครับ
    student = db.query(models.GradStudent).filter(models.GradStudent.studentcode == req.student_code).first()
    if not student:
        print(f"studentcode: {req.student_code} (from db: {student})")
        raise HTTPException(status_code=404, detail=f"ไม่พบรหัสนักศึกษา {req.student_code} ในระบบ")
        
    # 3. ตรวจสอบว่าเคยเช็คชื่อในรอบนี้ไปแล้วหรือยัง
    existing_log = db.query(models.AttendanceLog).filter(
        models.AttendanceLog.schedule_id == active_schedule.id,
        models.AttendanceLog.student_id == student.id
    ).first()

    # ดึง URL รูปภาพจากตาราง Graduation
    grad_info = db.query(models.Graduation).filter(models.Graduation.student_id == student.id).first()
    face_url = grad_info.face_image_url if grad_info else None

    # 4. หากยังไม่เคยเช็คชื่อ ให้บันทึกลงฐานข้อมูล
    if not existing_log:
        new_log = models.AttendanceLog(
            schedule_id=active_schedule.id,
            student_id=student.id,
            scan_method=req.scan_method,
            scanned_by="Scanner_App", # อนาคตสามารถผูกกับชื่อบัญชีเจ้าหน้าที่ได้
            checkin_point=req.checkin_point
        )
        db.add(new_log)
        db.commit()

    # 5. ส่งข้อมูลกลับไปให้มือถือแสดงผล
    now = datetime.now()
    return {
        "success": True,
        "is_duplicate": bool(existing_log), # แจ้งบอก frontend ว่าสแกนซ้ำหรือไม่
        "message": "เช็คชื่อสำเร็จ" if not existing_log else "สแกนซ้ำ (เช็คชื่อไปแล้ว)",
        "student": {
            "code": student.studentcode,
            "name": f"{student.studentname} {student.studentsurname}",
            "faculty": student.facultyname,
            "face_image_url": face_url,
            "time": f"{now.strftime('%H:%M')} น."
        }
    }

@router.get("/search")
def search_attendance(q: str = "", status: str = "all", db: Session = Depends(get_db)):
    # 1. ดึง "รอบการซ้อมทั้งหมด" เรียงตาม ID
    schedules = db.query(models.MstEventSchedule).order_by(models.MstEventSchedule.id).all()
    active_schedule = next((s for s in schedules if s.is_active), None)
    
    # 2. ค้นหาข้อมูลบัณฑิต
    query = db.query(models.GradStudent, models.Graduation).outerjoin(
        models.Graduation, models.GradStudent.id == models.Graduation.student_id
    ).order_by(models.GradStudent.orderno.asc())
    if q:
        query = query.filter(
            or_(
                models.GradStudent.studentcode.ilike(f"%{q}%"),
                models.GradStudent.studentname.ilike(f"%{q}%"),
                models.GradStudent.studentsurname.ilike(f"%{q}%")
            )
        )
    results = query.all()
    
    # 3. ดึง Log การเช็คชื่อของทุกคนในผลลัพธ์มารอไว้
    student_ids = [student.id for student, grad in results]
    logs = db.query(models.AttendanceLog).filter(models.AttendanceLog.student_id.in_(student_ids)).all()
    
    # จับคู่ Log ด้วย (student_id, schedule_id) เพื่อให้ค้นหาเร็วขึ้น
    log_dict = {(log.student_id, log.schedule_id): log for log in logs}
    
    response_data = []
    for student, grad in results:
        attendance_records = {}
        is_active_checked_in = False
        
        # วนลูปเช็คประวัติการเข้างาน "ทีละรอบ"
        for sched in schedules:
            log = log_dict.get((student.id, sched.id))
            
            attendance_records[sched.id] = {
                "is_checked_in": bool(log),
                "time": f"{log.timestamp.strftime('%H:%M')} น." if log else "-",
                "point": log.checkin_point if log else "-"
            }
            
            # จดจำสถานะของ "รอบปัจจุบัน" ไว้สำหรับตัวกรอง (Filter)
            if active_schedule and sched.id == active_schedule.id and log:
                is_active_checked_in = True
                
        # กรองข้อมูลตามสถานะที่เลือก (โดยอิงจาก "รอบที่กำลังเปิดอยู่" เป็นหลัก)
        if active_schedule:
            if status == "checked_in" and not is_active_checked_in:
                continue
            if status == "pending" and is_active_checked_in:
                continue
                
        response_data.append({
            "id": student.id,
            "student_code": student.studentcode,
            "name": f"{student.studentname} {student.studentsurname}",
            "faculty": student.facultyname,
            "has_face": bool(grad and grad.face_image_url),
            "orderno": student.orderno,
            "face_image_url": grad.face_image_url if grad else None,
            "attendance": attendance_records # ส่งประวัติทุกรอบไปด้วย
        })
        
    return {
        "schedules": [{"id": s.id, "name": s.event_name} for s in schedules],
        "students": response_data
    }


# --- Model สำหรับรับข้อมูลรูปภาพ ---
class FaceUpload(BaseModel):
    studentcode: str
    image_base64: str


# --- API บันทึกไฟล์รูปและเซฟ Path ลง Database ---
@router.post("/register-face")
def register_new_face(data: FaceUpload, db: Session = Depends(get_db)):
    try:
        # 1. ค้นหานักศึกษา
        student = db.query(models.GradStudent).filter(models.GradStudent.studentcode == data.studentcode).first()
        if not student:
            raise HTTPException(status_code=404, detail="ไม่พบรหัสนักศึกษานี้ในระบบ")

        # 2. ค้นหาข้อมูลการแจ้งความประสงค์
        graduation = db.query(models.Graduation).filter(models.Graduation.student_id == student.id).first()
        if not graduation:
            raise HTTPException(status_code=400, detail="นักศึกษาคนนี้ยังไม่มีข้อมูลการแจ้งความประสงค์ในระบบ")

        # 3. จัดการข้อความ Base64
        image_data = data.image_base64
        if "," in image_data:
            image_data = image_data.split(",")[1]

        # 4. กำหนดตำแหน่งเซฟไฟล์รูปภาพลงโฟลเดอร์ (เครื่อง Server)
        save_dir = r"D:\MyProjects\GraduFlow\uploads\faces"
        os.makedirs(save_dir, exist_ok=True)

        filename = f"{data.studentcode}.jpg"
        file_path = os.path.join(save_dir, filename)

        # เขียนไฟล์รูปลงโฟลเดอร์
        with open(file_path, "wb") as fh:
            fh.write(base64.b64decode(image_data))

        # 5. บันทึกเฉพาะ Path ตรงๆ ลง Database
        # เก็บในรูปแบบ: uploads/faces/6334002094.jpg
        graduation.face_image_url = f"uploads/faces/{filename}"

        db.commit()

        return {
            "status": "success",
            "message": f"บันทึกไฟล์รูปและอัปเดต Path ของ {student.studentname} สำเร็จ"
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()  # ยกเลิกการบันทึกฐานข้อมูลหาก Error
        raise HTTPException(status_code=500, detail=f"เกิดข้อผิดพลาด: {str(e)}")