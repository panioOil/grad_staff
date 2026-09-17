<template>
  <div class="p-4 md:p-6 space-y-6 pb-10">
    
    <!-- Header -->
    <div class="flex items-center justify-between pb-2 border-b border-slate-200">
      <h2 class="text-xl md:text-2xl font-bold text-slate-800 tracking-tight flex items-center gap-3">
        <Activity class="w-7 h-7 text-amber-500 stroke-[1.5]" />
        Dashboard: สถานการณ์เช็คชื่อ <span class="text-sm font-medium text-slate-400 ml-2 hidden sm:inline">(Live Updates)</span>
      </h2>
    </div>

    <!-- Main Content (รอโหลดข้อมูล) -->
    <div v-if="stats" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      
      <!-- กล่องซ้าย: สรุปภาพรวม -->
      <div class="lg:col-span-1 flex flex-col gap-5">
        
        <!-- การ์ดความคืบหน้ารอบปัจจุบัน -->
        <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-6 hover:shadow-md transition-shadow duration-300">
          <div class="flex items-center gap-2 mb-2">
            <Calendar class="w-4 h-4 text-slate-400 stroke-[1.5]" />
            <h4 class="text-slate-500 text-xs font-bold uppercase tracking-wider">รอบปัจจุบัน</h4>
          </div>
          <p class="text-lg text-slate-800 font-bold mb-6 flex flex-col">
            {{ stats.overview.active_schedule_name }}
            <span class="text-sm text-slate-500 font-medium font-sans mt-0.5">{{ formatDate(stats.overview.active_schedule_date) }}</span>
          </p>
          
          <div class="flex justify-between items-end mb-2">
            <div>
              <p class="text-xs text-slate-500 font-bold mb-1">ความคืบหน้าการเช็คชื่อ</p>
              <div class="flex items-baseline gap-1">
                <span class="text-4xl font-black text-emerald-600 tracking-tight">{{ stats.overview.checkin_percentage }}</span>
                <span class="text-lg font-bold text-emerald-600/70">%</span>
              </div>
            </div>
          </div>
          
          <!-- หลอด Progress Bar -->
          <div class="w-full bg-slate-100 rounded-full h-3 overflow-hidden shadow-inner mb-3">
            <div class="bg-emerald-500 h-3 rounded-full transition-all duration-1000 ease-out relative overflow-hidden" 
                 :style="{ width: stats.overview.checkin_percentage + '%' }">
                 <!-- ใส่เอฟเฟกต์เงาสะท้อนในหลอดให้ดูมีมิติ -->
                 <div class="absolute top-0 left-0 right-0 bottom-0 bg-white/20"></div>
            </div>
          </div>
          
          <div class="flex justify-between text-xs font-medium text-slate-600 bg-slate-50 p-2.5 rounded-lg border border-slate-100">
            <span class="flex items-center gap-1.5"><UserCheck class="w-4 h-4 text-emerald-500 stroke-[1.5]" /> เช็คชื่อแล้ว <b>{{ stats.overview.checked_in_count }}</b> คน</span>
            <span class="flex items-center gap-1.5"><Users class="w-4 h-4 text-slate-400 stroke-[1.5]" /> เป้าหมาย <b>{{ stats.overview.target }}</b> คน</span>
          </div>
        </div>

        <!-- Alert แจ้งเตือนคนไม่มีรูป -->
        <div v-if="stats.overview.checked_in_count > stats.overview.checked_in_with_face" 
             class="bg-rose-50 border border-rose-200 rounded-xl p-5 shadow-sm flex items-start gap-3 animate-fade-in">
          <AlertTriangle class="w-6 h-6 text-rose-500 flex-shrink-0 stroke-[1.5] mt-0.5" />
          <div>
            <h4 class="font-bold text-rose-700 text-sm mb-1">ต้องการอัปเดตใบหน้าด่วน!</h4>
            <p class="text-xs text-rose-600 leading-relaxed">
              พบ <span class="font-bold text-sm bg-rose-200/50 px-1.5 py-0.5 rounded">{{ stats.overview.checked_in_count - stats.overview.checked_in_with_face }}</span> คน ที่เช็คชื่อแล้วแต่ระบบยังไม่มีรูปถ่าย
            </p>
          </div>
        </div>
      </div>

      <!-- กล่องขวา: เรียลไทม์ Feed -->
      <div class="lg:col-span-2 bg-white rounded-xl shadow-sm border border-slate-200 p-5 md:p-6 flex flex-col">
        <div class="flex justify-between items-center mb-5 pb-3 border-b border-slate-100">
          <h4 class="text-lg font-bold text-slate-800 flex items-center gap-2">
            <History class="w-5 h-5 text-amber-500 stroke-[1.5]" /> เช็คชื่อล่าสุด
          </h4>
          <span class="flex items-center text-xs text-emerald-700 font-bold bg-emerald-50 border border-emerald-200 px-3 py-1.5 rounded-full shadow-sm">
            <Radio class="w-3.5 h-3.5 text-emerald-500 mr-1.5 animate-pulse stroke-[2]" /> Live Update
          </span>
        </div>
        
        <!-- แบ่ง 2 คอลัมน์ -->
        <div class="grid grid-cols-1 xl:grid-cols-2 gap-3 flex-1">
          
          <!-- ตารางจุดที่ 1 -->
          <div class="border border-slate-200 rounded-xl overflow-hidden flex flex-col shadow-sm">
            <div class="bg-slate-50 border-b border-slate-200 p-3.5 flex items-center gap-2">
              <MapPin class="w-5 h-5 text-blue-500 stroke-[1.5]" />
              <h5 class="font-bold text-slate-700 text-sm">จุดที่ 1 (หน้า C4)</h5>
            </div>
            <div class="overflow-x-auto flex-1 bg-white custom-scrollbar">
              <table class="w-full text-left border-collapse min-w-[300px]">
                <thead>
                  <tr class="bg-white text-slate-400 text-xs uppercase tracking-wider border-b border-slate-100">
                    <th class="p-3 font-semibold w-16">เวลา</th>
                    <th class="p-3 font-semibold">ข้อมูลบัณฑิต</th>
                    <th class="p-3 font-semibold text-center">ลำดับขึ้นรับ</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(person, index) in stats.recent_point_1" :key="index" class="border-b border-slate-50 hover:bg-slate-50/80 transition-colors">
                    <td class="p-3 text-xs text-slate-500 font-medium whitespace-nowrap">{{ person.time }}</td>
                    <td class="p-3">
                      <p class="text-sm font-bold text-slate-700">{{ person.code }}</p>
                      <p class="text-[11px] text-slate-500 truncate w-22 md:w-28">{{ person.name }}</p>
                    </td>
                    <td class="p-3 text-center">
                      <span class="inline-block bg-slate-100 text-slate-600 text-xs font-bold px-2.5 py-1 rounded-md">{{ person.orderno }}</span>
                    </td>
                  </tr>
                  <tr v-if="stats.recent_point_1.length === 0">
                    <td colspan="3" class="p-8 text-center text-slate-400 text-sm flex flex-col items-center justify-center gap-2">
                      <ScanLine class="w-6 h-6 stroke-[1.5] opacity-50" />
                      ยังไม่มีผู้เช็คชื่อผ่านจุดนี้
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- ตารางจุดที่ 2 -->
          <div class="border border-slate-200 rounded-xl overflow-hidden flex flex-col shadow-sm">
            <div class="bg-slate-50 border-b border-slate-200 p-3.5 flex items-center gap-2">
              <MapPin class="w-5 h-5 text-amber-500 stroke-[1.5]" />
              <h5 class="font-bold text-slate-700 text-sm">จุดที่ 2 (หน้า C5)</h5>
            </div>
            <div class="overflow-x-auto flex-1 bg-white custom-scrollbar">
              <table class="w-full text-left border-collapse min-w-[300px]">
                <thead>
                  <tr class="bg-white text-slate-400 text-xs uppercase tracking-wider border-b border-slate-100">
                    <th class="p-3 font-semibold w-16">เวลา</th>
                    <th class="p-3 font-semibold">ข้อมูลบัณฑิต</th>
                    <th class="p-3 font-semibold text-center">ลำดับขึ้นรับ</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(person, index) in stats.recent_point_2" :key="index" class="border-b border-slate-50 hover:bg-slate-50/80 transition-colors">
                    <td class="p-3 text-xs text-slate-500 font-medium whitespace-nowrap">{{ person.time }}</td>
                    <td class="p-3">
                      <p class="text-sm font-bold text-slate-700">{{ person.code }}</p>
                      <p class="text-[11px] text-slate-500 truncate w-22 md:w-28">{{ person.name }}</p>
                    </td>
                    <td class="p-3 text-center">
                      <span class="inline-block bg-slate-100 text-slate-600 text-xs font-bold px-2.5 py-1 rounded-md">{{ person.orderno }}</span>
                    </td>
                  </tr>
                  <tr v-if="stats.recent_point_2.length === 0">
                    <td colspan="3" class="p-8 text-center text-slate-400 text-sm flex flex-col items-center justify-center gap-2">
                      <ScanLine class="w-6 h-6 stroke-[1.5] opacity-50" />
                      ยังไม่มีผู้เช็คชื่อผ่านจุดนี้
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

        </div>
      </div>
    </div>
    
    <!-- Loading State -->
    <div v-else class="flex flex-col justify-center items-center h-64 text-slate-400 gap-3">
      <Loader2 class="animate-spin w-10 h-10 text-amber-500 stroke-[1.5]" />
      <span class="text-sm font-medium animate-pulse">กำลังเชื่อมต่อข้อมูล...</span>
    </div>
    
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { 
  Activity, Calendar, UserCheck, Users, 
  AlertTriangle, History, Radio, MapPin, 
  ScanLine, Loader2
} from 'lucide-vue-next'; // 💡 Import ไอคอนที่ใช้เพิ่มเข้ามาครับ
import api from '../services/api';

const stats = ref(null);
let refreshInterval = null;

const fetchStats = async () => {
  try {
    const response = await api.get('/dashboard/attendance-stats');
    stats.value = response.data;
  } catch (error) {
    console.error('Error fetching attendance stats:', error);
  }
};

const formatDate = (dateString) => {
  if (!dateString) return '-';
  
  const d = new Date(dateString);
  const day = String(d.getDate()).padStart(2, '0');
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const year = d.getFullYear() + 543; 

  return `${day}/${month}/${year}`;
};

onMounted(() => {
  fetchStats();
  refreshInterval = setInterval(fetchStats, 3000);
});

onUnmounted(() => {
  if (refreshInterval) clearInterval(refreshInterval);
});
</script>

<style scoped>
/* แต่ง Scrollbar ของตารางให้ดูเนียนตา */
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

/* เอฟเฟกต์เฟดตอนโหลด */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(5px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in {
  animation: fadeIn 0.4s ease-out forwards;
}
</style>