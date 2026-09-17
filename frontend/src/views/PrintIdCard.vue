<template>
  <div class="min-h-screen bg-slate-50 font-sans pb-20">    
    <!-- แถบสลับมุมมอง (Tabs) -->
    <div class="bg-white px-4 md:px-8 py-4 shadow-sm border-b border-slate-200 sticky top-0 z-20 flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4">
      <div>
        <h1 class="text-xl font-bold text-slate-800 tracking-tight flex items-center gap-2">
          <Layers class="w-6 h-6 text-amber-500 stroke-[1.5]" />
          ระบบจัดการบัตรและรายงานบัณฑิต
        </h1>
        <p class="text-xs font-medium text-slate-500 mt-1">เลือกมุมมองการทำงานด้านล่างเพื่อจัดการข้อมูล</p>
      </div>
      
      <div class="flex bg-slate-100 p-1.5 rounded-xl shadow-inner overflow-x-auto">
        <button @click="currentTab = 'cards'" 
                class="flex items-center gap-2 px-5 py-2.5 text-sm font-bold rounded-lg transition-all duration-300 whitespace-nowrap"
                :class="currentTab === 'cards' ? 'bg-white text-amber-600 shadow-sm ring-1 ring-slate-200/50' : 'text-slate-500 hover:text-slate-700 hover:bg-slate-200/50'">
          <Contact class="w-4 h-4 stroke-[2]" /> พิมพ์บัตรประจำตัว
        </button>
        <button @click="currentTab = 'report'" 
                class="flex items-center gap-2 px-5 py-2.5 text-sm font-bold rounded-lg transition-all duration-300 whitespace-nowrap"
                :class="currentTab === 'report' ? 'bg-white text-amber-600 shadow-sm ring-1 ring-slate-200/50' : 'text-slate-500 hover:text-slate-700 hover:bg-slate-200/50'">
          <ClipboardList class="w-4 h-4 stroke-[2]" /> รายงานใบลงทะเบียน
        </button>
      </div>
    </div>

    <div class="p-4 md:p-8">
        
        <!-- ================= 1. โซนพิมพ์บัตรประจำตัว (Cards Tab) ================= -->
        <div v-if="currentTab === 'cards'" class="max-w-7xl mx-auto space-y-6">
            <div v-if="!showPreview" class="bg-white p-6 md:p-8 rounded-2xl shadow-sm border border-slate-200">
                
                <div class="flex items-center gap-3 mb-6 border-b border-slate-100 pb-4">
                    <div class="bg-amber-100 p-2.5 rounded-xl">
                      <Search class="w-5 h-5 text-amber-600 stroke-[1.5]" />
                    </div>
                    <h2 class="text-lg md:text-xl font-bold text-slate-800">ค้นหารายชื่อเพื่อพิมพ์บัตรประจำตัว</h2>
                </div>

                <!-- ฟอร์มค้นหา Cards -->
                <div class="grid grid-cols-1 md:grid-cols-4 gap-5 mb-8 bg-slate-50/50 p-5 rounded-2xl border border-slate-100">
                    <div class="relative">
                        <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">ปีการศึกษา</label>
                        <input v-model="filters.year" type="text" class="w-full px-4 py-2.5 bg-white border border-slate-200 rounded-xl focus:ring-2 focus:ring-amber-500/20 focus:border-amber-500 text-slate-700 text-sm transition-all outline-none" placeholder="เช่น 2567">
                    </div>
                    <div class="relative">
                        <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">สำนักวิชา</label>
                        <select v-model="filters.facultyid" class="w-full pl-4 pr-10 py-2.5 bg-white border border-slate-200 rounded-xl focus:ring-2 focus:ring-amber-500/20 focus:border-amber-500 text-slate-700 text-sm appearance-none transition-all outline-none cursor-pointer">
                            <option value="">-- ทั้งหมด --</option>
                            <option v-for="fac in faculties" :key="fac.facultyid" :value="fac.facultyid">{{ fac.facultyname }}</option>
                        </select>
                        <ChevronDown class="w-4 h-4 text-slate-400 absolute right-3 bottom-3 pointer-events-none stroke-[1.5]" />
                    </div>
                    <div class="relative">
                        <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">สาขาวิชา</label>
                        <select v-model="filters.program" class="w-full pl-4 pr-10 py-2.5 bg-white border border-slate-200 rounded-xl focus:ring-2 focus:ring-amber-500/20 focus:border-amber-500 text-slate-700 text-sm appearance-none transition-all outline-none cursor-pointer disabled:bg-slate-100 disabled:text-slate-400" :disabled="!filters.facultyid && availableDepartments.length === 0">
                            <option value="">-- ทั้งหมด --</option>
                            <option v-for="dept in availableDepartments" :key="dept.departmentid" :value="dept.departmentname">{{ dept.departmentname }}</option>
                        </select>
                        <ChevronDown class="w-4 h-4 text-slate-400 absolute right-3 bottom-3 pointer-events-none stroke-[1.5]" />
                    </div>
                    <div class="relative">
                        <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">รหัสนักศึกษา</label>
                        <input v-model="filters.studentId" type="text" class="w-full px-4 py-2.5 bg-white border border-slate-200 rounded-xl focus:ring-2 focus:ring-amber-500/20 focus:border-amber-500 text-slate-700 text-sm transition-all outline-none" placeholder="ค้นหารหัส...">
                    </div>
                </div>

                <!-- สรุปผล Cards -->
                <div class="flex flex-col sm:flex-row justify-between items-center bg-emerald-50 border border-emerald-100 p-4 md:p-5 rounded-2xl mb-6 gap-4">
                    <div class="flex items-center gap-3">
                        <CheckCircle2 class="w-6 h-6 text-emerald-500 stroke-[1.5]" />
                        <div class="text-sm font-medium text-emerald-800">
                            พบรายชื่อที่ตรงเงื่อนไข <span class="text-emerald-600 font-bold text-lg mx-1">{{ filteredStudents.length }}</span> คน 
                            <span class="text-emerald-600/70 ml-2">(ใช้กระดาษ {{ paginatedPages.length }} หน้า)</span>
                        </div>
                    </div>
                    <button @click="generatePreview" :disabled="filteredStudents.length === 0"
                        class="w-full sm:w-auto bg-slate-800 hover:bg-slate-900 disabled:bg-slate-300 disabled:text-slate-500 text-white px-6 py-2.5 rounded-xl font-bold shadow-sm transition-all flex items-center justify-center gap-2 flex-shrink-0">
                        <LayoutTemplate class="w-4 h-4 stroke-[2]" /> ดูตัวอย่างบัตรบน A4
                    </button>
                </div>

                <!-- ตารางรายชื่อ Cards -->
                <div class="overflow-hidden border border-slate-200 rounded-xl shadow-sm">
                    <div class="overflow-x-auto max-h-[450px] custom-scrollbar">
                        <table class="w-full text-sm text-left whitespace-nowrap">
                            <thead class="text-xs text-slate-500 font-bold uppercase tracking-wider bg-slate-50 sticky top-0 z-10 shadow-sm border-b border-slate-200">
                                <tr>
                                    <th class="px-5 py-4">ลำดับ</th>
                                    <th class="px-5 py-4">รหัสนักศึกษา</th>
                                    <th class="px-5 py-4">ชื่อ-นามสกุล</th>
                                    <th class="px-5 py-4">สำนักวิชา</th>
                                    <th class="px-5 py-4">สาขาวิชา</th>
                                    <th class="px-5 py-4 text-center">ลำดับขึ้นรับ</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-slate-100">
                                <tr v-for="(student, index) in filteredStudents.slice(0, 50)" :key="student.studentcode" class="hover:bg-slate-50/80 transition-colors">
                                    <td class="px-5 py-3.5 text-slate-500">{{ index + 1 }}</td>
                                    <td class="px-5 py-3.5 font-bold text-slate-700">{{ student.studentcode }}</td>
                                    <td class="px-5 py-3.5 font-medium text-slate-600">{{ student.studentname }}</td>
                                    <td class="px-5 py-3.5 text-slate-500 truncate max-w-[200px]" :title="student.facultyname">{{ student.facultyname }}</td>
                                    <td class="px-5 py-3.5 text-slate-500 truncate max-w-[200px]" :title="student.programname">{{ student.programname }}</td>
                                    <td class="px-5 py-3.5 text-center">
                                      <span class="inline-flex items-center justify-center bg-slate-100 border border-slate-200 text-slate-700 px-3 py-1 rounded-lg text-xs font-bold shadow-sm">
                                        {{ student.orderno }}
                                      </span>
                                    </td>
                                </tr>
                                <tr v-if="filteredStudents.length === 0">
                                  <td colspan="6" class="px-5 py-12 text-center text-slate-400">
                                    <div class="flex flex-col items-center gap-2">
                                      <SearchX class="w-10 h-10 stroke-[1.5] opacity-50" />
                                      <span class="text-sm font-medium">ไม่พบข้อมูลตามเงื่อนไขที่ระบุ</span>
                                    </div>
                                  </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            
            <!-- หน้า Preview สำหรับ Cards -->
            <div v-else class="animate-fade-in-up">
                <div class="max-w-[210mm] mx-auto flex flex-col sm:flex-row justify-between items-center bg-slate-800 text-slate-200 p-4 rounded-2xl shadow-xl mb-6 sticky top-24 z-30 gap-4 border border-slate-700">
                    <button @click="showPreview = false" class="w-full sm:w-auto bg-slate-700 hover:bg-slate-600 px-5 py-2.5 rounded-xl text-sm font-bold transition-all flex items-center justify-center gap-2 shadow-sm">
                        <ArrowLeft class="w-4 h-4 stroke-[2]" /> กลับไปค้นหา
                    </button>
                    <div class="font-medium text-sm flex items-center gap-2">
                        <FileText class="w-4 h-4 text-amber-400 stroke-[2]" /> ตัวอย่างหน้า A4 (ทั้งหมด <span class="text-white font-bold">{{ paginatedPages.length }}</span> หน้า)
                    </div>
                    <button @click="downloadPDF" :disabled="isGeneratingPDF" class="w-full sm:w-auto bg-amber-500 hover:bg-amber-600 disabled:bg-slate-600 disabled:text-slate-400 text-white px-6 py-2.5 rounded-xl text-sm font-bold shadow-sm transition-all flex items-center justify-center gap-2">
                        <Loader2 v-if="isGeneratingPDF" class="w-4 h-4 animate-spin stroke-[2]" />
                        <Download v-else class="w-4 h-4 stroke-[2]" />
                        {{ isGeneratingPDF ? 'กำลังสร้าง PDF...' : 'ดาวน์โหลดไฟล์ PDF' }}
                    </button>
                </div>

                <div id="pdf-container" class="flex flex-col items-center space-y-8">
                    <div v-for="(page, pageIndex) in paginatedPages" :key="pageIndex" class="a4-page bg-white relative shadow-md ring-1 ring-slate-200" style="page-break-after: always;">
                        <div class="grid grid-cols-2 gap-x-4 gap-y-4 pt-8 px-6 pb-6 w-full">
                            <div v-for="student in page" :key="student.studentcode" class="card-item border-[1.5px] border-slate-800 rounded-lg overflow-hidden bg-white h-[180px] w-[320px] mx-auto" style="display: table; table-layout: fixed;">
                                <div style="display: table-row;">
                                    <div :class="getFacultyColor(student.facultyid)" style="display: table-cell; width: 12px;"></div>
                                    <div class="bg-[#D4AF37]" style="display: table-cell; width: 8px;"></div>
                                    <div style="display: table-cell; width: 200px; padding: 10px; vertical-align: top;">
                                        <h3 class="text-[14px] font-extrabold text-blue-900 text-center leading-tight">บัตรประจำตัวบัณฑิต</h3>
                                        <p class="text-[11px] font-medium text-slate-700 text-center leading-tight">พิธีพระราชทานปริญญาบัตร <br/>ปีการศึกษา {{ student.acadyear }}</p>
                                        <div class="flex items-center justify-center gap-5 mt-5">
                                            <svg :id="'barcode-' + student.studentcode" style="height: 50px; width: 80px;"></svg>
                                            <canvas :id="'qrcode-' + student.studentcode" style="width: 40px; height: 40px;"></canvas>
                                        </div>
                                        <div class="mt-3 text-center">
                                            <p class="text-[11px] font-bold text-slate-800 px-1">{{ student.studentname }}</p>
                                            <p class="text-[12px] font-medium text-slate-700 mt-0.5">รหัสนักศึกษา : {{ student.studentcode }}</p>
                                        </div>
                                    </div>
                                    <div style="display: table-cell; width: 108px; vertical-align: top;">
                                        <div class="h-[136px] bg-slate-100 p-0.5 relative flex items-center justify-center overflow-hidden">
                                            <img v-if="student.faceBase64" :src="student.faceBase64" class="w-full h-full object-cover">
                                            <User v-else class="w-8 h-8 text-slate-300" />
                                        </div>
                                        <div class="text-white bg-[#9E1B1B] flex flex-col items-center justify-center border-t-[2px] border-red-600" style="height: 45px; padding-top: 1px; padding-bottom: 14px;">
                                            <br/><p class="text-[8px] font-light leading-none mb-0.5">ลำดับขึ้นรับ</p>
                                            <p class="text-[14px] font-black leading-none tracking-wider">{{ student.orderno }}</p><br/>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ================= 2. โซนรายงานใบลงทะเบียน (Report Tab) ================= -->
        <div v-else class="max-w-[297mm] mx-auto bg-white p-6 md:p-8 rounded-2xl shadow-sm border border-slate-200 mb-8 animate-fade-in">
            <div class="flex items-center gap-3 mb-6 border-b border-slate-100 pb-4">
                <div class="bg-amber-100 p-2.5 rounded-xl">
                    <ClipboardList class="w-5 h-5 text-amber-600 stroke-[1.5]" />
                </div>
                <h2 class="text-lg md:text-xl font-bold text-slate-800">
                    รายงานใบลงทะเบียน
                </h2>
            </div>

            <!-- ฟอร์มค้นหา Report -->
            <div class="grid grid-cols-1 md:grid-cols-5 gap-4 md:gap-5 mb-8 bg-slate-50/50 p-5 rounded-2xl border border-slate-100">
                <div class="relative">
                    <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">ปีการศึกษา</label>
                    <input v-model="filters.year" type="text" class="w-full px-4 py-2.5 bg-white border border-slate-200 rounded-xl focus:ring-2 focus:ring-amber-500/20 focus:border-amber-500 text-slate-700 text-sm transition-all outline-none" placeholder="เช่น 2567">
                </div>
                <div class="relative">
                    <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">สำนักวิชา</label>
                    <select v-model="filters.facultyid" class="w-full pl-4 pr-10 py-2.5 bg-white border border-slate-200 rounded-xl focus:ring-2 focus:ring-amber-500/20 focus:border-amber-500 text-slate-700 text-sm appearance-none transition-all outline-none cursor-pointer">
                        <option value="">-- ทั้งหมด --</option>
                        <option v-for="fac in faculties" :key="fac.facultyid" :value="fac.facultyid">{{ fac.facultyname }}</option>
                    </select>
                    <ChevronDown class="w-4 h-4 text-slate-400 absolute right-3 bottom-3 pointer-events-none stroke-[1.5]" />
                </div>
                <div class="relative">
                    <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">สาขาวิชา</label>
                    <select v-model="filters.program" class="w-full pl-4 pr-10 py-2.5 bg-white border border-slate-200 rounded-xl focus:ring-2 focus:ring-amber-500/20 focus:border-amber-500 text-slate-700 text-sm appearance-none transition-all outline-none cursor-pointer disabled:bg-slate-100 disabled:text-slate-400" :disabled="!filters.facultyid && availableDepartments.length === 0">
                        <option value="">-- ทั้งหมด --</option>
                        <option v-for="dept in availableDepartments" :key="dept.departmentid" :value="dept.departmentname">{{ dept.departmentname }}</option>
                    </select>
                    <ChevronDown class="w-4 h-4 text-slate-400 absolute right-3 bottom-3 pointer-events-none stroke-[1.5]" />
                </div>
                <div class="relative">
                    <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">รหัสนักศึกษา</label>
                    <input v-model="filters.studentId" type="text" class="w-full px-4 py-2.5 bg-white border border-slate-200 rounded-xl focus:ring-2 focus:ring-amber-500/20 focus:border-amber-500 text-slate-700 text-sm transition-all outline-none" placeholder="ค้นหารหัส...">
                </div>
                <div class="flex flex-col gap-2 justify-end">
                    <button @click="fetchAllStudents" class="w-full bg-slate-800 text-white px-4 py-2.5 rounded-xl text-sm font-bold hover:bg-slate-900 shadow-sm transition-all flex items-center justify-center gap-2">
                        <Search class="w-4 h-4 stroke-[2]" /> ค้นหาข้อมูล
                    </button>
                    <button @click="downloadReportPDF" :disabled="isGeneratingReportPDF || reportPages.length === 0" class="w-full bg-amber-500 disabled:bg-slate-300 disabled:text-slate-500 text-white px-4 py-2.5 rounded-xl text-sm font-bold hover:bg-amber-600 shadow-sm transition-all flex items-center justify-center gap-2">
                        <Loader2 v-if="isGeneratingReportPDF" class="w-4 h-4 animate-spin stroke-[2]" />
                        <Printer v-else class="w-4 h-4 stroke-[2]" />
                        พิมพ์รายงาน
                    </button>
                </div>
            </div>

            <!-- ระบบ Pagination สำหรับดูตัวอย่างบนหน้าเว็บ -->
            <div v-if="reportPages.length > 0" class="flex flex-col sm:flex-row justify-between items-center bg-slate-800 text-slate-200 p-4 rounded-t-2xl mt-4 gap-4 border border-slate-700">
                <span class="text-sm font-medium flex items-center gap-2">
                  <FileText class="w-4 h-4 text-amber-400 stroke-[2]" /> 
                  ตัวอย่างรายงาน <span class="text-white font-bold ml-1">(หน้า {{ currentReportPage }} จาก {{ reportPages.length }})</span>
                </span>
                <div class="flex gap-2">
                    <button @click="prevReportPage" :disabled="currentReportPage === 1" class="px-4 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg disabled:opacity-50 text-sm font-bold flex items-center gap-1.5 transition-colors">
                      <ChevronLeft class="w-4 h-4 stroke-[2]" /> ก่อนหน้า
                    </button>
                    <button @click="nextReportPage" :disabled="currentReportPage === reportPages.length" class="px-4 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg disabled:opacity-50 text-sm font-bold flex items-center gap-1.5 transition-colors">
                      ถัดไป <ChevronRight class="w-4 h-4 stroke-[2]" />
                    </button>
                </div>
            </div>

            <!-- โซนแสดงหน้า A4 บนจอเว็บ -->
            <div id="report-screen-view" class="bg-slate-200/80 p-6 md:p-8 rounded-b-2xl flex justify-center overflow-auto border border-t-0 border-slate-300" v-if="!isGeneratingReportPDF && displayedReportPage">
                <div class="a4-page report-layout bg-white rounded-sm" style="box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);">
                    
                    <div class="text-center mb-5 border-b-2 border-slate-800 pb-4">
                        <h1 class="text-lg font-bold text-slate-900 tracking-tight">ใบลงทะเบียนพิธีพระราชทานปริญญาบัตร ประจำปีการศึกษา {{ filters.year || '2567' }}</h1>
                        <h2 class="text-sm font-bold text-slate-700 mt-2">ระดับ {{ displayedReportPage.levelName }}</h2>
                        <h2 class="text-sm font-bold text-slate-700 mt-0.5">สำนักวิชา {{ displayedReportPage.facultyName }}</h2>
                    </div>

                    <div class="bg-slate-800 text-white text-xs font-bold px-4 py-2 mt-0 flex justify-between rounded-t-sm border border-slate-800 border-b-0">
                        <span>{{ displayedReportPage.degreeName }}</span>
                        <span>ส่วนที่ {{ displayedReportPage.partNumber }} / {{ displayedReportPage.totalParts }}</span>
                    </div>

                    <table class="w-full border-collapse border border-slate-800 text-[10px]">
                        <thead>
                            <tr class="bg-slate-100 text-slate-800 text-center font-bold">
                                <th rowspan="2" class="border border-slate-800 p-1.5 w-12">ลำดับขึ้นรับ</th>
                                <th rowspan="2" class="border border-slate-800 p-1.5 w-10">ที่</th>
                                <th rowspan="2" class="border border-slate-800 p-1.5 w-32">ชื่อ</th>
                                <th rowspan="2" class="border border-slate-800 p-1.5 w-32">สกุล</th>
                                <th rowspan="2" class="border border-slate-800 p-1.5 w-24">รหัสนักศึกษา</th>
                                <th colspan="2" class="border border-slate-800 p-1.5">วันรายงานตัว</th>
                                <th colspan="2" class="border border-slate-800 p-1.5">วันซ้อมย่อย</th>
                                <th colspan="2" class="border border-slate-800 p-1.5">วันซ้อมใหญ่</th>
                                <th rowspan="2" class="border border-slate-800 p-1.5 w-20">พิธีพระราชทาน</th>
                            </tr>
                            <tr class="bg-slate-100 text-slate-800 text-center font-bold">
                                <th class="border border-slate-800 p-1.5 w-10">เช้า</th>
                                <th class="border border-slate-800 p-1.5 w-10">บ่าย</th>
                                <th class="border border-slate-800 p-1.5 w-10">เช้า</th>
                                <th class="border border-slate-800 p-1.5 w-10">บ่าย</th>
                                <th class="border border-slate-800 p-1.5 w-10">เช้า</th>
                                <th class="border border-slate-800 p-1.5 w-10">บ่าย</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(student, index) in displayedReportPage.students" :key="student.studentcode" 
                                class="text-center h-8" :class="{ 'bg-slate-200': shouldHighlight(student) }">
                                <td class="border border-slate-800 font-bold bg-slate-50">{{ student.orderno }}</td>
                                <td class="border border-slate-800 font-medium">{{ (displayedReportPage.partNumber - 1) * REPORT_ROWS_PER_PAGE + index + 1 }}</td>
                                <td class="border border-slate-800 text-left px-3 font-semibold text-slate-800">{{ student.studentname }}</td>
                                <td class="border border-slate-800 text-left px-3 font-semibold text-slate-800">{{ student.studentsurname || '-' }}</td>
                                <td class="border border-slate-800 tracking-wider font-medium text-slate-700">{{ student.studentcode }}</td>
                                <td class="border border-slate-800"></td><td class="border border-slate-800"></td>
                                <td class="border border-slate-800"></td><td class="border border-slate-800"></td>
                                <td class="border border-slate-800"></td><td class="border border-slate-800"></td>
                                <td class="border border-slate-800"></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- ================= หน้าจอ Loading & พื้นที่สร้าง PDF ================= -->
            <div v-if="isGeneratingReportPDF" class="fixed inset-0 z-[9999] bg-slate-900/90 backdrop-blur-sm overflow-y-auto flex flex-col items-center justify-center text-white">
                <Loader2 class="animate-spin w-12 h-12 text-amber-500 mb-4 stroke-[2]" />
                <h2 class="text-2xl font-bold tracking-tight">กำลังจัดเตรียมไฟล์ PDF...</h2>
                <p class="text-sm text-slate-300 mt-2 font-medium bg-slate-800 px-4 py-2 rounded-full border border-slate-700">ระบบกำลังประมวลผลทั้งหมด {{ reportPages.length }} หน้า กรุณารอสักครู่</p>
            </div>
        </div>
    </div>      
