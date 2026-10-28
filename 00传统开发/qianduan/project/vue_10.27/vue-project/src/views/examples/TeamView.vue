<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { request, errorMessage } from '@/api/http'
interface Team {
  teamId: number
  teamName: string
  teamEmail: string
  teamDescription: string
  createdAt: string
}
const teams = ref<Team[]>([])
const page = ref(1)
const count = ref(0)
const loading = ref(false)
const error = ref('')
async function load() {
  loading.value = true
  error.value = ''
  try {
    const result = await request<{ list: Team[]; count: number }>({
      method: 'GET',
      url: '/team',
      params: { page: page.value, rows: 10 },
    })
    if (!result || !Array.isArray(result.list) || !Number.isFinite(Number(result.count)))
      throw new Error('团队列表返回格式不正确')
    teams.value = result.list
    count.value = Number(result.count)
  } catch (cause) {
    error.value = errorMessage(cause)
  } finally {
    loading.value = false
  }
}
onMounted(load)
</script>
<template>
  <el-card shadow="never"
    ><template #header
      ><div class="heading">
        <strong>募捐团队</strong><el-button :loading="loading" @click="load">刷新</el-button>
      </div></template
    ><el-alert
      v-if="error"
      :title="error"
      type="error"
      :closable="false"
      show-icon
      class="error" /><el-table
      v-loading="loading"
      :data="teams"
      border
      stripe
      empty-text="暂无团队数据"
      ><el-table-column prop="teamId" label="ID" width="80" /><el-table-column
        prop="teamName"
        label="团队名称"
        min-width="160" /><el-table-column
        prop="teamEmail"
        label="联系邮箱"
        min-width="200" /><el-table-column
        prop="teamDescription"
        label="团队介绍"
        min-width="220"
        show-overflow-tooltip /><el-table-column
        prop="createdAt"
        label="创建时间"
        min-width="180" /></el-table
    ><el-pagination
      v-model:current-page="page"
      :page-size="10"
      :total="count"
      layout="total, prev, pager, next"
      class="pagination"
      :disabled="loading"
      @current-change="load"
  /></el-card>
</template>
<style scoped>
.heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.error {
  margin-bottom: 20px;
}
.pagination {
  justify-content: flex-end;
  margin-top: 24px;
}
</style>
