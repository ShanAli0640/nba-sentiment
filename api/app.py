from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
import asyncio
from twikit import Client
from transformers import pipeline
from collections import Counter
from dotenv import load_dotenv
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from typing import List
from pydantic import BaseModel

load_dotenv()


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

# Initialize client
client = Client('en-US')

# Path to the service account key JSON file
cred = credentials.Certificate("../firebase_sa_key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

@app.on_event("startup")
async def startup_event():
    logger.info("Logging into Twitter...")
    await client.login(
        auth_info_1=os.getenv('USERNAME'),
        auth_info_2=os.getenv('EMAIL'),
        password=os.getenv('PASSWORD'),
        cookies_file='cookies.json'
    )
    logger.info("Logged in successfully.")

    
temp_db = []

class Player(BaseModel):
    name: str
    description: str

@app.get("/")
async def get_projects():
    """ tesdt """
    return None

@app.get("/scores/{player}")
async def get_player_scores(player: str):
    tweets = await client.search_tweet(query=player, count=5, product='Latest')

    tweet_text_list = []

    for tweet in tweets:
        print(
            tweet.user.name,
            tweet.text,
            tweet.created_at
        )
        tweet_text_list.append(tweet.text)
        
    # Downloading the sentiment analysis model
    SentimentClassifier = pipeline("sentiment-analysis")

    # Calling the sentiment analysis function for 3 sentences
    sentiments_list = SentimentClassifier(tweet_text_list)

    score = sum([x['score'] for x in sentiments_list]) / len(sentiments_list)
    labels = [x['label'] for x in sentiments_list]
    final_label = max(set(labels), key=labels.count)

    doc_ref = db.collection("player_scores").document(player + '_' + datetime.utcnow().isoformat())
    doc_ref.set({
        "player": player,
        "label": final_label,
        "confidence": score,
        "timestamp": datetime.utcnow().isoformat()
    })

    return {'label': final_label, 'confidence': score}

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
    logout()