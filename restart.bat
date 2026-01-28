@echo off
chcp 65001 >nul

echo Restarting bot...

:: Kill existing node processes running index.js
echo Stopping existing processes...
taskkill /f /im node.exe >nul 2>&1

:: Short pause
timeout /t 1 /nobreak >nul

:: Start bot in this window
echo Starting bot...
echo ========================================
cd /d "%~dp0"
npm start
