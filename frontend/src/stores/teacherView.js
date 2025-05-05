import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useTeacherViewStore = defineStore('teacherView', () => {
  // Lưu trữ mã giảng viên đang được xem
  const currentTeacherId = ref(null);
  
  // Lưu trữ mã giảng viên đang được xem
  function setCurrentTeacherId(ma_gv) {
    currentTeacherId.value = ma_gv;
  }
  
  // Lấy mã giảng viên đang được xem
  function getCurrentTeacherId() {
    return currentTeacherId.value;
  }
  
  // Xóa mã giảng viên đang được xem
  function clearCurrentTeacherId() {
    currentTeacherId.value = null;
  }
  
  return {
    currentTeacherId,
    setCurrentTeacherId,
    getCurrentTeacherId,
    clearCurrentTeacherId
  };
}); 