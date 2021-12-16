import json
from typing import Optional
from kubernetes import client, config
from kubernetes.client import ApiClient
from app.core import KubernetesClient
from app.core.models import PodMetrics, PodMetadata


class KMonitorClient(KubernetesClient):
    def __init__(self):
        config.load_kube_config()
        self._api_client = ApiClient()

    def get_pod_metrics(self, namespace: str, name: Optional[str] = None):
        response = self._api_client.call_api(
            f"/apis/metrics.k8s.io/v1beta1/namespaces/{namespace}/pods{f'/{name}'if name else ''}",
            "GET",
            auth_settings=["BearerToken"],
            response_type="json",
            _preload_content=False,
        )
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


if __name__ == "__main__":
    client = KMonitorClient()
    client.get_pod_metrics(namespace="airflow-feature-datahub")
