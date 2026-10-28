<script setup lang="ts">
import { ref, type Directive } from 'vue'
const color = ref('#409eff')
const vTextColor: Directive<HTMLElement, string> = {
  mounted: (el, binding) => {
    el.style.color = binding.value
  },
  updated: (el, binding) => {
    el.style.color = binding.value
  },
}
</script>
<template>
  <el-card shadow="never"
    ><template #header><strong>自定义指令</strong></template>
    <p>使用局部指令 v-text-color，为文字绑定可变化的颜色。</p>
    <div class="color-row">
      <span>文字颜色</span><el-color-picker v-model="color" :show-alpha="false" />
    </div>
    <div v-text-color="color || '#409eff'" class="sample">你好，Vue 自定义指令！</div></el-card
  >
</template>
<style scoped>
p {
  color: #606266;
  margin: 0 0 24px;
}
.color-row {
  display: flex;
  align-items: center;
  gap: 16px;
}
.sample {
  margin-top: 24px;
  padding: 24px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 24px;
}
</style>
