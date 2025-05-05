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
      <div class="main-content">
        <div class="content">
          <div class="content-header">
            <h2>Quản lý sinh viên đăng ký nghiên cứu khoa học</h2>
          </div>
          <div class="filter-section" style="display: flex; align-items: center; gap: 10px;">
            <button class="filter-btn" @click="toggleFilter">
              {{ showFilter ? 'Ẩn bộ lọc' : 'Hiện bộ lọc' }}
            </button>
            <button
              class="action-btn"
              :disabled="!selectedGV || selectedSVs.length === 0"
              @click="taoNhom"
            >
              Tạo nhóm
            </button>
            <button class="action-btn" @click="toggleShowNhomNCKH">
              {{ showNhomNCKH ? 'Ẩn nhóm NCKH' : 'Hiện nhóm NCKH' }}
            </button>
          </div>

          <!-- Filter section -->
          <div v-if="showFilter" class="filter-form">
            <div class="filter-row">
              <div>
                <label class="label">Mã sinh viên</label>
                <input type="text" v-model="filterCriteria.ma_sv" class="input-field" />
              </div>
              <div>
                <label class="label">Tên sinh viên</label>
                <input type="text" v-model="filterCriteria.ten_sv" class="input-field" />
              </div>
              <div>
                <label class="label">Mã giảng viên</label>
                <input type="text" v-model="filterCriteria.ma_gv" class="input-field" />
              </div>
              <div>
                <label class="label">Hướng nghiên cứu</label>
                <select v-model="filterCriteria.ma_hnc" class="input-field">
                  <option value="">Tất cả</option>
                  <option v-for="hnc in huongNghienCuuList" :key="hnc.ma_hnc" :value="hnc.ma_hnc">
                    {{ hnc.ten_hnc }}
                  </option>
                </select>
              </div>
            </div>
          </div>

          <!-- Thông báo trạng thái -->
          <p v-if="loading" class="loading-text">Đang tải dữ liệu...</p>
          <p v-else-if="error" class="error-text">{{ error }}</p>

          <!-- Bảng danh sách đăng ký -->
          <div v-if="!loading && !error" class="table-container">
            <div class="mobile-cards">
              <div v-for="(dangky, index) in paginatedDangKyList" :key="dangky.ma_dk" class="mobile-card">
                <div class="card-header">
                  <span class="card-number">#{{ index + 1 }}</span>
                  <span class="card-status" :class="getStatusClass(dangky.trang_thai)">
                    {{ formatTrangThai(dangky.trang_thai) }}
                  </span>
                </div>
                <div class="card-body">
                  <div class="card-item">
                    <span class="label">Mã ĐK:</span>
                    <span class="value">{{ dangky.ma_dk }}</span>
                  </div>
                  <div class="card-item">
                    <span class="label">Mã SV:</span>
                    <span class="value">{{ dangky.ma_sv }}</span>
                  </div>
                  <div class="card-item">
                    <span class="label">Tên SV:</span>
                    <span class="value">{{ dangky.ten_sv }}</span>
                  </div>
                  <div class="card-item">
                    <span class="label">Giảng viên:</span>
                    <div class="value-list">
                      <div v-for="nv in dangky.list_nguyen_vong" :key="nv.ma_gv" class="list-item">
                        <input type="checkbox"
                          :checked="isGVChecked(nv.ma_gv)"
                          :disabled="!isGVChecked(nv.ma_gv) && selectedGV"
                          @change="handleSelectGV(nv.ma_gv)"
                        />
                        {{ getTenGiangVien(nv.ma_gv) }} (Ưu tiên {{ nv.muc_uu_tien }})
                      </div>
                      <div v-if="!dangky.list_nguyen_vong.length">Không có</div>
                    </div>
                  </div>
                  <div class="card-item">
                    <span class="label">Hướng nghiên cứu:</span>
                    <div class="value-list">
                      <div v-for="hnc in dangky.list_hnc" :key="hnc.ma_hnc" class="list-item">
                        {{ hnc.ten_hnc }}
                      </div>
                      <div v-if="!dangky.list_hnc.length">Không có</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <table class="dangky-table desktop-only">
              <thead>
                <tr>
                  <th>STT</th>
                  <th>Mã ĐK</th>
                  <th>Mã SV</th>
                  <th>Tên SV</th>
                  <th>Trạng Thái</th>
                  <th>Tên Giảng Viên</th>
                  <th>Hướng Nghiên Cứu</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(dangky, index) in paginatedDangKyList" :key="dangky.ma_dk">
                  <td>
                    {{ index + 1 }}
                  </td>
                  <td>{{ dangky.ma_dk }}</td>
                  <td>
                    <input type="checkbox"
                      :checked="isSVChecked(dangky.ma_sv)"
                      :disabled="!isSVChecked(dangky.ma_sv) && selectedSVs.length >= 3"
                      @change="handleSelectSV(dangky.ma_sv)"
                    />
                    {{ dangky.ma_sv }}
                  </td>
                  <td>{{ dangky.ten_sv }}</td>
                  <td>{{ formatTrangThai(dangky.trang_thai) }}</td>
                  <td>
                    <ul>
                      <li v-for="nv in dangky.list_nguyen_vong" :key="nv.ma_gv">
                        <input type="checkbox"
                          :checked="isGVChecked(nv.ma_gv)"
                          :disabled="!isGVChecked(nv.ma_gv) && selectedGV"
                          @change="handleSelectGV(nv.ma_gv)"
                        />
                        {{ getTenGiangVien(nv.ma_gv) }} (Ưu tiên {{ nv.muc_uu_tien }})
                      </li>
                      <li v-if="!dangky.list_nguyen_vong.length">Không có</li>
                    </ul>
                  </td>
                  <td>
                    <ul>
                      <li v-for="hnc in dangky.list_hnc" :key="hnc.ma_hnc">
                        {{ hnc.ten_hnc }}
                      </li>
                      <li v-if="!dangky.list_hnc.length">Không có</li>
                    </ul>
                  </td>
                </tr>
                <tr v-if="filteredDangKyList.length === 0">
                  <td colspan="7">Không có dữ liệu đăng ký</td>
                </tr>
              </tbody>
            </table>
            <div class="pagination">
              <button @click="changePageDangKy(currentPageDangKy - 1)" :disabled="currentPageDangKy === 1">Trang trước</button>
              <span>Trang {{ currentPageDangKy }} / {{ totalPagesDangKy }}</span>
              <button @click="changePageDangKy(currentPageDangKy + 1)" :disabled="currentPageDangKy === totalPagesDangKy">Trang sau</button>
            </div>
          </div>
          <div v-if="showNhomNCKH" class="nhom-nckh-list" style="margin-bottom: 24px; margin-top: 24px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
              <h3 style="color: #0082c6;">Danh sách nhóm NCKH</h3>
              <button class="filter-btn" @click="toggleFilterNhomNCKH">
                {{ showFilterNhomNCKH ? 'Ẩn bộ lọc' : 'Hiện bộ lọc' }}
              </button>
            </div>

            <!-- Bộ lọc nhóm NCKH -->
            <div v-if="showFilterNhomNCKH" class="filter-form">
              <div class="filter-row">
                <div>
                  <label class="label">Mã nhóm</label>
                  <input type="text" v-model="filterNhomNCKH.ma_nhom" class="input-field" />
                </div>
                <div>
                  <label class="label">Tên đề tài</label>
                  <input type="text" v-model="filterNhomNCKH.ten_de_tai" class="input-field" />
                </div>
                <div>
                  <label class="label">Giảng viên</label>
                  <input type="text" v-model="filterNhomNCKH.ten_gv" class="input-field" />
                </div>
                <div>
                  <label class="label">Trạng thái</label>
                  <select v-model="filterNhomNCKH.trang_thai" class="input-field">
                    <option value="">Tất cả</option>
                    <option value="0">Chưa duyệt</option>
                    <option value="1">Đã đăng ký</option>
                    <option value="2">Đã duyệt</option>
                  </select>
                </div>
              </div>
            </div>

            <div v-if="loadingNhomNCKH" style="color: #0082c6;">Đang tải danh sách nhóm...</div>
            <div v-else-if="filteredNhomNCKHList.length === 0" style="color: #888;">Không tìm thấy nhóm nào phù hợp.</div>
            <div v-else>
              <table class="nhom-nckh-table" style="width: 100%; border-collapse: collapse; background: #fff;">
                <thead>
                  <tr style="background: #0082c6; color: #fff;">
                    <th style="padding: 10px;">Mã nhóm</th>
                    <th style="padding: 10px;">Tên đề tài</th>
                    <th style="padding: 10px;">Giảng viên</th>
                    <th style="padding: 10px;">Trạng thái</th>
                    <th style="padding: 10px;">Thành viên</th>
                    <th style="padding: 10px;">Hành động</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="nhom in paginatedNhomNCKHList" :key="nhom.ma_nhom" style="border-bottom: 1px solid #e2e8f0;">
                    <td style="padding: 10px;">{{ nhom.ma_nhom }}</td>
                    <td style="padding: 10px;">{{ nhom.ten_de_tai }}</td>
                    <td style="padding: 10px;">{{ nhom.ten_gv }}</td>
                    <td style="padding: 10px;">{{ formatTrangThai(nhom.trang_thai) }}</td>
                    <td style="padding: 10px;">
                      <ul style="margin: 0; padding-left: 18px;">
                        <li v-for="tv in nhom.thanh_vien" :key="tv.ma_sv">
                          {{ tv.ma_sv }} - {{ tv.ten_sv }}
                        </li>
                      </ul>
                    </td>
                    <td style="padding: 10px; text-align:center;">
                      <button class="action-btn" style="margin-top:8px;" @click="openUpdateNhomForm(nhom)">Cập nhật</button>
                    </td>
                  </tr>
                </tbody>
              </table>
              <div class="pagination">
                <button @click="changePageNhomNCKH(currentPageNhomNCKH - 1)" :disabled="currentPageNhomNCKH === 1">Trang trước</button>
                <span>Trang {{ currentPageNhomNCKH }} / {{ totalPagesNhomNCKH }}</span>
                <button @click="changePageNhomNCKH(currentPageNhomNCKH + 1)" :disabled="currentPageNhomNCKH === totalPagesNhomNCKH">Trang sau</button>
              </div>
            </div>
          </div>
          <!-- Form cập nhật nhóm NCKH -->
          <div v-if="showUpdateNhomForm" class="update-nhom-modal">
            <div class="update-nhom-content big-modal">
              <h2 style="color:#0082c6; margin-bottom: 24px; font-size: 2rem; text-align:center;">Cập nhật nhóm NCKH</h2>
              <form @submit.prevent="handleUpdateNhom">
                <div class="form-group">
                  <label class="label" style="font-size:1.1rem;">Tên đề tài:</label>
                  <input v-model="updateNhomData.ten_de_tai" class="input-field big-input" required />
                </div>
                <div class="form-group">
                  <label class="label" style="font-size:1.1rem;">Giảng viên hướng dẫn:</label>
                  <input v-model="updateNhomData.ten_gv" class="input-field big-input" required />
                </div>
                <div class="form-group">
                  <label class="label" style="font-size:1.1rem;">Thành viên:</label>
                  <ul style="margin:0; padding-left:18px;">
                    <li v-for="(tv, idx) in updateNhomData.thanh_vien" :key="tv.ma_sv" style="margin-bottom:10px;">
                      <input v-model="updateNhomData.thanh_vien[idx].ten_sv" class="input-field big-input" style="width:60%; display:inline-block; margin-right:8px;" required />
                      <span style="color:#0082c6; font-weight:500;">({{ tv.ma_sv }})</span>
                    </li>
                  </ul>
                </div>
                <div style="display:flex; gap:16px; margin-top:24px; justify-content:center;">
                  <button type="submit" class="action-btn big-btn">Cập nhật</button>
                  <button type="button" class="action-btn big-btn" style="background:#ccc; color:#222;" @click="showUpdateNhomForm=false">Hủy</button>
                </div>
              </form>
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
import api from '@/config/api';
import SidebarManagerToNCKH from '@/components/SidebarManagerToNCKH.vue';
import Footer from '@/components/Footer.vue';

