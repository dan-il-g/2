from fastapi import FastAPI
from view import router

# End Setup
app = FastAPI()
app.include_router(router)