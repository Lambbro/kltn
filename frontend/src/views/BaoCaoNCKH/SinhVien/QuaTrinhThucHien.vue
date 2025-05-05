<template>
  <div class="container">
    <header class="header">
      <button v-if="isMobile" class="sidebar-toggle" @click="toggleSidebar">☰</button>
      <img src="@/assets/img/logo-hou.png" alt="Logo" class="logo"/>
      <div class="button-group">
        <button class="active" @click="$router.push(`/de-tai-nckh`)">Tổng hợp đề tài</button>
        <button class="active" @click="$router.push(`/de-tai-dang-thuc-hien-sinh-vien`)">Đề tài đang thực hiện</button>
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

            <!-- Submission Details Box -->
            <div class="submission-box" :class="{ 'submitted': isSubmitted }">
              <div class="submission-header">
                <h3>Trạng thái nộp bài</h3>
                <div class="status-checkbox">
                  <input type="checkbox" :checked="isSubmitted" disabled />
                  <span class="status-text">{{ getStatusText }}</span>
                </div>
              </div>

              <div class="submission-details">
                <div class="form-group">
                  <label>Thời gian lần nộp cuối:</label>
                  <input type="text" :value="lastSubmissionTime" class="form-input" readonly />
                </div>

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
                  <div v-if="currentDocument" class="submitted-file">
                    <p>File đã nộp:
                      <a :href="currentDocument.link_tep" target="_blank" class="file-link">
                        {{ getFileName(currentDocument.link_tep) }}
                      </a>
                    </p>
                  </div>
                  <p class="file-note">Lưu ý: Chỉ nộp báo cáo dưới dạng pdf, doc, docx, pptx</p>
                </div>

                <div class="form-group">
                  <label>Ý kiến:</label>
                  <input type="text" v-model="getFeedback" class="form-input" />
                </div>

                <div class="button-group">
                  <button class="action-btn submit" @click="handleSubmit">Nộp bài</button>
                  <button class="action-btn history" @click="showHistory = true">Lịch sử bài nộp</button>
                </div>
              </div>
            </div>

            <!-- Submission History Table -->
            <div v-if="showHistory" class="history-section">
              <h3>Lịch sử nộp bài</h3>
              <table class="history-table">
                <thead>
                  <tr>
                    <th>STT</th>
                    <th>Tên đề tài</th>
                    <th>Ngày nộp</th>
                    <th>Files nộp</th>
                    <th>Trạng thái</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(submission, index) in groupedSubmissionHistory" :key="index">
                    <td>{{ index + 1 }}</td>
                    <td>{{ projectData.ten_de_tai }}</td>
                    <td>{{ formatDate(submission.thoi_gian_nop) }}</td>
                    <td>
                      <div class="submitted-files-list">
                        <div v-for="(file, fileIndex) in submission.files" :key="fileIndex" class="file-item">
                          <a :href="file.link_tep" target="_blank" class="file-link">
                            {{ getFileName(file.link_tep) }}
                          </a>
                        </div>
                      </div>
                    </td>
                    <td :class="{ 'status-success': submission.trang_thai === 1 }">
                      {{ getStatusTextForHistory(submission.trang_thai) }}
                    </td>
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
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRoute } from 'vue-router';
import SidebarHome from '@/components/SidebarHome.vue';
import api from '@/config/api';

const route = useRoute();
const isSidebarOpen = ref(false);
const isMobile = ref(window.innerWidth <= 768);
const selectedFiles = ref([]);
const showHistory = ref(false);

// Project data structure
const projectData = ref({
  ten_de_tai: '',
  ma_de_tai: '',
  tai_lieu: [],
});

// Computed properties
const latestDocument = computed(() => {
  if (!projectData.value.tai_lieu) return null;
  const documents = projectData.value.tai_lieu.filter(doc => doc.loai_tai_lieu === Number(route.query.type));
  if (documents.length === 0) return null;
  
  // Sắp xếp theo thời gian nộp và lấy tài liệu mới nhất
  return documents.sort((a, b) => new Date(b.thoi_gian_nop) - new Date(a.thoi_gian_nop))[0];
});

const currentDocument = computed(() => {
  if (!projectData.value.tai_lieu) return null;
  const documents = projectData.value.tai_lieu.filter(doc => doc.loai_tai_lieu === Number(route.query.type));
  if (documents.length === 0) return null;
  
  // Sắp xếp theo thời gian nộp và lấy tài liệu mới nhất
  return documents.sort((a, b) => new Date(b.thoi_gian_nop) - new Date(a.thoi_gian_nop))[0];
});

const isSubmitted = computed(() => {
  if (!currentDocument.value) return false;
  return currentDocument.value.trang_thai === 1 || 
         currentDocument.value.trang_thai === 4 || 
         currentDocument.value.trang_thai === 6 || 
         currentDocument.value.trang_thai === 8;
});

const needsUpdate = computed(() => {
  if (!currentDocument.value) return false;
  return currentDocument.value.trang_thai === 3 || 
         currentDocument.value.trang_thai === 7;
});

