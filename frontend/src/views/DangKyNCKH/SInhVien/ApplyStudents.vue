<template>
  <div class="container">
    <!-- Header -->
    <header class="header">
      <button v-if="isMobile" class="sidebar-toggle" @click="toggleSidebar">☰</button>
      <img src="@/assets/img/logo-hou.png" alt="Logo" class="logo" />
      <h1>THAM GIA ĐĂNG KÝ NGHIÊN CỨU KHOA HỌC SINH VIÊN</h1>
    </header>

    <!-- Overlay khi sidebar mở trên mobile -->
    <div v-if="isSidebarOpen && isMobile" class="overlay" @click="toggleSidebar"></div>

    <!-- Main layout -->
    <div class="main-layout">
      <!-- Sidebar -->
      <SidebarHome
        class="sidebar"
        :class="{ 'sidebar-open': isSidebarOpen }"
        :is-open="isSidebarOpen"
        @toggle="toggleSidebar"
      />

      <!-- Nội dung chính -->
      <div class="main-content" :class="{ 'main-content-shifted': isSidebarOpen && !isMobile }">
        <div class="content">
          <p>Đăng ký nghiên cứu khoa học sinh viên đợt …</p>
          <p>Mỗi sinh viên chỉ được chọn tối đa 2 giảng viên từ tất cả các hướng nghiên cứu.</p>
          <p>Nếu chỉ chọn hướng nghiên cứu thì có thể chọn tất cả</p>
          <!-- Thông báo trạng thái -->
          <p v-if="loading" class="loading-text">Đang tải dữ liệu...</p>
          <p v-else-if="error" class="error-text">{{ error }}</p>

          <!-- Khu vực hướng nghiên cứu -->
          <div v-if="!loading && !error" class="huong-container">
            <!-- Cột 1 -->
            <div class="huong-column">
              <div
                v-for="(huong, index) in leftColumnHuong"
                :key="huong.ma_hnc"
                class="huong-item"
                :class="{ active: huong.open || huong.checked }"
              >
                <!-- Tiêu đề hướng nghiên cứu -->
                <div class="huong-header" @click="toggleHuong(huong)">
                  <label class="huong-label">
                    <input
                      type="checkbox"
                      v-model="huong.checked"
                      @change="handleHuongChange"
                    />
                    {{ huong.ten_hnc }}
                  </label>
                  <span class="toggle-icon"></span>
                </div>

                <!-- Dropdown danh sách giảng viên -->
                <transition name="fade">
                  <div v-if="huong.open" class="dropdown-teachers">
                    <!-- Thông báo trạng thái khi tải giảng viên -->
                    <p v-if="huong.loadingTeachers" class="loading-text">Đang tải giảng viên...</p>
                    <p v-else-if="huong.errorTeachers" class="error-text">{{ huong.errorTeachers }}</p>
                    <template v-else>
                      <p class="teacher-list-title">Danh sách giảng viên:</p>
                      <label
                        v-for="teacher in huong.teachers"
                        :key="teacher.ma_gv"
                        class="teacher-label"
                      >
                        <div class="teacher-info-container">
                          <div class="teacher-checkbox">
                            <input
                              type="checkbox"
                              :disabled="!teacher.checked && selectedTeachersCount >= 2"
                              v-model="teacher.checked"
                              @change="handleTeacherChange"
                            />
                            {{ teacher.ten_gv }}
                          </div>
                          <button 
                            class="view-info-btn"
                            @click.stop="viewTeacherInfo(teacher.ma_gv)"
                          >
                            Xem thông tin
                          </button>
                        </div>
                      </label>
                      <p v-if="huong.teachers.length === 0" class="no-data-text">
                        Không có giảng viên nào thuộc hướng nghiên cứu này.
                      </p>
                    </template>
                  </div>
                </transition>
              </div>
            </div>

            <!-- Cột 2 -->
            <div class="huong-column">
              <div
                v-for="(huong, index) in rightColumnHuong"
                :key="huong.ma_hnc"
                class="huong-item"
                :class="{ active: huong.open || huong.checked }"
              >
                <!-- Tiêu đề hướng nghiên cứu -->
                <div class="huong-header" @click="toggleHuong(huong)">
                  <label class="huong-label">
                    <input
                      type="checkbox"
                      v-model="huong.checked"
                      @change="handleHuongChange"
                    />
                    {{ huong.ten_hnc }}
                  </label>
                  <span class="toggle-icon"></span>
                </div>

                <!-- Dropdown danh sách giảng viên -->
                <transition name="fade">
                  <div v-if="huong.open" class="dropdown-teachers">
                    <!-- Thông báo trạng thái khi tải giảng viên -->
                    <p v-if="huong.loadingTeachers" class="loading-text">Đang tải giảng viên...</p>
                    <p v-else-if="huong.errorTeachers" class="error-text">{{ huong.errorTeachers }}</p>
                    <template v-else>
                      <p class="teacher-list-title">Danh sách giảng viên:</p>
                      <label
                        v-for="teacher in huong.teachers"
                        :key="teacher.ma_gv"
                        class="teacher-label"
                      >
                        <div class="teacher-info-container">
                          <div class="teacher-checkbox">
                            <input
                              type="checkbox"
                              :disabled="!teacher.checked && selectedTeachersCount >= 2"
                              v-model="teacher.checked"
                              @change="handleTeacherChange"
                            />
                            {{ teacher.ten_gv }}
                          </div>
                          <button 
                            class="view-info-btn"
                            @click.stop="viewTeacherInfo(teacher.ma_gv)"
                          >
                            Xem thông tin
                          </button>
                        </div>
                      </label>
                      <p v-if="huong.teachers.length === 0" class="no-data-text">
                        Không có giảng viên nào thuộc hướng nghiên cứu này.
                      </p>
                    </template>
                  </div>
                </transition>
              </div>
            </div>
          </div>

          <!-- Thông báo lỗi nếu chọn quá 2 giảng viên -->
          <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>
          <button
            class="action-btn"
            @click="submitRegistration"
            :disabled="loading || (selectedTeachersCount === 0 && selectedHuongCount === 0)"
          >
            Đăng ký
          </button>
        </div>

        <!-- Phần hiển thị nguyện vọng đã đăng ký -->
        <div class="preferences-toggle-btns" style="display: flex; gap: 10px; margin-bottom: 20px;">
          <button class="action-btn" :class="{active: showPreferences}" @click="showPreferences = true">Nguyện vọng đã đăng ký</button>
          <button class="action-btn" :class="{active: !showPreferences}" @click="showPreferences = false">Danh sách tổ đăng ký</button>
        </div>

        <!-- Danh sách tổ đăng ký NCKH -->
        <div v-if="!showPreferences" class="preferences-section">
          <h2>Danh sách tham gia NCKH được tổ đăng ký</h2>
          <p v-if="loadingNhomNCKH" class="loading-text">Đang tải danh sách...</p>
          <p v-else-if="errorNhomNCKH" class="error-text">{{ errorNhomNCKH }}</p>
          <div v-else class="preferences-list">
            <table class="topic-table">
              <thead>
                <tr>
                  <th>STT</th>
                  <th>Giảng viên</th>
                  <th>Thành viên</th>
                  <th>Đợt thực hiện</th>
                  <th>Trạng thái</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(nhom, idx) in nhomNCKHList.filter(n => n.trang_thai === 1 && !n.ten_de_tai && n.thanh_vien.some(tv => tv.ma_sv === ma_sv_hientai))" :key="'to-' + nhom.ma_nhom">
                  <td>{{ idx + 1 }}</td>
                  <td>
                    {{ nhom.ten_gv }}
                    <button v-if="nhom.ma_gv" class="view-info-btn" @click="viewTeacherInfo(nhom.ma_gv)">Xem chi tiết</button>
                  </td>
                  <td>
                    <ul>
                      <li v-for="sv in nhom.thanh_vien" :key="sv.ma_sv">
                        {{ sv.ma_sv }} - {{ sv.ten_sv }}
                      </li>
                      <li v-if="!nhom.thanh_vien?.length">Không có</li>
                    </ul>
                  </td>
                  <td>{{ nhom.dot_thuc_hien || 'N/A' }}</td>
                  <td>{{ getStatusText(nhom.trang_thai) }}</td>
                </tr>
                <tr v-if="nhomNCKHList.filter(n => n.trang_thai === 1 && !n.ten_de_tai && n.thanh_vien.some(tv => tv.ma_sv === ma_sv_hientai)).length === 0">
                  <td colspan="5">Không có tổ nào đăng ký NCKH đang chờ duyệt</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Nguyện vọng đã đăng ký -->
        <div v-if="showPreferences" class="content preferences-section">
          <h2>Nguyện vọng đã đăng ký</h2>
          <p v-if="loadingPreferences" class="loading-text">Đang tải danh sách nguyện vọng...</p>
          <p v-else-if="errorPreferences" class="error-text">{{ errorPreferences }}</p>
          <p v-else-if="registeredPreferences.length === 0" class="no-data-text">
            Bạn chưa có nguyện vọng đăng ký nào.
          </p>
          <div v-else class="preferences-list">
            <div v-for="pref in sortedPreferences" :key="pref.ma_dk" class="preference-item">
              <div class="preference-header">
                <div class="preference-info">
                  <h3>Nguyện vọng #{{ pref.ma_dk }}</h3>
                  <p class="student-info">Sinh viên: {{ pref.ten_sv }} ({{ pref.ma_sv }})</p>
                </div>
              </div>
              <div class="preference-content">
                <div class="preference-section">
                  <h4>Giảng viên hướng dẫn:</h4>
                  <ul>
                    <li v-for="nv in pref.list_nguyen_vong" :key="nv.ma_gv">
                      {{ getTeacherName(nv.ma_gv) }} (Ưu tiên: {{ nv.muc_uu_tien }})
                      <span class="status-badge" :class="getStatusClass(nv.trang_thai)">
                        {{ getStatusText(nv.trang_thai) }}
                      </span>
                      <button class="view-info-btn" @click="viewTeacherInfo(nv.ma_gv)">
                        Xem thông tin
                      </button>
                    </li>
                  </ul>
                </div>
                <div class="preference-section">
                  <h4>Hướng nghiên cứu:</h4>
                  <ul>
                    <li v-for="hnc in pref.list_hnc" :key="hnc.ma_hnc">
                      {{ hnc.ten_hnc }}
                    </li>
                  </ul>
                </div>
              </div>
              <div class="preference-footer">
                <span class="status-badge" :class="getStatusClass(pref.trang_thai)">
                  {{ getStatusText(pref.trang_thai) }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer 
       <footer class="footer">
      <Footer class="footer-content" />
    </footer> -->
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useTeacherViewStore } from '@/stores/teacherView';
import SidebarHome from '@/components/SidebarHome.vue';
import Footer from '@/components/Footer.vue';
import api from '@/config/api';
import { useRouter } from 'vue-router';

