from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from typing import List,Optional
from sqlalchemy import cast, String, Integer
import traceback
from collections import defaultdict

from fastapi.responses import StreamingResponse
import io
# นำเข้า ReportLab
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# สร้าง Router และกำหนด Prefix (URL หลัก) ให้กับ API กลุ่มนี้
router = APIRouter()


@router.get("/attendees")
def get_attending_students(db: Session = Depends(get_db)):
    try:
        # JOIN ตารางนักศึกษา, การเข้ารับ, สำนักวิชา และ สาขาวิชา
        query_results = db.query(
            models.GradStudent,
            models.Graduation,
            models.Faculty,
            models.Department
        ) \
            .join(models.Graduation, models.GradStudent.id == models.Graduation.student_id) \
            .join(models.Faculty, models.GradStudent.facultyid == cast(models.Faculty.facultyid, String)) \
            .join(models.Department, models.GradStudent.departmentid == cast(models.Department.departmentid, String)) \
            .filter(models.Graduation.status == "success",
                    models.Graduation.is_attending.cast(Integer) < 20) \
            .order_by(models.GradStudent.facultyid,models.GradStudent.orderno).all()

        # จัดรูปแบบข้อมูล
        attendees = []
        for student, grad, faculty, dept in query_results:
            attendees.append({
                "studentcode": student.studentcode,
                "studentname": f"{student.prefixname}{student.studentname} {student.studentsurname}",
                "acadyear": student.acadyear,  # ปรับเป็นชื่อฟิลด์ปีการศึกษาที่ถูกต้อง
                "facultyid": student.facultyid,
                "facultyname": faculty.facultyname,  # ปรับเป็นชื่อฟิลด์ที่เก็บชื่อสำนักวิชา เช่น faculty_name_th
                "programname": dept.departmentname,  # ปรับเป็นชื่อฟิลด์ที่เก็บชื่อสาขา เช่น department_name_th
                "orderno": student.orderno  # ปรับเป็นชื่อฟิลด์ลำดับที่นั่ง
            })

        return attendees

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/faculties", response_model=List[schemas.FacultyResponse])
def get_faculties(db: Session = Depends(get_db)):
    try:
        return db.query(models.Faculty).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/departments", response_model=List[schemas.DepartmentResponse])
def get_departments(db: Session = Depends(get_db)):
    try:
        return db.query(models.Department).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/all-graduates/{acad_year}")
async def get_all_graduates_by_year(acad_year: int, db: Session = Depends(get_db)):
    try:

        # ใช้ outerjoin เพื่อทำ Left Join
        results = db.query(models.GradStudent, models.Graduation) \
            .outerjoin(models.Graduation, models.GradStudent.id == models.Graduation.student_id) \
            .filter(models.GradStudent.acadyear == acad_year) \
            .order_by(models.GradStudent.orderno) \
            .all()

        # print(f"ดึงข้อมูลสำเร็จ: พบ {len(results)} แถว")

        # แปลงข้อมูล Tuple จากการ Join ให้เป็น List ของ Dictionary
        response_data = []
        for student, graduation in results:
            # 1. ดึงข้อมูลทุกคอลัมน์จากตาราง GradStudent ออกมาเป็น Dict
            student_dict = {c.name: getattr(student, c.name) for c in student.__table__.columns}

            # 2. ถ้ามีข้อมูลฝั่ง Graduation (Left Join แล้วเจอคู่) ให้นำมารวมกัน
            if graduation:
                grad_dict = {c.name: getattr(graduation, c.name) for c in graduation.__table__.columns}
                # ผสานฟิลด์เข้าด้วยกัน (ระวังชื่อคอลัมน์ซ้ำกัน ถ้าชื่อซ้ำฝั่ง graduation จะทับ)
                student_dict.update(grad_dict)
            else:
                # ถ้าฝั่งซ้ายมีแต่ฝั่งขวาไม่มี (เป็น NULL) กำหนดค่าว่างสำรองไว้ได้
                student_dict["is_attending"] = None

            response_data.append(student_dict)

        return response_data

    except Exception as e:
        # print("=== เกิดข้อผิดพลาด ===")
        import traceback
        # traceback.print_exc()
        return {"error": str(e)}

# 1. ลงทะเบียนฟอนต์ภาษาไทย (ชี้ Path ให้ตรงกับที่เก็บไฟล์ฟอนต์)
pdfmetrics.registerFont(TTFont('THSarabun', 'fonts/THSarabunNew.ttf'))
pdfmetrics.registerFont(TTFont('THSarabun-Bold', 'fonts/THSarabunNew Bold.ttf'))

def get_val(item, key, default=""):
        if isinstance(item, dict):
            val = item.get(key)
        else:
            val = getattr(item, key, None)
            
        # ถ้าหาไม่เจอ หรือค่าเป็น None หรือเป็นค่าว่าง ให้คืนค่า default
        if val is None or str(val).strip() == "":
            return default
        return val

