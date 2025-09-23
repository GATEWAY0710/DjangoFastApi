from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from api.controllers.user_controller import router as user_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


app.include_router(user_router, prefix="/users", tags=["Users"])