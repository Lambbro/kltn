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
                    <button class="filter-btn" @click="showFilter = !showFilter">
                        <i :class="['fas', showFilter ? 'fa-filter-circle-xmark' : 'fa-filter']"></i>
                        {{ showFilter ? 'Ẩn bộ lọc' : 'Hiện bộ lọc' }}
                    </button>
                </div>

                <!-- Form bộ lọc -->
                <div v-if="showFilter" class="filter-form">
                    <div class="filter-row">
                        <div class="filter-group">
                            <label>
                                <i class="fas fa-book"></i>
                                Tên đề tài
                            </label>
                            <input 
                                type="text" 
                                v-model="filterCriteria.title" 
                                placeholder="Nhập tên đề tài..."
                                @input="handleFilterChange"
                            />
                        </div>
                        <div class="filter-group">
                            <label>
                                <i class="fas fa-chalkboard-teacher"></i>
                                Giảng viên hướng dẫn
                            </label>
                            <input 
                                type="text" 
                                v-model="filterCriteria.researcher" 
                                placeholder="Nhập tên giảng viên..."
                                @input="handleFilterChange"
                            />
                        </div>
                        <div class="filter-group">
                            <label>
                                <i class="fas fa-users"></i>
                                Thành viên
                            </label>
                            <input 
                                type="text" 
                                v-model="filterCriteria.members" 
                                placeholder="Nhập tên thành viên..."
                                @input="handleFilterChange"
                            />
                        </div>
                    </div>
                    <div class="filter-row">
                        <div class="filter-group">
                            <label>
                                <i class="fas fa-calendar"></i>
                                Đợt thực hiện
                            </label>
                            <input 
                                type="text" 
                                v-model="filterCriteria.year" 
                                placeholder="Nhập đợt thực hiện..."
                                @input="handleFilterChange"
                            />
                        </div>
                        <div class="filter-group">
                            <label>
                                <i class="fas fa-flask"></i>
                                Hướng nghiên cứu
                            </label>
                            <div class="research-direction-input">
                                <input 
                                    type="text" 
                                    v-model="filterCriteria.huongNC" 
                                    placeholder="Nhập hoặc chọn hướng nghiên cứu..."
                                    @input="handleFilterChange"
                                />
                                <div class="dropdown-content" v-if="showResearchDirections">
                                    <div 
                                        v-for="direction in filteredResearchDirections" 
                                        :key="direction.id"
                                        class="dropdown-item"
                                        @click="selectResearchDirection(direction)"
                                    >
                                        {{ direction.name }}
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="filter-actions">
                            <button class="reset-btn" @click="resetFilters">
                                <i class="fas fa-undo"></i>
                                Đặt lại bộ lọc
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Vùng hiển thị danh sách đề tài, sử dụng filteredTopics -->
                <div class="research-list">
                    <div 
                      class="research-item"
                      v-for="(item, index) in filteredTopics" 
                      :key="index"
                      @click="goToDetailPage(item.ma_de_tai)"
                    >
                        <img src="@/assets/img/logo-hou.png" alt="Logo" class="research-logo"/>
                        <div class="research-info">
                            <p><strong>Tên đề tài:</strong> {{ item.ten_de_tai }}</p>
                            <p><strong>Giảng viên hướng dẫn:</strong> {{ item.ten_gv }}</p>
                            <p><strong>Thành viên:</strong> 
                              <ul class="research-members">
                                <li v-for="member in item.thanh_vien" :key="member.ma_sv">
                                  {{ member.ten_sv }}
                                </li>
                              </ul>
                            </p>
                            <p><strong>Đợt thực hiện:</strong> {{ item.dot_thuc_hien }}</p>
                            <p><strong>Hướng nghiên cứu:</strong> 
                                <ul class="research-directions">
                                    <li v-for="direction in item.huong_nghien_cuu" :key="direction.ma_hnc">
                                        {{ direction.ten_hnc }}
                                    </li>
                                </ul>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import SidebarHome from '@/components/SidebarHome.vue';
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import api from '@/config/api';

