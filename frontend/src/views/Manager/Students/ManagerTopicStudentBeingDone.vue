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

      <!-- Hiển thị trạng thái đăng nhập -->
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
          <div class="content-header">
            <h2>Danh sách đề tài đang thực hiện</h2>
            <button class="toggle-filter-btn" @click="showFilters = !showFilters">
              <i :class="['fas', showFilters ? 'fa-filter-circle-xmark' : 'fa-filter']"></i>
              {{ showFilters ? 'Ẩn bộ lọc' : 'Hiện bộ lọc' }}
            </button>
          </div>
          
          <!-- Filter Section -->
          <div class="filter-section" :class="{ 'filter-section-visible': showFilters }">
            <div class="filter-form">
              <div class="filter-row">
                <div class="filter-group">
                  <label>
                    <i class="fas fa-book"></i>
                    Tên đề tài
                  </label>
                  <input 
                    type="text" 
                    v-model="filters.tenDeTai" 
                    placeholder="Nhập tên đề tài..."
                    @input="currentPage = 1"
                  >
                </div>
                <div class="filter-group">
                  <label>
                    <i class="fas fa-chalkboard-teacher"></i>
                    Giảng viên hướng dẫn
                  </label>
                  <input 
                    type="text" 
                    v-model="filters.tenGv" 
                    placeholder="Nhập tên giảng viên..."
                    @input="currentPage = 1"
                  >
                </div>
                <div class="filter-group">
                  <label>
                    <i class="fas fa-users"></i>
                    Tên thành viên
                  </label>
                  <input 
                    type="text" 
                    v-model="filters.tenThanhVien" 
                    placeholder="Nhập tên thành viên..."
                    @input="currentPage = 1"
                  >
                </div>
              </div>
              <div class="filter-row">
                <div class="filter-group">
                  <label>
                    <i class="fas fa-flask"></i>
                    Hướng nghiên cứu
                  </label>
                  <input 
                    type="text" 
                    v-model="filters.huongNghienCuu" 
                    placeholder="Nhập hướng nghiên cứu..."
                    @input="currentPage = 1"
                  >
                </div>
                <div class="filter-group">
                  <label>
                      <i class="fas fa-chart-line"></i>
                    Tiến độ
                  </label>
                  <input 
                    type="text" 
                    v-model="filters.tienDo" 
                    placeholder="Nhập tiến độ..."
                    @input="currentPage = 1"
                  >
                </div>
                <div class="filter-actions">
                  <button class="reset-btn" @click="resetFilters">
                    <i class="fas fa-undo"></i>
                    Đặt lại bộ lọc
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Mobile Cards View -->
          <div class="mobile-cards">
            <div v-for="topic in paginatedTopics" :key="topic.ma_de_tai" class="mobile-card">
              <div class="card-header">
                <span class="card-title">{{ topic.ten_de_tai }}</span>
                <span :class="['card-status', getStatusClass(topic.trang_thai)]">
                  {{ getStatusText(topic.trang_thai) }}
                </span>
              </div>
              <div class="card-body">
                <!-- <div class="card-item">
                  <span class="label">Mã đề tài:</span>
                  <span class="value">{{ topic.ma_de_tai }}</span>
                </div>
                <div class="card-item">
                  <span class="label">Mã nhóm:</span>
                  <span class="value">{{ topic.ma_nhom }}</span>
                </div> -->
                <div class="card-item">
                  <span class="label">Đợt thực hiện:</span>
                  <span class="value">{{ topic.dot_thuc_hien }}</span>
                </div>
                <div class="card-item">
                  <span class="label">Tiến độ:</span>
                  <span class="progress-text">{{ getProgressText(topic) }}</span>
                </div>
                <div class="card-item">
                  <span class="label">Điểm số:</span>
                  <span class="value">{{ topic.diem_so }}</span>
                </div>
                <div class="card-item">
                  <span class="label">Giảng viên hướng dẫn:</span>
                  <span class="value">{{ topic.ten_gv }}</span>
                </div>
                <div class="card-item">
                  <span class="label">Thành viên:</span>
                  <div class="value-list">
                    <div v-for="member in topic.thanh_vien" :key="member.ma_sv" class="list-item">
                      {{ member.ma_sv }} - {{ member.ten_sv }}
                    </div>
                  </div>
                </div>
                <div class="card-actions">
                  <button class="documents-btn" @click="showDocumentDetails(topic)">
                    Xem tài liệu
                  </button>
                  <button class="approve-btn" @click="showApproveForm = true; selectedTopic = topic">
                    Duyệt
                  </button>
                  <button class="reject-btn" @click="handleReject(topic)">
                    Không duyệt
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Desktop Table View -->
          <div class="table-container desktop-only">
            <table class="research-table">
              <thead>
                <tr>
                  <!-- <th>Mã đề tài</th>
                  <th>Mã nhóm</th>   -->
                  <th>Tên đề tài</th>
                  <th>Hướng nghiên cứu</th>
                  <th>Đợt thực hiện</th>
                  <th>Trạng thái</th>
                  <th>Tiến độ</th>
                  <th>Điểm số</th>
                  <th>Giảng viên hướng dẫn</th>
                  <th>Thành viên</th>
                  <th>Tài liệu</th>
                  <th>Hành động</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="topic in paginatedTopics" :key="topic.ma_de_tai">
                  <!-- <td>{{ topic.ma_de_tai }}</td>
                  <td>{{ topic.ma_nhom }}</td> -->
                  <td>{{ topic.ten_de_tai }}</td>
                  <td>
                    <ul class="research-directions">
                      <li v-for="direction in topic.huong_nghien_cuu" :key="direction.ma_hnc">
                        {{ direction.ten_hnc }}
                      </li>
                    </ul>
                  </td>
                  <td>{{ topic.dot_thuc_hien }}</td>
                  <td>
                    <span :class="getStatusClass(topic.trang_thai)">
                      {{ getStatusText(topic.trang_thai) }}
                    </span>
                  </td>
                  <td>
                    <span class="progress-text">{{ getProgressText(topic) }}</span>
                  </td>
                  <td>{{ topic.diem_so }}</td>
                  <td>{{ topic.ten_gv }}</td>
                  <td>
                    <div class="members-list">
                      <div v-for="member in topic.thanh_vien" :key="member.ma_sv" class="member-item">
                        {{ member.ma_sv }} - {{ member.ten_sv }}
                      </div>
                    </div>
                  </td>
                  <td>
                    <div class="document-actions">
                      <button class="documents-btn" @click="showDocumentDetails(topic)">
                        Xem tài liệu
                      </button>
                    </div>
                  </td>
                  <td>
                    <div class="document-actions">
                      <button class="approve-btn" @click="showApproveForm = true; selectedTopic = topic">
                        Duyệt đề tài
                      </button>
                      <button class="reject-btn" @click="handleReject(topic)">
                        Không duyệt
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Document Details Modal -->
          <div v-if="selectedTopic" class="modal-overlay" @click="closeModal">
            <div class="modal-content" @click.stop>
              <div class="modal-header">
                <h3>Tài liệu đề tài: {{ selectedTopic.ten_de_tai }}</h3>
                <div class="modal-actions">
                  <button class="close-btn" @click="closeModal">&times;</button>
                </div>
              </div>
              <div class="modal-tabs">
                <button 
                  v-for="tab in documentTabs" 
                  :key="tab.id"
                  :class="['tab-button', { active: activeTab === tab.id }]"
                  @click="activeTab = tab.id"
                >
                  {{ tab.name }}
                </button>
              </div>
              <div class="modal-body">
                <!-- Đề cương đề tài -->
                <div v-if="activeTab === 'outline'" class="document-group">
                  <div v-for="(submission, index) in getDocumentsByType(1)" :key="index" class="document-section">
                    <div class="submission-header">
                      <h4>{{ getDocumentType(submission.loai_tai_lieu) }}</h4>
                      <div class="submission-info">
                        <span class="status" :class="{ 
                          'status-submitted': submission.trang_thai === 1,
                          'status-needs-update': submission.trang_thai === 3 || submission.trang_thai === 7
                        }">
                          {{ submission.trang_thai === 1 ? 'Đã nộp' : 
                             submission.trang_thai === 3 || submission.trang_thai === 7 ? 'Cần cập nhật' : 'Chưa nộp' }}
                        </span>
                        <span v-if="submission.thoi_gian_nop" class="submission-time">
                          Thời gian nộp: {{ formatDate(submission.thoi_gian_nop) }}
                        </span>
                      </div>
                    </div>
                    <div class="files-list">
                      <div v-for="(file, fileIndex) in submission.files" :key="fileIndex" class="file-item">
                        <a :href="file.link_tep" target="_blank" class="file-link">
                          {{ getFileName(file.link_tep) }}
                        </a>
                      </div>
                    </div>
                    <div class="feedback-section">
                      <textarea 
                        v-model="submission.feedback" 
                        class="feedback-input" 
                        :placeholder="getPlaceholderText(submission)"
                      ></textarea>
                      <div class="feedback-actions">
                        <button 
                          class="submit-feedback-btn" 
                          @click="handleFeedback(selectedTopic, submission.files[0], submission.feedback)"
                        >
                          Gửi ý kiến
                        </button>
                        <button 
                          class="update-required-btn" 
                          @click="handleUpdateRequest(selectedTopic, submission.files[0], submission.feedback, submission.loai_tai_lieu)"
                        >
                          Yêu cầu cập nhật
                        </button>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Báo cáo cấp khoa -->
                <div v-if="activeTab === 'faculty'" class="document-group">
                  <div v-for="(submission, index) in getDocumentsByType(3)" :key="index" class="document-section">
                    <div class="submission-header">
                      <h4>{{ getDocumentType(submission.loai_tai_lieu) }}</h4>
                      <div class="submission-info">
                        <span class="status" :class="{ 
                          'status-submitted': submission.trang_thai === 1,
                          'status-needs-update': submission.trang_thai === 3 || submission.trang_thai === 7
                        }">
                          {{ submission.trang_thai === 1 ? 'Đã nộp' : 
                             submission.trang_thai === 3 || submission.trang_thai === 7 ? 'Cần cập nhật' : 'Chưa nộp' }}
                        </span>
                        <span v-if="submission.thoi_gian_nop" class="submission-time">
                          Thời gian nộp: {{ formatDate(submission.thoi_gian_nop) }}
                        </span>
                      </div>
                    </div>
                    <div class="files-list">
                      <div v-for="(file, fileIndex) in submission.files" :key="fileIndex" class="file-item">
                        <a :href="file.link_tep" target="_blank" class="file-link">
                          {{ getFileName(file.link_tep) }}
                        </a>
                      </div>
                    </div>
                    <div class="feedback-section">
                      <textarea 
                        v-model="submission.feedback" 
                        class="feedback-input" 
                        :placeholder="getPlaceholderText(submission)"
                      ></textarea>
                      <div class="feedback-actions">
                        <button 
                          class="submit-feedback-btn" 
                          @click="handleFeedback(selectedTopic, submission.files[0], submission.feedback)"
                        >
                          Gửi ý kiến
                        </button>
                        <button 
                          class="update-required-btn" 
                          @click="handleUpdateRequest(selectedTopic, submission.files[0], submission.feedback, submission.loai_tai_lieu)"
                        >
                          Yêu cầu cập nhật
                        </button>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Báo cáo cấp trường -->
                <div v-if="activeTab === 'school'" class="document-group">
                  <div v-for="(submission, index) in getDocumentsByType(5)" :key="index" class="document-section">
                    <div class="submission-header">
                      <h4>{{ getDocumentType(submission.loai_tai_lieu) }}</h4>
                      <div class="submission-info">
                        <span class="status" :class="{ 
                          'status-submitted': submission.trang_thai === 1,
                          'status-needs-update': submission.trang_thai === 3 || submission.trang_thai === 7
                        }">
                          {{ submission.trang_thai === 1 ? 'Đã nộp' : 
                             submission.trang_thai === 3 || submission.trang_thai === 7 ? 'Cần cập nhật' : 'Chưa nộp' }}
                        </span>
                        <span v-if="submission.thoi_gian_nop" class="submission-time">
                          Thời gian nộp: {{ formatDate(submission.thoi_gian_nop) }}
                        </span>
                      </div>
                    </div>
                    <div class="files-list">
                      <div v-for="(file, fileIndex) in submission.files" :key="fileIndex" class="file-item">
                        <a :href="file.link_tep" target="_blank" class="file-link">
                          {{ getFileName(file.link_tep) }}
                        </a>
                      </div>
                    </div>
                    <div class="feedback-section">
                      <textarea 
                        v-model="submission.feedback" 
                        class="feedback-input" 
                        :placeholder="getPlaceholderText(submission)"
                      ></textarea>
                      <div class="feedback-actions">
                        <button 
                          class="submit-feedback-btn" 
                          @click="handleFeedback(selectedTopic, submission.files[0], submission.feedback)"
                        >
                          Gửi ý kiến
                        </button>
                        <button 
                          class="update-required-btn" 
                          @click="handleUpdateRequest(selectedTopic, submission.files[0], submission.feedback, submission.loai_tai_lieu)"
                        >
                          Yêu cầu cập nhật
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Approve Form Modal -->
          <div v-if="showApproveForm" class="modal-overlay" @click="showApproveForm = false">
            <div class="approve-form" @click.stop>
              <div class="form-header">
                <h3>Duyệt đề tài</h3>
                <button class="close-btn" @click="showApproveForm = false">&times;</button>
              </div>
              <div class="form-body">
                <div class="form-group">
                  <label for="score">Điểm số:</label>
                  <input 
                    type="number" 
                    id="score" 
                    v-model="approveScore" 
                    min="0" 
                    max="10" 
                    step="0.1"
                    class="score-input"
                  />
                </div>
                <div class="form-actions">
                  <button class="cancel-btn" @click="showApproveForm = false">Hủy</button>
                  <button class="submit-btn" @click="handleApprove">Xác nhận</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <!-- <footer class="footer">
      <Footer class="footer-content" />
    </footer> -->
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import SidebarManagerToNCKH from '@/components/SidebarManagerToNCKH.vue';
import Footer from '@/components/Footer.vue';
import api from '@/config/api';

