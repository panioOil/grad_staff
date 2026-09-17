<template>
  <div class="p-4 md:p-6 max-w-7xl mx-auto space-y-6 pb-10">
    
    <!-- Header -->
    <div class="flex items-center justify-between pb-2 border-b border-slate-200">
      <h2 class="text-xl md:text-2xl font-bold text-slate-800 tracking-tight flex items-center gap-3">
        <Users class="w-7 h-7 text-amber-500 stroke-[1.5]" />
        จัดการข้อมูลบัณฑิต <span class="text-sm font-medium text-slate-400 ml-2 hidden sm:inline">(เจ้าหน้าที่ส่วนพัฒฯ)</span>
      </h2>
    </div>
    
    <!-- ส่วนค้นหาข้อมูล และ แสดงจำนวนรายการ -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-white p-4 rounded-xl shadow-sm border border-slate-200">
      
      <!-- Input ค้นหา -->
      <div class="flex flex-1 w-full gap-3 relative">
        <div class="relative w-full max-w-md">
          <Search class="w-5 h-5 text-slate-400 absolute left-4 top-2.5 stroke-[1.5]" />
          <input 
            v-model="searchQuery" 
            @keyup.enter="handleSearch"
            type="text" 
            placeholder="ค้นหา: รหัสนักศึกษา, ชื่อ, หรือ สำนักวิชา..." 
            class="w-full pl-11 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:bg-white focus:ring-2 focus:ring-amber-500/20 focus:border-amber-500 text-slate-700 transition-all outline-none"
          >
        </div>
        <button 
          @click="handleSearch" 
          :disabled="isLoading"
          class="bg-slate-800 text-white px-6 py-2 rounded-lg hover:bg-slate-900 transition-all shadow-sm disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 flex-shrink-0 font-medium"
        >
          <Loader2 v-if="isLoading" class="w-4 h-4 animate-spin stroke-[2]" />
          <Search v-else class="w-4 h-4 stroke-[2]" />
          {{ isLoading ? 'กำลังค้นหา...' : 'ค้นหา' }}
        </button>
      </div>

      <!-- Badge จำนวนรายการ -->
      <div v-if="hasSearched" class="bg-amber-50 border border-amber-200 text-amber-700 px-4 py-2 rounded-lg text-sm font-bold shadow-sm flex items-center gap-2 whitespace-nowrap">
        <UserCheck class="w-4 h-4 stroke-[2]" /> พบข้อมูล {{ totalItems }} รายการ
      </div>
    </div>

    <!-- ตารางแสดงผลข้อมูล -->
    <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
      <div class="overflow-x-auto custom-scrollbar">
        <table class="min-w-full divide-y divide-slate-200">
          <thead class="bg-slate-50">
            <tr>
              <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">รหัสนักศึกษา</th>
              <th class="px-6 py-4 text-center text-xs font-bold text-slate-500 uppercase tracking-wider">ลำดับขึ้นรับ</th>
              <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">ชื่อ - นามสกุล</th>
              <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">สำนักวิชา</th>
              <th class="px-6 py-4 text-center text-xs font-bold text-slate-500 uppercase tracking-wider">สถานะการเข้ารับ</th>
              <th class="px-6 py-4 text-center text-xs font-bold text-slate-500 uppercase tracking-wider">จัดการ</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-slate-100">
            
            <tr v-if="students.length === 0">
              <td colspan="6" class="px-6 py-12 text-center text-slate-400">
                <div class="flex flex-col items-center justify-center gap-3">
                  <component :is="hasSearched ? SearchX : MousePointerClick" class="w-12 h-12 text-slate-300 stroke-[1.5]" />
                  <p class="text-sm font-medium">{{ hasSearched ? 'ไม่พบข้อมูลบัณฑิตที่ค้นหา' : 'กรุณาระบุคำค้นหาเพื่อดึงข้อมูล' }}</p>
                </div>
              </td>
            </tr>

            <tr v-for="student in students" :key="student.id" class="hover:bg-slate-50/80 transition-colors group">
              
              <td class="px-6 py-4 whitespace-nowrap text-sm font-bold text-slate-700">
                {{ student.studentcode }}
              </td>
              
              <td class="px-6 py-4 whitespace-nowrap text-center">
                <span class="inline-flex bg-slate-100 border border-slate-200 text-slate-600 px-3 py-1 rounded-md text-xs font-bold shadow-sm">
                  {{ student.orderno }}
                </span>
              </td>
              
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-slate-600">
                {{ student.prefixname || '' }} {{ student.studentname }} {{ student.studentsurname }}
              </td>
              
              <td class="px-6 py-4 whitespace-nowrap text-xs text-slate-500 truncate max-w-[200px]" :title="student.facultyname">
                {{ student.facultyname }}
              </td>
              
              <!-- Dropdown เลือกสถานะ -->
              <td class="px-6 py-4 whitespace-nowrap text-center relative">
                <div class="relative w-full min-w-[150px] max-w-[200px] mx-auto">
                  <select 
                    v-model="student.current_attendance_status"
                    class="w-full appearance-none bg-slate-50 border border-slate-200 rounded-lg text-sm px-3 py-1.5 focus:outline-none focus:bg-white focus:ring-2 focus:ring-amber-500/20 focus:border-amber-500 font-medium text-slate-600 cursor-pointer transition-all"
                  >
                    <option :value="null" disabled>รอระบุสถานะ...</option>
                    <option 
                      v-for="type in attendanceTypes" 
                      :key="type.type_id" 
                      :value="type.type_id"
                    >
                      {{ type.type_name }}
                    </option>
                  </select>
                  <ChevronDown class="w-4 h-4 text-slate-400 absolute right-2.5 top-2 pointer-events-none stroke-[1.5]" />
                </div>
              </td>
              
              <!-- ปุ่มบันทึก -->
              <td class="px-6 py-4 whitespace-nowrap text-center text-sm">
                <button 
                  @click="saveAttendance(student)"
                  class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-white border border-emerald-500 text-emerald-600 hover:bg-emerald-50 hover:text-emerald-700 rounded-lg text-xs font-bold shadow-sm transition-all opacity-70 group-hover:opacity-100"
                >
                  <Save class="w-3.5 h-3.5 stroke-[2]" /> บันทึก
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- แจ้งเตือนสถานะมุมขวาล่าง (Toast) -->
    <div v-if="toastMessage" class="fixed bottom-6 right-6 bg-slate-800 text-white px-5 py-3 rounded-xl shadow-xl border border-slate-700 flex items-center gap-3 animate-fade-in-up z-50">
      <CheckCircle2 class="w-5 h-5 text-emerald-400 stroke-[2]" />
      <span class="text-sm font-medium">{{ toastMessage }}</span>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../services/api';
