<template>
  <div class="upload-container">
    <div v-if="imageUrl" class="image-preview">
      <img :src="imageUrl" alt="Image Preview" />
    </div>
    <input type="file" @change="onFileChange" accept="image/*" ref="fileInput" style="display: none;" />
    <button @click="triggerFileInput" :disabled="disabled">Thay đổi ảnh</button>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import api from '@/config/api';

const props = defineProps({
  imageUrl: {
    type: String,
    default: ''
  },
  disabled: {
    type: Boolean,
    default: false
  },
  maGv: {
    type: String,
    required: true
  }
});

const emit = defineEmits(['update:image']);
const fileInput = ref(null);

const convertToBase64 = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
};

const triggerFileInput = () => {
  if (!props.disabled) {
    fileInput.value.click();
  }
};

const onFileChange = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  // Kiểm tra kích thước file (5MB)
  if (file.size > 5 * 1024 * 1024) {
    alert('File ảnh không được vượt quá 5MB');
    return;
  }

  // Kiểm tra loại file
  if (!file.type.startsWith('image/')) {
    alert('Vui lòng chọn file ảnh');
    return;
  }

  try {
    // Gửi file qua FormData
    const formData = new FormData();
    formData.append('image', file);
    formData.append('ma_gv', props.maGv);

    console.log('Sending FormData:', { ma_gv: props.maGv, file: file.name });

    // Gửi request tới API
    const response = await api.post(`/phongkhdn/gv/update/${props.maGv}/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });

    if (response.data?.success) {
      const newImageUrl = response.data.link_tep; // Đường dẫn file từ server
      console.log('Upload success:', response.data);
      emit('update:image', newImageUrl);
      alert('Cập nhật ảnh thành công!');
      fileInput.value.value = ''; // Reset input file
    } else {
      throw new Error(response.data?.message || 'Lỗi không xác định từ server');
    }
  } catch (error) {
    console.error('Error uploading image:', error);
    console.log('Error response:', error.response?.data);
    alert(`Có lỗi xảy ra khi cập nhật ảnh: ${error.message}`);
  }
};
</script>

<style scoped>
.upload-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.image-preview {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  border: 2px solid #ccc;
  margin-bottom: 10px;
}

.image-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

button {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 8px 16px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 14px;
  margin: 4px 2px;
  cursor: pointer;
  border-radius: 4px;
}

button:hover:not(:disabled) {
  background-color: #45a049;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style>