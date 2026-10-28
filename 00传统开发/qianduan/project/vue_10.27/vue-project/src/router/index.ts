import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView, meta: { title: '首页' } },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
      meta: { title: '登录' },
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/RegisterView.vue'),
      meta: { title: '注册' },
    },
    {
      path: '/admin',
      component: () => import('@/layouts/AdminLayout.vue'),
      meta: { requiresAuth: true },
      redirect: '/admin/roles',
      children: [
        {
          path: 'roles',
          name: 'roles',
          component: () => import('@/views/RoleListView.vue'),
          meta: { title: '角色管理' },
        },
        {
          path: 'component-demo',
          name: 'component-demo',
          component: () => import('@/views/examples/ComponentDemoView.vue'),
          meta: { title: '组件传参' },
        },
        {
          path: 'route-demo',
          name: 'route-demo',
          component: () => import('@/views/examples/RouteDemoView.vue'),
          meta: { title: '路由传参' },
        },
        {
          path: 'charts',
          name: 'charts',
          component: () => import('@/views/examples/ChartsView.vue'),
          meta: { title: '图表示例' },
        },
        {
          path: 'directives',
          name: 'directives',
          component: () => import('@/views/examples/DirectivesView.vue'),
          meta: { title: '自定义指令' },
        },
        {
          path: 'store-demo',
          name: 'store-demo',
          component: () => import('@/views/examples/StoreDemoView.vue'),
          meta: { title: '状态管理' },
        },
        {
          path: 'axios-demo',
          name: 'axios-demo',
          component: () => import('@/views/examples/AxiosDemoView.vue'),
          meta: { title: 'axios' },
        },
        {
          path: 'plugins',
          name: 'plugins',
          component: () => import('@/views/examples/PluginsView.vue'),
          meta: { title: '插件' },
        },
        {
          path: 'cross-origin',
          name: 'cross-origin',
          component: () => import('@/views/examples/CrossOriginView.vue'),
          meta: { title: '跨域' },
        },
        {
          path: 'team',
          name: 'team',
          component: () => import('@/views/examples/TeamView.vue'),
          meta: { title: '募捐团队' },
        },
        {
          path: 'map',
          name: 'map',
          component: () => import('@/views/examples/MapView.vue'),
          meta: { title: '高德地图' },
        },
      ],
    },
    { path: '/about', name: 'about', component: () => import('@/views/AboutView.vue') },
    { path: '/:pathMatch(.*)*', redirect: '/' },
  ],
})
router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }
  if (auth.isAuthenticated && (to.name === 'login' || to.name === 'register'))
    return { name: 'roles' }
})
router.afterEach((to) => {
  document.title = `${String(to.meta.title || '后台管理')} - 海南残联后台管理系统`
})
export default router