// Trạng thái sidebar
const isSidebarOpen = ref(false);
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
const huongNghienCuuList = ref([]);
const loading = ref(false);
const error = ref('');
const errorMessage = ref('');
const authStore = useAuthStore();
const teacherViewStore = useTeacherViewStore();
const router = useRouter();

// Thêm state cho nguyện vọng đã đăng ký
const registeredPreferences = ref([]);
const loadingPreferences = ref(false);
const errorPreferences = ref('');

// Thêm computed property để sắp xếp nguyện vọng
const sortedPreferences = computed(() => {
  return [...registeredPreferences.value].map(pref => ({
    ...pref,
    list_nguyen_vong: [...pref.list_nguyen_vong].sort((a, b) => a.muc_uu_tien - b.muc_uu_tien)
  })).sort((a, b) => {
    // Lấy mức ưu tiên cao nhất của mỗi nguyện vọng
    const priorityA = Math.min(...a.list_nguyen_vong.map(nv => nv.muc_uu_tien));
    const priorityB = Math.min(...b.list_nguyen_vong.map(nv => nv.muc_uu_tien));
    return priorityA - priorityB;
  });
});

// Toggle hiển thị bảng nguyện vọng hoặc tổ đăng ký
const showPreferences = ref(true);

// State cho danh sách nhóm NCKH
const nhomNCKHList = ref([]);
const loadingNhomNCKH = ref(false);
const errorNhomNCKH = ref('');

