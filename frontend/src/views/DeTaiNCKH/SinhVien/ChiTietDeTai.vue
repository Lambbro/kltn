<template>
  <div class="container">
    <header class="header">
      <img src="@/assets/img/logo-hou.png" alt="Logo" class="logo" />
      <div class="button-group">
        <button class="active" @click="$router.push('/de-tai-nckh')">Tổng hợp đề tài</button>
        <button class="active" @click="handleDangThucHienClick">Đề tài đang thực hiện</button>
      </div>
    </header>

    <div class="main-layout">
      <SidebarHome class="sidebar" />
      <div class="main-content">
        <div class="research-detail">
          <h2>Chi tiết đề tài </h2>
          <div v-if="loading" class="loading">
            <p>Đang tải dữ liệu...</p>
          </div>
          <div v-else-if="research" class="research-item">
            <img src="@/assets/img/logo-hou.png" alt="Logo" class="research-logo" />
            <div class="research-info">
              <div class="info-section">
                <h3>Thông tin cơ bản</h3>
                <p><strong>Mã đề tài:</strong> {{ research.ma_de_tai }}</p>
                <p><strong>Tên đề tài:</strong> {{ research.ten_de_tai }}</p>
                <p><strong>Đợt thực hiện:</strong> {{ research.dot_thuc_hien }}</p>
                <p><strong>Hướng nghiên cứu:</strong> 
                    <ul class="research-directions">
                        <li v-for="direction in research.huong_nghien_cuu" :key="direction.ma_hnc">
                            {{ direction.ten_hnc }}
                        </li>
                    </ul>
                </p>
                <p><strong>Trạng thái:</strong> 
                  <span :class="getStatusClass(research.trang_thai)">
                    {{ getStatusText(research.trang_thai) }}
                  </span>
                </p>
              </div>

              <div class="info-section">
                <h3>Giảng viên hướng dẫn</h3>
                <p><strong>Tên giảng viên:</strong> {{ research.ten_gv }}</p>
                <p><strong>Mã giảng viên:</strong> {{ research.ma_gv }}</p>
                <router-link :to="'/info?ma_gv=' + research.ma_gv" class="view-details-btn">
                  <i class="fas fa-user"></i> Xem chi tiết giảng viên
                </router-link>
              </div>

              <div class="info-section">
                <h3>Thành viên nhóm</h3>
                <div v-for="member in research.thanh_vien" :key="member.ma_sv" class="member-item">
                  <p><strong>Mã sinh viên:</strong> {{ member.ma_sv }}</p>
                  <p><strong>Tên sinh viên:</strong> {{ member.ten_sv }}</p>
                  <router-link :to="'/info-students?ma_sv=' + member.ma_sv" class="view-details-btn">
                    <i class="fas fa-user-graduate"></i> Xem chi tiết sinh viên
                  </router-link>
                </div>
              </div>

              <div class="info-section">
                <h3>Tài liệu đề tài</h3>
                <div class="document-tabs">
                  <button 
                    v-for="tab in documentTabs" 
                    :key="tab.id"
                    :class="['tab-button', { active: activeTab === tab.id }]"
                    @click="activeTab = tab.id"
                  >
                    {{ tab.name }}
                  </button>
                </div>
                <div class="document-content">
                  <div v-if="groupedDocuments[activeTab]?.length">
                    <div v-for="(group, index) in groupedDocuments[activeTab]" :key="index" class="document-group">
                      <div class="submission-header">
                        <h4>{{ group.name }}</h4>
                        <div class="submission-info">
                          <span class="status" :class="{ 
                            'status-submitted': group.trang_thai === 1,
                            'status-needs-update': group.trang_thai === 3 || group.trang_thai === 7
                          }">
                            {{ group.trang_thai === 1 ? 'Đã nộp' : 
                               group.trang_thai === 3 || group.trang_thai === 7 ? 'Cần cập nhật' : 'Chưa nộp' }}
                          </span>
                          <span v-if="group.phan_hoi" class="submission-feedback">
                            Phản hồi: {{ group.phan_hoi }}
                          </span>
                        </div>
                      </div>
                      <div class="files-list">
                        <div v-for="(file, fileIndex) in group.files" :key="fileIndex" class="file-item">
                          <div class="file-actions">
                            <div class="file-info">
                              <i :class="getFileIcon(file.link_tep)"></i>
                              <span class="file-name">{{ getFileName(file.link_tep) }}</span>
                            </div>
                            <div class="action-buttons">
                              <button @click="previewFile(file.link_tep)" class="action-btn" title="Xem trước">
                                <i class="fas fa-eye"></i>
                              </button>
                              <button @click="downloadFile(file.link_tep)" class="action-btn" title="Tải xuống">
                                <i class="fas fa-download"></i>
                              </button>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div v-else class="no-documents">
                    Không có tài liệu nào cho loại này.
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="not-found">
            <p>Không tìm thấy đề tài</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Preview Modal -->
    <div v-if="showPreview" class="preview-modal">
      <div class="preview-content">
        <div class="preview-header">
          <h3>Xem trước tài liệu</h3>
          <button @click="closePreview" class="close-btn">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="preview-body">
          <iframe v-if="previewUrl" :src="previewUrl" frameborder="0"></iframe>
          <div v-else class="preview-error">
            Không thể xem trước tài liệu này. Vui lòng tải xuống để xem.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import SidebarHome from '@/components/SidebarHome.vue';
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import api from '@/config/api';
import { saveAs } from 'file-saver';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const research = ref(null);
const loading = ref(true);

