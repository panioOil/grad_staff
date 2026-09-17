<template>
  <div class="p-8 max-w-md mx-auto bg-white rounded-xl shadow-md space-y-4 mt-10">
    <h2 class="text-xl font-bold text-slate-800">Mockup Login (Development Mode)</h2>
    <p class="text-sm text-slate-500">เลือกบัญชีจำลองเพื่อทดสอบสิทธิ์การใช้งานระบบ</p>
    
    <select v-model="selectedUser" class="w-full p-2 border rounded-lg">
      <option disabled value="">-- เลือกบัญชีทดสอบ --</option>
      <optgroup label="Admin">
        <option :value="mockAdmins[0]">Pattama (Admin)</option>
        <option :value="mockAdmins[1]">TUM (Admin)</option>
      </optgroup>
      <optgroup label="Staff">
        <option :value="mockStaffs[0]">Moo (Staff)</option>
      </optgroup>
      <optgroup label="ส่วนพัฒนาระบบ (PatStaff)">
        <option :value="mockPatStaffs[0]">Beer (PatStaff)</option>
      </optgroup>
      <optgroup label="REG Staff">
        <option :value="reg_staff[0]">Fasai (REG Staff)</option>
      </optgroup>
      <optgroup label="Other">
        <option :value="other[0]">Somchai (Other)</option>
      </optgroup>
    </select>

    <button @click="handleMockLogin" class="w-full bg-emerald-600 text-white p-2 rounded-lg font-semibold hover:bg-emerald-700 transition">
      เข้าสู่ระบบจำลอง
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const mockAdmins = [
  { upn: "pattama.non@mfu.ac.th", email: "pattama.non@mfu.ac.th", given_name: "Pattama", family_name: "Nondon", username: "57360045", depart_name: "DTI", depart_id: "6000", role: "admin" },
  { upn: "tum.it@mfu.ac.th", email: "tum.it@mfu.ac.th", given_name: "TUM", family_name: "Dev", username: "57360046", depart_name: "DTI", depart_id: "6000", role: "admin" }
]

const mockStaffs = [
  { upn: "moo.dev@mfu.ac.th", email: "moo.dev@mfu.ac.th", given_name: "Moo", family_name: "ส่วนพัฒ", username: "57360047", depart_name: "DEV", depart_id: "4000", role: "staff" }
]

const mockPatStaffs = [
  { upn: "beer.it@mfu.ac.th", email: "beer.it@mfu.ac.th", given_name: "Beer", family_name: "Support", username: "57360048", depart_name: "DEV", depart_id: "4000", role: "pat_staff" }
]

const reg_staff = [
  { upn: "fasai.user@mfu.ac.th", email: "fasai.user@mfu.ac.th", given_name: "Fasai", family_name: "General", username: "65310001", depart_name: "Academic Division", depart_id: "1000", role: "reg_staff" }
]

const other = [
  { upn: "somchai.student@mfu.ac.th", email: "somchai.student@mfu.ac.th", given_name: "Somchai", family_name: "Jaidee", username: "65310002", depart_name: "School of IT", depart_id: "2000", role: "other" }
]

const selectedUser = ref('')

const handleMockLogin = () => {
  if (!selectedUser.value) return
  localStorage.setItem('user_session', JSON.stringify(selectedUser.value))
  window.location.href = '/dashboard' // หรือเปลี่ยนเส้นทางตามต้องการ
  router.push('/dashboard')
}
</script>