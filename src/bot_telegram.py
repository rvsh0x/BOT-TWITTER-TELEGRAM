import os
import json
import pickle
import random
from datetime import datetime
import asyncio
from telegram import Bot

# --- CONSTANTES / CONFIG ---
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = int(os.getenv("TELEGRAM_CHAT_ID"))  # Attention : doit être un int
BUFFER_FILE = "id_buffer.pkl"
COUNTER_FILE = "publication_counter.json"
PUBLICATION_DAILY_LIMIT = 50

# Charger toutes les publications depuis fichier JSON
with open("publications.json", "r", encoding="utf-8") as f:
    all_publications = json.load(f)

total_ids = list(range(1, len(all_publications) + 1))

async def main():
    # --- Gestion du buffer pour ne pas republier les mêmes messages trop vite ---
    if os.path.exists(BUFFER_FILE):
        with open(BUFFER_FILE, "rb") as f:
            used_ids = pickle.load(f)
    else:
        used_ids = []

    if len(used_ids) >= len(total_ids):
        used_ids = []

    available_ids = list(set(total_ids) - set(used_ids))
    publication_id = random.choice(available_ids)
    used_ids.append(publication_id)

    with open(BUFFER_FILE, "wb") as f:
        pickle.dump(used_ids, f)

    # --- Récupérer la publication correspondante ---
    publication_data = next(p for p in all_publications if p["id"] == publication_id)
    parts = publication_data["parts"]
    source = publication_data.get("source")

    # --- Gestion compteur publication ---
    def load_publication_counter():
        today = datetime.now().strftime("%Y-%m-%d")
        if not os.path.exists(COUNTER_FILE):
            return {"date": today, "count": 0}
        with open(COUNTER_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if data["date"] != today:
            return {"date": today, "count": 0}
        return data

    def save_publication_counter(data):
        with open(COUNTER_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def check_can_post(number_to_post):
        counter = load_publication_counter()
        if counter["count"] + number_to_post > PUBLICATION_DAILY_LIMIT:
            print(f"⛔ Limite atteinte ({counter['count']}/{PUBLICATION_DAILY_LIMIT} messages aujourd'hui).")
            return False
        return True

    def update_publication_count(number_posted):
        counter = load_publication_counter()
        counter["count"] += number_posted
        save_publication_counter(counter)

    # --- Initialisation du bot Telegram ---
    bot = Bot(token=TOKEN)

    # --- Préparation du message ---
    message_text = "\n\n".join(parts)  # Concatène toutes les parties
    if source and source.strip():
        message_text += f"\n\n{source}"
    # --- Envoi du message ---
    if check_can_post(1):
        print(f"Publication de l'ID : {publication_id}")
        try:
            await bot.send_message(chat_id=CHAT_ID, text=message_text)
            update_publication_count(1)
        except Exception as e:
            print(f"Erreur lors de l'envoi: {e}")
    else:
        print("Limite de messages atteinte, pas d'envoi.")

if __name__ == "__main__":
    asyncio.run(main())
