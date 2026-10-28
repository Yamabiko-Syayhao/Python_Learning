import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus, { ElMessage } from 'element-plus'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import 'element-plus/dist/index.css'

import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/auth'
import { AUTH_EXPIRED_EVENT } from './utils/authSession'

const app = createApp(App)

app.use(createPinia())
app.use(ElementPlus, { locale: zhCn })
app.use(router)

window.addEventListener(AUTH_EXPIRED_EVENT, () => {
  const auth = useAuthStore()
  const wasLoggedIn = auth.isAuthenticated
  auth.logout()
  if (wasLoggedIn) ElMessage.warning('登录已失效，请重新登录')
  if (router.currentRoute.value.meta.requiresAuth) {
    void router.replace({ name: 'login', query: { redirect: router.currentRoute.value.fullPath } })
  }
})

app.mount('#app')
