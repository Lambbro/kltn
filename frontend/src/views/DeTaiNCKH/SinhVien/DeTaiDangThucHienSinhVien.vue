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
                <div v-if="loading">Đang tải...</div>
                <div v-else-if="error">{{ error }}</div>
                <div v-else-if="!projectData">Không tìm thấy thông tin đề tài.</div>
                <div v-else class="project-details">
                    <div class="info-section">
                        <div class="info-card">
                            <div class="info-item">
                                <span class="info-label">Tên đề tài:</span>
                                <span class="info-value">{{ projectData.ten_de_tai }}</span>
                            </div>
                            <div class="info-item">
                                <span class="info-label">Tên giảng viên hướng dẫn:</span>
                                <span class="info-value">{{ projectData.ten_gv }}</span>
                            </div>
                            <div class="info-item">
                                <span class="info-label">Đợt thực hiện:</span>
                                <span class="info-value">2025</span>
                            </div>
                            <div class="info-item">
                                <span class="info-label">Thành viên:</span>
                                <div class="members-list">
                                    <div v-for="member in projectData.thanh_vien" :key="member.ma_sv" class="member-item">
                                        {{ member.ma_sv }} - {{ member.ten_sv }}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="submission-section">
                        <button 
                            class="submit-btn" 
                            :class="{ 'completed': isProposalSubmitted }"
                            @click="handleSubmitProposal"
                        >
                            Nộp đề cương đề tài nghiên cứu khoa học
                        </button>

                        <button 
                            class="submit-btn" 
                            :class="{ 'completed': isDepartmentReportSubmitted }"
                            @click="handleSubmitDepartmentReport"
                        >
                            Nộp báo cáo cấp khoa
                        </button>

                        <button 
                            class="submit-btn" 
                            :class="{ 'completed': isSchoolReportSubmitted }"
                            @click="handleSubmitSchoolReport"
                        >
                            Nộp báo cáo cấp trường
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import SidebarHome from '@/components/SidebarHome.vue';
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/config/api';

const router = useRouter();

const projectData = ref(null);
const loading = ref(true);
const error = ref(null);

// Thêm state cho sidebar mobile
const isSidebarOpen = ref(false);
const isMobile = ref(window.innerWidth <= 768);

// Thêm state cho trạng thái nộp
const isProposalSubmitted = ref(false);
const isDepartmentReportSubmitted = ref(false);
const isSchoolReportSubmitted = ref(false);
const isProposalEditSubmitted = ref(false);
const isDepartmentReportEditSubmitted = ref(false);
const isSchoolReportEditSubmitted = ref(false);

const toggleSidebar = () => {
    isSidebarOpen.value = !isSidebarOpen.value;
};

// Thêm event listener cho resize
window.addEventListener('resize', () => {
    isMobile.value = window.innerWidth <= 768;
    if (!isMobile.value && isSidebarOpen.value) {
        isSidebarOpen.value = false;
    }
});

const fetchProjectData = async () => {
    try {
        loading.value = true;
        const response = await api.get('sv/detai'); 
        projectData.value = response.data;
    } catch (err) {
        error.value = 'Không thể tải thông tin đề tài. Vui lòng thử lại sau.';
        console.error('Error fetching project data:', err);
    } finally {
        loading.value = false;
    }
};

const handleSubmitProposal = () => {
    router.push({
        path: '/qua-trinh-thuc-hien',
        query: { type: 1 } // 1: Đề Cương
    });
};

const handleSubmitProposalEdit = () => {
    router.push({
        path: '/qua-trinh-thuc-hien',
        query: { type: 2 } // 2: Đề cương chỉnh sửa
    });
};

const handleSubmitDepartmentReport = () => {
    router.push({
        path: '/qua-trinh-thuc-hien',
        query: { type: 3 } // 3: Báo cáo cấp khoa
    });
};

const handleSubmitDepartmentReportEdit = () => {
    router.push({
        path: '/qua-trinh-thuc-hien',
        query: { type: 4 } // 4: Báo cáo cấp khoa chỉnh sửa
    });
};

const handleSubmitSchoolReport = () => {
    router.push({
        path: '/qua-trinh-thuc-hien',
        query: { type: 5 } // 5: Báo cáo cấp trường
    });
};

const handleSubmitSchoolReportEdit = () => {
    router.push({
        path: '/qua-trinh-thuc-hien',
        query: { type: 6 } // 6: Báo cáo cấp trường chỉnh sửa
    });
};

onMounted(() => {
    fetchProjectData();
});

</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  overflow-y: auto;
  background-color: #f0f7ff;
  max-width: 1280px;
  margin: 0 auto;
}

.container::-webkit-scrollbar {
  width: 8px;
}

.container::-webkit-scrollbar-track {
  background: #e6f2ff;
  border-radius: 10px;
}

