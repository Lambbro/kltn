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

        <!-- Thông tin cá nhân -->
        <div class="column">
          <h2 class="section-title">Thông tin cá nhân</h2>
          <div class="image">
            <UploadImage 
              :image-url="teacher.anh_dai_dien" 
              :disabled="!isEditable || isViewOnly" 
              :ma-gv="teacher.ma_gv"
              @update:image="handleImageUpdate" 
            />
          </div>
          <div class="information">
            <div class="info-row">
              <p class="label">Họ và tên</p>
              <input 
                type="text" 
                v-model="teacher.ten_gv" 
                :readonly="!isEditable"
                class="input-field"
              />
            </div>
            <div class="info-row">
              <p class="label">Căn cước công dân</p>
              <input 
                type="text" 
                v-model="teacher.cccd" 
                :readonly="!isEditable"
                class="input-field"
              />
            </div>
            <div class="info-row">
              <p class="label">Giới tính</p>
              <div class="gender-options">
                <label>
                  <input 
                    type="radio" 
                    v-model="teacher.gioi_tinh" 
                    :value="true" 
                    :disabled="!isEditable"
                    class="radio-input"
                  /> Nam
                </label>
                <label>
                  <input 
                    type="radio" 
                    v-model="teacher.gioi_tinh" 
                    :value="false" 
                    :disabled="!isEditable"
                    class="radio-input"
                  /> Nữ
                </label>
              </div>
            </div>
            <div class="info-row">
              <p class="label">Ngày sinh</p>
              <input 
                type="date" 
                v-model="teacher.ngay_sinh" 
                :readonly="!isEditable"
                class="input-field"
              />
            </div>
            <div class="info-row">
              <p class="label">Địa chỉ</p>
              <input 
                type="text" 
                v-model="teacher.que_quan" 
                :readonly="!isEditable"
                class="input-field"
              />
            </div>
            <div class="info-row">
              <p class="label">Số điện thoại</p>
              <input 
                type="text" 
                v-model="teacher.sdt" 
                :readonly="!isEditable"
                class="input-field"
              />
            </div>
            <div class="info-row">
              <p class="label">Email</p>
              <input 
                type="text" 
                v-model="teacher.email" 
                :readonly="!isEditable"
                class="input-field"
              />
            </div>
            <div class="info-row">
              <p class="label">Đơn vị công tác</p>
              <input 
                type="text" 
                v-model="teacher.don_vi_cong_tac" 
                :readonly="!isEditable"
                class="input-field"
              />
            </div>
            <div class="info-row">
              <p class="label">Địa chỉ công tác</p>
              <input 
                type="text" 
                v-model="teacher.dia_chi_cong_tac" 
                :readonly="!isEditable"
                class="input-field"
              />
            </div>
            <div class="info-row">
              <p class="label">Khoa</p>
              <select 
                v-model="teacher.ma_khoa" 
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
                :value="teacher.ma_khoa" 
                readonly 
                class="input-field readonly"
              />
            </div>
          </div>
          <button 
            v-if="isEditable && !isViewOnly" 
            class="save-button"
            @click="saveChanges" 
            :disabled="saving"
          >
            {{ saving ? 'Đang lưu...' : 'Lưu thông tin' }}
          </button>
        </div>

        <!-- Chức danh khoa học -->
        <div class="column">
          <h2 class="section-title">Chức danh khoa học</h2>
          <div class="scientific-title">
            <div class="info-row">
              <p class="label">Chức danh</p>
              <input 
                type="text" 
                v-model="chucDanhKhoaHoc.chuc_danh" 
                :readonly="!isEditable"
                class="input-field"
                placeholder="Nhập chức danh"
              />
            </div>
            <div class="info-row">
              <p class="label">Chức vụ</p>
              <input 
                type="text" 
                v-model="chucDanhKhoaHoc.chuc_vu" 
                :readonly="!isEditable"
                class="input-field"
                placeholder="Nhập chức vụ"
              />
            </div>
            <div class="info-row">
              <p class="label">Phó Giáo Sư</p>
              <div class="title-status">
                <div class="checkbox-container">
                  <input 
                    type="checkbox" 
                    :checked="chucDanhKhoaHoc.nam_dat_pgs > 0"
                    @change="(e) => chucDanhKhoaHoc.nam_dat_pgs = e.target.checked ? new Date().getFullYear() : 0"
                    :disabled="!isEditable"
                    class="checkbox-input"
                  />
                  <span>Đã đạt</span>
                </div>
                <div v-if="chucDanhKhoaHoc.nam_dat_pgs > 0" class="year-input-container">
                  <span class="year-label">Năm đạt:</span>
                  <input 
                    type="number" 
                    v-model="chucDanhKhoaHoc.nam_dat_pgs"
                    :readonly="!isEditable"
                    class="year-input"
                    min="1900"
                    :max="new Date().getFullYear()"
                    placeholder="Nhập năm"
                  />
                </div>
              </div>
            </div>
            <div class="info-row">
              <p class="label">Giáo Sư</p>
              <div class="title-status">
                <div class="checkbox-container">
                  <input 
                    type="checkbox" 
                    :checked="chucDanhKhoaHoc.nam_dat_gs > 0"
                    @change="(e) => chucDanhKhoaHoc.nam_dat_gs = e.target.checked ? new Date().getFullYear() : 0"
                    :disabled="!isEditable"
                    class="checkbox-input"
                  />
                  <span>Đã đạt</span>
                </div>
                <div v-if="chucDanhKhoaHoc.nam_dat_gs > 0" class="year-input-container">
                  <span class="year-label">Năm đạt:</span>
                  <input 
                    type="number" 
                    v-model="chucDanhKhoaHoc.nam_dat_gs"
                    :readonly="!isEditable"
                    class="year-input"
                    min="1900"
                    :max="new Date().getFullYear()"
                    placeholder="Nhập năm"
                  />
                </div>
              </div>
            </div>
          </div>
          <button 
            v-if="isEditable && !isViewOnly" 
            class="save-button"
            @click="saveChucDanhChanges" 
            :disabled="savingChucDanh"
          >
            {{ savingChucDanh ? 'Đang lưu...' : 'Lưu chức danh' }}
          </button>
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
import UploadImage from '../../components/UploadImage.vue';
import SidebarInfo from '../../components/SidebarInfo.vue';
import api from '@/config/api';

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

