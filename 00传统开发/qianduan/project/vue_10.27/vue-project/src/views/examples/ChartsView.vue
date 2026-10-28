<script setup lang="ts">
import { computed, ref } from 'vue'
const values = ref([40, 65, 52, 80, 92])
const max = computed(() => Math.max(...values.value, 1))
function changeValue(index: number, value: number | undefined) {
  values.value[index] = value ?? 0
}
</script>
<template>
  <el-card shadow="never"
    ><template #header><strong>数据图表</strong></template
    ><el-alert
      title="以下为可交互的图表示例数据，可调整数值查看变化。"
      type="info"
      :closable="false" />
    <div class="chart" role="img" :aria-label="`示例数据：${values.join('、')}`">
      <div v-for="(value, index) in values" :key="index" class="bar-group">
        <span>{{ value }}</span>
        <div class="bar" :style="{ height: `${(value / max) * 190}px` }" />
        <span>{{ index + 1 }} 月</span>
      </div>
    </div>
    <div class="controls">
      <el-input-number
        v-for="(value, index) in values"
        :key="index"
        :model-value="value"
        :min="0"
        :max="1000"
        :aria-label="`${index + 1}月示例数值`"
        size="small"
        @update:model-value="changeValue(index, $event)"
      /></div
  ></el-card>
</template>
<style scoped>
.chart {
  display: flex;
  align-items: flex-end;
  justify-content: space-around;
  gap: 18px;
  max-width: 760px;
  height: 270px;
  margin: 24px 0;
  padding: 0 12px 12px;
  border-bottom: 1px solid #dcdfe6;
}
.bar-group {
  flex: 1;
  display: flex;
  align-items: center;
  flex-direction: column;
  gap: 10px;
  color: #606266;
  font-size: 13px;
}
.bar {
  width: 70%;
  max-width: 70px;
  min-height: 2px;
  border-radius: 4px 4px 0 0;
  background: #409eff;
  transition: height 0.2s ease;
}
.controls {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}
</style>