const router = useRouter();
const authStore = useAuthStore();

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
const researchTopics = ref([]);
const loading = ref(true);

// Biến điều khiển việc hiện/ẩn form bộ lọc
const showFilter = ref(false);

// Đối tượng chứa các tiêu chí lọc
const filterCriteria = ref({
    title: '',
    researcher: '',
    members: '',
    year: '',
    huongNC: '',
    result: ''
});

// Danh sách hướng nghiên cứu
const researchDirections = ref([
    { id: 1, name: 'Công nghệ thông tin' },
    { id: 2, name: 'Khoa học máy tính' },
    { id: 3, name: 'Trí tuệ nhân tạo' },
    { id: 4, name: 'Hệ thống thông tin' },
    { id: 5, name: 'Mạng máy tính' },
    { id: 6, name: 'An toàn thông tin' },
    { id: 7, name: 'Khoa học dữ liệu' },
    { id: 8, name: 'Công nghệ phần mềm' }
]);

// Thêm các biến mới
const showResearchDirections = ref(false);
const filteredResearchDirections = ref([]);

// Hàm xử lý thay đổi bộ lọc
const handleFilterChange = () => {
    // Xử lý hiển thị dropdown hướng nghiên cứu
    if (filterCriteria.value.huongNC) {
        filteredResearchDirections.value = researchDirections.value.filter(direction => 
            direction.name.toLowerCase().includes(filterCriteria.value.huongNC.toLowerCase())
        );
        showResearchDirections.value = true;
    } else {
        showResearchDirections.value = false;
    }
};

// Hàm chọn hướng nghiên cứu từ dropdown
const selectResearchDirection = (direction) => {
    filterCriteria.value.huongNC = direction.name;
    showResearchDirections.value = false;
};

// Hàm reset bộ lọc
const resetFilters = () => {
    filterCriteria.value = {
        title: '',
        researcher: '',
        members: '',
        year: '',
        huongNC: ''
    };
};

