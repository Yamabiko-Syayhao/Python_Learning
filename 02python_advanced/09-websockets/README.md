# WebSocket 聊天室运行说明

## 最快启动

在项目文件夹中双击 **start.bat**。它使用本项目的 `.venv` Python，启动 9000 端口的服务，并在服务启动成功后打开 `index.html`。

保持命令窗口打开；按 `Ctrl+C` 停止服务。停止后再启动，已打开的聊天页面需要刷新。

## 已确认的原始问题

1. 网页原来固定连接 `192.168.0.100`，检查时这不是当前电脑的地址。现已改为：直接打开文件时连接 `127.0.0.1`；通过 HTTP 打开时连接网页所在电脑。
2. 电脑默认的 Python 未安装 `websockets`，直接执行 `python serverCopy.py` 会报 `ModuleNotFoundError`。项目自己的 `.venv` 已有依赖，应使用这个环境。
3. 原来没有启动脚本和运行说明。现已补充 `start.bat` 和本文档。

原项目未缺少前端资源或后端入口；入口名就是 `serverCopy.py`。不需要 npm，也不需要 `.env` 或密钥。

## 环境与依赖

- `pyproject.toml` 要求 Python **3.14 或更新版本**，依赖 `websockets>=17.3`。
- `uv.lock` 将本次依赖固定为 `websockets 17.3`。
- 检查时项目 `.venv` 使用 Python **3.14.7**，依赖已安装。
- uv 创建的 `.venv` 中没有 pip 也可以正常运行本项目。

若 `.venv` 丢失、移动后失效，或提示依赖缺失，在 PowerShell 运行：

```powershell
Set-Location -LiteralPath 'S:\09-websockets'
uv sync --locked
.\start.bat
```

`uv sync --locked` 会按已有清单和锁文件准备项目环境；首次准备环境可能需要联网。

## 手动运行

```powershell
Set-Location -LiteralPath 'S:\09-websockets'
.\.venv\Scripts\python.exe -u serverCopy.py --open-browser
```

省略 `--open-browser` 时，只启动后端，请手动打开同目录的 `index.html`。

在 PyCharm 中，请把项目解释器设为 `S:\09-websockets\.venv\Scripts\python.exe`，运行 `serverCopy.py`。通过 IDE 打开网页时，后端也需要保持运行。

## 常见现象

- **浏览器打开 `http://127.0.0.1:9000` 返回 426**：9000 只提供 WebSocket 通信，不提供网页。打开 `index.html` 才是聊天界面。
- **网页显示连接失败**：先确认后端窗口仍在运行，再刷新网页。本机连接地址为 `ws://127.0.0.1:9000/ws`。
- **WinError 10048 / 端口已使用**：通常是另一个服务窗口已占用 9000。关闭自己之前启动的服务窗口后重试，不要重复启动多个后端。
- **发送时尚未连接**：现在会保留输入并显示提示，服务启动后刷新再发送。
- **重启后历史记录消失**：后端记录保存在内存中，最多 200 条；重启后清空是当前设计。

可选：如需通过 HTTP 访问页面，可另开 PowerShell 窗口运行以下命令，并打开 `http://127.0.0.1:8000/index.html`。此时仍需启动 9000 端口的聊天后端。

```powershell
Set-Location -LiteralPath 'S:\09-websockets'
.\.venv\Scripts\python.exe -m http.server 8000 --bind 127.0.0.1
```

## 文件作用

| 文件 | 用途 |
| --- | --- |
| `index.html` | 聊天页面，包含样式与 JavaScript |
| `serverCopy.py` | WebSocket 后端与可选浏览器启动入口 |
| `start.bat` | Windows 启动脚本，固定使用项目环境 |
| `pyproject.toml` | Python 版本要求与依赖清单 |
| `uv.lock` | 依赖锁文件 |

## 验证记录

原后端已通过本机实际连接测试：`/ws` 握手、双客户端连接、在线人数变化、消息广播、历史记录请求及断线处理。普通 HTTP 请求到 9000 端口返回 426，符合其 WebSocket 服务用途。
