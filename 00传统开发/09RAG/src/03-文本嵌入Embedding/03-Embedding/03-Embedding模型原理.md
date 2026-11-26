# Embedding模型原理
    讲的是"从 BERT 到现代 Embedding 模型"的桥梁——为什么需要、怎么训练、有哪些代表模型、企业怎么选、在 RAG 里怎么用
---

# 理解

* 什么是现代Embedding模型
* Embedding与BERT是什么关系
* Embedding模型如何训练
* 什么是向量空间
* 什么是语义相似度
* Embedding模型如何用于RAG
* OpenAI Embedding原理
* BGE原理
* GTE原理
* Qwen Embedding原理
* 企业如何选择Embedding模型

---

# 一、前情回顾


```text
One-Hot
↓
Word2Vec
↓
FastText
↓
BERT
```
---

Word2Vec解决：
```text
词向量问题
```
---

FastText解决：
```text
OOV问题
```
---

BERT解决：
```text
上下文理解问题
```
---

那么：
```text
为什么还要Embedding模型？
```

---

# 二、BERT为什么不适合直接做检索

假设：

问题：
```text
如何申请退款？
```

文档：
```text
退款流程说明
```
---

我们希望：
```text
问题
↓
向量
↓
相似度
↓
找到文档
```
---

但是BERT原始设计目标：
```text
理解语言
```

而不是：
```text
相似度检索
```

---

BERT输出：
```text
Token级别向量
```

例如：
```text
退款

流程

说明
```

每个词都有向量。
---

问题：
```text
如何得到整个句子的向量？
```
---

BERT并不擅长。

---

# 三、Sentence-BERT诞生

2019年，提出：

```text
Sentence-BERT
```

简称：
```text
SBERT
```

---

目标：

让BERT学会：

```text
句子向量表示
```

---

例如：

```text
如何申请退款
```

↓

```text
[0.12,0.35,0.81...]
```
---

```text
退款流程说明
```
↓
```text
[0.13,0.34,0.79...]
```
---

距离很近。

---

这就是：
```text
现代Embedding模型起点
```
---

# 四、什么是Embedding模型

Embedding模型：

本质上是：

```text
文本
↓
向量
```
转换器。
---

输入：
```text
退款申请流程
```
---

输出：
```text
[0.22,
0.71,
0.55,
...
]
```
---

通常：
```text
768维

1024维

1536维

3072维
```

---

这些数字：

```text
称为Embedding向量
```
---

# 五、向量空间理解

假设：
二维空间。
---

文本：
```text
退款申请

退款流程

订单取消

北京天气
```

---

映射：

```text
退款申请
      ●

退款流程
       ●


订单取消
           ●


北京天气
                    ●
```

---

结果：

```text
退款申请
≈
退款流程
```
因为距离近。

---

```text
退款申请
≠
北京天气
```
因为距离远。

---

Embedding目标：
```text
语义相似
↓
向量接近
```

---

# 六、Embedding模型训练原理

现代Embedding训练：
通常采用：

```text
对比学习
```

Contrastive Learning。

---

训练样本：

正样本：
```text
如何申请退款
↓
退款流程说明
```
---

负样本：
```text
如何申请退款
↓
北京天气预报
```
---

训练目标：
```text
正样本接近
负样本远离
```
---

最终：
```text
语义空间形成
```

---

# 七、Embedding在RAG中的位置

RAG流程：
```text
用户问题
↓
Embedding
↓
向量检索
↓
召回文档
↓
LLM
↓
答案
```

---

Embedding决定：
```text
召回质量
```
---

如果Embedding不好：
```text
召回错误
↓
答案错误
```
---

# 八、Embedding模型分类

目前主流：

---

## 第一类
商业模型 例如：

```text
OpenAI Embedding

Voyage Embedding

Cohere Embedding
```

---

特点：
```text
效果好
收费
```

---

## 第二类

开源模型 例如：

```text
BGE

GTE

E5

Jina

Qwen Embedding
```
---

特点：
```text
可私有化部署
```
---
企业最常用。

---

# 九、OpenAI Embedding

代表模型：
```text
text-embedding-3-small
text-embedding-3-large
```

---

特点：

```text
多语言
效果优秀
API调用简单
```

---

向量维度：

```text
1536
3072
```

---

适合：

```text
中小企业
SaaS系统
快速验证
```

