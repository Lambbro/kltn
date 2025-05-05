<template>
  <div class="container">
    <div
      v-if="sidebarOpen"
      class="overlay"
      @click="toggleSidebar"
    ></div>

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
    <SidebarInfoStudents :is-open="isSidebarOpen" @toggle="toggleSidebar" />

    <!-- Nội dung chính -->
    <div class="main-content" :class="{ 'main-content-shifted': isSidebarOpen && !isMobile }">
      <div class="content">
        <!-- Thông báo trạng thái -->
        <p v-if="loading" class="loading-text">Đang tải dữ liệu...</p>
        <p v-else-if="error" class="error-text">{{ error }}</p>

        <!-- Cột thông tin cá nhân -->
        <div v-else class="column">
          <div class="image">
            <UploadImage
              :image-url="student.anh_dai_dien"
              :disabled="!isEditable"
              @update:image="updateImage"
            />
          </div>
          <div class="information">
            <div class="info-row">
              <p class="label">Căn cước công dân</p>
              <input
                type="text"
                v-model="student.cccd"
                :readonly="!isEditable"
                class="input-field"
              />
            </div>
            <div class="info-row">
              <p class="label">Họ và tên</p>
              <input
                type="text"
                v-model="student.ten_sv"
                :readonly="!isEditable"
                class="input-field"
              />
            </div>
            <div class="info-row">
              <p class="label">Mã sinh viên</p>
              <input
                type="text"
                v-model="student.ma_sv"
                readonly
                class="input-field readonly"
              />
            </div>
            <div class="info-row">
              <p class="label">Giới tính</p>
              <div class="gender-options">
                <label>
                  <input
                    type="radio"
                    v-model="student.gioi_tinh"
                    :value="true"
                    :disabled="!isEditable"
                    class="radio-input"
                  />
                  Nam
                </label>
                <label>
                  <input
                    type="radio"
                    v-model="student.gioi_tinh"
                    :value="false"
                    :disabled="!isEditable"
                    class="radio-input"
                  />
                  Nữ
                </label>
              </div>
            </div>
            <div class="info-row">
              <p class="label">Ngày sinh</p>
              <input
                type="date"
                v-model="student.ngay_sinh"
                :readonly="!isEditable"
                class="input-field"
              />
            </div>
            <div class="info-row">
              <p class="label">Địa chỉ</p>
              <input
                type="text"
                v-model="student.que_quan"
                :readonly="!isEditable"
                class="input-field"
              />
            </div>
            <div class="info-row">
              <p class="label">Số điện thoại</p>
              <input
                type="text"
                v-model="student.sdt"
                :readonly="!isEditable"
                class="input-field"
              />
            </div>
            <div class="info-row">
              <p class="label">Email</p>
              <input
                type="text"
                v-model="student.email"
                :readonly="!isEditable"
                class="input-field"
              />
            </div>
            <div class="info-row">
              <p class="label">Lớp hành chính</p>
              <input
                type="text"
                v-model="student.lop_hc"
                :readonly="!isEditable"
                class="input-field"
              />
            </div>
            <div class="info-row">
              <p class="label">Khóa học</p>
              <input
                type="number"
                v-model.number="student.khoa_hoc"
                :readonly="!isEditable"
                class="input-field"
              />
            </div>
            <div class="info-row">
              <p class="label">Khoa</p>
              <select
                v-model="student.ma_khoa"
                :disabled="!isEditable"
                v-if="khoaList.length"
                class="input-field"
              >
                <option v-for="khoa in khoaList" :key="khoa.ma_khoa" :value="khoa.ma_khoa">
                  {{ khoa.ten_khoa }}
                </option>
              </select>
              <input
                v-else
                type="text"
                :value="student.ma_khoa"
                readonly
                class="input-field readonly"
              />
            </div>
          </div>
          <button
            v-if="isEditable"
            class="save-button"
            @click="saveChanges"
            :disabled="saving"
          >
            {{ saving ? 'Đang lưu...' : 'Lưu thay đổi' }}
          </button>
        </div>
      </div>
      <router-view></router-view>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import UploadImage from '../../components/UploadImage.vue';
import SidebarInfoStudents from '../../components/SidebarInfoStudents.vue';
import api from '@/config/api';

// Trạng thái sidebar
const isSidebarOpen = ref(false);
const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value;
  localStorage.setItem('sidebarOpen', JSON.stringify(isSidebarOpen.value));
};

