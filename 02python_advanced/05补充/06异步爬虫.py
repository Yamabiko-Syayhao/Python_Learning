# 异步爬虫的特征：使用asyncio，aiohttp，httpx等 通过async/await语法去并发发送
# 送请求 ，多个请求在宏观上是同时等待返回结果
# 追求的是高并发
# aiohttp 用来发送异步请求
import asyncio, os, random, hashlib, aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser

baseUrl = "https://anime.bang-dream.com/yumemita/"
IMG_DIR = "serve_img"
os.makedirs(IMG_DIR, exist_ok=True)
# exist_ok=True 没有serve_img这个文件夹就创，有也不会报错

CONCURRENCY = 5  # 规则3 限速：同一时刻最多几个请求在飞
RETRIES = 3      # 规则4 重试：最多试几次

# ---------------- 规则1 合规 ----------------
# 目标网站允不允许你爬 先看robots.txt 不允许就不动手
def can_fetch(url, user_agent="*"):
    rp = RobotFileParser()
    rp.set_url(urljoin(url, "/robots.txt"))
    try:
        rp.read()  # 启动时同步请求一次robots.txt
    except Exception:
        print("[合规] robots.txt读取不到(可能没有) 按允许处理")
        return True
    return rp.can_fetch(user_agent, url)

# ---------------- 规则2 缓存 ----------------
# 不要重复干已经干过的事：文件名由url的md5决定 同一张图第二次进来直接跳过
def cached_path(idx, url):
    md5 = hashlib.md5(url.encode()).hexdigest()[:10]
    return os.path.join(IMG_DIR, f"bq_{idx}_{md5}.jpg")

# ---------------- 规则4 请求重试 ----------------
# 核心原则：该重试的去重试(超时/断连/5xx/429) 不该重试的立刻放弃(404等4xx)
async def fetch_with_retry(session, url):
    for attempt in range(1, RETRIES + 1):
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    return await resp.read()  # 读取图片二进制
                if resp.status >= 500 or resp.status == 429:
                    reason = f"HTTP {resp.status}"  # 服务器暂时抽风/限流 -> 该重试
                else:
                    # 4xx是请求本身的问题 重试也没用 立刻放弃
                    print(f"[放弃] {url} HTTP {resp.status} 不重试")
                    return None
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            reason = repr(e)  # 超时/网络抖动 -> 该重试
        if attempt < RETRIES:
            await asyncio.sleep(2 ** (attempt - 1))  # 指数退避 1s 2s 别立刻再撞
    print(f"[失败] {url} 重试{RETRIES}次后放弃: {reason}")
    return None

# 封装一个函数 给一个图片地址 把它下载下来存到本地
async def download(session, sem, url, idx):
    """
    :param session: 复用的aiohttp会话
    :param sem: 规则3 限速用的信号量
    :param url: 图片地址
    :param idx: 图片序号
    :return:
    """
    # 规则2 缓存：之前已经下过的 直接跳过不重复干
    path = cached_path(idx, url)
    if os.path.exists(path):
        print(f"[缓存] {url} 之前下过 跳过")
        return
    # 规则3 限速：信号量保证同一时刻最多CONCURRENCY个请求在飞
    async with sem:
        # 请求之间加一点随机小间隔 像人的节奏
        # 限速不是越慢越好 而是"不间断的可持续的快" 别被反爬识别成攻击信号
        await asyncio.sleep(random.uniform(0.2, 0.5))
        content = await fetch_with_retry(session, url)  # 规则4 带重试的请求
    if content is None:
        return
    with open(path, "wb") as f:  # 打开文件写入
        f.write(content)
    print(f"[完成] {url} -> {path}")

async def main():
    # 规则1 合规：robots.txt不让抓 就到此为止
    if not can_fetch(baseUrl):
        print(f"[合规] robots.txt 不允许抓取 {baseUrl} 已停止")
        return

    sem = asyncio.Semaphore(CONCURRENCY)  # 信号量在事件循环里创建
    # 单个请求最多等10秒 超时抛异常 走重试逻辑
    timeout = aiohttp.ClientTimeout(total=10)
    # aiohttp.ClientSession() 创建一个http会话---> 后续的请求共用它
    # async with 使用它退出之后会自动关闭
    async with aiohttp.ClientSession(timeout=timeout) as session:
        # 首页HTML同样享受限速+重试
        async with sem:
            html_bytes = await fetch_with_retry(session, baseUrl)
        if html_bytes is None:
            print("首页获取失败 结束")
            return
        html = html_bytes.decode("utf-8", errors="ignore")
        soup = BeautifulSoup(html, "lxml")  # lxml是个解析器
        imgs = soup.find_all("img")
        # 相当于列表推导式生成一批协程 只是额外过滤没src和重复的地址
        seen, tasks = set(), []
        for i, img in enumerate(imgs):
            src = img.get("src")
            if not src:
                continue
            url = urljoin(baseUrl, src)  # 相对路径拼成完整地址
            if url in seen:  # 规则2 缓存：同一次运行里重复的图只下一次
                continue
            seen.add(url)
            tasks.append(download(session, sem, url, i))
        # 并发执行 宏观上看起来是“同时” 这就是异步并发的体现 n张图片几乎同时开始下载而
        # 不是下完一张再下另外一张
        await asyncio.gather(*tasks)

asyncio.run(main())

"""
异步爬虫四大机制
   4 请求重试    核心原则该重试的去重试 不该重试的立刻放弃               -> fetch_with_retry
   3 限速  最终目标不是越慢越好 “不间断的可持续的快” 只要别被反爬识别成攻击信号 -> Semaphore+随机间隔
   2 缓存  不要重复干已经干过的事                                     -> cached_path/seen 命中即跳过
   1 合规  目标网站是不是允许你爬取，是否违反robots.txt，是否抓取个人隐私数据等等 -> can_fetch 先查robots
"""
