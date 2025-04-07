from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
import asyncio
from twikit import Client
from transformers import pipeline
from collections import Counter
 
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

@app.on_event("startup")
async def startup_event():
    USERNAME = 'okayburna'
    EMAIL = 'ccurrycollegemail@gmail.com'
    PASSWORD = 'Stephcurry101?'

    logger.info("Logging into Twitter...")
    await client.login(
        auth_info_1=USERNAME,
        auth_info_2=EMAIL,
        password=PASSWORD,
        cookies_file='cookies.json'
    )
    logger.info("Logged in successfully.")

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
    return {'label': max(set(labels), key=labels.count), 'confidence': score}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
    logout()