<template>
  <div class="container">
    <!-- Header -->
    <header class="header">
      <button v-if="isMobile" class="sidebar-toggle" @click="toggleSidebar">☰</button>
      <img src="@/assets/img/logo-hou.png" alt="Logo" class="logo" />
      <h1>HỆ THỐNG QUẢN LÝ NGHIÊN CỨU KHOA HỌC</h1>
      <div class="auth-buttons">
        <template v-if="isAuthenticated">
          <span>{{ storedEmail }}</span>
          <button @click="handleLogout">Đăng xuất</button>
        </template>
        <template v-else>
          <button @click="$router.push('/login')">Đăng nhập</button>
        </template>
      </div>
    </header>

    <!-- Overlay khi sidebar mở trên mobile -->
    <div v-if="isSidebarOpen && isMobile" class="overlay" @click="toggleSidebar"></div>

    <!-- Main layout -->
    <div class="main-layout">
      <SidebarManagerPhong
        v-if="authStore.user?.quyen_han === 1"
        class="sidebar"
        :class="{ 'sidebar-open': isSidebarOpen }"
        :is-open="isSidebarOpen"
        @toggle="toggleSidebar"
      />
      <SidebarManagerToNCKH
        v-else
        class="sidebar"
        :class="{ 'sidebar-open': isSidebarOpen }"
        :is-open="isSidebarOpen"
        @toggle="toggleSidebar"
      />
      <div class="main-content" :class="{ 'main-content-shifted': isSidebarOpen && !isMobile }">
        <div class="content">
          <h2>Đây là trang Quản lý danh sách sinh viên</h2>

          <p v-if="loadingStudents || loadingKhoas" class="loading-text">Đang tải dữ liệu...</p>
          <p v-else-if="errorStudents || errorKhoas" class="error-text">
            {{ errorStudents || errorKhoas }}
          </p>

          <!-- Nút bật/tắt bộ lọc -->
          <div class="filter-search">
            <button class="filter-btn" @click="showFilter = !showFilter">
              {{ showFilter ? 'Ẩn bộ lọc' : 'Hiện bộ lọc' }}
            </button>
          </div>

          <!-- Bộ lọc -->
          <div v-if="showFilter" class="filter-form">
            <div class="filter-row">
              <div>
                <label class="label">Mã sinh viên</label>
                <input type="text" v-model="filterCriteria.ma_sv" class="input-field" />
              </div>
              <div>
                <label class="label">Tên sinh viên</label>
                <input type="text" v-model="filterCriteria.ten_sv" class="input-field" />
              </div>
              <div>
                <label class="label">Lớp hành chính</label>
                <input type="text" v-model="filterCriteria.lop_hc" class="input-field" />
              </div>
              <div>
                <label class="label">Khoa</label>
                <input type="text" v-model="filterCriteria.khoa" class="input-field" />
              </div>
            </div>
          </div>

          <!-- Bảng danh sách sinh viên -->
          <div v-if="!loadingStudents && !errorStudents" class="student-table-container">
            <table class="student-table">
              <thead>
                <tr>
                  <th>STT</th>
                  <th>Mã SV</th>
                  <th>Tên SV</th>
                  <th>CCCD</th>
                  <th>Giới Tính</th>
                  <th>Ngày Sinh</th>
                  <th>Quê Quán</th>
                  <th>SĐT</th>
                  <th>Lớp HC</th>
                  <th>Khóa Học</th>
                  <th>Email</th>
                  <th>Tên Khoa</th>
                  <th>Hành Động</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(student, index) in filteredStudents" :key="student.ma_sv">
                  <td>{{ index + 1 }}</td>
                  <td>{{ student.ma_sv }}</td>
                  <td>{{ student.ten_sv }}</td>
                  <td>{{ student.cccd }}</td>
                  <td>{{ student.gioi_tinh ? 'Nam' : 'Nữ' }}</td>
                  <td>{{ student.ngay_sinh }}</td>
                  <td>{{ student.que_quan }}</td>
                  <td>{{ student.sdt }}</td>
                  <td>{{ student.lop_hc }}</td>
                  <td>{{ student.khoa_hoc }}</td>
                  <td>{{ student.email }}</td>
                  <td>{{ getTenKhoa(student.ma_khoa) }}</td>
                  <td>
                    <button class="delete-btn" @click="deleteStudent(student.ma_sv)">
                      <i class="fas fa-trash"></i> Xóa
                    </button>
                  </td>
                </tr>
                <tr v-if="filteredStudents.length === 0">
                  <td colspan="13">Không có dữ liệu phù hợp</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import SidebarManagerToNCKH from '@/components/SidebarManagerToNCKH.vue';
