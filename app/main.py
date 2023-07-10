from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routers.docs_page import doc_router as doc_router
from .routers.healthcheck import router as router

app = FastAPI(docs_url=None, redoc_url=None)
app.include_router(router)
app.include_router(doc_router)
