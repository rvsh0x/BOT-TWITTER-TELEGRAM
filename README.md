# Bot de Publication Multi-Plateforme

Un bot automatisé qui publie sur Twitter et Telegram.

## Description du Projet

Système de publication automatisé qui diffuse des textes sur Twitter et Telegram. Le bot utilise un système de rotation intelligent pour éviter les répétitions et respecter les limites de publication de chaque plateforme.

### Fonctionnalités Principales

- **Publication automatique** sur Twitter et Telegram
- **Système de rotation** des contenus pour éviter les répétitions
- **Gestion des limites quotidiennes** (50 publications max/jour)
- **Buffer intelligent** pour éviter de republier les mêmes contenus
- **Compteur de publications** avec suivi quotidien
- **Logs détaillés** pour le monitoring
- **Vérification de longueur** des tweets (limite 280 caractères)

## Architecture du Projet

```
bot_project/
├── bot_twitter.py          # Bot Twitter principal
├── bot_telegram.py         # Bot Telegram principal
├── Check.py               # Utilitaire de vérification des longueurs
├── run_bot.sh             # Script de lancement automatisé
├── publications.json      # Base de données des contenus
├── publication_counter.json # Compteur de publications quotidiennes
├── id_buffer.pkl          # Buffer des IDs utilisés
├── run_bot.log           # Fichier de logs
├── requirements.txt      # Dépendances Python
└── venv/                # Environnement virtuel
```

## Installation

### Prérequis

- Python 3.12+
- Compte développeur Twitter avec API v2
- Bot Telegram créé via @BotFather

### Étapes d'installation

1. **Cloner le projet**
   ```bash
   git clone <url-du-repo>
   cd bot_project
   ```

2. **Créer l'environnement virtuel**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Sur Linux/Mac
   # ou
   venv\Scripts\activate     # Sur Windows
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuration des variables d'environnement**
   
   Modifier le fichier `run_bot.sh` avec vos tokens :
   ```bash
   export BOT_TWITTER_BEARER_TOKEN="votre_bearer_token"
   export BOT_TWITTER_CONSUMER_KEY="votre_consumer_key"
   export BOT_TWITTER_CONSUMER_SECRET="votre_consumer_secret"
   export BOT_TWITTER_ACCESS_TOKEN="votre_access_token"
   export BOT_TWITTER_ACCESS_SECRET="votre_access_secret"
   export TELEGRAM_BOT_TOKEN="votre_telegram_bot_token"
   export TELEGRAM_CHAT_ID="votre_chat_id"
   ```

## Utilisation

### Lancement manuel

```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Lancer les bots
python3 bot_twitter.py
python3 bot_telegram.py
```

### Lancement automatisé

```bash
# Rendre le script exécutable
chmod +x run_bot.sh

# Lancer le script
./run_bot.sh
```

### Programmation avec cron

Pour automatiser les publications, ajoutez à votre crontab :

```bash
# Publication toutes les 6 heures
0 */6 * * * /chemin/vers/fadhail_project/run_bot.sh

# Publication quotidienne à 9h
0 9 * * * /chemin/vers/fadhail_project/run_bot.sh
```

## Structure des Fichiers

### `publications.json`
Base de données contenant tous les textes à publier :
```json
[
  {
    "id": 1,
    "parts": ["Texte à publier..."],
    "source": "Source du contenu"
  }
]
```

### `publication_counter.json`
Compteur quotidien des publications :
```json
{
  "date": "2025-01-13",
  "count": 5
}
```

### `id_buffer.pkl`
Fichier binaire contenant la liste des IDs déjà utilisés pour éviter les répétitions.

## 🔧 Configuration

### Limites de Publication
- **Twitter** : 50 publications maximum par jour (configurable). Limite définie par l'API Twitter. 
- **Telegram** : 50 publications maximum par jour (configurable).

### Personnalisation des Contenus
1. Modifier `publications.json` pour ajouter/supprimer des textes
2. Utiliser `Check.py` pour vérifier la longueur des tweets
3. Le bot sélectionnera automatiquement le prochain contenu

## Monitoring

### Logs
Les logs sont sauvegardés dans `run_bot.log` :
```
=== Lancement du script : lun. 13 jan. 2025 09:15:23 UTC ===
Publication du tweet ID : 1 (1 parties)
Publication de l'ID : 1
```

### Vérification des Longueurs
```bash
python3 Check.py
```
Cet utilitaire vérifie que tous les tweets respectent la limite de 280 caractères.

## Développement

### Ajout de Nouvelles Fonctionnalités
1. Modifier les scripts Python selon vos besoins
2. Ajouter de nouveaux contenus dans `publications.json`
3. Tester avec `Check.py` avant déploiement

### Débogage
- Consulter `run_bot.log` pour les erreurs
- Vérifier les variables d'environnement
- S'assurer que les tokens sont valides

## Dépendances

- **tweepy** : API Twitter
- **telegram** : API Telegram Bot
- **numpy** : Calculs numériques
- **json** : Gestion des données JSON
- **pickle** : Sérialisation des données

## Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit vos changements (`git commit -am 'Ajout nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créer une Pull Request

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## Support

Pour toute question ou problème :
1. Consulter les logs dans `run_bot.log`
2. Vérifier la configuration des tokens
3. Créer une issue sur le repository

---

**Note** : Assurez-vous de respecter les conditions d'utilisation de Twitter et Telegram lors de l'utilisation de ce bot.
