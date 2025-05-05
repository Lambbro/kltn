<template>
<div class="container">
    <!-- Header -->
    <header class="header">
      <img src="@/assets/img/logo-hou.png" alt="Logo" class="logo"/>
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

    <!-- Main layout -->
    <div class="main-layout">
      <!-- Sidebar -->
      <SidebarManagerPhong class="sidebar" />

      <!-- Main content -->
      <div class="main-content">
        <!-- Filter section -->
        <div class="filter-section">
          <div class="filter-group">
            <label>Trạng thái:</label>
            <select v-model="selectedStatus" @change="fetchProjects">
              <option value="">Tất cả</option>
              <option value="1">Đang thực hiện</option>
              <option value="2">Đã hoàn thành</option>
              <option value="3">Đã nghiệm thu</option>
              <option value="4">Đã hủy</option>
            </select>
          </div>
        </div>

        <!-- Projects table -->
        <div class="projects-table">
          <div v-if="loading" class="loading">Đang tải dữ liệu...</div>
          <div v-else-if="error" class="error">{{ error }}</div>
          <div v-else-if="projects.length === 0" class="no-data">Không có đề tài nào</div>
          <table v-else>
            <thead>
              <tr>
                <th>Mã đề tài</th>
                <th>Tên đề tài</th>
                <th>Chủ nhiệm</th>
                <th>Thời gian bắt đầu</th>
                <th>Thời gian kết thúc</th>
                <th>Trạng thái</th>
                <th>Thao tác</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="project in projects" :key="project.ma_de_tai">
                <td>{{ project.ma_de_tai }}</td>
                <td>{{ project.ten_de_tai }}</td>
                <td>{{ project.chu_nhiem?.ten_gv || 'Chưa có' }}</td>
                <td>{{ formatDate(project.tg_bat_dau) }}</td>
                <td>{{ formatDate(project.tg_ket_thuc) }}</td>
                <td>
                  <span :class="getStatusClass(project.trang_thai)">
                    {{ getStatusText(project.trang_thai) }}
                  </span>
                </td>
                <td>
                  <button class="view-btn" @click="viewProjectDetails(project)">
                    Xem chi tiết
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import api from '@/config/api';

import SidebarManagerPhong from '@/components/SidebarMangerPhong.vue';
import Footer from '@/components/Footer.vue';
// Khi ứng dụng chạy, kiểm tra trạng thái đăng nhập
onMounted(() => {
  authStore.loadUserFromStorage();
  fetchProjects();
});
// Sử dụng store để lấy thông tin đăng nhập
const router = useRouter();
const authStore = useAuthStore();

const { isAuthenticated, storedEmail, logout } = authStore;

// State variables
const projects = ref([]);
const loading = ref(false);
const error = ref(null);
const selectedStatus = ref('');

// Hàm đăng xuất
const handleLogout = () => {
  logout();  // Xóa token khỏi localStorage
  router.push('/login'); // Quay về trang chủ sau khi đăng xuất
};

// Hàm lấy danh sách đề tài
const fetchProjects = async () => {
  try {
    loading.value = true;
    error.value = null;
    
    const params = {};
    if (selectedStatus.value) {
      params.trang_thai = parseInt(selectedStatus.value);
    }

    const response = await api.get('detai_gv/de_tai', { params });
    projects.value = response.data;
  } catch (err) {
    console.error('Error fetching projects:', err);
    error.value = 'Không thể tải danh sách đề tài. Vui lòng thử lại sau.';
  } finally {
    loading.value = false;
  }
};

// Hàm chuyển đổi trạng thái
const getStatusText = (trangThai) => {
  const trangThaiMap = {
    1: 'Đang thực hiện',
    2: 'Đã hoàn thành',
    3: 'Đã nghiệm thu',
    4: 'Đã hủy'
  };
  return trangThaiMap[trangThai] || 'Không xác định';
};

const getStatusClass = (trangThai) => {
  const classMap = {
    1: 'status-ongoing',
    2: 'status-completed',
    3: 'status-accepted',
    4: 'status-cancelled'
  };
  return classMap[trangThai] || '';
};