const getStatusText = computed(() => {
  if (!currentDocument.value) return 'Chưa nộp';
  switch (currentDocument.value.trang_thai) {
    case 1:
      return 'Đã nộp';
    case 3:
      return 'Cần cập nhật';
    case 4:
      return 'Đã cập nhật';
    case 6:
      return 'Đã nộp chỉnh sửa';
    case 7:
      return 'Cần cập nhật chỉnh sửa';
    case 8:
      return 'Đã cập nhật chỉnh sửa';
    default:
      return 'Chưa nộp';
  }
});

const getFeedback = computed(() => {
  return currentDocument.value?.phan_hoi || '';
});

const lastSubmissionTime = computed(() => {
  if (!currentDocument.value?.thoi_gian_nop) return 'Chưa nộp';
  return formatDate(currentDocument.value.thoi_gian_nop);
});

const submissionHistory = computed(() => {
  if (!projectData.value.tai_lieu) return [];
  return projectData.value.tai_lieu.filter(doc => doc.loai_tai_lieu === Number(route.query.type));
});

const submissionTitle = computed(() => {
  const type = route.query.type;
  if (!type) return 'Không xác định';
  switch (type) {
    case '1':
      return 'Nộp đề cương đề tài nghiên cứu khoa học';
    case '3':
      return 'Nộp báo cáo cấp khoa';
    case '5':
      return 'Nộp báo cáo cấp trường';
    default:
      return 'Không xác định';
  }
});

// Thêm computed property để nhóm các bài nộp
const groupedSubmissionHistory = computed(() => {
  if (!projectData.value.tai_lieu) return [];
  
  // Lọc các tài liệu theo loại
  const submissions = projectData.value.tai_lieu.filter(doc => doc.loai_tai_lieu === Number(route.query.type));
  
  // Nhóm các tài liệu theo thời gian nộp
  const groupedByTime = submissions.reduce((acc, submission) => {
    const timeKey = submission.thoi_gian_nop;
    if (!acc[timeKey]) {
      acc[timeKey] = {
        thoi_gian_nop: submission.thoi_gian_nop,
        trang_thai: submission.trang_thai,
        files: []
      };
    }
    acc[timeKey].files.push(submission);
    return acc;
  }, {});

  // Chuyển đổi object thành array và sắp xếp theo thời gian
  return Object.values(groupedByTime).sort((a, b) => 
    new Date(b.thoi_gian_nop) - new Date(a.thoi_gian_nop)
  );
});

// Format date function
const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleString('vi-VN');
};

// Get file name from path
const getFileName = (path) => {
  if (!path) return '';
  return path.split('\\').pop();
};

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value;
};

// Fetch project data
const fetchProjectData = async () => {
  try {
    const response = await api.get('sv/detai');
    if (response.data && typeof response.data === 'object') {
      projectData.value = {
        ten_de_tai: response.data.ten_de_tai || '',
        ma_de_tai: response.data.ma_de_tai || '',
        tai_lieu: Array.isArray(response.data.tai_lieu) ? response.data.tai_lieu : [],
      };
    } else {
      throw new Error('Invalid API response structure');
    }
  } catch (error) {
    console.error('Error fetching project data:', error);
    alert('Không thể tải dữ liệu đề tài. Vui lòng thử lại sau.');
    projectData.value = { ten_de_tai: '', ma_de_tai: '', tai_lieu: [] };
  }
};

const handleFileChange = (event) => {
  const files = Array.from(event.target.files);
  const allowedTypes = [
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation',
  ];

  const validFiles = files.filter(file => {
    if (!allowedTypes.includes(file.type)) {
      alert(`File ${file.name} không đúng định dạng. Chỉ chấp nhận pdf, doc, docx hoặc pptx`);
      return false;
    }
    return true;
  });

  selectedFiles.value = [...selectedFiles.value, ...validFiles];
  event.target.value = ''; // Reset input to allow selecting the same file again
};

const removeFile = (index) => {
  selectedFiles.value.splice(index, 1);
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
      formData.append(`file_names[${index}]`, file.name);
      formData.append(`file_types[${index}]`, file.type);
    });

    const response = await api.post(
      `sv/upload/${projectData.value.ma_de_tai}/${route.query.type}`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );

    if (response.status === 200 || response.status === 201) {
      alert('Nộp bài thành công!');
      await fetchProjectData();
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

// Cập nhật phần hiển thị trạng thái trong bảng lịch sử
const getStatusTextForHistory = (status) => {
  switch (status) {
    case 1:
      return 'Đã nộp';
    case 3:
      return 'Cần cập nhật';
    case 4:
      return 'Đã cập nhật';
    case 6:
      return 'Đã nộp chỉnh sửa';
    case 7:
      return 'Cần cập nhật chỉnh sửa';
    case 8:
      return 'Đã cập nhật chỉnh sửa';
    default:
      return 'Chưa nộp';
  }
};

// Handle responsive sidebar
const handleResize = () => {
  isMobile.value = window.innerWidth <= 768;
  if (!isMobile.value && isSidebarOpen.value) {
    isSidebarOpen.value = false;
  }
};

onMounted(() => {
  window.addEventListener('resize', handleResize);
  handleResize();
  fetchProjectData();
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
</style>