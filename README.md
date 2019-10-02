# Django 博客系统

### 功能

>集成了Python3.7、 Django2.2.5 、客户端 React16、ES6+

- 用户注册（密码的加盐保护）、登录（JWT 认证）
- 博客编辑发布（markdown）、修改
- 评论及回复、点赞，消息通知

### 开发

将项目克隆值本地：`git clone https://github.com/qumuchegi/django-react-blog.git`

激活数据库模型：`python3 ./manage.py makemigrations`

同步数据库:   `python3 manage.py migrate`

进入项目，运行网站：`python3 manage.py runserver`