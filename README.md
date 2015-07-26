# Tickeys-linux
![Tickeys Icon](http://ww1.sinaimg.cn/large/8cc88963gw1er08h49mp5j203k03kdfx.jpg)
Instant audio feedback when typing. For Linux. 

### For use
___

实现了CLI版本和GUI版本，在不同发行版上可能会有因为文件的缺失或者环境不同导致无法使用，出现错误可参考下面解决方法。

打开方法：
权限：sudo chmod 777 run.sh
然后打开run.sh即可
打开CLI版本： sudo ./run -c

启动后会自动隐藏：按QAZ123唤出窗口

#### 报错解决方案：

提示：
ImportError: libSDL-1.2.so.0: cannot open shared object file: No such file or directory

解决方法：使用`yum install libSDL-1.2.so.0`安装依赖

提示：
NotImplementedError: mixer module not available
解决方法：同上


Debian and Ubuntu 用户则可以尝试安装:

    sudo apt-get install xdotool 
    sudo apt-get install libsdl1.2-dev
    sudo apt-get install libsdl-mixer1.2
    sudo apt-get install libsdl-ttf2.0

### For dev
___

安装依赖：
pip install -r requirements.txt

使用cx_freeze进行打包：
命令：`sudo python bulid.py bulid`

播放音乐通过pygame的mixer实现。
键盘事件获取通过evdev实现。
窗口的控制使用xdotool来实现。

获取窗口ID：
WID=`xdotool search "Tickeys" | head -1`

激活：
xdotool windowactivate --sync $WID

Hide实现：
xdotool getactivewindow windowminimize
or
xdotool getactivewindow windowmove 999 0

另一实现方法是使用wmctrl来控制窗口

### problem

___

    目前在Fedora上好像无法使用GUI的，不知道是因为我用虚拟机开的问题还是Kivy这个框架的问题，因为提示The 3D features of the virtual machine will be disabled。
