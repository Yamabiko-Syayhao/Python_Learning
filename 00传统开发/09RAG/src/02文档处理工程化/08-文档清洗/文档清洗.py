"""
'垃圾进，垃圾出'(GIGO) --- RAG效果差，90%是数据没洗干净
文档解析完，不能立马embedding。原始文本全是噪音：
    页眉页脚： "第 3 页 / 共 20 页"，"公司机密"
    水印，版权声明
    重复的空白，乱码，控制字符
    HTML残留标签，特殊符号
    解析错位换行 （一句话被切成好几行）
    隐私信息（手机号，身份证，邮箱）

这些噪音： 为什么
    污染Embedding --> 检索不准
    占用token --》浪费成本
    泄露隐私  --》 合规风险

必须清洗：
-基础清洗（空白/控制字符/乱码）
-去页眉页脚/ 水印/ 版权声明
-修复错误换行（段落重组）
-隐私脱敏（手机号/身份证/邮箱） 132****0000  3702***********0000
-去重（精确去重 + 近似去重）
-质量过滤（垃圾段落识别）

清洗在RAG里的位置：解析文档之后，分块之前清洗

"""
# 导入正则表达式库，用于文本匹配替换
import re

# =====================================================
# 二、基础清洗：空白、控制字符、乱码
""" 最基础也最常用的清洗。 """
def basic_clean(text):
    """基础文本清洗
    :param text: 原始待清洗文本
    :return: 清洗后的文本
    """
    # 1. 去除控制字符（除了换行和制表符）
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)
    # 2. 全角空格转半角空格
    text = text.replace("\u3000", " ")
    # 3. 多个连续空格合并成一个
    text = re.sub(r"[ \t]+", " ", text) # 保留了段落的空格
    # 4. 多个连续空行合并成一个
    text = re.sub(r"\n{3,}", "\n\n", text)
    # 5. 去除文本首尾空白字符
    return text.strip()

# 测试样例文本，包含全角空格、换页符、多空行
sample = "产品介绍 \u3000\u3000  这是一段\x0c正文。\n\n\n\n下一段。"
print(f"1 去除多余空格：{basic_clean(sample)}")

# =====================================================
# 三、去页眉页脚 / 水印 / 版权声明
""" 企业文档最常见的噪音。用正则 + 规则库批量清除。 """
# 噪音正则库（企业实践：维护成一个可配置列表） 看不懂就去找正则工具测试
NOISE_PATTERNS = [
    r"第\s*\d+\s*页",                  # 匹配：第 3 页
    r"第\s*\d+\s*页\s*/?\s*共\s*\d+\s*页",  # 匹配：第3页/共20页
    r"Page\s*\d+\s*of\s*\d+",         # 匹配英文页码 Page 3 of 20
    r"Confidential",                  # 匹配机密英文标识
    r"公司机密|内部资料|严禁外传|©版权所有|©2026",         # 匹配中文机密标识匹配版权符号+年份信息
    r"版权所有.*?保留所有权利",            # 匹配版权声明文本
]

def remove_noise(text):
    """去除页眉页脚、水印、版权等噪音
    :param text: 待处理文本
    :return: 移除噪音后的文本
    """
    # 遍历所有噪音正则表达式
    for pattern in NOISE_PATTERNS:
        # 忽略大小写替换，匹配到的噪音替换为空字符串
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)
    return text
test_sample = """
    第 3 页
    ©2026 公司机密
    人工智能RAG系统建设方案
    https://www.test‑company.com/report
    第一节 需求分析
    本章节主要分析业务场景与知识库建设目标。
    第3页/共20页
    """
res = remove_noise(test_sample)
print(f"2 去掉水印和页眉页脚版权符号：{res}")

