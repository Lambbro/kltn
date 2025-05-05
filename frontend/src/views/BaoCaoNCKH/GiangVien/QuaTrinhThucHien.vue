<template>
  <div class="container">
    <header class="header">
      <button v-if="isMobile" class="sidebar-toggle" @click="toggleSidebar">☰</button>
      <img src="@/assets/img/logo-hou.png" alt="Logo" class="logo"/>
      <div class="button-group">
        <button class="active" @click="$router.push(`/de-tai-nckh`)">Tổng hợp đề tài</button>
        <button class="active" @click="$router.push(`/de-tai-dang-thuc-hien-gv`)">Đề tài đang thực hiện</button>
      </div>
    </header>

    <!-- Overlay khi sidebar mở trên mobile -->
    <div v-if="isSidebarOpen && isMobile" class="overlay" @click="toggleSidebar"></div>

    <div class="main-layout">
      <SidebarHome class="sidebar" :class="{ 'sidebar-open': isSidebarOpen }" />
      <div class="main-content">
        <div class="content">
          <div class="form-container">
            <!-- Tên đề tài -->
            <div class="form-group">
              <label>Tên đề tài:</label>
              <input type="text" v-model="projectData.ten_de_tai" class="form-input" readonly />
            </div>

            <!-- Tên yêu cầu -->
            <div class="form-group">
              <label>Tên yêu cầu:</label>
              <input type="text" v-model="submissionTitle" class="form-input" readonly />
            </div>

            <!-- Form nộp thuyết minh -->
            <div v-if="route.query.type === '1'" class="thesis-form">
              <div class="form-section">
                <h3>Thông tin thuyết minh</h3>
                
                <!-- Cấp độ đề tài -->
                <div class="form-group">
                  <label>Cấp độ đề tài:</label>
                  <select v-model="thesisData.cap_do" class="form-input">
                    <option value="1">Cấp trường loại 1</option>
                    <option value="2">Cấp trường loại 2</option>
                    <option value="3">Cấp trường loại 3</option>
                  </select>
                </div>

                <!-- Danh sách thành viên -->
                <div class="form-group">
                  <label>Thành viên tham gia:</label>
                  <div class="member-list">
                    <div v-for="(member, index) in thesisData.thanh_vien" :key="index" class="member-item">
                      <div class="member-inputs">
                        <input 
                          type="text" 
                          v-model="member.ma_gv" 
                          placeholder="Mã giảng viên"
                          class="form-input"
                        />
                        <select v-model="member.vi_tri_tham_gia" class="form-input">
                            <option value="2">Thư ký khoa học</option>
                            <option value="3">Thành viên chính</option>
                            <option value="4">Thành viên</option>
                            <option value="5">Kỹ thuật viên</option>
                            <option value="6">Nhân viên hỗ trợ</option>
                        </select>
                        <button @click="removeMember(index)" class="remove-member-btn">×</button>
                      </div>
                    </div>
                    <button @click="addMember" class="add-member-btn">+ Thêm thành viên</button>
                  </div>
                </div>

                <!-- File nộp -->
                <div class="form-group">
                  <label>File thuyết minh:</label>
                  <div class="file-upload">
                    <input
                      type="file"
                      @change="handleFileChange"
                      class="file-input"
                      accept=".pdf,.doc,.docx"
                    />
                  </div>
                  <div v-if="selectedFiles.length > 0" class="selected-files">
                    <p>File đã chọn:</p>
                    <ul>
                      <li>
                        {{ selectedFiles[0].name }}
                        <button @click="removeFile(0)" class="remove-file-btn">×</button>
                      </li>
                    </ul>
                  </div>
                  <p class="file-note">Lưu ý: Chỉ nộp một file báo cáo dưới dạng pdf, doc, docx</p>
                </div>

                <div class="button-group">
                  <button class="action-btn submit" @click="handleSubmitThesis">Nộp thuyết minh</button>
                  <button class="action-btn submit" @click="handleViewThesis">Xem thuyết minh đã nộp</button>
                </div>
              </div>
            </div>

            <!-- Form nộp báo cáo tiến độ và nghiệm thu -->
            <div v-else class="submission-box">
              <div class="submission-header">
                <h3>Trạng thái nộp bài</h3>
                <div class="status-checkbox">
                  <input type="checkbox" :checked="false" disabled />
                  <span class="status-text">Chưa nộp</span>
                </div>
              </div>

              <div class="submission-details">
                <div class="form-group">
                  <label>File nộp:</label>
                  <div class="file-upload">
                    <input
                      type="file"
                      @change="handleFileChange"
                      class="file-input"
                      accept=".pdf,.doc,.docx,.pptx"
                      multiple
                    />
                  </div>
                  <div v-if="selectedFiles.length > 0" class="selected-files">
                    <p>File đã chọn:</p>
                    <ul>
                      <li v-for="(file, index) in selectedFiles" :key="index">
                        {{ file.name }}
                        <button @click="removeFile(index)" class="remove-file-btn">×</button>
                      </li>
                    </ul>
                  </div>
                  <p class="file-note">Lưu ý: Chỉ nộp báo cáo dưới dạng pdf, doc, docx, pptx</p>
                </div>

                <div class="button-group">
                  <button class="action-btn submit" @click="handleSubmit">Nộp bài</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Thêm bảng hiển thị thông tin thuyết minh -->
    <div v-if="showThesisModal" class="modal-overlay" @click="showThesisModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Thông tin thuyết minh</h3>
          <button class="close-btn" @click="showThesisModal = false">×</button>
        </div>
        <div class="modal-body">
          <div v-if="loadingThesis">Đang tải dữ liệu...</div>
          <div v-else-if="thesisError">{{ thesisError }}</div>
          <div v-else-if="currentThesis" class="thesis-info">
            <div class="info-section">
              <div class="info-item">
                <label>Tên đề tài:</label>
                <span>{{ currentThesis.ten_de_tai }}</span>
              </div>
              <div class="info-item">
                <label>Cấp độ:</label>
                <span>{{ getCapDoText(currentThesis.cap_do) }}</span>
              </div>
              <div class="info-item">
                <label>Thời gian bắt đầu:</label>
                <span>{{ formatDate(currentThesis.tg_bat_dau) }}</span>
              </div>
              <div class="info-item">
                <label>Thời gian nghiệm thu:</label>
                <span>{{ formatDate(currentThesis.tg_nghiem_thu) }}</span>
              </div>
              <div class="info-item">
                <label>Trạng thái:</label>
                <span>{{ getTrangThaiText(currentThesis.trang_thai) }}</span>
              </div>
              <div class="info-item">
                <label>Tiến độ:</label>
                <span>{{ currentThesis.tien_do }}%</span>
              </div>
            </div>

            <div class="members-section">
              <h4>Thành viên tham gia</h4>
              <table class="members-table">
                <thead>
                  <tr>
                    <th>Mã GV</th>
                    <th>Tên GV</th>
                    <th>Vị trí tham gia</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(member, index) in currentThesis.thanh_vien" :key="index">
                    <td>{{ member.ma_gv }}</td>
                    <td>{{ member.ten_gv }}</td>
                    <td>{{ getViTriText(member.vi_tri_tham_gia) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div class="documents-section">
              <h4>Tài liệu đã nộp</h4>
              <table class="documents-table">
                <thead>
                  <tr>
                    <th>Loại tài liệu</th>
                    <th>Thời gian nộp</th>
                    <th>Trạng thái</th>
                    <th>Link</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(doc, index) in filteredDocuments" :key="index">
                    <td>{{ getLoaiTaiLieuText(doc.loai_tai_lieu) }}</td>
                    <td>{{ formatDate(doc.thoi_gian_nop) }}</td>
                    <td>
                      <span class="status-badge" :class="getStatusClass(doc.trang_thai)">
                        {{ getTrangThaiText(doc.trang_thai) }}
                      </span>
                    </td>
                    <td>
                      <a v-if="doc.link_tep" :href="doc.link_tep" target="_blank" class="document-link">
                        Xem file
                      </a>
                      <span v-else>-</span>
                    </td>
                  </tr>
                </tbody>
              </table>
              <div v-if="!filteredDocuments || filteredDocuments.length === 0" class="no-documents">
                Chưa có tài liệu nào được nộp
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRoute } from 'vue-router';
import SidebarHome from '@/components/SidebarHome.vue';
import api from '@/config/api';

const route = useRoute();
const isSidebarOpen = ref(false);
const isMobile = ref(window.innerWidth <= 768);
const selectedFiles = ref([]);

// Project data structure
const projectData = ref({
  ten_de_tai: '',
  ma_de_tai: '',
});

// Thesis data structure
const thesisData = ref({
  cap_do: 3,
  thanh_vien: [
    {
      ma_gv: '',
      vi_tri_tham_gia: 2
    }
  ]
});

// Thêm state cho danh sách giảng viên
const teacherList = ref([]);

const submissionTitle = computed(() => {
  const type = route.query.type;
  if (!type) return 'Không xác định';
  switch (type) {
    case '1':
      return 'Nộp báo cáo thuyết minh';
    case '2':
      return 'Nộp báo cáo tiến độ đề tài';
    case '3':
      return 'Hồ sơ đề xuất nghiệm thu đề tài';
    default:
      return 'Không xác định';
  }
});

// Thêm các state mới
const showThesisModal = ref(false);
const currentThesis = ref(null);
const loadingThesis = ref(false);
const thesisError = ref(null);

// Thêm các hàm helper
const getCapDoText = (capDo) => {
  const capDoMap = {
    1: 'Cấp trường loại 1',
    2: 'Cấp trường loại 2',
    3: 'Cấp trường loại 3'
  };
  return capDoMap[capDo] || 'Không xác định';
};

const getViTriText = (viTri) => {
  const viTriMap = {
    1: 'Chủ nhiệm',
    2: 'Thư ký khoa học',
    3: 'Thành viên chính',
    4: 'Thành viên',
    5: 'Kỹ thuật viên',
    6: 'Nhân viên hỗ trợ'
  };
  return viTriMap[viTri] || 'Không xác định';
};

const getLoaiTaiLieuText = (loai) => {
  const loaiMap = {
    1: 'Báo cáo thuyết minh',
    2: 'Báo cáo tiến độ',
    3: 'Hồ sơ nghiệm thu'
  };
  return loaiMap[loai] || 'Không xác định';
};

const getTrangThaiText = (trangThai) => {
  const trangThaiMap = {
    0: 'Chưa nộp',
    1: 'Đã nộp',
    2: 'Đang xử lý',
    3: 'Cần chỉnh sửa',
    4: 'Đã duyệt'
  };
  return trangThaiMap[trangThai] || 'Không xác định';
};

const getStatusClass = (trangThai) => {
  const classMap = {
    0: 'status-pending',
    1: 'status-submitted',
    2: 'status-processing',
    3: 'status-need-update',
    4: 'status-approved'
  };
  return classMap[trangThai] || '';
};

const formatDate = (dateString) => {
  if (!dateString) return 'Chưa có';
  const date = new Date(dateString);
  return date.toLocaleString('vi-VN');
};

// Fetch project data
const fetchProjectData = async () => {
  try {
    const response = await api.get(`detai_gv/de_tai/${route.query.projectId}`);
    if (response.data && typeof response.data === 'object') {
      projectData.value = {
        ten_de_tai: response.data.ten_de_tai || '',
        ma_de_tai: response.data.ma_de_tai || '',
      };
    } else {
      throw new Error('Invalid API response structure');
    }
  } catch (error) {
    console.error('Error fetching project data:', error);
    alert('Không thể tải dữ liệu đề tài. Vui lòng thử lại sau.');
    projectData.value = { ten_de_tai: '', ma_de_tai: '' };
  }
};

// Hàm lấy danh sách giảng viên
const fetchTeacherList = async () => {
  try {
    const response = await api.get('phongkhdn/gv');
    if (response.data && Array.isArray(response.data)) {
      teacherList.value = response.data;
    }
  } catch (error) {
    console.error('Lỗi khi lấy danh sách giảng viên:', error);
    alert('Không thể tải danh sách giảng viên. Vui lòng thử lại sau.');
  }
};

// Hàm kiểm tra mã giảng viên
const validateTeacherCode = (ma_gv) => {
  return teacherList.value.some(teacher => teacher.ma_gv === ma_gv);
};

const handleFileChange = (event) => {
  const files = Array.from(event.target.files);
  const allowedTypes = [
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  ];

  if (files.length > 1) {
    alert('Chỉ được phép nộp một file duy nhất');
    event.target.value = '';
    return;
  }

  const validFiles = files.filter(file => {
    if (!allowedTypes.includes(file.type)) {
      alert(`File ${file.name} không đúng định dạng. Chỉ chấp nhận pdf, doc, docx`);
      return false;
    }
    return true;
  });

  selectedFiles.value = validFiles;
  event.target.value = ''; // Reset input to allow selecting the same file again
};

const removeFile = (index) => {
  selectedFiles.value = [];
};

const addMember = () => {
  thesisData.value.thanh_vien.push({
    ma_gv: '',
    vi_tri_tham_gia: ''
  });
};

const removeMember = (index) => {
  thesisData.value.thanh_vien.splice(index, 1);
};

const handleSubmitThesis = async () => {
  if (selectedFiles.value.length === 0) {
    alert('Vui lòng chọn file thuyết minh để nộp');
    return;
  }

  // Validate member data
  const invalidMember = thesisData.value.thanh_vien.find(member => !member.ma_gv || !member.vi_tri_tham_gia);
  if (invalidMember) {
    alert('Vui lòng nhập đầy đủ thông tin cho tất cả thành viên');
    return;
  }

  // Validate cap_do
  if (!thesisData.value.cap_do) {
    alert('Vui lòng nhập cấp độ đề tài');
    return;
  }

  // Kiểm tra mã giảng viên
  const invalidTeacher = thesisData.value.thanh_vien.find(member => !validateTeacherCode(member.ma_gv));
  if (invalidTeacher) {
    alert(`Mã giảng viên ${invalidTeacher.ma_gv} không tồn tại trong hệ thống. Vui lòng kiểm tra lại.`);
    return;
  }

  try {
    const formData = new FormData();
    formData.append('thuyet_minh_data', JSON.stringify(thesisData.value));
    formData.append('file', selectedFiles.value[0]);

    console.log('dữ liệu gửi đi:', formData);
    const response = await api.post(
      'detai_gv/thuyet_minh',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );

    if (response.status === 200 || response.status === 201) {
      alert('Nộp thuyết minh thành công!');
      selectedFiles.value = [];
      document.querySelector('.file-input').value = '';
      // Reset form
      thesisData.value = {
        cap_do: 3,
        thanh_vien: [
          {
            ma_gv: '',
            vi_tri_tham_gia: 2
          }
        ]
      };
    } else {
      throw new Error('Unexpected response status');
    }
  } catch (error) {
    console.error('Lỗi khi nộp thuyết minh:', error);
    alert('Có lỗi xảy ra khi nộp thuyết minh. Vui lòng thử lại.');
  }
};

const handleViewThesis = async () => {
  try {
    loadingThesis.value = true;
    thesisError.value = null;
    showThesisModal.value = true;

    const response = await api.get(`detai_gv/thuyet_minh`);
    if (response.data && Array.isArray(response.data)) {
      // Lọc ra thuyết minh của đề tài đang truy cập
      const currentThesisData = response.data.find(
        thesis => thesis.ma_de_tai === projectData.value.ma_de_tai
      );
      
      if (currentThesisData) {
        currentThesis.value = currentThesisData;
      } else {
        thesisError.value = 'Không tìm thấy thông tin thuyết minh cho đề tài này';
      }
    } else {
      throw new Error('Unexpected response structure');
    }
  } catch (error) {
    console.error('Lỗi khi xem thuyết minh:', error);
    thesisError.value = 'Có lỗi xảy ra khi xem thuyết minh. Vui lòng thử lại.';
  } finally {
    loadingThesis.value = false;
  }
};

const handleSubmit = async () => {
  if (selectedFiles.value.length === 0) {
    alert('Vui lòng chọn ít nhất một file để nộp');
    return;
  }

  try {
    const formData = new FormData();
    formData.append('ma_de_tai', projectData.value.ma_de_tai);
    formData.append('loai_tai_lieu', route.query.type);
    
    selectedFiles.value.forEach((file, index) => {
      formData.append(`files`, file);
    });

    const response = await api.post(
      `detai_gv/upload/${projectData.value.ma_de_tai}/${route.query.type}`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );

    if (response.status === 200 || response.status === 201) {
      alert('Nộp bài thành công!');
      selectedFiles.value = [];
      document.querySelector('.file-input').value = '';
    } else {
      throw new Error('Unexpected response status');
    }
  } catch (error) {
    console.error('Lỗi khi nộp:', error);
    alert('Có lỗi xảy ra khi nộp. Vui lòng thử lại.');
  }
};

// Handle responsive sidebar
const handleResize = () => {
  isMobile.value = window.innerWidth <= 768;
  if (!isMobile.value && isSidebarOpen.value) {
    isSidebarOpen.value = false;
  }
};

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value;
};

