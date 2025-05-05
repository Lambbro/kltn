<template>
  <div class="container">
    <!-- Header -->
    <header class="header">
      <button v-if="isMobile" class="sidebar-toggle" @click="toggleSidebar">☰</button>
      <img src="@/assets/img/logo-hou.png" alt="Logo" class="logo" />
      <h1>ĐĂNG KÝ ĐỀ TÀI NGHIÊN CỨU KHOA HỌC GIẢNG VIÊN</h1>
    </header>

    <!-- Overlay khi sidebar mở trên mobile -->
    <div v-if="isSidebarOpen && isMobile" class="overlay" @click="toggleSidebar"></div>

    <!-- Main layout -->
    <div class="main-layout">
      <!-- Sidebar -->
      <SidebarHome
        class="sidebar"
        :class="{ 'sidebar-open': isSidebarOpen }"
        :is-open="isSidebarOpen"
        @toggle="toggleSidebar"
      />

      <!-- Main content -->
      <div class="main-content" :class="{ 'main-content-shifted': isSidebarOpen && !isMobile }">
        <div class="content">
          <form @submit.prevent="handleSubmit" class="form-apply-topic">
            <div class="form-group">
              <label for="nameTopic" class="label">Tên đề tài:</label>
              <input
                type="text"
                id="nameTopic"
                v-model="currentTopic.ten_de_tai"
                class="input-field"
                required
              />
            </div>

            <div class="form-group">
              <label for="file" class="label">Đề cương:</label>
              <input
                type="file"
                id="file"
                @change="handleFileUpload"
                class="input-field"
                accept=".pdf,.doc,.docx"
                :required="!isEditing"
              />
              <div v-if="isEditing && currentTopic.tai_lieu.link_tep" class="current-file">
                File hiện tại: {{ currentTopic.tai_lieu.link_tep.name }}
              </div>
            </div>

            <div class="form-buttons">
              <button type="submit" class="action-btn">
                {{ isEditing ? 'Chỉnh sửa' : 'Đăng ký' }}
              </button>
              <button type="button" class="action-btn" @click="resetForm">Làm mới</button>
              <button type="button" class="action-btn" @click="toggleShowRegistered">
                {{ showRegistered ? 'Ẩn danh sách' : 'Xem đề tài đã đăng ký' }}
              </button>
            </div>
          </form>

          <!-- Bảng hiển thị đề tài đã đăng ký -->
          <div v-if="showRegistered" class="registered-topics">
            <h2>Danh sách đề tài đã đăng ký</h2>
            <div class="topic-table-container">
              <table class="topic-table">
                <thead>
                  <tr>
                    <th>STT</th>
                    <th>Tên đề tài</th>
                    <th>File upload</th>
                    <th>Hành động</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(topic, index) in registeredTopics" :key="topic.ma_de_tai">
                    <td>{{ index + 1 }}</td>
                    <td @click="editTopic(index)">{{ topic.ten_de_tai }}</td>
                    <td>
                      <a v-if="topic.tai_lieu?.link_tep" 
                         :href="topic.tai_lieu.link_tep" 
                         target="_blank" 
                         class="file-link">
                        {{ topic.tai_lieu.link_tep.split('/').pop() }}
                      </a>
                      <span v-else class="no-file">Chưa có file</span>
                    </td>
                    <td>
                      <button class="action-btn" @click="editTopic(index)">Sửa</button>
                      <button class="action-btn" @click="confirmDelete(index)">Xóa</button>
                    </td>
                  </tr>
                  <tr v-if="registeredTopics.length === 0">
                    <td colspan="4">Chưa có đề tài nào được đăng ký</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer
    <footer class="footer">
      <Footer class="footer-content" />
    </footer> -->
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import SidebarHome from '@/components/SidebarHome.vue';
import { useAuthStore } from '@/stores/auth';
import api from '@/config/api';

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

const registeredTopics = ref([]);
const showRegistered = ref(false);

