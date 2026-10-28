<template>
  <el-card shadow="never"
    ><template #header><strong>跨域配置</strong></template
    ><el-alert
      title="开发环境通过 Vite 代理转发接口请求。"
      type="info"
      show-icon
      :closable="false"
    />
    <p>
      前端统一使用相对地址请求接口，由开发服务器转发到接口服务。接口地址变更后，调整项目的代理目标并重启开发服务器。
    </p>
    <el-descriptions :column="1" border
      ><el-descriptions-item label="开发配置">vite.config.ts</el-descriptions-item
      ><el-descriptions-item label="生产环境"
        >在部署服务器配置同源反向代理，或由接口服务允许对应前端域名。</el-descriptions-item
      ></el-descriptions
    ></el-card
  >
</template>
<style scoped>
p {
  color: #606266;
  margin: 24px 0;
  line-height: 1.8;
}
</style>