// Thêm computed property để lọc tài liệu
const filteredDocuments = computed(() => {
  if (!currentThesis.value || !currentThesis.value.tai_lieu) return [];
  
  const currentType = parseInt(route.query.type);
  return currentThesis.value.tai_lieu.filter(doc => doc.loai_tai_lieu === currentType);
});

onMounted(() => {
  window.addEventListener('resize', handleResize);
  handleResize();
  fetchProjectData();
  fetchTeacherList(); // Lấy danh sách giảng viên khi component được mount
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
  background-color: #f0f7ff;
}

.header {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  background: linear-gradient(135deg, #0082c6 0%, #0069a3 100%);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
  height: 80px;
  padding: 10px 40px;
  box-sizing: border-box;
  box-shadow: 0 4px 20px rgba(0, 130, 198, 0.2);
}

.logo {
  width: 50px;
  margin-right: 2rem;
  margin-top: 2rem;
  margin-left: 2rem;
}

.logo:hover {
  transform: scale(1.05);
}

.button-group {
  display: flex;
  gap: 20px;
  align-items: center;
  margin-left: 120px;
}

.button-group button {
  padding: 12px 24px;
  border: none;
  background: white;
  cursor: pointer;
  border-radius: 8px;
  color: #0082c6;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  bottom: 15px;
}

.button-group button::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 130, 198, 0.1);
  transform: scaleX(0);
  transform-origin: right;
  transition: transform 0.3s ease;
}

