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

        <!-- Cột nhập liệu Trình độ học vấn -->
        <div v-else class="column" v-show="canEdit">
          <div class="hocVi">
            <p class="section-title">Thêm thông tin trình độ học vấn</p>
            <div class="info-row">
              <p class="sub-label">Bậc đào tạo</p>
              <select v-model="newEducationEntry.bac_dao_tao" class="input-field">
                <option value="1">Đại học</option>
                <option value="2">Thạc sĩ</option>
                <option value="3">Tiến sĩ</option>
                <option value="4">Tiến sĩ khoa học</option>
              </select>
            </div>
            <div class="info-row">
              <p class="sub-label">Ngành</p>
              <input type="text" v-model="newEducationEntry.nganh" class="input-field" />
            </div>
            <div class="info-row">
              <p class="sub-label">Chuyên ngành</p>
              <input type="text" v-model="newEducationEntry.chuyen_nganh" class="input-field" />
            </div>
            <div class="info-row">
              <p class="sub-label">Nơi đào tạo</p>
              <input type="text" v-model="newEducationEntry.noi_dao_tao" class="input-field" />
            </div>
            <div class="info-row">
              <p class="sub-label">Năm tốt nghiệp</p>
              <input type="number" v-model="newEducationEntry.nam_tot_nghiep" class="input-field" />
            </div>
            <button @click="addEducationEntry" class="save-button" :disabled="saving">
              {{ saving ? 'Đang lưu...' : 'Cập nhật' }}
            </button>
          </div>
        </div>

        <!-- Cột bảng hiển thị Trình độ học vấn -->
        <div class="column">
          <div class="table-container">
            <p class="section-title">Trình độ học vấn</p>
            <table>
              <thead>
                <tr>
                  <th>Bậc đào tạo</th>
                  <th>Ngành</th>
                  <th>Chuyên ngành</th>
                  <th>Nơi đào tạo</th>
                  <th>Năm tốt nghiệp</th>
                  <th v-if="canEdit">Hành động</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(entry, index) in educationEntries" :key="index">
                  <td>{{ getBacDaoTaoName(entry.bac_dao_tao) }}</td>
                  <td>{{ entry.nganh }}</td>
                  <td>{{ entry.chuyen_nganh }}</td>
                  <td>{{ entry.noi_dao_tao }}</td>
                  <td>{{ entry.nam_tot_nghiep }}</td>
                  <td v-if="canEdit">
                    <button @click="editEducationEntry(entry)" class="edit-button">
                      Sửa
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Cột nhập liệu Trình độ ngoại ngữ -->
        <div class="column" v-show="canEdit">
          <div class="ngoaiNgu">
            <p class="section-title">Thêm thông tin ngoại ngữ</p>
            <div class="info-row">
              <p class="sub-label">Ngoại ngữ</p>
              <select v-model="newLanguageEntry.ngoai_ngu" class="input-field">
                <option value="Tiếng Anh">Tiếng Anh</option>
                <option value="Tiếng Pháp">Tiếng Pháp</option>
                <option value="Tiếng Trung">Tiếng Trung</option>
                <option value="Tiếng Nhật">Tiếng Nhật</option>
                <option value="Tiếng Nga">Tiếng Nga</option>
                <option value="Tiếng Hàn">Tiếng Hàn</option>
                <option value="Tiếng Đức">Tiếng Đức</option>
                <option value="Tiếng Tây Ban Nha">Tiếng Tây Ban Nha</option>
                <option value="Tiếng Bồ Đào Nha">Tiếng Bồ Đào Nha</option>
                <option value="Tiếng Đan Mạch">Tiếng Đan Mạch</option>
                <option value="Tiếng Thụy Điển">Tiếng Thụy Điển</option>
                <option value="Tiếng Na Uy">Tiếng Na Uy</option>
                
                <option value="Khác">Khác</option>
              </select>
            </div>
            <div class="info-row">
              <p class="sub-label">Nghe</p>
              <select v-model="newLanguageEntry.nghe" class="input-field">
                <option value="1">Thông thạo</option>
                <option value="2">Rất tốt</option>
                <option value="3">Tốt</option>
                <option value="4">Khá</option>
                <option value="5">Bình thường</option>
              </select>
            </div>
            <div class="info-row">
              <p class="sub-label">Nói</p>
              <select v-model="newLanguageEntry.noi" class="input-field">
                <option value="1">Thông thạo</option>
                <option value="2">Rất tốt</option>
                <option value="3">Tốt</option>
                <option value="4">Khá</option>
                <option value="5">Bình thường</option>
              </select>
            </div>
            <div class="info-row">
              <p class="sub-label">Đọc</p>
              <select v-model="newLanguageEntry.doc" class="input-field">
                <option value="1">Thông thạo</option>
                <option value="2">Rất tốt</option>
                <option value="3">Tốt</option>
                <option value="4">Khá</option>
                <option value="5">Bình thường</option>
              </select>
            </div>
            <div class="info-row">
              <p class="sub-label">Viết</p>
              <select v-model="newLanguageEntry.viet" class="input-field">
                <option value="1">Thông thạo</option>
                <option value="2">Rất tốt</option>
                <option value="3">Tốt</option>
                <option value="4">Khá</option>
                <option value="5">Bình thường</option>
              </select>
            </div>
            <button @click="addLanguageEntry" class="save-button" :disabled="saving">
              {{ saving ? 'Đang lưu...' : 'Cập nhật' }}
            </button>
          </div>
        </div>

        <!-- Cột bảng hiển thị Trình độ ngoại ngữ -->
        <div class="column">
          <div class="table-container">
            <p class="section-title">Trình độ ngoại ngữ</p>
            <p class="sub-title">Mức độ: 1-Thông thạo; 2-Rất tốt; 3-Tốt; 4-Khá; 5-Bình thường</p>
            <table>
              <thead>
                <tr>
                  <th>Ngoại ngữ</th>
                  <th>Nghe</th>
                  <th>Nói</th>
                  <th>Đọc</th>
                  <th>Viết</th>
                  <th v-if="canEdit">Hành động</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(entry, index) in languageEntries" :key="index">
                  <td>{{ entry.ngoai_ngu }}</td>
                  <td>{{ getLevelName(entry.nghe) }}</td>
                  <td>{{ getLevelName(entry.noi) }}</td>
                  <td>{{ getLevelName(entry.doc) }}</td>
                  <td>{{ getLevelName(entry.viet) }}</td>
                  <td v-if="canEdit">
                    <button @click="editLanguageEntry(entry)" class="edit-button">
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