</div>
</template>

<script setup>
import { ref, shallowRef, computed, watch, nextTick, onMounted } from 'vue';
import JsBarcode from 'jsbarcode';
import QRCode from 'qrcode';
import html2pdf from 'html2pdf.js';
import api from '../services/api';
import { useRouter } from 'vue-router';
// 💡 Import ไอคอน Lucide แบบ Dynamic
import { 
  Printer, Download, ChevronDown, Layers, 
  Contact, ClipboardList, Search, CheckCircle2, 
  LayoutTemplate, SearchX, ArrowLeft, FileText, 
  Loader2, ChevronLeft, ChevronRight, User
} from 'lucide-vue-next';

const apiUrl = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8001';

const showPreview = ref(false);
const isGeneratingPDF = ref(false);
const isGeneratingReportPDF = ref(false); 

const currentTab = ref('cards');
const filters = ref({ year: '', facultyid: '', program: '', studentId: '' });

const students = shallowRef([]);
const allGraduates = shallowRef([]); 
const faculties = ref([]);
const allDepartments = ref([]);

const facultyColors = { "10": "bg-slate-500", "11": "bg-yellow-400", "12": "bg-sky-400", "13": "bg-blue-600", "14": "bg-pink-300", "16": "bg-white", "17": "bg-pink-600", "18": "bg-green-300", "19": "bg-orange-500", "20": "bg-green-800", "21": "bg-green-600", "22": "bg-purple-900", "23": "bg-amber-100", "24": "bg-rose-600", "25": "bg-teal-700" };
const getFacultyColor = (facultyId) => { return facultyColors[String(facultyId)] || "bg-slate-700"; };
const shouldHighlight = (student) => { const status = Number(student.is_attending || 0); return status >= 20 && status < 70; };

