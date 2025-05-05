<template>
  <div class="container">
    <!-- Header -->
    <header class="header">
      <button v-if="isMobile" class="sidebar-toggle" @click="toggleSidebar">☰</button>
      <img src="@/assets/img/logo-hou.png" alt="Logo" class="logo" />
      <h1>ĐĂNG KÝ ĐỀ TÀI NGHIÊN CỨU KHOA HỌC SINH VIÊN</h1>
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
      <!-- Main content -->
      <div class="main-content" :class="{ 'main-content-shifted': isSidebarOpen && !isMobile }">
        <div class="content">
          <!-- Bảng hiển thị danh sách sinh viên đăng ký -->
          <div class="registered-students">
            <div class="section-header">
              <h2>Danh sách sinh viên đăng ký theo hướng nghiên cứu</h2>
              <button type="button" class="action-btn" @click="toggleShowRegisteredStudents">
                {{ showRegisteredStudents ? 'Ẩn danh sách sinh viên' : 'Xem danh sách sinh viên đăng ký' }}
              </button>
            </div>
            <div v-if="showRegisteredStudents">
              <div v-if="loadingStudents" class="loading-text">Đang tải danh sách sinh viên...</div>
              <div v-else-if="errorStudentsList" class="error-text">{{ errorStudentsList }}</div>
              <div v-else class="students-table-container">
                <table class="students-table">
                  <thead>
                    <tr>
                      <th>STT</th>
                      <th>Hướng nghiên cứu</th>
                      <th>Danh sách sinh viên</th>
                      <th>Hành động</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(hnc, index) in registeredStudents" :key="hnc.ma_hnc">
                      <td>{{ index + 1 }}</td>
                      <td>
                        <div class="research-direction-checkbox">
                          <input
                            type="checkbox"
                            :id="'hnc-' + hnc.ma_hnc"
                            :value="hnc"
                            v-model="selectedResearchDirection"
                            @change="updateResearchDirectionInput"
                          />
                          <label :for="'hnc-' + hnc.ma_hnc">{{ hnc.ten_hnc }}</label>
                        </div>
                      </td>
                      <td>
                        <ul>
                          <li v-for="sv in hnc.list_sv" :key="sv.ma_sv" class="student-row">
                            <div class="student-info">
                              <div class="student-checkbox">
                                <input
                                  type="checkbox"
                                  :id="'sv-' + sv.ma_sv"
                                  :value="sv"
                                  v-model="selectedStudentCheckboxes"
                                  :disabled="isStudentDisabled(sv.ma_sv)"
                                  @change="updateStudentInput"
                                />
                                <label :for="'sv-' + sv.ma_sv">{{ sv.ma_sv }}</label>
                              </div>
                              <span>{{ sv.ten_sv }}</span>
                            </div>
                            <div class="student-actions">
                              <button 
                                class="action-btn view-btn"
                                @click="viewStudentInfo(sv.ma_sv)"
                              >
                                Xem thông tin
                              </button>
                            </div>
                          </li>
                          <li v-if="!hnc.list_sv?.length">Không có sinh viên đăng ký</li>
                        </ul>
                      </td>
                      <td></td>
                    </tr>
                    <tr v-if="registeredStudents.length === 0">
                      <td colspan="5">Chưa có sinh viên nào đăng ký</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <p>Đăng ký nghiên cứu khoa học sinh viên đợt …</p>
          <p>Mỗi giảng viên chỉ được đăng ký tối đa 2 đề tài trong một đợt</p>
          <br>
          <!-- Thông báo trạng thái -->
          <p v-if="loading" class="loading-text">Đang tải dữ liệu...</p>
          <p v-else-if="error" class="error-text" style="color: red;">{{ error }}</p>
          <br>
          <br>
          <form @submit.prevent="handleSubmit" class="form-apply-topic">
            <div class="form-group">
              <label for="nameTopic" class="label">Tên đề tài:</label>
              <input
                type="text"
                id="nameTopic"
                v-model="currentTopic.ten_de_tai"
                class="input-field"
                required
              />
            </div>
            <div class="form-group">
              <label for="researchDirection" class="label">Hướng nghiên cứu:</label>
              <input
                type="text"
                id="researchDirection"
                v-model="currentTopic.ten_hnc"
                class="input-field"
                readonly
                required
              />
            </div>
            <div class="form-group">
              <label for="nameStudent1" class="label">Sinh viên 1:</label>
              <input
                type="text"
                id="nameStudent1"
                v-model="currentTopic.student1.display"
                class="input-field"
                readonly
                required
              />
            </div>
            <div class="form-group">
              <label for="nameStudent2" class="label">Sinh viên 2:</label>
              <input
                type="text"
                id="nameStudent2"
                v-model="currentTopic.student2.display"
                class="input-field"
                readonly
              />
            </div>
            <div class="form-group">
              <label for="nameStudent3" class="label">Sinh viên 3:</label>
              <input
                type="text"
                id="nameStudent3"
                v-model="currentTopic.student3.display"
                class="input-field"
                readonly
              />
            </div>
            <div class="form-buttons">
              <button type="submit" class="action-btn">
                {{ isEditing ? 'Chỉnh sửa' : 'Đăng ký' }}
              </button>
              <button type="button" class="action-btn" @click="resetForm">Làm mới</button>
              <button type="button" class="action-btn" @click="toggleShowRegistered">
                {{ showRegistered ? 'Ẩn danh sách' : 'Xem đề tài đã đăng ký' }}
              </button>
            </div>
          </form>

          <!-- Bảng hiển thị đề tài tổ NCKH đăng ký -->
          <div class="registered-topics">
            <h2>Danh sách đề tài tổ NCKH đăng ký</h2>
            <div v-if="loadingTopics" class="loading-text">Đang tải danh sách đề tài...</div>
            <div v-else-if="errorTopics" class="error-text">{{ errorTopics }}</div>
            <div v-else class="topic-table-container">
              <table class="topic-table">
                <thead>
                  <tr>
                    <th>STT</th>
                    <th>Tên đề tài</th>
                    <th>Hướng nghiên cứu</th>
                    <th>Thành viên</th>
                    <th>Đợt thực hiện</th>
                    <th>Trạng thái</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(topic, index) in registeredTopics.filter(t => !t.ten_de_tai && t.trang_thai === 1)" :key="'to-' + topic.ma_nhom">
                    <td>{{ index + 1 }}</td>
                    <td>Chưa có</td>
                    <td>
                      <ul>
                        <li v-for="hnc in topic.list_hnc" :key="hnc.ma_hnc">
                          {{ hnc.ten_hnc }}
                        </li>
                        <li v-if="!topic.list_hnc?.length">Không có</li>
                      </ul>
                    </td>
                    <td>
                      <ul>
                        <li v-for="sv in topic.thanh_vien" :key="sv.ma_sv">
                          {{ sv.ma_sv }} - {{ sv.ten_sv }}
                        </li>
                        <li v-if="!topic.thanh_vien?.length">Không có</li>
                      </ul>
                    </td>
                    <td>{{ topic.dot_thuc_hien || 'N/A' }}</td>
                    <td>{{ formatTrangThai(topic.trang_thai) }}</td>
                  </tr>
                  <tr v-if="registeredTopics.filter(t => !t.ten_de_tai && t.trang_thai === 1).length === 0">
                    <td colspan="6">Không có đề tài tổ NCKH nào đang chờ duyệt</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div class="registered-topics">
            <h2>Danh sách đề tài đã đăng ký</h2>
            <div v-if="loadingTopics" class="loading-text">Đang tải danh sách đề tài...</div>
            <div v-else-if="errorTopics" class="error-text">{{ errorTopics }}</div>
            <div v-else class="topic-table-container">
              <table class="topic-table">
                <thead>
                  <tr>
                    <th>STT</th>
                    <th>Tên đề tài</th>
                    <th>Hướng nghiên cứu</th>
                    <th>Thành viên</th>
                    <th>Đợt thực hiện</th>
                    <th>Trạng thái</th>
                    <th>Hành động</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(topic, index) in registeredTopics.filter(t => t.ten_de_tai && t.trang_thai === 2)" :key="'dk-' + topic.ma_nhom">
                    <td>{{ index + 1 }}</td>
                    <td>{{ topic.ten_de_tai }}</td>
                    <td>
                      <ul>
                        <li v-for="hnc in topic.list_hnc" :key="hnc.ma_hnc">
                          {{ hnc.ten_hnc }}
                        </li>
                        <li v-if="!topic.list_hnc?.length">Không có</li>
                      </ul>
                    </td>
                    <td>
                      <ul>
                        <li v-for="sv in topic.thanh_vien" :key="sv.ma_sv">
                          {{ sv.ma_sv }} - {{ sv.ten_sv }}
                        </li>
                        <li v-if="!topic.thanh_vien?.length">Không có</li>
                      </ul>
                    </td>
                    <td>{{ topic.dot_thuc_hien || 'N/A' }}</td>
                    <td>{{ formatTrangThai(topic.trang_thai) }}</td>
                    <td>
                      <button class="action-btn" @click="editTopic(topic)">Cập nhật</button>
                    </td>
                  </tr>
                  <tr v-if="registeredTopics.filter(t => t.ten_de_tai && t.trang_thai === 2).length === 0">
                    <td colspan="7">Chưa có đề tài nào được duyệt</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import api from '@/config/api';
