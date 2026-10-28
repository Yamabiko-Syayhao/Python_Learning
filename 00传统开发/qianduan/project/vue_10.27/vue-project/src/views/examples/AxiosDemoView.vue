<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { ref } from 'vue'
import { getAdmins } from '@/api/admin'
import { errorMessage } from '@/api/http'
const loading = ref(false)
const result = ref('')
const error = ref('')
async function sendRequest() {
  loading.value = true
  error.value = ''
  result.value = ''
  try {
    const page = await getAdmins(1, 5)
    // Pick public table columns explicitly; never display unexpected token/password fields.
    result.value = JSON.stringify(
      {
        count: page.count,
        list: page.list.map((item) => ({
          id: item.id,
          name: item.name,
          userName: item.userName,
          role: item.role,
          lastLoginAt: item.lastLoginAt,
          createdAt: item.createdAt ?? item.createAt,
        })),
      },
      null,
      2,
    )
  } catch (cause) {
    error.value = errorMessage(cause)
  } finally {
    loading.value = false
  }
}
</script>
<template>
  <el-card shadow="never"
    ><template #header><strong>Axios 接口请求</strong></template>
    <p>登录、注册和角色管理均通过 Axios 调用接口文档中的服务。</p>
    <el-steps :active="3" finish-status="success" align-center
      ><el-step title="填写表单" /><el-step title="发送请求" /><el-step title="展示返回数据"
    /></el-steps>
    <div class="action">
      <el-button type="primary" :loading="loading" @click="sendRequest"
        >请求前 5 条角色数据</el-button
      ><RouterLink to="/admin/roles"><el-button>前往角色管理</el-button></RouterLink>
    </div>
    <el-alert v-if="error" :title="error" type="error" :closable="false" show-icon />
    <pre v-if="result">{{ result }}</pre>
  </el-card>
</template>
<style scoped>
p {
  color: #606266;
  margin: 0 0 32px;
}
.action {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin: 32px 0 20px;
}
a {
  text-decoration: none;
}
pre {
  max-height: 460px;
  overflow: auto;
  padding: 20px;
  background: #f6f8fa;
  color: #303133;
  border-radius: 4px;
  line-height: 1.6;
}
</style>
