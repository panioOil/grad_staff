from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, case, and_ # เพิ่ม import and_ เข้ามาสำหรับเงื่อนไขแบบช่วง
from app import models
from app.database import get_db

router = APIRouter()

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    # 1. สถิติภาพรวม (Overview)
    total_students = db.query(models.GradStudent).count()
    
    # ปรับเงื่อนไข เข้ารับ (< 20) และ ไม่เข้ารับ (>= 20 และ < 30)
    attended = db.query(models.Graduation).filter(models.Graduation.is_attending < 20).count()
    not_attended = db.query(models.Graduation).filter(
        and_(models.Graduation.is_attending >= 20, models.Graduation.is_attending < 30)
    ).count()
    
    # face_registered = db.query(models.Graduation).filter(models.Graduation.face_image_url.is_not(None)).count()
    
    pending = total_students - (attended + not_attended)

    # หาว่ารอบไหนเปิดให้เช็คชื่ออยู่ (is_active = True)
    active_schedule = db.query(models.MstEventSchedule).filter(models.MstEventSchedule.is_active == True).first()
    
    if active_schedule:
        schedule_name = active_schedule.event_name
        schedule_date = active_schedule.event_date
        # นับจำนวนคนที่ถูกเช็คชื่อในรอบนี้
        checked_in_count = db.query(models.AttendanceLog).filter(models.AttendanceLog.schedule_id == active_schedule.id).count()
        
        # นับคนที่เช็คชื่อแล้ว และมีรูปหน้าแล้ว (Join หา URL รูป)
        checked_in_with_face = db.query(models.AttendanceLog)\
            .join(models.Graduation, models.AttendanceLog.student_id == models.Graduation.student_id)\
            .filter(models.AttendanceLog.schedule_id == active_schedule.id)\
            .filter(models.Graduation.face_image_url.is_not(None))\
            .count()
    else:
        schedule_name = "ยังไม่มีรอบที่เปิดเช็คชื่อ"
        checked_in_count = 0
        checked_in_with_face = 0

    # ปรับ Logic ใหม่: คิด % จากคนเช็คชื่อ (checked_in_count) เทียบกับคนที่ลงทะเบียนเข้ารับ (attended)
    checkin_percentage = round((checked_in_count / attended * 100), 1) if attended > 0 else 0

    # 2. สถิติแยกตามสำนักวิชา (ปรับแก้เงื่อนไขใน case)
    fac_query = db.query(
        models.GradStudent.facultyid,
        models.GradStudent.facultyname,
        func.count(models.GradStudent.id).label('total'),
        # เข้ารับคือ is_attending < 20
        func.sum(case((models.Graduation.is_attending < 20, 1), else_=0)).label('attended'),
        # ไม่เข้ารับคือ is_attending >= 20 และ < 30
        func.sum(case((and_(models.Graduation.is_attending >= 20, models.Graduation.is_attending < 30), 1), else_=0)).label('not_attended')
    ).outerjoin(
        models.Graduation, models.GradStudent.id == models.Graduation.student_id
    ).group_by(models.GradStudent.facultyid,models.GradStudent.facultyname).all()

    faculties = []
    for fac in fac_query:
        total = fac.total or 0
        att = fac.attended or 0
        not_att = fac.not_attended or 0
        fac_pending = total - (att + not_att)

        
        att_percent = round((att / total * 100), 1) if total > 0 else 0
        not_att_percent = round((not_att / total * 100), 1) if total > 0 else 0

        faculties.append({
            "id": fac.facultyid,
            "name": fac.facultyname or "ไม่ระบุสำนักวิชา",
            "total": total,
            "attended": att,
            "not_attended": not_att,
            "pending": fac_pending,
            "attend_percent": att_percent,
            "not_attend_percent": not_att_percent
        })
        
    faculties = sorted(faculties, key=lambda x: x['total'], reverse=True)

    # 3. ความเคลื่อนไหวล่าสุด
    recent_records = db.query(models.GradStudent, models.Graduation)\
        .join(models.Graduation, models.GradStudent.id == models.Graduation.student_id)\
        .order_by(models.Graduation.updated_at.desc())\
        .limit(5).all()
    
    recent_activities = []
    for student, grad in recent_records:
        # ปรับเงื่อนไขการแสดงผลข้อความใน Recent Activities
        status_text = "รอระบุสถานะ"
        if grad.is_attending is not None:
            if grad.is_attending < 20:
                status_text = "เข้ารับ"
            elif 20 <= grad.is_attending < 30:
                status_text = "ไม่เข้ารับ"
            else:
                status_text = "สถานะอื่นๆ"

        recent_activities.append({
            "id": student.id,
            "studentcode": student.studentcode,
            "name": f"{student.studentname} {student.studentsurname}",
            "faculty": student.facultyname,
            "status": status_text,
            "orderno": student.orderno,
            "has_face": bool(grad.face_image_url)
        })

    return {
        "overview": {
            "total_students": total_students,
            "attended": attended,
            "not_attended": not_attended,
            "pending": pending,
            "checked_in_count": checked_in_count,             # ส่งจำนวนคนเช็คชื่อ
            "checked_in_with_face": checked_in_with_face,     # ส่งจำนวนคนเช็คชื่อที่มีรูป
            "checkin_percentage": checkin_percentage,         # ส่ง %
            "active_schedule_name": schedule_name,             # ส่งชื่อรอบปัจจุบัน
            "active_schedule_date": schedule_date             # ส่งวันที่รอบปัจจุบัน
        },
        "faculties": faculties,
        "recent_activities": recent_activities
    }

