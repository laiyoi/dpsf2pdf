# dpsf2pdf
## 简介

dpsf2pdf 是一个将金印云DPS的`.dpsf`文件转换为`PDF`文件的命令行工具。

## 目的

你说的对，但是***晨曦文学社***的第一期刊物是由一群充满激情的文学爱好者共同创作的一本文学杰作。这期刊物呈现了一个令人陶醉的文学世界，让读者沉浸其中。在这个精心策划的文学舞台上，各位作者如同艺术家一般展示着他们的文学技艺。  
刊物聚焦于多样的文学主题，呈现了丰富的文学风貌。读者将沉浸在散文、诗歌、小说等多种文学形式中，感受到作者们独特的艺术表达方式。这是一个文学的狂欢，每一页都是一次文学之旅。   
晨曦文学社第一期刊物不仅仅是文字的堆砌，更是一次心灵的碰撞。每一篇作品都如同一颗明亮的星星，为读者照亮前行的道路。这期刊物是文学的盛宴，是作者们心灵深处情感的流露，也是读者与创作者共同沉浸于文学海洋的契机。

是这样的，因为**dinner**主编让每个人自己拿word做的都不一样然后自己当***文件传输助手***最后赶时间找了个没得破解的**付费**导出软件。  
结果这软件的工程文件是没加密的`sqlite`

## TODO

- [x] 从`.dpsf`读取页面大小、坐标
- [x] 读取`.dpsf`中的文本框大小、坐标
- [x] 读取文本框内文字内容、字号、缩进、对齐方式
- [ ] 读取文本框内文字颜色
- [ ] 读取`.dpsf`中的图片