.container::-webkit-scrollbar-thumb {
  background: linear-gradient(to bottom, #0082c6, #0069a3);
  border-radius: 10px;
}

.container::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(to bottom, #0069a3, #005a8c);
}

/* Header */
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

/* Main layout */
.main-layout {
  display: flex;
  margin-top: 100px; /* Khoảng cách với header */
  min-height: calc(100vh - 100px);
  gap: 20px;
  width: 100%;
  position: relative;
}

/* Sidebar */
.sidebar {
  width: 220px;
  background: linear-gradient(180deg, #0082c6 0%, #0069a3 100%);
  position: fixed;
  top: 80px; /* Bắt đầu dưới header */
  left: 0;
  height: calc(100vh - 80px); /* Trừ header */
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  z-index: 999;
}

/* Main content */
.main-content {
  flex: 1;
  padding-left: 20px;
  padding-right: 20px;
  background: #f0f7ff;
  width: calc(100% - 240px);
  box-sizing: border-box;
  margin-left: 220px;
  transition: all 0.3s ease;
}

.project-details {
  background: white;
  padding: 30px;
  border-radius: 16px;
  box-shadow: 0 8px 30px rgba(0, 130, 198, 0.1);
  border: 1px solid rgba(0, 130, 198, 0.1);
  transition: all 0.3s ease;
}

.project-details:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(0, 130, 198, 0.15);
}

.info-section {
  margin-bottom: 2rem;
}

.info-card {
  background: white;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 130, 198, 0.1);
  border: 1px solid rgba(0, 130, 198, 0.1);
}

.info-item {
  display: flex;
  flex-direction: column;
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid rgba(0, 130, 198, 0.1);
}

.info-item:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.info-label {
  font-weight: 600;
  color: #0082c6;
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
}

.info-value {
  color: #1a3c5e;
  font-size: 1rem;
  line-height: 1.5;
}

.members-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.member-item {
  padding: 0.75rem;
  background: #f8fafc;
  border: 1px solid #e6f2ff;
  border-radius: 6px;
  transition: all 0.3s ease;
}

.member-item:hover {
  background: #f0f7ff;
  border-color: #0082c6;
  transform: translateX(5px);
}

.submission-section {
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
    margin-top: 2.5rem;
}

.submission-group {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    margin-bottom: 1.5rem;
}

.submit-btn {
    width: 100%;
    padding: 1rem 1.5rem;
    background: white;
    color: #0082c6;
    border: 2px solid #0082c6;
    border-radius: 8px;
    cursor: pointer;
    font-size: 1rem;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 130, 198, 0.1);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.submit-btn.edit-btn {
    background: #f0f7ff;
    color: #0069a3;
    border-color: #0069a3;
}

.submit-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 130, 198, 0.2);
    background: #f0f7ff;
}

.submit-btn.edit-btn:hover {
    background: #e6f2ff;
}

.submit-btn.completed {
    background: #10b981;
    color: white;
    border-color: #10b981;
    cursor: default;
}

.submit-btn.completed:hover {
    transform: none;
    background: #10b981;
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2);
}

/* Overlay cho mobile */
.overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    z-index: 998;
}

/* Sidebar toggle button */
.sidebar-toggle {
    display: none;
    background: #0082c6;
    color: white;
    border: none;
    padding: 0.5rem 0.8rem;
    font-size: 1.2rem;
    cursor: pointer;
    border-radius: 5px;
    margin-right: 1rem;
}

.sidebar-toggle:hover {
    background: #0069a3;
}

/* Responsive */
@media (max-width: 1024px) {
  .header {
    padding: 10px 20px;
  }

  .main-content {
    margin-left: 220px;
    width: calc(100% - 220px);
    padding: 20px;
  }

  .sidebar {
    width: 200px;
  }
}

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

  .main-layout {
    margin-top: 80px;
    min-height: calc(100vh - 80px);
  }

  .sidebar {
    width: 200px;
    left: -200px;
    top: 80px;
    height: calc(100vh - 80px);
  }

  .sidebar-open {
    left: 0;
  }

  .main-content {
    margin-left: 0;
    width: 100%;
    padding: 15px;
    margin-top: 0;
  }

  .project-details {
    padding: 15px;
  }

  .submit-btn {
    padding: 0.9rem 1.2rem;
    font-size: 0.95rem;
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

  .main-layout {
    margin-top: 70px;
    min-height: calc(100vh - 70px);
  }

  .sidebar {
    width: 180px;
    left: -180px;
    top: 70px;
    height: calc(100vh - 70px);
  }

  .main-content {
    padding: 10px;
  }

  .project-details {
    padding: 10px;
  }

  .info-card {
    padding: 15px;
  }

  .info-item {
    margin-bottom: 1rem;
    padding-bottom: 1rem;
  }

  .info-label {
    font-size: 0.95rem;
  }

  .info-value {
    font-size: 0.9rem;
  }

  .member-item {
    padding: 0.5rem;
    font-size: 0.9rem;
  }

  .submit-btn {
    padding: 0.8rem 1rem;
    font-size: 0.85rem;
  }
}
</style>