// State
const researchTopics = ref([]);
const selectedTopic = ref(null);
const loading = ref(true);
const currentPage = ref(1);
const itemsPerPage = 20;
const showFilters = ref(false);

// Filter state
const filters = ref({
  tenDeTai: '',
  tenGv: '',
  tenThanhVien: '',
  huongNghienCuu: '',
  tienDo: ''
});

// Mapping for progress status
const MAP_DE_TAI_NCKHSV_TIEN_DO = {
  1: "Chưa nộp đề cương",
  2: "Đã nộp đề cương",
  3: "Chưa bổ sung đề cương chỉnh sửa",
  4: "Đã nộp đề cương bổ sung chỉnh sửa",
  5: "Chưa nộp báo cáo",
  6: "Đã nộp báo cáo",
  7: "Chưa bổ sung báo cáo chỉnh sửa",
  8: "Đã nộp báo cáo bổ sung chỉnh sửa"
};

// Sidebar state
const isSidebarOpen = ref(false);
const isMobile = ref(window.innerWidth <= 768);

// Toggle sidebar
const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value;
  if (isSidebarOpen.value) {
    document.body.style.overflow = 'hidden';
  } else {
    document.body.style.overflow = '';
  }
};

// Close sidebar
const closeSidebar = () => {
  isSidebarOpen.value = false;
  document.body.style.overflow = '';
};

