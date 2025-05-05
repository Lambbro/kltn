<template>
  <nav class="sidebar" :class="{ 'sidebar-open': isOpen }">
    <ul>
      <li>
        <router-link to="/manager-home-to" @click="toggleSidebar">
          <i class="fas fa-home"></i>
          <span>Trang chủ</span>
        </router-link>
      </li>
      <li>
        <router-link to="/manager-list-students" @click="toggleSidebar">
          <i class="fas fa-user-graduate"></i>
          <span>Danh sách sinh viên</span>
        </router-link>
      </li>
      <li>
        <router-link to="/manager-list-teachers" @click="toggleSidebar">
          <i class="fas fa-chalkboard-teacher"></i>
          <span>Danh sách giảng viên</span>
        </router-link>
      </li>
      <li>
        <router-link to="/manager-research-topic" @click="toggleSidebar">
          <i class="fas fa-brain"></i>
          <span>Quản lý hướng NCKH</span>
        </router-link>
      </li>      
      <li>
        <router-link to="/manager-apply-students" @click="toggleSidebar">
          <i class="fas fa-user-plus"></i>
          <span>Quản lý sinh viên đăng ký NCKH</span>
        </router-link>
      </li>
      <!-- <li>
        <router-link to="/manager-apply-topic-students" @click="toggleSidebar">
          <i class="fas fa-file-signature"></i>
          <span>Quản lý đăng ký đề tài sinh viên</span>
        </router-link>
      </li> -->
      <li>
        <router-link to="/manager-topic-student-being-done" @click="toggleSidebar">
          <i class="fas fa-tasks"></i>
          <span>Quản lý đề tài sinh viên đang thực hiện</span>
        </router-link>
      </li>
      <li>
        <router-link to="/manager-topic-students" @click="toggleSidebar">
          <i class="fas fa-book"></i>
          <span>Quản lý đề tài NCKH sinh viên</span>
        </router-link>
      </li>
      <li>
        <router-link to="/manager-result" @click="toggleSidebar">
          <i class="fas fa-chart-bar"></i>
          <span>Quản lý kết quả đề tài</span>
        </router-link>
      </li>
      <li>
        <router-link to="/manager-notification-to-nckh" @click="toggleSidebar">
          <i class="fas fa-bell"></i>
          <span>Quản lý thông báo</span>
        </router-link>
      </li>
    </ul>
  </nav>
</template>

<script setup>
import { ref } from 'vue';

// Props để nhận trạng thái từ parent component
defineProps({
  isOpen: {
    type: Boolean,
    default: false,
  },
});

// Emits để gửi sự kiện toggle về parent
const emit = defineEmits(['toggle']);

const toggleSidebar = () => {
  emit('toggle');
};
</script>

<style scoped>
.sidebar {
  box-shadow: 2px 0 15px rgba(0, 0, 0, 0.1);
  background: linear-gradient(135deg, #0082c6, #1d4ed8);
  transition: left 0.3s ease;
  z-index: 999;
  position: fixed;
  top: 80px;
  left: 0;
  height: calc(100vh - 80px);
  width: 220px;
}

.sidebar ul {
  list-style: none;
  padding: 20px;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.sidebar li {
  padding: 0;
  position: relative;
  transition: all 0.3s ease;
  border-radius: 8px;
  overflow: hidden;
}

.sidebar a {
  color: #ffffff;
  text-decoration: none;
  font-size: 15px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  display: flex;
  align-items: center;
  padding: 12px 15px;
  border-radius: 8px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.sidebar a i {
  width: 24px;
  margin-right: 12px;
  font-size: 16px;
  text-align: center;
}

.sidebar a::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: rgba(255, 255, 255, 0.2);
  transform: scaleX(0);
  transform-origin: right;
  transition: transform 0.3s ease;
}

.sidebar a:hover {
  color: #ffffff;
  background: rgba(255, 255, 255, 0.1);
  transform: translateX(5px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.sidebar a:hover::after {
  transform: scaleX(1);
  transform-origin: left;
}

/* Responsive */

/* Tablet (≤1024px) */
@media (max-width: 1024px) {
  .sidebar {
    width: 220px;
  }

  .sidebar ul {
    padding: 15px;
  }

  .sidebar a {
    font-size: 14px;
    padding: 10px 12px;
  }

  .sidebar a i {
    font-size: 14px;
  }
}

/* Mobile (≤768px) */
@media (max-width: 768px) {
  .sidebar {
    width: 220px;
    left: -220px;
  }

  .sidebar-open {
    left: 0;
  }

  .sidebar a {
    font-size: 13px;
    padding: 8px 10px;
  }

  .sidebar a i {
    font-size: 13px;
  }
}

/* Small Mobile (≤480px) */
@media (max-width: 480px) {
  .sidebar {
    width: 200px;
    left: -200px;
  }

  .sidebar-open {
    left: 0;
  }

  .sidebar a {
    font-size: 12px;
    padding: 6px 8px;
  }

  .sidebar a i {
    font-size: 12px;
  }
}
</style>