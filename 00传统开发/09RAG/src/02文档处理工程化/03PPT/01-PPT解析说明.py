"""
项目中一般都是PDF/word
宣讲中一般会使用PPT展示知识

企业知识库中大量知识其实都在PPT里
比如：
    产品介绍PPT
    解决方案PPT
    培训课件
    销售话术PPT
    招投标PPT
    技术架构PPT
    项目汇报PPT
    行业研究报告

甚至有的公司：PDF不到20%、Word不到30%、PPT占50%以上
尤其是：咨询公司、金融行业、ToB软件公司、AI创业公司


一、PPT的本质
pptx=zip压缩包，本质：XML结构文件
pptx 是 OOXML（Office Open XML） 格式，zip 包里是一组 XML + 媒体文件 + 关系文件
修改后缀：demo.pptx -> demo.zip
文字在 slideN.xml 里，图片在 ppt/media/ 里，图表是 chartN.xml + 内嵌 xlsx

demo.pptx (zip)
├── [Content_Types].xml
├── _rels/.rels
├── ppt/
│   ├── presentation.xml
│   ├── slides/slide1.xml ...
│   ├── slideLayouts/
│   ├── slideMasters/
│   ├── media/          ← 图片、视频都在这
│   └── notesSlides/    ← 备注页
└── docProps/
二、企业中的PPT类型
类型1： 培训课件
比如：
    Java培训
    AI培训
    产品培训
特点：标题+正文

类型2：解决方案PPT
比如：
    智慧园区
    智能客服
    大模型解决方案

类型3：招投标PPT
比如L：
    技术方案
    实施方案
特点L：大量表格

类型4：研究报告
比如：券商研报、行业分析
特点：图表占70%以上

难点：
第1页：
AI客服解决方案
第2页：
整体架构
（下面是一张架构图）

直接提取：
AI客服解决方案
整体架构
[知识丢失90%。]

原因：
丢失的不只是"图片里的信息"，还有：
SmartArt / 组合形状（group shape） 里的文字，python-pptx 默认遍历不到嵌套形状
表格（招投标PPT大量表格）需要单独处理
图表（chart） 的数据在 embedded xlsx 里，不是图片
备注页（notes） 常含讲稿，价值很高但常被忽略
演讲者备注、超链接、隐藏页

所以企业通用解决方式：
    文字解析+图片理解+多模态RAG


三、python-pptx
    uv add python-pptx
"""