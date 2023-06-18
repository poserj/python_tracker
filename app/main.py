from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "python_tracker app", "title": "python_tracker"}