import SidebarHome from '@/components/SidebarHome.vue';
import Footer from '@/components/Footer.vue';

const router = useRouter();
const authStore = useAuthStore();

const researchDirections = ref([]);
const selectedStudentCheckboxes = ref([]);
const registeredTopics = ref([]);
const loadingTopics = ref(false);
const errorTopics = ref('');
const errorStudents = ref('');
const currentTopic = ref({
  ma_nhom: null,
  ma_de_tai: null,
  ma_gv: '',
  ten_de_tai: '',
  dot_thuc_hien: 0,
  trang_thai: 1,
  tien_do: 0,
  list_hnc: [
    {
      ma_hnc: null,
      ten_hnc: '',
    },
  ],
  student1: { ma_sv: '', ten_sv: '', display: '' },
  student2: { ma_sv: '', ten_sv: '', display: '' },
  student3: { ma_sv: '', ten_sv: '', display: '' },
});
const isEditing = ref(false);
const error = ref('');
const showRegistered = ref(false);
const isSidebarOpen = ref(false);
const isMobile = ref(window.innerWidth <= 768);
const showRegisteredStudents = ref(false);
const loadingStudents = ref(false);
const errorStudentsList = ref('');
const registeredStudents = ref([]);
const selectedResearchDirection = ref([]);

