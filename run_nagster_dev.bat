@echo off
echo Starting Nagster dev environment...

REM ==== BACKEND ====
cd /d C:\Users\ACER\Nagster\backend
start "Nagster Backend" py -m uvicorn main:app --reload

REM ==== FRONTEND ====
cd /d C:\Users\ACER\Nagster\frontend
start "Nagster Frontend" npm run dev

REM ==== AGENT ====
cd /d C:\Users\ACER\Nagster
start "Nagster Agent" py agent.py

echo All services started. You can close this window.
