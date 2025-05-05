<template>
  <div class="container">
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

    <!-- Overlay khi sidebar mở trên mobile -->
    <div v-if="isSidebarOpen && isMobile" class="overlay" @click="toggleSidebar"></div>

    <!-- SidebarInfo -->
    <SidebarInfo :is-open="isSidebarOpen" @toggle="toggleSidebar" />

    <!-- Nội dung chính -->
    <div class="main-content" :class="{ 'main-content-shifted': isSidebarOpen && !isMobile }">
      <div class="content">
        <!-- Thông báo trạng thái -->
        <p v-if="loading" class="loading-text">Đang tải dữ liệu...</p>
        <p v-else-if="error" class="error-text">{{ error }}</p>

        <!-- Cột nhập liệu -->
        <div v-else class="column" v-show="canEdit">
          <div class="quaTrinhCongTac">
            <p class="section-title">Thêm thông tin quá trình công tác</p>
            <div class="info-row">
              <p class="sub-label">Thời gian</p>
              <input
                type="text"
                v-model="newEntry.thoi_gian"
                placeholder="Ví dụ: 2020 - 2023"
                class="input-field"
              />
            </div>
            <div class="info-row">
              <p class="sub-label">Vị trí công tác</p>
              <select v-model="newEntry.vi_tri" class="input-field">
                <option value="Chuyên viên">Chuyên viên</option>
                <option value="Chuyên viên chính">Chuyên viên chính</option>
                <option value="Giảng viên">Giảng viên</option>
                <option value="Giảng viên chính">Giảng viên chính</option>
              </select>
            </div>
            <div class="info-row">
              <p class="sub-label">Lĩnh vực chuyên môn</p>
              <input
                type="text"
                v-model="newEntry.linh_vuc"
                placeholder="Ví dụ: Công nghệ Thông tin"
                class="input-field"
              />
            </div>
            <div class="info-row">
              <p class="sub-label">Cơ quan công tác</p>
              <input
                type="text"
                v-model="newEntry.co_quan"
                placeholder="Ví dụ: Viện Đại học Mở Hà Nội"
                class="input-field"
              />
            </div>
            <button @click="addEntry" class="save-button" :disabled="saving">
              {{ saving ? 'Đang lưu...' : (isEditing ? 'Cập nhật' : 'Thêm mới') }}
            </button>
          </div>
        </div>

        <!-- Cột bảng hiển thị -->
        <div class="column">
          <div class="table-container">
            <p class="section-title">
              Quá trình công tác và hoạt động khoa học trong và ngoài nước
            </p>
            <table>
              <thead>
                <tr>
                  <th>Thời gian</th>
                  <th>Vị trí công tác</th>
                  <th>Lĩnh vực chuyên môn</th>
                  <th>Cơ quan công tác</th>
                  <th v-if="canEdit">Hành động</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(entry, index) in workExperienceEntries" :key="index">
                  <td>{{ entry.thoi_gian }}</td>
                  <td>{{ entry.vi_tri }}</td>
                  <td>{{ entry.linh_vuc }}</td>
                  <td>{{ entry.co_quan }}</td>
                  <td v-if="canEdit">
                    <button @click="editEntry(entry)" class="edit-button">
                      Sửa
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <router-view></router-view>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { useTeacherViewStore } from '@/stores/teacherView';
import SidebarInfo from '../../components/SidebarInfo.vue';
import api from '@/config/api';

// Props
const props = defineProps({
  ma_gv: {
    type: String,
    default: ''
  },
  viewOnly: {
    type: Boolean,
    default: false
  }
});

// Trạng thái sidebar
const isSidebarOpen = ref(false); // Mặc định đóng
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
const loading = ref(false);
const saving = ref(false);
const error = ref('');
const isEditing = ref(false);

// Dữ liệu ban đầu của bảng
const workExperienceEntries = ref([]);

// Dữ liệu cho form nhập liệu
const newEntry = ref({
  thoi_gian: '',
  vi_tri: '',
  linh_vuc: '',
  co_quan: '',
});

// Khởi tạo stores và router
const authStore = useAuthStore();
const teacherViewStore = useTeacherViewStore();
const router = useRouter();
const route = useRoute();

// Thêm computed properties cho authentication
const isAuthenticated = computed(() => authStore.isAuthenticated);
const storedEmail = computed(() => authStore.user?.email || '');
const userPermission = computed(() => authStore.user?.quyen_han || 0);
const canEdit = computed(() => !props.viewOnly && userPermission.value === 3);

// Lấy dữ liệu khi component được mount
onMounted(() => {
  authStore.loadUserFromStorage();
  fetchWorkExperienceEntries();
});

