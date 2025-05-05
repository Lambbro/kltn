import {createRouter, createWebHistory} from "vue-router";
import ManagerHomePhong from '@/views/Manager/ManagerHomePhong.vue';
import ManagerListFacultys from "@/views/Manager/Facultys/ManagerListFacultys.vue";
import ManagerListAccount from "@/views/Manager/Facultys/ManagerListAccount.vue";
import ManagerResult from "@/views/Manager/Students/ManagerResult.vue";
import ManagerApplyTeachers from "@/views/Manager/Teachers/ManagerApplyTeachers.vue";
import ManagerTopicTeachers from "@/views/Manager/Teachers/ManagerTopicTeachers.vue";
import ManagerTopicTeacherBeingDone from "@/views/Manager/Teachers/ManagerTopicTeacherBeingDone.vue";
import ManagerListReachTopic from "@/views/Manager/PhongKHDN/ManagerListReachTopic.vue";
import ManagerNotificationPhong from "@/views/Manager/Notification/ManagerNotificationPhong.vue";
import { useAuthStore } from "@/stores/auth";

const routes = [
    { path: '/manager-home-phong', component: ManagerHomePhong },
    { path: '/manager-list-facultys', component: ManagerListFacultys },
    { path: '/manager-list-account', component: ManagerListAccount },
    { path: '/manager-apply-teachers', component: ManagerApplyTeachers },
    { path: '/manager-topic-teachers', component: ManagerTopicTeachers },
    { path: '/manager-topic-teachers-being-done', component: ManagerTopicTeacherBeingDone },
    { path: '/manager-result', component: ManagerResult },
    { path: '/manager-list-research-topics', component: ManagerListReachTopic },
    { path: '/manager-notification-phong', component: ManagerNotificationPhong },
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