// Dữ liệu ban đầu của bảng Trình độ học vấn
const educationEntries = ref([]);

// Dữ liệu cho form nhập liệu Trình độ học vấn
const newEducationEntry = ref({
  bac_dao_tao: 1,
  chuyen_nganh: '',
  noi_dao_tao: '',
  nam_tot_nghiep: new Date().getFullYear(),
});

// Dữ liệu ban đầu của bảng Trình độ ngoại ngữ
const languageEntries = ref([]);

// Dữ liệu cho form nhập liệu Trình độ ngoại ngữ
const newLanguageEntry = ref({
  ngoai_ngu: 'Tiếng Anh',
  nghe: 3,
  noi: 3,
  doc: 3,
  viet: 3,
});

// Khởi tạo authStore và router
const authStore = useAuthStore();
const teacherViewStore = useTeacherViewStore();
const router = useRouter();
const route = useRoute();

// Thêm computed properties cho authentication
const isAuthenticated = computed(() => authStore.isAuthenticated);
const storedEmail = computed(() => authStore.user?.email || '');
const userPermission = computed(() => authStore.user?.quyen_han || 0);
const canEdit = computed(() => userPermission.value === 3);

// Thêm biến để theo dõi trạng thái chỉnh sửa
const isEditingEducation = ref(false);
const isEditingLanguage = ref(false);

