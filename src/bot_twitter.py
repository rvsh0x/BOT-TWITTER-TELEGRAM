import random
import fileinput
import tweepy
import json
import os
import pickle
import numpy as np
from datetime import datetime


# === AUTHENTIFICATION TWITTER ===

bearer_token = os.getenv("BOT_TWITTER_BEARER_TOKEN")
consumer_key = os.getenv("BOT_TWITTER_CONSUMER_KEY")
consumer_secret = os.getenv("BOT_TWITTER_CONSUMER_SECRET")
access_token = os.getenv("BOT_TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("BOT_TWITTER_ACCESS_SECRET")

client = tweepy.Client(bearer_token=bearer_token)


client = tweepy.Client(
    consumer_key=consumer_key, consumer_secret=consumer_secret,
    access_token=access_token, access_token_secret=access_token_secret
)

# === CHARGEMENT DES DONNÉES JSON ===
with open("publications.json", "r", encoding="utf-8") as f:
    all_tweets = json.load(f)

# === CHARGEMENT DU BUFFER PICKLE ===

buffer_file = "id_buffer.pkl"
total_ids = list(range(1, len(all_tweets) + 1))

if os.path.exists(buffer_file):
    with open(buffer_file, "rb") as f:
        used_ids = pickle.load(f)
else:
    used_ids = []

# Si tous les tweets ont été utilisés, on réinitialise
if len(used_ids) >= len(total_ids):
    used_ids = []

# Choisir un tweet non utilisé
available_ids = list(set(total_ids) - set(used_ids))
tweet_id = random.choice(available_ids)
used_ids.append(tweet_id)

# Sauvegarder le buffer
with open(buffer_file, "wb") as f:
    pickle.dump(used_ids, f)

# === RÉCUPÉRER LE TWEET CORRESPONDANT ===
tweet_data = next(t for t in all_tweets if t["id"] == tweet_id)
parts = tweet_data["parts"]
source = tweet_data["source"]

# === CONFIGURATION ===
COUNTER_FILE = "publications_counter.json"
TWEET_DAILY_LIMIT = 50

# Charger ou initialiser le compteur
def load_tweet_counter():
    today = datetime.now().strftime("%Y-%m-%d")
    if not os.path.exists(COUNTER_FILE):
        return {"date": today, "count": 0}
    
    with open(COUNTER_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    if data["date"] != today:
        return {"date": today, "count": 0}
    return data

# Sauvegarder le compteur mis à jour
def save_tweet_counter(data):
    with open(COUNTER_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# Vérifier la limite avant de publier
def check_can_post(number_to_post):
    counter = load_tweet_counter()
    if counter["count"] + number_to_post > TWEET_DAILY_LIMIT:
        print(f"⛔ Limite atteinte ({counter['count']}/{TWEET_DAILY_LIMIT} tweets aujourd'hui).")
        return False
    return True

# Mettre à jour le compteur après publication
def update_tweet_count(number_posted):
    counter = load_tweet_counter()
    counter["count"] += number_posted
    save_tweet_counter(counter)

# === PUBLICATION THREAD ===

if check_can_post(len(parts) + 1):

    print(f"Publication du tweet ID : {tweet_id} ({len(parts)} parties)")

    tweet_ids = []
    response = None

    for index, part in enumerate(parts):
        if index == 0:
            response = client.create_tweet(text=part)
        else:
            response = client.create_tweet(
                text=part,
                in_reply_to_tweet_id=tweet_ids[-1]
            )
        tweet_ids.append(response.data["id"])

    # === AJOUTER LA SOURCE SI DISPONIBLE ===
    if source and len(source.strip()) > 0:
        client.create_tweet(
            text=source,
            in_reply_to_tweet_id=tweet_ids[-1]
        )

    update_tweet_count(len(parts) +1)