// Handle responsive sidebar
const handleResize = () => {
  isMobile.value = window.innerWidth <= 768;
  if (!isMobile.value && isSidebarOpen.value) {
    isSidebarOpen.value = false;
  }
};

// Auth store
const router = useRouter();
const authStore = useAuthStore();
const { isAuthenticated, storedEmail, logout } = authStore;

// Functions
const handleLogout = () => {
  logout();
  router.push('/login');
};

const getStatusClass = (status) => {
  switch (status) {
    case 0: return 'status-pending';
    case 1: return 'status-in-progress';
    case 2: return 'status-completed';
    default: return 'status-unknown';
  }
};

const getStatusText = (status) => {
  switch (status) {
    case 0: return 'Đã hủy';
    case 1: return 'Đang thực hiện';
    case 2: return 'Hoàn thành';
    default: return 'Không xác định';
  }
};

const getProgressText = (topic) => {
  if (!topic.tai_lieu || topic.tai_lieu.length === 0) {
    return MAP_DE_TAI_NCKHSV_TIEN_DO[1]; // "Chưa nộp đề cương"
  }
  
  // Lấy tài liệu mới nhất cho mỗi loại
  const latestDocs = {};
  topic.tai_lieu.forEach(doc => {
    if (!latestDocs[doc.loai_tai_lieu] || 
        new Date(doc.thoi_gian_nop) > new Date(latestDocs[doc.loai_tai_lieu].thoi_gian_nop)) {
      latestDocs[doc.loai_tai_lieu] = doc;
    }
  });

  // Kiểm tra từng giai đoạn
  if (latestDocs[5]) { // Báo cáo cấp trường
    if (latestDocs[5].trang_thai === 8) {
      return MAP_DE_TAI_NCKHSV_TIEN_DO[8];
    } else if (latestDocs[5].trang_thai === 1) {
      return MAP_DE_TAI_NCKHSV_TIEN_DO[6];
    } else if (latestDocs[5].trang_thai === 7) {
      return MAP_DE_TAI_NCKHSV_TIEN_DO[7];
    }
  } else if (latestDocs[3]) { // Báo cáo cấp khoa
    if (latestDocs[3].trang_thai === 8) {
      return MAP_DE_TAI_NCKHSV_TIEN_DO[8];
    } else if (latestDocs[3].trang_thai === 1) {
      return MAP_DE_TAI_NCKHSV_TIEN_DO[6];
    } else if (latestDocs[3].trang_thai === 7) {
      return MAP_DE_TAI_NCKHSV_TIEN_DO[7];
    }
  } else if (latestDocs[1]) { // Đề cương
    if (latestDocs[1].trang_thai === 4) {
      return MAP_DE_TAI_NCKHSV_TIEN_DO[4];
    } else if (latestDocs[1].trang_thai === 1) {
      return MAP_DE_TAI_NCKHSV_TIEN_DO[2];
    } else if (latestDocs[1].trang_thai === 3) {
      return MAP_DE_TAI_NCKHSV_TIEN_DO[3];
    }
  }

  return MAP_DE_TAI_NCKHSV_TIEN_DO[1]; // "Chưa nộp đề cương"
};

