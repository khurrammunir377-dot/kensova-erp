@echo off
setlocal
cd /d "%~dp0"

:: Kensova ERP - Daily Management Report at 7:00 PM Dubai time.
:: The task runs in the current Windows user's interactive session so
:: Outlook Desktop can use the logged-in Outlook profile.
if not exist "venv\Scripts\python.exe" (
    echo Kensova ERP virtual environment not found.
    echo Run setup_venv.bat first.
    exit /b 1
)

set "PYTHON=%~dp0venv\Scripts\python.exe"
set "TASKNAME=Kensova ERP - Daily Stores Report - 7PM"
set "SCRIPT=%~dp0run_daily_report_task.bat"

schtasks /Delete /TN "%TASKNAME%" /F >nul 2>&1
schtasks /Create /TN "%TASKNAME%" /TR "\"%SCRIPT%\"" /SC DAILY /ST 19:00 /F /RL LIMITED /IT
if errorlevel 1 (
    echo Failed to create scheduled task.
    pause
    exit /b 1
)

echo.
echo Daily report task installed successfully for 7:00 PM every day.
echo It uses the Windows user's logged-in Outlook Desktop account.
pause
