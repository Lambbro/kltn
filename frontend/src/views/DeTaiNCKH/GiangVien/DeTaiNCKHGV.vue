<template>
    <div class="container">
        <header class="header">
            <img src="@/assets/img/logo-hou.png" alt="Logo" class="logo"/>
            <div class="button-group">
                <button class="active" @click="$router.push(`/de-tai-nckh`)">Tổng hợp đề tài</button>
                <button class="active" @click="handleDangThucHienClick">Đề tài đang thực hiện</button>
            </div>
        </header>

        <div class="main-layout">
            <SidebarHome class="sidebar" />
            <div class="main-content">
                <!-- Vùng chứa nút Bộ lọc và ô tìm kiếm -->
                <div class="filter-search">
                    <button class="filter-btn" @click="handleDeTaiGVClick">Đề tài giảng viên</button>
                    <button class="filter-btn" @click="handleDeTaiSVClick">Đề tài sinh viên</button>
                    <!-- Khi click, ta thay đổi showFilter -->
                    <button class="filter-btn" @click="showFilter = !showFilter">
                        Bộ lọc
                    </button>
                </div>

                <!-- Form bộ lọc, hiển thị khi showFilter = true -->
                <div 
                    v-if="showFilter" 
                    class="filter-form" 
                    style="margin-bottom: 20px; border: 1px solid #ccc; padding: 10px; border-radius: 10px;">
                    <div style="display: flex; flex-wrap: wrap; gap: 10px;">
                        <div style="flex: 1 1 200px;">
                            <label>Tên đề tài</label>
                            <input type="text" v-model="filterCriteria.title" />
                        </div>
                        <div style="flex: 1 1 200px;">
                            <label>Người thực hiện</label>
                            <input type="text" v-model="filterCriteria.researcher" />
                        </div>
                        <div style="flex: 1 1 200px;">
                            <label>Năm</label>
                            <input type="text" v-model="filterCriteria.year" />
                        </div>
                        <div style="flex: 1 1 200px;">
                            <label>Hướng nghiên cứu</label>
                            <input type="text" v-model="filterCriteria.huongNC" />
                        </div>
                    </div>
                </div>

                <!-- Vùng hiển thị danh sách đề tài, sử dụng filteredTopics -->
                <div class="research-list">
                    <div 
                      class="research-item"
                      v-for="(item, index) in filteredTopics" 
                      :key="index"
                      @click="goToDetailPage(item.id)"
                    >
                        <img src="@/assets/img/logo-hou.png" alt="Logo" class="research-logo"/>
                        <div class="research-info">
                            <p><strong>Tên đề tài:</strong> {{ item.title }}</p>
                            <p><strong>Người thực hiện:</strong> {{ item.researcher }}</p>
                            <p><strong>Năm thực hiện:</strong> {{ item.year }}</p>
                            <p><strong>Hướng nghiên cứu: </strong>{{ item.huongNC }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import SidebarHome from '@/components/SidebarHome.vue';
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const router = useRouter();
const authStore = useAuthStore();

function handleDeTaiGVClick() {
    router.push('/de-tai-nckh-gv');
}

function handleDeTaiSVClick() {
    router.push('/de-tai-nckh');
}

// Hàm xóa dấu tiếng Việt
function removeAccents(str) {
  return str.normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/đ/g, 'd').replace(/Đ/g, 'D')
    .toLowerCase();
}

// Hàm tìm kiếm tương đối
function fuzzySearch(text, searchTerm) {
  if (!searchTerm) return true;
  
  const normalizedText = removeAccents(text);
  const normalizedSearch = removeAccents(searchTerm);
  
  // Tách các từ trong searchTerm
  const searchWords = normalizedSearch.split(/\s+/);
  
  // Kiểm tra xem tất cả các từ có xuất hiện trong text không (không cần đúng thứ tự)
  return searchWords.every(word => 
    normalizedText.includes(word)
  );
}