const router = useRouter();
const authStore = useAuthStore();
const { isAuthenticated, storedEmail, logout } = authStore;

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

// Trạng thái dữ liệu
const dangKyList = ref([]);
const giangVienList = ref([]);
const loading = ref(false);
const error = ref('');

// Thêm các state mới
const showFilter = ref(false);
const filterCriteria = ref({
  ma_sv: '',
  ten_sv: '',
  ma_gv: '',
  ma_hnc: ''
});

// Add new state for research directions
const huongNghienCuuList = ref([]);

// Add new state for selections
const selectedGV = ref(null);
const selectedSVs = ref([]);

// State cho nhóm NCKH
const showNhomNCKH = ref(false);
const nhomNCKHList = ref([]);
const loadingNhomNCKH = ref(false);

// Thêm state cho bộ lọc nhóm NCKH
const showFilterNhomNCKH = ref(false);
const filterNhomNCKH = ref({
  ma_nhom: '',
  ten_de_tai: '',
  ten_gv: '',
  trang_thai: ''
});

// State cho cập nhật nhóm NCKH
const showUpdateNhomForm = ref(false);
const updateNhomData = ref({});

// Thêm state cho phân trang
const currentPageDangKy = ref(1);
const currentPageNhomNCKH = ref(1);
const itemsPerPage = 20;

