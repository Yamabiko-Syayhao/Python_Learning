<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Refresh, Search } from '@element-plus/icons-vue'
import AdminAccountForm from '@/components/AdminAccountForm.vue'
import { createAdmin, deleteAdmin, getAdmins, getAllAdmins, updateAdmin } from '@/api/admin'
import { errorMessage } from '@/api/http'
import { emptyAdminForm, ROLE_OPTIONS, roleLabel } from '@/types/admin'
import type { AdminFormData, AdminPayload, AdminUser, Role } from '@/types/admin'

const loading = ref(false)
const loadError = ref('')
const page = ref(1)
const pageSize = ref(10)
const serverCount = ref(0)
const serverRows = ref<AdminUser[]>([])
const searchRows = ref<AdminUser[]>([])
const keywordInput = ref('')
const roleInput = ref<Role>()
const keyword = ref('')
const selectedRole = ref<Role>()
const filtering = computed(() => Boolean(keyword.value || selectedRole.value))
const filteredRows = computed(() => {
  const term = keyword.value.toLocaleLowerCase()
  return searchRows.value.filter(
    (row) =>
      (!selectedRole.value || row.role === selectedRole.value) &&
      (!term ||
        [row.id, row.name, row.userName, roleLabel(row.role)].some((value) =>
          String(value).toLocaleLowerCase().includes(term),
        )),
  )
})
const total = computed(() => (filtering.value ? filteredRows.value.length : serverCount.value))
const tableRows = computed(() =>
  filtering.value
    ? filteredRows.value.slice((page.value - 1) * pageSize.value, page.value * pageSize.value)
    : serverRows.value,
)
let controller: AbortController | undefined
let requestId = 0

async function loadRows() {
  controller?.abort()
  controller = new AbortController()
  const id = ++requestId
  loading.value = true
  loadError.value = ''
  try {
    if (filtering.value) {
      const result = await getAllAdmins(controller.signal)
      if (id !== requestId) return
      searchRows.value = result
      page.value = Math.min(
        page.value,
        Math.max(1, Math.ceil(filteredRows.value.length / pageSize.value)),
      )
    } else {
      const result = await getAdmins(page.value, pageSize.value, controller.signal)
      if (id !== requestId) return
      serverRows.value = result.list
      serverCount.value = result.count
      const maxPage = Math.max(1, Math.ceil(result.count / pageSize.value))
      if (page.value > maxPage) {
        page.value = maxPage
        await loadRows()
      }
    }
  } catch (error) {
    if (id !== requestId || axios.isCancel(error)) return
    loadError.value = errorMessage(error)
    serverRows.value = []
    searchRows.value = []
    serverCount.value = 0
  } finally {
    if (id === requestId) loading.value = false
  }
}

function search() {
  keyword.value = keywordInput.value.trim()
  selectedRole.value = roleInput.value
  page.value = 1
  void loadRows()
}
function resetSearch() {
  keywordInput.value = ''
  roleInput.value = undefined
  search()
}
function changePage(value: number) {
  page.value = value
  if (!filtering.value) void loadRows()
}
function changePageSize(value: number) {
  pageSize.value = value
  page.value = 1
  if (!filtering.value) void loadRows()
}

const dialogVisible = ref(false)
const editingId = ref<number | null>(null)
const accountForm = ref<InstanceType<typeof AdminAccountForm>>()
const form = ref<AdminFormData>(emptyAdminForm())
const saving = ref(false)
const saveError = ref('')
const deletingId = ref<number | null>(null)
function openCreate() {
  editingId.value = null
  form.value = emptyAdminForm()
  saveError.value = ''
  dialogVisible.value = true
}
function openEdit(row: AdminUser) {
  editingId.value = row.id
  // The PDF's detail example is inconsistent; editable fields are available in the list.
  form.value = { name: row.name, userName: row.userName, role: row.role, passWord: '' }
  saveError.value = ''
  dialogVisible.value = true
}
async function save() {
  if (saving.value) return
  saving.value = true
  saveError.value = ''
  try {
    if (!(await accountForm.value?.validate()) || !form.value.role) return
    const payload: AdminPayload = {
      name: form.value.name.trim(),
      userName: form.value.userName.trim(),
      passWord: form.value.passWord,
      role: form.value.role,
    }
    if (editingId.value !== null) await updateAdmin(editingId.value, payload)
    else await createAdmin(payload)
    ElMessage.success(editingId.value !== null ? '编辑成功' : '添加成功')
    dialogVisible.value = false
    form.value.passWord = ''
    await loadRows()
  } catch (error) {
    saveError.value = errorMessage(error)
  } finally {
    saving.value = false
  }
}
async function remove(row: AdminUser) {
  if (deletingId.value !== null) return
  try {
    await ElMessageBox.confirm(`确定删除用户“${row.name}”（${row.userName}）吗？`, '删除角色', {
      type: 'warning',
      confirmButtonText: '确定删除',
      cancelButtonText: '取消',
    })
  } catch {
    return
  }
  deletingId.value = row.id
  try {
    await deleteAdmin(row.id)
    ElMessage.success('删除成功')
    if (tableRows.value.length === 1 && page.value > 1) page.value -= 1
    await loadRows()
  } catch (error) {
    ElMessage.error(errorMessage(error))
  } finally {
    deletingId.value = null
  }
}
function displayTime(value?: string | null) {
  return value
    ? value
        .replace('T', ' ')
        .replace(/\.\d{3}Z$/, '')
        .replace(/Z$/, '')
    : '—'
}
onMounted(() => void loadRows())
onBeforeUnmount(() => controller?.abort())
</script>

