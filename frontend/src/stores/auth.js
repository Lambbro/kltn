import { defineStore } from 'pinia';
import { ref, computed, onMounted } from 'vue';

export const useAuthStore = defineStore('auth', () => {
  // user sẽ lưu đối tượng { email, quyen_han, token }
  const user = ref(null);

  // Hàm load trạng thái đăng nhập từ localStorage
  const loadUserFromStorage = () => {
    const storedToken = localStorage.getItem('access_token');
    const storedEmail = localStorage.getItem('email');
    const storedQuyenHan = localStorage.getItem('quyen_han');

    // Nếu có đầy đủ thông tin, gán vào user
    if (storedToken && storedEmail && storedQuyenHan) {
      user.value = {
        email: storedEmail,
        // Ép kiểu về number nếu server trả về quyen_han dạng số hoặc chuỗi
        quyen_han: Number(storedQuyenHan),
        token: storedToken
      };
    }
  };

  // Tự động load khi store khởi tạo
  onMounted(loadUserFromStorage);

  // Hàm login gọi API đăng nhập bên FastAPI
  const login = async (email, password) => {
    try {
      const response = await fetch('http://192.168.10.142:8000/dang-nhap/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        // Thêm tùy chọn này nếu cần cookie/session:
        credentials: 'include',
        body: JSON.stringify({ email, password })
      });

      if (!response.ok) {
        throw new Error('Email hoặc mật khẩu không đúng. Vui lòng thử lại!');
      }

      const data = await response.json();

      // Giả sử server trả về:
      // { email, quyen_han, access_token }
      user.value = {
        email: data.email,
        quyen_han: data.quyen_han,  // Nếu cần ép kiểu -> Number(data.quyen_han)
        token: data.access_token
      };

      // Lưu xuống localStorage
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('email', data.email);
      localStorage.setItem('quyen_han', data.quyen_han);

      return true;
    } catch (error) {
      console.error(error.message);
      user.value = null;
      alert(error.message);
      return false;
    }
  };

  // Hàm logout: xóa dữ liệu trong store & localStorage
  const logout = () => {
    user.value = null;
    localStorage.removeItem('access_token');
    localStorage.removeItem('email');
    localStorage.removeItem('quyen_han');
    console.log('Đã đăng xuất thành công!');
  };

  // Kiểm tra đơn giản xem có token hay không
  const isAuthenticated = computed(() => localStorage.getItem('access_token') !== null);

  // Lấy email từ localStorage (hoặc bạn có thể lấy từ user.value)
  const storedEmail = computed(() => localStorage.getItem('email'));

  return {
    user,
    loadUserFromStorage,
    login,
    logout,
    isAuthenticated,
    storedEmail
  };
});