// Lấy danh sách nhóm NCKH từ API
async function fetchNhomNCKH() {
  loadingNhomNCKH.value = true;
  errorNhomNCKH.value = '';
  try {
    const res = await api.get('gv/nhomnckh');
    nhomNCKHList.value = Array.isArray(res.data) ? res.data : [];
  } catch (err) {
    errorNhomNCKH.value = 'Không thể tải danh sách tổ đăng ký';
    nhomNCKHList.value = [];
    console.error('Lỗi khi lấy danh sách nhóm NCKH:', err);
  } finally {
    loadingNhomNCKH.value = false;
  }
}

// Lấy mã sinh viên hiện tại
const ma_sv_hientai = computed(() => authStore.user?.email?.split('@')[0] || '');

// Khi chuyển tab sang tổ đăng ký thì fetch nhóm NCKH
watch(
  () => showPreferences.value,
  (val) => {
    if (!val) fetchNhomNCKH();
  }
);

// Lấy dữ liệu từ API khi component được mount
onMounted(() => {
  authStore.loadUserFromStorage();
  fetchHuongNghienCuu().then(() => {
    // Sau khi lấy danh sách hướng nghiên cứu, tải danh sách giảng viên cho tất cả các hướng
    huongNghienCuuList.value.forEach(huong => {
      fetchTeachersForHuong(huong);
    });
  });
  fetchRegisteredPreferences();
});

