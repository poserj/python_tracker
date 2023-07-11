from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

#from .routers.docs_page import doc_router as doc_router
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles
from app.helpers import init_app
from .routers.healthcheck import router as router

conf = init_app()
app = FastAPI(docs_url=None, redoc_url=None, root_path=conf['ROOT_PATH'])
app.include_router(router)
#app.include_router(doc_router)

app.mount("/static", StaticFiles(directory="static"), name="static")



@app.get(f"{conf['ROOT_PATH']}/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get(f"{conf['ROOT_PATH']}/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )

