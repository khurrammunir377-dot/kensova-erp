@echo off
title Stop Kensova ERP Server
echo Stopping Kensova ERP server on port 8009...
set "FOUND_PID="
for /f "tokens=5" %%P in ('netstat -ano ^| findstr ":8009" ^| findstr "LISTENING"') do (
    set "FOUND_PID=%%P"
    taskkill /PID %%P /F >nul 2>&1
)
if defined FOUND_PID (
    echo Server stopped successfully.
) else (
    echo Kensova ERP server is not currently running on port 8009.
)
timeout /t 3 >nul
