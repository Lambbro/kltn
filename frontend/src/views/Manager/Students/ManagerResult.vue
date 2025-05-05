<template>
<div class="container">
    <!-- Header -->
    <header class="header">
      <img src="@/assets/img/logo-hou.png" alt="Logo" class="logo"/>
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

    <!-- Main layout -->
    <div class="main-layout">
      <!-- Sidebar -->
      <SidebarMangerPhong v-if="authStore.user?.quyen_han === 1" class="sidebar" />
      <SidebarManagerToNCKH v-else class="sidebar" />

      <!-- Main content -->
      <div class="main-content">
          <div> Chào mừng đến trang quản lý kết quả đề tài sinh viên</div>
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

import SidebarManagerToNCKH from '@/components/SidebarManagerToNCKH.vue';
import SidebarMangerPhong from '@/components/SidebarMangerPhong.vue';
import Footer from '@/components/Footer.vue';
// Khi ứng dụng chạy, kiểm tra trạng thái đăng nhập
onMounted(() => {
  authStore.loadUserFromStorage();
});
// Sử dụng store để lấy thông tin đăng nhập
const router = useRouter();
const authStore = useAuthStore();

const { isAuthenticated, storedEmail, logout } = authStore;

// Hàm đăng xuất
const handleLogout = () => {
  logout();  // Xóa token khỏi localStorage
  router.push('/login'); // Quay về trang chủ sau khi đăng xuất
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
  border-bottom: 1px solid #ccc;
  background: white;
  position: fixed;
  width: 100%;
  left: 0;
  z-index: 1000;
}

.logo {
  width: 50px;
  margin-right: 1rem;
  margin-left: 80px;
}

.header h1 {
  font-size: 1.5rem;
  margin: 0;
  flex-grow: 1;
  text-align: center;
  color: #2563eb;
}

.auth-buttons {
  display: flex;
  gap: 0.5rem;
  margin-right: 2rem;
}

.auth-buttons button {
  padding: 0.5rem 1rem;
  background: #2563eb;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
}

.auth-buttons button:hover {
  background: #2563eb;
}
.main-layout {
  display: flex;
  flex: 1;
  margin-top: 60px; 
}
.sidebar {
  width: 220px;
  height: 100vh;
  background: #2563eb;
  position: fixed;
  left: 0;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}
.main-content {
  flex: 1;
  padding: 1rem;
  background: #f4f4f4;
  width: 120%;
}
@media (max-width: 768px) {
  .header {
    flex-direction: column;
    text-align: center;
  }

  .logo {
    margin: 0 auto;
  }

  .auth-buttons {
    margin: 10px 0;
  }

  .main-layout {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
    height: auto;
    position: relative;
  }

  .main-content {
    padding-left: 0;
  }

  .wiper-slide-inner {
    width: 100%;
  }

  .news-section {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .header h1 {
    font-size: 1.2rem;
  }

  .auth-buttons button {
    padding: 0.4rem 0.8rem;
    font-size: 0.9rem;
  }

  .sidebar {
    padding-top: 10px;
  }

  .news-section {
    padding: 0.5rem;
  }

  .slide {
    height: 200px;
  }
}
</style>