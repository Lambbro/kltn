<template>
  <div class="container">
    <!-- Header -->
    <header class="header">
      <img src="@/assets/img/logo-hou.png" alt="Logo" class="logo"/>
      <h1>HỆ THỐNG QUẢN LÝ NGHIÊN CỨU KHOA HỌC</h1>

      <!-- Phần này đã được chỉnh sửa để hiển thị tùy thuộc vào trạng thái đăng nhập -->
      <div class="auth-buttons">
        <template v-if="user">
          <!-- Hiển thị email và nút đăng xuất khi đã đăng nhập -->
          <span>{{ user.email }}</span>
          <span>{{ user.role }}</span>
          <button @click="handleLogout">Đăng xuất</button>
        </template>
        <template v-else>
          <!-- Hiển thị nút đăng nhập, đăng ký khi chưa đăng nhập -->
          <button @click="$router.push('/login')">Đăng nhập</button>
          <button @click="$router.push('/register')">Đăng ký</button>
        </template>
      </div>
    </header>

    <!-- Main layout -->
    <div class="main-layout">
      <!-- Sidebar -->
      <SidebarHome class="sidebar" />
      <!-- Content -->
       <div class="content">
              <p>Hệ thống quản lý nghiên cứu khoa học tại Trường Đại học Mở Hà Nội được xây dựng nhằm hỗ trợ công tác quản lý,
               theo dõi và đánh giá các hoạt động nghiên cứu khoa học trong nhà trường. 
               Hệ thống giúp tối ưu hóa quy trình đăng ký, xét duyệt, thực hiện và báo cáo kết quả nghiên cứu khoa học, 
               đảm bảo sự minh bạch, chính xác và hiệu quả trong công tác quản lý.</p>
               <br>
              <p>
                Hệ thống được thiết kế với giao diện thân thiện, dễ sử dụng, 
              cho phép các đối tượng như giảng viên, sinh viên, cán bộ quản lý khoa học có thể truy cập và thao tác thuận tiện. 
              Các chức năng chính của hệ thống bao gồm:
              </p>
              <il style=" margin-left: 20px; font-weight: bold;">
                <li>Đăng ký đề tài nghiên cứu khoa học</li>
                <li>Xét duyệt đề tài nghiên cứu khoa học</li>
                <li>Thực hiện đề tài nghiên cứu khoa học</li>
                <li>Báo cáo kết quả nghiên cứu khoa học</li>
              </il>
              <p>
                Hệ thống được phát triển trên nền tảng công nghệ hiện đại, đảm bảo khả năng mở rộng và bảo mật cao. 
                Việc triển khai hệ thống không chỉ nâng cao hiệu quả quản lý mà còn góp phần thúc đẩy phong trào nghiên cứu khoa học trong trường, 
                tạo điều kiện thuận lợi cho giảng viên và sinh viên phát huy khả năng sáng tạo và đổi mới trong nghiên cứu.
              </p>
              <br>
              <div class="dev">
                  Phát triển bởi LABFITHOU
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
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

// Import các component con
import SidebarHome from '@/components/SidebarHome.vue';
import Footer from '@/components/Footer.vue';

// Khởi tạo store và router
const authStore = useAuthStore();
const router = useRouter();

// Tạo computed property để lấy user từ store
const user = computed(() => authStore.user);

// Hàm đăng xuất
const handleLogout = () => {
  authStore.logout();
   router.push('/home');
};
</script>

<style scoped>

.container {
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

/* Auth buttons */
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

/* Main layout */
.main-layout {
  display: flex;
  flex: 1;
  margin-top: 60px; 
}
.content {
  display: block !important; 
  column-count: 1 !important; 
  width: 100%; 
  text-align: justify;
}

/* Sidebar */
.sidebar {
  width: 220px;
  height: 100vh;
  background: #2563eb;
  padding-top: 20px;
  position: fixed;
  left: 0;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
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
