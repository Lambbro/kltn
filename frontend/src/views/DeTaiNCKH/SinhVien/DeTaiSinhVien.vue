<template>
  <div class="container">
    <div v-if="sidebarOpen" class="overlay" @click="toggleSidebar"></div>

    <!-- Header -->
    <header class="header">
      <button class="mobile-toggle" @click="toggleSidebar" v-if="isMobile">
        <span class="toggle-icon">☰</span>
      </button>
      <img src="@/assets/img/logo-hou.png" alt="Logo" class="logo" />
      <h1>HỆ THỐNG QUẢN LÝ NGHIÊN CỨU KHOA HỌC</h1>
      <div class="auth-buttons">
        <template v-if="isAuthenticated">
          <span class="user-email">{{ storedEmail }}</span>
          <button @click="handleLogout" class="logout-btn">Đăng xuất</button>
        </template>
        <template v-else>
          <button @click="$router.push('/login')" class="login-btn">Đăng nhập</button>
        </template>
      </div>
    </header>

    <div v-if="isSidebarOpen && isMobile" class="overlay" @click="toggleSidebar"></div>
    <SidebarInfoStudents :is-open="isSidebarOpen" @toggle="toggleSidebar" />

    <div class="main-layout">
      <SidebarInfoStudents :isOpen="isSidebarOpen" @toggle="toggleSidebar" />
      <div class="main-content">
        <div class="page-header">
          <h2>Danh sách đề tài nghiên cứu khoa học</h2>
        </div>

        <div class="research-list">
          <div v-if="loading" class="loading">
            <p>Đang tải dữ liệu...</p>
          </div>
          <div v-else-if="error" class="error">
            <p>{{ error }}</p>
          </div>
          <div v-else-if="tableData.length === 0" class="no-results">
            <p>Không có đề tài nào</p>
          </div>
          <div v-else class="research-items">
            <div v-for="item in tableData" :key="item.ma_de_tai" class="research-item" @click="handleViewDetail(item.ma_de_tai)">
              <div class="research-header">
                <h3>{{ item.ten_de_tai }}</h3>
                <span :class="['status-tag', getStatusClass(item.trang_thai)]">
                  {{ getStatusText(item.trang_thai) }}
                </span>
              </div>
              
              <div class="research-content">
                <div class="info-row">
                  <p><strong>Giảng viên hướng dẫn:</strong> {{ item.ten_gv }}</p>
                </div>

                <div class="info-row">
                  <p><strong>Đợt thực hiện:</strong> {{ item.dot_thuc_hien }}</p>
                </div>

                <div class="info-row">
                  <p><strong>Thành viên:</strong></p>
                  <div class="members-list">
                    <span v-for="member in item.thanh_vien" :key="member.ma_sv" class="member-tag">
                      {{ member.ten_sv }}
                    </span>
                  </div>
                </div>

                <div class="score-section" v-if="item.diem_so">
                  <span class="score-label">Điểm số:</span>
                  <span class="score-value">{{ item.diem_so }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import SidebarInfoStudents from '@/components/SidebarInfoStudents.vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/config/api'

const router = useRouter()
const authStore = useAuthStore()
const isSidebarOpen = ref(true)
const tableData = ref([])
const loading = ref(false)
const error = ref(null)

const isAuthenticated = computed(() => authStore.isAuthenticated)
const storedEmail = computed(() => authStore.user?.email || '')
const isMobile = computed(() => window.innerWidth <= 768)

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value
}

// Hàm lấy trạng thái
function getStatusText(status) {
  switch (status) {
    case 0: return 'Đã hủy'
    case 1: return 'Đang thực hiện'
    case 2: return 'Hoàn thành'
    default: return 'Không xác định'
  }
}

// Hàm lấy class trạng thái
function getStatusClass(status) {
  switch (status) {
    case 0: return 'status-cancelled'
    case 1: return 'status-in-progress'
    case 2: return 'status-completed'
    default: return 'status-unknown'
  }
}

// Hàm lấy class cho progress bar
function getProgressClass(progress) {
  if (progress >= 100) return 'progress-completed'
  if (progress >= 50) return 'progress-half'
  return 'progress-low'
}

// Hàm lọc tài liệu chỉ lấy báo cáo cấp khoa và cấp trường
function getFilteredDocuments(documents) {
  return documents.filter(doc => {
    // 3: Báo cáo cấp khoa, 5: Báo cáo cấp trường
    return doc.loai_tai_lieu === 3 || doc.loai_tai_lieu === 5;
  });
}

// Hàm lấy tên loại tài liệu
function getDocumentType(type) {
  switch (type) {
    case 3: return 'Báo cáo cấp khoa';
    case 5: return 'Báo cáo cấp trường';
    default: return 'Tài liệu khác';
  }
}

// Hàm định dạng ngày tháng
function formatDate(dateString) {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleString('vi-VN');
}