// Tính tổng số giảng viên đã chọn
const selectedTeachersCount = computed(() => {
  return huongNghienCuuList.value.reduce((total, huong) => {
    return total + huong.teachers.filter((t) => t.checked).length;
  }, 0);
});

// Tính tổng số hướng nghiên cứu đã chọn
const selectedHuongCount = computed(() => {
  return huongNghienCuuList.value.filter((h) => h.checked).length;
});

// Tính toán danh sách cho 2 cột
const leftColumnHuong = computed(() => {
  return huongNghienCuuList.value.filter((_, index) => index % 2 === 0);
});

const rightColumnHuong = computed(() => {
  return huongNghienCuuList.value.filter((_, index) => index % 2 === 1);
});

// Lấy danh sách hướng nghiên cứu từ API
async function fetchHuongNghienCuu() {
  try {
    loading.value = true;
    error.value = '';

    const response = await api.get('get_data/hnc/');
    const data = response.data;

    if (!Array.isArray(data)) {
      console.error('Dữ liệu trả về không phải mảng:', data);
      throw new Error('Dữ liệu hướng nghiên cứu không hợp lệ');
    }

    huongNghienCuuList.value = data.map((huong) => {
      if (!huong || typeof huong !== 'object') {
        console.warn('Phần tử dữ liệu không hợp lệ:', huong);
        return {
          ma_hnc: '',
          ten_hnc: 'Không xác định',
          checked: false,
          open: false,
          teachers: [],
          loadingTeachers: false,
          errorTeachers: '',
          teachersFetched: false,
        };
      }

      return {
        ma_hnc: huong.ma_hnc || '',
        ten_hnc: huong.ten_hnc || 'Không xác định',
        checked: false,
        open: false,
        teachers: [],
        loadingTeachers: false,
        errorTeachers: '',
        teachersFetched: false,
      };
    });
  } catch (err) {
    let errorMsg = 'Không thể tải danh sách hướng nghiên cứu';
    if (err.response) {
      console.error('Mã lỗi HTTP:', err.response.status);
      console.error('Chi tiết lỗi:', err.response.data);
      if (err.response.status === 401) {
        errorMsg = 'Phiên đăng nhập hết hạn';
      } else if (err.response.status === 403) {
        errorMsg = 'Bạn không có quyền truy cập danh sách hướng nghiên cứu';
      } else if (err.response.status === 404) {
        errorMsg = 'Endpoint không tồn tại';
      } else if (err.response.status === 500) {
        errorMsg = 'Lỗi server, vui lòng thử lại sau';
      }
    } else if (err.request) {
      errorMsg = 'Không thể kết nối đến server';
    } else {
      errorMsg = err.message;
    }
    error.value = errorMsg;
    huongNghienCuuList.value = [];
    console.error('Lỗi khi lấy hướng nghiên cứu:', err);
  } finally {
    loading.value = false;
  }
}

// Lấy danh sách giảng viên thuộc hướng nghiên cứu
async function fetchTeachersForHuong(huong) {
  if (huong.teachersFetched) return;
  if (!huong.ma_hnc) {
    huong.errorTeachers = 'Mã hướng nghiên cứu không hợp lệ';
    huong.teachers = [];
    return;
  }

  try {
    huong.loadingTeachers = true;
    huong.errorTeachers = '';
    console.log('Gọi API lấy giảng viên cho ma_hnc:', huong.ma_hnc);

    const response = await api.get(`get_data/gv_by_hnc/${huong.ma_hnc}/`);
    const data = response.data;

    if (!Array.isArray(data)) {
      console.error('Dữ liệu giảng viên trả về không phải mảng:', data);
      throw new Error('Dữ liệu giảng viên không hợp lệ');
    }

    huong.teachers = data.map((gv) => ({
      ma_gv: gv.ma_gv || '',
      ten_gv: gv.ten_gv || 'Không xác định',
      checked: false,
    }));
    huong.teachersFetched = true;
  } catch (err) {
    let errorMsg = 'Không thể tải danh sách giảng viên';
    if (err.response) {
      console.error('Mã lỗi HTTP:', err.response.status);
      console.error('Chi tiết lỗi:', err.response.data);
      if (err.response.status === 401) {
        errorMsg = 'Phiên đăng nhập hết hạn';
      } else if (err.response.status === 403) {
        errorMsg = 'Bạn không có quyền truy cập danh sách giảng viên';
      } else if (err.response.status === 404) {
        errorMsg = 'Hướng nghiên cứu không tồn tại';
      } else if (err.response.status === 500) {
        errorMsg = 'Lỗi server, vui lòng thử lại sau';
      }
    } else if (err.request) {
      errorMsg = 'Không thể kết nối đến server';
    } else {
      errorMsg = err.message;
    }
    huong.errorTeachers = errorMsg;
    huong.teachers = [];
    console.error('Lỗi khi lấy danh sách giảng viên:', err);
  } finally {
    huong.loadingTeachers = false;
  }
}

