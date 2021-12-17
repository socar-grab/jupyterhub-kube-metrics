import os
from fastapi import FastAPI, __version__

from app.controller import router

app = FastAPI(
    title="Jupyterhub kube monitoring service",
    version=__version__,
)

app.include_router(router)
