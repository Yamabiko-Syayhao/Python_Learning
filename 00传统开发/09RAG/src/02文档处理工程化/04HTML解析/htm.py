# 定义HTML字符串,包含了很多标签
html = """
<html>
  <body>
    <nav>首页 | 产品 | 关于我们</nav>
    <h1>产品介绍</h1>
    <p>这是我们的旗舰产品，支持私有化部署。</p >
    <ul>
        <li>支持 SSO 单点登录</li>
        <li>
            支持权限管理
            <ul>
                <li>韩信</li>
                <li>梦泪</li>
            </ul>
        </li>
    </ul>
    <ul>
        <li>雷布斯投资</li>
        <li>乔布斯投资</li>
    </ul>
    <footer>版权所有 © 2026</footer>
  </body>
  
   <table>
        <tr>
            <th>套餐</th>
            <th>价格</th>
            <th>并发</th>
        </tr>
        <tr>
            <td>基础版</td>
            <td>999/年</td>
            <td>100</td>
        </tr>
        <tr>
            <td>企业版</td>
            <td>9999/年</td>
            <td>不限</td>
        </tr>
    </table>
</html>

"""