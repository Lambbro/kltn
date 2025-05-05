<template>
  <div class="container">
    <!-- Overlay -->
    <div
      v-if="sidebarOpen"
      class="overlay"
      @click="toggleSidebar"
    ></div>

    <!-- Header -->
    <header class="header">
      <button class="sidebar-toggle" @click="toggleSidebar">☰</button>
      <img src="@/assets/img/logo-hou.png" alt="Logo" class="logo" />
      <h1>HỆ THỐNG QUẢN LÝ NGHIÊN CỨU KHOA HỌC</h1>
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
      <SidebarHome class="sidebar" :class="{ 'sidebar-open': sidebarOpen }" />
      <div class="main-content">
        <div class="wiper-slide-inner">
          <img class="slide" src="@/assets/img/hou_1713259719.jpg" />
          <img class="slide" src="@/assets/img/18.jpg" />
          <img class="slide" src="@/assets/img/3300-1200-scaled.jpg" />
        </div>
        <div class="news-section">
          <h2>Tin mới</h2>
          <div class="news-placeholder"></div>
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
import { useAuthStore } from '../stores/auth';
import SidebarHome from '../components/SidebarHome.vue';
import Footer from '../components/Footer.vue';

const sidebarOpen = ref(false);
const router = useRouter();
const authStore = useAuthStore();
const { isAuthenticated, storedEmail, logout } = authStore;

onMounted(() => {
  authStore.loadUserFromStorage();
});

const handleLogout = () => {
  logout();
  router.push('/login');
};

const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value;
};
</script>

<!-- Import external CSS -->
<style scoped src="../assets/css/HomePage.css"></style>