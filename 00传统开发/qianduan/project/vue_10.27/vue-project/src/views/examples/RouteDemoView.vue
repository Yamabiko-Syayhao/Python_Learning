<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
const route = useRoute()
const router = useRouter()
const name = ref(typeof route.query.name === 'string' ? route.query.name : '')
const currentName = computed(() =>
  typeof route.query.name === 'string' ? route.query.name : '尚未传入',
)
watch(
  () => route.query.name,
  (value) => {
    name.value = typeof value === 'string' ? value : ''
  },
)
function send() {
  void router.push({
    path: '/admin/route-demo',
    query: name.value.trim() ? { name: name.value.trim() } : {},
  })
}
</script>
<template>
  <el-card shadow="never"
    ><template #header><strong>路由传参</strong></template>
    <p>输入姓名后，参数会写入当前路由的 query。刷新页面仍能读取。</p>
    <el-form inline @submit.prevent="send"
      ><el-form-item label="姓名"
        ><el-input v-model="name" placeholder="请输入姓名" maxlength="50" /></el-form-item
      ><el-form-item
        ><el-button native-type="submit" type="primary">传递参数</el-button></el-form-item
      ></el-form
    ><el-descriptions :column="1" border
      ><el-descriptions-item label="当前路径">{{ route.path }}</el-descriptions-item
      ><el-descriptions-item label="name 参数">{{
        currentName
      }}</el-descriptions-item></el-descriptions
    ></el-card
  >
</template>
<style scoped>
p {
  margin: 0 0 20px;
  color: #606266;
}
</style>