// Toggle hiển thị danh sách giảng viên của hướng
async function toggleHuong(huong) {
  huong.open = !huong.open; // Chỉ toggle trạng thái của HNC được click
  if (huong.open) {
    await fetchTeachersForHuong(huong); // Chỉ gọi API khi mở
  }
}

// Xử lý khi thay đổi checkbox hướng nghiên cứu
function handleHuongChange() {
  if (!isEditing.value) {
    errorMessage.value = selectedTeachersCount.value > 2
      ? 'Bạn chỉ được chọn tối đa 2 giảng viên.'
      : '';
  }
}

// Xử lý khi thay đổi checkbox giảng viên
function handleTeacherChange() {
  if (!isEditing.value) {
    errorMessage.value = selectedTeachersCount.value > 2
      ? 'Bạn chỉ được chọn tối đa 2 giảng viên.'
      : '';
  }
}

// Gửi đăng ký
async function submitRegistration() {
  if (selectedTeachersCount.value === 0 && selectedHuongCount.value === 0) {
    errorMessage.value = 'Vui lòng chọn ít nhất một hướng nghiên cứu hoặc giảng viên.';
    return;
  }
  if (selectedTeachersCount.value > 2) {
    errorMessage.value = 'Bạn chỉ được chọn tối đa 2 giảng viên.';
    return;
  }

  const selectedTeachers = huongNghienCuuList.value
    .flatMap((huong) => huong.teachers)
    .filter((t) => t.checked)
    .map((t, index) => ({
      ma_gv: t.ma_gv,
      muc_uu_tien: index + 1, // Ưu tiên 1 cho giảng viên đầu, 2 cho giảng viên thứ hai
      trang_thai: 1,
    }));

  const selectedHuong = huongNghienCuuList.value
    .filter((h) => h.checked)
    .map((h) => h.ma_hnc);

  const payload = {
    dang_ky: {
      ma_sv: authStore.user?.email?.split('@')[0] || '', // Giả định ma_sv từ email
      trang_thai: 1,
    },
    list_nguyen_vong: selectedTeachers,
    list_hnc: selectedHuong,
  };

  console.log('Payload đăng ký:', payload);

  try {
    await api.post('sv/dangky/them', payload);
    alert('Đăng ký thành công!');
    
    // Reset form
    huongNghienCuuList.value.forEach((huong) => {
      huong.checked = false;
      huong.teachers.forEach((teacher) => {
        teacher.checked = false;
      });
      huong.open = false;
    });
    errorMessage.value = '';

    // Reload data
    await Promise.all([
      fetchHuongNghienCuu(),
      fetchRegisteredPreferences()
    ]);

    // Sau khi lấy danh sách hướng nghiên cứu, tải danh sách giảng viên cho tất cả các hướng
    huongNghienCuuList.value.forEach(huong => {
      fetchTeachersForHuong(huong);
    });

  } catch (err) {
    let errorMsg = 'Đăng ký thất bại';
    if (err.response) {
      console.error('Mã lỗi HTTP:', err.response.status);
      console.error('Chi tiết lỗi:', err.response.data);
      if (err.response.status === 401) {
        errorMsg = 'Phiên đăng nhập hết hạn';
        authStore.logout();
      } else if (err.response.status === 403) {
        errorMsg = 'Bạn không có quyền đăng ký';
      } else if (err.response.status === 400) {
        errorMsg = err.response.data.detail || 'Dữ liệu không hợp lệ';
      } else if (err.response.status === 500) {
        errorMsg = 'Lỗi server, vui lòng thử lại sau';
      }
    } else if (err.request) {
      errorMsg = 'Không thể kết nối đến server';
    }
    errorMessage.value = errorMsg;
    console.error('Lỗi khi đăng ký:', err);
  }
}