// Kiểm tra đăng nhập và tải dữ liệu
onMounted(() => {
  authStore.loadUserFromStorage();
  if (!authStore.isAuthenticated) {
    router.push('/login');
  } else {
    fetchResearchDirections();
    fetchRegisteredTopics();
  }
});

// Xử lý sidebar
const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value;
};

window.addEventListener('resize', () => {
  isMobile.value = window.innerWidth <= 768;
  if (isMobile.value && isSidebarOpen.value) {
    isSidebarOpen.value = false;
  }
});

// Lấy danh sách hướng nghiên cứu từ API
async function fetchResearchDirections() {
  try {
    const response = await api.get('gv/dk_sv/by_hnc');
    researchDirections.value = response.data;
    if (!response.data.length) {
      errorStudents.value = 'Không có hướng nghiên cứu nào';
    }
  } catch (err) {
    errorStudents.value = 'Không thể tải danh sách hướng nghiên cứu';
    console.error('Lỗi khi lấy hướng nghiên cứu:', err);
  }
}

function updateStudentInput() {
  // Lấy danh sách sinh viên được tích hiện tại
  const checkedStudents = selectedStudentCheckboxes.value;

  // Đặt lại 3 ô input
  currentTopic.value.student1 = { ma_sv: '', ten_sv: '', display: '' };
  currentTopic.value.student2 = { ma_sv: '', ten_sv: '', display: '' };
  currentTopic.value.student3 = { ma_sv: '', ten_sv: '', display: '' };

  // Gán sinh viên đã tích vào input theo thứ tự
  checkedStudents.forEach((sv, index) => {
    if (index === 0) {
      currentTopic.value.student1 = {
        ma_sv: sv.ma_sv,
        ten_sv: sv.ten_sv,
        display: `${sv.ma_sv} - ${sv.ten_sv}`,
      };
    } else if (index === 1) {
      currentTopic.value.student2 = {
        ma_sv: sv.ma_sv,
        ten_sv: sv.ten_sv,
        display: `${sv.ma_sv} - ${sv.ten_sv}`,
      };
    } else if (index === 2) {
      currentTopic.value.student3 = {
        ma_sv: sv.ma_sv,
        ten_sv: sv.ten_sv,
        display: `${sv.ma_sv} - ${sv.ten_sv}`,
      };
    }
  });
}

