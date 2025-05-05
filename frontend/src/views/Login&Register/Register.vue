<template>
  <div class="container">
    <div class="auth-container">
      <h2 style="padding-bottom: 20px;">Đăng ký</h2>
      <form @submit.prevent="handleRegister" class="auth-form">
        <p class="note">Sử dụng Email HOU để tạo tài khoản</p>
        <input v-model="email" type="email" placeholder="Email" required autofocus/>
        <input v-model="password" type="password" placeholder="Mật khẩu" required />
        <input v-model="confirmPassword" type="password" placeholder="Nhập lại mật khẩu" required />
              <div class="flex items-center space-x-2">
            <p class="text-sm font-medium">Quyền</p>
            <select name="role" class="border border-gray-300 rounded-md px-2 py-1 text-sm">
              <option value="phong-nckh">Phòng NCKH</option>
              <option value="to-nckh">Tổ NCKH</option>
              <option value="giang-vien">Giảng viên</option>
              <option value="sinh-vien">Sinh viên</option>
            </select>
          </div>
        <div v-if="password !== confirmPassword" class="error-message">
          Mật khẩu không khớp
        </div>
        <button type="submit" class="btn">Đăng ký</button>
      </form>
      
      <p>Bạn đã có tài khoản? <a @click="$router.push('/login')" class="link">Đăng nhập</a></p>
    </div>
  </div>
</template>
<script setup>
import { ref } from 'vue';  
import { useAuthStore } from '@/stores/auth'; 
import { useRouter } from 'vue-router';

const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const authStore = useAuthStore();
const router = useRouter();

const handleRegister = () => {
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.hou\.edu\.vn$/;
  if (!emailRegex.test(email.value)) {
    alert("Email không hợp lệ, bạn đang không dùng gmail của HOU");
    return;
  }

  if (password.value !== confirmPassword.value) {
    alert("Mật khẩu không khớp, vui lòng kiểm tra lại");
    return;
  }

  // Tiến hành đăng ký (giả sử authStore có phương thức đăng ký)
  // authStore.register(email.value, password.value); 
  router.push('/login');
};
</script>

<style scoped>
.auth-container {
  width: 400px;
  margin: auto;
  padding: 20px;
  text-align: center;
  border: 2px solid #ccc;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.auth-form input {
  display: block;
  width: 100%;
  padding: 10px;
  margin: 20px 0;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
}

.error-message {
  color: red;
  font-size: 14px;
  margin-top: 10px;
}

.btn {
  width: 100%;
  padding: 15px;
  font-size: 16px;
  cursor: pointer;
  border: none;
  background-color: #72b0dc;
  color: white;
  border-radius: 10px;
  margin-top: 10px;
  margin-bottom: 10px;
}

.btn:hover {
  background-color: #215b88;
}

.link {
  color: #007bff;
  cursor: pointer;
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}
.note {
  font-style: italic;
  color: #555;
  position: absolute;
  top: 65px;
  font-size: 14px;
  color: blue;
}
</style>
