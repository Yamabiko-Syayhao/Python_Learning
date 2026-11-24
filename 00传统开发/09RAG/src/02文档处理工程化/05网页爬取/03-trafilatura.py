# 导入trafilatura库,用于提取网址内容
import trafilatura


def fetch_article(url):
    # 请求网页内容
    downloaded = trafilatura.fetch_url(url)
    # 如果请求失败,返回None
    if downloaded is None:
        return None
    # 提取文章内容,不包含表格,输出格式为markdown
    content = trafilatura.extract(downloaded, include_tables=False, output_format='markdown')
    # 将结果返回给函数
    return content


res = fetch_article('https://qdstc.qingdao.gov.cn/ztxm/wgrlhgzxk/zcfh/202406/t20240625_8100279.shtml')
print(f"文章内容:{res}")

print("=================" * 5)

# ================= 2 =================
"""
爬虫需要注意三件事:
    1.限速, 避免把对方服务器 打挂/打穿, 避免被封IP
    2.去重: URL 去重, 避免重复抓取
    3.异常处理: 单页失败 不能中断 整个任务
"""
# 定义了一个空的列表
results = []
# 导入time库,用于限速
import time


# urls 是一个列表,包含要爬取的网址
# delay 用于控制爬取速度,默认值为1秒
def craw(urls, delay=1.0):
    # 遍历 urls 列表中的每个网址
    for url in urls:
        try:
            # 发送请求尝试抓取网址内容
            content = fetch_article(url)
            # 如果抓取成功,则将结果添加到 results 列表中
            if content:
                results.append({
                    'url': url,
                    'content': content
                })
                print(f'抓取成功 {url}')
        except Exception as e:
            print(f'抓取失败: {url}, 原因: {e}')
        #  做个有礼貌的爬虫  默认一秒 craw这个函数给了默认值 休眠1秒钟
        time.sleep(delay)
    print(f'批量爬取结果: len(visited) = {len(results)}, 内容: {results}')


# 定义一个集合,用于去重
urls = {
    'https://qdstc.qingdao.gov.cn/ztxm/wgrlhgzxk/zcfh/202412/t20241212_8689385.shtml',
    'https://qdstc.qingdao.gov.cn/ztxm/wgrlhgzxk/zcfh/202412/t20241212_8689385.shtml',
    'https://mp.weixin.qq.com/s/zoQGMsKv1Vxi0VG95PegTw',
    'https://qdstc.qingdao.gov.cn/zcfg/zcjd/202507/t20250728_9928259.shtml'
}
# 调用函数传递爬虫集合，及其限速时间
craw(urls, 0.5)
