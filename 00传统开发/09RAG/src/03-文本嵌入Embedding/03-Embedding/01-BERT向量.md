#  BERT向量
    "Word2Vec 和 FastText 已经能表示词义了，为什么还要 BERT？" 
    答案是：它们生成的是静态向量（一个词永远一个向量），无法理解上下文（"苹果"在"苹果好吃"和"苹果手机"里含义不同，但 Word2Vec 给的是同一个向量）。BERT 通过 Transformer + Self-Attention 实现了动态向量，同一个词在不同句子里生成不同向量。
---

# 要求理解：

* 为什么Word2Vec和FastText还不够
* 什么是静态词向量
* 什么是上下文(Context)
* BERT为什么诞生
* Transformer是什么
* Self-Attention是什么
* BERT如何生成向量
* BERT如何理解一词多义
* BERT与现代Embedding模型关系
* BERT在RAG中的作用

---

# 一、之前两节内容

已经学习：

```text
One-Hot
↓
Word2Vec
↓
FastText
```

Word2Vec解决：
```text
语义表示问题
```

FastText解决：
```text
OOV问题
```
（未登录词问题）

---

那么问题来了：

```text
Word2Vec
+
FastText

已经很好了

为什么还需要BERT？
```

---

# 二、Word2Vec最大的缺陷

场景距离：
```text
苹果很好吃
```

Word2Vec：
```text
苹果
↓
固定向量
```

---

再看：
```text
苹果手机很好用
```

Word2Vec：

```text
苹果
↓
还是同一个向量
```

---

问题来了：

第一句：
```text
苹果

水果
```

第二句：
```text
苹果

公司
```

含义完全不同。

---

但Word2Vec认为：
```text
完全一样
```

因为：

```text
一个词
只有一个向量
```

---

# 三、什么是静态词向量

Word2Vec：

```text
苹果
↓
固定向量
```

无论出现在哪里：

```text
苹果水果

苹果手机

苹果公司
```

向量都一样。

---

这种表示方式称为：

```text
Static Embedding

静态向量
```

---

问题：

```text
无法理解上下文
```

---

# 四、人类如何理解语言

看一句话：

```text
今天去银行开户
```

我们知道：
```text
银行 = Financial Bank
```
金融机构。

---

再看：

```text
河边有一家银行
```

你会发现：

```text
不合理
```

应该是：

```text
河岸（Bank）
```

---

为什么人类能理解？？？？？

因为：

```text
看上下文
```

---

银行前面：

```text
开户
```

金融含义。

---

银行前面：

```text
河边
```

地理含义。

---

这就是：

```text
Context

上下文
```

---

# 五、BERT为什么出现

Google发现：

语言理解核心问题：

```text
上下文理解
```

---

2018年

Google发布：

```text
BERT
```


```text
论文：BERT: Bidirectional Encoder Representations from Transformers
```

彻底改变NLP领域。

---

# 六、BERT名字解释

B：
```text
Bidirectional
双向。
```
---

E：
```text
Encoder
编码器。
```
---

R：
```text
Representations
表示。
```
---

T：
```text
Transformers
Transformer架构。
```
---

意思：

```text
利用Transformer
学习双向上下文表示
```
---

# 七、Transformer是什么

BERT建立在Transformer之上。

---

Transformer发表于：

```text
2017    Attention Is All You Need
```

---

在此之前：

```text
RNN

LSTM

GRU
```

主导NLP。

---

问题：

句子太长：

```text
前面内容忘记
```

---

Transformer解决：

```text
一次看到整个句子
```

---

例如：

```text
退款流程是什么
```

模型同时看到：

```text
退款
流程
是什么
```

全部内容。

---

# 八、Self-Attention是什么

Transformer核心：

```text
Self-Attention
```
自注意力机制。

---

假设：
```text
苹果手机很好用
```

当处理：

```text
苹果
```

时。

模型会关注：

```text
手机
```

---

因为：

```text
苹果
+
手机
```

说明：

```text
Apple公司
```

---

不是水果。

---

Self-Attention本质：

```text
一个词

关注句子中所有词
```

---

# 九、Attention直观理解

句子：

```text
我想申请退款
```

处理：

```text
退款
```

时。

模型关注：

```text
申请
退款
```

---

权重可能：
```text
申请   0.4

退款   0.5

我     0.05

想     0.05
```

---

因此：
```text
退款
```
获得更多上下文信息。

---

# 十、BERT如何生成向量

输入：
```text
苹果手机很好用
```

