<template>
  <nav class="sidebar">
    <ul>
      <!-- Trang chủ -->
      <li>
        <router-link to="/">
          <i class="fas fa-home"></i>
          <span>Trang Chủ</span>
        </router-link>
      </li>

      <!-- Đề tài NCKH -->
      <li>
        <template v-if="authStore.user">
          <template v-if="authStore.user.quyen_han == 3">
            <router-link to="/de-tai-nckh-gv">
              <i class="fas fa-book"></i>
              <span>Đề tài nckh</span>
            </router-link>
          </template>
          <template v-else-if="authStore.user.quyen_han == 4">
            <router-link to="/de-tai-nckh">
              <i class="fas fa-book"></i>
              <span>Đề tài nckh</span>
            </router-link>
          </template>
        </template>
      </li>
      <!-- Khu vực đăng ký NCKH -->
      <li>
        <template v-if="authStore.user">
          <!-- Giảng viên (quyen_han = 3) có submenu -->
          <template v-if="authStore.user.quyen_han == 3">
            <a href="javascript:void(0)" @click="toggleSubmenu">
              <i class="fas fa-pen-fancy"></i>
              <span>Đăng Ký NCKH</span>
              <i class="fas fa-chevron-down dropdown-icon" :class="{ 'rotate': showSubmenu }"></i>
            </a>
            <ul v-if="showSubmenu" class="submenu">
              <li>
                <router-link to="/apply-teachers">
                  <i class="fas fa-chalkboard-teacher"></i>
                  <span>Đăng Ký Đề Tài Giảng Viên</span>
                </router-link>
              </li>
              <li>
                <router-link to="/apply-topic-students">
                  <i class="fas fa-user-graduate"></i>
                  <span>Đăng Ký Đề Tài Sinh Viên</span>
                </router-link>
              </li>
            </ul>
          </template>

          <!-- Sinh viên (quyen_han = 4) chỉ có link Đăng Ký Đề Tài Sinh Viên -->
          <template v-else-if="authStore.user.quyen_han == 4">
            <router-link to="/apply-students">
              <i class="fas fa-pen-fancy"></i>
              <span>Đăng Ký NCKH</span>
            </router-link>
          </template>
        </template>

        <!-- Nếu chưa đăng nhập -->
        <template v-else>
          <router-link to="/login">
            <i class="fas fa-pen-fancy"></i>
            <span>Đăng Ký NCKH</span>
          </router-link>
        </template>
      </li>

      <!-- Thông tin cá nhân -->
      <li>
        <template v-if="authStore.user">
          <router-link
            :to="authStore.user.quyen_han == 3 ? '/info' : (authStore.user.quyen_han == 4 ? '/info-students' : '/info')"
          >
            <i class="fas fa-user-circle"></i>
            <span>Thông Tin Cá Nhân</span>
          </router-link>
        </template>
        <template v-else>
          <router-link to="/login">
            <i class="fas fa-user-circle"></i>
            <span>Thông Tin Cá Nhân</span>
          </router-link>
        </template>
      </li>

      <!-- Giới thiệu -->
      <li>
        <router-link to="/introduce">
          <i class="fas fa-info-circle"></i>
          <span>Giới thiệu</span>
        </router-link>
      </li>
    </ul>
  </nav>
</template>

<script>
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth';

export default {
  setup() {
    const authStore = useAuthStore();
    const showSubmenu = ref(false);

    const toggleSubmenu = () => {
      showSubmenu.value = !showSubmenu.value;
    };

    return {
      authStore,
      showSubmenu,
      toggleSubmenu
    };
  }
};
</script>

<style scoped>
.sidebar {
  box-shadow: 2px 0 15px rgba(0, 0, 0, 0.1);
  transition: left 0.3s ease;
  z-index: 999;
  background: linear-gradient(180deg, #2563eb 0%, #1e40af 100%);
  padding: 20px 0;
}

.sidebar ul {
  list-style: none;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 15px;
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

.submenu {
  list-style: none;
  padding-left: 0;
  background-color: rgba(37, 99, 235, 0.1);
  margin: 5px 0;
  border-radius: 8px;
  overflow: hidden;
}

.submenu li {
  padding: 0;
  margin: 0;
}

.submenu a {
  font-size: 13px;
  color: #ffffff;
  opacity: 0.9;
  padding: 10px 15px;
  padding-left: 45px;
}

.submenu a:hover {
  opacity: 1;
  background: rgba(255, 255, 255, 0.1);
}

.dropdown-icon {
  margin-left: auto;
  transition: transform 0.3s ease;
}

.rotate {
  transform: rotate(180deg);
}

/* Responsive */

/* Tablet (≤1024px) */
@media (max-width: 1024px) {
  .sidebar {
    width: 220px;
  }

  .sidebar a {
    font-size: 13px;
    padding: 10px 12px;
  }

  .submenu a {
    font-size: 12px;
    padding: 8px 12px;
    padding-left: 40px;
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
    padding: 8px 10px;
  }

  .submenu a {
    font-size: 11px;
    padding: 6px 10px;
    padding-left: 35px;
  }
}
</style>