// Kiểm tra đăng nhập và lấy dữ liệu khi mount
onMounted(() => {
  window.addEventListener('resize', handleResize);
  handleResize();
  authStore.loadUserFromStorage();
  fetchGiangVienList();
  fetchDangKyList();
  fetchHuongNghienCuu();
});

onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
});

// Hàm đăng xuất
const handleLogout = () => {
  logout();
  router.push('/login');
};

// Lấy danh sách giảng viên
async function fetchGiangVienList() {
  try {
    const response = await api.get('/phongkhdn/gv/');
    const data = response.data;

    if (!Array.isArray(data)) {
      throw new Error('Dữ liệu giảng viên không hợp lệ');
    }

    giangVienList.value = data;
  } catch (err) {
    console.error('Lỗi khi lấy danh sách giảng viên:', err);
    giangVienList.value = [];
  }
}

// Ánh xạ ma_gv sang ten_gv
function getTenGiangVien(ma_gv) {
  const gv = giangVienList.value.find((g) => g.ma_gv === ma_gv);
  return gv ? gv.ten_gv : ma_gv || 'Không xác định';
}

// Lấy danh sách đăng ký từ API
async function fetchDangKyList() {
  try {
    loading.value = true;
    error.value = '';

    const response = await api.get('/tonckh/dang_ky/danh_sach');
    const data = response.data;

    if (!Array.isArray(data)) {
      throw new Error('Dữ liệu đăng ký không hợp lệ');
    }

    dangKyList.value = data.map((item) => ({
      ma_dk: item.ma_dk,
      ma_sv: item.ma_sv,
      ten_sv: item.ten_sv,
      trang_thai: item.trang_thai,
      list_nguyen_vong: (item.list_nguyen_vong || []).sort((a, b) => a.muc_uu_tien - b.muc_uu_tien),
      list_hnc: item.list_hnc || [],
    }));
  } catch (err) {
    let errorMessage = 'Không thể tải danh sách đăng ký';
    if (err.response) {
      console.error('Mã lỗi HTTP:', err.response.status);
      console.error('Chi tiết lỗi:', err.response.data);
      if (err.response.status === 401) {
        errorMessage = 'Phiên đăng nhập hết hạn';
        authStore.logout();
        router.push('/login');
      } else if (err.response.status === 403) {
        errorMessage = 'Bạn không có quyền truy cập danh sách đăng ký';
      } else if (err.response.status === 404) {
        errorMessage = 'Endpoint không tồn tại';
      } else if (err.response.status === 500) {
        errorMessage = '';
      }
    } else if (err.request) {
      errorMessage = 'Không thể kết nối đến server';
    }
    error.value = errorMessage;
    dangKyList.value = [];
    console.error('Lỗi khi lấy danh sách đăng ký:', err);
  } finally {
    loading.value = false;
  }
}

