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
          <h2>Quản lý hướng NCKH</h2>

          <!-- Filter section -->
          <div class="filter-section">
            <div class="filter-form">
              <div class="filter-row">
                <div>
                  <label class="label">Tên hướng nghiên cứu</label>
                  <input 
                    type="text" 
                    v-model="filterCriteria.ten_hnc" 
                    class="input-field"
                    placeholder="Nhập tên hướng nghiên cứu cần tìm"
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- Bảng danh sách hướng nghiên cứu -->
          <div v-if="!loading && !error" class="table-container">
            <table class="research-table">
              <thead>
                <tr>
                  <th>STT</th>
                  <th>Tên hướng NCKH</th>
                  <th>Hành động</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(topic, index) in filteredResearchTopics" :key="topic.ma_hnc">
                  <td>{{ index + 1 }}</td>
                  <td>{{ topic.ten_hnc }}</td>
                  <td>
                    <button class="action-btn add-btn" @click="showAddModal = true">
                      <i class="fas fa-plus"></i> Thêm
                    </button>
                    <button class="action-btn edit-btn" @click="editTopic(topic)">
                      <i class="fas fa-edit"></i> Sửa
                    </button>
                    <button class="action-btn delete-btn" @click="deleteTopic(topic.ma_hnc)">
                      <i class="fas fa-trash"></i> Xóa
                    </button>
                  </td>
                </tr>
                <tr v-if="researchTopics.length === 0">
                  <td colspan="3">Không có dữ liệu</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-if="loading" class="loading-text">Đang tải dữ liệu...</div>
          <div v-if="error" class="error-text">{{ error }}</div>
        </div>
      </div>
    </div>
  </div>

  <!-- Modal thêm hướng nghiên cứu -->
  <div v-if="showAddModal" class="modal-overlay" @click="showAddModal = false">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h3>Thêm hướng nghiên cứu mới</h3>
        <button class="close-btn" @click="showAddModal = false">&times;</button>
      </div>
      <div class="modal-body">
        <div class="form-group">
          <label for="ten_hnc">Tên hướng nghiên cứu:</label>
          <input 
            type="text" 
            id="ten_hnc" 
            v-model="newTopic.ten_hnc" 
            class="form-input"
            placeholder="Nhập tên hướng nghiên cứu"
          />
        </div>
      </div>
      <div class="modal-footer">
        <button class="cancel-btn" @click="showAddModal = false">Hủy</button>
        <button class="submit-btn" @click="addTopic" :disabled="!newTopic.ten_hnc">
          Thêm
        </button>
      </div>
    </div>
  </div>

  <!-- Modal sửa hướng nghiên cứu -->
  <div v-if="showEditModal" class="modal-overlay" @click="showEditModal = false">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h3>Sửa hướng nghiên cứu</h3>
        <button class="close-btn" @click="showEditModal = false">&times;</button>
      </div>
      <div class="modal-body">
        <div class="form-group">
          <label for="edit_ten_hnc">Tên hướng nghiên cứu:</label>
          <input 
            type="text" 
            id="edit_ten_hnc" 
            v-model="editingTopic.ten_hnc" 
            class="form-input"
            placeholder="Nhập tên hướng nghiên cứu"
          />
        </div>
      </div>
      <div class="modal-footer">
        <button class="cancel-btn" @click="showEditModal = false">Hủy</button>
        <button class="submit-btn" @click="updateTopic" :disabled="!editingTopic.ten_hnc">
          Cập nhật
        </button>
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
    isSidebarOpen.value = false;
  }
});

const researchTopics = ref([]);
const loading = ref(true);
const error = ref(null);

// Modal states
const showAddModal = ref(false);
const showEditModal = ref(false);
const newTopic = ref({
  ten_hnc: ''
});
const editingTopic = ref({
  ma_hnc: null,
  ten_hnc: ''
});

// Add new state for filter
const filterCriteria = ref({
  ten_hnc: ''
});

// Add computed property for filtered topics
const filteredResearchTopics = computed(() => {
  if (!filterCriteria.value.ten_hnc) {
    return researchTopics.value;
  }
  
  const searchTerm = filterCriteria.value.ten_hnc.toLowerCase().trim();
  return researchTopics.value.filter(topic => 
    topic.ten_hnc.toLowerCase().includes(searchTerm)
  );
});

// Fetch research topics data
const fetchResearchTopics = async () => {
  try {
    loading.value = true;
    const response = await api.get('/phongkhdn/hnc');
    researchTopics.value = response.data;
    error.value = null;
  } catch (err) {
    error.value = 'Có lỗi xảy ra khi tải dữ liệu';
    console.error('Error fetching research topics:', err);
  } finally {
    loading.value = false;
  }
};

// Add topic
const addTopic = async () => {
  try {
    await api.post('/phongkhdn/hnc/add', {
      ten_hnc: newTopic.value.ten_hnc
    });
    
    await fetchResearchTopics(); // Refresh the list
    showAddModal.value = false;
    newTopic.value.ten_hnc = ''; // Reset form
    
    alert('Thêm hướng nghiên cứu thành công!');
  } catch (err) {
    console.error('Error adding topic:', err);
    alert('Có lỗi xảy ra khi thêm hướng nghiên cứu');
  }
};

// Edit topic
const editTopic = (topic) => {
  editingTopic.value = { ...topic };
  showEditModal.value = true;
};

