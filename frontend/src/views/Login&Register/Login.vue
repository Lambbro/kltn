<template>
  <div class="auth-container">
    <img src="@/assets/img/logo-hou.png" alt="Logo" class="logo" />
    <h2>Đăng nhập</h2>
    <form @submit.prevent="handleLogin" class="auth-form">
      <input v-model="email" type="email" placeholder="Email" required autofocus />
      
      <div class="password-container">
        <input :type="showPassword ? 'text' : 'password'" v-model="password" placeholder="Mật khẩu" required />
        <span class="toggle-password" @click="showPassword = !showPassword">
          <i :class="showPassword ? 'fas fa-eye' : 'fas fa-eye-slash'"></i>
        </span>
      </div>

      <div class="remember-me">
        <input style="margin-left: 22vh;" type="checkbox" id="remember" v-model="rememberMe" />
        <label for="remember">Nhớ mật khẩu</label>
      </div>

      <button type="submit" class="btn">Đăng nhập</button>
    </form>
    <p>
      Bạn chưa có tài khoản? 
      <a @click="$router.push('/register')" class="link">Đăng ký</a>
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import '@/assets/css/login/LoginForm.css';
import '@fortawesome/fontawesome-free/css/all.css';
import api from '@/config/api';

const email = ref('');
const password = ref('');
const rememberMe = ref(false);
const showPassword = ref(false);
const router = useRouter();

// Hàm gọi API đăng nhập
const handleLogin = async () => {
  try {
    const formData = new URLSearchParams();
    formData.append('username', email.value);
    formData.append('password', password.value);

    const response = await api.post('/dang-nhap/', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });

    const data = response.data;
    console.log('Đăng nhập thành công:', data);

    if (!data.access_token || !data.email || !data.quyen_han) {
      throw new Error('Dữ liệu trả về không hợp lệ');
    }
    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('email', data.email);
    localStorage.setItem('quyen_han', data.quyen_han);
    localStorage.setItem('ma_khoa', data.ma_khoa);
    
    const routes = {
      1: '/manager-home-phong',
      2: '/manager-home-to',
    };
    router.push(routes[data.quyen_han] || '/');
  } catch (error) {
    let errorMessage = 'Đăng nhập thất bại';
    if (error.response) {
      if (error.response.status === 401) {
        errorMessage = 'Sai email hoặc mật khẩu';
      } else if (error.response.status === 500) {
        errorMessage = 'Thông tin hoặc mật khẩu không chính xác';
      }
    } else {
      errorMessage = 'Không thể kết nối đến server';
    }
    console.error(errorMessage, error);
    password.value = '';
    alert(errorMessage);
  }
};
</script>
