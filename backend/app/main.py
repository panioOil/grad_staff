from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .routers import graduations  # เพิ่มบรรทัดนี้ลงไปตรงกลุ่มที่มีการ import routers

# Import การตั้งค่า Database
from app.database import Base, engine

# Import Router ต่างๆ ที่แยกไฟล์ไว้
from app.routers import attendance, dashboard, students, settings,graduations

# 1. สั่งให้ SQLAlchemy สร้างตารางใน PostgreSQL อัตโนมัติ (จาก models.py)
Base.metadata.create_all(bind=engine)

# 2. เริ่มต้นสร้างตัวแอปพลิเคชัน FastAPI
app = FastAPI(
    title="GraduFlow API",
    description="Backend API สำหรับระบบจัดการข้อมูลบัณฑิต",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # อนุญาตทุก Origin ในช่วงพัฒนา
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class StaticFilesWithCORS(StaticFiles):
    async def get_response(self, path: str, scope):
        response = await super().get_response(path, scope)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "*"
        return response

app.mount("/uploads/faces", StaticFiles(directory=r"D:\MyProjects\GraduFlow\uploads\faces"), name="uploads")
app.mount("/pic", StaticFilesWithCORS(directory=r"D:\MyProjects\pic"), name="pic")


# 4. ลงทะเบียน Router (ประกอบร่าง API เส้นต่างๆ เข้าสู่ระบบหลัก)
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(students.router, prefix="/api/students", tags=["Students"])
app.include_router(attendance.router, prefix="/api/attendance", tags=["Attendance"])
app.include_router(graduations.router, prefix="/api/graduations", tags=["Graduations"])
app.include_router(settings.router)
# หากมีเมนูอื่นๆ ในอนาคต (เช่น attendance, delivery) ให้นำมาเพิ่มบรรทัด include_router ตรงนี้

# 5. Root Endpoint (หน้าแรกสุดสำหรับทดสอบว่า API ทำงานหรือไม่)
@app.get("/", tags=["Health Check"])
def read_root():
    return {
        "status": "online", 
        "message": "GraduFlow_v2 API is up and running"
    }