const fetchDropdownData = async () => {
    try {
        const [facRes, deptRes] = await Promise.all([ api.get('/graduations/faculties'), api.get('/graduations/departments') ]);
        faculties.value = facRes.data; allDepartments.value = deptRes.data;
    } catch (error) { console.error("ดึงข้อมูลตัวเลือกผิดพลาด:", error); }
};

const fetchStudents = async () => {
    try { const response = await api.get('/graduations/attendees'); students.value = response.data; } 
    catch (error) { console.error("ดึงข้อมูลนักศึกษาผิดพลาด:", error); }
};

const fetchAllStudents = async () => {
    try {
        const targetYear = filters.value.year || '2567';
        const response = await api.get(`/graduations/all-graduates/${targetYear}`);
        allGraduates.value = response.data; 
    } catch (error) { console.error("ดึงข้อมูลบัณฑิตทั้งหมดผิดพลาด:", error); }
};

const availableDepartments = computed(() => {
    if (!filters.value.facultyid) return allDepartments.value;
    const selectedFac = faculties.value.find(f => f.facultyid === filters.value.facultyid);
    if (selectedFac) { return allDepartments.value.filter(d => d.facultyid === selectedFac.facultyid); }
    return allDepartments.value;
});

const filteredStudents = computed(() => {
    return students.value.filter(s => {
        const acadYear = s.acadyear ? s.acadyear.toString() : '';
        const facId = s.facultyid ? s.facultyid.toString() : ''; 
        const progName = s.programname || '';
        const stdCode = s.studentcode || '';

        const matchYear = !filters.value.year || acadYear.includes(filters.value.year);
        const matchFac = !filters.value.facultyid || facId === filters.value.facultyid.toString();
        const matchProg = !filters.value.program || progName.includes(filters.value.program);
        const matchId = !filters.value.studentId || stdCode.includes(filters.value.studentId);
        
        return matchYear && matchFac && matchProg && matchId;
    });
});

