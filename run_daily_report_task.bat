@echo off
setlocal
cd /d "%~dp0"
if not exist "venv\Scripts\python.exe" exit /b 1
"%~dp0venv\Scripts\python.exe" manage.py send_daily_report >> "%~dp0daily_report.log" 2>&1
