from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.links import router as link_router

app = FastAPI()
app.include_router(link_router)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

