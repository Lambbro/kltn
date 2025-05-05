<template>
<div class="container">
    <!-- Header -->
    <header class="header">
      <div class="header-left">
        <button v-if="isMobile" class="mobile-menu-btn" @click="toggleSidebar">
          <span class="menu-icon">☰</span>
        </button>
        <img src="@/assets/img/logo-hou.png" alt="Logo" class="logo"/>
      </div>
      <h1>HỆ THỐNG QUẢN LÝ NGHIÊN CỨU KHOA HỌC</h1>
      <div class="auth-buttons">
        <template v-if="isAuthenticated">
          <span class="user-email">{{ storedEmail }}</span>
          <button @click="handleLogout">Đăng xuất</button>
        </template>
        <template v-else>
          <button @click="$router.push('/login')">Đăng nhập</button>
        </template>
      </div>
    </header>

    <!-- Overlay for mobile -->
    <div class="overlay" :class="{ 'overlay-active': isSidebarOpen }" @click="closeSidebar"></div>

    <!-- Main layout -->
    <div class="main-layout">
      <!-- Sidebar -->
      <SidebarManagerToNCKH class="sidebar" :class="{ 'sidebar-open': isSidebarOpen }" />

      <!-- Main content -->
      <div class="main-content" :class="{ 'main-content-shifted': isSidebarOpen && !isMobile }">
        <div class="content">
          <h2>Quản lý đăng ký đề tài sinh viên</h2>

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
                <label class="label">Tên giảng viên</label>
                <input type="text" v-model="filters.ten_gv" class="input-field" />
              </div>
              <div>
                <label class="label">Tên sinh viên</label>
                <input type="text" v-model="filters.ten_sv" class="input-field" />
              </div>
              <div>
                <label class="label">Tên đề tài</label>
                <input type="text" v-model="filters.ten_de_tai" class="input-field" />
              </div>
              <div>
                <label class="label">Đợt thực hiện</label>
                <input type="number" v-model="filters.dot_thuc_hien" class="input-field" />
              </div>
            </div>
          </div>

          <!-- Thông báo trạng thái -->
          <p v-if="loading" class="loading-text">Đang tải dữ liệu...</p>
          <p v-else-if="error" class="error-text">{{ error }}</p>

          <!-- Bảng danh sách đề tài -->
          <div v-if="!loading && !error" class="table-container">
            <!-- Mobile Cards View -->
            <div class="mobile-cards">
              <div v-for="(topic, index) in filteredTopics" :key="topic.ma_nhom" class="mobile-card">
                <div class="card-header">
                  <span class="card-number">#{{ index + 1 }}</span>
                  <span class="card-status" :class="getStatusClass(topic.trang_thai)">
                    {{ formatTrangThai(topic.trang_thai) }}
                  </span>
                </div>
                <div class="card-body">
                  <div class="card-item">
                    <span class="label">Mã GV:</span>
                    <span class="value">{{ topic.ma_gv }}</span>
                  </div>
                  <div class="card-item">
                    <span class="label">Tên GV:</span>
                    <span class="value">{{ topic.ten_gv }}</span>
                  </div>
                  <div class="card-item">
                    <span class="label">Tên đề tài:</span>
                    <span class="value">{{ topic.ten_de_tai }}</span>
                  </div>
                  <div class="card-item">
                    <span class="label">Đợt thực hiện:</span>
                    <span class="value">{{ topic.dot_thuc_hien }}</span>
                  </div>
                  <div class="card-item">
                    <span class="label">Thành viên:</span>
                    <div class="value-list">
                      <div v-for="sv in topic.thanh_vien" :key="sv.ma_sv" class="list-item">
                        {{ sv.ma_sv }} - {{ sv.ten_sv }}
                      </div>
                      <div v-if="!topic.thanh_vien?.length">Không có</div>
                    </div>
                  </div>
                  <div class="card-actions">
                    <button class="action-btn view-btn" @click="handleView(topic)">Xem</button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Desktop Table View -->
            <table class="topic-table desktop-only">
              <thead>
                <tr>
                  <th>STT</th>
                  <th>Mã giảng viên</th>
                  <th>Tên giảng viên</th>
                  <th>Thành viên</th>
                  <th>Tên đề tài</th>
                  <th>Đợt thực hiện</th>
                  <th>Trạng thái</th>
                  <th>Hành động</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(topic, index) in filteredTopics" :key="topic.ma_nhom">
                  <td>{{ index + 1 }}</td>
                  <td>{{ topic.ma_gv }}</td>
                  <td>{{ topic.ten_gv }}</td>
                  <td>
                    <ul>
                      <li v-for="sv in topic.thanh_vien" :key="sv.ma_sv">
                        {{ sv.ma_sv }} - {{ sv.ten_sv }}
                      </li>
                      <li v-if="!topic.thanh_vien?.length">Không có</li>
                    </ul>
                  </td>
                  <td>{{ topic.ten_de_tai }}</td>
                  <td>{{ topic.dot_thuc_hien }}</td>
                  <td>{{ formatTrangThai(topic.trang_thai) }}</td>
                  <td>
                    <button class="action-btn view-btn" @click="handleView(topic)">Xem</button>
                  </td>
                </tr>
                <tr v-if="filteredTopics.length === 0">
                  <td colspan="8">Không có đề tài nào được đăng ký</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <footer class="footer">
      <Footer class="footer-content" />
    </footer>

    <!-- Modal Form -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ isEditing ? 'Chỉnh sửa đề tài' : 'Chi tiết đề tài' }}</h3>
          <button class="close-btn" @click="closeModal">×</button>
        </div>
        
        <form class="modal-form" @submit.prevent="handleSubmit">
          <div class="form-group">
            <label>Mã giảng viên:</label>
            <input type="text" v-model="currentTopic.ma_gv" :disabled="!isEditing" />
          </div>
          
          <div class="form-group">
            <label>Tên giảng viên:</label>
            <input type="text" v-model="currentTopic.ten_gv" :disabled="!isEditing" />
          </div>
          
          <div class="form-group">
            <label>Tên đề tài:</label>
            <input type="text" v-model="currentTopic.ten_de_tai" :disabled="!isEditing" />
          </div>
          
          <div class="form-group">
            <label>Đợt thực hiện:</label>
            <input type="number" v-model="currentTopic.dot_thuc_hien" :disabled="!isEditing" />
          </div>
          
          <div class="form-group">
            <label>Trạng thái:</label>
            <select v-model="currentTopic.trang_thai" :disabled="!isEditing">
              <option value="0">Bị Hủy</option>
              <option value="1">Đang Chờ Duyệt</option>
              <option value="2">Đã Được Duyệt</option>
            </select>
          </div>
          
          <div class="form-group">
            <label>Thành viên:</label>
            <div class="member-list">
              <div v-for="(member, index) in currentTopic.thanh_vien" :key="index" class="member-item">
                <input type="text" v-model="member.ma_sv" :disabled="!isEditing" placeholder="Mã sinh viên" />
                <input type="text" v-model="member.ten_sv" :disabled="!isEditing" placeholder="Tên sinh viên" />
              </div>
            </div>
          </div>
          
          <div class="form-actions" v-if="isEditing">
            <button type="submit" class="save-btn">Lưu</button>
            <button type="button" class="cancel-btn" @click="closeModal">Hủy</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import api from '@/config/api';
