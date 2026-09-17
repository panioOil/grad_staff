import { createRouter, createWebHistory } from 'vue-router'
// import Layout from '..//Layout.vue'

// 
const routes = [
  { path: '/login', name: 'Login', component: () => import('../views/Login.vue') },
  {
    path: '/',
    component: () => import('../Layout.vue'),
    redirect: '/dashboard',
    meta: { requiresAuth: true },
    children: [
      // เข้าได้: admin, staff, pat_staff, reg_staff, other
      { path: 'dashboard', name: 'Dashboard', component: () => import('../views/Dashboard.vue'), meta: { roles: ['admin', 'staff', 'pat_staff', 'reg_staff', 'other'] } },
      { path: 'attendance-dashboard', name: 'AttendanceDashboard', component: () => import('../views/AttendanceDashboard.vue'), meta: { roles: ['admin', 'staff', 'pat_staff', 'reg_staff', 'other'] } },

      // เข้าได้: admin, staff, pat_staff
      { path: 'students', name: 'Student Management', component: () => import('../views/StudentManage.vue'), meta: { roles: ['admin', 'staff', 'pat_staff'] } },
      { path: 'attendance', name: 'Attendance Check', component: () => import('../views/AttendanceScanner.vue'), meta: { roles: ['admin', 'staff', 'pat_staff'] } },
      { path: 'print-id-card', name: 'PrintIdCard', component: () => import('../views/PrintIdCard.vue'), meta: { roles: ['admin', 'staff', 'pat_staff'] } },

      // เข้าได้: admin, staff, pat_staff, reg_staff
      { path: 'attendance-verify', name: 'AttendanceVerification', component: () => import('../views/AttendanceVerification.vue'), meta: { roles: ['admin', 'staff', 'pat_staff', 'reg_staff'] } },

      // เข้าได้: admin, staff เท่านั้น
      { path: 'face', name: 'Face Registration', component: () => import('../views/FaceRegistration.vue'), meta: { roles: ['admin', 'staff'] } },
      { path: 'system-settings', name: 'SystemSettings', component: () => import('../views/SystemSettings.vue'), meta: { roles: ['admin', 'staff'] } }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const sessionStr = localStorage.getItem('user_session')
  const user = sessionStr ? JSON.parse(sessionStr) : null

  // 1. ถ้าหน้าเว็บต้องล็อกอิน แต่ยังไม่ล็อกอิน -> ดีดไปหน้า Login
  if (to.meta.requiresAuth && !user) {
    return next({ name: 'Login' })
  }
  console.log('User role:', user.role)
  // 2. ถ้าหน้านี้จำกัดสิทธิ์ตาม Role (มี meta.roles กำหนดไว้)
  if (to.meta.roles && user) {
    // ตรวจสอบว่า Role ของผู้ใช้ตรงกับที่อนุญาตไหม
    
    const hasPermission = to.meta.roles.includes(user.role)
    if (!hasPermission) {
      alert('คุณไม่มีสิทธิ์เข้าถึงเมนูนี้')
      // ดีดกลับไปหน้าแรกสุดที่มีสิทธิ์ (เช่น Dashboard) หรือหน้าที่เคยอยู่
      return next({ name: 'Dashboard' })
    }
  }

  next()
})

export default createRouter({ history: createWebHistory(), routes })
