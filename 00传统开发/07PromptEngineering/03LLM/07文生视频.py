import os
import dashscope
from dashscope.errors import DashScopeError

# 以下为华北2（北京）地域的配置。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="ws-bggm9k3qgbthz61a",
    region="cn-beijing",
)

print('please wait...')
# generate 为一步式调用（提交任务并等待完成），返回已完成的 Job
try:
    job = client.videos.generate(
        model='wan3.0-video-prime',
        prompt='20秒超宽银幕毛绒宇宙冒险片段，整体采用超精细毛绒材质、电影级太空尺度、可爱外形与强烈动作反差、夸张FPV运镜和真实软体物理。一艘由毛绒布、纽扣、拉链与填充棉制成的宇宙飞船，载着小二哈和他的爸妈，在由巨大毛线行星、绒毛星云和布偶巨兽组成的宇宙中高速逃亡。一只覆盖深蓝长绒毛、眼睛像两枚玻璃纽扣的巨大星际鲸兽从星云中追赶飞船。动态包括拉链飞船弹射起航、贴着毛线行星高速绕行、巨鲸从后方冲出、穿越纽扣小行星带、被一只小花猪吞入体内、沿金色拉链从背部逃出、小花猪如泄掉填充棉般缓慢变扁、最终穿越粉紫色绒毛星云向彩色纽扣太阳飞去。',
        resolution="480P",
        ratio="adaptive",
        duration=10,
        prompt_extend=True)
    print(job)
    print("video_url:", job.video_url)
except DashScopeError as e:
    print(f"HTTP返回码：{e.status_code}")
    print(f"错误码：{e.code}")
    print(f"错误信息：{e.message}")
    print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")




# # -*- coding: utf-8 -*-
# from http import HTTPStatus
# from dashscope import VideoSynthesis
# import dashscope
# import os
#
# # 以下为北京地域URL，各地域的URL不同，获取URL：https://help.aliyun.com/zh/model-studio/image-to-video-general-api-reference
# dashscope.base_http_api_url = 'https://ws-bggm9k3qgbthz61a.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
#
# # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# api_key = os.getenv("DASHSCOPE_API_KEY")
#
# media = [
#     {
#         "type": "first_clip",
#         "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260414/cqcbkw/wan2.7-i2v-video-continuation.mp4"
#     },
#     {
#         "type": "last_frame",
#         "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260414/mrwahg/wan2.7-i2v-video-continuation.webp"
#     }
# ]
#
# def sample_sync_call():
#     print('----sync call, please wait a moment----')
#     rsp = VideoSynthesis.call(
#         api_key=api_key,
#         model="wan2.7-i2v-2026-04-25",
#         media=media,
#         resolution="720P",
#         duration=10,
#         watermark=True,
#         prompt="男人低头向下看到地上的木箱，他弯下腰，小心翼翼打开箱盖，他紧盯着箱内的东西，嘴唇颤抖的微微张开，皱着眉头，眼睛微微张大，露出惊恐的表情。",
#     )
#     if rsp.status_code == HTTPStatus.OK:
#         print(rsp.output.video_url)
#     else:
#         print('Failed, status_code: %s, code: %s, message: %s' %
#               (rsp.status_code, rsp.code, rsp.message))
#
# if __name__ == '__main__':
#     sample_sync_call()