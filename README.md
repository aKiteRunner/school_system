# school_system
School grade manage system

﻿Environment:
- Anaconda 3.6
﻿所依赖的包
- Django 2.0.5
- pymysql
- pandas


1. 安装Anaconda 3.6
2. 安装MySQL 5.7
3. 将 school_system/school_system/settings.py 中的DATABASES中的用户名与密码改为自己数据库的用户名与密码
4. 在MySQL中建立数据库'web', 并将default character set设为utf8
3. python school_system/manage.py makemigrations
4. python school_system/manage.py migrate
5. 创建管理员账户: python school_system/manage.py createsuperuser
6. python school_system/manage.py runserver 8000(默认端口, 可以自行转换), 如果出现静态文件如图片等无法加载的问题, 改
用如下命令python school_system/manage.py runserver 8000 --insecure
7. 进入 localhost:8000/ 即可

添加用户:
1. 登录localhost:8000/admin/
2. 添加User并填写用户名密码

添加学生信息:
1. 上传Excel文件，如：

| 班级 | 学号 | 姓名 | 性别 |
| --- | --- | --- | --- |
| 1101 | 1 | 张三 | 男 |
| 1101 | 2 | 李四 | 男 |
