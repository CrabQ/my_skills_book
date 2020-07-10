# django开发项目流程

1. 切换虚拟环境，新建项目

   ```python
   # 切换虚拟环境
   conda activate first_pro
   # 安装django
   pip install django==2.2
   # 新建项目
   django-admin startproject first_pro
   # 测试是否成功启动
   python manage.py runserver 127.0.0.1:8080
   ```

2. 新建模板文件夹`templates`(与`manage.py`同级)

   ```python
   # 修改settings.py中的TEMPLATES
   'DIRS': [os.path.join(BASE_DIR, 'templates')],
   ```

3. 修改配置文件

   ```python
   # 时区
   LANGUAGE_CODE = 'zh-Hans'
   TIME_ZONE = 'Asia/Shanghai'
   # 数据库
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'HOST':'localhost',
           'PORT':'3306',
           'USER':'tiantian',
           'PASSWORD':'tiantian',
           'NAME': 'tiantian',
       }
   }
   ```

4. 新建静态文件文件夹`static`(与`manage.py`同级)

   ```python
   # 在settings.py中增加静态文件夹路径
   STATICFILES_DIRS = [
       os.path.join(BASE_DIR, 'static')
   ]
   ```

5. 创建用户登陆APP

   ```python
   python manage.py startapp df_user
   ```

6. 设计模型类

   ```python
   from django.db import models

   # Create your models here.
   class UserInfo(models.Model):
       uname = models.CharField(max_length=20)
       upwd = models.CharField(max_length=40)
       uemail = models.CharField(max_length=30)
       ushou = models.CharField(max_length=20)
       uaddress = models.CharField(max_length=100)
       uyoubian = models.CharField(max_length=6)
       uphone = models.CharField(max_length=11)
   ```

7. 添加应用

   ```python
   # 在settings.py中INSTALLED_APPS增加df_user
   INSTALLED_APPS = (
       'django.contrib.admin',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',

       'df_user',
   )
   ```

8. 生成迁移文件、执行迁移

   ```python
   # 生成迁移文件
   python manage.py makemigrations
   # 执行迁移
   python manage.py migrate
   ```

9. 创建应用的的模板文件夹`df_user`(`templates/df_user`)

10. 创建视图

    ```python
    # 用户注册页面
    def register(request):
        return render(request, 'df_user/register.html')
    ```

11. 配置url

    ```python
    # 根级url.py添加应用url
    from django.contrib import admin

    urlpatterns = [
        url(r'^admin/', include(admin.site.urls)),
        url(r'^user/', include('df_user.urls')),
    ]

    # 创建应用urls.py:df_user/urls.py,添加url配置
    from django.conf.urls import url
    from df_user import views

    urlpatterns = [
        url(r'^register/$', views.register)
    ]
    ```

12. 运行测试

    ```python
    python manage.py runserver
    ```