// Hàm format thời gian
function formatDate(dateString) {
  if (!dateString) return '';
  // dateString có định dạng "YYYY-MM"
  const [year, month] = dateString.split('-');
  return `${month}/${year}`;
}

// Lấy danh sách Quá trình công tác từ API
async function fetchWorkExperienceEntries() {
  try {
    loading.value = true;
    error.value = '';

    // Lấy ma_gv từ props hoặc store
    const ma_gv = props.ma_gv || teacherViewStore.getCurrentTeacherId();
    if (!ma_gv) {
      throw new Error('Không tìm thấy mã giảng viên');
    }

    const response = await api.get(`syll/quatrinhcongtac/${ma_gv}`);
    workExperienceEntries.value = response.data || [];
  } catch (err) {
    handleError(err, 'Không thể tải thông tin quá trình công tác');
  } finally {
    loading.value = false;
  }
}

// Hàm chỉnh sửa quá trình công tác
function editEntry(entry) {
  newEntry.value = {
    thoi_gian: entry.thoi_gian,
    vi_tri: entry.vi_tri,
    linh_vuc: entry.linh_vuc,
    co_quan: entry.co_quan,
    ma_ct: entry.ma_ct
  };
  isEditing.value = true;
}

// Hàm thêm mục mới vào bảng
async function addEntry() {
  if (
    !newEntry.value.thoi_gian ||
    !newEntry.value.vi_tri ||
    !newEntry.value.linh_vuc ||
    !newEntry.value.co_quan
  ) {
    alert('Vui lòng điền đầy đủ thông tin!');
    return;
  }

  try {
    saving.value = true;
    error.value = '';

    // Lấy ma_gv từ props hoặc store
    const ma_gv = props.ma_gv || teacherViewStore.getCurrentTeacherId();
    if (!ma_gv) {
      throw new Error('Không tìm thấy mã giảng viên');
    }

    const payload = { ...newEntry.value, ma_gv };

    if (isEditing.value) {
      // Cập nhật thông tin
      await api.put(`syll/quatrinhcongtac/${newEntry.value.ma_ct}`, payload);
      alert('Cập nhật quá trình công tác thành công!');
    } else {
      // Thêm mới
      await api.post('syll/quatrinhcongtac', payload);
      alert('Thêm quá trình công tác thành công!');
    }

    // Refresh dữ liệu sau khi thêm/cập nhật
    await fetchWorkExperienceEntries();

    // Reset form và trạng thái
    newEntry.value = {
      thoi_gian: '',
      vi_tri: '',
      linh_vuc: '',
      co_quan: '',
    };
    isEditing.value = false;
  } catch (err) {
    handleError(err, isEditing.value ? 'Không thể cập nhật quá trình công tác' : 'Không thể thêm quá trình công tác');
  } finally {
    saving.value = false;
  }
}

// Hàm xử lý lỗi chung
function handleError(err, defaultMsg) {
  let errorMsg = defaultMsg;
  if (err.response) {
    console.error('Mã lỗi HTTP:', err.response.status);
    console.error('Chi tiết lỗi:', err.response.data);
    if (err.response.status === 401) {
      errorMsg = 'Phiên đăng nhập hết hạn';
      authStore.logout();
      router.push('/login');
    } else if (err.response.status === 403) {
      errorMsg = 'Bạn không có quyền truy cập thông tin này';
    } else if (err.response.status === 404) {
      errorMsg = 'Không tìm thấy thông tin';
    } else if (err.response.status === 500) {
      errorMsg = 'Lỗi server, vui lòng thử lại sau';
    } else {
      errorMsg = err.response.data.detail || defaultMsg;
    }
  } else if (err.request) {
    errorMsg = 'Không thể kết nối đến server';
  } else {
    errorMsg = err.message || defaultMsg;
  }
  error.value = errorMsg;
  console.error('Lỗi:', err);
}

// Hàm xử lý đăng xuất
function handleLogout() {
  authStore.logout();
  router.push('/login');
}
</script>

<style scoped>
/* Container */
.container {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f8fafc;
  position: relative;
}

/* Header */
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

.login-btn, .logout-btn {
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

.login-btn:hover, .logout-btn:hover {
  background: #0069a3;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Overlay */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(2px);
  z-index: 999;
  transition: opacity 0.3s ease;
}

/* Main Content */
.main-content {
  flex: 1;
  margin-top: 100px;
  margin-left: 240px;
  margin-right: 30px;
  padding: 0;
  box-sizing: border-box;
  background: #f8fafc;
  transition: all 0.3s ease;
  min-height: calc(100vh - 100px);
}

.main-content-shifted {
  margin-left: 240px;
  margin-right: 30px;
}

/* Content Grid */
.content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  width: 100%;
  padding: 20px;
}