// Document tabs
const activeTab = ref('outline');
const documentTabs = [
  { id: 'outline', name: 'Đề cương đề tài' },
  { id: 'faculty', name: 'Báo cáo cấp khoa' },
  { id: 'school', name: 'Báo cáo cấp trường' }
];

const showPreview = ref(false);
const previewUrl = ref('');

// Hàm lấy trạng thái
function getStatusText(status) {
  switch (status) {
    case 0: return 'Đã hủy';
    case 1: return 'Đang thực hiện';
    case 2: return 'Hoàn thành';
    default: return 'Không xác định';
  }
}

// Hàm lấy class trạng thái
function getStatusClass(status) {
  switch (status) {
    case 0: return 'status-pending';
    case 1: return 'status-in-progress';
    case 2: return 'status-completed';
    default: return 'status-unknown';
  }
}

// Hàm xử lý click vào nút "Đề tài đang thực hiện"
function handleDangThucHienClick() {
  if (!authStore.user) {
    router.push('/login');
    return;
  }

  if (authStore.user.quyen_han === 3) {
    router.push('/de-tai-dang-thuc-hien-gv');
  } else if (authStore.user.quyen_han === 4) {
    router.push('/de-tai-dang-thuc-hien-sinh-vien');
  }
}

// Computed: Group documents by submission time
const groupedDocuments = computed(() => {
  if (!research.value?.tai_lieu) {
    return {
      outline: [],
      faculty: [],
      school: []
    };
  }

  const typeMap = {
    outline: [1, 2], // Đề cương đề tài và chỉnh sửa
    faculty: [3, 4], // Báo cáo cấp khoa và chỉnh sửa
    school: [5, 6]   // Báo cáo cấp trường và chỉnh sửa
  };

  // Initialize result
  const result = {
    outline: [],
    faculty: [],
    school: []
  };

  // Group documents by thoi_gian_nop
  const groupsByTime = {};
  research.value.tai_lieu.forEach(doc => {
    const tabId = Object.keys(typeMap).find(tab => typeMap[tab].includes(doc.loai_tai_lieu));
    if (!tabId) return; // Skip if loai_tai_lieu doesn't match any tab

    const timeKey = doc.thoi_gian_nop;
    if (!groupsByTime[tabId]) groupsByTime[tabId] = {};
    if (!groupsByTime[tabId][timeKey]) {
      groupsByTime[tabId][timeKey] = {
        name: getDocumentType(doc.loai_tai_lieu),
        thoi_gian_nop: doc.thoi_gian_nop,
        trang_thai: doc.trang_thai,
        phan_hoi: doc.phan_hoi,
        files: []
      };
    }

    groupsByTime[tabId][timeKey].files.push({
      link_tep: doc.link_tep
    });

    // Update trang_thai and phan_hoi if this document has higher priority
    if (doc.trang_thai === 3 || doc.trang_thai === 7) {
      groupsByTime[tabId][timeKey].trang_thai = doc.trang_thai;
      groupsByTime[tabId][timeKey].phan_hoi = doc.phan_hoi;
    }
  });

  // Convert groups to arrays
  for (const tabId in groupsByTime) {
    result[tabId] = Object.values(groupsByTime[tabId]).sort((a, b) => 
      new Date(b.thoi_gian_nop) - new Date(a.thoi_gian_nop)
    );
  }

  return result;
});