// Hàm helper để lấy tên bậc đào tạo
function getBacDaoTaoName(bacDaoTao) {
  const bacDaoTaoMap = {
    1: "Đại Học",
    2: "Thạc Sĩ",
    3: "Tiến Sĩ",
    4: "Tiến Sĩ Khoa Học"
  };
  return bacDaoTaoMap[bacDaoTao] || `Bậc đào tạo ${bacDaoTao}`;
}

// Hàm helper để lấy tên mức độ
function getLevelName(level) {
  const levelMap = {
    1: "Thông thạo",
    2: "Rất tốt",
    3: "Tốt",
    4: "Khá",
    5: "Bình thường"
  };
  return levelMap[level] || `Mức ${level}`;
}

// Lấy dữ liệu khi component được mount
onMounted(() => {
  authStore.loadUserFromStorage();
  fetchEducationEntries();
  fetchLanguageEntries();
});

// Lấy danh sách Trình độ học vấn từ API
async function fetchEducationEntries() {
  try {
    loading.value = true;
    error.value = '';

    // Lấy ma_gv từ store hoặc từ email của user đang đăng nhập
    const ma_gv = teacherViewStore.getCurrentTeacherId() || (authStore.user?.email?.split('@')[0]);
    
    if (!ma_gv) {
      throw new Error('Vui lòng đăng nhập để xem thông tin');
    }

    const response = await api.get(`syll/trinhdohocvan/${ma_gv}`);
    educationEntries.value = response.data || [];
  } catch (err) {
    handleError(err, 'Không thể tải thông tin trình độ học vấn');
  } finally {
    loading.value = false;
  }
}

// Lấy danh sách Trình độ ngoại ngữ từ API
async function fetchLanguageEntries() {
  try {
    loading.value = true;
    error.value = '';

    // Lấy ma_gv từ store hoặc từ email của user đang đăng nhập
    const ma_gv = teacherViewStore.getCurrentTeacherId() || (authStore.user?.email?.split('@')[0]);
    
    if (!ma_gv) {
      throw new Error('Vui lòng đăng nhập để xem thông tin');
    }

    const response = await api.get(`syll/ngoaingu/${ma_gv}`);
    languageEntries.value = response.data || [];
  } catch (err) {
    handleError(err, 'Không thể tải thông tin trình độ ngoại ngữ');
  } finally {
    loading.value = false;
  }
}

// Hàm chỉnh sửa trình độ học vấn
function editEducationEntry(entry) {
  newEducationEntry.value = {
    ...entry,
    bac_dao_tao: parseInt(entry.bac_dao_tao),
    nam_tot_nghiep: parseInt(entry.nam_tot_nghiep)
  };
  isEditingEducation.value = true;
}

// Hàm chỉnh sửa trình độ ngoại ngữ
function editLanguageEntry(entry) {
  newLanguageEntry.value = {
    ...entry,
    nghe: parseInt(entry.nghe),
    noi: parseInt(entry.noi),
    doc: parseInt(entry.doc),
    viet: parseInt(entry.viet)
  };
  isEditingLanguage.value = true;
}