.button-group button:hover::before {
  transform: scaleX(1);
  transform-origin: left;
}

.button-group button:hover {
  background: #f8fafc;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  color: #000000;
}

.button-group button.active:hover {
  background: #0069a3;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.main-layout {
  display: flex;
  margin-top: 100px;
  min-height: calc(100vh - 100px);
}

.sidebar {
  width: 220px;
  background: linear-gradient(180deg, #0082c6 0%, #0069a3 100%);
  position: fixed;
  top: 80px;
  left: 0;
  height: calc(100vh - 80px);
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  z-index: 999;
}

.main-content {
  flex: 1;
  padding-le: 20px;
  margin-left: 220px;
}

.content {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 130, 198, 0.1);
}

.title {
  color: #0082c6;
  margin-bottom: 2rem;
  font-size: 1.5rem;
}

.form-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #1a3c5e;
}

.form-input {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e6f2ff;
  border-radius: 6px;
  background-color: #fff;
  font-size: 1rem;
}

.form-input[readonly] {
  background-color: #f8fafc;
  cursor: not-allowed;
}

.submission-box {
  background: #fff;
  border: 2px solid #e6f2ff;
  border-radius: 12px;
  padding: 1.5rem;
  margin-top: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.submission-box.submitted {
  border-color: #10b981;
  background: #f0fdf4;
}

.submission-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #e6f2ff;
}