import SidebarManagerPhong from '@/components/SidebarMangerPhong.vue';
import Footer from '@/components/Footer.vue';
import api from '@/config/api';

const router = useRouter();
const authStore = useAuthStore();
const { isAuthenticated, storedEmail, logout } = authStore;

// Trạng thái sidebar
const isSidebarOpen = ref(false);
const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value;
};

// Kiểm tra màn hình mobile
const isMobile = ref(window.innerWidth <= 768);
window.addEventListener('resize', () => {
  isMobile.value = window.innerWidth <= 768;
  if (isMobile.value && isSidebarOpen.value) {
    isSidebarOpen.value = false; // Đóng sidebar khi resize về mobile
  }
});

const khoas = ref([]);
const loadingKhoas = ref(false);
const errorKhoas = ref('');
const students = ref([]);
const loadingStudents = ref(false);
const errorStudents = ref('');

onMounted(() => {
  authStore.loadUserFromStorage();
  fetchKhoas();
  fetchStudents();
});

const showFilter = ref(false);
const filterCriteria = ref({
  ma_sv: '',
  ten_sv: '',
  lop_hc: '',
  khoa: '',
});

// Chuẩn hóa chuỗi
function normalizeString(str) {
  if (!str) return '';
  return str
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/\s+/g, ' ')
    .trim();
}

// Tìm kiếm gần đúng
function fuzzySearch(text, searchTerm) {
  if (!searchTerm) return true;
  
  const normalizedText = normalizeString(text);
  const normalizedSearch = normalizeString(searchTerm);
  
  // Tách các từ trong chuỗi tìm kiếm
  const searchWords = normalizedSearch.split(/\s+/);
  
  // Kiểm tra xem tất cả các từ có xuất hiện trong text không
  return searchWords.every(word => normalizedText.includes(word));
}

// Ánh xạ mã khoa sang tên khoa
const khoaMap = computed(() => {
  const map = {};
  khoas.value.forEach((khoa) => {
    map[khoa.ma_khoa] = khoa.ten_khoa;
  });
  return map;
});

// Lấy tên khoa từ mã khoa
function getTenKhoa(ma_khoa) {
  return khoaMap.value[ma_khoa] || ma_khoa || 'Không xác định';
}

const filteredStudents = computed(() => {
  return students.value.filter((student) => {
    const maSvMatch = fuzzySearch(student.ma_sv, filterCriteria.value.ma_sv);
    const tenSvMatch = fuzzySearch(student.ten_sv, filterCriteria.value.ten_sv);
    const lopHcMatch = fuzzySearch(student.lop_hc, filterCriteria.value.lop_hc);
    const khoaMatch = fuzzySearch(getTenKhoa(student.ma_khoa), filterCriteria.value.khoa);

    return maSvMatch && tenSvMatch && lopHcMatch && khoaMatch;
  });
});

async function fetchKhoas() {
  try {
    loadingKhoas.value = true;
    errorKhoas.value = '';

    const response = await api.get('phongkhdn/khoa/');
    const data = response.data;

    if (!Array.isArray(data)) {
      throw new Error('Dữ liệu khoa không hợp lệ');
    }

    khoas.value = data;
  } catch (error) {
    let errorMessage = 'Không thể lấy danh sách khoa';
    if (error.response) {
      console.error('Mã lỗi HTTP:', error.response.status);
      console.error('Chi tiết lỗi:', error.response.data);
      if (error.response.status === 401) {
        errorMessage = 'Phiên đăng nhập hết hạn';
        authStore.logout();
        router.push('/login');
      } else if (error.response.status === 403) {
        errorMessage = 'Bạn không có quyền truy cập danh sách khoa';
      } else if (error.response.status === 404) {
        errorMessage = 'Endpoint khoa không tồn tại';
      } else if (error.response.status === 500) {
        errorMessage = 'Lỗi server, vui lòng thử lại sau';
      }
    } else if (error.request) {
      errorMessage = 'Không thể kết nối đến server';
    }
    errorKhoas.value = errorMessage;
    console.error('Lỗi khi lấy danh sách khoa:', error);
  } finally {
    loadingKhoas.value = false;
  }
}

