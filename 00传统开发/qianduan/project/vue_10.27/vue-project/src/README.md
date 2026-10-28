# Vue 项目文件与运行说明

项目已直接修改在：`S:\project\vue_10.27\vue-project`

## 已完成

- 白底阴影登录、注册页面，表单校验、重置、密码显示切换、请求状态提示。
- 超级管理员（1）、管理员（2）、普通用户（3）三种角色，登录后进入相同管理页面。
- 通过 Axios 请求 PDF 文档定义的真实接口，使用请求头 `token`。
- 角色列表：添加、刷新、姓名/用户名/ID/角色搜索、角色筛选、编辑、删除确认、每页条数与页码跳转。
- 深灰侧边栏、顶部展开/收起按钮、菜单路由切换，移动端显示抽屉。
- HomeView 中提供 RouterLink 登录入口；main.ts 引入 Element Plus、样式和中文语言包。
- 登录状态保存在 sessionStorage，刷新页面保留同一标签页会话；退出或接口返回 401 时清除。密码不持久化。

## 主要代码位置

| 完整路径 | 用途 |
| --- | --- |
| `S:\project\vue_10.27\vue-project\src\views\HomeView.vue` | 首页和进入登录页面的 RouterLink |
| `S:\project\vue_10.27\vue-project\src\views\LoginView.vue` | 登录页面 |
| `S:\project\vue_10.27\vue-project\src\views\RegisterView.vue` | 注册页面与三角色选择 |
| `S:\project\vue_10.27\vue-project\src\views\RoleListView.vue` | 角色列表、搜索、增删改和分页 |
| `S:\project\vue_10.27\vue-project\src\components\AdminAccountForm.vue` | 注册、添加和编辑共用的账号表单 |
| `S:\project\vue_10.27\vue-project\src\layouts\AdminLayout.vue` | 顶栏、用户信息、可折叠侧边栏与嵌套路由出口 |
| `S:\project\vue_10.27\vue-project\src\router\index.ts` | 页面路由、登录检查和页面标题 |
| `S:\project\vue_10.27\vue-project\src\api\http.ts` | Axios 实例、token 头、错误和失效处理 |
| `S:\project\vue_10.27\vue-project\src\api\admin.ts` | 登录、注册、角色列表/添加/编辑/删除接口 |
| `S:\project\vue_10.27\vue-project\src\types\admin.ts` | 账号字段类型与角色选项 |
| `S:\project\vue_10.27\vue-project\src\stores\auth.ts` | Pinia 登录状态 |
| `S:\project\vue_10.27\vue-project\src\utils\authSession.ts` | 会话读写与失效事件 |
| `S:\project\vue_10.27\vue-project\src\main.ts` | Element Plus、中文语言包、Pinia 和 Router 注册 |
| `S:\project\vue_10.27\vue-project\src\App.vue` | 应用 RouterView |
| `S:\project\vue_10.27\vue-project\src\assets\main.css` | 全局基础样式，替换脚手架的双栏样式 |

## 侧边栏独立组件

以下目录为 `S:\project\vue_10.27\vue-project\src\views\examples\`，每个菜单均连接自己的页面组件。

| 路由 | 完整组件路径 |
| --- | --- |
| /admin/component-demo | `S:\project\vue_10.27\vue-project\src\views\examples\ComponentDemoView.vue` |
| /admin/route-demo | `S:\project\vue_10.27\vue-project\src\views\examples\RouteDemoView.vue` |
| /admin/charts | `S:\project\vue_10.27\vue-project\src\views\examples\ChartsView.vue` |
| /admin/directives | `S:\project\vue_10.27\vue-project\src\views\examples\DirectivesView.vue` |
| /admin/store-demo | `S:\project\vue_10.27\vue-project\src\views\examples\StoreDemoView.vue` |
| /admin/axios-demo | `S:\project\vue_10.27\vue-project\src\views\examples\AxiosDemoView.vue` |
| /admin/plugins | `S:\project\vue_10.27\vue-project\src\views\examples\PluginsView.vue` |
| /admin/cross-origin | `S:\project\vue_10.27\vue-project\src\views\examples\CrossOriginView.vue` |
| /admin/team | `S:\project\vue_10.27\vue-project\src\views\examples\TeamView.vue` |
| /admin/map | `S:\project\vue_10.27\vue-project\src\views\examples\MapView.vue` |

组件传参页使用子组件 `S:\project\vue_10.27\vue-project\src\views\examples\MessagePreview.vue`。侧边菜单中的图表、组件、路由、指令、状态管理和插件为轻量示例页；Axios 示例与募捐团队列表使用文档接口。地图页已建好独立组件入口，需要高德 Web JS API Key 才能进一步接入地图。

## src 以外的必要修改

| 完整路径 | 修改 |
| --- | --- |
| `S:\project\vue_10.27\vue-project\package.json` | 补充 axios 和直接使用的 @element-plus/icons-vue 依赖 |
| `S:\project\vue_10.27\vue-project\package-lock.json` | 同步依赖锁定 |
| `S:\project\vue_10.27\vue-project\vite.config.ts` | 开发环境 /api 代理 |
| `S:\project\vue_10.27\vue-project\vitest.config.ts` | Element Plus 校验依赖的测试环境 ESM 转换配置 |
| `S:\project\vue_10.27\vue-project\index.html` | 中文页面语言和标题 |

## 接口约定

默认开发代理目标为 `http://joint.byesame.com`。

