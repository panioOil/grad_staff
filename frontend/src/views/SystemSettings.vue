<template>
  <div class="p-4 md:p-4 max-w-7xl mx-auto space-y-4 pb-10">
    <!-- Header -->
    <div class="flex items-center justify-between pb-2 border-b border-slate-200">
      <h2 class="text-xl md:text-2xl font-bold text-slate-800 tracking-tight flex items-center gap-3">
        <Settings class="w-7 h-7 text-amber-500 stroke-[1.5]" />
        ตั้งค่าระบบ <span class="text-sm font-medium text-slate-400 ml-2 hidden sm:inline">(System Settings)</span>
      </h2>
    </div>

    <div class="grid grid-cols-1 xl:grid-cols-2 gap-6">
      
      <!-- ส่วนที่ 1: ตั้งค่าการลงทะเบียน -->
      <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-5 md:p-6 h-fit">
        <h3 class="text-lg font-bold text-slate-800 mb-5 border-b border-slate-100 pb-4 flex items-center gap-2">
          <CalendarDays class="w-5 h-5 text-amber-500 stroke-[1.5]" /> ตั้งค่าการลงทะเบียน
        </h3>
        
        <form @submit.prevent="saveGeneralSettings" class="space-y-5">
          <div class="relative">
            <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">ปีการศึกษา (แสดงบนหน้าเว็บ)</label>
            <input v-model="settings.academic_year" type="text" class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-amber-500/20 focus:border-amber-500 text-slate-700 text-sm transition-all outline-none" placeholder="เช่น 2567">
          </div>
          
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
            <div class="relative">
              <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">เปิดรับลงทะเบียน</label>
              <input v-model="settings.reg_start_date" type="datetime-local" class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-amber-500/20 focus:border-amber-500 text-slate-700 text-sm transition-all outline-none">
            </div>
            <div class="relative">
              <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">ปิดรับลงทะเบียน</label>
              <input v-model="settings.reg_end_date" type="datetime-local" class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-amber-500/20 focus:border-amber-500 text-slate-700 text-sm transition-all outline-none">
            </div>
          </div>
          
          <div class="relative">
            <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">ข้อความประกาศ (Announcement)</label>
            <textarea v-model="settings.announcement" rows="3" class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-amber-500/20 focus:border-amber-500 text-slate-700 text-sm transition-all outline-none custom-scrollbar" placeholder="เช่น โปรดแต่งกายสุภาพ..."></textarea>
          </div>
          
          <button type="submit" class="w-full bg-slate-800 text-white font-bold py-3 rounded-xl hover:bg-slate-900 shadow-sm transition-all flex items-center justify-center gap-2">
            <Save class="w-4 h-4 stroke-[2]" /> บันทึกการตั้งค่า
          </button>
        </form>
      </div>

      <!-- ส่วนที่ 2: จัดการรอบการซ้อม -->
      <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-5 md:p-6 flex flex-col h-fit">
        <h3 class="text-lg font-bold text-slate-800 mb-5 border-b border-slate-100 pb-4 flex items-center gap-2">
          <MapPin class="w-5 h-5 text-amber-500 stroke-[1.5]" /> จัดการรอบการฝึกซ้อม
        </h3>
        
        <!-- ฟอร์มเพิ่มรอบซ้อม -->
        <div class="flex flex-col sm:flex-row gap-3 mb-5">
          <input v-model="newScheduleName" type="text" placeholder="ชื่อรอบ เช่น ซ้อมย่อย 1" class="flex-1 px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-amber-500/20 focus:border-amber-500 text-slate-700 text-sm transition-all outline-none">
          <button @click="addSchedule" class="bg-emerald-600 text-white px-5 py-2.5 rounded-xl text-sm font-bold hover:bg-emerald-700 shadow-sm transition-all flex items-center justify-center gap-2 flex-shrink-0">
            <Plus class="w-4 h-4 stroke-[2]" /> เพิ่มรอบ
          </button>
        </div>

        <!-- รายการรอบซ้อม -->
        <div class="flex-1 overflow-hidden border border-slate-200 rounded-xl shadow-sm">
          <div class="overflow-x-auto max-h-[280px] custom-scrollbar">
            <table class="w-full border-collapse">
              <thead>
                <tr class="bg-slate-100">
                  <th class="py-3 px-3 text-left text-sm font-medium text-slate-500">ชื่อรอบ</th>
                  <th class="py-3 px-3 text-left text-sm font-medium text-slate-500">วันที่</th>
                  <th class="py-3 px-3 text-left text-sm font-medium text-slate-500">สถานะ</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="sched in schedules" :key="sched.id" class="border-b">
                  <td class="py-3 px-3">
                    <!-- [แสดงผลปกติ: ชื่อรอบ และ วันที่] -->
                    <div v-if="editingId !== sched.id" class="flex flex-col">
                      <span class="font-medium text-slate-700">{{ sched.event_name }}</span>
                      <span class="text-xs text-slate-400" v-if="sched.event_date">📅 วันที่: {{ formatDate(sched.event_date) }}</span>
                    </div>

                    <!-- [ช่องสำหรับแก้ไข: ชื่อรอบ และ วันที่] -->
                    <div v-else class="space-y-2 py-1">
                      <input 
                        v-model="editingName" 
                        type="text" 
                        class="border border-emerald-300 rounded-lg px-3 py-1.5 w-full focus:ring-2 focus:ring-emerald-200 focus:outline-none text-sm text-slate-700 bg-emerald-50/30"
                        placeholder="ชื่อรอบ..."
                      />
                      <input 
                        v-model="editingDate" 
                        type="date" 
                        class="border border-emerald-300 rounded-lg px-3 py-1 w-full focus:ring-2 focus:ring-emerald-200 focus:outline-none text-xs text-slate-700 bg-emerald-50/30"
                      />
                    </div>
                  </td>
                  <!-- คอลัมน์สถานะ -->
                  <td class="py-3">
                    <button 
                      @click="toggleActive(sched.id)"
                      :class="sched.is_active 
                        ? 'bg-emerald-50 text-emerald-600 border border-emerald-300 shadow-sm' 
                        : 'bg-slate-50 text-slate-500 border border-slate-200'"
                      class="px-4 py-1.5 rounded-full text-xs font-semibold flex items-center gap-1.5 transition-all mx-auto"
                    >
                      <!-- ไอคอน Power ตามดีไซน์เดิม -->
                      <span class="text-base leading-none">⏻</span>
                      <span>{{ sched.is_active ? 'เปิดใช้งานอยู่' : 'ปิด' }}</span>
                    </button>
                  </td>
                  
                  <!-- คอลัมน์จัดการ -->
                  <td class="py-3 text-center flex justify-center items-center gap-1.5">
                    <template v-if="editingId !== sched.id">
                      <button 
                        @click="startEdit(sched)" 
                        class="text-blue-500 hover:text-blue-700 p-1.5 bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors"
                        title="แก้ไข"
                      >
                        ✏️
                      </button>
                    </template>
                    <template v-else>
                      <button 
                        @click="saveEdit(sched.id)" 
                        class="text-green-600 hover:text-green-800 px-2.5 py-1 bg-green-100 hover:bg-green-200 rounded-lg transition-colors text-xs font-bold"
                        title="บันทึก"
                      >
                        บันทึก
                      </button>
                      <button 
                        @click="cancelEdit" 
                        class="text-slate-500 hover:text-slate-700 px-2 py-1 bg-slate-100 hover:bg-slate-200 rounded-lg transition-colors text-xs"
                        title="ยกเลิก"
                      >
                        ยกเลิก
                      </button>
                    </template>

                    <button 
                      @click="deleteSchedule(sched.id)" 
                      class="text-red-500 hover:text-red-700 p-1.5 bg-red-50 hover:bg-red-100 rounded-lg transition-colors"
                      title="ลบ"
                    >
                      🗑️
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <p class="text-xs text-rose-500 mt-4 font-medium flex items-center gap-1.5">
          <AlertCircle class="w-4 h-4 stroke-[2]" /> *ระบบอนุญาตให้เปิด (Active) ได้ทีละ 1 รอบเท่านั้น เพื่อป้องกันความสับสน
        </p>
      </div>

      <!-- ส่วนที่ 3: ตั้งค่าข้อความหน้า Login (บัณฑิต) -->
      <div class="xl:col-span-2 bg-white rounded-2xl shadow-sm border border-slate-200 p-5 md:p-6 mt-2">
        <h3 class="text-lg font-bold text-slate-800 mb-6 border-b border-slate-100 pb-4 flex items-center gap-2">
          <LayoutTemplate class="w-5 h-5 text-amber-500 stroke-[1.5]" /> จัดการข้อความหน้า Login <span class="text-sm font-medium text-slate-400 ml-1">(สำหรับบัณฑิต)</span>
        </h3>
        
        <form @submit.prevent="saveLoginSettings" class="space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-5 bg-slate-50/50 p-5 rounded-2xl border border-slate-100">
            <div class="relative">
              <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">ชื่อระบบ (ภาษาไทย)</label>
              <input v-model="loginSettings.login_title_th" type="text" class="w-full px-4 py-2.5 bg-white border border-slate-200 rounded-xl focus:ring-2 focus:ring-amber-500/20 focus:border-amber-500 text-slate-700 text-sm transition-all outline-none" placeholder="เช่น ระบบแจ้งความประสงค์การเข้ารับปริญญาบัตร">
            </div>
            <div class="relative">
              <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">ชื่อระบบ (ภาษาอังกฤษ)</label>
              <input v-model="loginSettings.login_title_en" type="text" class="w-full px-4 py-2.5 bg-white border border-slate-200 rounded-xl focus:ring-2 focus:ring-amber-500/20 focus:border-amber-500 text-slate-700 text-sm transition-all outline-none" placeholder="เช่น Commencement Ceremony Registration System">
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-5 bg-slate-50/50 p-5 rounded-2xl border border-slate-100">
            <div class="relative">
              <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">ข้อความปีการศึกษา (ภาษาไทย)</label>
              <input v-model="loginSettings.login_year_th" type="text" class="w-full px-4 py-2.5 bg-white border border-slate-200 rounded-xl focus:ring-2 focus:ring-amber-500/20 focus:border-amber-500 text-slate-700 text-sm transition-all outline-none" placeholder="เช่น สำหรับรุ่นปีการศึกษา 2567">
            </div>
            <div class="relative">
              <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">ข้อความปีการศึกษา (ภาษาอังกฤษ)</label>
              <input v-model="loginSettings.login_year_en" type="text" class="w-full px-4 py-2.5 bg-white border border-slate-200 rounded-xl focus:ring-2 focus:ring-amber-500/20 focus:border-amber-500 text-slate-700 text-sm transition-all outline-none" placeholder="เช่น Academic Year 2024">
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-5 bg-slate-50/50 p-5 rounded-2xl border border-slate-100">
            <div class="relative">
              <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">วันที่รับลงทะเบียน (ภาษาไทย)</label>
              <input v-model="loginSettings.login_date_th" type="text" class="w-full px-4 py-2.5 bg-white border border-slate-200 rounded-xl focus:ring-2 focus:ring-amber-500/20 focus:border-amber-500 text-slate-700 text-sm transition-all outline-none" placeholder="เช่น แจ้งความประสงค์การเข้ารับปริญญา ตั้งแต่วันที่ 6 ม.ค. - 20 ก.พ. 2569">
            </div>
            <div class="relative">
              <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">วันที่รับลงทะเบียน (ภาษาอังกฤษ)</label>
              <input v-model="loginSettings.login_date_en" type="text" class="w-full px-4 py-2.5 bg-white border border-slate-200 rounded-xl focus:ring-2 focus:ring-amber-500/20 focus:border-amber-500 text-slate-700 text-sm transition-all outline-none" placeholder="เช่น During 6 January - 20 February 2026">
            </div>
          </div>

          <div class="bg-slate-50/50 p-5 rounded-2xl border border-slate-100 relative">
            <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">ข้อความส่วนท้าย (Footer แถบด้านล่างสุด)</label>
            <input v-model="loginSettings.login_footer" type="text" class="w-full px-4 py-2.5 bg-white border border-slate-200 rounded-xl focus:ring-2 focus:ring-amber-500/20 focus:border-amber-500 text-slate-700 text-sm transition-all outline-none" placeholder="เช่น พิธีพระราชทานปริญญาบัตร มหาวิทยาลัยแม่ฟ้าหลวง ประจำปีการศึกษา 2567...">
          </div>

          <div class="bg-amber-50/50 p-5 rounded-2xl border border-amber-100/60 relative">
            <label class="block text-xs font-bold text-amber-700 uppercase tracking-wider mb-2 flex items-center gap-1.5">
              <Megaphone class="w-4 h-4 stroke-[2]" /> ข้อความประกาศ (แสดงเหนือกล่องเข้าสู่ระบบ)
            </label>
            <textarea v-model="loginSettings.login_announcement" rows="3" class="w-full px-4 py-3 bg-white border border-amber-200/60 rounded-xl focus:ring-2 focus:ring-amber-500/20 focus:border-amber-500 text-slate-700 text-sm transition-all outline-none custom-scrollbar" placeholder="เช่น ระบบจะปิดปรับปรุงในวันที่..."></textarea>
            <p class="text-xs font-medium text-amber-600/70 mt-2">* หากเว้นว่างไว้ จะไม่มีกล่องประกาศแสดงในหน้า Login</p>
          </div>

          <div class="flex justify-end pt-2">
            <button type="submit" class="w-full sm:w-auto bg-slate-800 text-white font-bold py-3 px-8 rounded-xl hover:bg-slate-900 shadow-sm transition-all flex items-center justify-center gap-2">
              <Save class="w-4 h-4 stroke-[2]" /> บันทึกข้อความหน้า Login
            </button>
          </div>
        </form>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../services/api';