/* Column */
.column {
  background: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.column:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.1);
}

/* Status Messages */
.loading-text {
  color: #4b5563;
}

.error-text {
  color: #ef4444;
}

/* Section Title */
.section-title {
  font-weight: 600;
  color: #1e293b;
  font-size: 1.1rem;
  margin-bottom: 15px;
  padding-bottom: 8px;
  border-bottom: 2px solid #0082c6;
}

/* Form nhập liệu */
.quaTrinhCongTac {
  margin-top: 15px;
}

.info-row {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 8px 0;
}

.sub-label {
  font-weight: 600;
  color: #1e293b;
  font-size: 0.95rem;
  width: 200px;
  flex-shrink: 0;
}

.input-field {
  flex: 1;
  padding: 12px 15px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.95rem;
  background: #f8fafc;
  transition: all 0.3s ease;
  min-width: 0;
  max-width: 400px;
}

.input-field:focus {
  border-color: #0082c6;
  box-shadow: 0 0 0 3px rgba(0, 130, 198, 0.1);
  background: white;
  outline: none;
}

/* Save Button */
.save-button {
  margin-top: 20px;
  background: #0082c6;
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
  width: 100%;
  max-width: 200px;
}

.save-button:hover {
  background: #0069a3;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.save-button:disabled {
  background: #93c5fd;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

/* Bảng hiển thị */
.table-container {
  width: 100%;
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  margin-top: 10px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

th,
td {
  padding: 10px 12px;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
  font-size: 13px;
}

th {
  background: #0082c6;
  color: white;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 12px;
  letter-spacing: 0.5px;
}

td {
  background: #fff;
  color: #2d3748;
}

tr:last-child td {
  border-bottom: none;
}

tr:hover td {
  background: #f5faff;
}

/* Edit Button */
.edit-button {
  background: #0082c6;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.edit-button:hover {
  background: #0069a3;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Responsive */
@media (max-width: 1024px) {
  .header {
    padding: 10px 20px 10px 70px;
  }

  .header h1 {
    font-size: 1.1rem;
    padding: 0 8px;
  }

  .logo {
    width: 45px;
    margin-right: 1.5rem;
  }

  .main-content {
    margin-left: 240px;
    margin-right: 30px;
  }

  .sub-label {
    width: 180px;
  }

  .input-field {
    max-width: 350px;
  }
}

@media (max-width: 768px) {
  .header {
    height: 60px;
    padding: 10px 15px 10px 60px;
    gap: 10px;
  }

  .header h1 {
    font-size: 0.95rem;
    padding: 0 5px;
    max-width: 300px;
  }

  .logo {
    width: 40px;
    margin-right: 1rem;
    margin-top: 1.5rem;
  }

  .mobile-toggle {
    top: 15px;
    left: 15px;
    width: 28px;
    height: 28px;
  }

  .main-content {
    margin-top: 80px;
    margin-left: 20px;
    margin-right: 20px;
  }

  .main-content-shifted {
    margin-left: 20px;
    margin-right: 20px;
  }

  .content {
    grid-template-columns: 1fr;
  }

  .column {
    padding: 25px;
  }

  .info-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
    padding: 12px 0;
  }

  .sub-label {
    width: 100%;
    font-size: 0.9rem;
  }

  .input-field {
    width: 100%;
    max-width: none;
    padding: 10px 12px;
  }
}

@media (max-width: 480px) {
  .header {
    height: 50px;
    padding: 10px 10px 10px 50px;
    gap: 8px;
  }

  .header h1 {
    font-size: 0.85rem;
    padding: 0 3px;
    max-width: 200px;
  }

  .logo {
    width: 35px;
    margin-right: 0.8rem;
    margin-top: 1.2rem;
  }

  .mobile-toggle {
    top: 10px;
    left: 10px;
    width: 26px;
    height: 26px;
  }

  .main-content {
    margin-top: 70px;
    margin-left: 15px;
    margin-right: 15px;
  }

  .content {
    padding: 15px;
  }

  .column {
    padding: 20px;
  }

  .info-row {
    padding: 10px 0;
  }

  .sub-label {
    font-size: 0.85rem;
  }

  .input-field {
    padding: 8px 10px;
    font-size: 0.9rem;
  }

  .save-button {
    padding: 10px 20px;
    font-size: 0.9rem;
  }
}

/* Scrollbar */
.main-content::-webkit-scrollbar {
  width: 6px;
}

.main-content::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 10px;
}

.main-content::-webkit-scrollbar-thumb {
  background: #0082c6;
  border-radius: 10px;
}

.main-content::-webkit-scrollbar-thumb:hover {
  background: #0069a3;
}
</style>