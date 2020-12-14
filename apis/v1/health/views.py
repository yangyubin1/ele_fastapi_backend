from fastapi import APIRouter

from consts import CustomErr

router = APIRouter()


@router.get('/api/bff/probe', tags=['health'])
@router.head('/api/bff/probe', tags=['health'])
def startup_probe():
    """
    存活探针，用于 K8S 探活，代表服务器已启动。
    """
    return {'message': 'bff is healthy'}


@router.get('/api/bff/health', tags=['health'])
@router.head('/api/bff/health', tags=['health'])
def ready_probe():
    """
    就绪探针，接口健康页。用于 K8S 就绪检查、SLB 心跳，代表服务器当前可以对外服务。
    对于 SLB 心跳，需要实现 HEAD 方法。
    """
    return {'message': 'bff is ready'}


@router.get('/', tags=['index'])
def home():
    """
    index
    """
    return {'message': 'welcome to bff home'}


@router.get('/error', tags=['index'])
def home():
    """
    index
    """
    raise CustomErr()