async function fetchStudents() {
  try {
    loadingStudents.value = true;
    errorStudents.value = '';
    
    let response;

    // Lấy danh sách sinh viên theo quyền hạn
    if (authStore.user?.quyen_han === 1) {
      response = await api.get('phongkhdn/sv/');
    } else {
      response = await api.get('tonckh/sinh-vien/');
    }
    const data = response.data;
    if (!Array.isArray(data)) {
      throw new Error('Dữ liệu sinh viên không hợp lệ');
    }

    if (data.length === 0) {
      errorStudents.value = 'Bạn không có quyền xem danh sách sinh viên';
    }

    students.value = data;

  } catch (error) {
    let errorMessage = error.message || 'Không thể lấy danh sách sinh viên';

    if (error.response) {
      console.error('Mã lỗi HTTP:', error.response.status);
      console.error('Chi tiết lỗi:', error.response.data);
      switch (error.response.status) {
        case 401:
          errorMessage = 'Phiên đăng nhập hết hạn';
          authStore.logout();
          router.push('/login');
          break;
        case 403:
          errorMessage = 'Bạn không có quyền truy cập danh sách sinh viên';
          break;
        case 404:
          errorMessage = 'Endpoint sinh viên không tồn tại';
          break;
        case 500:
          errorMessage = 'Lỗi server, vui lòng thử lại sau';
          break;
      }
    } else if (error.request) {
      errorMessage = 'Không thể kết nối đến server';
    }

    errorStudents.value = errorMessage;
    students.value = [];
    console.error('Lỗi khi lấy danh sách sinh viên:', error);

  } finally {
    loadingStudents.value = false;
  }
}

function handleLogout() {
  logout();
  router.push('/login');
}

function editStudent(student) {
  console.log('Chỉnh sửa:', student);
  // Triển khai chuyển hướng đến trang chỉnh sửa
  // router.push(`/edit-sv/${student.ma_sv}`);
}

async function deleteStudent(ma_sv) {
  const confirmDelete = confirm(`Bạn có chắc xóa SV có mã: ${ma_sv}?`);
  if (!confirmDelete) return;
  
  try {
    // Xác định endpoint dựa trên quyền hạn
    const endpoint =`phongkhdn/sv/delete/${ma_sv}`
    await api.delete(endpoint);
    students.value = students.value.filter((sv) => sv.ma_sv !== ma_sv);
    alert('Xóa sinh viên thành công');
  } catch (error) {
    let errorMessage = 'Xóa sinh viên thất bại';
    
    if (error.response) {
      console.error('Mã lỗi HTTP:', error.response.status);
      console.error('Chi tiết lỗi:', error.response.data);
      
      switch (error.response.status) {
        case 401:
          errorMessage = 'Phiên đăng nhập hết hạn';
          authStore.logout();
          router.push('/login');
          break;
        case 403:
          errorMessage = 'Bạn không có quyền xóa sinh viên';
          break;
        case 404:
          errorMessage = 'Sinh viên không tồn tại';
          break;
        case 500:
          errorMessage = 'Lỗi server, vui lòng thử lại sau';
          break;
        default:
          errorMessage = error.response.data?.message || 'Có lỗi xảy ra khi xóa sinh viên';
      }
    } else if (error.request) {
      errorMessage = 'Không thể kết nối đến server';
    }
    
    alert(errorMessage);
    console.error('Lỗi khi xóa sinh viên:', error);
  }
}
</script>

<style scoped>
/* Container */
.container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  overflow-x: auto;
}

.container::-webkit-scrollbar {
  width: 5px;
}

.container::-webkit-scrollbar-track {
  background: #e6eef5;
  border-radius: 10px;
}

.container::-webkit-scrollbar-thumb {
  background: #1e88e5;
  border-radius: 10px;
}

