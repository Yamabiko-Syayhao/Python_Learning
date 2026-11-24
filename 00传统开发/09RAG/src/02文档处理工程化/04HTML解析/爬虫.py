import ipaddress
import os
import socket
import time
import urllib.parse
import urllib.robotparser

import requests
from bs4 import BeautifulSoup

IMAGE_DIR = "imagymmt"
USER_AGENT = "Mozilla/5.0 (compatible; CompliantImageCrawler/1.0)"
ROBOTS_TOKEN = "CompliantImageCrawler"
TIMEOUT = 15
MAX_IMAGES = 50
MAX_BYTES = 500 * 1024 * 1024
ALLOWED_SCHEMES = ("http", "https")
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg", ".ico", ".avif"}
CONTENT_TYPE_EXTS = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/gif": ".gif",
    "image/webp": ".webp",
    "image/svg+xml": ".svg",
    "image/bmp": ".bmp",
    "image/avif": ".avif",
    "image/x-icon": ".ico",
}

_robot_cache = {}


def _origin(url):
    parts = urllib.parse.urlsplit(url)
    return f"{parts.scheme}://{parts.netloc}"


def _is_public_host(hostname):
    if not hostname:
        return False, "URL 缺少主机名"
    try:
        infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror as e:
        return False, f"域名解析失败: {e}"
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast:
            return False, f"拒绝访问内网或保留地址: {ip}"
    return True, ""


def _get_robot_parser(url):
    origin = _origin(url)
    if origin in _robot_cache:
        return _robot_cache[origin], ""
    parser = urllib.robotparser.RobotFileParser()
    parser.set_url(origin + "/robots.txt")
    try:
        parser.read()
    except Exception as e:
        return None, f"读取 robots.txt 失败: {e}"
    _robot_cache[origin] = parser
    return parser, ""


def _robots_allowed(url):
    parser, err = _get_robot_parser(url)
    if err:
        return False, err
    if not parser.can_fetch(ROBOTS_TOKEN, url):
        return False, f"robots.txt 禁止抓取: {url}"
    return True, ""


def _crawl_delay(url):
    parser = _robot_cache.get(_origin(url))
    if parser is None:
        return 0.0
    return float(parser.crawl_delay(ROBOTS_TOKEN) or 0.0)


def _check_url(url):
    parts = urllib.parse.urlsplit(url)
    if parts.scheme not in ALLOWED_SCHEMES:
        return False, f"不支持的协议: {parts.scheme or '空'}"
    if not parts.netloc:
        return False, "URL 格式不合法"
    return _is_public_host(parts.hostname)


def _fetch(session, url):
    ok, reason = _check_url(url)
    if not ok:
        return None, {"ok": False, "url": url, "status_code": None, "reason": reason}
    try:
        resp = session.get(url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT)
    except requests.exceptions.RequestException as e:
        return None, {"ok": False, "url": url, "status_code": None, "reason": f"请求异常: {e}"}
    if resp.status_code != 200:
        return resp, {
            "ok": False,
            "url": url,
            "status_code": resp.status_code,
            "reason": resp.reason or "请求失败",
        }
    return resp, {"ok": True, "url": url, "status_code": resp.status_code, "reason": "OK"}


def _extract_image_urls(html_text, base_url):
    soup = BeautifulSoup(html_text, "lxml")
    urls = []
    seen = set()
    for img in soup.find_all("img"):
        candidates = []
        for attr in ("src", "data-src", "data-original"):
            value = img.get(attr)
            if value:
                candidates.append(value)
        srcset = img.get("srcset") or img.get("data-srcset")
        if srcset:
            for part in srcset.split(","):
                token = part.strip().split(" ")[0]
                if token:
                    candidates.append(token)
        for candidate in candidates:
            full = urllib.parse.urljoin(base_url, candidate.strip())
            if urllib.parse.urlsplit(full).scheme not in ALLOWED_SCHEMES:
                continue
            if full not in seen:
                seen.add(full)
                urls.append(full)
    return urls


def _extension(url, content_type):
    ext = os.path.splitext(urllib.parse.urlsplit(url).path)[1].lower()
    if ext in IMAGE_EXTS:
        return ext
    mime = (content_type or "").split(";")[0].strip().lower()
    return CONTENT_TYPE_EXTS.get(mime, ".jpg")