// Thêm method lấy nguyện vọng đã đăng ký
async function fetchRegisteredPreferences() {
  try {
    loadingPreferences.value = true;
    errorPreferences.value = '';
    const ma_sv = authStore.user?.email?.split('@')[0] || '';
    
    // Lấy danh sách đăng ký đầy đủ
    const response = await api.get('tonckh/dang_ky/danh_sach');
    const allRegistrations = response.data;
    
    // Lọc ra những đăng ký của sinh viên hiện tại
    registeredPreferences.value = allRegistrations.filter(reg => reg.ma_sv === ma_sv);
    
    if (registeredPreferences.value.length === 0) {
      errorPreferences.value = 'Bạn chưa có nguyện vọng đăng ký nào.';
    }
  } catch (err) {
    let errorMsg = 'Không thể tải danh sách nguyện vọng đã đăng ký';
    if (err.response) {
      if (err.response.status === 401) {
        errorMsg = 'Phiên đăng nhập hết hạn';
      } else if (err.response.status === 403) {
        errorMsg = 'Bạn không có quyền truy cập';
      } else if (err.response.status === 404) {
        errorMsg = 'Không tìm thấy thông tin đăng ký';
      }
    }
    errorPreferences.value = errorMsg;
    console.error('Lỗi khi lấy nguyện vọng đã đăng ký:', err);
  } finally {
    loadingPreferences.value = false;
  }
}

// Helper functions for status badges
function getStatusClass(trang_thai) {
  switch (trang_thai) {
    case 1:
      return 'status-approved';
    case 2:
      return 'status-pending';
    case 3:
      return 'status-rejected';
    default:
      return '';
  }
}

function getStatusText(trang_thai) {
  switch (trang_thai) {
    case 1:
      return 'Chờ duyệt';
    case 2:
      return 'Đã duyệt';
    case 3:
      return 'Đã từ chối';
    default:
      return '';
  }
}

// Hàm lấy tên giảng viên từ mã giảng viên
function getTeacherName(ma_gv) {
  // Tìm trong tất cả các hướng nghiên cứu
  for (const huong of huongNghienCuuList.value) {
    // Tìm trong danh sách giảng viên của mỗi hướng
    const teacher = huong.teachers.find(t => t.ma_gv === ma_gv);
    if (teacher) {
      return teacher.ten_gv;
    }
  }
  return ma_gv; // Trả về mã giảng viên nếu không tìm thấy tên
}

const viewTeacherInfo = (ma_gv) => {
  // Lưu ma_gv vào store trước khi chuyển trang
  teacherViewStore.setCurrentTeacherId(ma_gv);
  
  router.push({
    path: '/info',
    query: {
      ma_gv: ma_gv,
      viewOnly: 'true'
    }
  });
};
</script>

<style scoped>
/* Container */
.container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  overflow-y: auto;
  background-color: #f8fafc;
}

.container::-webkit-scrollbar {
  width: 6px;
}

.container::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 10px;
}

.container::-webkit-scrollbar-thumb {
  background: #0082c6;
  border-radius: 10px;
}

.container::-webkit-scrollbar-thumb:hover {
  background: #0069a3;
}

/* Overlay cho mobile */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(5px);
  z-index: 999;
}