// Kiểm tra màn hình mobile
const isMobile = ref(window.innerWidth <= 768);
window.addEventListener('resize', () => {
  isMobile.value = window.innerWidth <= 768;
  if (isMobile.value && isSidebarOpen.value) {
    isSidebarOpen.value = false;
    localStorage.setItem('sidebarOpen', JSON.stringify(isSidebarOpen.value));
  }
});

// Khôi phục trạng thái sidebar
onMounted(() => {
  const savedSidebarState = localStorage.getItem('sidebarOpen');
  if (savedSidebarState !== null) {
    isSidebarOpen.value = JSON.parse(savedSidebarState);
  }
});

// Trạng thái dữ liệu sinh viên
const student = ref({
  ma_sv: '',
  ten_sv: '',
  anh_dai_dien: '',
  cccd: '',
  gioi_tinh: true,
  ngay_sinh: '',
  que_quan: '',
  sdt: '',
  lop_hc: '',
  khoa_hoc: 0,
  email: '',
  ma_khoa: '',
});

// Danh sách khoa
const khoaList = ref([]);
const loading = ref(false);
const saving = ref(false);
const error = ref('');

// Khởi tạo authStore và router
const authStore = useAuthStore();
const router = useRouter();

// Kiểm tra quyền chỉnh sửa
const isEditable = computed(() => authStore.user?.quyen_han === 1);

// Trạng thái đăng nhập
const isAuthenticated = computed(() => authStore.isAuthenticated);
const storedEmail = computed(() => authStore.user?.email || '');

// Lấy dữ liệu khi component được mount
onMounted(() => {
  authStore.loadUserFromStorage();
  fetchStudent();
  fetchKhoa();
});

// Lấy thông tin sinh viên từ API
async function fetchStudent() {
  try {
    loading.value = true;
    error.value = '';

    // Lấy mã sinh viên từ query parameter hoặc từ email người dùng
    const ma_sv = router.currentRoute.value.query.ma_sv || authStore.user?.email?.split('@')[0];
    
    if (!ma_sv) {
      throw new Error('Không tìm thấy mã sinh viên');
    }

    const response = await api.get(`phongkhdn/sv/${ma_sv}/`);
    const data = response.data;

    if (!data || typeof data !== 'object') {
      throw new Error('Dữ liệu sinh viên không hợp lệ');
    }

    student.value = {
      ma_sv: data.ma_sv || '',
      ten_sv: data.ten_sv || '',
      anh_dai_dien: data.anh_dai_dien || '',
      cccd: data.cccd || '',
      gioi_tinh: typeof data.gioi_tinh === 'boolean' ? data.gioi_tinh : true,
      ngay_sinh: data.ngay_sinh || '',
      que_quan: data.que_quan || '',
      sdt: data.sdt || '',
      lop_hc: data.lop_hc || '',
      khoa_hoc: typeof data.khoa_hoc === 'number' ? data.khoa_hoc : 0,
      email: data.email || '',
      ma_khoa: data.ma_khoa || '',
    };
  } catch (err) {
    handleError(err, 'Không thể tải thông tin sinh viên');
  } finally {
    loading.value = false;
  }
}

// Lấy danh sách khoa từ API
async function fetchKhoa() {
  try {
    const response = await api.get('phongkhdn/khoa/');
    const data = response.data;

    if (!Array.isArray(data)) {
      console.error('Dữ liệu khoa không phải mảng:', data);
      return;
    }

    khoaList.value = data.map((khoa) => ({
      ma_khoa: khoa.ma_khoa || '',
      ten_khoa: khoa.ten_khoa || 'Không xác định',
    }));
  } catch (err) {
    console.error('Lỗi khi lấy danh sách khoa:', err);
  }
}

// Xử lý khi ảnh được cập nhật
function updateImage(newImageUrl) {
  if (isEditable.value) {
    student.value.anh_dai_dien = newImageUrl;
  }
}
// Lưu thay đổi thông tin sinh viên
async function saveChanges() {
  if (!isEditable.value) return;

  try {
    saving.value = true;
    error.value = '';

    const updatedData = {
      ten_sv: student.value.ten_sv,
      anh_dai_dien: student.value.anh_dai_dien,
      cccd: student.value.cccd,
      gioi_tinh: student.value.gioi_tinh,
      ngay_sinh: student.value.ngay_sinh,
      que_quan: student.value.que_quan,
      sdt: student.value.sdt,
      lop_hc: student.value.lop_hc,
      khoa_hoc: student.value.khoa_hoc,
      email: student.value.email,
      ma_khoa: student.value.ma_khoa,
    };

    await api.patch(`phongkhdn/sv/${student.value.ma_sv}/`, updatedData);
    alert('Lưu thông tin thành công!');
  } catch (err) {
    handleError(err, 'Không thể lưu thông tin');
  } finally {
    saving.value = false;
  }
}