def _download_image(session, url, index):
    allowed, reason = _robots_allowed(url)
    if not allowed:
        return {"ok": False, "url": url, "status_code": None, "reason": reason}
    ok, reason = _check_url(url)
    if not ok:
        return {"ok": False, "url": url, "status_code": None, "reason": reason}
    try:
        resp = session.get(url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT, stream=True)
    except requests.exceptions.RequestException as e:
        return {"ok": False, "url": url, "status_code": None, "reason": f"请求异常: {e}"}
    with resp:
        if resp.status_code != 200:
            return {
                "ok": False,
                "url": url,
                "status_code": resp.status_code,
                "reason": resp.reason or "请求失败",
            }
        content_type = resp.headers.get("Content-Type", "")
        if not content_type.lower().startswith("image/"):
            return {
                "ok": False,
                "url": url,
                "status_code": resp.status_code,
                "reason": f"非图片类型: {content_type or 'unknown'}",
            }
        length = resp.headers.get("Content-Length")
        if length and length.isdigit() and int(length) > MAX_BYTES:
            return {
                "ok": False,
                "url": url,
                "status_code": resp.status_code,
                "reason": f"文件超出大小限制({length} bytes)",
            }
        ext = _extension(url, content_type)
        filename = f"{index:03d}{ext}"
        path = os.path.join(IMAGE_DIR, filename)
        total = 0
        try:
            with open(path, "wb") as f:
                for chunk in resp.iter_content(8192):
                    if not chunk:
                        continue
                    total += len(chunk)
                    if total > MAX_BYTES:
                        raise ValueError("文件超出大小限制")
                    f.write(chunk)
        except Exception as e:
            if os.path.exists(path):
                os.remove(path)
            return {
                "ok": False,
                "url": url,
                "status_code": resp.status_code,
                "reason": f"下载失败: {e}",
            }
        return {
            "ok": True,
            "url": url,
            "status_code": resp.status_code,
            "reason": "OK",
            "path": path,
            "bytes": total,
        }


def crawl(url, max_images=MAX_IMAGES):
    parts = urllib.parse.urlsplit(url)
    if parts.scheme not in ALLOWED_SCHEMES:
        return {"ok": False, "status_code": None, "reason": f"不支持的协议: {parts.scheme or '空'}", "images": []}
    allowed, reason = _robots_allowed(url)
    if not allowed:
        return {"ok": False, "status_code": None, "reason": reason, "images": []}

    os.makedirs(IMAGE_DIR, exist_ok=True)
    session = requests.Session()
    try:
        resp, info = _fetch(session, url)
        if not info["ok"]:
            return {**info, "images": []}
        content_type = resp.headers.get("Content-Type", "")
        if "html" not in content_type.lower():
            return {
                "ok": False,
                "url": url,
                "status_code": resp.status_code,
                "reason": f"目标不是 HTML 页面: {content_type or 'unknown'}",
                "images": [],
            }

        image_urls = _extract_image_urls(resp.text, resp.url)[:max_images]
        results = []
        delay = _crawl_delay(resp.url)
        for index, image_url in enumerate(image_urls, start=1):
            if delay:
                time.sleep(delay)
            results.append(_download_image(session, image_url, index))
        return {
            "ok": True,
            "url": url,
            "status_code": resp.status_code,
            "reason": f"共发现 {len(image_urls)} 张图片",
            "images": results,
        }
    finally:
        session.close()


def main():
    url = input("请输入要爬取图片的网页地址: ").strip()
    if not url:
        print("未输入网址，已退出。")
        return
    result = crawl(url)
    print(f"目标: {result.get('url', url)}")
    print(f"结果: {'成功' if result['ok'] else '失败'} | 状态码: {result['status_code']} | 原因: {result['reason']}")
    for item in result["images"]:
        if item["ok"]:
            print(f"[成功] {item['status_code']} {item['path']} ({item['bytes']} bytes) <- {item['url']}")
        else:
            print(f"[失败] {item['status_code']} {item['reason']} <- {item['url']}")


if __name__ == "__main__":
    main()
