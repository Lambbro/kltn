<template>
  <div class="container">
    <header class="header">
      <button v-if="isMobile" class="sidebar-toggle" @click="toggleSidebar">☰</button>
      <img src="@/assets/img/logo-hou.png" alt="Logo" class="logo" />
      <h1>HỆ THỐNG QUẢN LÝ NGHIÊN CỨU KHOA HỌC</h1>
      <!-- Hiển thị trạng thái đăng nhập -->
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
    <div class="main-layout">
          <SidebarManagerPhong
            class="sidebar"
            :is-open="isSidebarOpen"
            @toggle="toggleSidebar"
          />
        <!-- Main content -->
    <div class="main-content" :class="{ 'main-content-shifted': isSidebarOpen && !isMobile }">
      <div class="content">
        <h2>Trang quản lý danh sách khoa trường Đại học Mở Hà Nội</h2>
        <p v-if="loadingKhoas" class="loading-text">Đang tải dữ liệu...</p>
        <p v-else-if="errorKhoas" class="error-text">{{ errorKhoas }}</p>

        <!-- Nút bật/tắt bộ lọc -->
        <div class="filter-search">
          <button class="filter-btn" @click="showFilter = !showFilter">
            {{ showFilter ? 'Ẩn bộ lọc' : 'Hiện bộ lọc' }}
          </button>
        </div>

        <!-- Form bộ lọc -->
        <div v-if="showFilter" class="filter-form">
          <div class="filter-row">
            <div>
              <label class="label">Mã khoa</label>
              <input type="text" v-model="filterCriteria.ma_khoa" class="input-field" />
            </div>
            <div>
              <label class="label">Tên khoa</label>
              <input type="text" v-model="filterCriteria.ten_khoa" class="input-field" />
            </div>
          </div>
        </div>

        <!-- Bảng danh sách khoa -->
        <div v-if="!loadingKhoas && !errorKhoas" class="khoa-table-container">
          <table class="khoa-table">
            <thead>
              <tr>
                <th>STT</th>
                <th>Mã Khoa</th>
                <th>Tên Khoa</th>
                <th>Địa Chỉ</th>
                <th>Hành Động</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(khoa, index) in filteredKhoas" :key="khoa.ma_khoa">
                <td>{{ index + 1 }}</td>
                <td>{{ khoa.ma_khoa }}</td>
                <td>{{ khoa.ten_khoa }}</td>
                <td>{{ khoa.dia_chi }}</td>
                <td>
                  <button class="action-btn" @click="editKhoa(khoa)">Sửa</button>
                  <button class="action-btn" @click="deleteKhoa(khoa.ma_khoa)">Xóa</button>
                </td>
              </tr>
              <tr v-if="filteredKhoas.length === 0">
                <td colspan="5">Không có dữ liệu phù hợp</td>
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
import SidebarManagerPhong from '@/components/SidebarMangerPhong.vue';
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

// Trạng thái dữ liệu khoa
const khoas = ref([]);
const loadingKhoas = ref(false);
const errorKhoas = ref('');

onMounted(() => {
  authStore.loadUserFromStorage();
  fetchKhoas();
});

const showFilter = ref(false);
const filterCriteria = ref({
  ma_khoa: '',
  ten_khoa: '',
});

function normalizeString(str) {
  return str
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/\s+/g, ' ')
    .trim();
}

const filteredKhoas = computed(() => {
  return khoas.value.filter((khoa) => {
    const normalizedMaKhoa = normalizeString(khoa.ma_khoa);
    const normalizedTenKhoa = normalizeString(khoa.ten_khoa);
    const normalizedFilterMaKhoa = normalizeString(filterCriteria.value.ma_khoa);
    const normalizedFilterTenKhoa = normalizeString(filterCriteria.value.ten_khoa);

    const maKhoaMatch = !filterCriteria.value.ma_khoa || normalizedMaKhoa.includes(normalizedFilterMaKhoa);
    const tenKhoaMatch = !filterCriteria.value.ten_khoa || normalizedTenKhoa.includes(normalizedFilterTenKhoa);

    return maKhoaMatch && tenKhoaMatch;
  });
});

