// import './assets/main.css'

// 引入vue
import { createApp } from 'vue'
// 引入pinia插件
import { createPinia } from 'pinia'

// 引入App.vue组件
import App from './App.vue'
// 引入路由实例
import router from './router'
// 引入element-plus插件
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

// 创建vue实例
const app = createApp(App)
// 挂载pinia插件
app.use(createPinia())
// 挂载路由实例
app.use(router)
// 挂载element-plus插件
app.use(ElementPlus)
// 将vue组件放到html中显示
app.mount('#app')






