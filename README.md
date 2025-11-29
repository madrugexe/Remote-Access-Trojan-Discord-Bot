# 🤖 RAT Bot - Remote Administration Tool

> ⚠️ **AVERTISSEMENT LEGAL**  
> Ce logiciel est fourni à des fins éducatives et de test de pénétration uniquement.  
> L'utilisation de ce tool sans autorisation explicite est illégale.

## 📋 Description

Un bot Discord permettant l'administration à distance d'un système via des commandes dédiées. Développé en Python avec l'API Discord.

## 🛠️ Fonctionnalités

### 🔍 Informations Système
- Récupération des informations hardware/software
- Informations réseau et utilisateur
- Statistiques système en temps réel

### 📁 Gestion des Fichiers
- Navigation dans l'arborescence
- Upload/Download de fichiers
- Exécution de commandes système

### 🎥 Surveillance
- Capture d'écran
- Enregistrement audio
- Logging des touches (keylogger)
- Contrôle clavier/souris à distance

### 🌐 Contrôle Réseau
- Ouverture de sites web
- Téléchargement de fichiers
- Analyse des connexions

## 📥 Installation

### Prérequis
- Python 3.8+
- Compte Discord Developer
- Bot Discord avec token

### 1. Configuration du Bot Discord

```python
# Dans votre script, remplacez le token:
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
bot.run('VOTRE_TOKEN_ICI')