const fetchData = async () => {
  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }

  try {
    loading.value = true
    error.value = null
    const ma_sv = authStore.user.email.split('@')[0]
    const response = await api.get(`get_data/detai_sv/hoan_thanh/${ma_sv}`)
    tableData.value = response.data
  } catch (err) {
    error.value = 'Không thể tải dữ liệu. Vui lòng thử lại sau.'
    console.error('Error fetching data:', err)
  } finally {
    loading.value = false
  }
}

const handleViewDetail = (maDeTai) => {
  if (authStore.isAuthenticated) {
    router.push(`/chi-tiet-de-tai/${maDeTai}`)
  } else {
    router.push('/login')
  }
}

const handleLogout = async () => {
  try {
    await authStore.logout()
    router.push('/login')
  } catch (err) {
    console.error('Logout error:', err)
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.container {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f8fafc;
  position: relative;
}

.header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 80px;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  padding: 10px 20px 10px 70px;
  z-index: 1000;
  gap: 20px;
}

.mobile-toggle {
  position: fixed;
  top: 20px;
  left: 20px;
  background: #0082c6;
  color: white;
  border: none;
  padding: 6px;
  border-radius: 6px;
  cursor: pointer;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1100;
  transition: all 0.3s ease;
}

.mobile-toggle:hover {
  background: #0069a3;
  transform: scale(1.05);
}

.toggle-icon {
  font-size: 1.2rem;
  line-height: 1;
}

.logo {
  width: 50px;
  margin-right: 2rem;
  margin-top: 2rem;
  transition: transform 0.3s ease;
}

.logo:hover {
  transform: scale(1.05);
}

.header h1 {
  font-size: 1.2rem;
  color: #0082c6;
  font-weight: 600;
  margin: 0;
  flex-grow: 1;
  text-align: center;
  background: linear-gradient(135deg, #0082c6, #0069a3);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
  padding: 0 10px;
}

.auth-buttons {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-left: auto;
}

.user-email {
  color: #1e293b;
  font-weight: 500;
  font-size: 0.95rem;
  padding: 8px 12px;
  background: #f1f5f9;
  border-radius: 6px;
  transition: all 0.3s ease;
}

.user-email:hover {
  background: #e2e8f0;
}

.login-btn,
.logout-btn {
  background: #0082c6;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
  min-width: 100px;
  text-align: center;
}

.login-btn:hover,
.logout-btn:hover {
  background: #0069a3;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.main-layout {
  display: flex;
  margin-top: 80px;
  min-height: calc(100vh - 80px);
}

.main-content {
  flex: 1;
  margin-left: 220px;
  padding: 20px;
  background-color: #f8fafc;
  transition: margin-left 0.3s ease;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h2 {
  color: #0082c6;
  font-size: 24px;
  font-weight: 600;
  margin: 0;
}

.research-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.research-items {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.research-item {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #e2e8f0;
  margin-bottom: 20px;
}

.research-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 130, 198, 0.15);
  border-color: #0082c6;
}

.research-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid #e2e8f0;
}

.research-header h3 {
  color: #0082c6;
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  flex: 1;
}

.status-tag {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.status-cancelled {
  background: #fef2f2;
  color: #dc2626;
}

.status-in-progress {
  background: #e6f2ff;
  color: #0082c6;
}

.status-completed {
  background: #dcfce7;
  color: #16a34a;
}

.status-unknown {
  background: #f1f5f9;
  color: #64748b;
}

.research-content {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.info-row {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.info-row p {
  margin: 0;
  color: #334155;
  font-size: 14px;
}

.info-row p strong {
  color: #0082c6;
  font-weight: 600;
  min-width: 120px;
  display: inline-block;
}

.members-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 5px;
}

.member-tag {
  background: #f1f5f9;
  color: #334155;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  transition: all 0.3s ease;
}

.member-tag:hover {
  background: #e2e8f0;
  transform: translateY(-1px);
}

.score-section {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid #e2e8f0;
}

.score-label {
  color: #64748b;
  font-size: 14px;
}

.score-value {
  color: #0082c6;
  font-weight: 600;
  font-size: 16px;
}

.loading,
.error,
.no-results {
  text-align: center;
  padding: 40px;
  color: #64748b;
  font-size: 16px;
  background: white;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.error {
  color: #dc2626;
}

.documents-section {
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid #e2e8f0;
}

.documents-header {
  margin-bottom: 15px;
}

.documents-header h4 {
  color: #0082c6;
  margin: 0;
  font-size: 16px;
  font-weight: 600;
}

.documents-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.document-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.document-info {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.document-type {
  color: #334155;
  font-weight: 500;
  font-size: 14px;
}

.document-date {
  color: #64748b;
  font-size: 12px;
}

.view-doc-btn {
  background: #0082c6;
  color: white;
  padding: 6px 12px;
  border-radius: 6px;
  text-decoration: none;
  font-size: 13px;
  transition: all 0.3s ease;
}

.view-doc-btn:hover {
  background: #0069a3;
  transform: translateY(-1px);
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
  }

  .research-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .status-tag {
    align-self: flex-start;
  }

  .document-item {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }

  .document-actions {
    width: 100%;
  }

  .view-doc-btn {
    width: 100%;
    text-align: center;
  }
}
</style>