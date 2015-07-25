
提示：
ImportError: libSDL-1.2.so.0: cannot open shared object file: No such file or directory
解决方法：使用`yum install libSDL-1.2.so.0`安装依赖
安装:
 SDL                      i686         1.2.15-17.fc22        fedora       223 k
 SDL                      x86_64       1.2.15-17.fc22        fedora       214 k
 glibc                    i686         2.21-5.fc22           fedora       4.2 M
 nss-softokn-freebl       i686         3.18.0-1.fc22         fedora       196 k

提示：
NotImplementedError: mixer module not available
解决方法：同上
安装:
 SDL_mixer         i686           1.2.12-7.fc22            fedora          96 k
 SDL_mixer         x86_64         1.2.12-7.fc22            fedora          95 k
 libmikmod         x86_64         3.3.7-1.fc22             fedora         148 k


Debian and Ubuntu 用户可以尝试安装:
    sudo apt-get install xdotool 
    sudo apt-get install libsdl1.2-dev
    sudo apt-get install libsdl-mixer1.2
    sudo apt-get install libsdl-ttf2.0


获取ID：
WID=`xdotool search "Tickeys" | head -1`
激活：
xdotool windowactivate --sync $WID
Hide实现：
xdotool getactivewindow windowminimize
xdotool getactivewindow windowmove 999 0

另一实现方法是使用wmctrl控制窗口