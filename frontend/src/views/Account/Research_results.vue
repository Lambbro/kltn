<template>
  <div class="container">
    <!-- Header -->
    <header class="header">
      <button class="mobile-toggle" @click="toggleSidebar" v-if="isMobile">
        <span class="toggle-icon">☰</span>
      </button>
      <img src="@/assets/img/logo-hou.png" alt="Logo" class="logo" />
      <h1>HỆ THỐNG QUẢN LÝ KẾT QUẢ NGHIÊN CỨU</h1>
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
        <p v-else-if="error" class="error-text">{{ error }}</p>

        <!-- Cột nhập liệu Sách, Báo, Công bố -->
        <div v-else class="column" v-show="canEdit">
          <div class="sachBaoCongBo">
            <p class="section-title">Thêm thông tin sách, báo, công bố</p>
            <div class="info-row">
              <p class="sub-label">Tên sách</p>
              <input
                type="text"
                v-model="newPublicationEntry.ten_sach"
                placeholder="Nhập tên sách"
                class="input-field"
              />
            </div>
            <div class="info-row">
              <p class="sub-label">Vị trí</p>
              <select v-model="newPublicationEntry.vi_tri" class="input-field">
                <option :value="true">Tác giả</option>
                <option :value="false">Đồng tác giả</option>
              </select>
            </div>
            <div class="info-row">
              <p class="sub-label">Nơi xuất bản</p>
              <input
                type="text"
                v-model="newPublicationEntry.noi_xb"
                placeholder="Nhập nơi xuất bản"
                class="input-field"
              />
            </div>
            <div class="info-row">
              <p class="sub-label">Năm xuất bản</p>
              <input
                type="number"
                v-model="newPublicationEntry.nam_xb"
                placeholder="Nhập năm xuất bản"
                class="input-field"
              />
            </div>
            <div class="info-row">
              <p class="sub-label">Loại sách</p>
              <select v-model="newPublicationEntry.loai_sach" class="input-field">
                <option :value="1">Sách giáo khoa</option>
                <option :value="2">Sách tham khảo</option>
                <option :value="3">Sách chuyên khảo</option>
                <option :value="4">Báo cáo khoa học</option>
              </select>
            </div>
            <button
              @click="addPublicationEntry"
              class="save-button"
              :disabled="saving"
            >
              {{ saving ? 'Đang lưu...' : (isEditingPublication ? 'Cập nhật' : 'Thêm mới') }}
            </button>
          </div>
        </div>

        <!-- Cột bảng hiển thị Sách, Báo, Công bố -->
        <div class="column">
          <div class="table-container">
            <p class="section-title">Sách, Báo, Công bố</p>
            <table>
              <thead>
                <tr>
                  <th>Tên sách</th>
                  <th>Vị trí</th>
                  <th>Nơi xuất bản</th>
                  <th>Năm xuất bản</th>
                  <th>Loại sách</th>
                  <th v-if="canEdit">Thao tác</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="entry in publicationEntries" :key="entry.ma_sach">
                  <td>{{ entry.ten_sach }}</td>
                  <td>{{ entry.vi_tri ? 'Tác giả' : 'Đồng tác giả' }}</td>
                  <td>{{ entry.noi_xb }}</td>
                  <td>{{ entry.nam_xb }}</td>
                  <td>{{ getLoaiSachText(entry.loai_sach) }}</td>
                  <td v-if="canEdit">
                    <button @click="editPublicationEntry(entry)" class="edit-button">
                      Sửa
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Cột nhập liệu Phát minh sáng chế -->
        <div class="column" v-show="canEdit">
          <div class="phatMinhSangChe">
            <p class="section-title">Thêm thông tin phát minh sáng chế</p>
            <div class="info-row">
              <p class="sub-label">Tên phát minh sáng chế</p>
              <input
                type="text"
                v-model="newPatentEntry.ten_pmsc"
                placeholder="Nhập tên phát minh sáng chế"
                class="input-field"
              />
            </div>
            <div class="info-row">
              <p class="sub-label">Loại phát minh</p>
              <select v-model="newPatentEntry.loai_pmsc" class="input-field">
                <option value="Sáng chế">Sáng chế</option>
                <option value="Giải pháp hữu ích">Giải pháp hữu ích</option>
                <option value="Kiểu dáng công nghiệp">Kiểu dáng công nghiệp</option>
              </select>
            </div>
            <div class="info-row">
              <p class="sub-label">Thông tin</p>
              <textarea
                v-model="newPatentEntry.thong_tin"
                placeholder="Nhập thông tin chi tiết"
                class="input-field"
                rows="3"
              ></textarea>
            </div>
            <div class="info-row">
              <p class="sub-label">Thời gian cấp bằng</p>
              <input
                type="number"
                v-model="newPatentEntry.tg_cap_bang"
                placeholder="Nhập năm cấp bằng"
                class="input-field"
              />
            </div>
            <button @click="addPatentEntry" class="save-button" :disabled="saving">
              {{ saving ? 'Đang lưu...' : (isEditingPatent ? 'Cập nhật' : 'Thêm mới') }}
            </button>
          </div>
        </div>

        <!-- Cột bảng hiển thị Phát minh sáng chế -->
        <div class="column">
          <div class="table-container">
            <p class="section-title">Phát minh sáng chế</p>
            <table>
              <thead>
                <tr>
                  <th>Tên phát minh sáng chế</th>
                  <th>Loại phát minh</th>
                  <th>Thông tin</th>
                  <th>Thời gian cấp bằng</th>
                  <th v-if="canEdit">Thao tác</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="entry in patentEntries" :key="entry.ma_pmsc">
                  <td>{{ entry.ten_pmsc }}</td>
                  <td>{{ entry.loai_pmsc }}</td>
                  <td>{{ entry.thong_tin }}</td>
                  <td>{{ entry.tg_cap_bang }}</td>
                  <td v-if="canEdit">
                    <button @click="editPatentEntry(entry)" class="edit-button">
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
const error = ref('');
const isEditingPublication = ref(false);
const isEditingPatent = ref(false);