// Helper functions
function getDocumentType(type) {
  switch (type) {
    case 1: return 'Đề cương đề tài';
    case 2: return 'Đề cương chỉnh sửa';
    case 3: return 'Báo cáo cấp khoa';
    case 4: return 'Báo cáo cấp khoa chỉnh sửa';
    case 5: return 'Báo cáo cấp trường';
    case 6: return 'Báo cáo cấp trường chỉnh sửa';
    default: return `Tài liệu khác (${type})`;
  }
}

function formatDate(dateString) {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleString('vi-VN');
}

function getFileIcon(filePath) {
  const extension = filePath.split('.').pop().toLowerCase();
  switch (extension) {
    case 'pdf':
      return 'fas fa-file-pdf';
    case 'docx':
    case 'doc':
      return 'fas fa-file-word';
    case 'pptx':
    case 'ppt':
      return 'fas fa-file-powerpoint';
    default:
      return 'fas fa-file';
  }
}
// Hàm lấy tên file từ URL
const getFileName = (fileUrl) => {
  try {
    if (!fileUrl || typeof fileUrl !== 'string') {
      return 'downloaded_file';
    }
    const urlParts = fileUrl.split('/');
    let fileName = urlParts[urlParts.length - 1];
    // Loại bỏ query parameters nếu có
    fileName = fileName.split('?')[0];
    return fileName || 'downloaded_file';
  } catch (error) {
    console.error('Error extracting file name:', error);
    return 'downloaded_file';
  }
};

