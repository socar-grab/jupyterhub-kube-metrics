from datetime import datetime
from typing import Dict, List

from pydantic.main import BaseModel


class PodMetadata(BaseModel):
    name: str
    namespace: str
    created_at: datetime


class ContainerUsage(BaseModel):
    cpu: str
    memory: str


class ContainerMetrics(BaseModel):
    name: str
    usage: ContainerUsage


class PodMetrics(BaseModel):
    metadata: PodMetadata
    containers: List[ContainerMetrics]