// Lấy danh sách đề tài đã đăng ký
async function fetchRegisteredTopics() {
  try {
    loadingTopics.value = true;
    errorTopics.value = '';
    const response = await api.get('gv/nhomnckh');
    const data = response.data;
    if (!Array.isArray(data)) {
      throw new Error('Dữ liệu đề tài không hợp lệ');
    }
    registeredTopics.value = data
      .map((topic) => ({
        ma_gv: topic.ma_gv || '',
        trang_thai: topic.trang_thai || 0,
        ma_de_tai: topic.ma_de_tai || null,
        ma_nhom: topic.ma_nhom || null,
        ten_de_tai: topic.ten_de_tai || '',
        dot_thuc_hien: topic.dot_thuc_hien || new Date().getFullYear(),
        thanh_vien: Array.isArray(topic.thanh_vien)
          ? topic.thanh_vien.map((sv) => ({
              ma_sv: sv.ma_sv || '',
              ten_sv: sv.ten_sv || '',
            }))
          : [],
        list_hnc: Array.isArray(topic.list_hnc)
          ? topic.list_hnc.map((hnc) => ({
              ma_hnc: hnc.ma_hnc || null,
              ten_hnc: hnc.ten_hnc || '',
            }))
          : [],
      }))
      .sort((a, b) => b.ma_nhom - a.ma_nhom);
  } catch (err) {
    let errorMessage = 'Không thể tải danh sách đề tài';
    if (err.response) {
      console.error('Mã lỗi HTTP:', err.response.status);
      if (err.response.status === 401) {
        errorMessage = 'Phiên đăng nhập hết hạn';
        authStore.logout();
        router.push('/login');
      } else if (err.response.status === 403) {
        errorMessage = 'Bạn không có quyền truy cập';
      } else if (err.response.status === 404) {
        errorMessage = 'Danh sách đề tài trống';
        registeredTopics.value = [];
      }
    }
    errorTopics.value = errorMessage;
    registeredTopics.value = [];
    console.error('Lỗi khi lấy danh sách đề tài:', err);
  } finally {
    loadingTopics.value = false;
  }
}

// Xử lý submit form
async function handleSubmit() {
  try {
    error.value = '';
    const dssv = [];
    if (currentTopic.value.student1.ma_sv) {
      dssv.push(currentTopic.value.student1.ma_sv.trim());
    }
    if (currentTopic.value.student2.ma_sv) {
      dssv.push(currentTopic.value.student2.ma_sv.trim());
    }
    if (currentTopic.value.student3.ma_sv) {
      dssv.push(currentTopic.value.student3.ma_sv.trim());
    }

    if (!dssv.length) {
      error.value = 'Vui lòng chọn ít nhất một sinh viên hợp lệ';
      return;
    }

    // Kiểm tra số lượng đề tài của giảng viên
    const currentYear = new Date().getFullYear();
    const teacherTopics = registeredTopics.value.filter(topic => topic.dot_thuc_hien === currentYear);
    if (!isEditing.value && teacherTopics.length >= 2) {
      error.value = 'Mỗi giảng viên chỉ được đăng ký tối đa 2 đề tài trong một đợt';
      return;
    }

    // Kiểm tra sinh viên đã tham gia đề tài khác trong cùng đợt
    const studentTopics = registeredTopics.value.filter(topic => {
      if (topic.dot_thuc_hien !== currentYear) return false;
      if (isEditing.value && topic.ma_de_tai === currentTopic.value.ma_de_tai) return false;
      return topic.thanh_vien.some(sv => dssv.includes(sv.ma_sv));
    });

    if (studentTopics.length > 0) {
      const studentNames = studentTopics.flatMap(topic => 
        topic.thanh_vien
          .filter(sv => dssv.includes(sv.ma_sv))
          .map(sv => `${sv.ma_sv} - ${sv.ten_sv}`)
      );
      error.value = `Các sinh viên sau đã tham gia đề tài khác trong đợt này: ${studentNames.join(', ')}`;
      return;
    }

    const ten_de_tai = String(currentTopic.value.ten_de_tai).trim();
    if (!ten_de_tai || ten_de_tai.match(/^\s*$/)) {
      error.value = 'Tên đề tài không được để trống hoặc chỉ chứa khoảng trắng';
      return;
    }
    if (ten_de_tai.length > 255) {
      error.value = 'Tên đề tài không được vượt quá 255 ký tự';
      return;
    }

    const dot_thuc_hien = currentYear;

    // Kiểm tra hướng nghiên cứu
    if (!selectedResearchDirection.value.length) {
      error.value = 'Vui lòng chọn ít nhất một hướng nghiên cứu';
      return;
    }

    const payload = {
      dssv,
      detai: {
        ten_de_tai,
        dot_thuc_hien,
        trang_thai: 1,
        tien_do: 1
      },
      list_hnc: selectedResearchDirection.value.map(hnc => hnc.ma_hnc)
    };

    if (isEditing.value) {
      if (!currentTopic.value.ma_de_tai) {
        throw new Error('Mã đề tài không hợp lệ khi chỉnh sửa');
      }
      await api.put(`gv/detaisv/update?ma_de_tai=${currentTopic.value.ma_de_tai}&ten_de_tai=${encodeURIComponent(ten_de_tai)}`, dssv);
    } else {
      await api.post(`gv/nhomnckh`, payload);
    }
    resetForm();
    fetchRegisteredTopics();
  } catch (err) {
    let errorMessage = 'Không thể đăng ký đề tài';
    console.log(err);
    if (err.response) {
      console.error('Mã lỗi HTTP:', err.response.status);
      if (err.response.status === 500) {
        errorMessage = 'Lỗi server nội bộ, vui lòng kiểm tra lại';
      } else if (err.response.status === 422) {
        errorMessage =
          err.response.data.detail
            ?.map((e) => `${e.loc.join('.')}: ${e.msg}`)
            .join(', ') || 'Dữ liệu không hợp lệ';
      } else if (err.response.status === 401) {
        errorMessage = 'Phiên đăng nhập hết hạn';
        authStore.logout();
        router.push('/login');
      } else if (err.response.status === 403) {
        errorMessage = 'Bạn không có quyền đăng ký';
      } else if (err.response.status === 400) {
        errorMessage = err.response.data.detail || 'Dữ liệu không hợp lệ';
      }
    } else {
      errorMessage = err.message || 'Lỗi không xác định';
    }
    error.value = errorMessage;
    console.error('Lỗi khi đăng ký đề tài:', err);
  }
}