const getDocumentType = (type) => {
  switch (type) {
    case 1: return 'Đề cương đề tài';
    case 2: return 'Đề cương chỉnh sửa';
    case 3: return 'Báo cáo cấp khoa';
    case 4: return 'Báo cáo cấp khoa chỉnh sửa';
    case 5: return 'Báo cáo cấp trường';
    case 6: return 'Báo cáo cấp trường chỉnh sửa';
    default: return 'Tài liệu khác';
  }
};

const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleString('vi-VN');
};

const getFileName = (path) => {
  if (!path) return '';
  return path.split('\\').pop();
};

const showDocumentDetails = (topic) => {
  selectedTopic.value = topic;
  // Reset feedback cho mỗi submission
  if (topic.tai_lieu) {
    topic.tai_lieu.forEach(doc => {
      doc.feedback = '';
    });
  }
};

const closeModal = () => {
  selectedTopic.value = null;
};

const handleFeedback = async (topic, document, feedback) => {
  try {
    const response = await api.patch(`tonckh/tailieu/capnhat_trangthai/${document.ma_tai_lieu}`, null, {
      params: {
        trang_thai: document.trang_thai // Giữ nguyên trạng thái hiện tại
      }
    });
    if (response.status === 200) {
      await fetchResearchTopics();
      alert('Đã gửi ý kiến thành công!');
    }
  } catch (error) {
    console.error('Error sending feedback:', error);
    alert('Có lỗi xảy ra khi gửi ý kiến');
  }
};

