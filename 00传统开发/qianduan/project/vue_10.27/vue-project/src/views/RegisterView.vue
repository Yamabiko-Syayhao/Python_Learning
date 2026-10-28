<script setup lang="ts">
import { nextTick, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import AdminAccountForm from '@/components/AdminAccountForm.vue'
import { registerAccount } from '@/api/admin'
import { errorMessage } from '@/api/http'
import type { AdminFormData } from '@/types/admin'

const router = useRouter()
const accountFormRef = ref<InstanceType<typeof AdminAccountForm>>()
const submitting = ref(false)
const form = ref<AdminFormData>(emptyForm())
function emptyForm(): AdminFormData {
  return { name: '', userName: '', passWord: '', role: undefined }
}
async function handleRegister() {
  if (submitting.value) return
  submitting.value = true
  try {
    if (!(await accountFormRef.value?.validate()) || !form.value.role) return
    await registerAccount({
      name: form.value.name.trim(),
      userName: form.value.userName.trim(),
      passWord: form.value.passWord,
      role: form.value.role,
    })
    ElMessage.success('注册成功，请登录')
    await router.replace({ path: '/login', query: { userName: form.value.userName.trim() } })
  } catch (error) {
    ElMessage.error(errorMessage(error))
  } finally {
    submitting.value = false
  }
}
async function resetForm() {
  form.value = emptyForm()
  await nextTick()
  accountFormRef.value?.resetValidation()
}
</script>

<template>
  <main class="auth-page">
    <section class="auth-card register-card" aria-labelledby="register-title">
      <h1 id="register-title">注册界面</h1>
      <AdminAccountForm
        id="register-account-form"
        ref="accountFormRef"
        v-model="form"
        :disabled="submitting"
        @submit.prevent="handleRegister"
      />
      <div class="form-actions">
        <el-button
          size="large"
          type="primary"
          native-type="submit"
          form="register-account-form"
          :loading="submitting"
          >立即注册</el-button
        >
        <el-button size="large" :disabled="submitting" @click="resetForm">重置</el-button>
      </div>
      <p class="login-link">已有账号？<RouterLink to="/login">返回登录</RouterLink></p>
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
  width: 780px;
  max-width: 100%;
  min-height: 640px;
  padding: 28px 32px 36px;
  background: #fff;
  box-shadow: 0 0 36px rgb(0 0 0 / 28%);
}
h1 {
  margin: 0 0 30px;
  color: #2c3e50;
  font-size: 32px;
  font-weight: 700;
  line-height: 1.5;
  text-align: center;
}
.register-card :deep(.el-form-item) {
  margin-bottom: 34px;
}
.register-card :deep(.el-form-item__label) {
  width: 158px !important;
  height: 62px;
  align-items: center;
  padding-right: 20px;
  font-size: 22px;
}
.register-card :deep(.el-input__wrapper),
.register-card :deep(.el-select__wrapper) {
  min-height: 62px;
  font-size: 22px;
}
.form-actions {
  display: flex;
  margin-left: 158px;
  gap: 8px;
}
.form-actions :deep(.el-button) {
  height: 62px;
  padding: 0 30px;
  font-size: 22px;
  font-weight: 600;
}
.login-link {
  margin: 26px 0 0;
  color: #606266;
  font-size: 15px;
  text-align: right;
}
.login-link a {
  color: var(--el-color-primary);
  text-decoration: underline;
}
@media (max-width: 600px) {
  .auth-page {
    padding: 24px 16px;
  }
  .auth-card {
    min-height: auto;
    padding: 24px 16px;
  }
  h1 {
    font-size: 26px;
  }
  .register-card :deep(.el-form-item__label) {
    width: 110px !important;
    height: 44px;
    padding-right: 12px;
    font-size: 16px;
  }
  .register-card :deep(.el-input__wrapper),
  .register-card :deep(.el-select__wrapper) {
    min-height: 44px;
    font-size: 16px;
  }
  .form-actions {
    margin-left: 0;
    justify-content: center;
    gap: 0;
  }
  .form-actions :deep(.el-button) {
    height: 44px;
    padding: 0 16px;
    font-size: 16px;
  }
}
</style>
