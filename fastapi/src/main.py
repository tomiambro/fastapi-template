from routes import public, users, utilities
from settings import logger_for

from fastapi import FastAPI

logger = logger_for(__name__)

app = FastAPI()
app.include_router(public.router)
app.include_router(utilities.router)
app.include_router(users.router)


@app.get("/")
def read_root():
    return {"200": "OK"}
