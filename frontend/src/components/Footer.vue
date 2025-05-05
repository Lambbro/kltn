<template>
    <footer class="footer">
        <div class="footer-container">
      <!-- Logo -->
      <div class="footer-logo">
        <img src="@/assets/img/logo-hou.png" alt="Trường Đại Học Mở Hà Nội" />
      </div>
      <!-- Contact Info -->
      <div class="footer-info">
        <h2>TRƯỜNG ĐẠI HỌC MỞ HÀ NỘI</h2>
        <p>📍 Địa chỉ: Nhà B101, phố Nguyễn Hiền, phường Bách Khoa, quận Hai Bà Trưng, TP Hà Nội</p>
        <p>📞 Điện thoại: 024.38682321</p>
      </div> 
    
    </div>
    </footer>
</template>
<style scoped>
/* Footer */
.footer {
  width: 100vw;  /* Full màn hình */
  height: 120px;  /* Chiều cao cố định */
  background: #0082c6;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  position: fixed; /* Cố định footer ở cuối màn hình */
  bottom: 0;
  left: 0;
  border-top: 1px solid #ccc;
  z-index: 2000;
}

/* Đảm bảo nội dung căn giữa */
.footer-container {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
}

/* Logo */
.footer-logo img {
  margin-top: 10px;
  width: 80px;
}

/* Thông tin trường */
.footer-info {
  flex: 1;
  text-align: left;
  margin-left: 30px;
}

.footer-info h2 {
  font-size: 1.2rem;
  margin-bottom: 10px;
  color:white
}

.footer-info p {
  margin: 5px 0;
  font-size: 12px;
  color:white
}

.footer-info a {
  color: white;
  text-decoration: none;
  font-weight: bold;
}

.footer-info a:hover {
  text-decoration: underline;
}
</style>