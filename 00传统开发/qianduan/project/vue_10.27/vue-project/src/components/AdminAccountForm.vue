<script setup lang="ts">
import { ref } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { ROLE_OPTIONS, type AdminFormData } from '@/types/admin'

const props = withDefaults(
  defineProps<{ modelValue: AdminFormData; editing?: boolean; disabled?: boolean }>(),
  { editing: false, disabled: false },
)
const emit = defineEmits<{ 'update:modelValue': [value: AdminFormData] }>()
const formRef = ref<FormInstance>()
const rules: FormRules<AdminFormData> = {
  name: [{ required: true, whitespace: true, message: '请输入管理员姓名', trigger: 'blur' }],
  userName: [{ required: true, whitespace: true, message: '请输入用户名', trigger: 'blur' }],
  passWord: [{ required: true, whitespace: true, message: '请输入密码', trigger: 'blur' }],
  role: [{ required: true, type: 'number', message: '请选择角色', trigger: 'change' }],
}

function updateField<Key extends keyof AdminFormData>(key: Key, value: AdminFormData[Key]) {
  emit('update:modelValue', { ...props.modelValue, [key]: value })
}
async function validate(): Promise<boolean> {
  if (!formRef.value) return false
  return formRef.value.validate().catch(() => false)
}
function resetValidation() {
  formRef.value?.clearValidate()
}
defineExpose({ validate, resetValidation })
</script>

<template>
  <el-form
    ref="formRef"
    class="account-form"
    :model="modelValue"
    :rules="rules"
    :disabled="disabled"
    label-width="110px"
    size="large"
    @submit.prevent
  >
    <el-form-item label="管理员姓名" prop="name">
      <el-input
        :model-value="modelValue.name"
        autocomplete="name"
        clearable
        @update:model-value="updateField('name', $event)"
      />
    </el-form-item>
    <el-form-item label="用户名" prop="userName">
      <el-input
        :model-value="modelValue.userName"
        autocomplete="username"
        clearable
        @update:model-value="updateField('userName', $event)"
      />
    </el-form-item>
    <el-form-item label="密码" prop="passWord">
      <el-input
        :model-value="modelValue.passWord"
        type="password"
        show-password
        autocomplete="new-password"
        :placeholder="editing ? '请填写密码' : ''"
        @update:model-value="updateField('passWord', $event)"
      />
      <p v-if="editing" class="password-hint">接口要求填写密码，请输入此账号的密码。</p>
    </el-form-item>
    <el-form-item label="角色" prop="role">
      <el-select
        :model-value="modelValue.role"
        placeholder="请选择"
        @update:model-value="updateField('role', $event)"
      >
        <el-option
          v-for="option in ROLE_OPTIONS"
          :key="option.value"
          :label="option.label"
          :value="option.value"
        />
      </el-select>
    </el-form-item>
  </el-form>
</template>

<style scoped>
.account-form :deep(.el-select) {
  width: 100%;
}
.account-form :deep(.el-form-item) {
  margin-bottom: 28px;
}
.password-hint {
  margin: 6px 0 0;
  color: var(--el-text-color-secondary);
  font-size: 12px;
  line-height: 1.5;
}
</style>
