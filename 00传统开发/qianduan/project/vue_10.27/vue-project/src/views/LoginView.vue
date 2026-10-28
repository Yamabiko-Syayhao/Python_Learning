<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import { errorMessage } from '@/api/http'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()
const formRef = ref<FormInstance>()
const submitting = ref(false)
const form = reactive({
  userName: typeof route.query.userName === 'string' ? route.query.userName : '',
  passWord: '',
})
const rules: FormRules<typeof form> = {
  userName: [{ required: true, whitespace: true, message: '请输入用户名', trigger: 'blur' }],
  passWord: [{ required: true, whitespace: true, message: '请输入密码', trigger: 'blur' }],
}
async function handleLogin() {
  if (submitting.value) return
  submitting.value = true
  try {
    if (!(await formRef.value?.validate().catch(() => false))) return
    const user = await auth.login({ userName: form.userName.trim(), passWord: form.passWord })
    ElMessage.success(`欢迎回来，${user.name || user.userName}`)
    const redirect = route.query.redirect
    await router.replace(
      typeof redirect === 'string' && redirect.startsWith('/admin') ? redirect : '/admin/roles',
    )
  } catch (error) {
    ElMessage.error(errorMessage(error))
  } finally {
    submitting.value = false
  }
}
function resetForm() {
  form.userName = ''
  form.passWord = ''
  formRef.value?.clearValidate()
}
</script>

<template>
  <main class="auth-page">
    <section class="auth-card login-card" aria-labelledby="login-title">
      <h1 id="login-title">请登录账号</h1>
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        :disabled="submitting"
        label-width="90px"
        size="large"
        @submit.prevent="handleLogin"
      >
        <el-form-item label="用户名" prop="userName">
          <el-input v-model="form.userName" autocomplete="username" clearable />
        </el-form-item>
        <el-form-item label="密码" prop="passWord">
          <el-input
            v-model="form.passWord"
            type="password"
            autocomplete="current-password"
            show-password
          />
        </el-form-item>
        <el-form-item class="form-actions">
          <el-button type="primary" native-type="submit" :loading="submitting">本地登录</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
      <p class="register-link">没有账号？请<RouterLink to="/register">注册</RouterLink></p>
    </section>
  </main>
</template>

<style scoped>
.auth-page {
  display: flex;
  min-height: 100vh;
  align-items: center;
  justify-content: center;
  padding: 40px 24px;
  background: #fff;
}
.auth-card {
  width: 620px;
  max-width: 100%;
  min-height: 480px;
  padding: 36px 32px 54px;
  background: #fff;
  box-shadow: 0 0 32px rgb(0 0 0 / 28%);
}
h1 {
  margin: 0 0 34px;
  color: #111;
  font-size: 30px;
  font-weight: 700;
  line-height: 1.5;
}
.login-card :deep(.el-form-item) {
  margin-bottom: 30px;
}
.login-card :deep(.el-form-item__label) {
  height: 50px;
  align-items: center;
  font-size: 20px;
}
.login-card :deep(.el-input__wrapper) {
  min-height: 50px;
  font-size: 20px;
}
.form-actions :deep(.el-form-item__content) {
  justify-content: center;
  gap: 8px;
  margin-right: 90px;
}
.form-actions :deep(.el-button) {
  height: 50px;
  padding: 0 24px;
  font-size: 20px;
  font-weight: 600;
}
.register-link {
  margin: 36px 0 0;
  color: #111;
  font-size: 20px;
  text-align: right;
}
.register-link a {
  color: #663399;
  text-decoration: underline;
}
@media (max-width: 600px) {
  .auth-page {
    padding: 24px 16px;
  }
  .auth-card {
    min-height: auto;
    padding: 28px 18px 36px;
  }
  h1 {
    font-size: 26px;
  }
  .login-card :deep(.el-form-item__label) {
    width: 80px !important;
    font-size: 16px;
  }
  .form-actions :deep(.el-form-item__content) {
    gap: 0;
    margin-left: 0 !important;
    margin-right: 0;
  }
  .form-actions :deep(.el-button) {
    padding: 0 18px;
    font-size: 16px;
  }
  .register-link {
    font-size: 16px;
  }
}
</style>