import SidebarManagerToNCKH from '@/components/SidebarManagerToNCKH.vue';
import Footer from '@/components/Footer.vue';

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

// Trạng thái dữ liệu
const topicList = ref([]);
const loading = ref(false);
const error = ref('');

// Thêm các ref mới
const showModal = ref(false);
const isEditing = ref(false);
const currentTopic = ref({
  ma_gv: '',
  ten_gv: '',
  ten_de_tai: '',
  dot_thuc_hien: new Date().getFullYear(),
  trang_thai: 0,
  thanh_vien: []
});

// Thêm ref cho bộ lọc
const filters = ref({
  ten_gv: '',
  ten_sv: '',
  ten_de_tai: '',
  dot_thuc_hien: ''
});

// Thêm ref cho trạng thái hiển thị bộ lọc
const showFilter = ref(false);

// Kiểm tra đăng nhập và lấy dữ liệu khi mount
onMounted(() => {
  authStore.loadUserFromStorage();
  fetchTopicList();
});

// Hàm đăng xuất
const handleLogout = () => {
  logout();
  router.push('/login');
};

// Lấy danh sách đề tài từ API
async function fetchTopicList() {
  try {
    loading.value = true;
    error.value = '';
    const response = await api.get('gv/nhomnckh');
    const data = response.data;

    if (!Array.isArray(data)) {
      throw new Error('Dữ liệu đề tài không hợp lệ');
    }

    topicList.value = data.map((item) => ({
      ma_nhom: item.ma_nhom,
      ma_gv: item.ma_gv || '',
      ten_gv: item.ten_gv || 'Không xác định',
      dot_thuc_hien: item.dot_thuc_hien || new Date().getFullYear(),
      ten_de_tai: item.ten_de_tai || 'Không xác định',
      trang_thai: item.trang_thai || 0,
      thanh_vien: Array.isArray(item.thanh_vien)
        ? item.thanh_vien.map((sv) => ({
            ma_sv: sv.ma_sv || '',
            ten_sv: sv.ten_sv || '',
          }))
        : [],
    }));
  } catch (err) {
    let errorMessage = 'Không thể tải danh sách đề tài';
    if (err.response) {
      console.error('Mã lỗi HTTP:', err.response.status);
      if (err.response.status === 401) {
        errorMessage = 'Phiên đăng nhập hết hạn';
        authStore.logout();
        router.push('/login');
      } else if (err.response.status === 403) {
        errorMessage = 'Bạn không có quyền truy cập';
      } else if (err.response.status === 404) {
        errorMessage = 'Danh sách đề tài trống';
        topicList.value = [];
      }
    }
    error.value = errorMessage;
    topicList.value = [];
    console.error('Lỗi khi lấy danh sách đề tài:', err);
  } finally {
    loading.value = false;
  }
}

