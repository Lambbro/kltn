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

    <!-- Sử dụng component SidebarInfo -->
    <SidebarInfo :is-open="isSidebarOpen" @toggle="toggleSidebar" />

    <!-- Nội dung chính -->
    <div class="main-content" :class="{ 'main-content-shifted': isSidebarOpen && !isMobile }">
      <div class="content">
        <!-- Thông báo trạng thái -->
        <p v-if="loading" class="loading-text">Đang tải dữ liệu...</p>

        <!-- Cột nhập liệu Hướng nghiên cứu -->
        <div v-else class="column" v-show="canEdit">
          <div class="huongNghienCuu">
            <p class="section-title">Thêm hướng nghiên cứu</p>
            <div class="info-row">
              <p class="sub-label">Hướng nghiên cứu</p>
              <div class="dropdown-wrapper">
                <select
                  v-model="selectedHnc"
                  class="input-field"
                >
                  <option value="" disabled selected>Chọn hướng nghiên cứu...</option>
                  <option
                    v-for="hnc in allHncList"
                    :key="hnc.ma_hnc"
                    :value="hnc"
                  >
                    {{ hnc.ten_hnc }}
                  </option>
                </select>
              </div>
            </div>
            <button
              @click="addResearchFieldEntry"
              class="save-button"
              :disabled="saving || !selectedHnc"
            >
              {{ saving ? 'Đang lưu...' : 'Thêm' }}
            </button>
          </div>
        </div>

        <!-- Cột hiển thị danh sách Hướng nghiên cứu -->
        <div class="column">
          <div class="list-container">
            <p class="section-title">Danh mục các hướng nghiên cứu</p>
            <p v-if="researchFields.length === 0" class="no-data-text">
              Chưa có hướng nghiên cứu nào.
            </p>
            <ol v-else>
              <li v-for="entry in researchFields" :key="entry.ma_hnc">
                {{ entry.ten_hnc }}
                <button 
                  v-if="canEdit"
                  @click="removeResearchField(entry)" 
                  class="remove-button"
                >
                  Xóa
                </button>
              </li>
            </ol>
          </div>
        </div>

        <!-- Cột nhập liệu Đề tài KHCN -->
        <div class="column" v-show="canEdit">
          <div class="deTaiKHCN">
            <p class="section-title">Thêm thông tin đề tài KHCN</p>
            <div class="info-row">
              <p class="sub-label">Tên đề tài</p>
              <input
                type="text"
                v-model="newProjectEntry.ten_dt"
                placeholder="Nhập tên đề tài"
                class="input-field"
              />
            </div>
            <div class="info-row">
              <p class="sub-label">Cấp quản lý</p>
              <input
                type="text"
                v-model="newProjectEntry.cap_quan_ly"
                placeholder="Nhập cấp quản lý"
                class="input-field"
              />
            </div>
            <div class="info-row">
              <p class="sub-label">Thời gian thực hiện</p>
              <input
                type="number"
                v-model.number="newProjectEntry.tg_thuc_hien"
                placeholder="Nhập thời gian thực hiện"
                class="input-field"
              />
            </div>
            <div class="info-row">
              <p class="sub-label">Trạng thái</p>
              <select v-model="newProjectEntry.trang_thai" class="input-field">
                <option :value="true">Đang thực hiện</option>
                <option :value="false">Hoàn thành</option>
              </select>
            </div>
            <div class="info-row">
              <p class="sub-label">Kết quả</p>
              <input
                type="text"
                v-model="newProjectEntry.ket_qua"
                placeholder="Nhập kết quả"
                class="input-field"
              />
            </div>
            <div class="info-row">
              <p class="sub-label">Loại đề tài</p>
              <select v-model.number="newProjectEntry.loai_de_tai" class="input-field">
                <option :value="1">Đề tài cấp bộ</option>
                <option :value="2">Đề tài cấp trường</option>
                <option :value="3">Đề tài cấp quốc gia</option>
              </select>
            </div>
            <div class="info-row">
              <p class="sub-label">Tư cách tham gia</p>
              <select v-model="newProjectEntry.tu_cach" class="input-field">
                <option :value="true">Chủ nhiệm</option>
                <option :value="false">Thành viên</option>
              </select>
            </div>
            <button @click="addProjectEntry" class="save-button" :disabled="saving">
              {{ saving ? 'Đang lưu...' : (isEditing ? 'Cập nhật' : 'Thêm mới') }}
            </button>
          </div>
        </div>

        <!-- Cột bảng hiển thị Đề tài KHCN -->
        <div class="column">
          <div class="table-container">
            <p class="section-title">Đề tài KHCN</p>
            <table>
              <thead>
                <tr>
                  <th>Tên đề tài</th>
                  <th>Cấp quản lý</th>
                  <th>Thời gian thực hiện</th>
                  <th>Trạng thái</th>
                  <th>Kết quả</th>
                  <th>Loại đề tài</th>
                  <th>Tư cách tham gia</th>
                  <th v-if="canEdit">Thao tác</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="entry in projectEntries" :key="entry.ma_dt_khcn">
                  <td>{{ entry.ten_dt }}</td>
                  <td>{{ entry.cap_quan_ly }}</td>
                  <td>{{ entry.tg_thuc_hien }}</td>
                  <td>{{ entry.trang_thai ? 'Đang thực hiện' : 'Hoàn thành' }}</td>
                  <td>{{ entry.ket_qua }}</td>
                  <td>{{ getLoaiDeTaiText(entry.loai_de_tai) }}</td>
                  <td>{{ entry.tu_cach ? 'Chủ nhiệm' : 'Thành viên' }}</td>
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
    </div>

    <!-- Error Modal -->
    <div v-if="showErrorModal" class="error-modal">
      <div class="error-modal-content">
        <div class="error-modal-header">
          <h3>Lỗi</h3>
          <button @click="closeErrorModal" class="close-button">&times;</button>
        </div>
        <div class="error-modal-body">
          <p>{{ errorMessage }}</p>
        </div>
        <div class="error-modal-footer">
          <button @click="closeErrorModal" class="confirm-button">Đóng</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
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
const isSidebarOpen = ref(true);
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

