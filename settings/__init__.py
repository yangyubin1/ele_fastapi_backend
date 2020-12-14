import os


def get_env(name, default=None):
    return os.environ.get(name, default)


# 项目配置
PROJECT_TITLE = 'ele'
PROJECT_DESC = 'ele'
PROJECT_VERSION = '1.0.0'

# 运行环境
ENV_STATUS = get_env('ENV_STATUS', 'dev')

SERVER_DEBUG = ENV_STATUS != 'product'
# 支持跨域
ENABLED_CORS = True

# 具体配置
if ENV_STATUS == 'product':
    from .product import settings
elif ENV_STATUS == 'testing':
    from .testing import settings
else:
    # dev.py 不要提交
    from .dev import settings
