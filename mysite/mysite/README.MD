遇到的问题


#1.django同步数据问题
原来用
>python manage.py syncdb
先改为：
Django 1.9以后没有syncdb,改为自建app模块名称为input，建好model需要同步的时候，先在程序根目录运行python manage.py makemigrations input，这样就进行了第一步的同步
然后在运行runserver之前，再运行一个 python manage.py migrate,这样就好了，然后登陆http://127.0.0.1:8000/admin就发现已经建了数据库表了。

#2.python manage.py migrate 报如下错误
>django.db.utils.InternalError: (1050, u"Table 'auth_permission' already exists")

解决办法:

https://stackoverflow.com/questions/3090648/django-south-table-already-exists
>since you already have the tables created in the database, you just need to run the initial migration as fake
./manage.py migrate myapp --fake
make sure that the schema of models is same as schema of tables in database.

#3.python manage.py migrate 仍是报错

>django.db.utils.OperationalError: (1142, u"REFERENCES command denied to user 'vamei'@'localhost' for table 'django_content_type'")

但是数据其实已经建立，登陆数据库，查看数据库，表格，插入内容。

#一些Django错误问题解决方法总结

错误: No module named 模块名称 
找不到模块，需要将模块添加到python的搜索目录中。 
方法一、在运行时添加参数--pythonpath="路径" 
方法二、将路径添加到path中。在settings.py中增加sys.path.insert(0,"path") 
方法三、安装模块到python的dist-packages文件夹中

#4 ImportError: No module named context_processors
解决办法：
>from django.core.context_processors import csrf

改为

>from  django.template.context_processors import csrf

https://docs.djangoproject.com/en/1.10/releases/1.8/#django-core-context-processors

>This is the code from 1.9.1
EMPLATES = [
{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(BASE_DIR, 'templates')],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.core.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
},
]

This is code for 1.10

>TEMPLATES = [
{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(BASE_DIR, 'templates')],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
},
]
The line django.core.context_processors.request is not valid in 1.10. Remove it and the code works well.

#5 报错CSRF token missing or incorrect.
>{% csrf_token %}

错写为

><% csrf_token %>

修改过来！！

#6 用django 模板中文显示乱码
网上找了各种解决办法，最终解决方法：　　因为原先写的模型代码中的方法用提　def __str__(self): 这个是旧版本中用的方法，在Django　0.96以后的版本中，应该换成　def __unicode__(self):，　这样就解决了字符串传递时出错的问题，统一编码为Unicode字符串。http://blog.csdn.net/jiangnanandi/article/details/3574007

>class Character(models.Model):
    name=models.CharField(max_length=200)
    # def __str__(self):
    #     return self.name
    def __unicode__(self):
         return self.name