// Trạng thái dữ liệu
const loading = ref(false);
const saving = ref(false);
const errorMessage = ref('');
const showErrorModal = ref(false);
const showDropdown = ref(false);
const isEditing = ref(false);

// Dữ liệu hướng nghiên cứu
const researchFields = ref([]); // HNC của giảng viên
const allHncList = ref([]); // Tất cả HNC
const searchHnc = ref('');
const selectedHnc = ref(null);

// Dữ liệu đề tài KHCN
const projectEntries = ref([]);
const newProjectEntry = ref({
  ten_dt: '',
  cap_quan_ly: '',
  tg_thuc_hien: 0,
  trang_thai: true,
  ket_qua: '',
  loai_de_tai: 1,
  tu_cach: true,
  ma_dt_khcn: 0,
  ma_gv: ''
});

// Khởi tạo authStore và router
const authStore = useAuthStore();
const teacherViewStore = useTeacherViewStore();
const router = useRouter();

// Thêm computed properties cho authentication
const isAuthenticated = computed(() => authStore.isAuthenticated);
const storedEmail = computed(() => authStore.user?.email || '');
const userPermission = computed(() => authStore.user?.quyen_han || 0);
const canEdit = computed(() => !props.viewOnly && userPermission.value === 3);

// Lấy dữ liệu khi component được mount
onMounted(() => {
  authStore.loadUserFromStorage();
  fetchAllHnc();
  fetchProjectEntries();
  fetchTeacherResearchFields();
});

// Lấy danh sách hướng nghiên cứu của giảng viên
async function fetchTeacherResearchFields() {
  try {
    loading.value = true;
    errorMessage.value = '';
    // Lấy ma_gv từ props hoặc store
    const ma_gv = props.ma_gv || teacherViewStore.getCurrentTeacherId();
    if (!ma_gv) {
      throw new Error('Không tìm thấy mã giảng viên');
    }
    const response = await api.get(`get_data/hnc_by_gv/${ma_gv}`);
    researchFields.value = response.data || [];
  } catch (err) {
    handleError(err, 'Không thể tải thông tin hướng nghiên cứu của giảng viên');
  } finally {
    loading.value = false;
  }
}

// Lấy danh sách tất cả hướng nghiên cứu từ API
async function fetchAllHnc() {
  try {
    loading.value = true;
    errorMessage.value = '';
    const response = await api.get('phongkhdn/hnc');
    allHncList.value = response.data || [];
  } catch (err) {
    handleError(err, 'Không thể tải danh sách hướng nghiên cứu');
  } finally {
    loading.value = false;
  }
}

