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
            <h2>Danh sách đề tài</h2>
          </div>
          <div class="filter-section" style="display: flex; align-items: center; gap: 10px;">
            <button class="filter-btn" @click="toggleFilter">
              {{ showFilter ? 'Ẩn bộ lọc' : 'Hiện bộ lọc' }}
            </button>
          </div>
          
          <!-- Filter Section -->
          <div v-if="showFilter" class="filter-form">
            <div class="filter-row">
              <div>
                <label class="label">Tên đề tài</label>
                <input type="text" v-model="filterCriteria.ten_de_tai" class="input-field" />
              </div>
              <div>
                <label class="label">Tên giảng viên</label>
                <input type="text" v-model="filterCriteria.ten_gv" class="input-field" />
              </div>
              <div>
                <label class="label">Tên thành viên</label>
                <input type="text" v-model="filterCriteria.ten_thanh_vien" class="input-field" />
              </div>
              <div>
                <label class="label">Trạng thái</label>
                <select v-model="filterCriteria.trang_thai" class="input-field">
                  <option value="">Tất cả</option>
                  <option value="0">Đã hủy</option>
                  <option value="1">Đang thực hiện</option>
                  <option value="2">Hoàn thành</option>
                </select>
              </div>
              <div>
                <label class="label">Tiến độ</label>
                <input type="text" v-model="filterCriteria.tien_do" class="input-field" />
              </div>
            </div>
            <div class="filter-actions">
              <button class="reset-btn" @click="resetFilters">Đặt lại</button>
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
                  <span class="label">Hướng nghiên cứu:</span>
                  <span class="value">{{ topic.ma_hnc }}</span>
                </div>
                <div class="card-item">
                  <span class="label">Đợt thực hiện:</span>
                  <span class="value">{{ topic.dot_thuc_hien }}</span>
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
                  <button class="documents-btn" @click="viewDocuments(topic)">
                    <i class="fas fa-eye"></i> Xem tài liệu
                  </button>
                  <button class="delete-btn" @click="handleDelete(topic)">
                    <i class="fas fa-trash"></i> Xóa
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
                  <th>Điểm số</th>
                  <th>Giảng viên hướng dẫn</th>
                  <th>Thành viên</th>
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
                      <button class="documents-btn" @click="viewDocuments(topic)">
                        <i class="fas fa-eye"></i> Xem tài liệu
                      </button>
                      <button class="delete-btn" @click="handleDelete(topic)">
                        <i class="fas fa-trash"></i> Xóa
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
                  <button class="close-btn" @click="closeModal">×</button>
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
                <!-- Document Groups -->
                <div class="document-group">
                  <div v-for="(group, index) in groupedDocuments[activeTab]" :key="index" class="document-section">
                    <div class="submission-header">
                      <h4>{{ group.name }} (Nộp lúc: {{ formatDate(group.thoi_gian_nop) }})</h4>
                      <div class="submission-info">
                        <span class="status" :class="{ 
                          'status-submitted': group.trang_thai === 1,
                          'status-needs-update': group.trang_thai === 3 || group.trang_thai === 7
                        }">
                          {{ group.trang_thai === 1 ? 'Đã nộp' : 
                             group.trang_thai === 3 || group.trang_thai === 7 ? 'Cần cập nhật' : 'Chưa nộp' }}
                        </span>
                        <span v-if="group.phan_hoi" class="submission-feedback">
                          Phản hồi: {{ group.phan_hoi }}
                        </span>
                      </div>
                    </div>
                    <div class="files-list">
                      <div v-for="(file, fileIndex) in group.files" :key="fileIndex" class="file-item">
                        <a :href="file.link_tep" target="_blank" class="file-link">
                          {{ getFileName(file.link_tep) }}
                        </a>
                      </div>
                    </div>
                  </div>
                  <div v-if="!groupedDocuments[activeTab]?.length">Không có tài liệu nào cho loại này.</div>
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
import { ref, onMounted, onUnmounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import SidebarManagerToNCKH from '@/components/SidebarManagerToNCKH.vue';
import api from '@/config/api';

// State
const topics = ref([]);
const selectedTopic = ref(null);
const loading = ref(true);
const currentPage = ref(1);
const itemsPerPage = 20;
const showFilter = ref(false);

// Filter state
const filterCriteria = ref({
  ten_de_tai: '',
  ten_gv: '',
  ten_thanh_vien: '',
  trang_thai: '',
  tien_do: ''
});

// Add new state for research directions
const huongNghienCuuList = ref([]);

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

// Document tabs
const activeTab = ref('outline');
const documentTabs = [
  { id: 'outline', name: 'Đề cương đề tài' },
  { id: 'faculty', name: 'Báo cáo cấp khoa' },
  { id: 'school', name: 'Báo cáo cấp trường' }
];

// Toggle bộ lọc
const toggleFilter = () => {
  showFilter.value = !showFilter.value;
};

// Add function to fetch research directions
async function fetchHuongNghienCuu() {
  try {
    const response = await api.get('get_data/hnc/');
    const data = response.data;
    if (Array.isArray(data)) {
      huongNghienCuuList.value = data;
    }
  } catch (err) {
    console.error('Lỗi khi lấy danh sách hướng nghiên cứu:', err);
  }
}

// Computed property cho danh sách đã lọc
const filteredTopics = computed(() => {
  return topics.value.filter(item => {
    const tenDeTaiMatch = !filterCriteria.value.ten_de_tai || 
      item.ten_de_tai.toLowerCase().includes(filterCriteria.value.ten_de_tai.toLowerCase());
    const tenGvMatch = !filterCriteria.value.ten_gv || 
      item.ten_gv.toLowerCase().includes(filterCriteria.value.ten_gv.toLowerCase());
    const tenThanhVienMatch = !filterCriteria.value.ten_thanh_vien || 
      item.thanh_vien.some(member => 
        member.ten_sv.toLowerCase().includes(filterCriteria.value.ten_thanh_vien.toLowerCase())
      );
    const trangThaiMatch = !filterCriteria.value.trang_thai || 
      item.trang_thai === parseInt(filterCriteria.value.trang_thai);
    const tienDoMatch = !filterCriteria.value.tien_do || 
      item.tien_do.toLowerCase().includes(filterCriteria.value.tien_do.toLowerCase());

    return tenDeTaiMatch && tenGvMatch && tenThanhVienMatch && trangThaiMatch && tienDoMatch;
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
  filterCriteria.value = {
    ten_de_tai: '',
    ten_gv: '',
    ten_thanh_vien: '',
    trang_thai: '',
    tien_do: ''
  };
  currentPage.value = 1;
};

// Computed: Group documents by submission time
const groupedDocuments = computed(() => {
  if (!selectedTopic.value?.tai_lieu) {
    console.warn('No tai_lieu found for selectedTopic:', selectedTopic.value);
    return {
      outline: [],
      faculty: [],
      school: []
    };
  }

  const typeMap = {
    outline: [1, 2], // Đề cương đề tài và chỉnh sửa
    faculty: [3, 4], // Báo cáo cấp khoa và chỉnh sửa
    school: [5, 6]   // Báo cáo cấp trường và chỉnh sửa
  };

  // Initialize result
  const result = {
    outline: [],
    faculty: [],
    school: []
  };

  // Group documents by thoi_gian_nop
  const groupsByTime = {};
  selectedTopic.value.tai_lieu.forEach(doc => {
    const tabId = Object.keys(typeMap).find(tab => typeMap[tab].includes(doc.loai_tai_lieu));
    if (!tabId) return; // Skip if loai_tai_lieu doesn't match any tab

    const timeKey = doc.thoi_gian_nop;
    if (!groupsByTime[tabId]) groupsByTime[tabId] = {};
    if (!groupsByTime[tabId][timeKey]) {
      groupsByTime[tabId][timeKey] = {
        name: getDocumentType(doc.loai_tai_lieu),
        thoi_gian_nop: doc.thoi_gian_nop,
        trang_thai: doc.trang_thai,
        phan_hoi: doc.phan_hoi,
        files: []
      };
    }

    groupsByTime[tabId][timeKey].files.push({
      link_tep: doc.link_tep
    });

    // Update trang_thai and phan_hoi if this document has higher priority (e.g., trang_thai = 3 over 1)
    if (doc.trang_thai === 3 || doc.trang_thai === 7) {
      groupsByTime[tabId][timeKey].trang_thai = doc.trang_thai;
      groupsByTime[tabId][timeKey].phan_hoi = doc.phan_hoi;
    }
  });

  // Convert groups to arrays
  for (const tabId in groupsByTime) {
    result[tabId] = Object.values(groupsByTime[tabId]).sort((a, b) => 
      new Date(b.thoi_gian_nop) - new Date(a.thoi_gian_nop) // Sort by newest first
    );
  }

  console.log('Grouped documents:', result);
  return result;
});

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

const getDocumentType = (type) => {
  switch (type) {
    case 1: return 'Đề cương đề tài';
    case 2: return 'Đề cương chỉnh sửa';
    case 3: return 'Báo cáo cấp khoa';
    case 4: return 'Báo cáo cấp khoa chỉnh sửa';
    case 5: return 'Báo cáo cấp trường';
    case 6: return 'Báo cáo cấp trường chỉnh sửa';
    default: return `Tài liệu khác (${type})`;
  }
};

const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleString('vi-VN');
};

const getFileName = (path) => {
  if (!path) return 'Không có tên file';
  return path.split(/[\\/]/).pop();
};

const viewDocuments = (topic) => {
  selectedTopic.value = topic;
  console.log('Selected topic:', topic);
  console.log('Active tab:', activeTab.value);
};

const closeModal = () => {
  selectedTopic.value = null;
};

// Fetch topics
const fetchTopics = async () => {
  try {
    loading.value = true;
    const response = await api.get('get_data/detai_sv');
    topics.value = response.data;
    console.log('topics.value', topics.value);
  } catch (error) {
    console.error('Error fetching topics:', error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  window.addEventListener('resize', handleResize);
  handleResize();
  authStore.loadUserFromStorage();
  fetchTopics();
  fetchHuongNghienCuu();
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

/* Content Header */
.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.filter-btn {
  background: #0082c6;
  color: white;
  border: none;
  padding: 8px 20px;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s;
  font-size: 0.9rem;
  white-space: nowrap;
  margin-bottom: 20px;
  margin-top: -20px;
}

.filter-btn:hover {
  background: #0069a3;
}

/* Filter section */
.filter-form {
  border: 1px solid #d1dbe3;
  padding: 15px;
  border-radius: 10px;
  background: white;
  margin-bottom: 20px;
  position: sticky;
  top: 100px;
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

.filter-row input.input-field,
.filter-row select.input-field {
  width: 100%;
  padding: 8px;
  border: 1px solid #d1dbe3;
  border-radius: 6px;
  font-size: 14px;
  background-color: #f9fafb;
  transition: border-color 0.3s, box-shadow 0.3s, background-color 0.3s;
}

.filter-row input.input-field:focus,
.filter-row select.input-field:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2);
  background-color: white;
  outline: none;
}

.filter-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 15px;
  gap: 10px;
}

.reset-btn {
  padding: 8px 20px;
  background: #f3f4f6;
  color: #4b5563;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
}

.reset-btn:hover {
  background: #e5e7eb;
  color: #1f2937;
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

.documents-btn, .delete-btn {
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

.delete-btn {
  background: #ef4444;
  color: white;
}

.delete-btn:hover {
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

.document-group {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.document-section {
  background: white;
  border-radius: 8px;
  border: 1px solid #e6f2ff;
  padding: 1rem;
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
  margin-bottom: 1rem;
}

.file-item {
  padding: 0.5rem;
  background: #f8fafc;
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
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.file-link:hover {
  text-decoration: underline;
}

.feedback-section {
  margin-top: 1rem;
}

.feedback-input {
  width: 100%;
  min-height: 100px;
  padding: 0.75rem;
  border: 1px solid #e6f2ff;
  border-radius: 6px;
  resize: vertical;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.feedback-input:focus {
  outline: none;
  border-color: #0082c6;
  box-shadow: 0 0 0 2px rgba(0, 130, 198, 0.1);
}

.feedback-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.submit-feedback-btn,
.update-required-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.submit-feedback-btn {
  background: #0082c6;
  color: white;
}

.submit-feedback-btn:hover {
  background: #0069a3;
}

.update-required-btn {
  background: #f59e0b;
  color: white;
}

.update-required-btn:hover {
  background: #d97706;
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

  .filter-row {
    flex-direction: column;
    gap: 0.5rem;
  }

  .filter-actions {
    margin-left: 0;
    margin-top: 0.5rem;
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

.document-actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.document-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.document-item {
  background: white;
  border-radius: 8px;
  border: 1px solid #e6f2ff;
  padding: 1rem;
}

.document-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #e6f2ff;
}

.document-header h4 {
  color: #0082c6;
  margin: 0;
  font-size: 1.1rem;
}

.document-status {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.5rem;
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.9rem;
  font-weight: 500;
}

.status-submitted {
  background: #dcfce7;
  color: #16a34a;
}

.status-needs-update {
  background: #fef3c7;
  color: #d97706;
}

.submission-time {
  font-size: 0.9rem;
  color: #64748b;
}

.document-files {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.file-item {
  padding: 0.5rem;
  background: #f8fafc;
  border-radius: 4px;
  border: 1px solid #e6f2ff;
  transition: all 0.3s ease;
}

.file-item:hover {
  background: #f0f7ff;
  transform: translateX(5px);
}

.file-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #0082c6;
  text-decoration: none;
  font-size: 0.9rem;
}

.file-link:hover {
  text-decoration: underline;
}

.file-link i {
  font-size: 1rem;
  color: #64748b;
}

.no-documents {
  text-align: center;
  padding: 2rem;
  color: #64748b;
  font-size: 1.1rem;
}

.modal-body {
  padding: 1rem;
  max-height: 70vh;
  overflow-y: auto;
}

.modal-content {
  width: 90%;
  max-width: 800px;
}
</style>