// Cập nhật hàm addEducationEntry để xử lý cả thêm mới và cập nhật
async function addEducationEntry() {
  if (
    !newEducationEntry.value.bac_dao_tao ||
    !newEducationEntry.value.nganh ||
    !newEducationEntry.value.chuyen_nganh ||
    !newEducationEntry.value.noi_dao_tao ||
    !newEducationEntry.value.nam_tot_nghiep
  ) {
    alert('Vui lòng điền đầy đủ thông tin trình độ học vấn!');
    return;
  }

  try {
    saving.value = true;
    error.value = '';

    // Lấy ma_gv từ store hoặc từ email của user đang đăng nhập
    const ma_gv = teacherViewStore.getCurrentTeacherId() || (authStore.user?.email?.split('@')[0]);
    
    if (!ma_gv) {
      throw new Error('Vui lòng đăng nhập để thêm thông tin');
    }

    // Thêm ma_gv vào dữ liệu gửi lên API
    const dataToSend = {
      ...newEducationEntry.value,
      ma_gv: ma_gv
    };

    if (isEditingEducation.value) {
      // Cập nhật thông tin
      await api.put(`syll/trinhdohocvan/${newEducationEntry.value.ma_tdhv}`, dataToSend);
      alert('Cập nhật trình độ học vấn thành công!');
    } else {
      // Thêm mới
      await api.post('syll/trinhdohocvan', dataToSend);
      alert('Thêm trình độ học vấn thành công!');
    }

    // Refresh dữ liệu sau khi thêm/cập nhật
    await fetchEducationEntries();

    // Reset form và trạng thái
    newEducationEntry.value = {
      bac_dao_tao: 1,
      nganh: '',
      chuyen_nganh: '',
      noi_dao_tao: '',
      nam_tot_nghiep: new Date().getFullYear(),
    };
    isEditingEducation.value = false;
  } catch (err) {
    handleError(err, isEditingEducation.value ? 'Không thể cập nhật trình độ học vấn' : 'Không thể thêm trình độ học vấn');
  } finally {
    saving.value = false;
  }
}

// Cập nhật hàm addLanguageEntry để xử lý cả thêm mới và cập nhật
async function addLanguageEntry() {
  if (
    !newLanguageEntry.value.ngoai_ngu ||
    !newLanguageEntry.value.nghe ||
    !newLanguageEntry.value.noi ||
    !newLanguageEntry.value.doc ||
    !newLanguageEntry.value.viet
  ) {
    alert('Vui lòng điền đầy đủ thông tin trình độ ngoại ngữ!');
    return;
  }

  try {
    saving.value = true;
    error.value = '';

    // Lấy ma_gv từ store hoặc từ email của user đang đăng nhập
    const ma_gv = teacherViewStore.getCurrentTeacherId() || (authStore.user?.email?.split('@')[0]);
    
    if (!ma_gv) {
      throw new Error('Vui lòng đăng nhập để thêm thông tin');
    }

    // Thêm ma_gv vào dữ liệu gửi lên API
    const dataToSend = {
      ...newLanguageEntry.value,
      ma_gv: ma_gv
    };

    if (isEditingLanguage.value) {
      // Cập nhật thông tin
      await api.put(`syll/ngoaingu/${newLanguageEntry.value.ma_nn}`, dataToSend);
      alert('Cập nhật trình độ ngoại ngữ thành công!');
    } else {
      // Thêm mới
      await api.post('syll/ngoaingu', dataToSend);
      alert('Thêm trình độ ngoại ngữ thành công!');
    }

    // Refresh dữ liệu sau khi thêm/cập nhật
    await fetchLanguageEntries();

    // Reset form và trạng thái
    newLanguageEntry.value = {
      ngoai_ngu: 'Tiếng Anh',
      nghe: 3,
      noi: 3,
      doc: 3,
      viet: 3,
    };
    isEditingLanguage.value = false;
  } catch (err) {
    handleError(err, isEditingLanguage.value ? 'Không thể cập nhật trình độ ngoại ngữ' : 'Không thể thêm trình độ ngoại ngữ');
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

/* Sub Title */
.sub-title {
  font-weight: 500;
  color: #4b5563;
  font-size: 0.9rem;
  margin-bottom: 10px;
}

/* Form nhập liệu */
.hocVi,
.ngoaiNgu {
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

/* Update save button text based on edit state */
.save-button {
  content: attr(data-text);
}

.save-button[data-text="Cập nhật"] {
  background: #0082c6;
}

.save-button[data-text="Lưu thay đổi"] {
  background: #059669;
}
</style>