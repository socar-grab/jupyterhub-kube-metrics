from pydantic.env_settings import BaseSettings
from pydantic.fields import Field


class BaseConfig(BaseSettings):
    class Config:
        env_file = ".env"


class KubeConfig(BaseConfig):
    pod_namespace: str = Field(..., env="POD_NAMESPACE")
    pod_name: str = Field(..., env="POD_NAME")


class JupyterConfig(BaseConfig):
    JUPYTERHUB_API_URI: str = Field(..., env="JUPYTERHUB_API_URI")