---

# 十、BGE模型

BAAI： 北京智源人工智能研究院（Beijing Academy of Artificial Intelligence）的缩写。由智源研究院发布的。

---

代表：

```text
bge-small
bge-base
bge-large
bge-m3
```

---

BGE含义：
```text
BAAI General Embedding  BAAI发布的开源通用文本嵌入模型‌
```
---

特点：
```text
中文能力强
开源
RAG首选
```
---
企业部署最多。

---

# 十一、BGE-M3

目前企业非常常见。
M3：

```text
Multi Function
Multi Lingual
Multi Granularity
```
---

支持：

```text
中文
英文
日韩文
```
---

支持：
```text
短文本
长文本
```
---

支持：

```text
Dense Retrieval 稠密检索
Sparse Retrieval 稀疏检索
Hybrid Retrieval 混合检索

# 以上是信息检索中三种主流的召回策略
```
---

非常适合：
```text
企业知识库
```

---

# 十二、GTE模型

阿里巴巴推出。

---

代表：
```text
gte-large
gte-qwen2
```

---

特点：

```text
中文优秀
多语言优秀
长文本能力强
```

---

很多企业：

```text
BGE
🆚
GTE
```

二选一。

---

# 十三、Qwen Embedding
阿里通义千问系列。

---

特点：
```text
中文优化
与Qwen模型协同
```
---

适合：
```text
Qwen生态
```
企业项目。

---

# 十四、Embedding维度越高越好吗？

错误理解解：
```text
维度越高
效果越好
```
---

然鹅并非如此。

例如：

```text
768维
1024维
1536维
```
---

高维度：

优点：

```text
表达能力强
```
---

缺点：
```text
存储增加
检索变慢
成本增加
```

---

企业中：
```text
768
1024
```

已经足够。

---

# 十五、Embedding评测指标

企业不会盲选模型。

---

必须评测：

## Recall@K 召回率

---

例如：
```text
Top5
是否召回正确答案
```
---

## MRR

Mean Reciprocal Rank 平均倒数排名

---

正确答案：

```text
排第一

还是排第五
```

---

## Latency 延迟

---

Embedding速度。

---

## Cost 成本

---

API费用。

---

# 十六、企业如何选Embedding

场景1：

创业公司

---

推荐：

```text
OpenAI Embedding
```

原因：

```text
效果好
开发快
```

---

场景2：

私有化部署

---

推荐：

```text
BGE-M3
GTE-Qwen2
```

---

场景3：

中文知识库

---

推荐：

```text
BGE-M3
```

---

场景4：

多语言知识库

---

推荐：

```text
OpenAI
GTE
Jina
```
---

# 十七、Embedding与Rerank区别


---

Embedding：

负责：

```text
召回
```

---

Rerank：

负责：

```text
排序
```

---

流程：
```text
问题
↓
Embedding
↓
Top20
↓
Rerank
↓
Top3
```

---

# 十八、企业知识库案例

知识：
```text
退款申请流程

订单取消流程

售后服务规范
```

---

用户：
```text
订单怎么退？
```

---

Embedding：

发现：

```text
订单怎么退
≈
退款申请流程
```

---

成功召回。
---

然后：
```text
LLM回答
```

---

这就是：

```text
现代RAG
```

核心。

---

# 十九、现代Embedding发展路线

```text
One-Hot
↓
Word2Vec
↓
FastText
↓
BERT
↓
Sentence-BERT
↓
BGE
↓
GTE
↓
OpenAI Embedding
↓
Qwen Embedding
↓
RAG
```

---

# 二十、面试题

Q1： Embedding本质是什么？

答案：

```text
文本在高维空间中的语义表示
```

---

Q2： 为什么BERT不能直接用于向量检索？

答案：

```text
BERT擅长理解

不擅长句向量表示
```

---

Q3： Sentence-BERT解决什么问题？

答案：

```text
句子级Embedding
```

---

Q4： RAG中Embedding作用是什么？

答案：

```text
负责召回相关知识
```

---

Q5： 企业为什么要评测Embedding？

答案：

```text
不同模型召回率差异巨大
```

---

# 企业问题

问题：

如果知识库：

```text
100万文档
```

应该选择：

```text
768维

还是

3072维
```

请从：

```text
性能
成本
召回率
```
三个角度分析。

---