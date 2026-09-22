@echo off
setlocal
cd /d "%~dp0"

:: Kensova ERP - one-time Windows setup.
:: Ask AI Gemini API key is bundled in api.txt and configured automatically
:: for this Windows user during setup.

:: Load the bundled API key.
if exist "api.txt" set /p "GEMINI_API_KEY=" < "api.txt"
if defined GEMINI_API_KEY setx GEMINI_API_KEY "%GEMINI_API_KEY%" >nul

echo.
echo ========================================
echo   KENSOVA ERP - FIRST TIME SETUP
echo ========================================
echo.

echo Creating virtual environment...
if not exist "venv\Scripts\python.exe" (
    python -m venv venv
    if errorlevel 1 (
        echo.
        echo ERROR: Python could not create the virtual environment.
        echo Install Python 3.11+ and try again.
        pause
        exit /b 1
    )
)

call "venv\Scripts\activate.bat"
if errorlevel 1 (
    echo ERROR: Could not activate the virtual environment.
    pause
    exit /b 1
)

echo Installing requirements (Django, pandas, openpyxl, waitress)...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR: Dependency installation failed.
    pause
    exit /b 1
)

echo.
if defined GEMINI_API_KEY (
    echo Ask AI Gemini API key configured automatically.
) else (
    echo WARNING: api.txt was not found. Ask AI will require GEMINI_API_KEY to be configured manually.
)

echo.
echo Setup complete. You can now start the ERP with START_kensova_ERP.vbs.
echo.
pause
