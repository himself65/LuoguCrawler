# LuoguNotice

【暂时停更】[等待洛谷4发布](https://github.com/Himself65/LuoguCrawler/issues/1)

提供各种洛谷爬虫

查看别人@你的犇犇

## 项目分支1 —— 下载你的所有AC代码

效果图：

快速下载你所有的AC代码

![04](/img/04.png)

[脚本地址](/example_codedownload.py)

## 项目分支2 —— 洛谷用户爬取

多线程爬下用户信息

![03](/img/03.png)

[脚本地址](/example_userInfoCrawler.py)

## 其他使用截图

![01](/img/01.png)

![02](/img/02.png)

## 使用须知

主目录创建cookie文件，然后填入以下内容：

``` json
{
    "cookie": "这里填你的luoguCookie"
}
```

其次，在各个脚本中修改需填内容，例如：

``` python
myUrl = "https://www.luogu.org/space/show?uid=72813"
myID = 72813
```

## 待办清单

详见[TODO.md](TODO.md)

### 项目灵感

本人被洛谷拒之后突然灵感写下，这东西应该没有侵犯用户协议吧应该。

## 开源协议

LowguNotice is available under the MIT license. See the [LICENSE](LICENSE) file for more information.