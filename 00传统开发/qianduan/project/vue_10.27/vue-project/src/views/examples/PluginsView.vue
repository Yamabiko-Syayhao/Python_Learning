<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
const enabled = ref(true)
const date = ref('')
</script>
<template>
  <el-card shadow="never"
    ><template #header><strong>Element Plus 组件</strong></template>
    <p>项目已全局引入 Element Plus，下列控件可直接使用。</p>
    <el-form label-width="90px"
      ><el-form-item label="状态开关"
        ><el-switch v-model="enabled" active-text="启用" inactive-text="关闭" /></el-form-item
      ><el-form-item label="日期选择"
        ><el-date-picker
          v-model="date"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="选择日期" /></el-form-item
      ><el-form-item
        ><el-button type="primary" @click="ElMessage.success('Element Plus 消息提示已正常加载')"
          >显示消息</el-button
        ></el-form-item
      ></el-form
    ></el-card
  >
</template>
<style scoped>
p {
  color: #606266;
  margin: 0 0 24px;
}
</style>
