<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { RouterView, useRoute, useRouter } from 'vue-router'
import {
  DataAnalysis,
  Document,
  Grid,
  Location,
  Menu,
  Share,
  Tools,
  User,
  Warning,
} from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'
import { roleLabel } from '@/types/admin'

const auth = useAuthStore()
const route = useRoute()
const router = useRouter()
const collapsed = ref(false)
const mobile = ref(false)
const mobileOpen = ref(false)
const drawerClosed = computed(() => mobile.value && !mobileOpen.value)
const displayName = computed(() => auth.user?.name || auth.user?.username || '当前用户')

function updateViewport() {
  mobile.value = window.innerWidth < 768
  if (!mobile.value) mobileOpen.value = false
}
function toggleSidebar() {
  if (mobile.value) mobileOpen.value = !mobileOpen.value
  else collapsed.value = !collapsed.value
}
function selectPage() {
  if (mobile.value) mobileOpen.value = false
}
async function logout() {
  auth.logout()
  await router.replace('/login')
}
onMounted(() => {
  updateViewport()
  window.addEventListener('resize', updateViewport)
})
onBeforeUnmount(() => window.removeEventListener('resize', updateViewport))
</script>

<template>
  <div class="admin-shell" :class="{ 'is-collapsed': collapsed, 'is-mobile': mobile }">
    <button
      v-if="mobileOpen"
      class="sidebar-backdrop"
      aria-label="关闭侧边栏"
      @click="mobileOpen = false"
    />
    <aside id="admin-sidebar" class="sidebar" :class="{ 'drawer-closed': drawerClosed }">
      <RouterLink class="brand" to="/admin/roles" @click="selectPage">
        <span v-if="!collapsed || mobile">海南残联后台管理系统</span>
        <el-icon v-else :size="23"><Grid /></el-icon>
      </RouterLink>
      <el-menu
        class="sidebar-menu"
        :default-active="route.path"
        :default-openeds="['system']"
        :collapse="collapsed && !mobile"
        :collapse-transition="false"
        background-color="#535b64"
        text-color="#f0f1f3"
        active-text-color="#f6d76a"
        router
        @select="selectPage"
      >
        <el-sub-menu index="components">
          <template #title
            ><el-icon><Location /></el-icon><span>组件传参</span></template
          >
          <el-menu-item index="/admin/component-demo">父子组件传参</el-menu-item>
        </el-sub-menu>
        <el-menu-item index="/admin/route-demo"
          ><el-icon><Document /></el-icon><span>路由传参</span></el-menu-item
        >
        <el-sub-menu index="charts">
          <template #title
            ><el-icon><DataAnalysis /></el-icon><span>图表展示</span></template
          >
          <el-menu-item index="/admin/charts">数据图表</el-menu-item>
        </el-sub-menu>
        <el-menu-item index="/admin/directives"
          ><el-icon><Grid /></el-icon><span>自定义指令</span></el-menu-item
        >
        <el-sub-menu index="store">
          <template #title
            ><el-icon><DataAnalysis /></el-icon><span>Pinia 状态管理</span></template
          >
          <el-menu-item index="/admin/store-demo">计数器示例</el-menu-item>
        </el-sub-menu>
        <el-sub-menu index="axios">
          <template #title
            ><el-icon><Share /></el-icon><span>axios</span></template
          >
          <el-menu-item index="/admin/axios-demo">接口请求</el-menu-item>
        </el-sub-menu>
        <el-sub-menu index="plugins">
          <template #title
            ><el-icon><Tools /></el-icon><span>插件</span></template
          >
          <el-menu-item index="/admin/plugins">Element Plus</el-menu-item>
        </el-sub-menu>
        <el-sub-menu index="system">
          <template #title
            ><el-icon><Warning /></el-icon><span>系统设置</span></template
          >
          <el-menu-item index="/admin/roles">角色管理</el-menu-item>
          <el-menu-item index="/admin/cross-origin">跨域配置</el-menu-item>
          <el-menu-item index="/admin/team">募捐团队</el-menu-item>
        </el-sub-menu>
        <el-menu-item index="/admin/map"
          ><el-icon><Location /></el-icon><span>高德地图</span></el-menu-item
        >
      </el-menu>
    </aside>

    <div class="main-shell">
      <header class="topbar">
        <button
          class="menu-toggle"
          type="button"
          aria-label="展开或收起侧边栏"
          aria-controls="admin-sidebar"
          :aria-expanded="mobile ? mobileOpen : !collapsed"
          @click="toggleSidebar"
        >
          <el-icon :size="21"><Menu /></el-icon>
        </button>
        <span class="topbar-title">管理控制台</span>
        <div class="account">
          <span class="avatar" aria-hidden="true"
            ><el-icon :size="20"><User /></el-icon
          ></span>
          <span class="account-name">{{ displayName }}</span>
          <span v-if="auth.user" class="account-role">（{{ roleLabel(auth.user.role) }}）</span>
          <el-button link class="logout-button" @click="logout">退出登录</el-button>
        </div>
      </header>
      <main class="main-content"><RouterView /></main>
    </div>
  </div>