// Reset form
function resetForm() {
  currentTopic.value = {
    ma_nhom: null,
    ma_de_tai: null,
    ma_gv: '',
    ten_de_tai: '',
    dot_thuc_hien: 0,
    trang_thai: 1,
    tien_do: 0,
    ma_hnc: null,
    ten_hnc: '',
    student1: { ma_sv: '', ten_sv: '', display: '' },
    student2: { ma_sv: '', ten_sv: '', display: '' },
    student3: { ma_sv: '', ten_sv: '', display: '' },
  };
  isEditing.value = false;
  error.value = '';
  selectedStudentCheckboxes.value = [];
  selectedResearchDirection.value = [];
}

// Sửa đề tài
function editTopic(topic) {
  currentTopic.value = {
    ma_de_tai: topic.ma_de_tai,
    ten_de_tai: topic.ten_de_tai,
    ma_hnc: topic.ma_hnc,
    ten_hnc: topic.ten_hnc,
    student1: topic.thanh_vien[0]
      ? { ma_sv: topic.thanh_vien[0].ma_sv, ten_sv: topic.thanh_vien[0].ten_sv, display: `${topic.thanh_vien[0].ma_sv} - ${topic.thanh_vien[0].ten_sv}` }
      : { ma_sv: '', ten_sv: '', display: '' },
    student2: topic.thanh_vien[1]
      ? { ma_sv: topic.thanh_vien[1].ma_sv, ten_sv: topic.thanh_vien[1].ten_sv, display: `${topic.thanh_vien[1].ma_sv} - ${topic.thanh_vien[1].ten_sv}` }
      : { ma_sv: '', ten_sv: '', display: '' },
    student3: topic.thanh_vien[2]
      ? { ma_sv: topic.thanh_vien[2].ma_sv, ten_sv: topic.thanh_vien[2].ten_sv, display: `${topic.thanh_vien[2].ma_sv} - ${topic.thanh_vien[2].ten_sv}` }
      : { ma_sv: '', ten_sv: '', display: '' },
  };
  isEditing.value = true;
  
  // Cập nhật selectedResearchDirection
  if (topic.ma_hnc) {
    const hnc = registeredStudents.value.find(h => h.ma_hnc === topic.ma_hnc);
    if (hnc) {
      selectedResearchDirection.value = [hnc];
    }
  }
}

// Xóa đề tài
async function confirmDelete(ma_nhom) {
  if (!window.confirm('Bạn có chắc chắn muốn xóa nhóm này?')) return;
  try {
    await api.delete(`gv/nhomnckh/${ma_nhom}`);
    fetchRegisteredTopics();
  } catch (err) {
    let errorMessage = 'Không thể xóa nhóm';
    if (err.response) {
      console.error('Mã lỗi HTTP:', err.response.status);
      if (err.response.status === 401) {
        errorMessage = 'Phiên đăng nhập hết hạn';
        authStore.logout();
        router.push('/login');
      } else if (err.response.status === 403) {
        errorMessage = 'Bạn không có quyền xóa';
      }
    }
    error.value = errorMessage;
    console.error('Lỗi khi xóa nhóm:', err);
  }
}