const handleUpdateRequest = async (topic, document, feedback, documentType) => {
  try {
    let status;
    switch (documentType) {
      case 1: // Đề cương
        status = 3; // Chưa bổ sung đề cương chỉnh sửa
        break;
      case 3: // Báo cáo cấp khoa
      case 5: // Báo cáo cấp trường
        status = 7; // Chưa bổ sung báo cáo chỉnh sửa
        break;
      default:
        status = 3;
    }

    const response = await api.patch(`tonckh/tailieu/capnhat_trangthai/${document.ma_tai_lieu}`, null, {
      params: {
        trang_thai: status
      }
    });
    
    if (response.status === 200) {
      await fetchResearchTopics();
      alert('Đã yêu cầu cập nhật thành công!');
    }
  } catch (error) {
    console.error('Error requesting update:', error);
    alert('Có lỗi xảy ra khi yêu cầu cập nhật');
  }
};

// Thêm hàm mới để lấy placeholder text
const getPlaceholderText = (submission) => {
  if (!submission.files || submission.files.length === 0) return 'Nhập ý kiến đóng góp...';
  
  const latestFile = submission.files[0];
  if (latestFile.phan_hoi) {
    return `Ý kiến gần nhất: ${latestFile.phan_hoi}`;
  }
  return 'Nhập ý kiến đóng góp...';
};

// Thêm hàm để tính toán tiến độ dựa trên trạng thái
const calculateProgress = (topic) => {
  if (!topic.tai_lieu || topic.tai_lieu.length === 0) return 0;
  
  // Lấy tài liệu mới nhất cho mỗi loại
  const latestDocs = {};
  topic.tai_lieu.forEach(doc => {
    if (!latestDocs[doc.loai_tai_lieu] || 
        new Date(doc.thoi_gian_nop) > new Date(latestDocs[doc.loai_tai_lieu].thoi_gian_nop)) {
      latestDocs[doc.loai_tai_lieu] = doc;
    }
  });

  // Tính tiến độ dựa trên trạng thái của các tài liệu
  let progress = 0;
  
  // Kiểm tra đề cương
  if (latestDocs[1]) {
    if (latestDocs[1].trang_thai === 1) progress = 25; // Đã nộp đề cương
    else if (latestDocs[1].trang_thai === 4) progress = 30; // Đã nộp đề cương bổ sung
  }
  
  // Kiểm tra báo cáo cấp khoa
  if (latestDocs[3]) {
    if (latestDocs[3].trang_thai === 1) progress = 50; // Đã nộp báo cáo cấp khoa
    else if (latestDocs[3].trang_thai === 8) progress = 60; // Đã nộp báo cáo cấp khoa bổ sung
  }
  
  // Kiểm tra báo cáo cấp trường
  if (latestDocs[5]) {
    if (latestDocs[5].trang_thai === 1) progress = 75; // Đã nộp báo cáo cấp trường
    else if (latestDocs[5].trang_thai === 8) progress = 100; // Đã nộp báo cáo cấp trường bổ sung
  }
  
  return progress;
};