const paginatedPages = computed(() => {
    const pages = []; const itemsPerPage = 10;
    for (let i = 0; i < filteredStudents.value.length; i += itemsPerPage) { pages.push(filteredStudents.value.slice(i, i + itemsPerPage)); }
    return pages;
});

const convertImageToBase64 = async (url) => {
    try {
        const response = await fetch(url); const blob = await response.blob();
        return new Promise((resolve) => { const reader = new FileReader(); reader.onloadend = () => resolve(reader.result); reader.readAsDataURL(blob); });
    } catch (err) { return ''; }
};

const loadStudentImages = async () => {
    for (const student of students.value) {
        if (!student.studentcode) continue;
        try { student.faceBase64 = await convertImageToBase64(`${apiUrl}/pic/${student.studentcode}.jpg`) || ''; } catch (e) { student.faceBase64 = ''; }
    }
};

const generatePreview = async () => {
    showPreview.value = true;
    await nextTick();
    filteredStudents.value.forEach(student => {
        const barcodeEl = document.querySelector(`#barcode-${student.studentcode}`);
        if (barcodeEl) JsBarcode(`#barcode-${student.studentcode}`, student.studentcode, { format: "CODE128", width: 1.0, height: 30, displayValue: false, margin: 0, lineColor: "#0f172a" });
        const canvasEl = document.getElementById(`qrcode-${student.studentcode}`);
        if (canvasEl) QRCode.toCanvas(canvasEl, student.studentcode, { width: 45, margin: 0, color: { dark: '#0f172a', light: '#ffffff' } }, (error) => {});
    });
};