// Định dạng trạng thái
function formatTrangThai(trang_thai) {
  switch (trang_thai) {
    case 1:
      return 'Đang chờ duyệt';
    case 2:
      return 'Đã được duyệt';
    case 0:
      return 'Đã bị hủy';
    default:
      return 'Không xác định';
  }
}

// Toggle danh sách đề tài đã đăng ký
function toggleShowRegistered() {
  showRegistered.value = !showRegistered.value;
}

// Toggle danh sách sinh viên đăng ký
function toggleShowRegisteredStudents() {
  showRegisteredStudents.value = !showRegisteredStudents.value;
  if (showRegisteredStudents.value) {
    fetchRegisteredStudents();
  }
}

// Lấy danh sách sinh viên đăng ký
async function fetchRegisteredStudents() {
  try {
    loadingStudents.value = true;
    errorStudentsList.value = '';
    const response = await api.get('gv/dk_sv/by_hnc');
    registeredStudents.value = response.data;
  } catch (err) {
    let errorMessage = 'Không thể tải danh sách sinh viên';
    if (err.response) {
      console.error('Mã lỗi HTTP:', err.response.status);
      if (err.response.status === 401) {
        errorMessage = 'Phiên đăng nhập hết hạn';
        authStore.logout();
        router.push('/login');
      } else if (err.response.status === 403) {
        errorMessage = 'Bạn không có quyền truy cập';
      } else if (err.response.status === 404) {
        errorMessage = 'Không tìm thấy dữ liệu';
      }
    }
    errorStudentsList.value = errorMessage;
    registeredStudents.value = [];
  } finally {
    loadingStudents.value = false;
  }
}

// Xem thông tin sinh viên
function viewStudentInfo(ma_sv) {
  if (!ma_sv) {
    console.error('Mã sinh viên không hợp lệ');
    return;
  }
  router.push({
    path: '/info-students',
    query: { ma_sv }
  });
}

// Kiểm tra xem sinh viên có thể được chọn hay không
function isStudentDisabled(ma_sv) {
  // Nếu sinh viên đã được chọn trong selectedStudentCheckboxes, cho phép bỏ chọn
  if (selectedStudentCheckboxes.value.some(sv => sv.ma_sv === ma_sv)) {
    return false;
  }
  
  // Nếu đã chọn 3 sinh viên, disable tất cả các sinh viên chưa được chọn
  if (selectedStudentCheckboxes.value.length >= 3) {
    return true;
  }

  // Kiểm tra xem sinh viên đã được chọn ở hướng nghiên cứu khác chưa
  const selectedHncs = new Set(selectedStudentCheckboxes.value.map(sv => {
    const hnc = registeredStudents.value.find(h => 
      h.list_sv.some(s => s.ma_sv === sv.ma_sv)
    );
    return hnc?.ma_hnc;
  }));

  const currentHnc = registeredStudents.value.find(h => 
    h.list_sv.some(s => s.ma_sv === ma_sv)
  )?.ma_hnc;

  // Nếu sinh viên thuộc hướng nghiên cứu khác với các sinh viên đã chọn
  if (selectedHncs.size > 0 && !selectedHncs.has(currentHnc)) {
    return true;
  }

  return false;
}

function updateResearchDirectionInput() {
  if (selectedResearchDirection.value.length > 0) {
    const hnc = selectedResearchDirection.value[0];
    currentTopic.value.ma_hnc = hnc.ma_hnc;
    currentTopic.value.ten_hnc = hnc.ten_hnc;
  } else {
    currentTopic.value.ma_hnc = null;
    currentTopic.value.ten_hnc = '';
  }
}
</script>

<style scoped>
/* Container */
.container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  overflow-y: auto;
}

.container::-webkit-scrollbar {
  width: 5px;
}

.container::-webkit-scrollbar-track {
  background: #e6eef5;
  border-radius: 10px;
}

.container::-webkit-scrollbar-thumb {
  background: #0082c6;
  border-radius: 10px;
}

.container::-webkit-scrollbar-thumb:hover {
  background: #0069a3;
}
.form-group select.input-field {
  width: 100%;
  padding: 8px;
  border: 1px solid #d1dbe3;
  border-radius: 6px;
  font-size: 14px;
  background-color: #f9fafb;
  transition: border-color 0.3s, box-shadow 0.3s, background-color 0.3s;
}

.form-group select.input-field:focus {
  border-color: #0082c6;
  box-shadow: 0 0 0 2px rgba(0, 130, 198, 0.2);
  background-color: white;
  outline: none;
}

/* Overlay cho mobile */
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

