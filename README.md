# PYTHON_SIFT
使用的python版本为2.7.12

启动server , server监听10001端口
向server发送命令
    1 E:\test\upload.jpg
    1 E:\test\upload.jpg E:\test\upload_feature.jpg
    2 E:\test\upload.jpg E:\test\upload_feature.txt
    3 E:\test\upload.jpg E:\test\upload1.jpg
    3 E:\test\upload.jpg E:\test\upload1.jpg E:\test\upload_upload1_match.jpg
    4 F:\images E:\test\upload.jpg
 其中1表示绘制特征图 , 2存储特征点到对应txt文件中 , 3绘制匹配图 , 4为在对应位置中找到所有的图像
 对于画特征点和匹配图的命令，最后一个参数是对应绘制图的存储位置，如果没有提供绘制点的位置，则直接显示
  
