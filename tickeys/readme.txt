
实现了CLI版本和GUI版本，在不同发行版上可能会有因为文件的缺失或者环境不同导致无法使用，出现错误可参考下面解决方法。

打开方法：

打开exe.linux-x86_64-2.7文件夹

权限：sudo chmod 777 tickeys & sudo chmod 777 run

然后打开tickeys即可

打开CLI版本： sudo sh tickeys -c

启动后会自动隐藏：按QAZ123唤出窗口


报错解决方案：

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

