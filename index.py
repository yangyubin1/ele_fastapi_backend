from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fishbase.fish_file import get_abs_filename_with_sub_path
from fishbase.fish_logger import set_log_file
from apis.v1.api import api_v1_router
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles

import uvicorn

import settings
from consts import CustomErr

# 配置logger
log_abs_filename = get_abs_filename_with_sub_path('logs', 'ele.log')[1]
set_log_file(log_abs_filename)

# Debug 文档
if settings.SERVER_DEBUG:
    docs_url = '/docs'
    redoc_url = '/redoc'
else:
    docs_url = None
    redoc_url = None


def register_router(app: FastAPI):
    """
    注册路由
    这里暂时把两个API服务写到一起，后面在拆分
    :param app:
    :return:
    """
    app.mount("/img", StaticFiles(directory="img"), name="img")

    # 项目API
    app.include_router(
        api_v1_router,
        prefix=settings.settings.API_V1_STR  # 前缀
    )


app = FastAPI(
    title=settings.PROJECT_TITLE,
    description=settings.PROJECT_DESC,
    version=settings.PROJECT_VERSION,
    docs_url=docs_url,
    redoc_url=redoc_url
)
# CORS 配置
if settings.ENABLED_CORS:
    app.add_middleware(CORSMiddleware,
                       allow_origins=['http://localhost:8000'],
                       allow_credentials=True,
                       allow_methods=['*'],
                       allow_headers=['*'], )

# https://segmentfault.com/a/1190000022946719
app.add_middleware(SessionMiddleware, secret_key='redFlowerParty')


# 注册路由
register_router(app)


@app.exception_handler(CustomErr)
def handle_custom_error(request: Request, exc: CustomErr):
    return JSONResponse(exc.to_dict(), exc.status_code)


if __name__ == "__main__":
    # uvicorn.run(app='app', host="0.0.0.0", port=8000,reload=True, debug=True)
    uvicorn.run(app='index:app', host="127.0.0.1", port=8001, reload=True, debug=True)
