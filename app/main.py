from fastapi import FastAPI


from app.routers.users import usr_router
from app.routers.login import login_router

app = FastAPI()

app.include_router(usr_router, prefix="/user")
app.include_router(login_router, prefix="/login")