// Danh sách đề tài
const researchTopics = ref([
    { id: 1, title: 'DGA bonet chaterbased', researcher: 'La Tiến Nam', year: 2025, huongNC: 'mang', result: 'Hoàn thành' },
    { id: 2, title: 'Nghiên cứu cách tấn công', researcher: 'Hoàng Đức Trang', year: 2025, huongNC: 'phanmem', result: 'Đang thực hiện' },
    { id: 3, title: 'Nghiên cứu và ứng dụng Blockchain trong quản lý chuỗi cung ứng', researcher: 'Lê Xuân Thịnh', year: 2024, huongNC: 'mang', result: 'Hoàn thành' },
    { id: 4, title: 'Tối ưu hóa thuật toán tìm kiếm trong hệ thống Big Data', researcher: 'Hoàng Tiến Vân', year: 2024, huongNC: 'mang', result: 'Hoàn thành' },
    { id: 5, title: 'Phân tích hành vi người dùng trên website bằng kỹ thuật Data Mining', researcher: 'Chu Thanh Thanh', year: 2025, huongNC: 'mang', result: 'Đang thực hiện' },
    { id: 6, title: 'Ứng dụng Deepfake Detection trong xác thực hình ảnh và video', researcher: 'Hồ Vĩnh Trang', year: 2024, huongNC: 'mang', result: 'Hoàn thành' },
   
]);

// Biến điều khiển việc hiện/ẩn form bộ lọc
const showFilter = ref(false);

// Đối tượng chứa các tiêu chí lọc
const filterCriteria = ref({
    title: '',
    researcher: '',
    year: '',
    huongNC: '',
    result: ''
});

// Computed property để áp dụng các điều kiện lọc
const filteredTopics = computed(() => {
    return researchTopics.value.filter((item) => {
        // Kiểm tra từng trường với tìm kiếm tương đối
        const matchTitle = fuzzySearch(item.title, filterCriteria.value.title);
        const matchResearcher = fuzzySearch(item.researcher, filterCriteria.value.researcher);
        const matchYear = fuzzySearch(String(item.year), filterCriteria.value.year);
        const matchHuongNC = fuzzySearch(item.huongNC, filterCriteria.value.huongNC);
        const matchResult = fuzzySearch(item.result, filterCriteria.value.result);

        // Kết hợp tất cả các điều kiện
        return matchTitle && matchResearcher && matchYear && matchHuongNC && matchResult;
    });
});

// Hàm điều hướng đến trang chi tiết
function goToDetailPage(id) {
  if (authStore.user) {
    router.push(`/chi-tiet-de-tai/${id}`);
  } else {
    router.push('/login');
  }
}

// Hàm xử lý click vào nút "Đề tài đang thực hiện"
function handleDangThucHienClick() {
  if (!authStore.user) {
    router.push('/login');
    return;
  }

  if (authStore.user.quyen_han === 3) {
    router.push('/de-tai-dang-thuc-hien-gv');
  } else if (authStore.user.quyen_han === 4) {
    router.push('/de-tai-dang-thuc-hien-sinh-vien');
  }
}

// Hàm áp dụng lọc
function applyFilter() {
    console.log('Áp dụng lọc với tiêu chí:', filterCriteria.value);
}


</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  overflow-y: auto;
  background-color: #f8fafc;
}

.container::-webkit-scrollbar {
  width: 6px;
}

.container::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 10px;
}

.container::-webkit-scrollbar-thumb {
  background: #0082c6;
  border-radius: 10px;
}

.container::-webkit-scrollbar-thumb:hover {
  background: #0082c6;
}

