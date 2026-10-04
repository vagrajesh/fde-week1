from importlib import import_module
from fastapi import FastAPI, APIRouter

post_employees_router = import_module("fast_api.03_fastapi_postemployees").router
get_employees_router = import_module("fast_api.02_fastapi_getemployees").router

app = FastAPI()
app.include_router(post_employees_router)
app.include_router(get_employees_router)