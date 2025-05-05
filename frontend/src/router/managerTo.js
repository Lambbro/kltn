import { createRouter, createWebHistory } from "vue-router";
import ManagerHomeTo from '@/views/Manager/ManagerHomeTo.vue'
import ManagerApplyStudents from "@/views/Manager/Students/ManagerApplyStudents.vue";
import ManagerTopicStudentBeingDone from "@/views/Manager/Students/ManagerTopicStudentBeingDone.vue";
import ManagerTopicStudents from "@/views/Manager/Students/ManagerTopicStudents.vue";
import ManagerListTeachers from "@/views/Manager/Facultys/ManagerListTeachers.vue";
import ManangerListStudents from "@/views/Manager/Facultys/ManangerListStudents.vue";
import ManagerApplyTopicStudents from "@/views/Manager/Students/ManagerApplyTopicStudents.vue";
import ManagerResult from "@/views/Manager/Students/ManagerResult.vue";
import ManagerResearchTopic from "@/views/Manager/Facultys/ManagerResearchTopic.vue";
import ManagerNotificationTo from "@/views/Manager/Notification/ManagerNotificationTo.vue";
import { useAuthStore } from "@/stores/auth";

const routes = [
    { path: '/manager-home-to', component: ManagerHomeTo },
    { path: '/manager-list-teachers', component: ManagerListTeachers },
    { path: '/manager-list-students', component: ManangerListStudents },
    { path: '/manager-apply-students', component: ManagerApplyStudents },
    { path: '/manager-apply-topic-students', component: ManagerApplyTopicStudents},
    { path: '/manager-topic-students', component: ManagerTopicStudents },
    { path: '/manager-topic-student-being-done', component: ManagerTopicStudentBeingDone },
    { path: '/manager-result', component: ManagerResult },
    { path: '/manager-research-topic', component: ManagerResearchTopic },
    { path: '/manager-notification-to-nckh', component: ManagerNotificationTo },
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