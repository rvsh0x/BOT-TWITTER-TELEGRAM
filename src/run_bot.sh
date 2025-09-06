#!/bin/bash
# Active l'environnement virtuel
source /home/rvsh0x/fadhail_project/venv/bin/activate

#exporte les token
export BOT_TWITTER_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAAOkDtAEAAAAAyvx4rui2oxSkK2Qcurpz5e1Uk8k%3DxmbHDTNEqsnT4eD29naZttZ6l9T1g0ii1G77VgPF0mnH6wr6Rk
export BOT_TWITTER_CONSUMER_KEY=xsDwqX253GlFbNuGye5Sl1vj0
export BOT_TWITTER_CONSUMER_SECRET=ITQguDyi7O3kwMLy35sIhXbUJRqgi1t2ElaqHlWYjn2H3yxN2n
export BOT_TWITTER_ACCESS_TOKEN=1771189813158334464-KHvr3VgWa0a15z6CobThUhJ6ROeOH6
export BOT_TWITTER_ACCESS_SECRET=cwBzGsbLDUc8rZwn6htCKLPS0tRhs6UfjY1JUbBj5DpMl
export TELEGRAM_BOT_TOKEN=8264989674:AAGoY0ubdX986nXRSBJcB3N-MRhLCmf0voU
export TELEGRAM_CHAT_ID=-1001908854217

# Chemin vers le fichier log
LOGFILE="/home/rvsh0x/fadhail_project/run_bot.log"

# Date et heure du lancement
echo "=== Lancement du script : $(date) ===" >> "$LOGFILE"

# Lance le script Python
python3 /home/rvsh0x/fadhail_project/bot_twitter.py >> "$LOGFILE" 2>&1
python3 /home/rvsh0x/fadhail_project/bot_telegram.py >> "$LOGFILE" 2>&1

# Désactive l'environnement virtuel (optionnel)
deactivate

# Séparateur pour plus de lisibilité dans le log
echo -e "\n" >> "$LOGFILE"