// Trạng thái dữ liệu giảng viên
const teacher = ref({
  ma_gv: '',
  ten_gv: '',
  anh_dai_dien: '',
  cccd: '',
  gioi_tinh: true,
  ngay_sinh: '',
  que_quan: '',
  sdt: '',
  don_vi_cong_tac: '',
  dia_chi_cong_tac: '',
  email: '',
  ma_khoa: '',
  chuc_danh: {
    pho_giao_su: false,
    pho_giao_su_nam: '',
    giao_su: false,
    giao_su_nam: '',
    chuc_danh: '',
    chuc_vu: '',
  },
});

// Danh sách khoa
const khoaList = ref([]);
const loading = ref(false);
const saving = ref(false);
const error = ref('');

// Khởi tạo authStore và router
const authStore = useAuthStore();
const teacherViewStore = useTeacherViewStore();
const router = useRouter();
const route = useRoute();

// Kiểm tra quyền chỉnh sửa
const isViewOnly = computed(() => route.query.viewOnly === 'true' || authStore.user?.quyen_han === 4);
const isEditable = computed(() => {
  if (isViewOnly.value) return false;
  return authStore.user?.quyen_han < 4;
});

// Thêm computed properties cho authentication
const isAuthenticated = computed(() => authStore.isAuthenticated);
const storedEmail = computed(() => authStore.user?.email || '');