// Fetch research topics
const fetchResearchTopics = async (filter = 'all') => {
  try {
    loading.value = true;

    if (filter === 'all') {
      const [resTrue, resFalse] = await Promise.all([
        api.get('tonckh/detai_sv', { params: { is_doing: true } }),
        api.get('tonckh/detai_sv', { params: { is_doing: false } }),
      ]);
      researchTopics.value = [...resTrue.data, ...resFalse.data];
    } else {
      const is_doing = filter === 'doing';
      const response = await api.get('tonckh/detai_sv', { params: { is_doing } });
      researchTopics.value = response.data;
    }

  } catch (error) {
    console.error('Error fetching research topics:', error);
  } finally {
    loading.value = false;
  }
};

// Thêm computed property để nhóm các tài liệu
const groupedDocuments = computed(() => {
  if (!selectedTopic.value?.tai_lieu) return [];
  
  // Nhóm các tài liệu theo loại và thời gian nộp
  const groupedByTypeAndTime = selectedTopic.value.tai_lieu.reduce((acc, doc) => {
    const key = `${doc.loai_tai_lieu}_${doc.thoi_gian_nop}`;
    if (!acc[key]) {
      acc[key] = {
        loai_tai_lieu: doc.loai_tai_lieu,
        trang_thai: doc.trang_thai,
        thoi_gian_nop: doc.thoi_gian_nop,
        files: []
      };
    }
    acc[key].files.push(doc);
    return acc;
  }, {});

  // Chuyển đổi object thành array và sắp xếp theo thời gian
  return Object.values(groupedByTypeAndTime).sort((a, b) => 
    new Date(b.thoi_gian_nop || 0) - new Date(a.thoi_gian_nop || 0)
  );
});

const updateStatus = async (topic, document, status) => {
  const response = await api.patch(`tonckh/detai/capnhat_trangthai/${document.ma_de_tai}`, null, {
    params: {
      trang_thai: 2,
    }
  });
}

// Add these new refs and computed properties in the script setup section
const activeTab = ref('outline');
const documentTabs = [
  { id: 'outline', name: 'Đề cương đề tài' },
  { id: 'faculty', name: 'Báo cáo cấp khoa' },
  { id: 'school', name: 'Báo cáo cấp trường' }
];

const getDocumentsByType = (type) => {
  if (!selectedTopic.value?.tai_lieu) return [];
  return groupedDocuments.value.filter(doc => doc.loai_tai_lieu === type);
};

// Add these new refs and functions in the script setup section
const showApproveForm = ref(false);
const approveScore = ref(0);

const handleApprove = async () => {
  try {
    if (approveScore.value < 0 || approveScore.value > 100) {
      alert('Điểm số phải từ 0 đến 100');
      return;
    }

    const response = await api.patch(`tonckh/detai/capnhat_trangthai/${selectedTopic.value.ma_de_tai}`, null, {
      params: {
        trang_thai: 2,
        tien_do: 8,
        diem_so: approveScore.value
      }
    });

    if (response.status === 200) {
      alert('Đã duyệt đề tài thành công!');
      showApproveForm.value = false;
      await fetchResearchTopics();
      closeModal();
    }
  } catch (error) {
    console.error('Error approving topic:', error);
    alert('Có lỗi xảy ra khi duyệt đề tài');
  }
};

const handleReject = async (topic) => {
  try {
    const response = await api.patch(`tonckh/detai/capnhat_trangthai/${topic.ma_de_tai}`, null, {
      params: {
        trang_thai: 0
      }
    });

    if (response.status === 200) {
      alert('Đã từ chối đề tài thành công!');
      await fetchResearchTopics();
    }
  } catch (error) {
    console.error('Error rejecting topic:', error);
    alert('Có lỗi xảy ra khi từ chối đề tài');
  }
};

// Computed properties for pagination and filtering
const filteredTopics = computed(() => {
  return researchTopics.value.filter(topic => {
    const matchesTenDeTai = !filters.value.tenDeTai || 
      topic.ten_de_tai.toLowerCase().includes(filters.value.tenDeTai.toLowerCase());
    
    const matchesTenGv = !filters.value.tenGv || 
      topic.ten_gv.toLowerCase().includes(filters.value.tenGv.toLowerCase());
    
    const matchesTenThanhVien = !filters.value.tenThanhVien || 
      topic.thanh_vien.some(member => 
        member.ten_sv.toLowerCase().includes(filters.value.tenThanhVien.toLowerCase())
      );
    
    const matchesHuongNghienCuu = !filters.value.huongNghienCuu || 
      topic.huong_nghien_cuu.some(direction => 
        direction.ten_hnc.toLowerCase().includes(filters.value.huongNghienCuu.toLowerCase())
      );
    
    const matchesTienDo = !filters.value.tienDo || 
      getProgressText(topic).toLowerCase().includes(filters.value.tienDo.toLowerCase());

    return matchesTenDeTai && matchesTenGv && matchesTenThanhVien && 
           matchesHuongNghienCuu && matchesTienDo;
  });
});

