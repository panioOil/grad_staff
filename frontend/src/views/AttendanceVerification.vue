<template>
  <div class="p-4 md:p-6 max-w-7xl mx-auto space-y-6 pb-10">
    
    <!-- Header -->
    <div class="flex items-center justify-between pb-2 border-b border-slate-200">
      <h2 class="text-xl md:text-2xl font-bold text-slate-800 tracking-tight flex items-center gap-3">
        <ClipboardCheck class="w-7 h-7 text-amber-500 stroke-[1.5]" />
        ตรวจสอบประวัติการเข้าร่วมพิธี
      </h2>
    </div>

    <!-- เครื่องมือค้นหาและคัดกรอง -->
    <div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-200 flex flex-col md:flex-row gap-4">
      
      <!-- ช่องค้นหา -->
      <div class="flex-1 relative">
        <Search class="w-5 h-5 text-slate-400 absolute left-4 top-3.5 stroke-[1.5]" />
        <input 
          v-model="searchQuery" 
          @keyup.enter="fetchData"
          type="text" 
          placeholder="พิมพ์รหัสนักศึกษา หรือ ชื่อ-สกุล เพื่อค้นหา..." 
          class="w-full pl-11 pr-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-amber-500/20 focus:border-amber-500 text-slate-700 transition-all outline-none"
        >
      </div>
      
      <!-- Dropdown คัดกรองสถานะ -->
      <div class="relative min-w-[240px]">
        <Filter class="w-5 h-5 text-slate-400 absolute left-4 top-3.5 stroke-[1.5]" />
        <select 
          v-model="filterStatus" 
          @change="fetchData" 
          class="w-full pl-11 pr-10 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-amber-500/20 focus:border-amber-500 font-medium text-slate-600 transition-all outline-none appearance-none cursor-pointer"
        >
          <option value="all">สถานะรอบปัจจุบัน (ทั้งหมด)</option>
          <option value="checked_in">เข้าฮอลล์แล้ว (รอบปัจจุบัน)</option>
          <option value="pending">ยังไม่มา (รอบปัจจุบัน)</option>
        </select>
        <ChevronDown class="w-4 h-4 text-slate-400 absolute right-4 top-4 pointer-events-none stroke-[1.5]" />
      </div>

      <!-- ปุ่มค้นหา -->
      <button @click="fetchData" class="bg-slate-800 hover:bg-slate-900 text-white px-8 py-3 rounded-xl font-semibold shadow-sm transition-all flex items-center justify-center gap-2 flex-shrink-0">
        <Search class="w-4 h-4 stroke-[2]" /> ค้นหา
      </button>
    </div>

    <!-- ตารางแสดงผล -->
    <div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
      <div class="overflow-x-auto custom-scrollbar">
        <table class="w-full text-left border-collapse whitespace-nowrap min-w-[800px]">
          <thead>
            <tr class="bg-white text-slate-400 text-xs uppercase tracking-wider border-b border-slate-200">
              <th class="p-4 font-semibold text-center w-20">รูป</th>
              <th class="p-4 font-semibold text-center w-32">ลำดับขึ้นรับ</th>
              <th class="p-4 font-semibold">ข้อมูลบัณฑิต</th>
              <!-- สร้างหัวคอลัมน์แบบไดนามิก -->
              <th v-for="schedule in schedules" :key="schedule.id" class="p-4 font-semibold text-center border-l border-slate-100">
                <div class="flex items-center justify-center gap-1.5 text-slate-500">
                  <CalendarClock class="w-4 h-4 stroke-[1.5]" /> {{ schedule.name }}
                </div>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="student in students" :key="student.id" class="border-b border-slate-50 hover:bg-slate-50/80 transition-colors">
              
              <!-- รูปภาพ -->
              <td class="p-4">
                <div class="w-12 h-12 rounded-full bg-slate-50 mx-auto overflow-hidden border border-slate-200 shadow-sm flex items-center justify-center">
                  <img v-if="student.has_face" :src="`${apiUrl}/${student.face_image_url}`" class="w-full h-full object-cover">
                  <User v-else class="w-6 h-6 text-slate-300 stroke-[1.5]" />
                </div>
              </td>
              
              <!-- ลำดับขึ้นรับ -->
              <td class="p-4 text-center">
                <span class="inline-flex items-center justify-center bg-slate-100 border border-slate-200 text-slate-700 font-bold px-3 py-1.5 rounded-lg shadow-sm">
                  {{ student.orderno }}
                </span>
              </td>
              
              <!-- ข้อมูลบัณฑิต -->
              <td class="p-4">
                <p class="font-bold text-slate-800 text-sm mb-0.5">{{ student.student_code }}</p>
                <p class="text-sm font-medium text-slate-600 mb-0.5">{{ student.name }}</p>
                <p class="text-xs text-slate-400 truncate max-w-[250px]">{{ student.faculty }}</p>
              </td>
              
              <!-- วนลูปแสดงสถานะการเช็คชื่อตามคอลัมน์รอบซ้อม -->
              <td v-for="schedule in schedules" :key="schedule.id" class="p-4 text-center border-l border-slate-50">
                
                <!-- กรณีมาเช็คชื่อ -->
                <div v-if="student.attendance[schedule.id].is_checked_in" class="flex flex-col items-center justify-center gap-1">
                  <CheckCircle2 class="w-6 h-6 text-emerald-500 stroke-[1.5]" />
                  <span class="text-[11px] font-bold text-emerald-700 bg-emerald-50 border border-emerald-100 px-2 py-0.5 rounded shadow-sm">
                    {{ student.attendance[schedule.id].time }}
                  </span>
                  <span class="text-[10px] text-slate-400 font-medium">{{ student.attendance[schedule.id].point }}</span>
                </div>
                
                <!-- กรณียังไม่มาเช็คชื่อ -->
                <div v-else class="flex flex-col items-center justify-center h-full">
                  <span class="w-6 h-px bg-slate-300 rounded-full mt-3"></span>
                </div>
                
              </td>
            </tr>
            
            <!-- กรณีไม่พบข้อมูล -->
            <tr v-if="students.length === 0">
              <td :colspan="schedules.length + 3" class="p-16 text-center text-slate-400">
                <div class="flex flex-col items-center justify-center gap-3">
                  <SearchX class="w-12 h-12 text-slate-300 stroke-[1.5]" />
                  <p class="text-sm font-medium">ไม่พบข้อมูลบัณฑิตที่ค้นหา</p>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../services/api';
// 💡 Import ไอคอน Lucide ที่ใช้ในหน้านี้
import { 
  ClipboardCheck, Search, Filter, 
  ChevronDown, CalendarClock, User, 
  CheckCircle2, SearchX 
} from 'lucide-vue-next';

const apiUrl = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8001';
const schedules = ref([]);
const students = ref([]);
const searchQuery = ref('');
const filterStatus = ref('all');

const fetchData = async () => {
  try {
    const response = await api.get('/attendance/search', {
      params: {
        q: searchQuery.value,
        status: filterStatus.value
      }
    });
    // แยกรับข้อมูล หัวคอลัมน์ (schedules) และ ข้อมูลแถว (students)
    schedules.value = response.data.schedules;
    students.value = response.data.students;
  } catch (error) {
    console.error('Error fetching data:', error);
  }
};

onMounted(() => {
  fetchData();
});
</script>

<style scoped>
/* แต่ง Scrollbar ของตารางให้แนวนอนเลื่อนได้สมูทและสวยงาม */
.custom-scrollbar::-webkit-scrollbar {
  height: 6px;
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #cbd5e1;
  border-radius: 10px;
}
.custom-scrollbar:hover::-webkit-scrollbar-thumb {
  background-color: #94a3b8;
}
</style>