const downloadPDF = async () => {
    isGeneratingPDF.value = true;
    let facultySuffix = filters.value.facultyid ? `_${filters.value.facultyid.trim().replace(/\s+/g, '_')}` : '_all';
    const images = document.querySelectorAll('#pdf-container img');
    const imagePromises = Array.from(images).map(img => new Promise((resolve) => { if (img.complete) resolve(); else { img.onload = resolve; img.onerror = resolve; }}));
    await Promise.all(imagePromises);
    const element = document.getElementById('pdf-container');
    const options = { margin: 3, filename: `Graduation_ID_Cards${facultySuffix}.pdf`, image: { type: 'jpeg', quality: 0.98 }, html2canvas: { scale: 2, useCORS: true, logging: false }, jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' } };
    await html2pdf().from(element).set(options).save();
    isGeneratingPDF.value = false;
};

// ================= ระบบ PAGINATION สำหรับหน้ารายงาน =================
const REPORT_ROWS_PER_PAGE = 60; 
const currentReportPage = ref(1);

const reportPages = computed(() => {
    if (!allGraduates.value || allGraduates.value.length === 0) return [];
    
    const filtered = allGraduates.value.filter(s => {
        const acadYear = s.acadyear ? s.acadyear.toString() : '';
        const facId = s.facultyid ? s.facultyid.toString() : '';
        const progName = s.programname || '';
        
        const matchYear = !filters.value.year || acadYear.includes(filters.value.year);
        const matchFac = !filters.value.facultyid || facId === filters.value.facultyid.toString();
        const matchProg = !filters.value.program || progName.includes(filters.value.program);
        
        return matchYear && matchFac && matchProg;
    });

    const sorted = [...filtered].sort((a, b) => (a.orderno || 0) - (b.orderno || 0));

    const grouped = sorted.reduce((groups, student) => {
        const levKey = student.levelname || 'ไม่ระบุระดับ'; 
        const facKey = student.facultyname || 'ไม่ระบุสำนักวิชา';
        const degKey = student.programname || 'ไม่ระบุหลักสูตร';
        
        if (!groups[levKey]) groups[levKey] = {};
        if (!groups[levKey][facKey]) groups[levKey][facKey] = {};
        if (!groups[levKey][facKey][degKey]) groups[levKey][facKey][degKey] = [];
        
        groups[levKey][facKey][degKey].push(student);
        return groups;
    }, {});

    const pages = [];
    for (const levKey in grouped) {
        for (const facKey in grouped[levKey]) {
            for (const degKey in grouped[levKey][facKey]) {
                const studentsInDegree = grouped[levKey][facKey][degKey];
                const totalParts = Math.ceil(studentsInDegree.length / REPORT_ROWS_PER_PAGE);
                
                for (let i = 0; i < studentsInDegree.length; i += REPORT_ROWS_PER_PAGE) {
                    pages.push({
                        levelName: levKey, 
                        facultyName: facKey,
                        degreeName: degKey,
                        students: studentsInDegree.slice(i, i + REPORT_ROWS_PER_PAGE),
                        partNumber: Math.floor(i / REPORT_ROWS_PER_PAGE) + 1,
                        totalParts: totalParts
                    });
                }
            }
        }
    }
    return pages;
});

const displayedReportPage = computed(() => {
    if (reportPages.value.length === 0) return null;
    return reportPages.value[currentReportPage.value - 1];
});

const nextReportPage = () => { if (currentReportPage.value < reportPages.value.length) currentReportPage.value++; };
const prevReportPage = () => { if (currentReportPage.value > 1) currentReportPage.value--; };

const downloadReportPDF = async () => {
    isGeneratingReportPDF.value = true;
    
    try {
        const response = await api.get('/graduations/report/pdf', { 
              params: {
                  year: filters.value.year || '2567', 
                  facultyid: filters.value.facultyid || ''
              },
              responseType: 'blob'
          });

        if (response.data.type === 'application/json') {
            const textData = await response.data.text();
            const errorJson = JSON.parse(textData);
            alert(`แจ้งเตือน: ${errorJson.message || 'ไม่พบข้อมูลบัณฑิตตามเงื่อนไขที่ค้นหา'}`);
            isGeneratingReportPDF.value = false;
            return; 
        }
        
        const blob = new Blob([response.data], { type: 'application/pdf' }); 
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        
        link.href = url;
        link.setAttribute('download', `Graduation_Report_${filters.value.year || '2567'}.pdf`);
        document.body.appendChild(link);
        link.click();
        
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
        
    } catch (error) {
        console.error("ดาวน์โหลด PDF ไม่สำเร็จ:", error);
        alert("เกิดข้อผิดพลาดในการดึงไฟล์ PDF จากเซิร์ฟเวอร์");
    } finally {
        isGeneratingReportPDF.value = false;
    }
};

watch(() => filters.value.facultyid, () => { filters.value.program = ''; });

onMounted(async () => {
    await fetchDropdownData();
    await fetchStudents();
    await fetchAllStudents();
    if (students.value.length > 0) { await loadStudentImages(); }
});
</script>

<style scoped>
@media print {
    body { background: white; }
    .a4-page {
        width: 210mm !important;
        min-height: 297mm !important;
        margin: 0 !important;
        box-shadow: none !important;
        page-break-after: always;
    }
}
.a4-page {
    width: 100%; max-width: 210mm; min-height: 297mm;
    background: white; box-sizing: border-box; display: flex; flex-direction: column;
}

.report-layout {
    max-width: 297mm !important; 
    min-height: 210mm !important; 
    padding: 10mm;
    margin: 0 auto;
}

thead { display: table-header-group; }
tr { break-inside: avoid; }
tr { 
    page-break-inside: avoid !important; 
    break-inside: avoid-page !important; 
}

table, th, td {
    border: 1px solid #0f172a !important; 
}

.report-layout {
    box-shadow: none !important;
    background-color: #ffffff !important;
}

@media screen {
    .print-only-section {
        display: none !important; 
    }
}

@media print {
    body * {
        visibility: hidden;
    }
    .print-only-section, .print-only-section * {
        visibility: visible; 
    }
    .print-only-section {
        position: absolute;
        left: 0;
        top: 0;
        width: 100%;
        display: block !important;
    }
    
    @page {
        size: A4 landscape;
        margin: 0; 
    }

    .print-bg-dark { background-color: #1e293b !important; color: white !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    .print-bg-light { background-color: #f1f5f9 !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    .print-bg-gray { background-color: #d1d5db !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    
    .print-table th, .print-table td {
        border: 1px solid #000000 !important;
    }
}

/* Custom Scrollbar for tables */
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

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(15px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in-up {
  animation: fadeInUp 0.4s ease-out forwards;
}
.animate-fade-in {
  animation: fadeInUp 0.3s ease-out forwards;
}
</style>