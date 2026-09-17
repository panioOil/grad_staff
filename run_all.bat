@echo off
echo ==========================================
echo Starting GraduFlow Project...
echo ==========================================

:: 1. รัน Backend ในหน้าต่างใหม่
echo Starting Backend (FastAPI on Port 8001)...
cd backend
start "GraduFlow - Backend" cmd /k "uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload"

:: ถอยกลับมาโฟลเดอร์หลัก
cd ..

:: 2. รัน Frontend ในหน้าต่างใหม่
echo Starting Frontend (Vue.js)...
cd frontend
start "GraduFlow - Frontend" cmd /k "npm run dev"

echo All services started successfully!
exit