from fastapi import FastAPI

from .routers.healthcheck import router as router


app = FastAPI()
app.include_router(router)

