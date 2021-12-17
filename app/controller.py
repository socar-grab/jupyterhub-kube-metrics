import os

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form, BackgroundTasks
from fastapi import Request

from .client import get_client
from .config.settings import KubeConfig, JupyterConfig
from .core.kubernetes.kubernetes_client import KubeMetricsClient
from .models import AuthorizationError, CullRequest
from .models import HubApiError
from .models import User
from .security import get_current_user

# APIRouter prefix cannot end in /
from .service import CullingService

router = APIRouter(prefix="/test")


@router.post("/cull")
async def cull(body: CullRequest, background_tasks: BackgroundTasks):
    service = CullingService(
        api_client=KubeMetricsClient(KubeConfig()), config=JupyterConfig()
    )
    return service.cull(allowable_idle_minutes=body.allowable_idle_minutes)
