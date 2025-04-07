from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
from typing import List
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

ALLOWED_ORIGINS = os.environ.get(
    "ALLOWED_ORIGINS", 
    "http://localhost:3000"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

temp_db = []

class Player(BaseModel):
    name: str
    description: str


@app.get("/")
async def get_projects():
    """ tesdt """
    return None


@app.post("/addPlayer")
async def add_player(player: Player):
    """ add a player """
    player_dict = player.dict()
    temp_db.append(player_dict)
    print(f"{temp_db}") 
    return player

@app.get("/players")
async def get_Players():
    """ get all players from db """
    return temp_db

@app.get("/player/{player_name}", response_model=Player)
async def get_player(player_name: str):
    """ get data for player """
    print(player_name)
    for p in temp_db:
        if p["name"] == player_name:
            return p
    return None

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)