// Hàm thêm hướng nghiên cứu mới
async function addResearchFieldEntry() {
  if (!selectedHnc.value) {
    alert('Vui lòng chọn hướng nghiên cứu!');
    return;
  }
  try {
    saving.value = true;
    errorMessage.value = '';
    const ma_gv = props.ma_gv || teacherViewStore.getCurrentTeacherId();
    if (!ma_gv) {
      throw new Error('Không tìm thấy mã giảng viên');
    }
    console.log(selectedHnc.value.ma_hnc);
    console.log(ma_gv);
    const url = `syll/hnc/add?ma_gv=${ma_gv}&ma_hnc=${selectedHnc.value.ma_hnc}`;
    console.log('API URL:', url);
    await api.post(url);
    alert('Thêm hướng nghiên cứu thành công!');
    await fetchTeacherResearchFields();

    // Reset form và trạng thái
    selectedHnc.value = null;
  } catch (err) {
    handleError(err, 'Không thể thêm hướng nghiên cứu');
  } finally {
    saving.value = false;
  }
}

// Hàm xóa hướng nghiên cứu
async function removeResearchField(entry) {
  if (!confirm('Bạn có chắc chắn muốn xóa hướng nghiên cứu này?')) {
    return;
  }

  try {
    saving.value = true;
    errorMessage.value = '';

    // Lấy ma_gv từ props hoặc store
    const ma_gv = props.ma_gv || teacherViewStore.getCurrentTeacherId();
    if (!ma_gv) {
      throw new Error('Không tìm thấy mã giảng viên');
    }

    await api.delete(`syll/hnc/${ma_gv}/${entry.ma_hnc}`);
    alert('Xóa hướng nghiên cứu thành công!');

    // Refresh dữ liệu sau khi xóa
    await fetchTeacherResearchFields();
  } catch (err) {
    handleError(err, 'Không thể xóa hướng nghiên cứu');
  } finally {
    saving.value = false;
  }
}

// Lấy danh sách đề tài nghiên cứu từ API
async function fetchProjectEntries() {
  try {
    loading.value = true;
    errorMessage.value = '';

    // Lấy ma_gv từ props hoặc store
    const ma_gv = props.ma_gv || teacherViewStore.getCurrentTeacherId();
    if (!ma_gv) {
      throw new Error('Không tìm thấy mã giảng viên');
    }

    const response = await api.get(`syll/detaikhcn/${ma_gv}`);
    projectEntries.value = response.data || [];
  } catch (err) {
    handleError(err, 'Không thể tải thông tin đề tài nghiên cứu');
  } finally {
    loading.value = false;
  }
}

// Hàm thêm đề tài nghiên cứu mới
async function addProjectEntry() {
  if (
    !newProjectEntry.value.ten_dt ||
    !newProjectEntry.value.cap_quan_ly ||
    !newProjectEntry.value.tg_thuc_hien ||
    newProjectEntry.value.trang_thai === null ||
    !newProjectEntry.value.ket_qua ||
    !newProjectEntry.value.loai_de_tai ||
    newProjectEntry.value.tu_cach === null
  ) {
    alert('Vui lòng điền đầy đủ thông tin!');
    return;
  }

  try {
    saving.value = true;
    errorMessage.value = '';

    // Lấy ma_gv từ props hoặc store
    const ma_gv = props.ma_gv || teacherViewStore.getCurrentTeacherId();
    if (!ma_gv) {
      throw new Error('Không tìm thấy mã giảng viên');
    }

    const payload = { 
      ...newProjectEntry.value, 
      ma_gv,
      tg_thuc_hien: Number(newProjectEntry.value.tg_thuc_hien),
      loai_de_tai: Number(newProjectEntry.value.loai_de_tai)
    };

    if (isEditing.value) {
      // Cập nhật thông tin
      await api.put(`syll/detaikhcn/${newProjectEntry.value.ma_dt_khcn}`, payload);
      alert('Cập nhật đề tài nghiên cứu thành công!');
    } else {
      // Thêm mới
      await api.post('syll/detaikhcn', payload);
      alert('Thêm đề tài nghiên cứu thành công!');
    }

    // Refresh dữ liệu sau khi thêm/cập nhật
    await fetchProjectEntries();

    // Reset form và trạng thái
    resetProjectEntryForm();
    isEditing.value = false;
  } catch (err) {
    handleError(err, isEditing.value ? 'Không thể cập nhật đề tài nghiên cứu' : 'Không thể thêm đề tài nghiên cứu');
  } finally {
    saving.value = false;
  }
}

