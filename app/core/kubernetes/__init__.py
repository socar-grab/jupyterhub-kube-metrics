import abc
from abc import ABC
from typing import Optional


class KubernetesClient(ABC):
    @abc.abstractmethod
    def get_pod_metrics(self, namespace: str, name: Optional[str] = None):
        pass
