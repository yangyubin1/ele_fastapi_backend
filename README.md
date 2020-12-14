#  规范 - Python 脚手架

脚手架工程技术栈： Python3.7 + FastAPI，通过 pydantic 做数据校验，实现对外接口服务。

## 环境安装

### 开发工具

```
# 安装python，版本 == python3.7.2
https://www.python.org/

# 安装代码编辑器，推荐Pycharm
https://www.jetbrains.com/pycharm/download/#section=mac
```


### 代码框架、依赖包

```
# requirements.txt
fastapi==0.54.1
ujson==2.0.3
uvicorn==0.11.3
requests==2.22.0
pydantic==1.5
pyDes==2.0.1
fishbase==1.3
```

安装依赖

```
$ pip install -r requirements.txt
```


## 脚手架使用

### 使用脚手架工具在线版（自动）

[http://192.168.25.182:32092/](http://192.168.25.182:32092/)


### 下载脚手架工具（手动）

脚手架会从远程下载项目模版，并根据配置文件生成项目。

```
$ # 下载脚手架
$ wget https://cdn.cloudpnr.com/adapayresource/tiramisu.py
$ # 下载脚手架配置文件
$ wget https://cdn.cloudpnr.com/adapayresource/tiramisu-config.py
```

修改配置文件 tiramisu-config.py:

```Python
# 项目模版URL
template_project = 'https://cdn.cloudpnr.com/adapayresource/mobile_py_scaffold_1.1.0.zip'

# 约定字段，对应 FastAPI 项目名，也对应目标文件夹名称。
project_name = 'Ranger2'

# 约定字段，对应 FastAPI 项目标题。
project_title = 'Endurance Ranger2'

# 约定字段，对应 FastAPI 项目的描述。
project_description = 'Ranger2 is a single-staged-to-orbit (SSTO) reconnaissance spacecraft.'

# 约定字段，对应 FastAPI 项目的版本。
project_version = '1.0.0'

# 脚手架会将下列字典，替换到项目文件中。
tiramisu = {
    # 上述约定字段
    'project_name': project_name,
    'project_title': project_title,
    'project_description': project_description,
    'project_version': project_version,
    # 自定义配置，目前只支持两个
    'enable_cors': 'False',
    'k8s_app_name': project_name.lower()
}
```

运行脚手架

```
$ python3 tiramisu.py tiramisu-config.py
done
```


## 项目代码结构

```
apis/
    __init__.py
    deps.py
logs/
    __init__.py
models/
    __init__.py
schemes/
    __init__.py
services/
    __init__.py
settings/
    __init__.py
    product.py
    testing.py
tests/
    __init__.py
tools/
    __init__.py
Dockerfile
README.md
USAGE.md
__init__.py
consts.py
index.py
middlewares.py
requirements.txt
```

### index.py

程序主入口。

- 配置 logger
- 根据环境开启或关闭 docs
- 创建 FastAPI 对象
- 配置 CORS
- 健康页
- 错误处理


### models/

放置数据库 Model，\_\_init__.py 已经定义了 BaseModel。自建的 Model 放在各自的 py 文件中，并继承 BaseModel（通过 `from . import Base` ）

示例 user.py:

```Python
from sqlalchemy import Column, Integer, String

from . import Base


class User(Base):
    id = Column(Integer(), primary_key=True)
    username = Column(String(64))
    password = Column(String(64))

```


### schemes/

使用 pydantic 第三方模块自定义 ResquestModel、ResponseModel，可以实现类型校验，数据转换。

```Python
from pydantic import Field

from . import BaseReqModel, BaseRespModel


class UserCreateReqModel(BaseReqModel):
    username: str = Field(max_length=16)
    password: str = Field(max_length=32)
```


### services/

业务逻辑层，放置主要业务逻辑代码。

示例 user_service.py:

```Python
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from models.user import User
from schemes.user import UserCreateReqModel, UserUpdateReqModel

from tools import get_hash


class UserService:
    model = User

    def get(self, db: Session, id: int) -> Optional[User]:
        """
        获取 User
        """
        return db.query(self.model).filter(self.model.id == id).first()

    def create(self, db: Session, user_in: UserCreateReqModel) -> User:
        """
        创建用户
        """
        user = self.model(
            username=user_in.username,
            password=get_hash(user_in.password)
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def update(self, db: Session, user: User, user_in: UserUpdateReqModel) -> User:
        """
        更新用户信息
        """
        data = jsonable_encoder(user)
        if isinstance(user_in, dict):
            update_data = user_in
        else:
            update_data = user_in.dict(exclude_unset=True)
        for field in data:
            if field in update_data:
                setattr(user, field, update_data[field])
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

```


### apis/

对外提供的接口服务。

**deps.py 文件**：配置 api 层依赖，例如获取数据库连接、获取当前用户等等。

```Python
from typing import Generator

from authlib.jose import jwt
from authlib.jose.errors import JoseError
from fastapi import Depends, Cookie, HTTPException
from sqlalchemy.orm import Session

import settings
from middlewares import db_session
from models.user import User
from services.user_service import UserService


def get_db() -> Generator[Session, None, None]:
    """
    获取数据库连接
    """
    db = None
    try:
        db = db_session()
        yield db
    finally:
        if db is not None:
            db.close()


def get_current_user(
    db: Session = Depends(get_db), bff_token: str = Cookie(None)
) -> User:
    """
    获取当前用户
    """
    # bff_token 为 Cookie 字段，其值为 token 内容。
    token = bff_token
    if token is None:
        raise HTTPException(401)

    try:
        # 解码 jwt
        payload = jwt.decode(token, settings.SECRET_KEY)
        uid: str = payload.get("sub")
        if uid is None:
            raise HTTPException(401)
    except JoseError:
        raise HTTPException(401)

    user = UserService().get(db, int(uid))
    if user is None:
        raise HTTPException(401)
    return user
```

**router_xxx.py 文件**：实际负责处理对应业务的接口。

示例 router_user.py:

```Python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from apis.deps import get_db, issue_token, get_current_user
from models.user import User
from schemes.user import UserCreateRespModel, UserCreateReqModel
from services.user_service import UserService

# 创建 APIRouter 路由子模块
router = APIRouter()


@router.post('/register', tags=['用户'], response_model=UserCreateRespModel)
def register(user_create: UserCreateReqModel, *, db: Session = Depends(get_db)):
    """
    注册用户
    """
    # 调用 service 创建用户。
    user = UserService().create(db, user_create)
    # 生成 token。
    token = issue_token(user)
    return {
        'response_code': 0,
        'response_msg': '',
        'token': token,
        # ...
    }


@router.get('/me', tags=['用户'], response_model=UserCreateRespModel)
def get_me(*, user: User = Depends(get_current_user)):
    """
    获取当前登录用户的信息。
    """
    # user 即为当前用户。
    return {
        'response_code': 0,
        'response_msg': '',
        'user': user.to_dict()
    }
```

创建 router_user.py 后，在 index.py 使用下列方法将 APIRouter 绑定到 app 上。

```Python
from apis import router_user

app.include(router_user.router, prefix='/api/user')
```

### settings/

项目配置模块，结构如下

```
settings/
    __init__.py
    product.py
    testing.py
    dev.py
```

- 目前配置放在各环境对应文件中，由 \_\_init__.py 根据环境变量 `ENV_STATUS` 加载对应配置文件。
- 开发环境配置 dev.py 需要自行创建， **请不要提交到仓库** 。

**使用方法**

例如 testing.py 中:

```Python
REDIS_URL = 'redis://:password@127.0.0.1/1'
```

调用时，要确保环境变量 ENV_STATUS 是 testing：

```Python
import settings

print(settings.REDIS_URL)
```

### middlewares.py

集中管理中间件实例，例如数据库连接、代理，缓存，消息队列等等，以防止循环依赖。


### consts.py

管理项目常量，自定义异常。


### tests/

单元测试
﻿

### tools/

工具类，提供多种通用功能


### Dockerfile

流水线构建使用的 Dockerfile。


### manifests/

流水线构建使用的 K8S 配置文件，目录对应环境。


### logs/

```Python
from fishbase.fish_file import get_abs_filename_with_sub_path
from fishbase.fish_logger import set_log_file

log_abs_filename = get_abs_filename_with_sub_path('logs', 'server.log')[1]
set_log_file(log_abs_filename)
```

默认使用 Fishbase 配置的日志输出目录。

**日志文件请不要提交到仓库！！！**
# ele_fastapi_backend