@router.get("/attendance-stats")
def get_attendance_dashboard_stats(db: Session = Depends(get_db)):
    # 1. ยอดเป้าหมาย (บัณฑิตที่ตอบรับเข้าร่วม)
    attended_target = db.query(models.Graduation).filter(models.Graduation.is_attending < 20).count()
    
    # 2. หารอบเช็คชื่อปัจจุบัน
    active_schedule = db.query(models.MstEventSchedule).filter(models.MstEventSchedule.is_active == True).first()
    
    recent_point_1 = []
    recent_point_2 = []
    
    if active_schedule:
        schedule_name = active_schedule.event_name
        schedule_date = active_schedule.event_date
        checked_in_count = db.query(models.AttendanceLog).filter(models.AttendanceLog.schedule_id == active_schedule.id).count()
        
        checked_in_with_face = db.query(models.AttendanceLog)\
            .join(models.Graduation, models.AttendanceLog.student_id == models.Graduation.student_id)\
            .filter(models.AttendanceLog.schedule_id == active_schedule.id)\
            .filter(models.Graduation.face_image_url.is_not(None))\
            .count()
            
        # --- ฟังก์ชันช่วยดึงข้อมูล 5 คนล่าสุดของแต่ละจุด ---
        def get_recent_by_point(point_name):
            logs = db.query(models.AttendanceLog, models.GradStudent, models.Graduation)\
                .join(models.GradStudent, models.AttendanceLog.student_id == models.GradStudent.id)\
                .outerjoin(models.Graduation, models.GradStudent.id == models.Graduation.student_id)\
                .filter(models.AttendanceLog.schedule_id == active_schedule.id)\
                .filter(models.AttendanceLog.checkin_point == point_name)\
                .order_by(models.AttendanceLog.timestamp.desc())\
                .limit(5).all()
            
            result = []
            for log, student, grad in logs:
                result.append({
                    "time": log.timestamp.strftime("%H:%M") if log.timestamp else "-",
                    "code": student.studentcode,
                    "name": f"{student.studentname} {student.studentsurname}",
                    "faculty": student.facultyname,
                    "has_face": bool(grad and grad.face_image_url),
                    "orderno": student.orderno
                })
            return result
        # -----------------------------------------------
        
        recent_point_1 = get_recent_by_point("1")
        recent_point_2 = get_recent_by_point("2")
        
    else:
        schedule_name = "ยังไม่ได้เปิดรอบการเช็คชื่อ"
        checked_in_count = 0
        checked_in_with_face = 0

    checkin_percentage = round((checked_in_count / attended_target * 100), 1) if attended_target > 0 else 0

    return {
        "overview": {
            "target": attended_target,
            "checked_in_count": checked_in_count,
            "checked_in_with_face": checked_in_with_face,
            "checkin_percentage": checkin_percentage,
            "active_schedule_name": schedule_name,
            "active_schedule_date": schedule_date
        },
        "recent_point_1": recent_point_1,
        "recent_point_2": recent_point_2
    }