/* Header */
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(135deg, #0082c6 0%, #0069a3 100%);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 80px;
  z-index: 1000;
  padding: 10px 20px 10px 70px;
  box-sizing: border-box;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.logo {
  width: 50px;
  margin-right: 2rem;
  margin-top: 2rem;
}

.header h1 {
  font-size: 1.3rem;
  margin: 0;
  flex-grow: 1;
  text-align: center;
  color: white;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.sidebar-toggle {
  display: none;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: none;
  padding: 8px 12px;
  font-size: 1.2rem;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.sidebar-toggle:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-1px);
}

/* Main layout */
.main-layout {
  display: flex;
  margin-top: 20px;
  min-height: calc(100vh - 100px);
  gap: 20px;
}

/* Sidebar */
.sidebar {
  width: 220px;
  background: linear-gradient(180deg, #0082c6 0%, #0069a3 100%);
  position: fixed;
  top: 80px;
  left: 0;
  height: calc(100vh - 100px);
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  z-index: 999;
}

/* Main Content */
.main-content {
  flex: 1;
  padding: 20px;
  box-sizing: border-box;
  background: #f8fafc;
  transition: margin-left 0.3s ease;
  margin-left: 240px;
  width: calc(100% - 240px);
  margin-top: 20px;
}

.main-content-shifted {
  margin-left: 240px;
}

/* Content */
.content {
  background-color: white;
  border-radius: 12px;
  padding: 25px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.content:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
}

/* Status Messages */
.loading-text {
  color: #4b5563;
  font-size: 1.1rem;
  font-weight: 500;
}

.error-text {
  color: #ef4444;
  font-size: 1.1rem;
  font-weight: 500;
}

.no-data-text {
  color: #6b7280;
  font-size: 1rem;
  font-style: italic;
}

/* Huong Container */
.huong-container {
  display: flex;
  gap: 20px;
  margin-top: 20px;
}

.huong-column {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.huong-item {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  transition: all 0.3s ease;
  overflow: hidden;
}

.huong-item.active {
  border-color: #0082c6;
  box-shadow: 0 4px 15px rgba(0, 130, 198, 0.1);
}

.huong-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background: #0082c6;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.huong-header:hover {
  background: #0069a3;
}

.huong-label {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 16px;
  cursor: pointer;
  user-select: none;
  flex: 1;
}

.huong-label input[type="checkbox"] {
  width: 20px;
  height: 20px;
  cursor: pointer;
  accent-color: white;
}

.toggle-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  transition: all 0.3s ease;
}

.toggle-icon::before {
  content: '';
  width: 12px;
  height: 12px;
  border-right: 2px solid white;
  border-bottom: 2px solid white;
  transform: rotate(45deg);
  transition: all 0.3s ease;
}

.huong-item.active .toggle-icon::before {
  transform: rotate(-135deg);
}

.toggle-icon:hover {
  background: rgba(255, 255, 255, 0.2);
}

/* Dropdown Teachers */
.dropdown-teachers {
  background: white;
  padding: 0;
  max-height: 0;
  overflow: hidden;
  transition: all 0.3s ease;
  opacity: 0;
}

.huong-item.active .dropdown-teachers {
  max-height: 300px;
  opacity: 1;
  padding: 20px;
}

.teacher-list-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e2e8f0;
}

.teacher-label {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 1rem;
  margin: 10px 0;
  padding: 12px 15px;
  border-radius: 8px;
  transition: all 0.2s ease;
  background: #f8fafc;
}

.teacher-label:hover {
  background: #f1f5f9;
  transform: translateX(5px);
}

.teacher-label input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
  accent-color: #0082c6;
}

/* Action Button */
.action-btn {
  background: linear-gradient(135deg, #0082c6 0%, #0069a3 100%);
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  margin-top: 20px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 130, 198, 0.2);
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 130, 198, 0.3);
  background: linear-gradient(135deg, #0069a3 0%, #005a8c 100%);
}