// Hàm reset form đề tài KHCN
function resetProjectEntryForm() {
  newProjectEntry.value = {
    ten_dt: '',
    cap_quan_ly: '',
    tg_thuc_hien: 0,
    trang_thai: true,
    ket_qua: '',
    loai_de_tai: 1,
    tu_cach: true,
    ma_dt_khcn: 0,
    ma_gv: ''
  };
}

// Hàm chỉnh sửa đề tài KHCN
function editEntry(entry) {
  newProjectEntry.value = { ...entry };
  isEditing.value = true;
}

// Xử lý lỗi
function handleError(err, defaultMessage) {
  console.error(err);
  errorMessage.value = err.response?.data?.message || err.response?.data?.detail || defaultMessage;
  showErrorModal.value = true;
}

// Đóng modal lỗi
function closeErrorModal() {
  showErrorModal.value = false;
  errorMessage.value = '';
}

// Xử lý đăng xuất
function handleLogout() {
  authStore.logout();
  router.push('/login');
}

// Hàm helper để hiển thị loại đề tài
function getLoaiDeTaiText(loaiDeTai) {
  const loaiDeTaiMap = {
    1: 'Đề tài cấp bộ',
    2: 'Đề tài cấp trường',
    3: 'Đề tài cấp quốc gia'
  };
  return loaiDeTaiMap[loaiDeTai] || 'Không xác định';
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
.deTaiKHCN {
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
  max-width: 450px;
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

/* Dropdown */
.dropdown-wrapper {
  position: relative;
  width: 100%;
}

.dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  max-height: 200px;
  overflow-y: auto;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.dropdown-item {
  padding: 10px 15px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.dropdown-item:hover {
  background: #f1f5f9;
}

.no-data-text {
  padding: 10px 15px;
  color: #64748b;
  font-style: italic;
  text-align: center;
}

/* List Container */
.list-container {
  width: 100%;
}

ol {
  padding-left: 20px;
  margin-top: 10px;
}

ol li {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
  color: #2d3748;
  font-size: 14px;
  line-height: 1.5;
  padding-left: 10px;
  position: relative;
}

ol li:before {
  content: '';
  position: absolute;
  left: 0;
  top: 8px;
  width: 5px;
  height: 5px;
  background: #0082c6;
  border-radius: 50%;
}

.selected-hnc {
  margin-top: 15px;
  padding: 10px;
  background: #f1f5f9;
  border-radius: 8px;
}

.selected-text {
  color: #1e293b;
  font-weight: 500;
  margin-top: 5px;
}

.remove-button {
  background: #ef4444;
  color: white;
  border: none;
  padding: 4px 8px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
  margin-left: 10px;
  transition: all 0.3s ease;
}

.remove-button:hover {
  background: #dc2626;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

select.input-field {
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 10px center;
  background-size: 1em;
  padding-right: 2.5em;
  cursor: pointer;
}

select.input-field:focus {
  outline: none;
  border-color: #0082c6;
  box-shadow: 0 0 0 3px rgba(0, 130, 198, 0.1);
}

select.input-field option {
  padding: 10px;
  background: white;
}

select.input-field option:checked {
  background: #f1f5f9;
  color: #0082c6;
}

/* Error Modal */
.error-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

.error-modal-content {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  animation: modalFadeIn 0.3s ease;
}

.error-modal-header {
  padding: 20px;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.error-modal-header h3 {
  margin: 0;
  color: #ef4444;
  font-size: 1.2rem;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #64748b;
  cursor: pointer;
  padding: 0;
  line-height: 1;
}

.close-button:hover {
  color: #1e293b;
}

.error-modal-body {
  padding: 20px;
  color: #1e293b;
  font-size: 1rem;
  line-height: 1.5;
}

.error-modal-footer {
  padding: 20px;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: flex-end;
}

.confirm-button {
  background: #0082c6;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
}

.confirm-button:hover {
  background: #0069a3;
  transform: translateY(-1px);
}

@keyframes modalFadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>