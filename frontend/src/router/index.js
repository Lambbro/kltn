import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Login from '../views/Login&Register/Login.vue';
import Register from '../views/Login&Register/Register.vue';
import Info from '../views/Account/Info.vue';
import Training from '../views/Account/Training.vue';
import Education from '../views/Account/Education.vue';
import Work_experience from '../views/Account/Work_experience.vue';
import Teaching_activities from '../views/Account/Teaching_activities.vue';
import Research from '../views/Account/Research.vue';
import Research_results from '../views/Account/Research_results.vue';
import ApplyStudent from '../views/DangKyNCKH/SInhVien/ApplyStudents.vue';
import ApplyTeacher from '../views/DangKyNCKH/GiangVien/ApplyTeachers.vue';
import ApplyTopicStudents from '../views/DangKyNCKH/SInhVien/ApplyTopicStudents.vue';
import DeTaiNCKH from '../views/DeTaiNCKH/SinhVien/DeTaiNCKH.vue';
import ChiTietDeTai from '../views/DeTaiNCKH/SinhVien/ChiTietDeTai.vue';
import DeTaiDangThucHienSinhVien from '../views/DeTaiNCKH/SinhVien/DeTaiDangThucHienSinhVien.vue';
import DeTaiDangThucHienGV from '../views/DeTaiNCKH/GiangVien/DeTaiDangThucHienGV.vue';
import Introduce from '../views/Introduction/Introduction.vue';
import InfoStudents from '../views/Account/InfoStudents.vue';
import DeTaiSinhVien from '@/views/DeTaiNCKH/SinhVien/DeTaiSinhVien.vue'
import QuaTrinhThucHien from '../views/BaoCaoNCKH/SinhVien/QuaTrinhThucHien.vue';
import DeTaiNCKHGV from '../views/DeTaiNCKH/GiangVien/DeTaiNCKHGV.vue';
import QuaTrinhThucHienGV from '../views/BaoCaoNCKH/GiangVien/QuaTrinhThucHien.vue';
import managerTo from './managerTo';
import managerPhong from './managerPhong';

import { useAuthStore } from '../stores/auth';

const routes = [
  ...managerTo.options.routes,
  ...managerPhong.options.routes,
  { path: '/', component: Home },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/introduce', component: Introduce },

  //router cho trang thông tin cá nhân
  { path: '/info', component: Info, props: (route) => ({ ma_gv: route.query.ma_gv, viewOnly: route.query.viewOnly === 'true' }) },
  { path: '/info-students', component: InfoStudents},
  { path: '/education', component: Education, props: (route) => ({ ma_gv: route.query.ma_gv, viewOnly: route.query.viewOnly === 'true' }) },
  { path: '/training', component: Training, props: (route) => ({ ma_gv: route.query.ma_gv, viewOnly: route.query.viewOnly === 'true' }) },
  { path: '/work-experience', component: Work_experience, props: (route) => ({ ma_gv: route.query.ma_gv, viewOnly: route.query.viewOnly === 'true' }) },
  { path: '/teaching-activities', component: Teaching_activities, props: (route) => ({ ma_gv: route.query.ma_gv, viewOnly: route.query.viewOnly === 'true' }) },
  { path: '/research', component: Research, props: (route) => ({ ma_gv: route.query.ma_gv, viewOnly: route.query.viewOnly === 'true' }) },
  { path: '/research-results', component: Research_results, props: (route) => ({ ma_gv: route.query.ma_gv, viewOnly: route.query.viewOnly === 'true' }) },

  //router cho trang đăng ký
  { path: '/apply-students', component: ApplyStudent },
  { path: '/apply-teachers', component: ApplyTeacher },
  { path: '/apply-topic-students', component: ApplyTopicStudents },

  // Route cho đề tài
  { path: '/de-tai-nckh', component: DeTaiNCKH },
  { path: '/chi-tiet-de-tai/:id', name: 'chi-tiet-de-tai', component: ChiTietDeTai },
  { path: '/de-tai-dang-thuc-hien-sinh-vien', component: DeTaiDangThucHienSinhVien },
  { path: '/de-tai-sinh-vien', component: DeTaiSinhVien},
  { path: '/de-tai-dang-thuc-hien-gv', component: DeTaiDangThucHienGV},
  { path: '/de-tai-nckh-gv', component: DeTaiNCKHGV},
  { path: '/qua-trinh-thuc-hien', component: QuaTrinhThucHien},
  { path: '/qua-trinh-thuc-hien-gv', component: QuaTrinhThucHienGV},
];
const router = createRouter({
  history: createWebHistory(),
  routes
});

// Global guard: yêu cầu đăng nhập mới được truy cập một số trang (nếu cần)
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();

  // Nếu route có meta.requiresAuth = true mà store chưa có user => chuyển login
  if (to.meta.requiresAuth && !authStore.user) {
    next('/login');
  } else {
    next();
  }
});

export default router;
