# !/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author   ：zheng xingtao


from utils.log_theme import *
import environ

ROOT_DIR = environ.Path(__file__) - 3
APPS_DIR = ROOT_DIR.path("zanhu")

env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=True)
if READ_DOT_ENV_FILE:
    env.read_env(str(ROOT_DIR.path(".env")))

DEBUG = env.bool("DJANGO_DEBUG", False)

TIME_ZONE = "Asia/Shanghai"
LANGUAGE_CODE = "zh-Hans"
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOCALE_PATHS = [str(ROOT_DIR.path("locale"))]

# 数据库连接
DATABASES = {
    "default": env.db("DATABASE_URL", default="postgres:///zanhu")
}

# 是否将HTTP请求中对数据库的操作封装成事务
DATABASES["default"]["ATOMIC_REQUESTS"] = True

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# Django自己的APP
DJANGO_APPS = [
    "simpleui",  # 配置后台站点
    'django.contrib.admin',
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 'django.contrib.humanize',  # 友好的标签模板
    'django.forms',  # 用于后面重写django内置的widget模板
]

# 第三方应用的APP
THIRD_PARTY_APPS = [
    "crispy_forms",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.github",  # github登录
    # "allauth.socialaccount.providers.weibo",  # weibo登录
    # "allauth.socialaccount.providers.weixin",  # weixin登录
    # "allauth.socialaccount.providers.baidu",  # baidu登录
    # "django_celery_beat",
    "rest_framework",
    # "rest_framework.authtoken",
    "corsheaders",
    "sorl.thumbnail",
    "taggit",
    "markdownx",
    "django_comments",
    "channels",
    "haystack",
]

# 本地应用的APP
LOCAL_APPS = [
    "users.apps.UsersConfig",
    "news.apps.NewsConfig",
    "articles.apps.ArticlesConfig",
    "qa.apps.QaConfig",
    "messager.apps.MessagerConfig",
    "notifications.apps.NotificationsConfig",
    "search.apps.SearchConfig"

]

# 将上面三个APP相加
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# 更改查找组件模板的顺序，先自定义的模板，然后是系统默认的模板
FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

MIGRATION_MODULES = {"sites": "zanhu.contrib.sites.migrations"}

# 认证功能
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# 用户登录
AUTH_USER_MODEL = "users.User"
LOGIN_REDIRECT_URL = "news:list"
LOGIN_URL = "news:list"
# 用户登录的session缓存
# SESSION_ENGINE = "django.contrib.sessions.backends.db"  # 默认使用的是保存到数据库
# SESSION_ENGINE = "django.contrib.sessions.backends.cache"  # 使用cache
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"  # 使用redis数据库

# 加密算法
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

# 密码校验
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# 中间件
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# 配置redis缓存
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,
        },
    }
}

# 静态文件配置
STATIC_ROOT = str(ROOT_DIR("staticfiles"))
STATIC_URL = "/static/"
STATICFILES_DIRS = [str(APPS_DIR("static"))]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

MEDIA_ROOT = str(APPS_DIR("media"))
MEDIA_URL = "/media/"

# 模板文件的配置
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(APPS_DIR("templates"))],
        "OPTIONS": {
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "zanhu.utils.context_processors.settings_context",
            ],
        },
    }
]

# FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

CRISPY_TEMPLATE_PACK = "bootstrap4"

FIXTURE_DIRS = (str(APPS_DIR.path("fixtures")),)

# 安全配置
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False  # 是否允许HTTP获取CSRFToken
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"