const totalPages = computed(() => {
  return Math.ceil(filteredTopics.value.length / itemsPerPage);
});

const paginatedTopics = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return filteredTopics.value.slice(start, end);
});

// Function to reset filters
const resetFilters = () => {
  filters.value = {
    tenDeTai: '',
    tenGv: '',
    tenThanhVien: '',
    huongNghienCuu: '',
    tienDo: ''
  };
  currentPage.value = 1;  
};

onMounted(() => {
  window.addEventListener('resize', handleResize);
  handleResize();
  authStore.loadUserFromStorage();
  fetchResearchTopics('doing');
});

onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
});
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  overflow-y: auto;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
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

.sidebar-open {
  left: 0;
}

.sidebar ul {
  list-style: none;
  padding: 20px;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.sidebar li {
  padding: 12px 0;
  position: relative;
  transition: all 0.3s ease;
}

.sidebar li::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 1px;
  background: rgba(255, 255, 255, 0.1);
}

.sidebar li:last-child::after {
  display: none;
}

.sidebar a {
  color: #ffffff;
  text-decoration: none;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  display: block;
  padding: 10px 15px;
  border-radius: 8px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  font-weight: 500;
}

.sidebar a::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.1);
  transform: translateX(-100%);
  transition: transform 0.3s ease;
}