// Định dạng trạng thái
function formatTrangThai(trang_thai) {
  switch (trang_thai) {
    case 1:
      return 'Đã đăng ký';
    case 2:
      return 'Đã duyệt';
    case 0:
      return 'Chưa duyệt';
    default:
      return 'Không xác định';
  }
}

// Add new function for status class
const getStatusClass = (trang_thai) => {
  switch (trang_thai) {
    case 1:
      return 'status-registered';
    case 2:
      return 'status-approved';
    case 0:
      return 'status-pending';
    default:
      return '';
  }
};

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
const filteredDangKyList = computed(() => {
  return dangKyList.value.filter(item => {
    const maSvMatch = !filterCriteria.value.ma_sv || isSimilar(filterCriteria.value.ma_sv, item.ma_sv);
    const tenSvMatch = !filterCriteria.value.ten_sv || isSimilar(filterCriteria.value.ten_sv, item.ten_sv);
    const maGvMatch = !filterCriteria.value.ma_gv || 
      item.list_nguyen_vong.some(nv => isSimilar(filterCriteria.value.ma_gv, nv.ma_gv));
    const maHncMatch = !filterCriteria.value.ma_hnc || 
      item.list_hnc.some(hnc => hnc.ma_hnc === filterCriteria.value.ma_hnc);

    return maSvMatch && tenSvMatch && maGvMatch && maHncMatch;
  });
});