import Swal from 'sweetalert2';
import { 
  Settings, CalendarDays, Save, MapPin, 
  Plus, AlertCircle, 
  LayoutTemplate, Megaphone 
} from 'lucide-vue-next';

// State สำหรับส่วนที่ 1
const settings = ref({
  academic_year: '',
  reg_start_date: '',
  reg_end_date: '',
  announcement: ''
});

// State สำหรับส่วนที่ 2 (จัดการรอบการฝึกซ้อม)
const schedules = ref([]);
const newScheduleName = ref('');
const editingId = ref(null);
const editingName = ref('');
const editingDate = ref('');

onMounted(async () => {
  await fetchSettings();
  await fetchSchedules();
  await fetchLoginSettings(); 
});

// เพิ่มฟังก์ชัน formatDate นี้เข้าไปใน <script setup> ของคุณ
const formatDate = (dateString) => {
  if (!dateString) return '-'; 
  
  const d = new Date(dateString);
  if (isNaN(d.getTime())) return dateString; // ถ้าแปลงเป็นวันที่ไม่ได้ ให้แสดงค่าเดิมตาม string

  const day = String(d.getDate()).padStart(2, '0');
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const year = d.getFullYear() + 543; // แปลงเป็นปี พ.ศ.

  return `${day}/${month}/${year}`;
};