@router.get("/report/pdf")
async def generate_pdf_report(
    year: Optional[str] = '2567',   # 👈 รับเป็นข้อความ และมีค่าเริ่มต้น
    facultyid: Optional[str] = '',  # 👈 รับเป็นข้อความ และมีค่าเริ่มต้นเป็นค่าว่าง
    db: Session = Depends(get_db)
):
    # แปลงปีเป็นตัวเลขสำหรับใช้คิวรี
    query_year = int(year) if year and year.isdigit() else 2567
    
    # 1. คิวรีข้อมูลเบื้องต้น
    query = db.query(models.GradStudent, models.Graduation) \
        .outerjoin(models.Graduation, models.GradStudent.id == models.Graduation.student_id) \
        .filter(models.GradStudent.acadyear == query_year)

    # 2. ถ้ามี facultyid ส่งมา (และไม่ใช่ค่าว่าง) ให้กรองเพิ่ม
    if facultyid and facultyid.strip() != "":
        query = query.filter(models.GradStudent.facultyid == facultyid)

    # 3. สั่งเรียงลำดับ และดึงข้อมูลจริงออกมา
    real_students = query.order_by(models.GradStudent.orderno).all()
    
    if not real_students:
        return {"message": "ไม่พบข้อมูลบัณฑิตที่ค้นหาในระบบ"}

    # ==========================================
    # 2. จัดกลุ่มข้อมูล (สำนักวิชา -> หลักสูตร)
    # ==========================================
    grouped_data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    
    for row in real_students:
        std = row[0] 
        
        # 💡 ลองปริ้นท์ดูชื่อคอลัมน์ที่แท้จริง (ถ้าระบบทำงานได้แล้ว ลบ 3 บรรทัดนี้ทิ้งได้เลยครับ)
        # print("====== ชื่อคอลัมน์ใน Database ======")
        # print(std.__dict__.keys()) 
        # print("=================================")
        
        # เปลี่ยนมาใช้ get_val (ถ้าชื่อคอลัมน์ใน Database สะกดไม่เหมือนข้างล่างนี้ อย่าลืมแก้ให้ตรงนะครับ)
        lev_name = get_val(std, "levelname", "ไม่ระบุระดับ") 
        fac_name = get_val(std, "facultyname", "ไม่ระบุสำนักวิชา") 
        prog_name = get_val(std, "programname", "ไม่ระบุหลักสูตร")
        
        grouped_data[lev_name][fac_name][prog_name].append(std)

    # ==========================================
    # 3. ตั้งค่าหน้ากระดาษ PDF
    # ==========================================
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=landscape(A4),
        rightMargin=20, leftMargin=20, topMargin=25, bottomMargin=20 # ปรับขอบกระดาษที่นี่
    )
    elements = []
    
    header_style = ParagraphStyle(name='Header', fontName='THSarabun-Bold', fontSize=20, alignment=1, leading=22)
    subheader_style = ParagraphStyle(name='SubHeader', fontName='THSarabun-Bold', fontSize=16, alignment=1, leading=20)
    degree_style = ParagraphStyle(name='Degree', fontName='THSarabun-Bold', fontSize=14, alignment=0,leftIndent=0)
    degree_right_style = ParagraphStyle(name='DegreeRight', fontName='THSarabun-Bold', fontSize=12, alignment=2)

    ROWS_PER_PAGE = 18 # ปรับจำนวนแถวต่อ 1 หน้าตามความเหมาะสม (เช่น 35-40 คน)

    # ==========================================
    # 4. วาดตารางทีละกลุ่มหลักสูตร
    # ==========================================
    for lev_name, faculties in grouped_data.items():
        for fac_name, programs in faculties.items():
            for prog_name, students in programs.items():
                
                # หั่นนักศึกษาในหลักสูตรนี้เป็นหน้าๆ (หน้าละ 35 คน)
                chunks = [students[i:i + ROWS_PER_PAGE] for i in range(0, len(students), ROWS_PER_PAGE)]
                total_parts = len(chunks)
                
                for part_idx, chunk in enumerate(chunks):
                    # 💡 แก้ไขหัวรายงานให้ดึง lev_name และ fac_name มาแสดงอย่างถูกต้อง
                    elements.append(Paragraph(f"ใบลงทะเบียนพิธีพระราชทานปริญญาบัตร ประจำปีการศึกษา {year}", header_style))
                    elements.append(Paragraph(f"ระดับ{lev_name}", subheader_style))
                    elements.append(Paragraph(f"สำนักวิชา{fac_name}", subheader_style))
                    elements.append(Spacer(1, 15))
                    
                    col_widths = [30, 30, 115, 115, 80, 45, 45, 45, 45, 45, 45, 45]
                    total_width = sum(col_widths)
                    # แถบชื่อหลักสูตร และเลขหน้า
                    part_text = f"( {part_idx + 1} / {total_parts} )"
                    
                    # จับยัดใส่ตารางล่องหน 1 แถว 2 คอลัมน์
                    header_table_data = [[
                        Paragraph(prog_name, degree_style),
                        Paragraph(part_text, degree_right_style)
                    ]]
                    
                    # แบ่งพื้นที่: ฝั่งขวาเอาไป 80 จุด ที่เหลือดันให้ฝั่งซ้ายทั้งหมด
                    ht = Table(header_table_data, colWidths=[total_width - 80, 80])
                    ht.setStyle(TableStyle([
                        ('VALIGN', (0,0), (-1,-1), 'BOTTOM'), # จัดข้อความชิดขอบล่าง
                        ('LEFTPADDING', (0,0), (-1,-1), 0),   # ลบช่องว่างขอบซ้ายขวาออกให้แนบสนิท
                        ('RIGHTPADDING', (0,0), (-1,-1), 0),
                        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
                    ]))
                    
                    elements.append(ht)
                    elements.append(Spacer(1, 10)) # ระยะห่างก่อนถึงตารางหลัก
                    
                    # โครงสร้างตาราง (หัวตาราง 2 บรรทัด)
                    table_data = [
                        ["ลำดับ", "ที่", "ชื่อ", "สกุล", "รหัสนักศึกษา", "วันรายงานตัว", "", "วันซ้อมย่อย", "", "วันซ้อมใหญ่", "", "พิธีฯ"],
                        ["", "", "", "", "", "เช้า", "บ่าย", "เช้า", "บ่าย", "เช้า", "บ่าย", ""]
                    ]
                    
                    highlight_rows = [] # 💡 1. สร้าง List มาเก็บเลขบรรทัดที่จะไฮไลท์
                    
                    # ดึงข้อมูลจริงลงตาราง
                    for index, std in enumerate(chunk):
                        row_data = [
                            str(get_val(std, "orderno", "")),
                            str((part_idx * ROWS_PER_PAGE) + index + 1),
                            str(get_val(std, "studentname", "")),
                            str(get_val(std, "studentsurname", "-")),
                            str(get_val(std, "is_attending", "")),
                            "", "", "", "", "", "", "" 
                        ]
                        table_data.append(row_data)
                        
                        # 💡 2. เช็คเงื่อนไข "ไม่เข้ารับ" 
                        # (*** จุดนี้คุณออยต้องเปลี่ยนชื่อฟิลด์ "status" และค่า "ไม่เข้ารับ" ให้ตรงกับใน Database นะครับ ***)
                        attend_status = get_val(std, "is_attending", "0")
                        try:
                            status_num = int(attend_status)
                            print("ss==",get_val(std, "is_attending", "0"))
                            if status_num > 19:
                                highlight_rows.append(index + 2)
                        except (ValueError, TypeError):
                            pass
                
                    # กำหนดความกว้างคอลัมน์ (รวมกันให้ได้ประมาณ 780-800)
                    # [25, 25] คือความสูงของ "หัวตาราง" บรรทัดที่ 1 และ 2
                    # [14] คือความสูงของ "แถวรายชื่อนักศึกษา" (ปรับเลข 14 ให้มาก/น้อยตามต้องการ)
                    col_widths = [30, 30, 115, 115, 80, 45, 45, 45, 45, 45, 45, 45]
                    t = Table(table_data, colWidths=col_widths, rowHeights=[15, 15] + [18] * len(chunk))
                    
                    # 💡 3. แยก Style ออกมาเป็นตัวแปรก่อน
                    style_commands = [
                        ('FONT', (0,0), (-1,-1), 'THSarabun', 12),
                        ('FONT', (0,0), (-1,1), 'THSarabun-Bold', 12),
                        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
                        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                        ('SPAN', (0,0), (0,1)), ('SPAN', (1,0), (1,1)), 
                        ('SPAN', (2,0), (2,1)), ('SPAN', (3,0), (3,1)), 
                        ('SPAN', (4,0), (4,1)), ('SPAN', (11,0), (11,1)),
                        ('SPAN', (5,0), (6,0)), ('SPAN', (7,0), (8,0)), ('SPAN', (9,0), (10,0)),
                        ('BACKGROUND', (0,0), (-1,1), colors.lightgrey),
                        ('TOPPADDING', (0,0), (-1,1), 1),
                        ('BOTTOMPADDING', (0,0), (-1,1), 2),
                    ]
                    
                    # 💡 4. วนลูปเทสีเทา (#cbd5e1) ให้กับแถวที่จดเลขบรรทัดไว้
                    for row_idx in highlight_rows:
                        # ('BACKGROUND', (คอลัมน์แรก, แถว), (คอลัมน์สุดท้าย, แถว), สี)
                        style_commands.append(('BACKGROUND', (0, row_idx), (-1, row_idx), colors.HexColor('#cbd5e1')))
                        
                    # ยัด Style ทั้งหมดกลับเข้าไปในตาราง
                    t.setStyle(TableStyle(style_commands))
                    
                    elements.append(t)
                
                # ขึ้นหน้าใหม่หากไม่ใช่หน้าสุดท้ายของข้อมูลทั้งหมด
                elements.append(PageBreak())

    # ==========================================
    # 5. สร้าง PDF และส่งกลับ
    # ==========================================
    doc.build(elements)
    buffer.seek(0)
    
    return StreamingResponse(buffer, media_type="application/pdf", headers={
        "Content-Disposition": f"attachment; filename=Graduation_Report_{year}.pdf"
    })