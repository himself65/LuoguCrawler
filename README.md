# LuoguNotice

即时回复别人的犇犇，从luogu上快速的爬下题面（无数据）

(当然以上都还没开始做)

查看别人@你的犇犇

## 项目分支 —— 洛谷用户爬取

成果如下：

![03](/img/03.png)

[脚本](/example_userInfoCrawler.py)

## 使用截图

![01](/img/01.png)

![02](/img/02.png)

## 使用须知

自己在main.py同文件夹里创建cookie.json 然后填入你的cookie，如下。

``` json
{
    "cookie": "这里填你的luoguCookie"
}
```

其次，在main.py中修改

``` python
myUrl = "https://www.luogu.org/space/show?uid=72813"
myID = 72813
```

## 待办清单

详见[TODO.md](TODO.md)

### 其他

本人被洛谷拒之后突然灵感写下，这东西应该没有侵犯用户协议吧（逃。不过本人的确太弱了，还需努力。

### LICENSE

LowguNotice is available under the MIT license. See the [LICENSE](LICENSE) file for more information.