// Lấy dữ liệu khi component được mount
onMounted(() => {
  authStore.loadUserFromStorage();
  fetchTeacher();
  fetchKhoa();
});

// Trong phần script setup, thêm biến chucDanhKhoaHoc
const chucDanhKhoaHoc = ref({
  chuc_danh: '',
  chuc_vu: '',
  nam_dat_pgs: 0,
  nam_dat_gs: 0,
  ma_cd: 0,
  ma_gv: ''
});

// Lấy thông tin giảng viên từ API
async function fetchTeacher() {
  try {
    loading.value = true;
    error.value = '';

    // Lấy ma_gv từ query parameters hoặc từ email của user đang đăng nhập
    const ma_gv = route.query.ma_gv || (authStore.user?.email?.split('@')[0]);
    
    if (!ma_gv) {
      throw new Error('Không tìm thấy mã giảng viên');
    }

    // Lưu ma_gv vào store
    teacherViewStore.setCurrentTeacherId(ma_gv);

    const response = await api.get(`phongkhdn/gv/${ma_gv}/`);
    const data = response.data;

    if (!data || typeof data !== 'object') {
      throw new Error('Dữ liệu giảng viên không hợp lệ');
    }

    teacher.value = {
      ma_gv: data.ma_gv || '',
      ten_gv: data.ten_gv || '',
      anh_dai_dien: data.anh_dai_dien || '',
      cccd: data.cccd || '',
      gioi_tinh: typeof data.gioi_tinh === 'boolean' ? data.gioi_tinh : true,
      ngay_sinh: data.ngay_sinh || '',
      que_quan: data.que_quan || '',
      sdt: data.sdt || '',
      don_vi_cong_tac: data.don_vi_cong_tac || '',
      dia_chi_cong_tac: data.dia_chi_cong_tac || '',
      email: data.email || '',
      ma_khoa: data.ma_khoa || '',
    };

    // Gọi API lấy thông tin chức danh khoa học sau khi có ma_gv
    await fetchScientificTitle(ma_gv);
  } catch (err) {
    handleError(err, 'Không thể tải thông tin giảng viên');
  } finally {
    loading.value = false;
  }
}

