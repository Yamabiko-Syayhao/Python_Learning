<script setup lang="ts">
import { ref } from 'vue'
import MessagePreview from './MessagePreview.vue'
const message = ref('你好，Vue！')
const reply = ref('')
</script>
<template>
  <el-card shadow="never"
    ><template #header><strong>组件传参</strong></template>
    <p>父组件通过 props 传递内容，子组件通过 emit 返回消息。</p>
    <el-input
      v-model="message"
      maxlength="100"
      placeholder="输入传给子组件的内容"
      class="message-input" /><MessagePreview
      :message="message"
      @acknowledge="reply = `父组件已收到：${$event}`" /><el-alert
      v-if="reply"
      :title="reply"
      type="success"
      :closable="false"
      show-icon
      class="result"
  /></el-card>
</template>
<style scoped>
p {
  margin: 0 0 20px;
  color: #606266;
}
.message-input {
  margin-bottom: 20px;
  max-width: 560px;
}
.result {
  margin-top: 20px;
}
</style>
