<!-- <script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

onMounted(async () => {
  const token = localStorage.getItem('access_token') || sessionStorage.getItem('access_token');
  if (token) {
    try {
      const res = await fetch('http://lamb.servebeer.com:8000/kiem-tra-token/', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!res.ok) {
        throw new Error('Token hết hạn');
      }

      console.log('Token hợp lệ');
    } catch (err) {
      console.error('Lỗi xác thực:', err.message);
      localStorage.clear();
      sessionStorage.clear();
      router.push('/login');
    }
  } else {
    router.push('/');
  }
});
</script> -->
<template>
  <router-view />
</template>
