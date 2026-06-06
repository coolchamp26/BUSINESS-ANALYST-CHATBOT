@echo off
title FlowArchitect AI - Startup Utility
echo ==========================================
echo Starting FlowArchitect AI Web Application
echo ==========================================

:: Activate python venv and start backend server
echo Starting Backend FastAPI Server on http://127.0.0.1:8000...
start cmd /k "cd backend && .venv\Scripts\activate && uvicorn main:app --reload --host 127.0.0.1 --port 8000"

:: Start frontend Vite dev server
echo Starting Frontend React/Vite Developer Server...
start cmd /k "cd frontend && npm run dev -- --host 127.0.0.1"

echo ==========================================
echo Startup completed! Open http://127.0.0.1:5173/ in your browser.
echo ==========================================
pause