// Computed property cho phân trang danh sách đăng ký
const paginatedDangKyList = computed(() => {
  const start = (currentPageDangKy.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return filteredDangKyList.value.slice(start, end);
});

const totalPagesDangKy = computed(() => {
  return Math.ceil(filteredDangKyList.value.length / itemsPerPage);
});

// Chuẩn hóa chuỗi
function normalizeString(str) {
  return str
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/\s+/g, ' ')
    .trim();
}

// Kiểm tra tương đồng
function isSimilar(source, target, isExactField = false) {
  if (!source || !target) return true;

  const normalizedSource = normalizeString(source);
  const normalizedTarget = normalizeString(target);

  if (isExactField) {
    return normalizedTarget === normalizedSource || normalizedTarget.startsWith(normalizedSource);
  }

  if (normalizedTarget === normalizedSource) return true;
  if (normalizedTarget.includes(normalizedSource)) return true;

  const maxDistance = 2;
  const len1 = normalizedSource.length;
  const len2 = normalizedTarget.length;
  if (Math.abs(len1 - len2) > maxDistance) return false;

  let distance = 0;
  for (let i = 0; i < Math.min(len1, len2); i++) {
    if (normalizedSource[i] !== normalizedTarget[i]) distance++;
    if (distance > maxDistance) return false;
  }
  return true;
}

// Add new functions for selections
function handleSelectGV(ma_gv) {
  selectedGV.value = selectedGV.value === ma_gv ? null : ma_gv;
}
function handleSelectSV(ma_sv) {
  if (selectedSVs.value.includes(ma_sv)) {
    selectedSVs.value = selectedSVs.value.filter(id => id !== ma_sv);
  } else if (selectedSVs.value.length < 3) {
    selectedSVs.value.push(ma_sv);
  }
}
function isSVChecked(ma_sv) {
  return selectedSVs.value.includes(ma_sv);
}
function isGVChecked(ma_gv) {
  return selectedGV.value === ma_gv;
}