.container::-webkit-scrollbar-thumb:hover {
  background: #1565c0;
}

/* Overlay cho mobile */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 999; /* Dưới sidebar */
}

/* Header */
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: white;
  border-bottom: 1px solid #ccc;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 80px; /* Chiều cao cố định */
  z-index: 1000;
  padding: 10px 20px 10px 70px;
  box-sizing: border-box;
}

.logo {
  width: 50px;
  margin-right: 2rem;
  margin-top: 2rem;
}

.header h1 {
  font-size: 1.2rem;
  margin: 0;
  flex-grow: 1;
  text-align: center;
  color: #0082c6;
}

.auth-buttons {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.auth-buttons span {
  font-size: 0.9rem;
}

.auth-buttons button {
  padding: 0.4rem 0.8rem;
  background: #0082c6;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  font-size: 0.9rem;
}

.auth-buttons button:hover {
  background: #0069a3;
}

.sidebar-toggle {
  display: none; /* Ẩn mặc định trên laptop */
  background: #0082c6;
  color: white;
  border: none;
  padding: 0.5rem 0.8rem;
  font-size: 1.2rem;
  cursor: pointer;
  border-radius: 5px;
}

/* Main layout */
.main-layout {
  display: flex;
  margin-top: 80px; /* Khoảng cách với header cố định */
  min-height: calc(100vh - 80px - 100px); /* Trừ header và footer */
}

/* Sidebar */
.sidebar {
  width: 220px;
  background: #0082c6;
  position: fixed;
  top: 80px; /* Bắt đầu dưới header */
  left: 0;
  height: calc(100vh - 60px); /* Trừ header */
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  transition: left 0.3s ease;
  z-index: 1000;
}

/* Main Content */
.main-content {
  flex: 1;
  margin-left: 240px; /* 220px (chiều rộng sidebar) + 20px margin */
  margin-top: 20px; /* Khoảng cách với header */
  padding: 20px 40px;
  box-sizing: border-box;
  background: #f4f7fa;
  transition: all 0.3s ease;
}

.main-content-shifted {
  margin-left: 240px;
}

/* Content */
.content {
  background-color: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.content:hover {
  transform: translateY(-2px);
}

/* Status Messages */
.loading-text {
  color: #4b5563;
  font-size: 1.1rem;
}

.error-text {
  color: #ef4444;
  font-size: 1.1rem;
}

/* Filter search */
.filter-search {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.filter-btn {
  background-color: #0082c6;
  color: white;
  padding: 8px 20px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s;
  font-size: 0.9rem;
}

.filter-btn:hover {
  background-color: #0069a3;
}

/* Filter form */
.filter-form {
  border: 1px solid #d1dbe3;
  padding: 15px;
  border-radius: 10px;
  background: white;
  margin-bottom: 20px;
  position: sticky;
  top: 100px; /* Khoảng cách với header */
  z-index: 100;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.filter-row > div {
  flex: 1 1 200px;
}

.filter-row label.label {
  display: block;
  margin-bottom: 5px;
  font-weight: 600;
  color: #1a3c5e;
  font-size: 16px;
}

.filter-row input.input-field {
  width: 100%;
  padding: 8px;
  border: 1px solid #d1dbe3;
  border-radius: 6px;
  font-size: 14px;
  background-color: #f9fafb;
  transition: border-color 0.3s, box-shadow 0.3s, background-color 0.3s;
}

.filter-row input.input-field:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2);
  background-color: white;
  outline: none;
}

/* Table */
.student-table-container {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow-x: auto;
  width: 100%;
}

.student-table-container::-webkit-scrollbar {
  height: 8px;
}

.student-table-container::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 10px;
}

.student-table-container::-webkit-scrollbar-thumb {
  background: #2563eb;
  border-radius: 10px;
}

.student-table-container::-webkit-scrollbar-thumb:hover {
  background: #1d4ed8;
}

.student-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
  min-width: 1200px; /* Đảm bảo bảng không bị co lại quá mức */
}

.student-table th,
.student-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #d1dbe3;
}

.student-table th {
  background: #0082c6;
  color: white;
  font-weight: 600;
  font-size: 14px;
}

.student-table td {
  background: white;
  font-size: 14px;
}

