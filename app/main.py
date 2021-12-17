import os

from fastapi import FastAPI, __version__

from app.controller import router

app = FastAPI(
    title="Jupyterhub kube monitoring service",
    version=__version__,
    ### Add our service client id to the /docs Authorize form automatically
    swagger_ui_init_oauth={"clientId": os.environ["JUPYTERHUB_CLIENT_ID"]},
    ### Default /docs/oauth2 redirect will cause Hub
    ### to raise oauth2 redirect uri mismatch errors
    swagger_ui_oauth2_redirect_url=os.environ["JUPYTERHUB_OAUTH_CALLBACK_URL"],
)

app.include_router(router)
