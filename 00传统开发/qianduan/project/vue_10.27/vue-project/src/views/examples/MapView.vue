<template>
  <el-card shadow="never"
    ><template #header><strong>高德地图</strong></template
    ><el-empty description="地图服务尚未配置" /><el-alert
      title="需要配置高德地图 Web JS API Key 后接入地图。"
      type="info"
      :closable="false"
      show-icon
    />
    <p>本页面已建立独立路由组件，地图相关展示可集中在此扩展。</p></el-card
  >
</template>
<style scoped>
p {
  color: #909399;
  margin: 20px 0 0;
  line-height: 1.8;
}
</style>