async function taoNhom() {
  if (!selectedGV.value || selectedSVs.value.length === 0) {
    alert('Vui lòng chọn 1 giảng viên và ít nhất 1 sinh viên!');
    return;
  }
   try {
    console.log('selectedGV.value', selectedGV.value);
    console.log('selectedSVs.value', selectedSVs.value);

    const payload = {
      dssv: selectedSVs.value,
      detai: null
    };

    await api.post(`gv/nhomnckh?ma_gv=${selectedGV.value}`, payload);

    alert('Tạo nhóm thành công!');
    selectedGV.value = null;
    selectedSVs.value = [];

  } catch (err) {
    let errorMessage = 'Không thể tạo nhóm';
    console.log('Chi tiết lỗi:', err);

    if (err.response) {
      console.error('Mã lỗi HTTP:', err.response.status);
      const status = err.response.status;

      if (status === 500) {
        errorMessage = 'Lỗi server nội bộ, vui lòng kiểm tra lại.';
      } else if (status === 422) {
        errorMessage =
          err.response.data.detail
            ?.map((e) => `${e.loc.join('.')}: ${e.msg}`)
            .join(', ') || 'Dữ liệu không hợp lệ.';
      } else if (status === 401) {
        errorMessage = 'Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.';
        authStore.logout();
        router.push('/login');
      } else if (status === 403) {
        errorMessage = 'Bạn không có quyền thực hiện hành động này.';
      } else if (status === 400) {
        errorMessage = err.response.data.detail || 'Sinh viên đã được tham gia nhóm khác';
      }
    } else {
      errorMessage = err.message || 'Lỗi không xác định.';
    }

    alert(errorMessage);
    console.error('Lỗi khi tạo nhóm:', err);
  }
}

function toggleShowNhomNCKH() {
  showNhomNCKH.value = !showNhomNCKH.value;
  if (showNhomNCKH.value && nhomNCKHList.value.length === 0) {
    fetchNhomNCKH();
  }
}

async function fetchNhomNCKH() {
  loadingNhomNCKH.value = true;
  try {
    const res = await api.get('gv/nhomnckh');
    nhomNCKHList.value = Array.isArray(res.data) ? res.data : [];
  } catch (err) {
    nhomNCKHList.value = [];
    console.error('Lỗi khi lấy danh sách nhóm NCKH:', err);
  } finally {
    loadingNhomNCKH.value = false;
  }
}

function openUpdateNhomForm(nhom) {
  updateNhomData.value = { ...nhom };
  showUpdateNhomForm.value = true;
}

async function handleUpdateNhom() {
  try {
    const ma_nhom = updateNhomData.value.ma_nhom;
    const payload = {
      ...updateNhomData.value
    };
    await api.put(`gv/nhomnckh/${ma_nhom}`, payload);
    alert('Cập nhật nhóm thành công!');
    showUpdateNhomForm.value = false;
    fetchNhomNCKH();
  } catch (err) {
    alert('Cập nhật nhóm thất bại!');
    console.error(err);
  }
}

// Computed property cho danh sách nhóm NCKH đã lọc và sắp xếp
const filteredNhomNCKHList = computed(() => {
  let filtered = nhomNCKHList.value.filter(nhom => {
    const maNhomMatch = !filterNhomNCKH.value.ma_nhom || 
      nhom.ma_nhom.toString().includes(filterNhomNCKH.value.ma_nhom);
    const tenDeTaiMatch = !filterNhomNCKH.value.ten_de_tai || 
      isSimilar(filterNhomNCKH.value.ten_de_tai, nhom.ten_de_tai);
    const tenGVMatch = !filterNhomNCKH.value.ten_gv || 
      isSimilar(filterNhomNCKH.value.ten_gv, nhom.ten_gv);
    const trangThaiMatch = !filterNhomNCKH.value.trang_thai || 
      nhom.trang_thai.toString() === filterNhomNCKH.value.trang_thai;

    return maNhomMatch && tenDeTaiMatch && tenGVMatch && trangThaiMatch;
  });

  // Sắp xếp theo mã nhóm từ lớn đến nhỏ
  return filtered.sort((a, b) => b.ma_nhom - a.ma_nhom);
});

// Thêm hàm toggle bộ lọc nhóm NCKH
const toggleFilterNhomNCKH = () => {
  showFilterNhomNCKH.value = !showFilterNhomNCKH.value;
};

// Computed property cho phân trang danh sách nhóm NCKH
const paginatedNhomNCKHList = computed(() => {
  const start = (currentPageNhomNCKH.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return filteredNhomNCKHList.value.slice(start, end);
});

const totalPagesNhomNCKH = computed(() => {
  return Math.ceil(filteredNhomNCKHList.value.length / itemsPerPage);
});

// Hàm chuyển trang
const changePageDangKy = (page) => {
  currentPageDangKy.value = page;
};

const changePageNhomNCKH = (page) => {
  currentPageNhomNCKH.value = page;
};
</script>

<style scoped>
/* Container */
.container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  overflow-y: auto;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
}