.student-table tr:hover {
  background: #f9fafb;
}

.action-btn {
  background-color: #0082c6;
  color: white;
  padding: 6px 12px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-size: 13px;
  margin-right: 8px;
  transition: background-color 0.3s;
}

.action-btn:hover {
  background-color: #0069a3;
}

/* Footer */
.footer {
  background: #0082c6;
  color: white;
  padding: 1rem;
  text-align: center;
  height: 100px; /* Chiều cao cố định từ trang trước */
}

/* Responsive */

/* Tablet (≤1024px) */
@media (max-width: 1024px) {
  .header {
    padding: 0 15px;
  }

  .main-content {
    margin-left: 220px;
    padding: 20px;
  }

  .sidebar {
    width: 200px;
  }

  .main-content-shifted {
    margin-left: 200px;
  }

  .header h1 {
    font-size: 1.1rem;
  }

  .student-table {
    min-width: 1000px;
  }
}

/* Mobile (≤768px) */
@media (max-width: 768px) {
  .sidebar-toggle {
    display: block; /* Hiện nút toggle trên mobile */
  }

  .header {
    padding: 0 10px;
    height: 60px;
    justify-content: center;
    align-items: center;
  }

  .logo {
    width: 30px;
    margin-right: 5px;
    margin-left: 40px; /* Khoảng cách với nút toggle */
  }

  .header h1 {
    font-size: 1rem;
    flex-grow: 1;
    text-align: center;
  }

  .auth-buttons {
    margin-right: 0;
    gap: 0.3rem;
  }

  .auth-buttons span {
    font-size: 0.8rem;
  }

  .auth-buttons button {
    padding: 0.3rem 0.6rem;
    font-size: 0.8rem;
  }

  .sidebar {
    width: 200px;
    left: -200px; /* Ẩn sidebar */
    top: 60px;
    height: calc(100vh - 60px);
  }

  .sidebar-open {
    left: 0; /* Hiện sidebar */
  }

  .main-content {
    margin-left: 0;
    margin-top: 20px;
    padding: 15px;
  }

  .main-content-shifted {
    margin-left: 0;
  }

  .overlay ~ .main-content {
    pointer-events: none; /* Vô hiệu hóa thao tác khi sidebar mở */
  }

  .filter-row {
    flex-direction: column;
    gap: 10px;
  }

  .filter-row > div {
    flex: 1 1 auto;
  }

  .delete-btn {
    padding: 6px 12px;
    font-size: 13px;
  }

  .student-table {
    min-width: 800px;
  }
}

/* Small Mobile (≤480px) */
@media (max-width: 480px) {
  .header {
    padding: 0 5px;
  }

  .header h1 {
    font-size: 0.9rem;
  }

  .logo {
    width: 25px;
    margin-left: 35px;
  }

  .auth-buttons button {
    padding: 0.2rem 0.5rem;
    font-size: 0.7rem;
  }

  .sidebar {
    width: 180px;
    left: -180px;
  }

  .sidebar-open {
    left: 0;
  }

  .main-content {
    padding: 10px;
    overflow-x: auto;
  }

  .content {
    overflow-x: auto;
  }

  .filter-btn {
    width: 100%;
    padding: 8px;
  }

  .filter-form {
    padding: 0.5rem;
  }

  .filter-row label.label {
    font-size: 14px;
  }

  .filter-row input.input-field {
    padding: 6px;
    font-size: 13px;
  }

  .student-table th,
  .student-table td {
    padding: 8px;
    font-size: 13px;
  }

  .action-btn {
    padding: 5px 10px;
    font-size: 12px;
  }

  .delete-btn {
    padding: 5px 10px;
    font-size: 12px;
  }

  .student-table {
    min-width: 600px;
  }
}

/* Action Buttons */
.delete-btn {
  background-color: #dc2626;
  color: white;
  padding: 8px 16px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(220, 38, 38, 0.2);
}

.delete-btn:hover {
  background-color: #b91c1c;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(220, 38, 38, 0.3);
}

.delete-btn:active {
  transform: translateY(0);
  box-shadow: 0 1px 2px rgba(220, 38, 38, 0.2);
}

.delete-btn i {
  font-size: 14px;
}
</style>