.sidebar a:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateX(5px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.sidebar a:hover::before {
  transform: translateX(0);
}

.sidebar a.router-link-active {
  background: rgba(255, 255, 255, 0.2);
  font-weight: 600;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
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

.content {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h2 {
  color: #0082c6;
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e6f2ff;
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

.card-title {
  font-weight: 600;
  color: #0082c6;
  font-size: 14px;
}

.card-status {
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
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
  flex-direction: column;
  gap: 0.5rem;
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #e2e8f0;
}

.documents-btn, .approve-btn, .reject-btn {
  width: 100%;
  padding: 0.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
  text-align: center;
}

.documents-btn {
  background: #0082c6;
  color: white;
}

.documents-btn:hover {
  background: #0069a3;
  transform: translateY(-2px);
}

.approve-btn {
  background: #10b981;
  color: white;
}

.approve-btn:hover {
  background: #059669;
  transform: translateY(-2px);
}

.reject-btn {
  background: #ef4444;
  color: white;
}

.reject-btn:hover {
  background: #dc2626;
  transform: translateY(-2px);
}

.table-container {
  overflow-x: auto;
  margin-bottom: 2rem;
}

.research-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
}

.research-table th,
.research-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #e6f2ff;
}

.research-table th {
  background: #f0f7ff;
  color: #0082c6;
  font-weight: 600;
}

.research-table tr:hover {
  background: #f8fafc;
}

.status-pending {
  color: #f59e0b;
  font-weight: 500;
}

.status-in-progress {
  color: #0082c6;
  font-weight: 500;
}

.status-completed {
  color: #10b981;
  font-weight: 500;
}

.progress-text {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.9rem;
  font-weight: 500;
  background: #f0f7ff;
  color: #0082c6;
  border: 1px solid #e6f2ff;
}

.members-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.member-item {
  padding: 0.5rem;
  background: #f8fafc;
  border-radius: 4px;
  font-size: 0.9rem;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  width: 80%;
  max-width: 1000px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.modal-header {
  padding: 1rem;
  border-bottom: 1px solid #e6f2ff;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  color: #0082c6;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #94a3b8;
}

.modal-tabs {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  border-bottom: 1px solid #e6f2ff;
  background: #f8fafc;
}

.tab-button {
  padding: 0.75rem 1.5rem;
  border: none;
  background: none;
  color: #64748b;
  font-weight: 500;
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.3s ease;
}

.tab-button:hover {
  background: #e6f2ff;
  color: #0082c6;
}

.tab-button.active {
  background: #0082c6;
  color: white;
}

.document-section {
  margin-bottom: 2rem;
  padding: 1rem;
  background: white;
  border-radius: 8px;
  border: 1px solid #e6f2ff;
}

.document-section:last-child {
  margin-bottom: 0;
}

.submission-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #e6f2ff;
}

.submission-header h4 {
  color: #0082c6;
  margin: 0;
  font-size: 1.1rem;
}

.submission-info {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.5rem;
}

.status {
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.9rem;
  background: #f1f5f9;
  color: #64748b;
}

.status-submitted {
  background: #dcfce7;
  color: #16a34a;
}

.status-needs-update {
  color: #f59e0b;
  font-weight: 500;
}

.submission-time {
  font-size: 0.9rem;
  color: #64748b;
}

.files-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.file-item {
  padding: 0.5rem;
  background: white;
  border-radius: 4px;
  border: 1px solid #e6f2ff;
  transition: all 0.3s ease;
}

.file-item:hover {
  background: #f0f7ff;
  transform: translateX(5px);
}

.file-link {
  color: #0082c6;
  text-decoration: none;
  display: block;
  width: 100%;
}

.file-link:hover {
  text-decoration: underline;
}

/* User Email */
.user-email {
  max-width: 150px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
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

  .card-actions {
    flex-direction: column;
  }
  
  .card-actions button {
    width: 100%;
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

.feedback-section {
  margin-top: 1rem;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e6f2ff;
}

.feedback-input {
  width: 100%;
  min-height: 100px;
  padding: 0.75rem;
  border: 2px solid #e6f2ff;
  border-radius: 6px;
  margin-bottom: 1rem;
  resize: vertical;
  font-family: inherit;
}

.feedback-input:focus {
  outline: none;
  border-color: #0082c6;
}

.submit-feedback-btn {
  padding: 0.75rem 1.5rem;
  background: #0082c6;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.submit-feedback-btn:hover {
  background: #0069a3;
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.update-required-btn {
  padding: 0.75rem 1.5rem;
  background: #f59e0b;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.update-required-btn:hover {
  background: #e58e0b;
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.modal-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.approve-form {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.form-header {
  padding: 1rem;
  border-bottom: 1px solid #e6f2ff;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.form-header h3 {
  color: #0082c6;
  margin: 0;
}

.form-body {
  padding: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #4b5563;
  font-weight: 500;
}

.score-input {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e6f2ff;
  border-radius: 6px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.score-input:focus {
  outline: none;
  border-color: #0082c6;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}

.cancel-btn {
  padding: 0.75rem 1.5rem;
  background: #e5e7eb;
  color: #4b5563;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
}

.cancel-btn:hover {
  background: #d1d5db;
}

.submit-btn {
  padding: 0.75rem 1.5rem;
  background: #10b981;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
}

.submit-btn:hover {
  background: #059669;
  transform: translateY(-2px);
}

.document-actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

/* Content Header */
.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.toggle-filter-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: #0082c6;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
}

.toggle-filter-btn:hover {
  background: #0069a3;
  transform: translateY(-2px);
}

.toggle-filter-btn i {
  font-size: 1rem;
}

/* Filter Section Styles */
.filter-section {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease-out, opacity 0.3s ease-out;
  opacity: 0;
}

.filter-section-visible {
  max-height: 500px;
  opacity: 1;
}

.filter-form {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 1.5rem;
}

.filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.filter-row:last-child {
  margin-bottom: 0;
}

.filter-group {
  flex: 1 1 300px;
}

.filter-group label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  color: #1a3c5e;
  font-weight: 600;
  font-size: 0.95rem;
}

.filter-group label i {
  color: #0082c6;
  font-size: 1rem;
}

.filter-group input,
.filter-group select {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: all 0.3s ease;
  background-color: #f8fafc;
}

.filter-group input:focus,
.filter-group select:focus {
  outline: none;
  border-color: #0082c6;
  box-shadow: 0 0 0 3px rgba(0, 130, 198, 0.1);
  background-color: white;
}

.filter-actions {
  display: flex;
  align-items: flex-end;
  justify-content: flex-end;
  flex: 1 1 300px;
}

.reset-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: #f3f4f6;
  color: #4b5563;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
}

.reset-btn:hover {
  background: #e5e7eb;
  color: #1f2937;
  transform: translateY(-2px);
}

.reset-btn i {
  font-size: 0.9rem;
}

.toggle-filter-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: #0082c6;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
}

.toggle-filter-btn:hover {
  background: #0069a3;
  transform: translateY(-2px);
}

.toggle-filter-btn i {
  font-size: 1rem;
}

@media (max-width: 768px) {
  .filter-row {
    flex-direction: column;
    gap: 1rem;
  }

  .filter-group {
    flex: 1 1 100%;
  }

  .filter-actions {
    justify-content: center;
    margin-top: 1rem;
  }

  .toggle-filter-btn {
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
  }
}
</style>