.container::-webkit-scrollbar {
  width: 6px;
}

.container::-webkit-scrollbar-track {
  background: #e2e8f0;
  border-radius: 10px;
}

.container::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, #0082c6, #0069a3);
  border-radius: 10px;
}

.container::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, #0069a3, #005a8c);
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

/* Content */
.content {
  background-color: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 30px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  border: 1px solid rgba(226, 232, 240, 0.8);
}

.content:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.content h2 {
  font-size: 1.5rem;
  background: linear-gradient(135deg, #0082c6, #0069a3);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 1.5rem;
  font-weight: 700;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  letter-spacing: 0.5px;
}

/* Status Messages */
.loading-text {
  color: #4b5563;
  font-size: 1.1rem;
  text-align: center;
  padding: 20px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 8px;
  backdrop-filter: blur(5px);
}

.error-text {
  color: #ef4444;
  font-size: 1.1rem;
  text-align: center;
  padding: 20px;
  background: rgba(254, 226, 226, 0.8);
  border-radius: 8px;
  margin: 10px 0;
  backdrop-filter: blur(5px);
  border: 1px solid rgba(239, 68, 68, 0.2);
}

/* Table */
.table-container {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow-x: auto;
  width: 100%;
  margin-top: 20px;
  border: 1px solid #e2e8f0;
}

.table-container::-webkit-scrollbar {
  height: 8px;
}

.table-container::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 10px;
}

.table-container::-webkit-scrollbar-thumb {
  background: #0082c6;
  border-radius: 10px;
}

.table-container::-webkit-scrollbar-thumb:hover {
  background: #0069a3;
}

.dangky-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
  min-width: 1200px;
}

.dangky-table th,
.dangky-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #d1dbe3;
}

.dangky-table th {
  background: #0082c6;
  color: white;
  font-weight: 600;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  position: sticky;
  top: 0;
  z-index: 1;
  white-space: nowrap;
}

.dangky-table th:first-child {
  border-top-left-radius: 12px;
}

.dangky-table th:last-child {
  border-top-right-radius: 12px;
}

.dangky-table td {
  background: white;
  font-size: 14px;
  color: #4b5563;
}

.dangky-table tr:hover {
  background: #f9fafb;
}

.dangky-table ul {
  margin: 0;
  padding-left: 20px;
  list-style-type: none;
}

.dangky-table ul li {
  font-size: 14px;
  margin-bottom: 8px;
  color: #4b5563;
  transition: all 0.3s ease;
  position: relative;
  padding-left: 15px;
}

.dangky-table ul li:before {
  content: "•";
  color: #0082c6;
  position: absolute;
  left: 0;
  font-size: 16px;
}

.dangky-table ul li:hover {
  color: #0082c6;
  transform: translateX(5px);
}

.dangky-table ul li:last-child {
  margin-bottom: 0;
}

/* Action Buttons */
.action-btn {
  background-color: #0082c6;
  color: white;
  padding: 8px 16px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(220, 38, 38, 0.2);
}

.action-btn:hover {
  background-color: #b91c1c;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(220, 38, 38, 0.3);
}

.action-btn:active {
  transform: translateY(0);
  box-shadow: 0 1px 2px rgba(220, 38, 38, 0.2);
}

.action-btn i {
  font-size: 14px;
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

  .dangky-table {
    min-width: 1000px;
  }
  
  .dangky-table th,
  .dangky-table td {
    padding: 12px;
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

.card-number {
  font-weight: 600;
  color: #0082c6;
}

.card-status {
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
}

.status-registered {
  background: #e0f2fe;
  color: #0369a1;
}

.status-approved {
  background: #dcfce7;
  color: #166534;
}

.status-pending {
  background: #fef9c3;
  color: #854d0e;
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

/* User Email */
.user-email {
  max-width: 150px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Content Header */
.content-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  gap: 10px;
}

.header-left {
  margin-right: 10px;
}

.content-header h2 {
  margin: 0;
  flex-grow: 1;
}

/* Filter Button */
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
}

.filter-btn:hover {
  background: #0069a3;
}

/* Filter form */
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

.filter-row input.input-field {
  width: 100%;
  padding: 8px;
  border: 1px solid #d1dbe3;
  border-radius: 6px;
  font-size: 14px;
  background-color: #f9fafb;
  transition: border-color 0.3s, box-shadow 0.3s, background-color 0.3s;
}

.filter-row input.input-field:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2);
  background-color: white;
  outline: none;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .content-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }

  .header-left {
    margin-right: 0;
    margin-bottom: 10px;
  }

  .content-header h2 {
    font-size: 1.2rem;
  }

  .filter-form {
    padding: 10px;
  }

  .filter-row {
    flex-direction: column;
    gap: 10px;
  }
}