// Định dạng trạng thái
function formatTrangThai(trang_thai) {
  switch (trang_thai) {
    case 1:
      return 'Đã đăng ký';
    case 2:
      return 'Đã duyệt';
    case 0:
      return 'Bị Hủy';
    default:
      return 'Không xác định';
  }
}

// Cập nhật hàm handleView
function handleView(topic) {
  isEditing.value = false;
  currentTopic.value = { ...topic };
  showModal.value = true;
}

// Thêm hàm closeModal
function closeModal() {
  showModal.value = false;
  currentTopic.value = {
    ma_gv: '',
    ten_gv: '',
    ten_de_tai: '',
    dot_thuc_hien: new Date().getFullYear(),
    trang_thai: 0,
    thanh_vien: []
  };
}

// Thêm hàm handleSubmit
async function handleSubmit() {
  try {
    const response = await api.put(`gv/nhomnckh/${currentTopic.value.ma_nhom}`, currentTopic.value);
    if (response.data) {
      // Cập nhật lại danh sách
      await fetchTopicList();
      closeModal();
    }
  } catch (err) {
    console.error('Lỗi khi cập nhật đề tài:', err);
    error.value = 'Không thể cập nhật đề tài';
  }
}

// Thêm computed property cho danh sách đã lọc
const filteredTopics = computed(() => {
  return topicList.value.filter(topic => {
    const matchesGV = !filters.value.ten_gv || 
      topic.ten_gv.toLowerCase().includes(filters.value.ten_gv.toLowerCase());
    
    const matchesSV = !filters.value.ten_sv || 
      topic.thanh_vien.some(sv => 
        sv.ten_sv.toLowerCase().includes(filters.value.ten_sv.toLowerCase())
      );
    
    const matchesTopic = !filters.value.ten_de_tai || 
      topic.ten_de_tai.toLowerCase().includes(filters.value.ten_de_tai.toLowerCase());
    
    const matchesDot = !filters.value.dot_thuc_hien || 
      topic.dot_thuc_hien.toString().includes(filters.value.dot_thuc_hien.toString());
    
    return matchesGV && matchesSV && matchesTopic && matchesDot;
  });
});
</script>

<style scoped>
/* Container */
.container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  overflow-y: auto;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
}

.container::-webkit-scrollbar {
  width: 6px;
}

.container::-webkit-scrollbar-track {
  background: #e2e8f0;
  border-radius: 10px;
}

.container::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, #0082c6, #0069a3);
  border-radius: 10px;
}

.container::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, #0069a3, #005a8c);
}

/* Header */
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(226, 232, 240, 0.8);
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 80px;
  z-index: 1000;
  padding: 10px 20px 10px 70px;
  box-sizing: border-box;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo {
  width: 50px;
  margin-right: 2rem;
  margin-top: 2rem;
  transition: all 0.3s ease;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
}

.logo:hover {
  transform: scale(1.05) rotate(5deg);
  filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.2));
}

.header h1 {
  font-size: 1.2rem;
  margin: 0;
  text-align: center;
  color: #0082c6;
}

.auth-buttons {
  display: flex;
  gap: 0.8rem;
  align-items: center;
}

.auth-buttons span {
  font-size: 0.9rem;
  color: #4b5563;
  font-weight: 500;
}

.auth-buttons button {
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, #0082c6, #0069a3);
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 130, 198, 0.2);
}

.auth-buttons button:hover {
  background: linear-gradient(135deg, #0069a3, #005a8c);
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 130, 198, 0.3);
}

/* Mobile menu button */
.mobile-menu-btn {
  display: none;
  background: none;
  border: none;
  color: #0082c6;
  font-size: 24px;
  cursor: pointer;
  padding: 8px;
  transition: all 0.3s ease;
}

