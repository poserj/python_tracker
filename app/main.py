from fastapi import FastAPI

from .routers.healthcheck import router as root_router


app = FastAPI()
app.include_router(root_router)