# =====================================================
# 四、修复错误换行（段落重组）
""" PDF 解析常见问题：一句话被硬换行切成好几行。
    "本产品支持私有化\n部署，并提供\n7x24 技术支持。"
需要把不该断的换行接回去。
"""
def fix_linebreaks(text):
    """修复 PDF 解析导致的错误换行
    :param text: 存在错误换行的文本
    :return: 重组段落之后的文本
    """
    # 按换行符切分成多行列表
    lines = text.split("\n")
    # 存放最终修复完成的段落
    fixed = []
    # 临时缓冲区，拼接未结束的句子
    buffer = ""

    # 逐行遍历
    for line in lines:
        # 去除单行首尾空格
        line = line.strip()
        # 如果是空行，代表真实段落分隔
        if not line:
            # 缓冲区有内容，存入结果列表，清空缓冲区
            if buffer:
                fixed.append(buffer)
                buffer = ""
            continue
        # 缓冲区不为空，并且上一行结尾不是句末标点，说明句子被截断
        if buffer and not buffer.endswith(("。", "！", "？", ".", "!", "?", "：", ":")):
            # 和当前行拼接在一起
            buffer += line
        else:
            # 句子已经完整，先存入结果
            if buffer:
                fixed.append(buffer)
            # 将当前行放入缓冲区作为新句子开头
            buffer = line
    # 循环结束，如果缓冲区还有剩余文本，追加进结果
    if buffer:
        fixed.append(buffer)
    # 使用换行符拼接所有段落返回
    return "\n".join(fixed)

# 测试文本，模拟PDF解析错误断行场景
broken = "本产品支持私有化\n部署，并提供\n7x24 技术支持。\n\n下一段开始。"
print(f"3 去除换行:{fix_linebreaks(broken)}")

# =====================================================
# 五、隐私脱敏（合规必做）
""" 入库前必须对个人隐私脱敏，否则违反《个人信息保护法》。 """
def desensitize(text):
    """隐私信息脱敏
    :param text: 包含隐私信息的原始文本
    :return: 脱敏之后文本
    """
    # 手机号：保留前3后4位，中间4位替换为****
    text = re.sub(r"(1[3-9]\d)\d{4}(\d{4})", r"\1****\2", text)
    # 身份证号：前14位替换为******，保留后面
    text = re.sub(r"\d{6}\d{8}(\d{3}[\dxX])", r"******\1", text)
    # 邮箱：用户名部分脱敏，保留@域名
    text = re.sub(r"([\w.])[\w.]*(@[\w.]+)", r"\1***\2", text)
    # 银行卡号：连续16~19位数字整体替换为****
    text = re.sub(r"\b\d{16,19}\b", "****", text)
    return text

# 隐私信息测试文本
pii = "联系人张三，手机13812345678，邮箱zhangsan@example.com,身份证371122202609160123"
print(f"4 隐私信息:{desensitize(pii)}")

# =====================================================
# 六、精确去重（哈希去重）
""" 知识库里大量重复内容（同一份文件传了多次、模板段落）。
精确去重：内容完全一样的，用哈希过滤。
"""
# 导入哈希库，用于生成文本指纹
import hashlib

def dedup_exact(chunks):
    """精确去重
    :param chunks: chunk文本列表
    :return: 去重后的chunk列表
    """
    # 集合存放已经见过的md5指纹
    seen = set()
    # 保存去重之后结果
    result = []
    # 遍历每一个分块
    for chunk in chunks:
        # 将文本编码，计算md5哈希值作为文本指纹 如果两句话一模一样，哈希值一定一样
        h = hashlib.md5(chunk.encode("utf-8")).hexdigest()
        # 如果指纹不在已存在集合
        if h not in seen:
            seen.add(h)
            result.append(chunk)
    return result

res = dedup_exact(['今天天气不错','张春旺丢了三天','今天天气不错','张春旺丢了三天'])
print(f"5 精确去重:{res}")
# =====================================================
# 七、近似去重（MinHash / 相似度）
""" 更狠的去重：内容"差不多"也算重复。
比如同一段话改了个标点、加了个空格。
企业实践：用 simhash / minhash，或简单用 jaccard 相似度。
"""
def jaccard_similarity(a, b):
    """基于字符集合的 Jaccard 相似度（简易版）
    :param a: 文本a
    :param b: 文本b
    :return: 杰卡德相似度 0~1
    """
    # 转为字符集合
    set_a, set_b = set(a), set(b)
    # 交集字符数量
    inter = len(set_a & set_b)
    # 并集字符数量
    union = len(set_a | set_b)
    # 并集为0返回0，否则返回交集/并集
    return inter / union if union else 0

