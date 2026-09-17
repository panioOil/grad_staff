<template>
  <div class="h-screen flex overflow-hidden bg-slate-50">
    
    <!-- ฉากหลังสีดำโปร่งแสงตอนเปิดเมนูบนมือถือ (คลิกเพื่อปิด) -->
    <div 
      v-if="isSidebarOpen" 
      @click="isSidebarOpen = false" 
      class="fixed inset-0 z-20 bg-slate-900/60 backdrop-blur-sm md:hidden transition-opacity"
    ></div>

    <!-- Sidebar (ซ่อนอัตโนมัติบนมือถือ, แสดงตลอดบนจอใหญ่) -->
    <aside 
      :class="isSidebarOpen ? 'translate-x-0' : '-translate-x-full'" 
      class="fixed inset-y-0 left-0 z-30 w-64 bg-slate-900 text-slate-300 flex flex-col transition-transform duration-300 ease-in-out md:relative md:translate-x-0 shadow-2xl md:shadow-none"
    >
      <!-- Logo / Branding -->
      <div class="h-16 flex items-center justify-between px-6 border-b border-slate-800/60 md:justify-center">
        <div class="flex items-center gap-2">
          <GraduationCap class="w-7 h-7 text-amber-500 stroke-[1.5]" />
          <h1 class="text-xl font-bold text-white tracking-wide">
            GCMS <span class="text-amber-500">MFU</span>
          </h1>
        </div>
        <!-- ปุ่มปิดเมนูบนมือถือ -->
        <button @click="isSidebarOpen = false" class="md:hidden text-slate-400 hover:text-white transition-colors">
          <X class="w-6 h-6 stroke-[1.5]" />
        </button>
      </div>
      
      <!-- Navigation Menu -->
      <nav class="flex-1 overflow-y-auto py-6 custom-scrollbar">
        <ul class="space-y-1.5 px-3 text-sm font-medium">
          
          <li v-if="['admin', 'staff', 'pat_staff', 'reg_staff', 'other'].includes(currentUser?.role)">
            <router-link to="/dashboard" @click="isSidebarOpen = false" 
              class="flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-slate-800 hover:text-white transition-all duration-200" 
              active-class="bg-slate-800/80 text-amber-400 shadow-sm ring-1 ring-slate-700/50">
              <LayoutDashboard class="w-5 h-5 stroke-[1.5]" /> ภาพรวมลงทะเบียน
            </router-link>
          </li>
          
          <li v-if="['admin', 'staff', 'pat_staff', 'reg_staff', 'other'].includes(currentUser?.role)">
            <router-link to="/attendance-dashboard" @click="isSidebarOpen = false"
              class="flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-slate-800 hover:text-white transition-all duration-200"
              active-class="bg-slate-800/80 text-amber-400 shadow-sm ring-1 ring-slate-700/50">
              <Activity class="w-5 h-5 stroke-[1.5]" /> ภาพรวมเข้าฝึกซ้อม
            </router-link>
          </li>
          
          <li v-if="['admin', 'staff', 'pat_staff'].includes(currentUser?.role)">
            <router-link to="/students" @click="isSidebarOpen = false" 
              class="flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-slate-800 hover:text-white transition-all duration-200" 
              active-class="bg-slate-800/80 text-amber-400 shadow-sm ring-1 ring-slate-700/50">
              <Users class="w-5 h-5 stroke-[1.5]" /> จัดการข้อมูลบัณฑิต
            </router-link>
          </li>
          
          <li v-if="['admin', 'staff', 'pat_staff'].includes(currentUser?.role)">
            <router-link to="/attendance" @click="isSidebarOpen = false" 
              class="flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-slate-800 hover:text-white transition-all duration-200" 
              active-class="bg-slate-800/80 text-amber-400 shadow-sm ring-1 ring-slate-700/50">
              <CheckSquare class="w-5 h-5 stroke-[1.5]" /> เช็คชื่อเข้าฝึกซ้อม
            </router-link>
          </li>
          
          <li v-if="['admin', 'staff', 'pat_staff', 'reg_staff'].includes(currentUser?.role)">
            <router-link to="/attendance-verify" @click="isSidebarOpen = false" 
              class="flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-slate-800 hover:text-white transition-all duration-200" 
              active-class="bg-slate-800/80 text-amber-400 shadow-sm ring-1 ring-slate-700/50">
              <FileSearch class="w-5 h-5 stroke-[1.5]" /> ตรวจสอบการเข้าพิธี
            </router-link>
          </li>
          
          <li v-if="['admin', 'staff'].includes(currentUser?.role)">
            <router-link to="/face" @click="isSidebarOpen = false" 
              class="flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-slate-800 hover:text-white transition-all duration-200" 
              active-class="bg-slate-800/80 text-amber-400 shadow-sm ring-1 ring-slate-700/50">
              <Camera class="w-5 h-5 stroke-[1.5]" /> บันทึกใบหน้า น.ศ.
            </router-link>
          </li>
          
          <li v-if="['admin', 'staff'].includes(currentUser?.role)">
            <router-link to="/print-id-card" @click="isSidebarOpen = false" 
              class="flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-slate-800 hover:text-white transition-all duration-200" 
              active-class="bg-slate-800/80 text-amber-400 shadow-sm ring-1 ring-slate-700/50">
              <Printer class="w-5 h-5 stroke-[1.5]" /> พิมพ์บัตรประจำตัว น.ศ.
            </router-link>
          </li>
          
        </ul>
        
        <!-- Divider & Settings -->
        <div class="mt-6 pt-6 border-t border-slate-800/60 px-3">
          <ul class="space-y-1.5 text-sm font-medium">
            <li v-if="['admin', 'staff'].includes(currentUser?.role)">
              <router-link to="/system-settings" @click="isSidebarOpen = false" 
                class="flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-slate-800 hover:text-white transition-all duration-200" 
                active-class="bg-slate-800/80 text-amber-400 shadow-sm ring-1 ring-slate-700/50">
                <Settings class="w-5 h-5 stroke-[1.5]" /> ตั้งค่าระบบ
              </router-link>
            </li>
          </ul>
        </div>
      </nav>
      
      <!-- Mock SSO Dropdown (Dark Theme) -->
      <!-- <div class="p-5 bg-slate-950/50 border-t border-slate-800/60">
        <label class="text-xs font-medium text-slate-400 mb-2 block flex items-center gap-2">
          <ShieldAlert class="w-3.5 h-3.5" /> ทดสอบเปลี่ยนสิทธิ์
        </label>
        <div class="relative">
          <select v-model="currentUser" class="w-full appearance-none bg-slate-800 border border-slate-700 text-slate-200 text-sm py-2 pl-3 pr-8 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500/50 focus:border-amber-500 transition-colors">
            <option value="admin">Admin (ผู้ดูแลระบบ)</option>
            <option value="staff">Staff (เจ้าหน้าที่)</option>
            <option value="pat_staff">จนท. ส่วนพัฒฯ</option>
            <option value="reg_staff">จนท. ทะเบียน</option>
            <option value="other">หน่วยงานอื่นๆ</option>
          </select>
          <ChevronDown class="absolute right-2.5 top-2.5 w-4 h-4 text-slate-400 pointer-events-none stroke-[1.5]" />
        </div>
      </div> -->
    </aside>

    <!-- Main Content Area -->
    <main class="flex-1 flex flex-col min-w-0 overflow-hidden">
      
      <!-- Header -->
      <header class="h-16 bg-white/80 backdrop-blur-md border-b border-slate-200 flex items-center justify-between px-4 md:px-8 z-10">
        <div class="flex items-center">
          <!-- ปุ่ม Hamburger Menu -->
          <button 
            @click="isSidebarOpen = !isSidebarOpen" 
            class="md:hidden mr-4 text-slate-500 hover:text-slate-800 focus:outline-none bg-slate-100 p-1.5 rounded-md"
          >
            <Menu class="h-5 w-5 stroke-[1.5]" />
          </button>
          
          <h2 class="text-lg md:text-xl font-semibold text-slate-800 tracking-tight">{{ $route.name || 'GraduFlow' }}</h2>
        </div>
        
        <!-- Role Badge (สไตล์ Pill สวยๆ) -->
        <!-- <div class="inline-flex items-center gap-1.5 px-5 py-1.5 rounded-full bg-amber-50 border border-amber-200/60 text-xs md:text-sm font-medium text-amber-700 shadow-sm">
          <div class="text-right">
            <div class="text-sm font-semibold text-slate-800">
              {{ currentUser?.given_name }} {{ currentUser?.family_name }}
            </div>
            <div class="text-xs text-slate-500">
              {{ currentUser?.depart_name }} ({{ currentUser?.role }})
            </div>
          </div>
          <span class="w-2 h-2 rounded-full bg-amber-500 animate-pulse"></span>
          Role: <span class="font-bold text-amber-900 ml-0.5">{{ userRole }}</span>
        
          <button 
            @click="handleLogout"
            class="bg-rose-50 text-rose-600 hover:bg-rose-100 px-3 py-1.5 rounded-lg text-sm font-medium transition flex items-center gap-1.5 border border-rose-200"
          >
            <span>🚪</span>
            <span>ออกจากระบบ</span>
          </button>
        </div> -->
        <!-- โปรไฟล์และปุ่มออกจากระบบ (ดีไซน์ใหม่ เรียบหรู กลมกลืน) -->
        <div class="inline-flex items-center gap-3 px-4 py-1.5 rounded-full bg-white border border-slate-200 shadow-sm">
          
          <!-- วงกลมแสดงตัวย่อชื่อ (Avatar) -->
          <div class="w-8 h-8 rounded-full bg-amber-500/10 text-amber-700 font-bold flex items-center justify-center text-xs border border-amber-500/20 shrink-0">
            {{ currentUser?.given_name?.charAt(0) || 'U' }}
          </div>

          <!-- ข้อมูลผู้ใช้ (ชื่อ, แผนก, บทบาท) -->
          <div class="text-left flex flex-col leading-tight">
            <div class="text-xs md:text-sm font-semibold text-slate-800">
              {{ currentUser?.given_name }} {{ currentUser?.family_name }}
            </div>
            <div class="text-[11px] text-slate-500 flex items-center gap-1.5 mt-0.5">
              <span>{{ currentUser?.depart_name }}</span>
              <span class="w-1 h-1 rounded-full bg-slate-300"></span>
              <span class="text-amber-700 font-semibold uppercase tracking-wider text-[9px] bg-amber-50 px-1 py-0.2 rounded border border-amber-200">
                {{ currentUser?.role }}
              </span>
            </div>
          </div>

          <!-- เส้นคั่น -->
          <div class="h-5 w-[1px] bg-slate-200 mx-0.5"></div>

          <!-- ปุ่มออกจากระบบแบบไอคอนกลมกลืน -->
          <button 
            @click="handleLogout"
            class="text-slate-400 hover:text-rose-600 hover:bg-rose-50 p-1.5 rounded-full transition-all duration-200 flex items-center justify-center group"
            title="ออกจากระบบ"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 transition-transform group-hover:scale-110" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
          </button>
          
        </div>
      </header>
      
      <!-- Content -->
      <div class="flex-1 overflow-y-auto p-4 md:p-8 bg-slate-50/50">
        <router-view></router-view>
      </div>
      
    </main>
  </div>
</template>

<script setup>
import { ref,onMounted } from 'vue';
import { useRouter } from 'vue-router'
// Import ไอคอนทั้งหมดที่ใช้จาก lucide
import { 
  Menu, X, LayoutDashboard, Users, CheckSquare, 
  FileSearch, Camera, Printer, Settings, ChevronDown, 
  GraduationCap, ShieldAlert, Activity 
} from 'lucide-vue-next';

const isSidebarOpen = ref(false);
const userRole = ref('admin');
const router = useRouter()
const currentUser = ref(null)
onMounted(() => {
  // ดึงข้อมูล session ผู้ใช้ที่ล็อกอินอยู่มาแสดง
  const session = localStorage.getItem('user_session')
  if (session) {
    currentUser.value = JSON.parse(session)
  }
})
const handleLogout = () => {
  // 1. ลบข้อมูล session ออกจากเครื่อง
  localStorage.removeItem('user_session')
  
  // 2. ดีดกลับไปหน้า Login ทันที
  router.push('/login')
}
</script>

<style scoped>
/* แต่ง Scrollbar ของเมนูให้ดูเนียนตา ไม่เกะกะ */
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #334155; /* slate-700 */
  border-radius: 10px;
}
</style>