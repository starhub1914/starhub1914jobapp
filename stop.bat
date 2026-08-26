@echo off
echo Stopping Software Development Document Environment / My Job App Services...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM java.exe 2>nul
echo Services stopped cleanly.