# Email==> env()--在.env文件中定义
EMAIL_BACKEND = env("DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = env("DJANGO_EMAIL_HOST")
EMAIL_USE_SSL = env("DJANGO_EMAIL_USE_SSL", default=True)
EMAIL_PORT = env("DJANGO_EMAIL_PORT", default=465)
EMAIL_HOST_USER = env("DJANGO_EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("DJANGO_EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = env("DJANGO_DEFAULT_FROM_EMAIL")
EMAIL_TIMEOUT = 5

# Admin
ADMIN_URL = "admin/"
ADMINS = [("""__zheng__""", "__zheng__@example.com")]
MANAGERS = ADMINS

# Log
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用已经存在的日志器
    'formatters': {  # 日志信息显示的格式
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '[%(levelname)s] %(message)s'
        },
    },
    'filters': {  # 对日志进行过滤
        'require_debug_true': {  # django在debug模式下才输出日志
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # 日志处理方法
        'console': {  # 向终端中输出日志
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {  # 日志器
        'django': {  # 定义了一个名为django的日志器
            'handlers': ['console'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'INFO',  # 日志器接收的最低日志级别
        },
    }
}

# Celery
# INSTALLED_APPS += ['zanhu.tas kapp.celery.CeleryAppConfig']
if USE_TZ:
    CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_URL = env("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND")
CELERY_ACCEPT_CONTENT = ["json", "msgpack"]  # msgpack-> celery序列化和反序列化的数据格式
CELERY_TASK_SERIALIZER = "msgpack"  # 序列化和反序列化的数据格式，二进制的json序列化方案
CELERY_RESULT_SERIALIZER = "json"  # 读取任务结果，一般性能不高，所以使用可读性更好的json
CELERY_TASK_TIME_LIMIT = 5 * 60  # 单个任务最大运行时间
CELERY_TASK_SOFT_TIME_LIMIT = 60  # 任务的软时间限制，超时后SoftTimeLimitExceeded异常会被抛出
# CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# django-allauth
ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)  # 是否允许用户注册
ACCOUNT_AUTHENTICATION_METHOD = "username"  # 用户使用什么登录, email/user_email
ACCOUNT_EMAIL_REQUIRED = True  # 是否要求用户输入邮箱信息
ACCOUNT_EMAIL_VERIFICATION = "none"  # 是否验证邮件, none-不验证, mandatory-强制验证, optional-可选项
ACCOUNT_ADAPTER = "zanhu.users.adapters.AccountAdapter"
SOCIALACCOUNT_ADAPTER = "zanhu.users.adapters.SocialAccountAdapter"

# django-compressor
INSTALLED_APPS += ["compressor"]
STATICFILES_FINDERS += ["compressor.finders.CompressorFinder"]

# rest-framework
# REST_FRAMEWORK = {
#     "DEFAULT_AUTHENTICATION_CLASSES": (
#         "rest_framework.authentication.SessionAuthentication",
#         "rest_framework.authentication.TokenAuthentication",
#     ),
#     "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
# }

CORS_URLS_REGEX = r"^/api/.*$"

MARKDOWNX_MEDIA_PATH = "markdownx/"  # markdownx文件保存的路径
MARKDOWNX_SERVER_CALL_LATENCY = 1000  # 特殊情况特殊调节
MARKDOWNX_UPLOAD_MAX_SIZE = 5 * 1024 * 1024 # Markdown最大上传的图片大小5M
MARKDOWNX_IMAGE_MAX_SIZE = {'size':(1000, 1000), 'quality': 100}   # 设置Markdown的图片质量：1000 --> 图片不压缩
# Django Channels 的数据

# ASGI server setup
ASGI_APPLICATION = 'config.routing.application'

# 频道层的缓存
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            # channel layers缓存使用Redis 3: { "hosts": ["redis://:password@127.0.0.1:6379/
            # "hosts": [f'{env("REDIS_URL", default="redis://:root@127.0.0.1:6379")}/3', ],
            "hosts": ["redis://:root@0.0.0.0:6379/3", ],
        },
    },
}

HAYSTACK_CONNECTIONS = {
    'default': {
        # 使用的Elasticsearch搜索引擎
        'ENGINE': 'haystack.backends.elasticsearch2_backend.Elasticsearch2SearchEngine',
        # Elasticsearch连接的地址
        'URL': 'http://127.0.0.1:9200/',
        # 默认的索引名
        'INDEX_NAME': 'zanhu',
    }
}

# 对搜索的结果进行分页
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 20

# 实时信号量处理器，模型类中数据增加、更新、删除时自动更新索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'





