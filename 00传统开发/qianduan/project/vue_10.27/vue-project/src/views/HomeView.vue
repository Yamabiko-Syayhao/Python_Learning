<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>
<template>
  <main class="home-page">
    <section class="home-card">
      <h1>海南残联后台管理系统</h1>
      <p>欢迎使用，请登录后进入管理页面。</p>
      <RouterLink to="/login" class="login-link"
        ><el-button type="primary" size="large">进入登录页面</el-button></RouterLink
      >
      <RouterLink to="/register">注册账号</RouterLink>
    </section>
  </main>
</template>
<style scoped>
.home-page {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 24px;
}
.home-card {
  width: min(600px, 100%);
  padding: 60px 40px;
  box-shadow: 0 0 26px #0003;
  text-align: center;
}
h1 {
  font-size: 26px;
  margin: 0 0 20px;
}
p {
  color: #909399;
  margin-bottom: 32px;
}
.login-link {
  display: inline-block;
  margin-right: 20px;
}
</style>