// Update topic
const updateTopic = async () => {
  try {
    await api.put(`/phongkhdn/hnc/update/${editingTopic.value.ma_hnc}`, {
      ten_hnc: editingTopic.value.ten_hnc
    });
    
    await fetchResearchTopics(); // Refresh the list
    showEditModal.value = false;
    editingTopic.value = { ma_hnc: null, ten_hnc: '' }; // Reset form
    
    alert('Cập nhật hướng nghiên cứu thành công!');
  } catch (err) {
    console.error('Error updating topic:', err);
    alert('Có lỗi xảy ra khi cập nhật hướng nghiên cứu');
  }
};

// Delete topic
const deleteTopic = async (ma_hnc) => {
  if (confirm('Bạn có chắc chắn muốn xóa hướng nghiên cứu này?')) {
    try {
      await api.delete(`/phongkhdn/hnc/delete/${ma_hnc}`);
      await fetchResearchTopics(); // Refresh the list
      alert('Xóa hướng nghiên cứu thành công!');
    } catch (err) {
      console.error('Error deleting topic:', err);
      alert('Có lỗi xảy ra khi xóa hướng nghiên cứu');
    }
  }
};

function handleLogout() {
  logout();
  router.push('/login');
}

onMounted(() => {
  authStore.loadUserFromStorage();
  fetchResearchTopics();
});
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
  z-index: 999;
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

.sidebar-toggle {
  display: none;
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

/* Table */
.table-container {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow-x: auto;
  width: 100%;
}

.research-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

.research-table th,
.research-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #d1dbe3;
}

.research-table th {
  background: #0082c6;
  color: white;
  font-weight: 600;
  font-size: 14px;
}

.research-table td {
  background: white;
  font-size: 14px;
}

.research-table tr:hover {
  background: #f9fafb;
}

/* Action Buttons */
.action-btn {
  padding: 8px 16px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-size: 14px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all 0.3s ease;
  margin-right: 8px;
}

.edit-btn {
  background-color: #0082c6;
  color: white;
}

.edit-btn:hover {
  background-color: #0069a3;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(0, 130, 198, 0.3);
}

.delete-btn {
  background-color: #dc2626;
  color: white;
}

.delete-btn:hover {
  background-color: #b91c1c;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(220, 38, 38, 0.3);
}

.add-btn {
  background-color: #10b981;
  color: white;
}

.add-btn:hover {
  background-color: #059669;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(16, 185, 129, 0.3);
}

/* Modal styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1100;
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  animation: modalSlideIn 0.3s ease;
}

@keyframes modalSlideIn {
  from {
    transform: translateY(-20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.modal-header {
  padding: 20px;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  color: #1e293b;
  font-size: 1.25rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #64748b;
  cursor: pointer;
  padding: 0;
  line-height: 1;
}

.close-btn:hover {
  color: #1e293b;
}

.modal-body {
  padding: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #1e293b;
  font-weight: 500;
}

.form-input {
  width: 100%;
  padding: 10px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-input:focus {
  border-color: #0082c6;
  box-shadow: 0 0 0 3px rgba(0, 130, 198, 0.1);
  outline: none;
}

.modal-footer {
  padding: 20px;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.cancel-btn {
  padding: 8px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  background: white;
  color: #64748b;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-btn:hover {
  background: #f8fafc;
  border-color: #cbd5e1;
}

.submit-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  background: #0082c6;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.submit-btn:hover:not(:disabled) {
  background: #0069a3;
}

.submit-btn:disabled {
  background: #94a3b8;
  cursor: not-allowed;
}

/* Status Messages */
.loading-text {
  color: #4b5563;
  font-size: 1.1rem;
  text-align: center;
  padding: 20px;
}

.error-text {
  color: #ef4444;
  font-size: 1.1rem;
  text-align: center;
  padding: 20px;
  background: #fee2e2;
  border-radius: 8px;
  margin: 10px 0;
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

  .main-content-shifted {
    margin-left: 200px;
  }

  .header h1 {
    font-size: 1.1rem;
  }
}

@media (max-width: 768px) {
  .sidebar-toggle {
    display: block;
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

  .main-content-shifted {
    margin-left: 0;
  }

  .overlay ~ .main-content {
    pointer-events: none;
  }

  .research-table th,
  .research-table td {
    padding: 8px;
    font-size: 13px;
  }

  .action-btn {
    padding: 6px 12px;
    font-size: 13px;
  }

  .filter-row {
    flex-direction: column;
    gap: 15px;
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

  .research-table th,
  .research-table td {
    padding: 6px;
    font-size: 12px;
  }

  .action-btn {
    padding: 4px 8px;
    font-size: 12px;
  }

  .modal-content {
    width: 95%;
    margin: 10px;
  }

  .modal-header h3 {
    font-size: 1.1rem;
  }

  .form-input {
    padding: 8px;
    font-size: 0.9rem;
  }

  .modal-footer button {
    padding: 6px 12px;
    font-size: 0.9rem;
  }
}

/* Filter Section */
.filter-section {
  margin: 20px 0;
}

.filter-form {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.filter-row {
  display: flex;
  gap: 20px;
}

.filter-row > div {
  flex: 1;
}

.label {
  display: block;
  font-size: 0.9rem;
  color: #4b5563;
  margin-bottom: 8px;
  font-weight: 500;
}

.input-field {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.input-field:focus {
  border-color: #0082c6;
  box-shadow: 0 0 0 2px rgba(0, 130, 198, 0.1);
  outline: none;
}
</style>


