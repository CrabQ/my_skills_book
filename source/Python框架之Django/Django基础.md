# Django基础

## 简单Django项目流程

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

2. 创建用户登陆APP

   ```python
   python manage.py startapp df_user
   ```

3. 添加应用

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

4. 创建视图

    ```python
    # 用户注册页面
    def register(request):
        return HttpResponse('ok')
    ```

5. 配置url

    ```python
    from django.contrib import admin

    urlpatterns = [
        url(r'^admin/', include(admin.site.urls)),
        url(r'^register/$', views.register),
    ]
    ```

6. 运行测试

    ```shell
    python manage.py runserver
    ```