// Gọi API lấy danh sách khoa
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
        errorMessage = 'Không có quyền truy cập';
      } else if (error.response.status === 404) {
        errorMessage = 'Endpoint không tồn tại';
      } else if (error.response.status === 500) {
        errorMessage = 'Lỗi server, vui lòng thử lại sau';
      }
    } else if (error.request) {
      errorMessage = 'Không thể kết nối đến server';
      console.error('Không nhận được phản hồi từ server');
    } else {
      console.error('Lỗi khác:', error.message);
    }
    errorKhoas.value = errorMessage;
    console.error('Lỗi khi lấy danh sách khoa:', error);
  } finally {
    loadingKhoas.value = false;
  }
}

// Đăng xuất
function handleLogout() {
  logout();
  router.push('/login');
}

// Sửa khoa
function editKhoa(khoa) {
  console.log('Chỉnh sửa:', khoa);
}

// Xóa khoa
async function deleteKhoa(ma_khoa) {
  const confirmDelete = confirm(`Bạn có chắc xóa khoa có mã: ${ma_khoa}?`);
  if (!confirmDelete) return;

  try {
    await api.delete(`phongkhdn/khoa/delete/${ma_khoa}/`);
    khoas.value = khoas.value.filter((khoa) => khoa.ma_khoa !== ma_khoa);
  } catch (error) {
    let errorMessage = 'Xóa khoa thất bại';
    if (error.response) {
      console.error('Mã lỗi HTTP:', error.response.status);
      console.error('Chi tiết lỗi:', error.response.data);
      if (error.response.status === 401) {
        errorMessage = 'Phiên đăng nhập hết hạn';
        authStore.logout();
        router.push('/login');
      } else if (error.response.status === 404) {
        errorMessage = 'Khoa không tồn tại';
      } else if (error.response.status === 500) {
        errorMessage = 'Lỗi server, vui lòng thử lại sau';
      }
    } else if (error.request) {
      errorMessage = 'Không thể kết nối đến server';
    }
    alert(errorMessage);
    console.error('Lỗi khi xóa khoa:', error);
  }
}
</script>
<style scoped>
.container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  overflow-y: auto;
  background: #f8fafc;
}

.container::-webkit-scrollbar {
  width: 6px;
}

.container::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 10px;
}

.container::-webkit-scrollbar-thumb {
  background: #0082c6;
  border-radius: 10px;
}

.container::-webkit-scrollbar-thumb:hover {
  background: #0069a3;
}

/* Overlay cho mobile */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(2px);
  z-index: 999;
}

/* Header */
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 70px;
  z-index: 1000;
  padding: 0 24px;
  box-sizing: border-box;
}

.logo {
  width: 45px;
  margin-right: 12px;
  transition: transform 0.3s ease;
}

.logo:hover {
  transform: scale(1.05);
}

.header h1 {
  font-size: 1.3rem;
  margin: 0;
  flex-grow: 1;
  text-align: center;
  color: #0082c6;
  font-weight: 600;
}

.auth-buttons {
  display: flex;
  gap: 0.8rem;
  align-items: center;
}

.auth-buttons span {
  font-size: 0.95rem;
  color: #4b5563;
}

.auth-buttons button {
  padding: 0.5rem 1rem;
  background: #0082c6;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.auth-buttons button:hover {
  background: #0069a3;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.sidebar-toggle {
  display: none;
  background: #0082c6;
  color: white;
  border: none;
  padding: 0.6rem 1rem;
  font-size: 1.2rem;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.sidebar-toggle:hover {
  background: #0069a3;
  transform: translateY(-1px);
}

/* Main layout */
.main-layout {
  display: flex;
  margin-top: 70px;
  min-height: calc(100vh - 70px);
  width: 100%;
  box-sizing: border-box;
}

/* Sidebar */
.sidebar {
  width: 250px;
  background: #0082c6;
  position: fixed;
  top: 70px;
  left: 0;
  height: calc(100vh - 70px);
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
  transition: left 0.3s ease;
  z-index: 1000;
}

/* Main Content */
.main-content {
  flex: 1;
  width: 100%;
  margin-left: 270px; /* 250px (sidebar width) + 20px (margin) */
  padding: 20px;
  box-sizing: border-box;
  overflow-y: auto;
  background: #f8fafc;
  transition: margin-left 0.3s ease;
}

/* Content */
.content {
  background-color: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.content:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.1);
}