// Cập nhật hàm fetchScientificTitle
async function fetchScientificTitle(ma_gv) {
  try {
    if (!ma_gv) {
      console.error('Mã giảng viên không hợp lệ:', ma_gv);
      return;
    }

    const response = await api.get(`/syll/chucdanhkhoahoc/${ma_gv}`);
    console.log('Dữ liệu từ API:', response.data);

    const data = response.data;
    if (data && typeof data === 'object') {
      chucDanhKhoaHoc.value = {
        chuc_danh: data.chuc_danh ?? '',
        chuc_vu: data.chuc_vu ?? '',
        nam_dat_pgs: data.nam_dat_pgs ?? 0,
        nam_dat_gs: data.nam_dat_gs ?? 0,
        ma_cd: data.ma_cd ?? 0,
        ma_gv: data.ma_gv ?? ma_gv
      };
      console.log('chucDanhKhoaHoc:', chucDanhKhoaHoc.value);
    } else {
      console.warn('Không có dữ liệu chức danh khoa học');
    }
  } catch (err) {
    console.error('Lỗi khi gọi API chức danh khoa học:', err);
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

// Trong phần script setup, cập nhật hàm updateImage
function updateImage(newImageUrl) {
  if (isEditable.value) {
    teacher.value.anh_dai_dien = newImageUrl;
    // Không cần gọi API ở đây nữa vì đã được xử lý trong component UploadImage
  }
}

// Hàm lưu thông tin
const saveChanges = async () => {
  if (!isEditable.value) return;

  try {
    saving.value = true;
    error.value = '';

    const updatedData = {
      ten_gv: teacher.value.ten_gv,
      cccd: teacher.value.cccd,
      gioi_tinh: teacher.value.gioi_tinh,
      ngay_sinh: teacher.value.ngay_sinh,
      que_quan: teacher.value.que_quan,
      sdt: teacher.value.sdt,
      don_vi_cong_tac: teacher.value.don_vi_cong_tac,
      dia_chi_cong_tac: teacher.value.dia_chi_cong_tac,
      email: teacher.value.email,
      ma_khoa: teacher.value.ma_khoa
    };

    const response = await api.put(`phongkhdn/gv/update/${teacher.value.ma_gv}/`, updatedData);
    if (response.data?.success) {
      alert('Lưu thông tin thành công!');
      teacher.value = response.data.data; // Cập nhật dữ liệu từ server
      tempImage.value = null; // Reset ảnh tạm
    } else {
      throw new Error(response.data?.message || 'Lỗi không xác định');
    }
  } catch (err) {
    handleError(err, 'Không thể lưu thông tin');
  } finally {
    saving.value = false;
  }
};

// Hàm xử lý khi component upload ảnh emit sự kiện
const handleImageUpdate = (imageUrl) => {
  tempImage.value = imageUrl; // Lưu URL ảnh tạm thời
  teacher.value.anh_dai_dien = imageUrl; // Cập nhật giao diện ngay lập tức
};

// Add to script setup section
const savingChucDanh = ref(false);

// Cập nhật hàm saveChucDanhChanges
async function saveChucDanhChanges() {
  if (!isEditable.value) return;

  try {
    savingChucDanh.value = true;
    error.value = '';

    const payload = {
      chuc_danh: chucDanhKhoaHoc.value.chuc_danh,
      chuc_vu: chucDanhKhoaHoc.value.chuc_vu,
      nam_dat_pgs: chucDanhKhoaHoc.value.nam_dat_pgs,
      nam_dat_gs: chucDanhKhoaHoc.value.nam_dat_gs,
      ma_gv: teacher.value.ma_gv
    };

    if (chucDanhKhoaHoc.value.ma_cd) {
      // Nếu đã có, cập nhật
      await api.put(`syll/chucdanhkhoahoc/${chucDanhKhoaHoc.value.ma_cd}`, payload);
    } else {
      // Nếu chưa có, thêm mới
      await api.post('syll/chucdanhkhoahoc', payload);
    }
    alert('Lưu thông tin chức danh thành công!');
  } catch (err) {
    handleError(err, 'Không thể lưu thông tin chức danh');
  } finally {
    savingChucDanh.value = false;
  }
}

// Hàm xử lý lỗi chung
function handleError(err, defaultMessage) {
  let errorMsg = defaultMessage;
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
    }
  } else if (err.request) {
    errorMsg = 'Không thể kết nối đến server';
  } else {
    errorMsg = err.message;
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

/* Information Section */
.information {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.info-row {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 8px 0;
}

.label {
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

.input-field.readonly {
  background: #f1f5f9;
  cursor: not-allowed;
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

  .label,
  .degree-label,
  .title-label {
    width: 180px;
  }

  .input-field,
  .degree-input,
  .title-input,
  .checkbox-container {
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

  .info-row,
  .degree-row,
  .title-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
    padding: 12px 0;
  }

  .label,
  .degree-label,
  .title-label {
    width: 100%;
    font-size: 0.9rem;
  }

  .input-field,
  .degree-input,
  .title-input,
  .checkbox-container {
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

  .info-row,
  .degree-row,
  .title-row {
    padding: 10px 0;
  }

  .label,
  .degree-label,
  .title-label {
    font-size: 0.85rem;
  }

  .input-field,
  .degree-input,
  .title-input {
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

/* Status Messages */
.loading-text {
  color: #4b5563;
}

.error-text {
  color: #ef4444;
}

/* Gender Options */
.gender-options {
  display: flex;
  gap: 12px;
}

.radio-input {
  margin-right: 6px;
}

.radio-input:checked {
  background-color: #0082c6;
  border-color: #0082c6;
}

/* Checkbox */
.checkbox-input:checked {
  background-color: #0082c6;
  border-color: #0082c6;
}

/* Academic Degree and Scientific Title */
.academic-degree,
.scientific-title {
  display: flex;
  flex-direction: column;
  gap: 12px;
  background: #f8fafc;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #0082c6;
}

.degree-row,
.title-row {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 6px 0;
}

.degree-label,
.title-label {
  font-weight: 500;
  color: #1e293b;
  font-size: 0.9rem;
  width: 150px;
  flex-shrink: 0;
}

.degree-input,
.title-input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 0.9rem;
  background: white;
  transition: all 0.3s ease;
  min-width: 0;
  max-width: 300px;
}

.degree-input:focus,
.title-input:focus {
  border-color: #0082c6;
  box-shadow: 0 0 0 2px rgba(0, 130, 198, 0.1);
  outline: none;
}

.degree-input.readonly,
.title-input.readonly {
  background: #f1f5f9;
  cursor: not-allowed;
}

/* Checkbox Container */
.checkbox-container {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 300px;
}

.checkbox-input {
  width: 16px;
  height: 16px;
  border: 2px solid #e2e8f0;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

/* Save Button for sections */
.save-button {
  margin-top: 15px;
  background: #0082c6;
  color: white;
  padding: 8px 16px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
  width: auto;
  min-width: 150px;
  align-self: flex-start;
}

.save-button:hover {
  background: #0069a3;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.save-button:disabled {
  background: #93c5fd;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

/* Responsive adjustments */
@media (max-width: 1024px) {
  .degree-label,
  .title-label {
    width: 130px;
  }

  .degree-input,
  .title-input,
  .checkbox-container {
    max-width: 250px;
  }
}

@media (max-width: 768px) {
  .academic-degree,
  .scientific-title {
    padding: 15px;
  }

  .degree-row,
  .title-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 6px;
    padding: 8px 0;
  }

  .degree-label,
  .title-label {
    width: 100%;
    font-size: 0.85rem;
  }

  .degree-input,
  .title-input,
  .checkbox-container {
    width: 100%;
    max-width: none;
  }

  .save-button {
    width: 100%;
    margin-top: 12px;
  }
}

@media (max-width: 480px) {
  .academic-degree,
  .scientific-title {
    padding: 12px;
  }

  .section-title {
    font-size: 1rem;
    margin-bottom: 8px;
  }

  .degree-row,
  .title-row {
    padding: 6px 0;
  }

  .degree-input,
  .title-input {
    padding: 6px 10px;
    font-size: 0.85rem;
  }
}

.input-field[readonly],
.input-field:disabled {
  background-color: #f1f5f9;
  cursor: not-allowed;
  opacity: 0.8;
}

.view-only-message {
  text-align: center;
  color: #64748b;
  font-size: 0.9rem;
  margin-top: 10px;
  font-style: italic;
}

/* Title Status */
.title-status {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.year-achieved {
  color: #0082c6;
  font-weight: 500;
  font-size: 0.9rem;
}

.checkbox-container {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.checkbox-container span {
  font-size: 0.9rem;
  color: #4b5563;
}

.year-input-container {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-left: 16px;
}

.year-label {
  font-size: 0.9rem;
  color: #4b5563;
  white-space: nowrap;
}

.year-input {
  width: 100px;
  padding: 6px 8px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 0.9rem;
  background: white;
  transition: all 0.3s ease;
}

.year-input:focus {
  border-color: #0082c6;
  box-shadow: 0 0 0 2px rgba(0, 130, 198, 0.1);
  outline: none;
}

.year-input[readonly] {
  background: #f1f5f9;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .year-input-container {
    margin-left: 8px;
  }
  
  .year-input {
    width: 80px;
  }
}

.image {
  display: flex;
  justify-content: center;
  margin-bottom: 2rem;
}
</style>