// Xử lý đăng xuất
const handleLogout = () => {
  authStore.logout();
  router.push('/login');
};

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
</script>

<style scoped>
/* Container */
.container {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f8fafc;
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
  background: #2563eb;
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
  background: #1d4ed8;
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
}

.header h1 {
  font-size: 1.2rem;
  color: #1e293b;
  font-weight: 600;
  margin: 0;
  flex-grow: 1;
  text-align: center;
  background: linear-gradient(135deg, #2563eb, #1e40af);
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
  background: #2563eb;
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
  background: #1d4ed8;
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
  margin-top: 100px; /* 70px header height + 30px spacing */
  margin-left: 250px; /* 220px sidebar width + 30px spacing */
  padding: 30px;
  box-sizing: border-box;
  background: #f8fafc;
  transition: margin-left 0.3s ease;
  min-height: calc(100vh - 100px);
}

.main-content-shifted {
  margin-left: 250px;
}

/* Content Grid */
.content {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr;
  gap: 30px;
}

/* Column */
.column {
  background: white;
  border-radius: 16px;
  padding: 30px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.column:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.1);
}

/* Image Section */
.image {
  display: flex;
  justify-content: center;
  margin-bottom: 30px;
}

/* Information Section */
.information {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.info-row {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.label {
  font-weight: 600;
  color: #1e293b;
  font-size: 0.95rem;
}

.input-field {
  width: 100%;
  padding: 12px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.95rem;
  background: #f8fafc;
  transition: all 0.3s ease;
}

.input-field:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
  background: white;
  outline: none;
}

.input-field.readonly {
  background: #f1f5f9;
  cursor: not-allowed;
}

/* Gender Options */
.gender-options {
  display: flex;
  gap: 20px;
  margin-top: 8px;
}

.gender-options label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  color: #475569;
}

.radio-input {
  width: 16px;
  height: 16px;
  cursor: pointer;
}

/* Save Button */
.save-button {
  margin-top: 30px;
  background: #2563eb;
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
  background: #1d4ed8;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.save-button:disabled {
  background: #93c5fd;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

/* Status Messages */
.loading-text {
  color: #64748b;
  text-align: center;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.error-text {
  color: #dc2626;
  text-align: center;
  padding: 20px;
  background: #fee2e2;
  border-radius: 8px;
  margin: 20px 0;
  border: 1px solid #fecaca;
}

/* Responsive Header */
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

  .auth-buttons {
    gap: 12px;
  }

  .mobile-toggle {
    top: 24px;
    left: 20px;
    width: 30px;
    height: 30px;
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

  .auth-buttons {
    gap: 8px;
  }

  .user-email {
    display: none; /* Ẩn email trên màn hình tablet */
  }

  .login-btn, .logout-btn {
    padding: 6px 12px;
    font-size: 0.9rem;
    min-width: 90px;
  }

  .mobile-toggle {
    top:20px;
    left: 10px;
    width: 28px;
    height: 28px;
  }

  .toggle-icon {
    font-size: 1.1rem;
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

  .auth-buttons {
    gap: 6px;
  }

  .user-email {
    display: none; /* Ẩn email trên màn hình mobile */
  }

  .login-btn, .logout-btn {
    padding: 5px 10px;
    font-size: 0.8rem;
    min-width: 80px;
  }

  .mobile-toggle {

    left: 10px;
    width: 26px;
    height: 26px;
  }

  .toggle-icon {
    font-size: 1rem;
  }
}

/* Responsive */
@media (max-width: 1024px) {
  .main-content {
    margin-left: 250px;
    padding: 25px;
  }
}

@media (max-width: 768px) {
  .main-content {
    margin-top: 90px; /* 60px header height + 30px spacing */
    margin-left: 0;
    padding: 20px;
  }

  .main-content-shifted {
    margin-left: 0;
  }

  .information {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .main-content {
    margin-top: 80px; /* 50px header height + 30px spacing */
    padding: 15px;
  }

  .column {
    padding: 15px;
  }

  .input-field {
    padding: 10px;
    font-size: 0.9rem;
  }

  .save-button {
    padding: 10px 20px;
    font-size: 0.9rem;
  }
}
</style>