const fetchSettings = async () => {
  try {
    const res = await api.get('/settings/general');
    if (res.data) {
      settings.value = { ...settings.value, ...res.data };
    }
  } catch (error) {
    console.error(error);
  }
};

const saveGeneralSettings = async () => {
  try {
    await api.post('/settings/general', settings.value);
    Swal.fire({ 
      icon: 'success', 
      title: 'บันทึกสำเร็จ', 
      showConfirmButton: false, 
      timer: 1500,
      customClass: { popup: 'rounded-2xl' }
    });
  } catch (error) {
    Swal.fire({
      icon: 'error',
      title: 'ผิดพลาด',
      text: 'เกิดข้อผิดพลาดในการบันทึก',
      confirmButtonColor: '#f43f5e',
      customClass: { popup: 'rounded-2xl', confirmButton: 'rounded-lg px-6' }
    });
  }
};

const fetchSchedules = async () => {
  try {
    const res = await api.get('/settings/schedules');
    schedules.value = res.data;
  } catch (error) {
    console.error(error);
  }
};

const addSchedule = async () => {
  if (!newScheduleName.value) return;
  try {
    await api.post('/settings/schedules', { event_name: newScheduleName.value });
    newScheduleName.value = '';
    await fetchSchedules(); 
  } catch (error) {
    console.error(error);
  }
};

