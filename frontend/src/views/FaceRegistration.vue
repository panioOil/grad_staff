<template>
  <div class="p-4 md:p-6 max-w-5xl mx-auto space-y-6 pb-10">
    
    <!-- Header -->
    <div class="flex items-center justify-between pb-2 border-b border-slate-200">
      <h2 class="text-xl md:text-2xl font-bold text-slate-800 tracking-tight flex items-center gap-3">
        <Camera class="w-7 h-7 text-amber-500 stroke-[1.5]" />
        บันทึกใบหน้า น.ศ. <span class="text-sm font-medium text-slate-400 ml-2 hidden sm:inline">(Face Registration)</span>
      </h2>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      
      <!-- ส่วนค้นหานักศึกษา -->
      <div class="md:col-span-1 bg-white p-5 rounded-2xl border border-slate-200 shadow-sm h-fit">
        <label class="block text-sm font-bold text-slate-700 mb-3">ค้นหารหัสนักศึกษา</label>
        
        <div class="flex flex-col gap-3 mb-5">
          <div class="relative w-full">
            <Search class="w-5 h-5 text-slate-400 absolute left-3.5 top-3 stroke-[1.5]" />
            <input 
              v-model="studentCode" 
              type="text" 
              placeholder="เช่น 6334002094" 
              class="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-amber-500/20 focus:border-amber-500 text-slate-700 transition-all outline-none"
              @keyup.enter="searchStudent"
            >
          </div>
          <button @click="searchStudent" class="w-full bg-slate-800 text-white px-4 py-2.5 rounded-xl hover:bg-slate-900 font-semibold shadow-sm transition-all flex justify-center items-center gap-2">
            <Search class="w-4 h-4 stroke-[2]" /> ค้นหา
          </button>
        </div>

        <!-- แสดงข้อมูลนักศึกษาเมื่อค้นหาเจอ -->
        <div v-if="studentInfo" class="p-4 bg-emerald-50/50 border border-emerald-100 rounded-xl text-sm animate-fade-in-up relative overflow-hidden">
          <!-- แถบสีด้านซ้าย -->
          <div class="absolute left-0 top-0 bottom-0 w-1 bg-emerald-400"></div>
          
          <div class="flex items-start gap-3">
            <div class="bg-white p-2 rounded-lg shadow-sm border border-emerald-100">
              <User class="w-5 h-5 text-emerald-600 stroke-[1.5]" />
            </div>
            <div class="min-w-0 flex-1">
              <p class="font-bold text-slate-800 text-base mb-0.5 truncate">{{ studentInfo.name }}</p>
              <p class="text-xs font-medium text-slate-500 mb-2 truncate">{{ studentInfo.faculty }}</p>
              <p class="text-[11px] font-bold text-emerald-700 bg-emerald-100/50 border border-emerald-200 px-2 py-1 rounded-md inline-flex items-center gap-1.5 shadow-sm">
                <UserCheck class="w-3.5 h-3.5 stroke-[2]" /> พร้อมบันทึกใบหน้า
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- ส่วนกล้องถ่ายรูป -->
      <div class="md:col-span-2 bg-white p-5 md:p-6 rounded-2xl border border-slate-200 shadow-sm">
        <div class="flex justify-between items-center mb-5 pb-3 border-b border-slate-100">
          <h3 class="text-lg font-bold text-slate-700 flex items-center gap-2">
            <Video class="w-5 h-5 text-amber-500 stroke-[1.5]" /> กล้องถ่ายรูป
          </h3>
          
          <button @click="startCamera" v-if="!isCameraOn" class="bg-white border border-slate-200 text-slate-700 px-4 py-2 rounded-lg text-xs font-bold hover:bg-slate-50 hover:border-slate-300 shadow-sm transition-all flex items-center gap-1.5">
            <Video class="w-4 h-4 stroke-[1.5]" /> เปิดกล้อง
          </button>
          <button @click="stopCamera" v-else class="bg-rose-50 border border-rose-200 text-rose-600 px-4 py-2 rounded-lg text-xs font-bold hover:bg-rose-100 shadow-sm transition-all flex items-center gap-1.5">
            <VideoOff class="w-4 h-4 stroke-[1.5]" /> ปิดกล้อง
          </button>
        </div>

        <!-- กล่องแสดงภาพจากกล้อง -->
        <div class="relative bg-slate-900 rounded-2xl overflow-hidden flex justify-center items-center aspect-[4/3] w-full mb-6 ring-4 ring-slate-50 border border-slate-200 shadow-inner group">
          <video ref="videoEl" autoplay playsinline class="h-full w-full object-cover" v-show="isCameraOn && !capturedImage"></video>
          
          <!-- ภาพพรีวิวที่ถ่ายแล้ว -->
          <img :src="capturedImage" v-if="capturedImage" class="h-full w-full object-cover" />
          
          <div v-if="!isCameraOn && !capturedImage" class="text-slate-400 flex flex-col items-center justify-center gap-3 w-full h-full bg-slate-800/50">
            <VideoOff class="w-10 h-10 stroke-[1.5] opacity-50" />
            <span class="text-sm font-medium tracking-wide">กล้องปิดอยู่</span>
          </div>
          
          <!-- กรอบโฟกัส (โชว์ตอนเปิดกล้อง) -->
          <div v-if="isCameraOn && !capturedImage" class="absolute inset-0 pointer-events-none flex items-center justify-center">
             <div class="w-56 h-64 border border-white/20 rounded-[100px] relative">
                <!-- เส้นไกด์นำสายตา -->
                <div class="absolute inset-0 border-2 border-dashed border-white/40 rounded-[100px] animate-[spin_10s_linear_infinite]"></div>
             </div>
          </div>
        </div>

        <!-- ปุ่มควบคุมการถ่าย -->
        <div class="flex flex-wrap justify-center gap-3">
          <button 
            v-if="isCameraOn && !capturedImage" 
            @click="takePhoto" 
            class="bg-amber-500 text-white px-8 py-3 rounded-full font-bold hover:bg-amber-600 shadow-md hover:shadow-lg transition-all flex items-center gap-2 transform active:scale-95"
          >
            <Aperture class="w-5 h-5 stroke-[2]" /> ถ่ายรูป
          </button>
          
          <button 
            v-if="capturedImage" 
            @click="retakePhoto" 
            class="bg-white border border-slate-300 text-slate-600 px-6 py-2.5 rounded-xl font-bold hover:bg-slate-50 hover:text-slate-800 shadow-sm transition-all flex items-center gap-2"
          >
            <RefreshCw class="w-4 h-4 stroke-[2]" /> ถ่ายใหม่
          </button>
          
          <button 
            v-if="capturedImage" 
            @click="saveFaceData" 
            :disabled="!studentInfo || isSaving"
            class="bg-emerald-600 text-white px-8 py-2.5 rounded-xl font-bold hover:bg-emerald-700 disabled:bg-slate-300 disabled:text-slate-500 shadow-sm hover:shadow transition-all flex items-center gap-2"
          >
            <Loader2 v-if="isSaving" class="w-4 h-4 animate-spin stroke-[2]" />
            <Save v-else class="w-4 h-4 stroke-[2]" />
            บันทึกรูปภาพ
          </button>
        </div>

        <!-- Canvas ซ่อนไว้สำหรับแปลงวิดีโอเป็นรูปภาพ -->
        <canvas ref="canvasEl" class="hidden"></canvas>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onBeforeUnmount } from 'vue';