/* Status Messages */
.loading-text {
  color: #4b5563;
  font-size: 1rem;
  text-align: center;
  padding: 1rem;
}

.error-text {
  color: #ef4444;
  font-size: 1rem;
  text-align: center;
  padding: 1rem;
  background: #fee2e2;
  border-radius: 8px;
  margin: 1rem 0;
}

/* Filter search */
.filter-search {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
}

.filter-btn {
  background-color: #0082c6;
  color: white;
  padding: 10px 24px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
}

.filter-btn:hover {
  background-color: #0069a3;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Filter form */
.filter-form {
  border: 1px solid #e2e8f0;
  padding: 20px;
  border-radius: 12px;
  background: white;
  margin-bottom: 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.filter-row > div {
  flex: 1 1 250px;
}

.filter-row label.label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #1e293b;
  font-size: 0.95rem;
}

.filter-row input.input-field {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.95rem;
  background-color: #f8fafc;
  transition: all 0.3s ease;
}

.filter-row input.input-field:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
  background-color: white;
  outline: none;
}

/* Table */
.khoa-table-container {
  background-color: white;
  border-radius: 16px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.khoa-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  margin-top: 1rem;
}

.khoa-table th,
.khoa-table td {
  padding: 16px;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
}

.khoa-table th {
  background: #0082c6;
  color: white;
  font-weight: 600;
  font-size: 0.95rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.khoa-table td {
  background: white;
  font-size: 0.95rem;
  color: #4b5563;
}

.khoa-table tr:hover {
  background: #f8fafc;
}

.khoa-table tr:last-child td {
  border-bottom: none;
}

.action-btn {
  background-color: #0082c6;
  color: white;
  padding: 8px 16px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  margin-right: 8px;
  transition: all 0.3s ease;
}

.action-btn:hover {
  background-color: #0069a3;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Footer */
.footer {
  background: #0082c6;
  color: white;
  padding: 1rem;
  text-align: center;
  height: 60px; /* Chiều cao cố định */
}

/* Responsive */
@media (max-width: 768px) {
  .sidebar-toggle {
    display: flex;
  }

  .header {
    padding: 0 16px;
    height: 60px;
  }

  .logo {
    width: 35px;
    margin-right: 8px;
    margin-left: 40px;
  }

  .header h1 {
    font-size: 1.1rem;
  }

  .auth-buttons {
    gap: 0.5rem;
  }

  .auth-buttons span {
    font-size: 0.85rem;
  }

  .auth-buttons button {
    padding: 0.4rem 0.8rem;
    font-size: 0.85rem;
  }

  .sidebar {
    width: 250px;
    left: -250px;
    top: 70px;
    height: calc(100vh - 70px);
  }

  .main-content {
    margin-left: 0;
    padding: 20px;
    margin-top: 70px;
  }

  .content {
    padding: 16px;
  }

  .filter-row {
    flex-direction: column;
    gap: 16px;
  }

  .filter-row > div {
    flex: 1 1 auto;
  }

  .khoa-table th,
  .khoa-table td {
    padding: 12px;
    font-size: 0.9rem;
  }

  .action-btn {
    padding: 6px 12px;
    font-size: 0.85rem;
  }

  .sidebar-open {
    left: 0;
  }

  .main-content-shifted {
    margin-left: 20px;
  }
}

@media (max-width: 480px) {
  .header h1 {
    font-size: 1rem;
  }

  .logo {
    width: 30px;
    margin-left: 35px;
  }

  .auth-buttons button {
    padding: 0.3rem 0.6rem;
    font-size: 0.8rem;
  }

  .content {
    padding: 12px;
  }

  .filter-btn {
    width: 100%;
    padding: 8px 16px;
  }

  .filter-form {
    padding: 16px;
  }

  .filter-row label.label {
    font-size: 0.9rem;
  }

  .filter-row input.input-field {
    padding: 8px;
    font-size: 0.9rem;
  }

  .khoa-table th,
  .khoa-table td {
    padding: 10px;
    font-size: 0.85rem;
  }

  .action-btn {
    padding: 6px 10px;
    font-size: 0.8rem;
  }
}
</style>