// Hàm tải file
const downloadFile = async (fileUrl) => {
  try {
    if (!fileUrl || typeof fileUrl !== 'string') {
      throw new Error('Invalid file URL');
    }

    const fileName = getFileName(fileUrl);
    const response = await fetch(fileUrl, {
      method: 'GET',
      headers: {
        'Accept': 'application/octet-stream',
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch file: ${response.status} ${response.statusText}`);
    }

    const blob = await response.blob();
    // Sử dụng file-saver để tải file
    saveAs(blob, fileName);
  } catch (error) {
    console.error('Error downloading file:', error);
    let errorMessage = 'Không thể tải file. ';
    if (error.message.includes('NetworkError') || error.message.includes('Failed to fetch')) {
      errorMessage += 'Kiểm tra kết nối mạng hoặc quyền truy cập file.';
    } else {
      errorMessage += 'Vui lòng thử lại sau.';
    }
    alert(errorMessage);
  }
};

// Hàm xem trước file
const previewFile = async (fileUrl) => {
  try {
    if (!fileUrl || typeof fileUrl !== 'string') {
      throw new Error('Invalid file URL');
    }

    const fileExtension = fileUrl.split('.').pop().toLowerCase();
    const previewableExtensions = ['pdf', 'docx', 'doc', 'pptx', 'ppt'];

    if (previewableExtensions.includes(fileExtension)) {
      let url = '';

      if (fileExtension === 'pdf') {
        // Kiểm tra truy cập file PDF
        const response = await fetch(fileUrl, { method: 'HEAD' });
        if (!response.ok) {
          throw new Error(`Cannot access PDF file: ${response.status} ${response.statusText}`);
        }
        url = fileUrl;
      } else if (['docx', 'doc', 'pptx', 'ppt'].includes(fileExtension)) {
        // Sử dụng Microsoft Office Viewer
        url = `https://view.officeapps.live.com/op/embed.aspx?src=${encodeURIComponent(fileUrl)}`;
      }

      if (url) {
        // Hiển thị trong modal thay vì mở tab mới
        previewUrl.value = url;
        showPreview.value = true;
      } else {
        throw new Error('No preview URL generated');
      }
    } else {
      // Nếu không hỗ trợ xem trước, thông báo và tải file
      alert('Định dạng file không hỗ trợ xem trước. Đang tải xuống...');
      await downloadFile(fileUrl);
    }
  } catch (error) {
    console.error('Error previewing file:', error);
    let errorMessage = 'Không thể xem trước file. ';
    if (error.message.includes('NetworkError') || error.message.includes('Failed to fetch')) {
      errorMessage += 'Kiểm tra kết nối mạng hoặc quyền truy cập file.';
    } else if (error.message.includes('Cannot access')) {
      errorMessage += 'File không thể truy cập.';
    } else {
      errorMessage += 'Đang thử tải xuống...';
    }
    alert(errorMessage);
    await downloadFile(fileUrl);
  }
};

// Hàm đóng modal preview
const closePreview = () => {
  showPreview.value = false;
  previewUrl.value = '';
};
// Fetch research details
const fetchResearchDetails = async () => {
  try {
    loading.value = true;
    const response = await api.get(`get_data/detai_sv_mdt/dang_thuc_hien/${route.params.id}`);
    research.value = response.data;
    console.log('Research details:', research.value);
  } catch (error) {
    console.error('Error fetching research details:', error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchResearchDetails();
});
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: #f8fafc;
}
.header {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  background: linear-gradient(135deg, #0082c6 100%, #0069a3 100%);
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

.button-group {
  display: flex;
  gap: 15px;
  align-items: center;
  margin-left: 120px;
  position: relative;
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
  color: #ffffff;
}

.button-group button.active:hover {
  background: #0069a3;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.main-layout {
  display: flex;
  margin-top: 80px;
  min-height: calc(100vh - 80px);
}

.sidebar {
  width: 220px;
  background: linear-gradient(180deg, #0082c6 0%, #0069a3 100%);
  position: fixed;
  left: 0;
  height: calc(100vh - 80px);
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  z-index: 999;
  padding-top: 20px;
}

.sidebar ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar li {
  padding: 0;
  position: relative;
}

.sidebar li::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 20px;
  right: 20px;
  height: 1px;
  background: rgba(255, 255, 255, 0.1);
}

.sidebar li:last-child::after {
  display: none;
}

.sidebar a {
  display: block;
  padding: 15px 20px;
  color: white;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
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
  background: rgba(255, 255, 255, 0.1);
  transform: translateX(5px);
}

.sidebar a:hover::before {
  transform: translateX(0);
}

.sidebar a.router-link-active {
  background: rgba(255, 255, 255, 0.2);
  font-weight: 600;
}

.main-content {
  flex: 1;
  margin-left: 220px;
  padding: 20px 40px;
  background: #f8fafc;
  min-height: calc(100vh - 80px);
}

.research-detail {
  margin: 0 auto;
  max-width: 1200px;
  padding: 20px;
}

.research-detail h2 {
  color: #0082c6;
  font-size: 28px;
  margin-bottom: 30px;
  padding-bottom: 15px;
  border-bottom: 2px solid #e6f2ff;
  text-align: center;
}

.research-item {
  display: flex;
  align-items: flex-start;
  gap: 30px;
  padding: 30px;
  border: 1px solid #e2e8f0;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 130, 198, 0.1);
  transition: all 0.3s ease;
}

.research-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(0, 130, 198, 0.15);
}

.research-logo {
  width: 100px;
  height: 120px;
  object-fit: contain;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 10px;
  background: white;
}

.research-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.info-section {
  background: #f8fafc;
  padding: 20px;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
}

.info-section:hover {
  border-color: #0082c6;
  box-shadow: 0 4px 15px rgba(0, 130, 198, 0.1);
}

.info-section h3 {
  color: #0082c6;
  font-size: 18px;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 2px solid #e6f2ff;
}

.info-section p {
  margin: 12px 0;
  color: #334155;
  font-size: 15px;
  line-height: 1.6;
}

.info-section p strong {
  color: #0082c6;
  font-weight: 600;
  min-width: 150px;
  display: inline-block;
}

.member-item {
  padding: 15px;
  background: white;
  border-radius: 8px;
  margin-bottom: 12px;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
  position: relative;
  padding-bottom: 15px;
}

.member-item:hover {
  transform: translateX(5px);
  border-color: #0082c6;
  box-shadow: 0 2px 8px rgba(0, 130, 198, 0.1);
}

.document-tabs {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  border-bottom: 2px solid #e6f2ff;
  padding-bottom: 5px;
}

.tab-button {
  padding: 10px 20px;
  border: none;
  background: #e2e8f0;
  color: #64748b;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.3s ease;
  font-weight: 500;
}

.tab-button:hover {
  background: #cbd5e1;
  transform: translateY(-2px);
}

.tab-button.active {
  background: #0082c6;
  color: white;
  box-shadow: 0 4px 12px rgba(0, 130, 198, 0.2);
}

.document-content {
  background: white;
  padding: 20px;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.document-group {
  margin-bottom: 25px;
  padding: 20px;
  background: #f8fafc;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
}

.document-group:hover {
  border-color: #0082c6;
  box-shadow: 0 4px 15px rgba(0, 130, 198, 0.1);
}

.submission-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 2px solid #e6f2ff;
}

.submission-header h4 {
  color: #0082c6;
  margin: 0;
  font-size: 16px;
}

.submission-info {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 8px;
}

.status {
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 500;
}

.status-submitted {
  background: #dcfce7;
  color: #16a34a;
}

.status-needs-update {
  background: #fef3c7;
  color: #d97706;
}

.submission-feedback {
  font-size: 0.9rem;
  color: #64748b;
  background: #f1f5f9;
  padding: 8px 12px;
  border-radius: 6px;
  max-width: 300px;
}

.files-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.file-item {
  padding: 12px;
  background: white;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
}

.file-item:hover {
  border-color: #0082c6;
  transform: translateX(5px);
}

.file-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.file-name {
  color: #0082c6;
  font-weight: 500;
}

.file-info i {
  color: #64748b;
  font-size: 18px;
}

.file-info i.fa-file-pdf {
  color: #ef4444;
}

.file-info i.fa-file-word {
  color: #2563eb;
}

.file-info i.fa-file-powerpoint {
  color: #d97706;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.action-btn {
  background: none;
  border: none;
  color: #64748b;
  cursor: pointer;
  padding: 6px;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.action-btn:hover {
  background: #f1f5f9;
  color: #0082c6;
}

.no-documents {
  text-align: center;
  padding: 30px;
  color: #64748b;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px dashed #e2e8f0;
}

.loading {
  text-align: center;
  padding: 30px;
  color: #64748b;
  font-size: 16px;
}

.not-found {
  text-align: center;
  padding: 30px;
  color: #ef4444;
  background: #fef2f2;
  border-radius: 8px;
  border: 1px solid #fee2e2;
}

/* Status classes */
.status-pending {
  color: #f59e0b;
  font-weight: 600;
  background: #fef3c7;
  padding: 4px 8px;
  border-radius: 4px;
}

.status-in-progress {
  color: #0082c6;
  font-weight: 600;
  background: #e6f2ff;
  padding: 4px 8px;
  border-radius: 4px;
}

.status-completed {
  color: #10b981;
  font-weight: 600;
  background: #dcfce7;
  padding: 4px 8px;
  border-radius: 4px;
}

.status-unknown {
  color: #64748b;
  font-weight: 600;
  background: #f1f5f9;
  padding: 4px 8px;
  border-radius: 4px;
}

/* Responsive styles */
@media (max-width: 1024px) {
  .research-detail {
    padding: 15px;
  }

  .research-item {
    padding: 20px;
    gap: 20px;
  }

  .research-logo {
    width: 80px;
    height: 100px;
  }
}

@media (max-width: 768px) {
  .research-item {
    flex-direction: column;
    align-items: center;
  }

  .research-logo {
    width: 70px;
    height: 90px;
  }

  .info-section {
    padding: 15px;
  }

  .document-tabs {
    flex-wrap: wrap;
  }

  .tab-button {
    padding: 8px 16px;
    font-size: 14px;
  }
}

@media (max-width: 480px) {
  .research-detail h2 {
    font-size: 24px;
  }

  .info-section h3 {
    font-size: 16px;
  }

  .info-section p {
    font-size: 14px;
  }

  .submission-header {
    flex-direction: column;
    gap: 10px;
  }

  .submission-info {
    align-items: flex-start;
  }
}

.profile-link {
  color: #0082c6;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

.profile-link:hover {
  color: #0069a3;
  text-decoration: underline;
}

.view-details-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: #0082c6;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
  margin-top: 10px;
}

.view-details-btn:hover {
  background: #0069a3;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.view-details-btn i {
  font-size: 16px;
}

.file-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

/* Preview Modal Styles */
.preview-modal {
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

.preview-content {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 1200px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

.preview-header {
  padding: 16px 24px;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.preview-header h3 {
  margin: 0;
  color: #0082c6;
}

.close-btn {
  background: none;
  border: none;
  color: #64748b;
  cursor: pointer;
  font-size: 20px;
  padding: 4px;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: #f1f5f9;
  color: #0082c6;
}

.preview-body {
  flex: 1;
  padding: 24px;
  overflow: auto;
}

.preview-body iframe {
  width: 100%;
  height: 100%;
  min-height: 500px;
  border: none;
}

.preview-error {
  text-align: center;
  color: #64748b;
  padding: 20px;
}

.research-directions {
  list-style-type: disc;
  margin-left: 20px;
  margin-top: 10px;
  margin-bottom: 20px;
  padding-left: 150px;
}

.research-directions li {
  margin-bottom: 5px;
}

</style>