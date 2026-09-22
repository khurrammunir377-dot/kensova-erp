@echo off
setlocal
cd /d "%~dp0"

:: Ask AI reads GEMINI_API_KEY from the Windows user environment when configured.

:: --- Close any previous instance of this app already running on port 8009 ---
for /f "tokens=5" %%p in ('netstat -ano ^| findstr ":8009" ^| findstr "LISTENING"') do (
    taskkill /F /PID %%p >nul 2>&1
)

:: --- Start the server (binds to 0.0.0.0 so it keeps working even if the PC's IP changes) ---
if exist "venv\Scripts\activate.bat" (
    call "venv\Scripts\activate.bat"
) else (
    echo venv not found - run setup_venv.bat once before first use.
    exit /b 1
)

:: Applies any pending database migrations. Safe/no-op if there are none.
python manage.py migrate --noinput >nul 2>&1

:: Gathers CSS/JS/fonts (including the vendor/ offline libraries) into
:: staticfiles\ so they can be served with DEBUG off. Safe to run every time.
python manage.py collectstatic --noinput >nul 2>&1

:: waitress is a real production-grade WSGI server (unlike manage.py
:: runserver, which Django explicitly says not to use continuously).
python serve_waitress.py