---

Tokenizer：
```text
苹果

手机

很好

用
```

---

经过：
```text
Embedding Layer
↓
Transformer
↓
Self Attention
↓
Encoder
```

---

输出：

```text
苹果向量

手机向量

很好向量

用向量
```

---

注意：

```text
苹果
```
向量已经变化。

因为：
```text
受到了手机影响
```

---

# 十一、动态向量

Word2Vec：
```text
苹果

=

固定向量
```

---

BERT：
```text
苹果(水果)

≠

苹果(公司)
```

---

因此：

```text
同一个词

不同上下文

不同向量
```

---

称为：

```text
Dynamic Embedding
动态向量
```

---

# 十二、举例理解

例子1：
```text
苹果很好吃
```

BERT：
```text
苹果

接近：
    香蕉
    橘子
    西瓜
```

---

例子2：

```text
苹果手机很好用
```

BERT：

```text
苹果

接近：
    华为
    小米
    三星
```

---

同一个词：

```text
向量不同
```

---

这就是：

```text
BERT革命性突破
```

---

# 十三、BERT预训练任务

BERT训练时做两件事。

---

## 任务1

Masked Language Model

MLM

---

句子：

```text
我喜欢吃苹果
```

随机遮挡：

```text
我喜欢吃[MASK]
```

---

目标：

```text
预测：

苹果
```

---

模型被迫学习：

```text
上下文关系
```

---

## 任务2

Next Sentence Prediction

NSP

---

句子1：

```text
我想申请退款
```

句子2：

```text
退款需要订单号
```

---

判断：

```text
是否连续句子
```

---

学习：

```text
句间关系
```

---

# 十四、BERT为什么重要

几乎所有现代Embedding：

```text
Sentence-BERT

BGE

GTE

E5

Qwen Embedding

Jina Embedding
```

都建立在：

```text
Transformer
```

基础上。

---

如果没有BERT：

```text
不会有今天的RAG
```

---

# 十五、BERT与Sentence-BERT

一定不要产生误解：

```text
BERT = Embedding
```

其实不完全正确。

---

BERT擅长：

```text
理解文本
```

---

但不擅长：

```text
句向量检索
```

---

于是出现：

```text
Sentence-BERT
```

简称：

```text
SBERT
```

---

专门用于：

```text
相似度计算
```

---

这也是：

```text
现代Embedding模型祖先
```

---

# 十六、BERT与RAG

RAG核心：
```text
问题
↓
Embedding
↓
检索
↓
答案
```

---

Embedding模型：

```text
BGE

GTE

Qwen Embedding
```

本质：

```text
Transformer
+
BERT思想
```

---

因此：

```text
理解BERT

就理解了现代Embedding
```

---

# 十七、企业案例

企业知识库：

文档：

```text
退款申请流程
```

---

用户问题：

```text
订单怎么退
```

---

关键词完全不同。

---

Word2Vec：

效果有限。

---

BERT类模型：

能够理解：

```text
订单怎么退

≈

退款申请流程
```

---

因此：

```text
召回率大幅提升
```

---

# 十八、BERT与FastText对比

| 能力     | FastText | BERT |
| ------ | -------- | ---- |
| OOV处理  | √        | √    |
| 上下文理解  | ×        | √    |
| 静态向量   | √        | ×    |
| 动态向量   | ×        | √    |
| 句子理解   | 弱        | 强    |
| RAG适用性 | 一般       | 优秀   |

---

# 十九、面试题

Q1： Word2Vec最大缺陷是什么？

答案：

```text
静态向量

无法理解上下文
```

---

Q2： BERT最大创新是什么？

答案：

```text
双向上下文理解
```

---

Q3： 什么是Self-Attention？

答案：

```text
一个词关注句子中所有词
```

---

Q4： 什么是动态向量？

答案：

```text
同一个词

不同上下文

不同向量
```

---

Q5： 为什么说现代Embedding建立在BERT基础上？

答案：

```text
现代Embedding都基于Transformer架构

继承了BERT上下文表示思想
```

---

# 企业实场景问题

问题：

为什么：

```text
订单怎么退

退款申请流程
```

能够被Embedding模型识别为相似？

请结合：

```text
Transformer

Attention

上下文
```

解释。

---
总结：Word2Vec 给每个词一张"死画像"，BERT 让画像随句子"活"起来；靠的是 Transformer 的 Self-Attention 让每个词看遍全句；这种动态向量思想，正是今天所有 Embedding 模型和 RAG 检索的基石