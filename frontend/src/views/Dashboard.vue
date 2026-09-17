<template>
  <div class="space-y-6 pb-10">
    <!-- Header -->
    <div class="flex items-center justify-between pb-2 border-b border-slate-200">
      <h3 class="text-xl md:text-2xl font-bold text-slate-800 tracking-tight flex items-center gap-3">
        <LayoutDashboard class="w-7 h-7 text-amber-500 stroke-[1.5]" />
        Dashboard ระบบบริหารจัดการบัณฑิต
      </h3>
      <button @click="fetchStats" 
              class="flex items-center gap-2 text-sm font-medium text-slate-600 bg-white border border-slate-200 px-4 py-2 rounded-lg hover:text-amber-600 hover:border-amber-300 hover:shadow-sm focus:outline-none focus:ring-2 focus:ring-amber-500/20 transition-all duration-300">
        <RefreshCcw :class="{'animate-spin text-amber-500': loading}" class="w-4 h-4 stroke-[1.5]" />
        รีเฟรชข้อมูล
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex flex-col justify-center items-center h-64 text-slate-400 gap-3">
      <Loader2 class="animate-spin w-10 h-10 text-amber-500 stroke-[1.5]" />
      <span class="text-sm font-medium animate-pulse">กำลังดึงข้อมูลล่าสุด...</span>
    </div>

    <div v-else class="space-y-8">
      
      <!-- 1. การ์ดสถิติภาพรวม (Overview Cards) -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        <!-- บัณฑิตทั้งหมด -->
        <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-6 flex items-center hover:-translate-y-1 hover:shadow-md hover:border-blue-200 transition-all duration-300 group">
          <div class="bg-slate-50 text-slate-600 border border-slate-200 p-3.5 rounded-xl mr-4 group-hover:bg-blue-50 group-hover:text-blue-600 group-hover:border-blue-200 transition-colors">
            <Users class="w-7 h-7 stroke-[1.5]" />
          </div>
          <div>
            <p class="text-xs font-medium text-slate-500 uppercase tracking-wider mb-1">จำนวนบัณฑิตทั้งหมด</p>
            <h4 class="text-3xl font-bold text-slate-800">{{ stats.overview.total_students }} <span class="text-sm font-normal text-slate-400">คน</span></h4>
          </div>
        </div>
        <!-- เข้ารับ -->
        <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-6 flex items-center hover:-translate-y-1 hover:shadow-md hover:border-emerald-200 transition-all duration-300 group">
          <div class="bg-emerald-50 text-emerald-600 border border-emerald-100 p-3.5 rounded-xl mr-4">
            <UserCheck class="w-7 h-7 stroke-[1.5]" />
          </div>
          <div>
            <p class="text-xs font-medium text-slate-500 uppercase tracking-wider mb-1">ยืนยัน "เข้ารับ"</p>
            <h4 class="text-3xl font-bold text-emerald-600">{{ stats.overview.attended }} <span class="text-sm font-normal text-slate-400">คน</span></h4>
          </div>
        </div>
        <!-- ไม่เข้ารับ -->
        <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-6 flex items-center hover:-translate-y-1 hover:shadow-md hover:border-rose-200 transition-all duration-300 group">
          <div class="bg-rose-50 text-rose-500 border border-rose-100 p-3.5 rounded-xl mr-4">
            <UserX class="w-7 h-7 stroke-[1.5]" />
          </div>
          <div>
            <p class="text-xs font-medium text-slate-500 uppercase tracking-wider mb-1">ยืนยัน "ไม่เข้ารับ"</p>
            <h4 class="text-3xl font-bold text-rose-500">{{ stats.overview.not_attended }} <span class="text-sm font-normal text-slate-400">คน</span></h4>
          </div>
        </div>
        <!-- รอดำเนินการ -->
        <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-6 flex items-center hover:-translate-y-1 hover:shadow-md hover:border-amber-200 transition-all duration-300 group">
          <div class="bg-amber-50 text-amber-500 border border-amber-100 p-3.5 rounded-xl mr-4">
            <Clock class="w-7 h-7 stroke-[1.5]" />
          </div>
          <div>
            <p class="text-xs font-medium text-slate-500 uppercase tracking-wider mb-1">รอดำเนินการ</p>
            <h4 class="text-3xl font-bold text-amber-600">{{ stats.overview.pending }} <span class="text-sm font-normal text-slate-400">คน</span></h4>
          </div>
        </div>
      </div>

      <!-- 2. ส่วนกลาง: ความคืบหน้า Face Recognition & รายการล่าสุด -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        <!-- Recent Activity -->
        <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-6 flex flex-col">
          <h4 class="text-lg font-bold text-slate-800 mb-5 flex items-center gap-2">
            <Bell class="w-5 h-5 text-amber-500 stroke-[1.5]" /> ความเคลื่อนไหวล่าสุด
          </h4>
          
          <div v-if="stats.recent_activities.length === 0" class="flex-1 flex flex-col items-center justify-center text-slate-400">
            <Activity class="w-8 h-8 mb-2 stroke-[1.5] opacity-50" />
            <span class="text-sm">ยังไม่มีการเคลื่อนไหว</span>
          </div>
          
          <ul v-else class="space-y-4 flex-1 overflow-y-auto pr-2 custom-scrollbar">
            <li v-for="activity in stats.recent_activities" :key="activity.id" class="flex items-start bg-slate-50 p-3 rounded-lg border border-slate-100">
              <span class="flex-shrink-0 w-2.5 h-2.5 mt-1.5 rounded-full mr-3 shadow-sm" :class="activity.status === 'เข้ารับ' ? 'bg-emerald-400' : 'bg-rose-400'"></span>
              <div class="flex-1 min-w-0">
                <p class="text-sm font-semibold text-slate-700 truncate">
                  {{activity.studentcode}} : {{ activity.name }} <span class="text-slate-400 font-normal">({{ activity.orderno }})</span>
                </p>
                <div class="flex items-center mt-1.5 gap-3 text-xs">
                  <span class="text-slate-500 font-medium">{{ activity.status }}</span>
                  <span v-if="activity.has_face" class="flex items-center text-slate-600 bg-white border border-slate-200 shadow-sm px-2 py-0.5 rounded-md">
                    <Camera class="w-3.5 h-3.5 mr-1.5 text-blue-500 stroke-[1.5]" />
                    อัปรูปแล้ว
                  </span>
                </div>
              </div>
            </li>
          </ul>
        </div>

        <!-- 3. ส่วนสถิติแยกตามสำนักวิชา -->
        <div class="bg-white col-span-1 lg:col-span-2 rounded-xl shadow-sm border border-slate-200 p-6">
          
          <!-- ส่วนหัวและ Dropdown เรียงลำดับ -->
          <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 border-b border-slate-100 pb-4 gap-4">
            <h3 class="text-lg font-bold text-slate-800 flex items-center gap-2">
              <BarChart3 class="w-5 h-5 text-amber-500 stroke-[1.5]" />
              ความคืบหน้าแยกสำนักวิชา
            </h3>
            
            <div class="flex items-center bg-white border border-slate-200 px-3 py-1.5 rounded-lg shadow-sm hover:border-slate-300 transition-colors">
              <ListFilter class="w-4 h-4 text-slate-400 mr-2 stroke-[1.5]" />
              <select v-model="sortOption" class="bg-transparent text-sm font-medium text-slate-700 focus:outline-none cursor-pointer pr-4 appearance-none">
                <option value="percent_desc">🔥 % ยืนยัน (สูงไปต่ำ)</option>
                <option value="percent_asc">⚠️ % ยืนยัน (ต่ำไปสูง)</option>
                <option value="code_asc">🏢 เรียงตามชื่อสำนักวิชา</option>
              </select>
            </div>
          </div>

          <!-- วนลูปแสดงผล -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div v-for="faculty in sortedFaculties" :key="faculty.id" class="p-4 border border-slate-100 rounded-xl bg-slate-50/50 hover:bg-white hover:border-amber-200 hover:shadow-md transition-all duration-300">
              
              <div class="flex justify-between items-start mb-2.5">
                <h4 class="font-bold text-slate-700 text-sm flex-1 pr-2 line-clamp-2 leading-tight flex items-start gap-2">
                  <Building2 class="w-4 h-4 text-slate-400 flex-shrink-0 mt-0.5 stroke-[1.5]" />
                  {{ faculty.name }}
                </h4>
                <span class="bg-white border border-slate-200 text-slate-700 text-xs font-bold px-2.5 py-1 rounded-md shadow-sm whitespace-nowrap">
                  {{ faculty.attend_percent }}%
                </span>
              </div>
              
              <div class="flex justify-between text-xs text-slate-500 mb-2.5 font-medium px-6">
                <span>ตอบรับ: <b class="text-slate-800">{{ faculty.attended }}</b></span>
                <span>รวม: <b class="text-slate-800">{{ faculty.total }}</b></span>
              </div>
              
              <!-- หลอด Progress Bar -->
              <div class="w-full bg-slate-200/80 rounded-full h-1.5 mt-1 overflow-hidden">
                <div 
                  class="h-1.5 rounded-full transition-all duration-1000 ease-out"
                  :class="faculty.attend_percent >= 80 ? 'bg-emerald-500' : (faculty.attend_percent >= 50 ? 'bg-amber-500' : 'bg-rose-400')"
                  :style="{ width: faculty.attend_percent + '%' }">
                </div>
              </div>
            </div>
          </div>
          
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { 
  LayoutDashboard, RefreshCcw, Loader2, Users, 
  UserCheck, UserX, Clock, Bell, Activity, 
  Camera, BarChart3, ListFilter, Building2 
} from 'lucide-vue-next';
import api from '../services/api';

const stats = ref({
  overview: {},
  faculties: [],
  recent_activities: []
});
const loading = ref(true);

const sortOption = ref('percent_desc');

const fetchStats = async () => {
  loading.value = true;
  try {
    const response = await api.get('/dashboard/stats');
    stats.value = response.data;
  } catch (error) {
    console.error('API Error:', error);
  } finally {
    loading.value = false;
  }
};

const sortedFaculties = computed(() => {
  if (!stats.value || !stats.value.faculties) return [];
  let faculties = [...stats.value.faculties];

  if (sortOption.value === 'code_asc') {
    faculties.sort((a, b) => a.id.localeCompare(b.id));
  } else if (sortOption.value === 'percent_desc') {
    faculties.sort((a, b) => b.attend_percent - a.attend_percent);
  } else if (sortOption.value === 'percent_asc') {
    faculties.sort((a, b) => a.attend_percent - b.attend_percent);
  }
  return faculties;
});

onMounted(() => {
  fetchStats();
});
</script>

<style scoped>
/* Scrollbar สำหรับลิสต์ความเคลื่อนไหวล่าสุด */
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
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