<template>
  <section class="role-panel">
    <header class="panel-header"><h1>角色列表</h1></header>
    <div class="panel-body">
      <div class="toolbar">
        <div class="toolbar-actions">
          <el-button type="primary" :icon="Plus" @click="openCreate">添加角色</el-button>
          <el-button :icon="Refresh" :loading="loading" @click="loadRows">刷新</el-button>
        </div>
        <form class="search-form" @submit.prevent="search">
          <el-input
            v-model="keywordInput"
            placeholder="搜索姓名、用户名或 ID"
            aria-label="搜索用户"
            clearable
          />
          <el-select v-model="roleInput" placeholder="全部角色" aria-label="筛选角色" clearable>
            <el-option v-for="option in ROLE_OPTIONS" :key="option.value" v-bind="option" />
          </el-select>
          <el-button type="primary" :icon="Search" native-type="submit" :disabled="loading"
            >搜索</el-button
          >
          <el-button @click="resetSearch">重置</el-button>
        </form>
      </div>
      <el-alert
        v-if="loadError"
        class="list-alert"
        :title="loadError"
        type="error"
        show-icon
        :closable="false"
      >
        <el-button link type="primary" @click="loadRows">重新加载</el-button>
      </el-alert>
      <p v-if="filtering" class="search-note">正在筛选全部接口数据，共找到 {{ total }} 条记录。</p>
      <el-table
        v-loading="loading"
        :data="tableRows"
        row-key="id"
        border
        stripe
        class="role-table"
        :empty-text="
          loadError ? '数据加载失败，请重试' : filtering ? '没有找到匹配的角色' : '暂无角色数据'
        "
      >
        <el-table-column prop="id" label="ID" min-width="76" />
        <el-table-column prop="name" label="管理员名称" min-width="140" show-overflow-tooltip />
        <el-table-column prop="userName" label="用户名" min-width="145" show-overflow-tooltip />
        <el-table-column label="角色" min-width="125">
          <template #default="{ row }">
            <el-tag
              :type="row.role === 1 ? 'danger' : row.role === 2 ? 'warning' : 'info'"
              effect="light"
              >{{ roleLabel(row.role) }}</el-tag
            >
          </template>
        </el-table-column>
        <el-table-column label="最后登录时间" min-width="190">
          <template #default="{ row }">{{ displayTime(row.lastLoginAt) }}</template>
        </el-table-column>
        <el-table-column label="创建时间" min-width="190">
          <template #default="{ row }">{{ displayTime(row.createdAt || row.createAt) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="140" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" :disabled="deletingId !== null" @click="openEdit(row)"
              >编辑</el-button
            >
            <el-button
              link
              type="danger"
              :loading="deletingId === row.id"
              :disabled="deletingId !== null && deletingId !== row.id"
              @click="remove(row)"
              >删除</el-button
            >
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination-wrap">
        <el-pagination
          background
          :current-page="page"
          :page-size="pageSize"
          :page-sizes="[5, 10, 20, 50]"
          :total="total"
          :disabled="loading"
          layout="total, sizes, prev, pager, next, jumper"
          @current-change="changePage"
          @size-change="changePageSize"
        />
      </div>
    </div>
    <el-dialog
      v-model="dialogVisible"
      :title="editingId !== null ? '编辑角色' : '添加角色'"
      width="560px"
      class="account-dialog"
      destroy-on-close
      :close-on-click-modal="!saving"
      :close-on-press-escape="!saving"
      :show-close="!saving"
      @closed="form.passWord = ''"
    >
      <el-alert
        v-if="saveError"
        class="list-alert"
        :title="saveError"
        type="error"
        show-icon
        :closable="false"
      />
      <AdminAccountForm
        ref="accountForm"
        v-model="form"
        :editing="editingId !== null"
        :disabled="saving"
      />
      <template #footer>
        <el-button :disabled="saving" @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="save">保存</el-button>
      </template>
    </el-dialog>
  </section>
</template>

<style scoped>
.role-panel {
  background: #fff;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  min-width: 0;
}
.panel-header {
  padding: 20px 24px;
  border-bottom: 1px solid #ebeef5;
}
h1 {
  margin: 0;
  font-size: 20px;
  color: #303133;
  font-weight: 600;
}
.panel-body {
  padding: 24px;
}
.toolbar,
.toolbar-actions,
.search-form {
  display: flex;
  align-items: center;
  gap: 12px;
}
.toolbar {
  justify-content: space-between;
  flex-wrap: wrap;
  margin-bottom: 20px;
}
.toolbar-actions .el-button + .el-button,
.search-form .el-button + .el-button {
  margin-left: 0;
}
.search-form {
  flex-wrap: wrap;
}
.search-form .el-input {
  width: 220px;
}
.search-form .el-select {
  width: 140px;
}
.list-alert {
  margin-bottom: 16px;
}
.search-note {
  margin: 0 0 14px;
  color: #909399;
  font-size: 13px;
}
.role-table {
  width: 100%;
}
.role-table :deep(.el-table__cell) {
  padding: 14px 0;
}
.role-table :deep(th.el-table__cell) {
  background: #fafafa;
  color: #606266;
  font-weight: 600;
}
.pagination-wrap {
  display: flex;
  justify-content: flex-end;
  padding-top: 22px;
  overflow-x: auto;
}
@media (max-width: 768px) {
  .panel-body {
    padding: 16px;
  }
  .panel-header {
    padding: 18px 16px;
  }
  .search-form {
    width: 100%;
    gap: 8px;
  }
  .search-form .el-input {
    width: 100%;
  }
  .search-form .el-select {
    flex: 1;
    min-width: 120px;
  }
  .pagination-wrap {
    justify-content: flex-start;
  }
}
</style>
