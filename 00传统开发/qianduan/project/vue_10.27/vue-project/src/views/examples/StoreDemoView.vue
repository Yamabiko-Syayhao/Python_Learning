<script setup lang="ts">
import { useCounterStore } from '@/stores/counter'
const counter = useCounterStore()
</script>
<template>
  <el-card shadow="never"
    ><template #header><strong>Pinia 状态管理</strong></template>
    <p>复用项目的 Pinia 计数器，切换页面后保留当前会话中的状态。</p>
    <div class="stats">
      <el-statistic title="当前计数" :value="counter.count" /><el-statistic
        title="两倍计数"
        :value="counter.doubleCount"
      />
    </div>
    <el-button type="primary" @click="counter.increment">增加 1</el-button
    ><el-button @click="counter.count = 0">重置</el-button></el-card
  >
</template>
<style scoped>
p {
  color: #606266;
  margin: 0 0 24px;
}
.stats {
  display: flex;
  gap: 80px;
  margin: 24px 0;
}
</style>
