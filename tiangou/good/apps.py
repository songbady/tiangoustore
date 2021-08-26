from django.apps import AppConfig


class GoodConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'good'
    verbose_name = '商品管理' #配置名字