/* Filter Section */
.filter-section {
  margin: 10px 0 20px 0;
}

.filter-btn {
  background: #0082c6;
  color: white;
  border: none;
  padding: 8px 20px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.filter-btn:hover {
  background: #0069a3;
  transform: translateY(-1px);
}

/* Filter Form */
.filter-form {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.filter-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.filter-row > div {
  display: flex;
  flex-direction: column;
}

.label {
  font-size: 0.9rem;
  color: #4b5563;
  margin-bottom: 8px;
  font-weight: 500;
}

.input-field {
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.input-field:focus {
  border-color: #0082c6;
  box-shadow: 0 0 0 2px rgba(0, 130, 198, 0.1);
  outline: none;
}

select.input-field {
  background-color: white;
  cursor: pointer;
}

@media (max-width: 768px) {
  .filter-row {
    grid-template-columns: 1fr;
    gap: 15px;
  }
}

/* Bảng nhóm NCKH */
.nhom-nckh-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  margin-bottom: 10px;
  margin-top: 10px;
  padding: 10px;
}
.nhom-nckh-table th {
  background: #0082c6;
  color: #fff;
  font-weight: 600;
  font-size: 15px;
  padding: 12px 10px;
  text-align: left;
  border: none;
}
.nhom-nckh-table th:first-child {
  border-top-left-radius: 12px;
}
.nhom-nckh-table th:last-child {
  border-top-right-radius: 12px;
}
.nhom-nckh-table td {
  padding: 12px 10px;
  font-size: 14px;
  color: #334155;
  background: #fff;
  border-bottom: 1px solid #e2e8f0;
  vertical-align: top;
}
.nhom-nckh-table tr:last-child td {
  border-bottom: none;
}
.nhom-nckh-table tr:hover td {
  background: #f1f5f9;
}
.nhom-nckh-table ul {
  margin: 0;
  padding-left: 18px;
  list-style-type: disc;
}
.nhom-nckh-table ul li {
  font-size: 14px;
  color: #0082c6;
  margin-bottom: 4px;
  padding-left: 0;
}
.nhom-nckh-table ul li:last-child {
  margin-bottom: 0;
}

/* Modal cập nhật nhóm NCKH */
.update-nhom-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0,0,0,0.25);
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
}
.update-nhom-content {
  background: #fff;
  border-radius: 12px;
  padding: 28px 32px 20px 32px;
  min-width: 340px;
  max-width: 95vw;
  box-shadow: 0 4px 24px rgba(0,0,0,0.13);
}

.big-modal {
  min-width: 480px;
  max-width: 700px;
  padding: 40px 48px 32px 48px;
}

.big-input {
  font-size: 1.1rem;
  padding: 14px 16px;
  width: 100%;
  margin-bottom: 8px;
}

.big-btn {
  font-size: 1.1rem;
  padding: 12px 32px;
  border-radius: 8px;
}

/* Phân trang */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-top: 20px;
  padding: 10px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.pagination button {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  background: #0082c6;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 14px;
}

.pagination button:hover:not(:disabled) {
  background: #0069a3;
  transform: translateY(-1px);
}

.pagination button:disabled {
  background: #ccc;
  cursor: not-allowed;
  transform: none;
}

.pagination span {
  color: #4b5563;
  font-size: 14px;
  font-weight: 500;
}

@media (max-width: 768px) {
  .pagination {
    flex-direction: column;
    gap: 8px;
  }
  
  .pagination button {
    width: 100%;
  }
}
</style>