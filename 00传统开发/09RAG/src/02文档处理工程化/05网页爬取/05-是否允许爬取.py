"""
爬虫合规与道德
爬虫红线:
    - 遵守 robots.txt 网络爬虫协议
    - 控制频率,不要 DDOS 别人     DOS  拒绝服务,单台攻击一台服务器  DDOS 分布式拒绝服务  成千上万台机器一起发起攻击
                                携带海量数据包攻击服务器 ,服务器带宽被占满,网络被堵死
                                模拟大量网页请求,疯狂刷新页面,耗尽服务器资源
    - 不抓取个人隐私 付费内容
    - 不绕过登录墙抓取受保护数据
    - 遵守 <数据安全法> <个人信息保护法>

robots.txt 检查示例
"""
# 导入robotparser协议解析器
import urllib.robotparser
# 导入SSL模块证书校验
import ssl
# 关闭ssl证书校验  避免证书校验失败导致的异常
ssl._create_default_https_context = ssl._create_unverified_context
# 实例化robotparser协议解析器对象
rp = urllib.robotparser.RobotFileParser()
# 设置robots.txt文件地址
rp.set_url('https://byesame.com/robots.txt')
# 读取robots.txt文件
rp.read()
# 检查是否允许抓取
can_fetch = rp.can_fetch('*', 'https://byesame.com/home')
print('是否允许抓取', can_fetch)

#
# """
#   场景               推荐方案
#   --------------   ---------------------
#   静态网页/文档站       requests + trafilatura
#   动态 SPA 网站        Playwright
#   大规模分布式爬取      Scrapy
#   反爬严格站点          Playwright + 代理 IP 池
#   只要正文             trafilatura（最省心）
# """