const currentTopic = ref({
  ten_de_tai: '',
  tai_lieu: {
    link_tep: null
  }
});
const isEditing = ref(false);
async function handleSubmit() {
  try {
    const ten_de_tai = currentTopic.value.ten_de_tai.trim();
    if (!ten_de_tai || ten_de_tai.match(/^\s*$/)) {
      alert('Tên đề tài không được để trống hoặc chỉ chứa khoảng trắng');
      return;
    }

    if (ten_de_tai.length > 255) {
      alert('Tên đề tài không được vượt quá 255 ký tự');
      return;
    }

    if (!currentTopic.value.tai_lieu.link_tep) {
      alert('Vui lòng chọn file đề cương');
      return;
    }

    // Lấy thông tin giảng viên từ auth store
    const authStore = useAuthStore();
    if (!authStore.user) {
      alert('Vui lòng đăng nhập để tiếp tục');
      return;
    }

    // Tạo FormData để gửi file
    const formData = new FormData();
    formData.append('file', currentTopic.value.tai_lieu.link_tep);

    let response;
    if (isEditing.value) {
      // Nếu đang chỉnh sửa, sử dụng PUT API
      const ma_de_tai = currentTopic.value.ma_de_tai;
      response = await api.put(`detai_gv/de_xuat/${ma_de_tai}?ten_de_tai=${encodeURIComponent(ten_de_tai)}`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
    } else {
      // Nếu đang tạo mới, sử dụng POST API
      response = await api.post(`detai_gv/de_xuat?ten_de_tai=${encodeURIComponent(ten_de_tai)}`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
    }
    
    console.log('Phản hồi từ server:', response);
    
    if (response.status === 200) {
      alert(isEditing.value ? 'Chỉnh sửa đề tài thành công!' : 'Đăng ký đề tài thành công!');
      resetForm();
      fetchRegisteredTopics();
    } else {
      alert(isEditing.value ? 'Có lỗi xảy ra khi chỉnh sửa đề tài' : 'Có lỗi xảy ra khi đăng ký đề tài');
    }
  } catch (error) {
    console.error('Lỗi:', error);
    if (error.response) {
      console.error('Chi tiết lỗi:', error.response.data);
      alert(`Lỗi: ${error.response.data.message || 'Có lỗi xảy ra'}`);
    } else {
      alert('Có lỗi xảy ra');
    }
  }
}

// Hàm reset form
function resetForm() {
  currentTopic.value = {
    ten_de_tai: '',
    tai_lieu: {
      link_tep: null
    }
  };
  isEditing.value = false;
}

// Hàm xử lý khi đổi file
function handleFileUpload(event) {
  const file = event.target.files[0];
  if (!file) return;

  // Kiểm tra định dạng file
  const allowedTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
  if (!allowedTypes.includes(file.type)) {
    alert('Chỉ chấp nhận file PDF hoặc Word (.doc, .docx)');
    event.target.value = '';
    return;
  }

  // Kiểm tra kích thước file (ví dụ: tối đa 10MB)
  const maxSize = 10 * 1024 * 1024; // 10MB
  if (file.size > maxSize) {
    alert('Kích thước file không được vượt quá 10MB');
    event.target.value = '';
    return;
  }

  // Lưu file object thay vì URL
  currentTopic.value.tai_lieu.link_tep = file;
}

function toggleShowRegistered() {
  showRegistered.value = !showRegistered.value;
  if (showRegistered.value) {
    fetchRegisteredTopics();
  }
}

// Hàm lấy danh sách đề tài đã đăng ký
async function fetchRegisteredTopics() {
  try {
    const authStore = useAuthStore();
    if (!authStore.user) return;

    const ma_gv = authStore.user.email.split('@')[0];
    const response = await api.get(`detai_gv/de_xuat/giang_vien/${ma_gv}`);
    if (response.data) {
      // Chuyển đổi dữ liệu để hiển thị file đúng cách
      registeredTopics.value = response.data.map(topic => ({
        ...topic,
        tai_lieu: {
          ...topic.tai_lieu,
          link_tep: topic.tai_lieu?.link_tep || null
        }
      }));
    } else {
      registeredTopics.value = [];
    }
  } catch (error) {
    console.error('Lỗi khi lấy danh sách đề tài:', error);
    alert('Có lỗi xảy ra khi lấy danh sách đề tài');
  }
}

// Hàm chỉnh sửa đề tài
function editTopic(index) {
  currentTopic.value = { ...registeredTopics.value[index] };
  isEditing.value = true;
}

// Hàm xác nhận xóa đề tài
async function confirmDelete(index) {
  if (window.confirm('Bạn có chắc chắn muốn xóa đề tài này không?')) {
    try {
      const ma_de_tai = registeredTopics.value[index].ma_de_tai;
      const response = await api.delete(`detai_gv/de_xuat/${ma_de_tai}`);
      
      if (response.status === 200) {
        registeredTopics.value.splice(index, 1);
        alert('Xóa đề tài thành công!');
      } else {
        alert('Có lỗi xảy ra khi xóa đề tài');
      }
    } catch (error) {
      console.error('Lỗi khi xóa đề tài:', error);
      alert('Có lỗi xảy ra khi xóa đề tài');
    }
  }
}

onMounted(() => {
  // Khởi tạo mảng thành viên nếu chưa có
  if (!Array.isArray(currentTopic.value.thanh_vien)) {
    currentTopic.value.thanh_vien = [];
  }
});
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
  height: calc(100vh - 80px); /* Trừ header */
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  transition: left 0.3s ease;
  z-index: 1000;
}

/* Main Content */
.main-content {
  flex: 1;
  padding: 20px;
  box-sizing: border-box;
  background: #f4f7fa;
  transition: margin-left 0.3s ease;
  margin-left: 240px; /* Tăng khoảng cách với sidebar */
}

.main-content-shifted {
  margin-left: 240px; /* Cập nhật margin khi sidebar mở */
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

/* Form */
.form-apply-topic {
  display: flex;
  flex-direction: column;
  gap: 15px;
  max-width: 600px;
  margin: 0 auto;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label.label {
  display: block;
  margin-bottom: 5px;
  font-weight: 600;
  color: #1a3c5e;
  font-size: 16px;
}

.form-group input.input-field {
  width: 100%;
  padding: 8px;
  border: 1px solid #d1dbe3;
  border-radius: 6px;
  font-size: 14px;
  background-color: #f9fafb;
  transition: border-color 0.3s, box-shadow 0.3s, background-color 0.3s;
}

.form-group input.input-field:focus {
  border-color: #0082c6;
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2);
  background-color: white;
  outline: none;
}

.form-buttons {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

/* Registered Topics */
.registered-topics {
  margin-top: 20px;
}

.registered-topics h2 {
  font-size: 1.5rem;
  color: #1a3c5e;
  margin-bottom: 15px;
}

.topic-table-container {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow-x: auto; /* Cho phép cuộn ngang trên mobile */
}

.topic-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

.topic-table th,
.topic-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #d1dbe3;
}

.topic-table th {
  background: #0082c6;
  color: white;
  font-weight: 600;
  font-size: 14px;
  position: sticky;
  top: 0;
}

.topic-table td {
  background: white;
  font-size: 14px;
}

.topic-table td:first-child {
  width: 50px;
  text-align: center;
}

.topic-table td:nth-child(2) {
  cursor: pointer;
}

.topic-table td:nth-child(4) {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.topic-table tr:hover {
  background: #f9fafb;
}

.no-file {
  color: #6b7280;
  font-style: italic;
}

.action-btn {
  background-color: #0082c6;
  color: white;
  padding: 8px 16px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-size: 14px;
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
  height: 100px;
}

/* Responsive */

/* Tablet (≤1024px) */
@media (max-width: 1024px) {
  .main-layout {
    margin-top: 80px;
  }

  .sidebar {
    top: 80px;
    width: 200px;
  }

  .main-content {
    margin-left: 220px;
  }

  .main-content-shifted {
    margin-left: 220px;
  }
}

/* Mobile (≤768px) */
@media (max-width: 768px) {
  .main-layout {
    margin-top: 80px;
  }

  .sidebar {
    top: 80px;
    width: 200px;
    left: -200px;
  }

  .sidebar-open {
    left: 0;
  }

  .main-content {
    margin-left: 0;
    padding: 15px;
  }

  .main-content-shifted {
    margin-left: 0;
  }

  .topic-table-container {
    overflow-x: auto;
  }

  .topic-table {
    min-width: 600px;
  }
}

/* Small Mobile (≤480px) */
@media (max-width: 480px) {
  .main-layout {
    margin-top: 80px;
  }

  .sidebar {
    top: 80px;
    width: 180px;
    left: -180px;
  }

  .sidebar-open {
    left: 0;
  }

  .main-content {
    padding: 10px;
  }
}

.current-file {
  margin-top: 5px;
  font-size: 14px;
  color: #4b5563;
  font-style: italic;
}

.status-badge {
  padding: 8px 12px;
  border-radius: 6px;
  font-weight: 500;
  font-size: 14px;
  display: inline-block;
  margin-top: 5px;
}

.status-badge.chua-nop {
  background-color: #f3f4f6;
  color: #6b7280;
}

.status-badge.da-nop {
  background-color: #d1fae5;
  color: #065f46;
}

.status-badge.da-hoan-thien {
  background-color: #dbeafe;
  color: #1e40af;
}

.status-badge.can-chinh-sua {
  background-color: #fee2e2;
  color: #991b1b;
}

.file-link {
  color: #0082c6;
  text-decoration: none;
  cursor: pointer;
}

.file-link:hover {
  text-decoration: underline;
}
</style>