// ฟังก์ชันสำหรับกดสลับสถานะ เปิด/ปิด
const toggleActive = async (id) => {
  try {
    await api.put(`/settings/schedules/${id}/toggle`);
    await fetchSchedules(); // โหลดข้อมูลใหม่เพื่อให้หน้าจออัปเดตสถานะทันที
  } catch (error) {
    console.error("Failed to toggle status:", error);
  }
};

const deleteSchedule = async (id) => {
  Swal.fire({
    title: 'ยืนยันการลบรอบนี้?',
    text: "ประวัติการเช็คชื่อของรอบนี้จะหายไปด้วย!",
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#f43f5e',
    cancelButtonColor: '#64748b',
    confirmButtonText: 'ยืนยันลบ',
    cancelButtonText: 'ยกเลิก',
    customClass: { popup: 'rounded-2xl', confirmButton: 'rounded-lg px-6', cancelButton: 'rounded-lg px-6' }
  }).then(async (result) => {
    if (result.isConfirmed) {
      try {
        await api.delete(`/settings/schedules/${id}`);
        await fetchSchedules();
        Swal.fire({ 
          icon: 'success', 
          title: 'ลบสำเร็จ', 
          showConfirmButton: false, 
          timer: 1500,
          customClass: { popup: 'rounded-2xl' }
        });
      } catch (error) {
        console.error(error);
      }
    }
  });
};

