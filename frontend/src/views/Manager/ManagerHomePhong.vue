<template>
  <div class="container">
    <!-- Header -->
    <header class="header">
      <button v-if="isMobile" class="sidebar-toggle" @click="toggleSidebar">☰</button>
      <img src="@/assets/img/logo-hou.png" alt="Logo" class="logo" />
      <h1>HỆ THỐNG QUẢN LÝ NGHIÊN CỨU KHOA HỌC</h1>
      <!-- Hiển thị trạng thái đăng nhập -->
      <div class="auth-buttons">
        <template v-if="isAuthenticated">
          <span>{{ storedEmail }}</span>
          <button @click="handleLogout">Đăng xuất</button>
        </template>
        <template v-else>
          <button @click="$router.push('/login')">Đăng nhập</button>
        </template>
      </div>
    </header>

    <!-- Overlay khi sidebar mở trên mobile -->
    <div v-if="isSidebarOpen && isMobile" class="overlay" @click="toggleSidebar"></div>

    <!-- Main layout -->
    <div class="main-layout">
      <!-- Sidebar -->
      <SidebarManagerPhong
        class="sidebar"
        :is-open="isSidebarOpen"
        @toggle="toggleSidebar"
      />

      <!-- Main content -->
      <div class="main-content" :class="{ 'main-content-shifted': isSidebarOpen && !isMobile }">
        <!-- Slideshow -->
        <div class="wiper-slide-inner">
          <img class="slide" src="@/assets/img/hou_1713259719.jpg" alt="Đại học Mở Hà Nội" />
          <img class="slide" src="@/assets/img/18.jpg" alt="Ảnh 2" />
          <img class="slide" src="@/assets/img/3300-1200-scaled.jpg" alt="Ảnh 3" />
        </div>

        <!-- News section -->
        <div class="news-section">
          <div>Chào mừng đến trang quản lý</div>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <footer class="footer">
      <Footer class="footer-content" />
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import SidebarManagerPhong from '@/components/SidebarMangerPhong.vue';
import Footer from '@/components/Footer.vue';

const router = useRouter();
const authStore = useAuthStore();

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
    isSidebarOpen.value = false; // Đóng sidebar khi resize về mobile
  }
});

onMounted(() => {
  authStore.loadUserFromStorage();
});

const { isAuthenticated, storedEmail, logout } = authStore;

const handleLogout = () => {
  logout();
  router.push('/login');
};
</script>
<style scoped>
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
  background: #1e88e5;
  border-radius: 10px;
}

.container::-webkit-scrollbar-thumb:hover {
  background: #1565c0;
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
  margin-top: 2rem;
}

.header h1 {
  font-size: 1.5rem;
  margin: 0;
  flex-grow: 1;
  text-align: center;
  color: #0082c6;
}

.auth-buttons {
  display: flex;
  gap: 0.5rem;
}

.auth-buttons button {
  padding: 0.5rem 1rem;
  background: #0082c6;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
}

.auth-buttons button:hover {
  background: #1e88e5;
}

.sidebar-toggle {
  display: none;
  background: #0082c6;
  color: white;
  border: none;
  padding: 0.5rem 0.8rem;
  font-size: 1.2rem;
  cursor: pointer;
  border-radius: 5px;
}

/* Main layout */
.main-layout {
  display: flex;
  margin-top: 80px; /* Khoảng cách với header */
  min-height: calc(100vh - 80px);
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
  z-index: 111;
}

/* Main content */
.main-content {
  flex: 1;
  padding: 20px 40px;
  background: #f4f4f4;
  margin-left: 260px; /* Sidebar (220px) + khoảng cách 40px */
  margin-right: 40px; /* Cách viền phải 40px */
  box-sizing: border-box;
}

/* Slideshow */
.wiper-slide-inner {
  position: relative;
  width: 100%;
  height: 300px;
  overflow: hidden;
  margin-bottom: 1rem;
}

.slide {
  position: absolute;
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0;
  animation: slideShow 9s infinite;
}

.slide:nth-child(1) { animation-delay: 0s; }
.slide:nth-child(2) { animation-delay: 3s; }
.slide:nth-child(3) { animation-delay: 6s; }

@keyframes slideShow {
  0% { opacity: 0; }
  11% { opacity: 1; }
  33% { opacity: 1; }
  44% { opacity: 0; }
  100% { opacity: 0; }
}

/* News Section */
.news-section {
  width: 100%;
  border: 1px solid #ccc;
  padding: 1rem;
}

.news-section div {
  margin-top: 0;
}

/* Footer */
.footer {
  background: #0082c6;
  color: white;
  padding: 1rem;
  text-align: center;
  height: 120px; /* Chiều cao cố định */
}

/* Responsive */

/* Tablet (≤1024px) */
@media (max-width: 1024px) {
  .header {
    padding: 10px 20px;
  }

  .main-content {
    margin-left: 260px; /* Giữ khoảng cách với sidebar */
    margin-right: 20px; /* Giảm cách viền phải */
  }

  .sidebar {
    width: 200px;
  }

  .header h1 {
    font-size: 1.3rem;
  }
}

/* Mobile (≤768px) */
@media (max-width: 768px) {
  .header {
    flex-wrap: wrap;
    padding: 10px 15px;
    position: relative;
  }

  .sidebar-toggle {
    display: block;
    position: absolute;
    left: 15px;
    top: 15px;
  }

  .logo {
    margin: 0 auto;
    order: 1;
  }

  .header h1 {
    font-size: 1.2rem;
    width: 100%;
    text-align: center;
    margin-top: 10px;
    order: 2;
  }

  .auth-buttons {
    order: 3;
    margin: 10px auto;
  }

  .main-layout {
    flex-direction: column;
  }

  .sidebar {
    width: 200px;
    left: -200px;
    top: 60px; /* Header nhỏ hơn */
    height: calc(100vh - 60px);
  }

  .sidebar-open {
    left: 0;
  }

  .main-content {
    margin-left: 0;
    margin-right: 0;
    padding: 15px;
  }

  .wiper-slide-inner {
    height: 250px;
  }

  .news-section {
    padding: 0.5rem;
  }
}

/* Small Mobile (≤480px) */
@media (max-width: 480px) {
  .header {
    padding: 10px;
  }

  .header h1 {
    font-size: 1rem;
  }

  .logo {
    width: 40px;
  }

  .auth-buttons button {
    padding: 0.4rem 0.8rem;
    font-size: 0.9rem;
  }

  .sidebar {
    width: 180px;
    left: -180px;
  }

  .sidebar-open {
    left: 0;
  }

  .main-content {
    padding: 10px;
  }

  .wiper-slide-inner {
    height: 200px;
  }

  .news-section {
    padding: 0.5rem;
  }
}
</style>