.mobile-menu-btn:hover {
  color: #0069a3;
}

/* Overlay */
.overlay {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 998;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.overlay-active {
  opacity: 1;
}

/* Main layout */
.main-layout {
  display: flex;
  margin-top: 100px;
  min-height: calc(100vh - 100px - 100px);
}

/* Sidebar */
.sidebar {
  box-shadow: 4px 0 15px rgba(0, 0, 0, 0.1);
  background: linear-gradient(135deg, #0082c6, #0069a3);
  transition: all 0.3s ease;
  z-index: 999;
  width: 220px;
  position: fixed;
  top: 80px;
  left: 0;
  height: calc(100vh - 60px);
}

/* Main Content */
.main-content {
  flex: 1;
  margin-left: 240px;
  margin-top: 20px;
  padding: 20px 40px;
  box-sizing: border-box;
  background: transparent;
  transition: all 0.3s ease;
}

.main-content-shifted {
  margin-left: 240px;
}

/* Content */
.content {
  background-color: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 30px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  border: 1px solid rgba(226, 232, 240, 0.8);
}

.content:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.content h2 {
  font-size: 1.5rem;
  background: linear-gradient(135deg, #0082c6, #0069a3);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 1.5rem;
  font-weight: 700;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  letter-spacing: 0.5px;
}

/* Mobile Cards */
.mobile-cards {
  display: none;
  flex-direction: column;
  gap: 15px;
  padding: 10px;
}

.mobile-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: all 0.3s ease;
}

.mobile-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 15px;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

.card-number {
  font-weight: 600;
  color: #0082c6;
}

.card-status {
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
}

.status-registered {
  background: #e0f2fe;
  color: #0369a1;
}

.status-approved {
  background: #dcfce7;
  color: #166534;
}

.status-pending {
  background: #fef9c3;
  color: #854d0e;
}

.card-body {
  padding: 15px;
}

.card-item {
  margin-bottom: 12px;
}

.card-item:last-child {
  margin-bottom: 0;
}

.label {
  display: block;
  font-size: 12px;
  color: #64748b;
  margin-bottom: 4px;
}

.value {
  display: block;
  font-size: 14px;
  color: #1e293b;
  font-weight: 500;
}

.value-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.list-item {
  font-size: 14px;
  color: #1e293b;
  padding: 4px 0;
  border-bottom: 1px solid #e2e8f0;
}

.list-item:last-child {
  border-bottom: none;
}

.card-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #e2e8f0;
}

/* Responsive */
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

  .sidebar ul {
    padding: 15px;
  }

  .sidebar a {
    font-size: 13px;
    padding: 8px 12px;
  }

  .header h1 {
    font-size: 1.1rem;
  }

  .topic-table {
    min-width: 1000px;
  }
  
  .topic-table th,
  .topic-table td {
    padding: 12px;
  }
}

@media (max-width: 768px) {
  .mobile-menu-btn {
    display: block;
  }

  .overlay {
    display: block;
  }

  .header {
    padding: 0 15px;
    height: 60px;
    justify-content: space-between;
  }

  .header h1 {
    font-size: 1rem;
    margin: 0 10px;
    text-align: center;
  }

  .logo {
    width: 30px;
    margin: 0;
  }

  .auth-buttons {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .auth-buttons span {
    font-size: 0.8rem;
  }

  .auth-buttons button {
    padding: 6px 12px;
    font-size: 0.8rem;
  }

  .sidebar {
    width: 250px;
    left: -250px;
    top: 60px;
    height: calc(100vh - 60px);
  }

  .sidebar-open {
    left: 0;
  }

  .main-content {
    margin-left: 0;
    padding: 15px;
  }

  .content {
    padding: 15px;
  }

  .mobile-cards {
    display: flex;
  }

  .desktop-only {
    display: none;
  }

  .table-container {
    background: none;
    box-shadow: none;
    border: none;
  }
}

@media (max-width: 480px) {
  .header {
    padding: 0 10px;
  }

  .header h1 {
    font-size: 0.9rem;
  }

  .logo {
    width: 25px;
  }

  .mobile-menu-btn {
    font-size: 20px;
    padding: 6px;
  }

  .auth-buttons button {
    padding: 4px 8px;
    font-size: 0.7rem;
  }

  .mobile-card {
    border-radius: 8px;
  }

  .card-header {
    padding: 10px 12px;
  }

  .card-body {
    padding: 12px;
  }

  .label {
    font-size: 11px;
  }

  .value, .list-item {
    font-size: 13px;
  }
}

/* User Email */
.user-email {
  max-width: 150px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>