// Computed property để áp dụng các điều kiện lọc
const filteredTopics = computed(() => {
    return researchTopics.value.filter((item) => {
        // Kiểm tra từng trường với tìm kiếm tương đối
        const matchTitle = fuzzySearch(item.ten_de_tai, filterCriteria.value.title);
        const matchResearcher = fuzzySearch(item.ten_gv, filterCriteria.value.researcher);
        const matchYear = fuzzySearch(item.dot_thuc_hien, filterCriteria.value.year);
        const matchHuongNC = fuzzySearch(
            item.huong_nghien_cuu.map(d => d.ten_hnc).join(' '), 
            filterCriteria.value.huongNC
        );
        
        // Kiểm tra thành viên
        const matchMembers = !filterCriteria.value.members || 
            item.thanh_vien.some(member => 
                fuzzySearch(member.ten_sv, filterCriteria.value.members)
            );

        return matchTitle && matchResearcher && matchYear && matchHuongNC && matchMembers;
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

// Hàm lấy trạng thái
function getStatusText(status) {
  switch (status) {
    case 0: return 'Đã hủy';
    case 1: return 'Đang thực hiện';
    case 2: return 'Hoàn thành';
    default: return 'Không xác định';
  }
}

// Hàm lấy class trạng thái
function getStatusClass(status) {
  switch (status) {
    case 0: return 'status-pending';
    case 1: return 'status-in-progress';
    case 2: return 'status-completed';
    default: return 'status-unknown';
  }
}

// Fetch topics
const fetchTopics = async () => {
  try {
    loading.value = true;
    const response = await api.get('get_data/detai_sv/hoan_thanh');
    researchTopics.value = response.data;
    console.log('Fetched topics:', researchTopics.value);
  } catch (error) {
    console.error('Error fetching topics:', error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchTopics();
});
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
    background: white;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    margin-bottom: 1.5rem;
    border: 1px solid #e2e8f0;
}

.filter-row {
    display: flex;
    flex-wrap: wrap;
    gap: 1.5rem;
    margin-bottom: 1.5rem;
}

.filter-row:last-child {
    margin-bottom: 0;
}

.filter-group {
    flex: 1 1 300px;
}

.filter-group label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
    color: #1a3c5e;
    font-weight: 600;
    font-size: 0.95rem;
}

.filter-group label i {
    color: #0082c6;
    font-size: 1rem;
}

.filter-group input {
    width: 100%;
    padding: 0.75rem 1rem;
    border: 2px solid #e2e8f0;
    border-radius: 8px;
    font-size: 0.95rem;
    transition: all 0.3s ease;
    background-color: #f8fafc;
}

.filter-group input:focus {
    outline: none;
    border-color: #0082c6;
    box-shadow: 0 0 0 3px rgba(0, 130, 198, 0.1);
    background-color: white;
}

.research-direction-input {
    position: relative;
}

.dropdown-content {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    margin-top: 0.25rem;
    max-height: 200px;
    overflow-y: auto;
    z-index: 1000;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.dropdown-item {
    padding: 0.75rem 1rem;
    cursor: pointer;
    transition: all 0.2s ease;
}

.dropdown-item:hover {
    background: #f0f7ff;
    color: #0082c6;
}

.filter-actions {
    display: flex;
    align-items: flex-end;
    justify-content: flex-end;
    flex: 1 1 300px;
}

.reset-btn {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1.5rem;
    background: #f3f4f6;
    color: #4b5563;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 500;
    transition: all 0.3s ease;
}

.reset-btn:hover {
    background: #e5e7eb;
    color: #1f2937;
    transform: translateY(-2px);
}

.reset-btn i {
    font-size: 0.9rem;
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

/* Research directions */
.research-directions {
    display: flex;
    flex-direction: column;
    gap: 8px;
    list-style: none;
    padding: 0;
    margin: 8px 0 0 0;
}

.research-directions li {
    background-color: #f0f7ff;
    color: #0082c6;
    padding: 6px 12px;
    border-radius: 16px;
    font-size: 13px;
    border: 1px solid #e6f2ff;
    transition: all 0.3s ease;
    width: fit-content;
    margin-left: 10px;
}
.research-directions li:last-child {
  margin-right: 0;
}

.research-directions li:hover {
    background-color: #e6f2ff;
    transform: translateX(2px);
}

.research-members {
  background-color: #f0f7ff;
    color: #0082c6;
    padding: 6px 12px;
    border-radius: 16px;
    font-size: 13px;
    border: 1px solid #e6f2ff;
    transition: all 0.3s ease;
    width: fit-content;
    margin-left: 10px;
}
.research-members li {
  margin-right: 5px;
  list-style: none;
}

.research-members li:last-child {
  margin-right: 0;
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

  .filter-row {
    flex-direction: column;
    gap: 1rem;
  }

  .filter-group {
    flex: 1 1 100%;
  }

  .filter-actions {
    justify-content: center;
    margin-top: 1rem;
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

/* Status classes */
.status-pending {
  color: #f59e0b;
  font-weight: 500;
}

.status-in-progress {
  color: #0082c6;
  font-weight: 500;
}

.status-completed {
  color: #10b981;
  font-weight: 500;
}

.status-unknown {
  color: #64748b;
  font-weight: 500;
}

.filter-select {
    width: 100%;
    padding: 10px 12px;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    box-sizing: border-box;
    transition: all 0.3s ease;
    font-size: 14px;
    background-color: white;
    cursor: pointer;
    appearance: none;
    background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
    background-repeat: no-repeat;
    background-position: right 10px center;
    background-size: 15px;
}

.filter-select:focus {
    outline: none;
    border-color: #0082c6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.filter-select option {
    padding: 10px;
  }
</style>