.submission-header h3 {
  color: #0082c6;
  margin: 0;
}

.status-checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.status-text {
  font-weight: 600;
  color: #666;
}

.submitted .status-text {
  color: #10b981;
}

.file-upload {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.file-input {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e6f2ff;
  border-radius: 6px;
  background: white;
  cursor: pointer;
}

.file-input:hover {
  border-color: #0082c6;
}

.file-note {
  margin-top: 0.5rem;
  color: #666;
  font-size: 0.9rem;
  font-style: italic;
}

.button-group {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.action-btn {
  flex: 1;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn.submit {
  background: #0082c6;
  color: white;
}

.action-btn.history {
  background: #e6f2ff;
  color: #1a3c5e;
}

.action-btn.edit {
  background: #f0f7ff;
  color: #0082c6;
  border: 2px solid #0082c6;
}

.action-btn.edit:disabled {
  background: #e2e8f0;
  color: #94a3b8;
  border-color: #e2e8f0;
  cursor: not-allowed;
}

.action-btn.edit:not(:disabled):hover {
  background: #e6f2ff;
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.history-section {
  margin-top: 2rem;
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.history-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

.history-table th,
.history-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #e6f2ff;
}

.history-table th {
  background: #f8fafc;
  font-weight: 600;
  color: #1a3c5e;
}

.submitted-files-list {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.file-item {
  padding: 4px 8px;
  background: #f8fafc;
  border-radius: 4px;
  border: 1px solid #e6f2ff;
}

.file-item:hover {
  background: #f0f7ff;
}

.file-link {
  color: #0082c6;
  text-decoration: none;
  display: block;
  width: 100%;
}

.file-link:hover {
  text-decoration: underline;
}

.status-success {
  color: #10b981;
  font-weight: 600;
}

.submitted-file {
  margin-top: 0.5rem;
  padding: 0.75rem;
  background: #f0fdf4;
  border: 1px solid #10b981;
  border-radius: 6px;
}

.submitted-file p {
  margin: 0;
  color: #1a3c5e;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.feedback-input {
  background-color: #f8fafc;
  resize: none;
  min-height: 100px;
  padding: 12px;
  line-height: 1.5;
}

.feedback-input::placeholder {
  color: #94a3b8;
  font-style: italic;
}

.feedback-input:focus {
  outline: none;
  border-color: #0082c6;
}

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 998;
  transition: opacity 0.3s ease;
}

.selected-files {
  margin-top: 1rem;
  padding: 0.5rem;
  background: #f8fafc;
  border-radius: 4px;
}

.selected-files ul {
  list-style: none;
  padding: 0;
  margin: 0.5rem 0;
}

.selected-files li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem;
  background: white;
  border: 1px solid #e6f2ff;
  border-radius: 4px;
  margin-bottom: 0.5rem;
}

.remove-file-btn {
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 1rem;
  padding: 0;
}

.remove-file-btn:hover {
  background: #dc2626;
}

/* Responsive styles */
@media (max-width: 768px) {
  .header {
    flex-wrap: nowrap;
    padding: 10px 15px;
    height: 80px;
    align-items: center;
  }

  .sidebar-toggle {
    display: block;
    margin-right: 10px;
  }

  .logo {
    width: 40px;
    margin-right: 15px;
    margin-left: 0;
    margin-top: 0;
  }

  .button-group {
    display: flex;
    flex-direction: row;
    gap: 10px;
    margin-left: 0;
    align-items: center;
  }

  .button-group button {
    padding: 8px 12px;
    font-size: 13px;
    white-space: nowrap;
  }

  .main-content {
    margin-left: 0;
    padding: 15px;
  }

  .sidebar {
    left: -220px;
  }

  .sidebar-open {
    left: 0;
  }

  .content {
    padding: 20px;
  }

  .form-container {
    padding: 15px;
  }

  .button-group {
    flex-direction: column;
  }

  .action-btn {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .header {
    padding: 10px;
    height: 70px;
  }

  .logo {
    width: 35px;
    margin-right: 10px;
  }

  .button-group {
    gap: 5px;
  }

  .button-group button {
    padding: 6px 10px;
    font-size: 12px;
  }

  .content {
    padding: 15px;
  }

  .title {
    font-size: 1.2rem;
  }
}

.thesis-form {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 130, 198, 0.1);
  margin-top: 2rem;
}

.form-section {
  max-width: 800px;
  margin: 0 auto;
}

.form-section h3 {
  color: #0082c6;
  margin-bottom: 1.5rem;
  font-size: 1.2rem;
}

.member-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.member-item {
  background: #f8fafc;
  padding: 1rem;
  border-radius: 8px;
  border: 1px solid #e6f2ff;
}

.member-inputs {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.member-inputs input,
.member-inputs select {
  flex: 1;
}

.remove-member-btn {
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 1.2rem;
  padding: 0;
}

.remove-member-btn:hover {
  background: #dc2626;
}

.add-member-btn {
  background: #0082c6;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 0.75rem 1.5rem;
  cursor: pointer;
  font-weight: 600;
  margin-top: 1rem;
  transition: all 0.3s ease;
}

.add-member-btn:hover {
  background: #0069a3;
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Responsive styles */
@media (max-width: 768px) {
  .member-inputs {
    flex-direction: column;
    gap: 0.5rem;
  }

  .member-inputs input,
  .member-inputs select {
    width: 100%;
  }

  .remove-member-btn {
    width: 28px;
    height: 28px;
    font-size: 1rem;
  }
}

/* Modal styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 1000px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e6f2ff;
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
  color: #666;
}

.modal-body {
  padding: 1.5rem;
}

.thesis-info {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.info-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.info-item label {
  font-weight: 600;
  color: #1a3c5e;
}

.members-section,
.documents-section {
  margin-top: 1rem;
}

.members-table,
.documents-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

.members-table th,
.members-table td,
.documents-table th,
.documents-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #e6f2ff;
}

.members-table th,
.documents-table th {
  background: #f8fafc;
  font-weight: 600;
  color: #1a3c5e;
}

.status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.9rem;
  display: inline-block;
}

.document-link {
  color: #0082c6;
  text-decoration: none;
  font-weight: 600;
}

.document-link:hover {
  text-decoration: underline;
}

.status-pending {
  background: #fef3c7;
  color: #92400e;
}

.status-submitted {
  background: #d1fae5;
  color: #065f46;
}

.status-processing {
  background: #dbeafe;
  color: #1e40af;
}

.status-need-update {
  background: #fee2e2;
  color: #991b1b;
}

.status-approved {
  background: #dcfce7;
  color: #166534;
}

.no-documents {
  text-align: center;
  color: #666;
  padding: 2rem;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px dashed #e6f2ff;
  margin-top: 1rem;
}

@media (max-width: 768px) {
  .modal-content {
    width: 95%;
    margin: 1rem;
  }

  .info-section {
    grid-template-columns: 1fr;
  }

  .members-table,
  .documents-table {
    display: block;
    overflow-x: auto;
  }
}
</style>


