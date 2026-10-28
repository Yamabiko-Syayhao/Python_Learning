<script setup lang="ts">
defineProps<{ message: string }>()
const emit = defineEmits<{ acknowledge: [message: string] }>()
</script>
<template>
  <div class="preview">
    <span>子组件收到：{{ message || '请在上方输入内容' }}</span
    ><el-button :disabled="!message.trim()" @click="emit('acknowledge', message)"
      >通知父组件</el-button
    >
  </div>
</template>
<style scoped>
.preview {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
  padding: 20px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
}
</style>