/* Header */
.header {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  background: linear-gradient(135deg, #0082c6 100%, #0069a3 100%);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 80px;
  z-index: 1000;
  padding: 10px 20px 10px 70px;
  box-sizing: border-box;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.logo {
  width: 50px;
  margin-right: 2rem;
  margin-top: 2rem;
}

.button-group {
  display: flex;
  gap: 15px;
  align-items: center;
  margin-left: 120px;
  position: relative;
}

.button-group button {
  padding: 12px 24px;
  border: none;
  background: white;
  cursor: pointer;
  border-radius: 8px;
  color: #0082c6;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.button-group button::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 130, 198, 0.1);
  transform: scaleX(0);
  transform-origin: right;
  transition: transform 0.3s ease;
}

.button-group button:hover::before {
  transform: scaleX(1);
  transform-origin: left;
}

.button-group button:hover {
  background: #f8fafc;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  color: #ffffff;
}

.button-group button.active:hover {
  background: #0069a3;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

/* Main layout */
.main-layout {
  display: flex;
  margin-top: 80px;
  min-height: calc(100vh - 80px);
}

/* Sidebar */
.sidebar {
  width: 220px;
  background: linear-gradient(180deg, #0082c6 100%, #0069a3 100%);
  position: fixed;
  left: 0;
  height: calc(100vh - 80px);
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  z-index: 999;
}

/* Main content */
.main-content {
  flex: 1;
  padding: 20px 50px;
  background: #f8fafc;
  margin-left: 220px;
  width: calc(100% - 220px);
  box-sizing: border-box;
}

/* Filter search */
.filter-search {
  display: flex;
  gap: 15px;
  margin-bottom: 25px;
}

.filter-btn {
  padding: 12px 24px;
  background: #0082c6;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.filter-btn:hover {
  background: #0082c6 ;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

/* Filter form */
.filter-form {
  border: 1px solid #e2e8f0;
  padding: 20px;
  border-radius: 12px;
  background: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.filter-form div {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.filter-form div > div {
  flex: 1 1 200px;
}

.filter-form label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #1e293b;
}

.filter-form input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  box-sizing: border-box;
  transition: all 0.3s ease;
  font-size: 14px;
}

.filter-form input:focus {
  outline: none;
  border-color: #0082c6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Research list */
.research-list {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.research-item {
  display: flex;
  align-items: center;
  gap: 25px;
  padding: 20px;
  border: 1px solid #e2e8f0;
  background: white;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.research-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  border-color: #0082c6;
}

.research-logo {
  width: 85px;
  height: 100px;
  object-fit: contain;
  border-radius: 8px;
}

.research-info {
  flex: 1;
}

.research-info p {
  margin: 8px 0;
  color: #334155;
  font-size: 14px;
  line-height: 1.5;
}

.research-info p strong {
  color: #0082c6;
  font-weight: 600;
}

/* Responsive */

/* Tablet (≤1024px) */
@media (max-width: 1024px) {
  .header {
    padding: 10px 20px;
  }

  .main-content {
    margin-left: 200px;
    width: calc(100% - 200px);
    padding: 25px 30px;
  }

  .sidebar {
    width: 200px;
  }

  .button-group {
    margin-left: 15px;
    gap: 12px;
  }

  .button-group button {
    padding: 10px 20px;
    font-size: 13px;
  }

  .filter-form div {
    gap: 15px;
  }

  .filter-form div > div {
    flex: 1 1 180px;
  }
}

/* Mobile (≤768px) */
@media (max-width: 768px) {
  .header {
    flex-wrap: wrap;
    padding: 10px 15px;
    height: auto;
    min-height: 80px;
  }

  .sidebar-toggle {
    display: block;
    position: absolute;
    left: 15px;
    top: 15px;
    background: rgba(255, 255, 255, 0.2);
    color: white;
    border: none;
    padding: 8px 12px;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.3s ease;
  }

  .sidebar-toggle:hover {
    background: rgba(255, 255, 255, 0.3);
  }

  .logo {
    margin-left: 50px;
    order: 1;
  }

  .button-group {
    order: 2;
    width: 100%;
    justify-content: flex-start;
    gap: 8px;
    margin-top: 10px;
    margin-left: 0;
  }

  .main-layout {
    flex-direction: column;
    margin-top: 120px;
  }

  .sidebar {
    width: 200px;
    left: -200px;
    top: 0;
    height: 100vh;
  }

  .sidebar-open {
    left: 0;
  }

  .main-content {
    margin-left: 0;
    width: 100%;
    padding: 20px;
  }

  .filter-btn {
    padding: 10px 20px;
    font-size: 13px;
  }

  .filter-form div {
    flex-direction: column;
    gap: 15px;
  }

  .filter-form div > div {
    flex: 1 1 auto;
  }

  .research-item {
    flex-direction: row;
    gap: 15px;
    padding: 15px;
  }

  .button-group button {
    padding: 8px 16px;
    font-size: 13px;
  }
}

/* Small Mobile (≤480px) */
@media (max-width: 480px) {
  .header {
    padding: 8px 12px;
  }

  .logo {
    width: 40px;
    margin-left: 50px;
  }

  .button-group {
    flex-direction: column;
    gap: 5px;
    align-items: flex-start;
  }

  .button-group button {
    width: 100%;
    padding: 10px 15px;
    font-size: 12px;
  }

  .sidebar {
    width: 180px;
    left: -180px;
  }

  .sidebar-open {
    left: 0;
  }

  .main-content {
    padding: 15px;
  }

  .filter-btn {
    width: 100%;
    padding: 10px 15px;
  }

  .filter-form {
    padding: 15px;
  }

  .filter-form input {
    padding: 8px 10px;
    font-size: 13px;
  }

  .research-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
    padding: 12px;
  }

  .research-logo {
    width: 60px;
    height: 70px;
  }

  .research-info p {
    font-size: 13px;
    margin: 6px 0;
  }
}
</style>