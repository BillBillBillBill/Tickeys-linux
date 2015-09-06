# Tickeys-linux

Instant audio feedback when typing. For Linux.

如果有任何问题或建议，可以在这提出：
[![Join the chat at https://gitter.im/BillBillBillBill/Tickeys-linux](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/BillBillBillBill/Tickeys-linux?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
![Tickeys Icon](http://img.blog.csdn.net/20150802103616846)

# 简介
Tickeys是一款很强大的键盘音效软件。Tickeys 自带了四种声音效果方案，有打字机、冒泡、机械键盘、剑气等。每天都听着键盘声音是不是很烦闷，现在有了这款神器你就可以瞬间帮助自己的键盘加上逼格特效。

这个软件之前发布了Windows和Mac版，Tickeys 是由 Nozama 所做的一个 Mac 平台的开源小项目 ([GitHub](https://github.com/yingDev/Tickeys))，Windows 版由黄飞实现。我使用了之后，觉得挺有意思的，因此用Python写了个Linux版的。

# 项目网站
http://www.yingdev.com/projects/tickeys

PyPI: https://pypi.python.org/pypi/tickeys 

# Tickeys的Mac版本
https://github.com/yingDev/Tickeys

# 安装说明
在不同发行版上可能会有因为文件的缺失或者环境不同导致无法使用，需要安装相关依赖。

#### 快速安装（最方便）：执行`sudo apt-get install python-dev python-pip python-kivy xdotool && sudo easy_install tickeys`，使用此命令可忽略下面的方法。

* 以下方法需要**先执行**`sudo apt-get install python-dev python-pip python-kivy xdotool`来安装依赖，一般这样就可以满足运行条件了。

###方法1.自动安装

* 执行`sudo easy_install tickeys` or `sudo pip install tickeys`安装
* 然后通过 `sudo tickeys` 来打开 (sudo tickeys -c 打开CLI版本)

###方法2.半自动安装

* 下载 https://github.com/BillBillBillBill/Tickeys-linux/archive/master.zip ，解压后运行 `sudo python setup.py install`
* 然后通过 `sudo tickeys` 来打开 (sudo tickeys -c 打开CLI版本)

###方法3.直接下载编译好的程序

* 通过本目录下载tickeys-v0.1.1a5.tar.gz或通过 http://pan.plyz.net/d.asp?u=570504130&p=tickeys-v0.1.1a5.tar.gz 下载
* 打开文件夹 然后 `sudo chmod 777 tickeys && sudo chmod 777 run`
* 然后打开tickeys
* 打开CLI版本： `sudo sh tickeys -c`

###方法4.在本地打包成可执行程序

* 先下载 https://github.com/BillBillBillBill/Tickeys-linux/archive/master.zip
* 然后使用cx_freeze进行打包：`sudo python bulid.py bulid`
* 然后下面跟方法2一样打开

#### 其他错误解决方案：

* 无法隐藏窗口：

解决方法：使用`sudo apt-get install xdotool `安装xdotool

* 若没有setuptools or pip

解决方法：使用`sudo apt-get install python-pip` 安装

* Python.h：没有那个文件或目录 

解决方法：使用`sudo apt-get install python-dev`安装

* ImportError: No module named Cython.Distutils  

解决方法：使用`sudo easy_install cython`安装


* ImportError: libSDL-1.2.so.0: cannot open shared object file: No such file or directory

    解决方法：使用`yum install libSDL-1.2.so.0`安装依赖

* NotImplementedError: mixer module not available

    解决方法：同上

Debian and Ubuntu 用户则可以尝试安装:

    * sudo apt-get install xdotool 
    * sudo apt-get install libsdl1.2-dev
    * sudo apt-get install libsdl-mixer1.2
    * sudo apt-get install libsdl-ttf2.0

# 使用说明
需要以root权限才能启动，实现了CLI版本和GUI版本，默认启动GUI版本，GUI版本启动后会自动隐藏，按QAZ123唤出窗口。

调整参数后会自动保存，下次开启会使用该设置。

Open at startup是开启开机自启动功能选项，开关置为ON开启功能，开关置为OFF关闭功能。

# TODO
1.打开程序后出现气泡提醒（已实现）
2.使GUI真正后台化（已实现）
3.按最小化按钮或退出按钮隐藏GUI
4.程序运行情况输出到log文件中,以便调试（已实现）

# 开发
* ####编码规范: PEP8

* ####应用UI框架：Kivy

* ####开源许可证： MIT License

依赖安装：

    pip install -r requirements.txt

使用cx_freeze进行打包：

    命令：`sudo python bulid.py bulid`


播放音乐通过pygame的mixer实现。

键盘事件的获取通过evdev实现。

窗口的控制使用工具xdotool来实现。(另一方法是使用wmctrl来控制窗口)

xdotool的使用：
* 获取窗口ID：
    WID=`xdotool search "Tickeys" | head -1`

* 激活窗口：
    xdotool windowactivate --sync $WID

* 隐藏窗口实现：
    xdotool getactivewindow windowminimize
    或
    xdotool getactivewindow windowmove 999 0


# 项目结构
Tickeys-linux
```
├── AUTHOURS
├── LICENSE
├── MANIFEST.in
├── README.md
├── setup.py
└── tickeys
    ├── build.py
    ├── CLI.py
    ├── GUI.py
    ├── config.py
    ├── __init__.py
    ├── KeyboardHandler.py
    ├── logger.py
    ├── requirements.txt
    ├── Resources
    │   └── data
    │       ├── bubble
    │       ├── mechanical
    │       ├── sword
    │       ├── typewriter
    │       └── schemes.json
    ├── run.py
    ├── SoundPlayer.py
    ├── StartupHandler.py
    ├── tickeys
    ├── tickeys.png
    └── tickeysui.kv
```

# 文件说明
* build.py 打包函数

* run.py 存放入口函数

* readme.txt 放进打包后程序文件夹的readme

* requirements.txt 开发模块依赖包

* tickeys 启动tickeys的脚本，打包时放进打包后的文件夹使用

* CLI.py 启动CLI的模块

* GUI.py 启动GUI的模块

* config.py 处理配置保存和读取的模块

* tickeysui.kv kv的ui文件，当在GUI中不使用load_string来创建时把此文件更名为Tickeys.kv使用

* KeyboardHandler.py 处理键盘输入的函数

* logger.py 日志记录函数，调试时使用

* SoundPlayer.py 播放声效的模块

* StartupHandler.py 控制开机自启动的模块


# 问题
* 目前在Fedora上好像无法使用GUI的，不知道是因为我用虚拟机开的问题还是Kivy这个框架的问题，因为提示The 3D features of the virtual machine will be disabled。

* 用pyinstaller来打包会有很多模块打包不进去，故使用cx_freeze打包

# 作者
Huang Xiongbiao

billo@qq.com