// ----------------------------------------
// ฟังก์ชันสำหรับการแก้ไขชื่อรอบการซ้อม
// ----------------------------------------
const startEdit = (sched) => {
  editingId.value = sched.id;
  editingName.value = sched.event_name;
  editingDate.value = sched.event_date ? sched.event_date.split('T')[0] : ''; // ดึงค่าวันที่มาใส่ (ตัดเวลาออกให้เหลือ YYYY-MM-DD สำหรับ input type="date")
};

const cancelEdit = () => {
  editingId.value = null;
  editingName.value = '';
  editingDate.value = '';
};

const saveEdit = async (id) => {
  if (!editingName.value.trim()) return;
  try {
    // ส่งทั้ง event_name และ event_date ไปที่ Backend
    await api.put(`/settings/schedules/${id}`, { 
      event_name: editingName.value,
      event_date: editingDate.value || null 
    });
    
    // อัปเดตข้อมูลฝั่ง Frontend ทันที
    const target = schedules.value.find(r => r.id === id);
    if (target) {
      target.event_name = editingName.value;
      target.event_date = editingDate.value;
    }
    
    editingId.value = null;
    editingName.value = '';
    editingDate.value = '';

    Swal.fire({ 
      icon: 'success', 
      title: 'แก้ไขสำเร็จ', 
      showConfirmButton: false, 
      timer: 1200,
      customClass: { popup: 'rounded-2xl' }
    });
  } catch (error) {
    console.error("Failed to update schedule:", error);
    Swal.fire({
      icon: 'error',
      title: 'ผิดพลาด',
      text: 'ไม่สามารถบันทึกการแก้ไขได้',
      confirmButtonColor: '#f43f5e'
    });
  }
};

const loginSettings = ref({
  login_title_th: '',
  login_title_en: '',
  login_year_th: '',
  login_year_en: '',
  login_date_th: '',
  login_date_en: '',
  login_footer: '',
  login_announcement: ''
});

const fetchLoginSettings = async () => {
  try {
    const res = await api.get('/settings/login-page');
    if (res.data) {
      loginSettings.value = { ...loginSettings.value, ...res.data };
    }
  } catch (error) {
    console.error(error);
  }
};

const saveLoginSettings = async () => {
  try {
    await api.post('/settings/login-page', loginSettings.value);
    Swal.fire({ 
      icon: 'success', 
      title: 'บันทึกสำเร็จ', 
      showConfirmButton: false, 
      timer: 1500,
      customClass: { popup: 'rounded-2xl' }
    });
  } catch (error) {
    Swal.fire({
      icon: 'error',
      title: 'ผิดพลาด',
      text: 'เกิดข้อผิดพลาดในการบันทึก',
      confirmButtonColor: '#f43f5e',
      customClass: { popup: 'rounded-2xl', confirmButton: 'rounded-lg px-6' }
    });
  }
};
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
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
</style>