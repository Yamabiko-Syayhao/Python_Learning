<template>
  <div class="page">
    <!-- 顶部工具栏 -->
    <div class="toolbar">
      <el-input
        v-model="keyword"
        placeholder="搜索姓名 / 标题 / 关键词"
        clearable
        class="search-input"
      />
      <el-button type="primary" :icon="Search" @click="handleSearch">搜索</el-button>
      <el-button type="success" :icon="Plus" @click="handleAdd">新增</el-button>
    </div>

    <!-- 数据表格 -->
    <el-table :data="pagedData" border stripe class="data-table">
      <el-table-column prop="id" label="序号" width="80" align="center" />
      <el-table-column prop="name" label="姓名" min-width="100" />
      <el-table-column prop="gender" label="性别" width="80" align="center" />
      <el-table-column prop="age" label="年龄" width="80" align="center" />
      <el-table-column prop="address" label="住址" min-width="180" />
      <el-table-column prop="title" label="标题" min-width="140" />
      <el-table-column prop="keyword" label="关键词" min-width="120" />
      <el-table-column label="操作" width="180" align="center" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
          <el-button type="danger" size="small" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页（依赖 main.ts 的 zhCn locale 自动显示中文） -->
    <div class="pagination-wrap">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[5, 10, 20, 50]"
        :total="filteredData.length"
        layout="total, sizes, prev, pager, next, jumper"
        background
      />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Plus } from '@element-plus/icons-vue'

interface Row {
  id: number
  name: string
  gender: '男' | '女'
  age: number
  address: string
  title: string
  keyword: string
}

// 模拟 15 条数据（最后 5 条对应图片中第 3 页）
const allData = ref<Row[]>([
  { id: 1,  name: '赵一', gender: '男', age: 25, address: '北京市朝阳区',   title: '入门指引', keyword: 'intro' },
  { id: 2,  name: '钱二', gender: '女', age: 24, address: '上海市浦东新区', title: '表单组件', keyword: 'form' },
  { id: 3,  name: '孙三', gender: '男', age: 30, address: '广州市天河区',   title: '表格展示', keyword: 'table' },
  { id: 4,  name: '李四', gender: '女', age: 27, address: '深圳市南山区',   title: '布局容器', keyword: 'layout' },
  { id: 5,  name: '周五', gender: '男', age: 29, address: '杭州市西湖区',   title: '导航菜单', keyword: 'nav' },
  { id: 6,  name: '吴六', gender: '女', age: 22, address: '南京市鼓楼区',   title: '徽章标记', keyword: 'badge' },
  { id: 7,  name: '郑七', gender: '男', age: 35, address: '成都市锦江区',   title: '进度条',   keyword: 'progress' },
  { id: 8,  name: '王八', gender: '女', age: 26, address: '武汉市洪山区',   title: '抽屉组件', keyword: 'drawer' },
  { id: 9,  name: '冯九', gender: '男', age: 31, address: '西安市雁塔区',   title: '标签页',   keyword: 'tabs' },
  { id: 10, name: '陈十', gender: '女', age: 28, address: '长沙市岳麓区',   title: '头像组件', keyword: 'avatar' },
  { id: 11, name: '冯三', gender: '男', age: 28, address: '重庆市渝中区',   title: '消息提示', keyword: 'message' },
  { id: 12, name: '陈四', gender: '女', age: 26, address: '天津市和平区',   title: '确认框',   keyword: 'messagebox' },
  { id: 13, name: '褚五', gender: '男', age: 33, address: '青岛市市南区',   title: '本地数据', keyword: '纯前端' },
  { id: 14, name: '卫六', gender: '女', age: 29, address: '大连市中山区',   title: '搜索过滤', keyword: 'keyword' },
  { id: 15, name: '蒋七', gender: '男', age: 27, address: '厦门市思明区',   title: '综合练习', keyword: '增删改查' },
])

const keyword = ref('')
const currentPage = ref(3) // 图片中初始在第 3 页
const pageSize = ref(5)

// 搜索过滤
const filteredData = computed(() => {
  const kw = keyword.value.trim().toLowerCase()
  if (!kw) return allData.value
  return allData.value.filter(r =>
    r.name.toLowerCase().includes(kw) ||
    r.title.toLowerCase().includes(kw) ||
    r.keyword.toLowerCase().includes(kw)
  )
})

// 分页切片
const pagedData = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return filteredData.value.slice(start, start + pageSize.value)
})

const handleSearch = () => {
  currentPage.value = 1
  ElMessage.success(keyword.value ? `搜索：${keyword.value}` : '已重置搜索')
}

const handleAdd = () => {
  ElMessage.info('点击了新增按钮（示例，未调接口）')
}

const handleEdit = (row: Row) => {
  ElMessage.info(`编辑：${row.name}`)
}

const handleDelete = (row: Row) => {
  ElMessageBox.confirm(`确定删除「${row.name}」吗？`, '提示', {
    type: 'warning',
  }).then(() => {
    allData.value = allData.value.filter(r => r.id !== row.id)
    ElMessage.success('删除成功')
  }).catch(() => { /* 用户取消 */ })
}
</script>

<style scoped>
.page {
  padding: 20px;
}
.toolbar {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
  align-items: center;
}
.search-input {
  width: 280px;
}
.data-table {
  width: 100%;
}
.pagination-wrap {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}
</style>
