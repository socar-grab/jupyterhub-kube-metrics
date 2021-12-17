import json
import logging
from typing import Optional
from kubernetes import client, config
from kubernetes.client import ApiClient

from app.config.settings import KubeConfig
from app.core.kubernetes import KubernetesClient
from app.core.kubernetes.models import PodMetrics, PodMetadata


class KubeMetricsClient(KubernetesClient):
    def __init__(self, _config: KubeConfig):
        config.load_kube_config()
        self._api_client = ApiClient()
        self.logger = logging.getLogger(__name__)
        self.config = _config

    def _get_pod_metrics(self):
        v = client.V2beta1ResourceMetricSource()

    def get_pod_metrics(
        self, namespace: Optional[str] = None, name: Optional[str] = None
    ):
        try:
            namespace = namespace or self.config.pod_namespace
            response = self._api_client.call_api(
                f"/apis/metrics.k8s.io/v1beta1/namespaces/{namespace}/pods{f'/{name}'if name else ''}",
                "GET",
                auth_settings=["BearerToken"],
                response_type="json",
                _preload_content=False,
            )
            # [0]: http response, [1]: statusCode, [2]: http header
            if response[1] >= 400:
                raise Exception(f"status {response[1]} error occured")
        except Exception as e:
            self.logger.error("API Error Occurred : ", e)
            raise e

        raw_result = response[0].data.decode("utf8")
        pod_metrics = []

        for pod_info in json.loads(raw_result)["items"]:
            pod_metrics.append(
                PodMetrics(
                    metadata=PodMetadata(
                        **pod_info["metadata"],
                        created_at=pod_info["metadata"]["creationTimestamp"],
                    ),
                    containers=pod_info["containers"],
                )
            )
        return pod_metrics
