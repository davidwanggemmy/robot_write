一、版本说明
当前版本为v1.2.2

二、压缩包文件说明
1，libpyauboi5-v1.2.2.x64.tar.gz是ｌｉｎｕｘ６４位ｐｙｔｈｏｎ扩展库
2，libpyauboi5-v1.2.2.x86.tar.gz是ｌｉｎｕｘ３２位ｐｙｔｈｏｎ扩展库

三、压缩包内文件说明
1，libpyauboi5.so* 文件是机械臂I5的Python扩展库
2，liblog4cplus-1.2.so.5和libprotobuf.so.9是依赖库
3，robotcontrol.py是python的调用接口封装
4，目录config是ｐｙｔｈｏｎ库的日志配置文件目录

四、安装说明
1，将libpyauboi5.so*和robotcontrol.py文件放在一起
2，将liblog4cplus-1.2.so.5和libprotobuf.so.9文件拷贝到/usr/lib
3，在终端中执行sudo ldconfig
4，使用robotcontrol.py文件进行测试

五，更新说明
1，添加了末端３６０度支持


https://stackoverflow.com/questions/36816570/glibcxx-3-4-21-not-defined-in-file-libstdc-so-6-with-link-time-reference

如果出现了这样的错误，就执行一下下面的代码
wget -q -O libstdc++6 http://security.ubuntu.com/ubuntu/pool/main/g/gcc-5/libstdc++6_5.4.0-6ubuntu1~16.04.10_amd64.deb
sudo dpkg --force-all -i libstdc++6


wget -q -O gcc-5 http://archive.ubuntu.com/ubuntu/pool/main/g/gcc-5/gcc-5_5.4.0-6ubuntu1~16.04.11_amd64.deb
sudo dpkg --force-all -i gcc-5