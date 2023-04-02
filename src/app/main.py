# python imports
from typing import List

# fastapi  imports
from fastapi import Depends, FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

# application imports
from src.auth.memb_router import memb_router, fellowship_router

# fastapi initialization
app = FastAPI()


# CORS Middleware
origins: List = []


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routers from the application
app.include_router(memb_router)
app.include_router(fellowship_router)


# root of the server
@app.get("/", status_code=status.HTTP_200_OK)
def root() -> dict:
    return {"message": "Welcome to inventory", "docs": "/docs"}
