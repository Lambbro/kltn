<template>
  <nav class="sidebar" :class="{ 'sidebar-open': isOpen }">
    <ul>
      <li>
        <router-link to="/info-students" @click="toggleSidebar">
          <i class="fas fa-user-circle"></i>
          <span>Thông tin cá nhân</span>
        </router-link>
      </li>
      <li>
        <router-link to="/de-tai-sinh-vien" @click="toggleSidebar">
          <i class="fas fa-trophy"></i>
          <span>Kết quả nghiên cứu</span>
        </router-link>
      </li>
      <li>
        <router-link to="/" @click="toggleSidebar">
          <i class="fas fa-home"></i>
          <span>Trang Chủ</span>
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
/* Sidebar */
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  width: 220px;
  height: 100vh;
  box-shadow: 2px 0 15px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  z-index: 999;
  background: linear-gradient(180deg, #0082c6 0%, #0069a3 100%);
}

.sidebar ul {
  list-style: none;
  padding: 100px 0 20px;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.sidebar li {
  padding: 0;
  margin: 0 10px;
  border-radius: 8px;
  transition: all 0.3s ease;
  overflow: hidden;
}

.sidebar li:hover {
  background: rgba(255, 255, 255, 0.1);
}

.sidebar a {
  color: #ffffff;
  text-decoration: none;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  display: flex;
  align-items: center;
  font-family: Arial, sans-serif;
  font-size: 16px;
  padding: 12px 15px;
  position: relative;
  transition: all 0.3s ease;
}

.sidebar a i {
  width: 24px;
  margin-right: 12px;
  font-size: 16px;
  text-align: center;
}

.sidebar a:hover {
  color: #ffffff;
  transform: translateX(5px);
  text-shadow: 0 0 8px rgba(255, 255, 255, 0.5);
}

.sidebar a::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 1px;
  background: rgba(255, 255, 255, 0.2);
  transform: scaleX(0);
  transform-origin: right;
  transition: transform 0.3s ease;
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
    padding: 85px 0 20px;
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
    transform: translateX(-100%);
  }

  .sidebar-open {
    transform: translateX(0);
  }

  .sidebar ul {
    padding: 80px 0 20px;
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
  }

  .sidebar ul {
    padding: 75px 0 20px;
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