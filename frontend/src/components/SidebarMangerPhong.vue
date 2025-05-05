<template>
  <nav class="sidebar" :class="{ 'sidebar-open': isOpen }">
    <ul>
      <li>
        <router-link to="/manager-home-phong" @click="toggleSidebar">
          <i class="fas fa-home"></i>
          <span>Trang chủ</span>
        </router-link>
      </li>
      <li>
        <router-link to="/manager-list-facultys" @click="toggleSidebar">
          <i class="fas fa-university"></i>
          <span>Danh sách khoa</span>
        </router-link>
      </li>
      <li>
        <router-link to="/manager-list-teachers" @click="toggleSidebar">
          <i class="fas fa-chalkboard-teacher"></i>
          <span>Danh sách giảng viên</span>
        </router-link>
      </li>
      <li>
        <router-link to="/manager-list-students" @click="toggleSidebar">
          <i class="fas fa-user-graduate"></i>
          <span>Danh sách sinh viên</span>
        </router-link>
      </li>
      <li>
        <router-link to="/manager-list-research-topics" @click="toggleSidebar">
          <i class="fas fa-brain"></i>
          <span>Quản lý hướng nghiên cứu</span>
        </router-link>
      </li>
      <li>
        <router-link to="/manager-apply-teachers" @click="toggleSidebar">
          <i class="fas fa-file-signature"></i>
          <span>Quản lý đăng ký đề tài giảng viên</span>
        </router-link>
      </li>
      <li>
        <router-link to="/manager-topic-teachers-being-done" @click="toggleSidebar">
          <i class="fas fa-tasks"></i>
          <span>Quản lý đề tài giảng viên đang thực hiện</span>
        </router-link>
      </li>
      <li>
        <router-link to="/manager-topic-teachers" @click="toggleSidebar">
          <i class="fas fa-book"></i>
          <span>Quản lý đề tài giảng viên</span>
        </router-link>
      </li>
      <li>
        <router-link to="/manager-result" @click="toggleSidebar">
          <i class="fas fa-chart-bar"></i>
          <span>Quản lý kết quả đề tài sinh viên</span>
        </router-link>
      </li>
      <li>
        <router-link to="/manager-notification-phong" @click="toggleSidebar">
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
  background: linear-gradient(135deg, #0082c6, #0082c6);
  transition: left 0.3s ease;
  z-index: 999;
  position: fixed;
  top: 80px;
  left: 0;
  height: calc(100vh - 80px);
  width: 220px;
  overflow-y: auto;
}

.sidebar-header {
  padding: 20px;
  text-align: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-header h3 {
  color: #ffffff;
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.sidebar ul {
  list-style: none;
  padding: 15px;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 15px;
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
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  display: flex;
  align-items: center;
  padding: 12px 15px;
  border-radius: 8px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.05);
}

.sidebar a i {
  width: 24px;
  margin-right: 12px;
  font-size: 16px;
  text-align: center;
  transition: transform 0.3s ease;
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

.sidebar a:hover i {
  transform: scale(1.1);
}

.sidebar a:hover::after {
  transform: scaleX(1);
  transform-origin: left;
}

/* Scrollbar Styling */
.sidebar::-webkit-scrollbar {
  width: 6px;
}

.sidebar::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
}

.sidebar::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
}

.sidebar::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
}

/* Responsive */

/* Tablet (≤1024px) */
@media (max-width: 1024px) {
  .sidebar {
    width: 220px;
  }

  .sidebar-header {
    padding: 15px;
  }

  .sidebar-header h3 {
    font-size: 16px;
  }

  .sidebar ul {
    padding: 12px;
  }

  .sidebar a {
    font-size: 13px;
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
    font-size: 12px;
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
    font-size: 11px;
    padding: 6px 8px;
  }

  .sidebar a i {
    font-size: 12px;
  }
}
</style>