// Dữ liệu ban đầu của bảng Sách, Báo, Công bố
const publicationEntries = ref([]);

// Dữ liệu cho form nhập liệu Sách, Báo, Công bố
const newPublicationEntry = ref({
  ten_sach: '',
  vi_tri: true,
  noi_xb: '',
  nam_xb: new Date().getFullYear(),
  loai_sach: 1,
  ma_sach: 0,
  ma_gv: ''
});

// Dữ liệu ban đầu của bảng Phát minh sáng chế
const patentEntries = ref([]);

// Dữ liệu cho form nhập liệu Phát minh sáng chế
const newPatentEntry = ref({
  ten_pmsc: '',
  loai_pmsc: 'Sáng chế',
  thong_tin: '',
  tg_cap_bang: new Date().getFullYear(),
  ma_gv: '',
  ma_pmsc: 0
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
onMounted(async () => {
  authStore.loadUserFromStorage();
  if (!authStore.user?.email) {
    router.push('/login');
    return;
  }
  await Promise.all([fetchPublicationEntries(), fetchPatentEntries()]);
});

// Lấy danh sách Sách, Báo, Công bố từ API
async function fetchPublicationEntries() {
  try {
    loading.value = true;
    error.value = '';
    
    // Lấy ma_gv từ props hoặc store
    const ma_gv = props.ma_gv || teacherViewStore.getCurrentTeacherId() || authStore.user.email.split('@')[0];
    
    if (!ma_gv) {
      throw new Error('Không tìm thấy mã giảng viên');
    }
    
    const response = await api.get(`syll/sachbaocongbo/${ma_gv}`);
    publicationEntries.value = response.data || [];
  } catch (err) {
    handleError(err, 'Không thể tải thông tin sách, báo, công bố');
  } finally {
    loading.value = false;
  }
}

// Lấy danh sách Phát minh sáng chế từ API
async function fetchPatentEntries() {
  try {
    loading.value = true;
    error.value = '';
    
    // Lấy ma_gv từ props hoặc store
    const ma_gv = props.ma_gv || teacherViewStore.getCurrentTeacherId() || authStore.user.email.split('@')[0];
    
    if (!ma_gv) {
      throw new Error('Không tìm thấy mã giảng viên');
    }
    
    const response = await api.get(`syll/phatminhsangche/${ma_gv}`);
    patentEntries.value = response.data || [];
  } catch (err) {
    handleError(err, 'Không thể tải thông tin phát minh sáng chế');
  } finally {
    loading.value = false;
  }
}

// Hàm thêm mục mới vào bảng Sách, Báo, Công bố
async function addPublicationEntry() {
  if (
    !newPublicationEntry.value.ten_sach ||
    !newPublicationEntry.value.noi_xb ||
    !newPublicationEntry.value.nam_xb ||
    !newPublicationEntry.value.loai_sach
  ) {
    error.value = 'Vui lòng điền đầy đủ thông tin sách, báo, công bố!';
    return;
  }

  try {
    saving.value = true;
    error.value = '';
    
    // Lấy ma_gv từ props hoặc store
    const ma_gv = props.ma_gv || teacherViewStore.getCurrentTeacherId() || authStore.user.email.split('@')[0];
    
    if (!ma_gv) {
      throw new Error('Không tìm thấy mã giảng viên');
    }
    
    const payload = { ...newPublicationEntry.value, ma_gv };

    if (isEditingPublication.value) {
      // Cập nhật thông tin
      await api.put(`syll/sachbaocongbo/${newPublicationEntry.value.ma_sach}`, payload);
      alert('Cập nhật sách, báo, công bố thành công!');
    } else {
      // Thêm mới
      await api.post('syll/sachbaocongbo', payload);
      alert('Thêm sách, báo, công bố thành công!');
    }

    await fetchPublicationEntries();
    resetPublicationForm();
  } catch (err) {
    handleError(err, isEditingPublication.value ? 'Không thể cập nhật sách, báo, công bố' : 'Không thể thêm sách, báo, công bố');
  } finally {
    saving.value = false;
  }
}

// Hàm thêm mục mới vào bảng Phát minh sáng chế
async function addPatentEntry() {
  if (
    !newPatentEntry.value.ten_pmsc ||
    !newPatentEntry.value.loai_pmsc ||
    !newPatentEntry.value.thong_tin ||
    !newPatentEntry.value.tg_cap_bang
  ) {
    error.value = 'Vui lòng điền đầy đủ thông tin phát minh sáng chế!';
    return;
  }

  try {
    saving.value = true;
    error.value = '';
    
    // Lấy ma_gv từ props hoặc store
    const ma_gv = props.ma_gv || teacherViewStore.getCurrentTeacherId() || authStore.user.email.split('@')[0];
    
    if (!ma_gv) {
      throw new Error('Không tìm thấy mã giảng viên');
    }
    
    const payload = { ...newPatentEntry.value, ma_gv };

    if (isEditingPatent.value) {
      // Cập nhật thông tin
      await api.put(`syll/phatminhsangche/${newPatentEntry.value.ma_pmsc}`, payload);
      alert('Cập nhật phát minh sáng chế thành công!');
    } else {
      // Thêm mới
      await api.post('syll/phatminhsangche', payload);
      alert('Thêm phát minh sáng chế thành công!');
    }

    await fetchPatentEntries();
    resetPatentForm();
  } catch (err) {
    handleError(err, isEditingPatent.value ? 'Không thể cập nhật phát minh sáng chế' : 'Không thể thêm phát minh sáng chế');
  } finally {
    saving.value = false;
  }
}

// Hàm chỉnh sửa sách, báo, công bố
function editPublicationEntry(entry) {
  newPublicationEntry.value = { ...entry };
  isEditingPublication.value = true;
}

// Hàm chỉnh sửa phát minh sáng chế
function editPatentEntry(entry) {
  newPatentEntry.value = { ...entry };
  isEditingPatent.value = true;
}

// Reset form sách, báo, công bố
function resetPublicationForm() {
  newPublicationEntry.value = {
    ten_sach: '',
    vi_tri: true,
    noi_xb: '',
    nam_xb: new Date().getFullYear(),
    loai_sach: 1,
    ma_sach: 0,
    ma_gv: ''
  };
  isEditingPublication.value = false;
}

// Reset form phát minh sáng chế
function resetPatentForm() {
  newPatentEntry.value = {
    ten_pmsc: '',
    loai_pmsc: 'Sáng chế',
    thong_tin: '',
    tg_cap_bang: new Date().getFullYear(),
    ma_gv: '',
    ma_pmsc: 0
  };
  isEditingPatent.value = false;
}

// Xử lý lỗi
function handleError(err, defaultMessage) {
  console.error(err);
  error.value = err.response?.data?.detail || defaultMessage;
}

// Xử lý đăng xuất
function handleLogout() {
  authStore.logout();
  router.push('/login');
}

// Hàm helper để hiển thị loại sách
function getLoaiSachText(loaiSach) {
  const loaiSachMap = {
    1: 'Sách giáo khoa',
    2: 'Sách tham khảo',
    3: 'Sách chuyên khảo',
    4: 'Báo cáo khoa học'
  };
  return loaiSachMap[loaiSach] || 'Không xác định';
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
.sachBaoCongBo,
.phatMinhSangChe {
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

textarea.input-field {
  resize: vertical;
  min-height: 80px;
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