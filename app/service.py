import abc
import logging
from typing import Optional

from app.config.settings import BaseConfig, JupyterConfig
from app.core.kubernetes.kubernetes_client import KubeMetricsClient

logger = logging.getLogger(__name__)


class CullingService:
    def __init__(self, api_client: KubeMetricsClient, config: JupyterConfig):
        self.api_client = api_client
        self.config = config

    def cull(self, allowable_idle_minutes: int, pod_name: Optional[str] = None):
        result = self.api_client.get_pod_metrics(name=pod_name)
        # Validation...
        return result
