from fastapi import FastAPI

from app.api.versions.v1 import app_v1


app = FastAPI()

app.mount(path='/v1', app=app_v1)