import api from '../services/api';
import Swal from 'sweetalert2';
// 💡 Import ไอคอนจาก Lucide
import { 
  Camera, Search, User, UserCheck, 
  Video, VideoOff, Aperture, 
  RefreshCw, Save, Loader2 
} from 'lucide-vue-next';

const studentCode = ref('');
const studentInfo = ref(null);

const videoEl = ref(null);
const canvasEl = ref(null);
const isCameraOn = ref(false);
const streamData = ref(null);
const capturedImage = ref(null);
const isSaving = ref(false);

const searchStudent = async () => {
  if (!studentCode.value) return;
  try {
    // ข้อมูลจำลองชั่วคราว
    studentInfo.value = {
      name: "นางสาว พัทธมา นนท์ดอน",
      faculty: "สำนักวิชาเทคโนโลยีสารสนเทศ"
    };
  } catch (error) {
    Swal.fire({
      icon: 'error',
      title: 'ไม่พบข้อมูล',
      text: 'กรุณาตรวจสอบรหัสนักศึกษาอีกครั้ง',
      confirmButtonColor: '#f43f5e',
      customClass: { popup: 'rounded-2xl', confirmButton: 'rounded-lg px-6' }
    });
    studentInfo.value = null;
  }
};

const startCamera = async () => {
  try {
    const constraints = { video: { facingMode: 'user' } };
    streamData.value = await navigator.mediaDevices.getUserMedia(constraints);
    if (videoEl.value) {
      videoEl.value.srcObject = streamData.value;
    }
    isCameraOn.value = true;
    capturedImage.value = null;
  } catch (error) {
    console.error('Camera error:', error);
    Swal.fire({
      icon: 'error',
      title: 'ผิดพลาด',
      text: 'ไม่สามารถเข้าถึงกล้องได้ กรุณาตรวจสอบสิทธิ์',
      confirmButtonColor: '#f43f5e',
      customClass: { popup: 'rounded-2xl', confirmButton: 'rounded-lg px-6' }
    });
  }
};

const stopCamera = () => {
  if (streamData.value) {
    streamData.value.getTracks().forEach(track => track.stop());
    streamData.value = null;
  }
  isCameraOn.value = false;
};

const takePhoto = () => {
  if (!videoEl.value || !canvasEl.value) return;
  const video = videoEl.value;
  const canvas = canvasEl.value;
  
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  
  const ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  
  capturedImage.value = canvas.toDataURL('image/jpeg', 0.8);
};

const retakePhoto = () => {
  capturedImage.value = null;
};

const saveFaceData = async () => {
  if (!studentCode.value || !capturedImage.value) return;
  
  isSaving.value = true;
  try {
    const response = await api.post('/attendance/register-face', {
      studentcode: studentCode.value,
      image_base64: capturedImage.value
    });
    
    Swal.fire({
      icon: 'success',
      title: 'บันทึกสำเร็จ',
      text: response.data?.message || 'บันทึกใบหน้าเรียบร้อยแล้ว',
      timer: 1500,
      showConfirmButton: false,
      customClass: { popup: 'rounded-2xl' }
    });
    
    studentCode.value = '';
    studentInfo.value = null;
    retakePhoto();
    
  } catch (error) {
    Swal.fire({
      icon: 'error',
      title: 'ผิดพลาด',
      text: error.response?.data?.detail || 'ไม่สามารถบันทึกข้อมูลได้',
      confirmButtonColor: '#f43f5e',
      customClass: { popup: 'rounded-2xl', confirmButton: 'rounded-lg px-6' }
    });
  } finally {
    isSaving.value = false;
  }
};

onBeforeUnmount(() => {
  stopCamera();
});
</script>

<style scoped>
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(15px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in-up {
  animation: fadeInUp 0.4s ease-out forwards;
}
</style>