/* Header */
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: white;
  border-bottom: 1px solid #ccc;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 80px;
  z-index: 1000;
  padding: 10px 20px 10px 70px;
  box-sizing: border-box;
}

.logo {
  width: 50px;
  margin-right: 2rem;
  margin-top:2rem
}

.header h1 {
  font-size: 1.2rem;
  margin: 0;
  flex-grow: 1;
  text-align: center;
  color: #0082c6;
}

.sidebar-toggle {
  position: fixed;
  top: 20px;
  left: 20px;
  background: #0082c6;
  color: white;
  border: none;
  padding: 0.5rem 0.8rem;
  font-size: 1.2rem;
  cursor: pointer;
  border-radius: 5px;
}

.sidebar-toggle:hover {
  background: #0069a3;
}

/* Main layout */
.main-layout {
  display: flex;
  margin-top: 80px;
  min-height: calc(100vh - 80px - 100px);
}

/* Sidebar */
.sidebar {
  width: 220px;
  background: #0082c6;
  position: fixed;
  top: 80px;
  left: 0;
  height: calc(100vh - 80px);
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  transition: left 0.3s ease;
  z-index: 1000;
}

/* Main Content */
.main-content {
  flex: 1;
  padding: 20px;
  box-sizing: border-box;
  background: #f4f7fa;
  transition: margin-left 0.3s ease;
  margin-left: 240px;
}

.main-content-shifted {
  margin-left: 240px;
}