.action-btn:disabled {
  background: #e2e8f0;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

/* Footer */
.footer {
  background: linear-gradient(135deg, #0082c6 0%, #0069a3 100%);
  color: white;
  padding: 1.5rem;
  text-align: center;
  height: 100px;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
}

/* Transition for dropdown */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.fade-enter-to,
.fade-leave-from {
  opacity: 1;
  transform: translateY(0);
}

/* Responsive adjustments */
@media (max-width: 1024px) {
  .main-content {
    margin-left: 220px;
    width: calc(100% - 220px);
    padding: 20px;
  }

  .sidebar {
    width: 200px;
    top: 100px;
    height: calc(100vh - 100px);
  }

  .main-content-shifted {
    margin-left: 220px;
  }

  .header {
    padding: 0 20px;
    height: 65px;
  }

  .header h1 {
    font-size: 1.2rem;
  }

  .huong-container {
    gap: 15px;
  }

  .huong-column {
    gap: 15px;
  }

  .huong-header {
    padding: 12px 15px;
  }

  .huong-label {
    font-size: 1rem;
  }

  .toggle-icon {
    width: 32px;
    height: 32px;
  }
}

@media (max-width: 768px) {
  .sidebar-toggle {
    display: block;
  }

  .main-layout {
    margin-top: 20px;
    min-height: calc(100vh - 140px);
  }

  .header {
    padding: 0 15px;
    height: 60px;
  }

  .logo {
    width: 35px;
    margin-right: 10px;
    margin-left: 40px;
  }

  .header h1 {
    font-size: 1.1rem;
  }

  .sidebar {
    width: 200px;
    left: -200px;
    top: 140px;
    height: calc(100vh - 140px);
  }

  .main-content {
    margin-left: 0;
    width: 100%;
    padding: 20px;
    margin-top: 20px;
  }

  .main-content-shifted {
    margin-left: 0;
  }

  .content {
    padding: 20px;
  }

  .huong-container {
    flex-direction: column;
  }

  .huong-column {
    width: 100%;
  }

  .huong-header {
    padding: 10px 12px;
  }

  .huong-label {
    font-size: 0.95rem;
  }

  .teacher-label {
    padding: 10px 12px;
    font-size: 0.95rem;
  }
}

@media (max-width: 480px) {
  .main-layout {
    margin-top: 20px;
    min-height: calc(100vh - 140px);
  }

  .sidebar {
    width: 180px;
    left: -180px;
    top: 140px;
    height: calc(100vh - 140px);
  }

  .main-content {
    padding: 20px;
    margin-top: 20px;
  }

  .header {
    padding: 0 10px;
    height: 55px;
  }

  .header h1 {
    font-size: 1rem;
  }

  .logo {
    width: 30px;
    margin-left: 35px;
  }

  .huong-header {
    padding: 8px 10px;
  }

  .huong-label {
    font-size: 0.9rem;
    gap: 8px;
  }

  .toggle-icon {
    width: 28px;
    height: 28px;
  }

  .teacher-label {
    padding: 8px 10px;
    font-size: 0.9rem;
  }

  .action-btn {
    padding: 10px 20px;
    font-size: 0.95rem;
  }
}

/* Preferences Section Styles */
.preferences-section {
  margin-top: 30px;
}

.preferences-section h2 {
  color: #1e293b;
  font-size: 1.5rem;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #e2e8f0;
}

.preferences-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.preference-item {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 20px;
  transition: all 0.3s ease;
}

.preference-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
}

.preference-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.preference-header h3 {
  color: #0082c6;
  font-size: 1.2rem;
  margin: 0;
}

.preference-actions {
  display: flex;
  gap: 10px;
}

.edit-btn {
  background: #0082c6;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.edit-btn:hover {
  background: #0069a3;
}

.preference-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.preference-section {
  background: white;
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.preference-section h4 {
  color: #1e293b;
  font-size: 1.1rem;
  margin: 0 0 10px 0;
}

.preference-section ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.preference-section li {
  padding: 8px 0;
  border-bottom: 1px solid #e2e8f0;
}

.preference-section li:last-child {
  border-bottom: none;
}

.preference-info {
  flex: 1;
}

.student-info {
  font-size: 0.9rem;
  color: #6b7280;
}

.preference-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 15px;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600;
}

.status-approved {
  background-color: #d1fae5;
  color: #15803d;
}

.status-pending {
  background-color: #fef3c7;
  color: #a16207;
}

.status-rejected {
  background-color: #fef2f2;
  color: #b91c1c;
}

.teacher-info-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.teacher-checkbox {
  display: flex;
  align-items: center;
  gap: 12px;
}

.view-info-btn {
  margin-left: 10px;
  padding: 4px 8px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9em;
}

.view-info-btn:hover {
  background-color: #45a049;
}

/* Bảng tổ đăng ký NCKH */
.topic-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  margin-bottom: 10px;
}
.topic-table th {
  background: #0082c6;
  color: #fff;
  font-weight: 600;
  font-size: 15px;
  padding: 12px 10px;
  text-align: left;
  border: none;
}
.topic-table th:first-child {
  border-top-left-radius: 12px;
}
.topic-table th:last-child {
  border-top-right-radius: 12px;
}
.topic-table td {
  padding: 12px 10px;
  font-size: 14px;
  color: #334155;
  background: #fff;
  border-bottom: 1px solid #e2e8f0;
  vertical-align: top;
}
.topic-table tr:last-child td {
  border-bottom: none;
}
.topic-table tr:hover td {
  background: #f1f5f9;
}
.topic-table ul {
  margin: 0;
  padding-left: 18px;
  list-style-type: disc;
}
.topic-table ul li {
  font-size: 14px;
  color: #0082c6;
  margin-bottom: 4px;
  padding-left: 0;
}
.topic-table ul li:last-child {
  margin-bottom: 0;
}
.view-info-btn {
  margin-left: 10px;
  padding: 4px 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.95em;
  transition: background 0.2s;
}
.view-info-btn:hover {
  background-color: #388e3c;
}
</style>