| 操作 | 方法与路径 | 参数 |
| --- | --- | --- |
| 登录 | POST /login | JSON：userName、passWord |
| 注册 | POST /register | JSON：name、userName、passWord、role |
| 列表 | GET /admin | Query：page、rows |
| 添加 | POST /admin | JSON：name、userName、passWord、role |
| 编辑 | PUT /admin | JSON：id、name、userName、passWord、role |
| 删除 | DELETE /admin | JSON：id |

成功响应兼容 `code: 200` 和 `meta.status: 200`。角色列表从 `data.list`、`data.count` 读取，时间兼容 `createdAt` 和 `createAt`。

PDF 未提供搜索参数，因此有筛选条件时会分批取回接口全部角色，在前端筛选并分页；无筛选时使用服务端分页。列表和搜索中的旧请求会取消，防止慢响应覆盖新结果。

PDF 的编辑接口要求密码必填，因此编辑时需要重新填写密码。详情接口示例字段与账号字段不一致，编辑表单使用列表行的真实字段回填。注册成功响应没有 token，因此注册成功后返回登录页。

部署时可在服务器将 /api 反向代理到该接口；也可通过构建环境变量 `VITE_API_BASE_URL` 指定可访问的 API 网关。使用 history 路由时，服务器需要将前端路由回退到 index.html；HTTPS 页面应连接 HTTPS 网关。

## 启动

常规方式，在项目目录执行：

```powershell
cd S:\project\vue_10.27\vue-project
npm run dev
```

打开终端显示的本地地址。首页 `/` 可以进入登录页面，登录页为 `/login`，注册页为 `/register`，角色列表为 `/admin/roles`。

当前会话检测到本机 NVM 的 Node/npm 入口配置异常，所以还提供了输出附件中的“启动项目.cmd”。该脚本直接使用本机已存在的 Codex Node 运行时启动项目，不修改全局 Node/NVM 设置；双击后保持窗口开启即可。

正常 Node/npm 环境的检查命令：

```powershell
npm run type-check
npm run test:unit -- --run
npm run build
```

## 验证结果与范围

- TypeScript 类型检查通过。
- Vite 生产构建通过，产物在 `S:\project\vue_10.27\vue-project\dist`。
- 4 个测试文件共 28 项测试通过（含原脚手架的 1 项测试）。
- 已检查真实服务可连接，并验证开发代理能收到真实接口的 token 验证响应。
- 使用独立本地内存 API 验证登录、增删改、跨页搜索、分页、退出、侧边栏开合和菜单切组件。
- 未提供真实账号，线上登录后的增删改尚未实测。实际项目仍连接文档中的服务；本地模拟 API 和测试数据只用于本次验证。
- 附带的“角色管理预览-测试数据.png”显示本地测试数据。

新增测试位于：
`S:\project\vue_10.27\vue-project\src\api\__tests__\admin.spec.ts`
`S:\project\vue_10.27\vue-project\src\api\__tests__\http.spec.ts`
`S:\project\vue_10.27\vue-project\src\views\__tests__\auth.spec.ts`

