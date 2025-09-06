import json


#CE PROGRAMME SERT A VERIFIER SI VOS PUBLICATIONS SONT PLUS LONGUES QUE 280 CARACTERES

# Charger les tweets depuis le fichier JSON
with open("publications.json", "r", encoding="utf-8") as f:
    tweets = json.load(f)

# Seuil de longueur à vérifier (280 caractères)
max_len = 280

for tweet in tweets:
    tweet_id = tweet["id"]
    parts = tweet["parts"]
    
    long_parts = [len(p) for p in parts if len(p) > max_len]

    if long_parts:
        print(f"Tweet ID {tweet_id} :")
        print(f"  Longueurs excessives : {long_parts}")
        for i, p in enumerate(parts):
            if len(p) > max_len:
                print(f"  ➤ Part {i+1} ({len(p)} chars): {p}\n")

print("\n✅ Vérification terminée.")
