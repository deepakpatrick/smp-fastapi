######### Approach 4 - Using ORM with SQLAlchemy (No explicit SQL queries) ##############

from fastapi import FastAPI

from . import models # from current location get the models.py file loaded. This defines DB tables
from .routers import posts, users, auth, votes
from .database import engine

from fastapi.middleware.cors import CORSMiddleware

# Mandatory SQLAlchemy setting
# models.Base.metadata.create_all(bind=engine)

# create FastAPI object
app = FastAPI()

# origins = ["https://www.google.com"] # list of domains from where you can reach our api
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)


# Home page or Root
@app.get("/")
async def root():
    return {"message":"SMP Fastapi comprehensive - now syncs with docker container - using bind service"}

     
     

