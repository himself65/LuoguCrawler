# LuoguNotice

[![Build Status](https://travis-ci.org/Himself65/LuoguCrawler.svg?branch=master)](https://travis-ci.org/Himself65/LuoguCrawler) [![LICENSE](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) ![language](https://img.shields.io/badge/language-python3-blue.svg)

【暂时停更】[等待洛谷 4 发布](https://github.com/Himself65/LuoguCrawler/issues/1)

* 快速爬取洛谷上各方面信息

## Quick Start

注意：luogu/ 文件夹为必备内容，**请不要直接拷贝 example\*.py 代码直接运行**

1.  下载至本地，并解压

2.  运行相关脚本

```bash
cd LuoguCrawler

py example_download.py
```

## Scripts

* 下载你的所有 AC 代码

效果图：

快速下载你所有的 AC 代码

![04](/img/04.png)

[脚本地址](/example_codedownload.py)

* 洛谷用户爬取

多线程爬下用户信息

![03](/img/03.png)

[脚本地址](/example_userInfoCrawler.py)

* 其他脚本截图

![01](/img/01.png)

![02](/img/02.png)

## Config

* 修改 config.json 内容

* 某些特定脚本或许有需要配置的地方（将会修复）

```python
myUrl = "https://www.luogu.org/space/show?uid=72813"
myID = 72813
```

## TODO

详见[TODO.md](TODO.md)

### Credits

感谢洛谷开发组提供的灵感

## LICENSE

LowguNotice is available under the MIT license. See the [LICENSE](LICENSE) file for more information.
