<template>
  <div class="bg-slate-50 min-h-screen flex flex-col pb-20">
    
    <!-- ส่วนหัว: แสดงรอบที่กำลังเช็คชื่อ และเลือกจุดสแกน -->
    <header class="bg-white px-4 md:px-6 py-4 shadow-sm border-b border-slate-200 sticky top-0 z-20 flex justify-between items-center">
      <div class="flex items-center gap-3">
        <div class="bg-amber-100 p-2 rounded-lg hidden sm:block">
          <ScanLine class="w-5 h-5 text-amber-600 stroke-[1.5]" />
        </div>
        <div>
          <h2 class="text-lg md:text-xl font-bold text-slate-800 tracking-tight">จุดเช็คชื่อบัณฑิต</h2>
          <!-- Dropdown เลือกจุดเช็คชื่อ -->
          <div class="mt-1 flex items-center gap-2">
            <MapPin class="w-3.5 h-3.5 text-slate-400 stroke-[1.5]" />
            <select v-model="selectedPoint" class="bg-slate-50 border border-slate-200 text-slate-600 text-xs font-semibold rounded-md focus:ring-amber-500 focus:border-amber-500 block px-2 py-1 outline-none transition-colors cursor-pointer">
              <option value="1">จุดที่ 1 (หน้า C4)</option>
              <option value="2">จุดที่ 2 (หน้า C5)</option>
            </select>
          </div>
        </div>
      </div>
      
      <!-- ป้ายสถานะออนไลน์ -->
      <span class="bg-emerald-50 border border-emerald-200 text-emerald-600 text-[10px] font-bold uppercase tracking-wider px-2.5 py-1.5 rounded-full flex items-center shadow-sm h-fit">
        <Radio class="w-3 h-3 mr-1.5 text-emerald-500 animate-pulse stroke-[2]" /> ออนไลน์
      </span>
    </header>

    <!-- เมนูสลับโหมด (Tabs) -->
    <div class="bg-white border-b border-slate-200 flex overflow-x-auto custom-scrollbar shadow-sm z-10">
      <button 
        v-for="tab in scanModes" :key="tab.id"
        @click="switchMode(tab.id)"
        :class="[
          'flex-1 py-3.5 text-sm font-semibold whitespace-nowrap px-4 border-b-[3px] transition-all duration-300 flex items-center justify-center gap-2',
          currentMode === tab.id ? 'border-amber-500 text-amber-600 bg-amber-50/50' : 'border-transparent text-slate-500 hover:text-slate-700 hover:bg-slate-50'
        ]"
      >
        <component :is="tab.icon" class="w-4 h-4 stroke-[1.5]" :class="currentMode === tab.id ? 'stroke-[2]' : ''" />
        {{ tab.name }}
      </button>
    </div>

    <!-- พื้นที่แสดงผล -->
    <div class="p-4 md:p-6 flex-1 flex flex-col items-center">
      
      <!-- โหมดเปิดกล้อง (QR / Barcode / Face) -->
      <div v-show="currentMode !== 'manual'" class="w-full max-w-md bg-slate-900 rounded-2xl overflow-hidden shadow-lg relative aspect-[4/3] flex items-center justify-center ring-4 ring-white border border-slate-200">
        
        <!-- ตัวกล้องจะมาแสดงใน div นี้ -->
        <div id="reader" class="w-full h-full object-cover"></div>
        
        <!-- กรอบเป้าหมาย (UI overlay) -->
        <div v-if="isScanning" class="absolute inset-0 pointer-events-none">
          <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-48 h-48 border border-emerald-500/50 rounded-xl">
             <div class="absolute top-0 left-0 w-5 h-5 border-t-[3px] border-l-[3px] border-emerald-400 rounded-tl-lg -mt-[1px] -ml-[1px]"></div>
             <div class="absolute top-0 right-0 w-5 h-5 border-t-[3px] border-r-[3px] border-emerald-400 rounded-tr-lg -mt-[1px] -mr-[1px]"></div>
             <div class="absolute bottom-0 left-0 w-5 h-5 border-b-[3px] border-l-[3px] border-emerald-400 rounded-bl-lg -mb-[1px] -ml-[1px]"></div>
             <div class="absolute bottom-0 right-0 w-5 h-5 border-b-[3px] border-r-[3px] border-emerald-400 rounded-br-lg -mb-[1px] -mr-[1px]"></div>
          </div>
          <!-- เส้นสแกนวิ่งขึ้นลง -->
          <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-44 h-[2px] bg-emerald-400 shadow-[0_0_12px_#34d399] animate-scan"></div>
        </div>

        <!-- หน้าจอ Loading กล้อง -->
        <div v-if="!isScanning" class="absolute inset-0 flex flex-col items-center justify-center bg-slate-900/95 z-10 text-slate-300 backdrop-blur-sm">
          <Loader2 class="w-8 h-8 mb-3 animate-spin text-amber-500 stroke-[1.5]" />
          <p class="text-sm font-medium tracking-wide">กำลังเตรียมกล้อง...</p>
        </div>
      </div>

      <!-- โหมด Manual (คีย์รหัส) -->
      <div v-show="currentMode === 'manual'" class="w-full max-w-md bg-white p-6 rounded-2xl shadow-sm border border-slate-200 mt-2">
        <label class="block text-sm font-semibold text-slate-700 mb-2">ป้อนรหัสนักศึกษา (10 หลัก)</label>
        <div class="flex gap-2">
          <input 
            v-model="manualStudentCode" 
            @keyup.enter="processScannedCode(manualStudentCode)"
            type="number" 
            placeholder="เช่น 6652803xxx" 
            class="w-full bg-slate-50 border border-slate-200 px-4 py-2.5 rounded-xl focus:ring-2 focus:ring-amber-500/20 focus:border-amber-500 focus:bg-white text-slate-800 transition-all outline-none"
          >
          <button @click="processScannedCode(manualStudentCode)" class="bg-slate-800 hover:bg-slate-900 text-white px-5 py-2.5 rounded-xl font-semibold shadow-sm transition-all flex items-center gap-1.5 flex-shrink-0">
            <CheckCircle2 class="w-4 h-4 stroke-[2]" /> ตกลง
          </button>
        </div>
      </div>

      <!-- Popup Card ผลลัพธ์การสแกน (สำเร็จ) -->
      <div v-if="lastScannedStudent" class="mt-6 w-full max-w-md bg-white rounded-2xl shadow-lg border border-slate-100 overflow-hidden relative group animate-fade-in-up">
        <!-- แถบสีเขียวซ้ายมือ -->
        <div class="absolute left-0 top-0 bottom-0 w-1.5 bg-emerald-500"></div>
        
        <div class="p-5 pl-6 flex gap-4">
          <!-- รูปใบหน้า -->
          <div class="w-20 h-28 bg-slate-50 rounded-lg flex-shrink-0 border border-slate-200 object-cover overflow-hidden relative shadow-sm">
            <img v-if="lastScannedStudent.face_image_url" :src="lastScannedStudent.face_image_url" class="w-full h-full object-cover">
            <div v-else class="w-full h-full flex flex-col items-center justify-center text-slate-400 bg-slate-100/50">
              <UserX class="w-6 h-6 mb-1 stroke-[1.5]" />
              <span class="text-[9px] font-bold uppercase tracking-wider">ไม่มีรูป</span>
            </div>
          </div>
          
          <div class="flex-1 flex flex-col justify-center min-w-0">
            <div class="flex justify-between items-center mb-1.5">
              <span class="bg-emerald-50 border border-emerald-100 text-emerald-600 text-[10px] px-2 py-0.5 rounded-md font-bold uppercase tracking-wide flex items-center shadow-sm">
                <CheckCircle2 class="w-3 h-3 mr-1 stroke-[2]" /> บันทึกแล้ว
              </span>
              <span class="text-[11px] font-medium text-slate-400 flex items-center gap-1">
                <Clock class="w-3 h-3 stroke-[1.5]" /> {{ lastScannedStudent.time }}
              </span>
            </div>
            <h4 class="text-lg font-bold text-slate-800 leading-tight truncate">{{ lastScannedStudent.name }}</h4>
            <p class="text-xs font-semibold text-slate-500 mt-1">รหัส: <span class="text-slate-700">{{ lastScannedStudent.code }}</span></p>
            <p class="text-[11px] text-slate-400 mt-1 truncate">{{ lastScannedStudent.faculty }}</p>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue';
import { Html5Qrcode } from 'html5-qrcode';
import api from '../services/api';
import Swal from 'sweetalert2';

// 💡 Import ไอคอน Lucide แบบ Dynamic
import { 
  ScanLine, MapPin, Radio, Camera, 
  QrCode, Barcode, Keyboard, CheckCircle2, 
  UserX, Clock, Loader2 
} from 'lucide-vue-next';

// State
const currentMode = ref('qr');
const isScanning = ref(false);
const manualStudentCode = ref('');
const lastScannedStudent = ref(null);
const selectedPoint = ref('1');

// 💡 เปลี่ยนจาก Emoji เป็น Object ของ Icon แทน เพื่อให้เข้ากับ <component :is="...">
const scanModes = [
  { id: 'face', name: 'สแกนหน้า', icon: Camera },
  { id: 'qr', name: 'QR Code', icon: QrCode },
  { id: 'barcode', name: 'Barcode', icon: Barcode },
  { id: 'manual', name: 'คีย์รหัส', icon: Keyboard }
];

// ตัวแปรเก็บ Instance ของกล้อง
let html5QrCode = null;
let isProcessing = false;

// -----------------------------------------
// ฟังก์ชันจัดการกล้อง
// -----------------------------------------
const startCamera = async () => {
  if (currentMode.value === 'manual') return;

  await nextTick();

  if (html5QrCode && html5QrCode.isScanning) {
    isScanning.value = true;
    return;
  }

  if (html5QrCode) {
    try { html5QrCode.clear(); } catch (e) {}
    html5QrCode = null;
  }

  isScanning.value = false;
  html5QrCode = new Html5Qrcode("reader");

  try {
    await html5QrCode.start(
      { facingMode: "environment" },
      {
        fps: 10,
        qrbox: { width: 250, height: 250 },
        aspectRatio: 1.333334
      },
      onScanSuccess,
      onScanFailure
    );
    isScanning.value = true;
  } catch (err) {
    console.error("เริ่มกล้องไม่สำเร็จ:", err);
  }
};

const stopCamera = async () => {
  if (html5QrCode) {
    try {
      if (html5QrCode.isScanning) {
        await html5QrCode.stop();
      }
      html5QrCode.clear();
    } catch (err) {
      console.error("ปิดกล้องไม่สำเร็จ:", err);
    } finally {
      html5QrCode = null;
      isScanning.value = false;
    }
  }
};

const switchMode = async (modeId) => {
  lastScannedStudent.value = null; 

  if (modeId === 'manual') {
    await stopCamera();
    currentMode.value = modeId;
  } else {
    currentMode.value = modeId;
    await startCamera();
  }
};

const onScanSuccess = (decodedText, decodedResult) => {
  if (isProcessing) return;
  isProcessing = true;
  
  processScannedCode(decodedText);

  setTimeout(() => {
    isProcessing = false;
  }, 2000);
};

const onScanFailure = (error) => {
  // ไม่ต้อง alert
};

// -----------------------------------------
// ฟังก์ชันส่งรหัสเข้าระบบ (SweetAlert2)
// -----------------------------------------
const processScannedCode = async (code) => {
  if (!code) return;
  
  const cleanCode = code.toString().trim();

  try {
    const response = await api.post('/attendance/checkin', {
      student_code: cleanCode,
      scan_method: currentMode.value,
      checkin_point: selectedPoint.value
    });
    console.log('API Response:', response.data);
    const data = response.data;

    if (data.success) {
      const audio = new Audio('https://www.soundjay.com/buttons_c2026/sounds/button-35.mp3');
      audio.play().catch(e => console.log('บราวเซอร์บล็อกเสียง'));

      lastScannedStudent.value = data.student;

      if (data.is_duplicate) {
         Swal.fire({
           toast: true,
           position: 'top-end',
           icon: 'warning',
           title: 'เช็คชื่อรอบนี้ไปแล้ว',
           showConfirmButton: false,
           timer: 2000,
           timerProgressBar: true
         });
      }
    }
  } catch (error) {
    const errorAudio = new Audio('https://www.soundjay.com/buttons_c2026/sounds/button-09a.mp3');
    errorAudio.play().catch(e => console.log('บราวเซอร์บล็อกเสียง'));

    let errorMsg = "ไม่สามารถเชื่อมต่อเซิร์ฟเวอร์ได้";
    const detail = error.response?.data?.detail;
    
    if (detail) {
      if (typeof detail === 'string') {
        errorMsg = detail;
      } else if (Array.isArray(detail)) {
        errorMsg = `ข้อมูลผิดพลาด: ${detail[0].loc.join(' -> ')} (${detail[0].msg})`;
      } else {
        errorMsg = JSON.stringify(detail);
      }
    } else if (error.message) {
      errorMsg = error.message;
    }
    
    Swal.fire({
      icon: 'error',
      title: 'ปฏิเสธการเช็คชื่อ',
      text: errorMsg,
      confirmButtonColor: '#f43f5e', // ปรับโทนสีแดงให้เป็น Rose ของ Tailwind
      confirmButtonText: 'ตกลง',
      customClass: {
        popup: 'rounded-2xl',
        confirmButton: 'rounded-lg font-bold text-lg px-6'
      }
    });
    
    lastScannedStudent.value = null; 
  } finally {
    manualStudentCode.value = ''; 
  }
};

onMounted(() => {
  startCamera();
});

onBeforeUnmount(async () => {
  await stopCamera();
});
</script>

<style scoped>
/* Animation สำหรับเส้นสีเขียววิ่งขึ้นลงเวลาสแกน */
@keyframes scan {
  0% { top: 15%; opacity: 0; }
  20% { opacity: 1; }
  80% { opacity: 1; }
  100% { top: 85%; opacity: 0; }
}
.animate-scan {
  animation: scan 2.5s cubic-bezier(0.4, 0, 0.2, 1) infinite;
}

/* เอฟเฟกต์เด้งป๊อปอัปขึ้นมา */
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(15px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in-up {
  animation: fadeInUp 0.4s ease-out forwards;
}

/* Scrollbar สำหรับ Tabs บนมือถือ */
.custom-scrollbar::-webkit-scrollbar {
  height: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #e2e8f0;
  border-radius: 10px;
}

/* ปรับแต่งส่วนกล้องของ Library */
:deep(#reader video) {
  object-fit: cover !important;
  width: 100% !important;
  height: 100% !important;
}
:deep(#reader) {
  border: none !important;
}
</style>