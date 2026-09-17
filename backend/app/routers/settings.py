from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, date
from ..database import get_db
from .. import models

router = APIRouter(prefix="/api/settings", tags=["Settings"])

# --- 1. API สำหรับตั้งค่าทั่วไป (ลงทะเบียน) ---
class SettingUpdate(BaseModel):
    academic_year: str
    reg_start_date: str
    reg_end_date: str
    announcement: str

@router.get("/general")
def get_general_settings(db: Session = Depends(get_db)):
    settings = db.query(models.SystemSetting).all()
    # แปลงจาก Row ให้กลายเป็น Dictionary เพื่อง่ายต่อการใช้ใน Frontend
    result = {s.setting_key: s.setting_value for s in settings}
    return result

@router.post("/general")
def update_general_settings(data: SettingUpdate, db: Session = Depends(get_db)):
    # เตรียมข้อมูลที่ต้องการอัปเดต
    settings_data = {
        "academic_year": data.academic_year,
        "reg_start_date": data.reg_start_date,
        "reg_end_date": data.reg_end_date,
        "announcement": data.announcement
    }
    
    for key, value in settings_data.items():
        setting = db.query(models.SystemSetting).filter(models.SystemSetting.setting_key == key).first()
        if setting:
            setting.setting_value = value
        else:
            new_setting = models.SystemSetting(setting_key=key, setting_value=value)
            db.add(new_setting)
            
    db.commit()
    return {"message": "บันทึกการตั้งค่าสำเร็จ"}

# --- 2. API สำหรับจัดการรอบการซ้อม (Event Schedules) ---
class ScheduleCreate(BaseModel):
    event_name: str
    event_date: Optional[str] = None

@router.get("/schedules")
def get_schedules(db: Session = Depends(get_db)):
    return db.query(models.MstEventSchedule).order_by(models.MstEventSchedule.id).all()

@router.post("/schedules")
def add_schedule(data: ScheduleCreate, db: Session = Depends(get_db)):
    # ใส่ datetime ชั่วคราว (หรือจะแปลงจาก string ก็ได้)
    new_sched = models.MstEventSchedule(
        event_name=data.event_name,
        is_active=False
    )
    db.add(new_sched)
    db.commit()
    db.refresh(new_sched)
    return new_sched

@router.put("/schedules/{sched_id}/toggle")
def toggle_schedule(sched_id: int, db: Session = Depends(get_db)):
    # 1. ปิดทุกรอบก่อน (เพื่อให้มีรอบที่ Active ได้แค่รอบเดียว)
    db.query(models.MstEventSchedule).update({models.MstEventSchedule.is_active: False})
    
    # 2. เปิดรอบที่เลือก
    target = db.query(models.MstEventSchedule).filter(models.MstEventSchedule.id == sched_id).first()
    if target:
        target.is_active = True
        db.commit()
        return {"message": f"เปิดรอบ {target.event_name} สำเร็จ"}
    raise HTTPException(status_code=404, detail="ไม่พบรอบการซ้อมนี้")

@router.delete("/schedules/{sched_id}")
def delete_schedule(sched_id: int, db: Session = Depends(get_db)):
    target = db.query(models.MstEventSchedule).filter(models.MstEventSchedule.id == sched_id).first()
    if target:
        db.delete(target)
        db.commit()
        return {"message": "ลบสำเร็จ"}
    return {"message": "ไม่พบข้อมูล"}

class ScheduleUpdate(BaseModel):
    event_name: str
    event_date: Optional[date] = None

@router.put("/schedules/{schedule_id}")
def update_schedule(schedule_id: int, data: ScheduleUpdate, db: Session = Depends(get_db)):
    # 1. ค้นหาข้อมูลเดิมจาก Database ก่อน
    schedule = db.query(models.MstEventSchedule).filter(models.MstEventSchedule.id == schedule_id).first()
    
    if schedule:
        # 2. กำหนดค่าใหม่ผ่านตัว instance (Pylance จะไม่ฟ้อง error นี้แล้ว)
        schedule.event_name = data.event_name
        schedule.event_date = data.event_date

    db.commit()
    db.refresh(schedule)
    
    return {"message": "Updated successfully", "data": schedule}

# --- 3. API สำหรับจัดการข้อความหน้า Login ฝั่งบัณฑิต ---
class LoginSettingUpdate(BaseModel):
    login_title_th: str
    login_title_en: str
    login_year_th: str
    login_year_en: str
    login_date_th: str
    login_date_en: str
    login_footer: str
    login_announcement: str


@router.get("/login-page")
def get_login_settings(db: Session = Depends(get_db)):
    # กำหนด Key ที่เกี่ยวข้องกับหน้า Login
    keys = [
        "login_title_th", "login_title_en",
        "login_year_th", "login_year_en",
        "login_date_th", "login_date_en",
        "login_footer", "login_announcement"
    ]
    settings = db.query(models.SystemSetting).filter(models.SystemSetting.setting_key.in_(keys)).all()

    # ถ้ายังไม่มีข้อมูลใน DB ให้ส่งค่าว่างกลับไปก่อน
    result = {key: "" for key in keys}
    for s in settings:
        result[s.setting_key] = s.setting_value

    return result


@router.post("/login-page")
def update_login_settings(data: LoginSettingUpdate, db: Session = Depends(get_db)):
    settings_data = data.dict()

    for key, value in settings_data.items():
        setting = db.query(models.SystemSetting).filter(models.SystemSetting.setting_key == key).first()
        if setting:
            setting.setting_value = value
        else:
            new_setting = models.SystemSetting(setting_key=key, setting_value=value)
            db.add(new_setting)

    db.commit()
    return {"message": "บันทึกการตั้งค่าหน้า Login สำเร็จ"}