def dedup_near(chunks, threshold=0.9):
    """近似去重
    :param chunks: chunk列表
    :param threshold: 相似度阈值，超过判定重复
    :return: 近似去重后的chunk列表
    """
    result = []
    # 遍历每个chunk
    for chunk in chunks:
        # 判断是否和已保留的任意文本相似度超过阈值 每一次的新文本都会跟已经存下来的所有文本比一遍，如果相似度超过了90%就是废话
        # 缺点时间复杂度比较高
        is_dup = any(jaccard_similarity(chunk, kept) > threshold for kept in result )
        # 不是重复内容，则加入结果
        if not is_dup:
            result.append(chunk)
    return result
# 越小越精准
res = dedup_near(["今天天气不错","今天天气还可以","今天天气晴朗"],0.2)
print(f"6 近似去重：{res}")

# =====================================================
# 八、质量过滤（丢掉垃圾段落）
""" 不是所有文本都值得入库。过滤掉：
    太短的（"目录"、"图1"）
    乱码率高的
    数字/符号占比过高的（表格残渣）
"""
def is_valid_chunk(text, min_len=10):
    """判断 chunk 是否值得入库
    :param text: chunk文本
    :param min_len: 最小文本长度阈值
    :return: True合格；False丢弃
    """
    text = text.strip()
    # 1. 文本长度小于阈值，直接丢弃
    if len(text) < min_len:
        return False
    # 提取中文、英文、数字有效字符
    valid_chars = re.findall(r"[\u4e00-\u9fa5a-zA-Z0-9]", text)
    # 有效字符占比低于50%，判定为垃圾文本
    if len(valid_chars) / len(text) < 0.5:
        return False
    return True

data_list = [
    '第一章节 三顾茅庐',
    '========\n====\n',
    '备注',
    '诸葛亮等着刘备三顾茅庐'
]

# 将列表遍历循环，取出每一项的值然后当作参数传递进去，返回的结果生成一个新的列表
goods = [chunk for chunk in data_list if is_valid_chunk(chunk)]
print(f"7 质量过滤:{goods}")

# =====================================================
# 九、清洗 Pipeline
""" 原始文本 ↓ 基础清洗（空白/控制字符） ↓ 去噪音（页眉页脚/水印/版权） ↓ 修复换行（段落重组） ↓ 隐私脱敏 ↓ chunk ↓ （分块后）质量过滤 + 去重 ↓ 干净文本 → Embedding  → VectorDB
"""
class TextCleaner:
    """文档清洗器，封装完整文本清洗流水线，一步一步往下走"""
    # 接收的是字符串
    def clean_text(self, text):
        """单段文本完整清洗
        :param text: 原始文本
        :return: 清洗完成文本
        """
        text = desensitize(text)      # 隐私脱敏优先执行
        text = basic_clean(text)      # 基础清洗空白、控制字符
        text = remove_noise(text)     # 移除页眉页脚水印噪音
        text = fix_linebreaks(text)   # 修复错误换行，重组段落
        return text
    # 接收的是列表
    def clean_chunks(self, chunks):
        """分块后的清洗：质量过滤 + 去重
        :param chunks: chunk文本数组
        :return: 过滤+去重后的chunk列表
        """
        # 1. 质量过滤，丢掉不合格chunk 废品
        chunks = [c for c in chunks if is_valid_chunk(c)]
        # 2. 精确哈希去重 去掉一模一样
        chunks = dedup_exact(chunks)
        # 3. 近似相似度去重 去掉差不多一样
        chunks = dedup_near(chunks)
        return chunks

if __name__ == "__main__":
    # 1 实例化清洗器对象
    cleaner = TextCleaner()
    # 2 待清洗脏文本样例
    # 对象.函数(参数)
    dirty = "  公司机密\n本产品支持\n私有化部署。第 3 页\n联系 13812345678  "
    print("清洗后：\n", cleaner.clean_text(dirty))

# =====================================================
# 十、如何清洗（经验之谈）
"""
1. 清洗规则要"可配置"：不同来源文档用不同规则库
2. 清洗要"可回溯"：保留原文，方便对照排查
3. 不要过度清洗：删多了会丢失语义信息
4. 隐私脱敏放在最前面：避免脱敏前的原文进日志
5. 去重放在分块之后：chunk 级去重比文档级更有效
6. 用数据质量看板监控：清洗前后字数、过滤率
"""
