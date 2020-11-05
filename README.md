## Back Translation

调用各个翻译平台的API对各个问题进行回译

### 如何使用

1. 安装依赖环境: `pip install -r requirements.txt`
2. 运行测试: `python3 back_translate.py`

### 谷歌翻译

使用了`googletrans`这个包，来获取单词的翻译结果，见[py-googletrans](https://github.com/ssut/py-googletrans)。

调用时需要翻墙。

调用速度有一定限制，不能太快，否则调用报错。

### 百度翻译

使用了一部分来自[hBaiduTranslate](https://github.com/ZCY01/BaiduTranslate)的代码，用于获取单次翻译结果。

请求速度不能太快，不然会返回`None`。在代码里加入了`time.sleep`。

### 标准语言代码表

本程序的语言代码完全按照谷歌翻译的语言代码，可以在[这里](https://b.imacroc.cn/original/74.html)找到，具体如下：
- zh-CN：简体中文
- en：英语
- ja：日语
- ko：韩语
- fr：法语
- es：西班牙语
- th：泰语
- de：德语
- zh-TW：繁体中文

对于不同翻译平台API之间的语言代码不适配，会在内部通过语言代码映射进行处理。