</template>

<style scoped>
.admin-shell {
  --sidebar-width: 220px;
  min-height: 100vh;
  background: #f6f7fb;
}
.admin-shell.is-collapsed {
  --sidebar-width: 64px;
}
.sidebar {
  position: fixed;
  inset: 0 auto 0 0;
  z-index: 30;
  width: var(--sidebar-width);
  background: #535b64;
  overflow-y: auto;
  transition:
    width 0.2s ease,
    transform 0.2s ease;
}
.brand {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 72px;
  padding: 0 12px;
  color: #fff;
  font-size: 18px;
  font-weight: 600;
  text-decoration: none;
  white-space: nowrap;
}
.sidebar-menu {
  border: 0;
  width: 100%;
}
.sidebar-menu :deep(.el-menu-item),
.sidebar-menu :deep(.el-sub-menu__title) {
  height: 58px;
}
.sidebar-menu :deep(.el-menu-item.is-active) {
  background: #474f58;
}
.sidebar-menu :deep(.el-menu-item:hover),
.sidebar-menu :deep(.el-sub-menu__title:hover) {
  background: #48515b;
}
.sidebar-menu :deep(.el-sub-menu .el-menu-item) {
  height: 48px;
  min-width: 0;
}
.main-shell {
  margin-left: var(--sidebar-width);
  min-width: 0;
  transition: margin-left 0.2s ease;
}
.topbar {
  height: 72px;
  display: flex;
  align-items: center;
  gap: 18px;
  padding: 0 26px;
  color: #f7f7fa;
  background: #242733;
}
.menu-toggle {
  display: grid;
  place-items: center;
  width: 36px;
  height: 36px;
  border: 0;
  border-radius: 4px;
  color: #fff;
  background: transparent;
  cursor: pointer;
}
.menu-toggle:hover {
  background: #383d4b;
}
.menu-toggle:focus-visible {
  outline: 2px solid #409eff;
  outline-offset: 2px;
}
.topbar-title {
  font-size: 14px;
  color: #c5c8d0;
}
.account {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
}
.avatar {
  display: grid;
  place-items: center;
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: #3a6079;
}
.account-role {
  color: #b8bdc8;
  font-size: 12px;
}
.logout-button {
  color: #8dc7ff;
  margin-left: 12px;
}
.main-content {
  padding: 24px;
  min-width: 0;
}
.sidebar-backdrop {
  position: fixed;
  inset: 0;
  z-index: 25;
  background: #0006;
  border: 0;
}
@media (max-width: 767px) {
  .admin-shell {
    --sidebar-width: 220px;
  }
  .admin-shell.is-collapsed {
    --sidebar-width: 220px;
  }
  .main-shell {
    margin-left: 0;
  }
  .sidebar.drawer-closed {
    transform: translateX(-100%);
  }
  .topbar {
    height: 64px;
    padding: 0 14px;
    gap: 8px;
  }
  .topbar-title,
  .account-role {
    display: none;
  }
  .account {
    gap: 6px;
  }
  .account-name {
    max-width: 100px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .logout-button {
    margin-left: 4px;
  }
  .main-content {
    padding: 14px;
  }
}
</style>