// Hàm định dạng ngày
const formatDate = (dateString) => {
  if (!dateString) return 'Chưa có';
  const date = new Date(dateString);
  return date.toLocaleDateString('vi-VN');
};

// Hàm xem chi tiết đề tài
const viewProjectDetails = (project) => {
  router.push({
    path: '/manager/project-details',
    query: { id: project.ma_de_tai }
  });
};
</script>

<style scoped>
/* Container */
.container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  overflow-y: auto;
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
  height: 80px;
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

/* Main layout */
.main-layout {
  display: flex;
  margin-top: 80px;
  min-height: calc(100vh - 80px - 100px);
}

/* Sidebar */
.sidebar {
  width: 220px;
  background: #0082c6;
  position: fixed;
  top: 80px;
  left: 0;
  height: calc(100vh - 60px);
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  transition: left 0.3s ease;
  z-index: 1000;
}

/* Main Content */
.main-content {
  flex: 1;
  margin-left: 240px;
  margin-top: 20px;
  padding: 20px 40px;
  box-sizing: border-box;
  background: #f4f7fa;
  transition: all 0.3s ease;
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

/* Filter section */
.filter-section {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.filter-group label {
  font-weight: 600;
  color: #1a3c5e;
  font-size: 1.1rem;
}

.filter-group select {
  padding: 0.75rem 1rem;
  border: 2px solid #e6f2ff;
  border-radius: 8px;
  min-width: 250px;
  font-size: 1rem;
  color: #1a3c5e;
  background-color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-group select:hover {
  border-color: #0082c6;
}

.filter-group select:focus {
  outline: none;
  border-color: #0082c6;
  box-shadow: 0 0 0 3px rgba(0, 130, 198, 0.1);
}

/* Projects table */
.projects-table {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #d1dbe3;
}

th {
  background: #0082c6;
  color: white;
  font-weight: 600;
  font-size: 14px;
}

td {
  background: white;
  font-size: 14px;
}

tr:hover {
  background: #f9fafb;
}

/* Status badges */
.status-badge {
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.9rem;
  display: inline-block;
  font-weight: 500;
}

.status-ongoing {
  background: #dbeafe;
  color: #1e40af;
}

.status-completed {
  background: #dcfce7;
  color: #166534;
}

.status-accepted {
  background: #f0fdf4;
  color: #065f46;
}

.status-cancelled {
  background: #fee2e2;
  color: #991b1b;
}

/* View button */
.view-btn {
  background-color: #0082c6;
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
  box-shadow: 0 2px 4px rgba(0, 130, 198, 0.2);
}

.view-btn:hover {
  background-color: #0069a3;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(0, 130, 198, 0.3);
}

.view-btn:active {
  transform: translateY(0);
  box-shadow: 0 1px 2px rgba(0, 130, 198, 0.2);
}

/* Status messages */
.loading, .error, .no-data {
  text-align: center;
  padding: 3rem;
  color: #666;
  font-size: 1.1rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.error {
  color: #ef4444;
}

/* Footer */
.footer {
  background: #0082c6;
  color: white;
  padding: 1rem;
  text-align: center;
  height: 100px;
}

/* Responsive styles */
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

  .header h1 {
    font-size: 1.1rem;
  }
}

@media (max-width: 768px) {
  .header {
    padding: 0 10px;
    height: 60px;
    justify-content: center;
    align-items: center;
  }

  .logo {
    width: 30px;
    margin-right: 5px;
    margin-left: 40px;
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
    left: -200px;
    top: 60px;
    height: calc(100vh - 60px);
  }

  .sidebar-open {
    left: 0;
  }

  .main-content {
    margin-left: 0;
    margin-top: 20px;
    padding: 15px;
  }

  .filter-group {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .filter-group select {
    width: 100%;
  }
}

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
  }

  .filter-section {
    padding: 1rem;
  }

  .filter-group label {
    font-size: 14px;
  }

  .filter-group select {
    padding: 6px;
    font-size: 13px;
  }

  th, td {
    padding: 8px;
    font-size: 13px;
  }

  .view-btn {
    padding: 6px 12px;
    font-size: 13px;
  }
}
</style>