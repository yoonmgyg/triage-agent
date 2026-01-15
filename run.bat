@echo off
if "%ROLE%"=="white" (
    .\venv313\Scripts\python.exe greenagent\main_white.py < nul
) else (
    .\venv313\Scripts\python.exe greenagent\main.py < nul
)
