// 引入路由实例
import { createRouter, createWebHistory } from 'vue-router'

// 引入HomeView组件
import HomeView from '../views/HomeView.vue'

// 路由表
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      //  / 是路径 / 默认打开的组件
      path: '/',
      // home 是路由的名称，用于在代码中引用路由
      name: 'home',
      // component 是路由的组件，用于在路由匹配时
      // HomeView 是组件的名称
      // 这里也是使用了HomeView组件
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      // 懒加载的形式 用的时候再去加载组件
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/vfor',
      name: 'vfor',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      // 懒加载的形式 用的时候再去加载组件
      component: () => import('../views/02vfor.vue'),
    },
    {
      path: '/v-on',
      name: '03von',
      component: () => import('../views/03v-on.vue'),
    },
     {
      path: '/smzq',
      name: '04smzq',
      component: () => import('../views/04smzq.vue'),
    },
     {
      path: '/axios',
      name: '05axios',
      component: () => import('../views/05axios.vue'),
    },
    {
      path: '/06img',
      name: '06img',
      component: () => import('../views/06img.vue'),
    },
    {
      path: '/07father',
      name: '07father',
      component: () => import('../views/07father.vue'),
    },
  ],
})

// 导出
export default router