/* Content */
.content {
  background-color: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.content:hover {
  transform: translateY(-2px);
}
/* Dropdown */

.dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  background: white;
  border: 1px solid #d1dbe3;
  border-radius: 6px;
  max-height: 200px;
  overflow-y: auto;
  width: 100%;
  z-index: 1000;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.dropdown-item {
  padding: 8px 12px;
  cursor: pointer;
  font-size: 14px;
}

.dropdown-item:hover {
  background: #f9fafb;
}

.dropdown-item.disabled {
  color: #6b7280;
  cursor: default;
}

.dropdown-item.disabled:hover {
  background: none;
}

.student-list {
  max-height: 150px;
  overflow-y: auto;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 10px;
  font-size: 14px;
}

.student-item {
  display: flex;
  align-items: center;
  padding: 5px 0;
}

.student-item input[type="checkbox"] {
  margin-right: 10px;
}

.no-students {
  color: #888;
  padding: 10px;
}

.input-field[readonly] {
  background-color: #f0f0f0;
  cursor: not-allowed;
}

/* Form group để chứa dropdown */
.form-group {
  position: relative;
}

/* Form */
.form-apply-topic {
  display: flex;
  flex-direction: column;
  gap: 15px;
  max-width: 600px;
  margin: 0 auto;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label.label {
  display: block;
  margin-bottom: 5px;
  font-weight: 600;
  color: #1a3c5e;
  font-size: 16px;
}

.form-group input.input-field {
  width: 100%;
  padding: 8px;
  border: 1px solid #d1dbe3;
  border-radius: 6px;
  font-size: 14px;
  background-color: #f9fafb;
  transition: border-color 0.3s, box-shadow 0.3s, background-color 0.3s;
}

.form-group input.input-field:focus {
  border-color: #0082c6;
  box-shadow: 0 0 0 2px rgba(0, 130, 198, 0.2);
  background-color: white;
  outline: none;
}

.form-buttons {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

/* Registered Topics */
.registered-topics {
  margin-top: 20px;
}

.registered-topics h2 {
  font-size: 1.5rem;
  color: #1a3c5e;
  margin-bottom: 15px;
}

.topic-table-container {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow-x: auto; /* Cho phép cuộn ngang trên mobile */
}

.topic-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

.topic-table th,
.topic-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #d1dbe3;
}

.topic-table th {
  background: #0082c6;
  color: white;
  font-weight: 600;
  font-size: 14px;
}

.topic-table td {
  background: white;
  font-size: 14px;
}

.topic-table td:first-child,
.topic-table td:nth-child(2),
.topic-table td:nth-child(3) {
  cursor: pointer;
}

.topic-table tr:hover {
  background: #f9fafb;
}

.action-btn {
  background-color: #0082c6;
  color: white;
  padding: 8px 16px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.action-btn:hover {
  background-color: #0069a3;
}

/* Footer */
.footer {
  background: #0082c6;
  color: white;
  padding: 1rem;
  text-align: center;
  height: 100px; /* Chiều cao cố định từ trang trước */
}

/* Suggestions */
.suggestions {
  position: absolute;
  background: white;
  border: 1px solid #d1dbe3;
  border-radius: 6px;
  max-height: 150px;
  overflow-y: auto;
  width: calc(100% - 16px); /* Trừ padding của input */
  z-index: 1000;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.suggestion-item {
  padding: 8px;
  cursor: pointer;
  font-size: 14px;
}

.suggestion-item:hover {
  background: #f9fafb;
}

/* Form group để chứa suggestions */
.form-group {
  position: relative;
}

/* Table */
.topic-table ul {
  margin: 0;
  padding-left: 20px;
}

.topic-table ul li {
  font-size: 14px;
  margin-bottom: 5px;
}

/* Responsive */
@media (max-width: 1024px) {
  .header {
    padding: 10px 20px 10px 60px;
  }

  .sidebar-toggle {
    top: 20px;
    left: 20px;
    width: 30px;
    height: 30px;
  }

  .main-layout {
    margin-top: 80px;
  }

  .sidebar {
    top: 80px;
    width: 200px;
  }

  .main-content {
    margin-left: 220px;
  }

  .main-content-shifted {
    margin-left: 220px;
  }
}

@media (max-width: 768px) {
  .header {
    padding: 10px 15px 10px 50px;
  }

  .sidebar-toggle {
    top: 15px;
    left: 15px;
    width: 28px;
    height: 28px;
  }

  .main-layout {
    margin-top: 80px;
  }

  .sidebar {
    top: 80px;
    width: 200px;
    left: -200px;
  }

  .sidebar-open {
    left: 0;
  }

  .main-content {
    margin-left: 0;
    padding: 15px;
  }

  .main-content-shifted {
    margin-left: 0;
  }
}

@media (max-width: 480px) {
  .header {
    padding: 10px 10px 10px 45px;
  }

  .sidebar-toggle {
    top: 10px;
    left: 10px;
    width: 26px;
    height: 26px;
  }

  .main-layout {
    margin-top: 80px;
  }

  .sidebar {
    top: 80px;
    width: 180px;
    left: -180px;
  }

  .sidebar-open {
    left: 0;
  }

  .main-content {
    padding: 10px;
  }
}

/* Registered Students */
.registered-students {
  margin-top: 20px;
}

.registered-students h2 {
  font-size: 1.5rem;
  color: #1a3c5e;
  margin-bottom: 15px;
}

.students-table-container {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow-x: auto;
}

.students-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

.students-table th,
.students-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #d1dbe3;
}

.students-table th {
  background: #0082c6;
  color: white;
  font-weight: 600;
  font-size: 14px;
}

.students-table td {
  background: white;
  font-size: 14px;
  vertical-align: top;
  padding: 8px;
}

.students-table ul {
  margin: 0;
  padding: 0;
  list-style: none;
}

.students-table ul li {
  font-size: 14px;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.student-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.student-info {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
}

.student-checkbox {
  display: flex;
  align-items: center;
  gap: 5px;
}

.student-checkbox input[type="checkbox"] {
  width: 16px;
  height: 16px;
  cursor: pointer;
  margin: 0;
}

.student-checkbox input[type="checkbox"]:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.student-checkbox label {
  cursor: pointer;
  font-size: 14px;
  margin: 0;
}

.student-actions {
  display: flex;
  align-items: center;
  gap: 5px;
}

.view-btn {
  margin: 0;
  padding: 6px 12px;
  font-size: 12px;
  white-space: nowrap;
}

.view-btn:hover {
  background-color: #0069a3;
}

/* Section Header */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header h2 {
  margin: 0;
  font-size: 1.5rem;
  color: #1a3c5e;
}

/* Registered Students */
.registered-students {
  margin-bottom: 30px;
  background-color: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.checkbox-container {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 4px 0;
}

.checkbox-container input[type="checkbox"] {
  width: 16px;
  height: 16px;
  cursor: pointer;
  margin: 0;
}

.checkbox-container input[type="checkbox"]:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.checkbox-container label {
  cursor: pointer;
  font-size: 14px;
  margin: 0;
}

/* Student row container */
.student-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 5px;
}

.student-info {
  flex: 1;
}

.student-actions {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

/* Research Direction Checkbox */
.research-direction-checkbox {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px;
  background-color: #f9fafb;
  border-radius: 6px;
  transition: background-color 0.3s;
}

.research-direction-checkbox:hover {
  background-color: #f0f4f8;
}

.research-direction-checkbox input[type="checkbox"] {
  width: 16px;
  height: 16px;
  cursor: pointer;
  margin: 0;
}

.research-direction-checkbox label {
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  color: #1a3c5e;
  margin: 0;
  flex: 1;
}
</style>