// 💡 Import ไอคอน Lucide 
import { 
  Users, Search, Loader2, UserCheck, 
  SearchX, MousePointerClick, ChevronDown, 
  Save, CheckCircle2 
} from 'lucide-vue-next';

const searchQuery = ref('');
const students = ref([]);
const attendanceTypes = ref([]);
const isLoading = ref(false);
const hasSearched = ref(false);
const toastMessage = ref('');

// ตัวแปรสำหรับ Pagination
const currentPage = ref(1);
const totalPages = ref(1);
const totalItems = ref(0);
const pageSize = 20;

// โหลดตัวเลือกสถานะตอนเปิดหน้าเว็บ
onMounted(async () => {
  try {
    const response = await api.get('/students/attendance-types');
    attendanceTypes.value = response.data;
  } catch (error) {
    console.error('Error fetching attendance types:', error);
  }
});

const showToast = (msg) => {
  toastMessage.value = msg;
  setTimeout(() => {
    toastMessage.value = '';
  }, 3000);
};

const handleSearch = () => {
  if (!searchQuery.value.trim()) return; 
  currentPage.value = 1;
  fetchData();
};

const changePage = (pageNumber) => {
  if (pageNumber >= 1 && pageNumber <= totalPages.value) {
    currentPage.value = pageNumber;
    fetchData();
  }
};

const fetchData = async () => {
  isLoading.value = true;
  hasSearched.value = true;
  
  try {
    const response = await api.get('/students/search', {
      params: {
        q: searchQuery.value,
        page: currentPage.value,
        limit: pageSize
      }
    });
    
    totalItems.value = response.data.total_items;
    totalPages.value = response.data.total_pages;
    
    students.value = response.data.data.map(std => ({
      ...std,
      current_attendance_status: std.graduation_info ? std.graduation_info.is_attending : null
    }));

  } catch (error) {
    console.error('Error fetching students:', error);
    showToast('เกิดข้อผิดพลาดในการดึงข้อมูล');
  } finally {
    isLoading.value = false;
  }
};

const saveAttendance = async (student) => {
  if (student.current_attendance_status === null) {
    showToast('กรุณาเลือกสถานะก่อนบันทึก');
    return;
  }

  try {
    await api.put(`/students/${student.id}/attendance`, null, {
      params: { is_attending: student.current_attendance_status }
    });
    showToast(`อัปเดตสถานะของ ${student.studentname} สำเร็จแล้ว`);
  } catch (error) {
    console.error('Error updating attendance:', error);
    showToast('เกิดข้อผิดพลาดในการบันทึกข้อมูล');
  }
};
</script>

<style scoped>
/* แต่ง Scrollbar ของตารางให้แนวนอนเลื่อนได้สมูทและสวยงาม */
.custom-scrollbar::-webkit-scrollbar {
  height: 6px;
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

/* เอฟเฟกต์เด้งป๊อปอัป Toast */
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in-up {
  animation: fadeInUp 0.3s ease-out forwards;
}
</style>