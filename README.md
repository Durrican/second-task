![github](https://img.shields.io/badge/%7B%E5%B0%8F%E7%BB%84%E5%90%8D%7D-%7B%E9%9B%A8%E6%96%87%E4%B8%B6%E4%B8%B6%E4%B8%B6%7D-%7Bbrown%7D.svg)

一、项目简介：

大三上软工的第二次结对编程作业的课题作业，主要为字母华容道的游戏主体以及华容道AI算法的完成。

![github](https://img.shields.io/badge/%7B%E4%BD%BF%E7%94%A8%E7%8E%AF%E5%A2%83%7D-%7Banaconda%E3%80%81python%7D-%7Bbrown%7D.svg)

二、运行环境:

用了anaconda以及python3.8相应的包

三、编译软件：

pycharm

四、使用方法：

华容道游戏可以在cmd或者anaconda命令行运行文件mainHuaRongDao.py，需要先将num.png以及目标图片放在指定的目录下，AI部分则在大比拼中使用。

五、AI使用方法

1.将打乱后的图片保存在本地中，在代码的主函数中将Image.open（）中的图片读取地址改为本地图片所在地址

2.下载github中所有切割后的小图片，将createlist中的compare的地址改为切割后的小图片的本地地址

3.然后设置强制交换的步数step和强制交换的序列

4.运行主函数，得到结果


