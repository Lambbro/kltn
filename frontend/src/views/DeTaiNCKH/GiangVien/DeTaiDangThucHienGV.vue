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
                <div v-if="loading">Đang tải...</div>
                <div v-else-if="error">{{ error }}</div>
                <div v-else-if="!projects || projects.length === 0">Không có đề tài nào đang thực hiện.</div>
                <div v-else class="project-details">
                    <div class="info-section">
                        <div class="info-card">
                            <div class="info-item">
                                <span class="info-label">Tên đề tài:</span>
                                <span class="info-value">{{ projects[0].ten_de_tai }}</span>
                            </div>
                            <!-- <div class="info-item">
                                <span class="info-label">Mã đề tài:</span>
                                <span class="info-value">{{ projects[0].ma_de_tai }}</span>
                            </div> -->
                            <div class="info-item">
                                <span class="info-label">Vị trí tham gia:</span>
                                <span class="info-value">Chủ nhiệm</span>
                            </div>
                            <div class="info-item">
                                <span class="info-label">Trạng thái:</span>
                                <span class="info-value">{{ getStatusText(projects[0].trang_thai) }}</span>
                            </div>
                        </div>
                    </div>

                    <div class="submission-section">
                        <button 
                            class="submit-btn" 
                            :class="{ 'completed': projects[0].tai_lieu?.loai_tai_lieu === 1 }"
                            @click="handleSubmitThesis(projects[0])"
                        >
                            Nộp báo cáo thuyết minh
                        </button>

                        <button 
                            class="submit-btn" 
                            :class="{ 'completed': projects[0].tai_lieu?.loai_tai_lieu === 2 }"
                            @click="handleSubmitProgressReport(projects[0])"
                        >
                            Nộp báo cáo tiến độ đề tài
                        </button>

                        <button 
                            class="submit-btn" 
                            :class="{ 'completed': projects[0].tai_lieu?.loai_tai_lieu === 3 }"
                            @click="handleSubmitAcceptanceProposal(projects[0])"
                        >
                            Hồ sơ đề xuất nghiệm thu đề tài
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
import { useAuthStore } from '@/stores/auth';

const router = useRouter();

const projects = ref([]);
const loading = ref(true);
const error = ref(null);

// Thêm state cho sidebar mobile
const isSidebarOpen = ref(false);
const isMobile = ref(window.innerWidth <= 768);

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

// Hàm chuyển đổi trạng thái
const getStatusText = (trangThai) => {
    const trangThaiMap = {
        1: 'Đang thực hiện',
        2: 'Đã hoàn thành',
        3: 'Đã nghiệm thu',
        4: 'Đã hủy'
    };
    return trangThaiMap[trangThai] || 'Không xác định';
};

const fetchProjects = async () => {
    try {
        loading.value = true;
        error.value = null;
        const ma_gv = useAuthStore().user.email.split('@')[0];
        const response = await api.get(`detai_gv/de_tai_mgv/${ma_gv}`, {
            params: {
                trang_thai: 1,
                is_chu_nhiem: true
            }
        });
        projects.value = response.data;
        console.log(projects.value);
    } catch (err) {
        error.value = 'Không thể tải thông tin đề tài. Vui lòng thử lại sau.';
        console.error('Error fetching project data:', err);
    } finally {
        loading.value = false;
    }
};

const handleSubmitThesis = (project) => {
    router.push({
        path: '/qua-trinh-thuc-hien-gv',
        query: { 
            type: 1, // 1: Báo cáo thuyết minh
            projectId: project.ma_de_tai
        }
    });
};

const handleSubmitProgressReport = (project) => {
    router.push({
        path: '/qua-trinh-thuc-hien-gv',
        query: { 
            type: 2, // 2: Báo cáo tiến độ
            projectId: project.ma_de_tai
        }
    });
};

const handleSubmitAcceptanceProposal = (project) => {
    router.push({
        path: '/qua-trinh-thuc-hien-gv',
        query: { 
            type: 3, // 3: Hồ sơ đề xuất nghiệm thu
            projectId: project.ma_de_tai
        }
    });
};

onMounted(() => {
    fetchProjects();
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

.submission-section {
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
    margin-top: 2.5rem;
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

.submit-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 130, 198, 0.2);
    background: #f0f7ff;
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

  .submit-btn {
    padding: 0.8rem 1rem;
    font-size: 0.85rem;
  }
}
</style>


