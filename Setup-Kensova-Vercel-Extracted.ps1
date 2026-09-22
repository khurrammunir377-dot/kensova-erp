# Setup-Kensova-Vercel.ps1
# Run this script FROM the extracted Kensova ERP folder containing manage.py.
# Example:
# PS C:\Users\DELL\OneDrive\Desktop\Kensova_ERP-Vercel> Set-ExecutionPolicy -Scope Process Bypass
# PS C:\Users\DELL\OneDrive\Desktop\Kensova_ERP-Vercel> .\Setup-Kensova-Vercel.ps1

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " KENSOVA ERP - VERCEL PREPARATION" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Always work from the folder where this script is located.
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot

Write-Host "Project folder:" -ForegroundColor Yellow
Write-Host "  $ProjectRoot"
Write-Host ""

# -------------------------------------------------------------------
# 1. Verify this is the extracted Django project
# -------------------------------------------------------------------
if (-not (Test-Path (Join-Path $ProjectRoot "manage.py"))) {
    throw "manage.py was not found in $ProjectRoot. Put this script in the same folder as manage.py."
}

Write-Host "[1/8] Django project detected." -ForegroundColor Green

# -------------------------------------------------------------------
# 2. Create a safety backup of the current database
# -------------------------------------------------------------------
$BackupRoot = Join-Path $ProjectRoot "_local_backup"
$DbBackup = Join-Path $BackupRoot "db.sqlite3"

New-Item -ItemType Directory -Force -Path $BackupRoot | Out-Null

if (Test-Path (Join-Path $ProjectRoot "db.sqlite3")) {
    Copy-Item (Join-Path $ProjectRoot "db.sqlite3") $DbBackup -Force
    Write-Host "[2/8] SQLite database backed up to:" -ForegroundColor Green
    Write-Host "      $DbBackup"
} else {
    Write-Host "[2/8] No db.sqlite3 found. Continuing." -ForegroundColor Yellow
}

# -------------------------------------------------------------------
# 3. Create a Windows/local requirements file preserving Outlook use
# -------------------------------------------------------------------
$Requirements = Join-Path $ProjectRoot "requirements.txt"
$WindowsRequirements = Join-Path $ProjectRoot "requirements-windows.txt"

if (Test-Path $Requirements) {
    $reqText = Get-Content $Requirements -Raw

    # Create a Windows requirements file from the current requirements.
    if ($reqText -notmatch '(?im)^\s*pywin32') {
        Add-Content $WindowsRequirements "`r`npywin32>=306"
    } else {
        Copy-Item $Requirements $WindowsRequirements -Force
    }

    # Remove pywin32 from the production requirements.
    $prodReq = $reqText -split "`r?`n" |
        Where-Object { $_ -notmatch '^\s*pywin32\s*' }

    Set-Content -Path $Requirements -Value ($prodReq -join "`r`n") -Encoding UTF8

    Write-Host "[3/8] requirements.txt prepared for Vercel; requirements-windows.txt preserves Outlook support." -ForegroundColor Green
}

# -------------------------------------------------------------------
# 4. Create .gitignore
# -------------------------------------------------------------------
$GitIgnore = @'
# Python
__pycache__/
*.py[cod]
*$py.class
*.pyo

# Django
*.log
staticfiles/
media/
.DS_Store

# Local database - NEVER commit live ERP data
db.sqlite3
*.sqlite3
_local_backup/

# Local secrets
.env
.env.*
!.env.example
.secret_key

# Virtual environments
.venv/
venv/
env/
ENV/

# IDE
.vscode/
.idea/

# Windows
Thumbs.db
Desktop.ini

# Local deployment/backups
deployment-backup/
*.bak

# Vercel local files
.vercel/
'@

Set-Content -Path (Join-Path $ProjectRoot ".gitignore") -Value $GitIgnore -Encoding UTF8
Write-Host "[4/8] .gitignore created." -ForegroundColor Green

# -------------------------------------------------------------------
# 5. Create .env.example
# -------------------------------------------------------------------
$EnvExample = @'
# Django production settings
DJANGO_SECRET_KEY=CHANGE_THIS_TO_A_LONG_RANDOM_SECRET
DEBUG=False
ALLOWED_HOSTS=your-project.vercel.app
CSRF_TRUSTED_ORIGINS=https://your-project.vercel.app

# PostgreSQL
# Set this on Vercel after creating your PostgreSQL database.
DATABASE_URL=postgresql://USER:PASSWORD@HOST/DATABASE?sslmode=require

# Email will be configured later.
'@

Set-Content -Path (Join-Path $ProjectRoot ".env.example") -Value $EnvExample -Encoding UTF8
Write-Host "[5/8] .env.example created." -ForegroundColor Green

# -------------------------------------------------------------------
# 6. Create a Vercel deployment notes file
# -------------------------------------------------------------------
$Notes = @'
KENSOVA ERP - VERCEL DEPLOYMENT NOTES
=====================================

This folder is the Vercel deployment copy of the extracted Kensova ERP.

IMPORTANT:
- The original local SQLite database is backed up in _local_backup\db.sqlite3
- db.sqlite3 is intentionally excluded from Git.
- Local Windows ERP can continue using SQLite.
- Online Vercel deployment will use PostgreSQL through DATABASE_URL.
- Outlook/pywin32 email is intentionally NOT configured for Vercel yet.
- Email will be configured later.

NEXT STEPS:
1. Review the generated settings.py changes.
2. Test the application locally.
3. Create PostgreSQL (Neon recommended).
4. Configure DATABASE_URL on Vercel.
5. Migrate existing SQLite data into PostgreSQL.
6. Push the production source to GitHub.
7. Deploy to Vercel.
8. Configure email and 7 PM reports later.

DO NOT delete _local_backup\db.sqlite3 until the PostgreSQL migration has been verified.
'@

Set-Content -Path (Join-Path $ProjectRoot "VERCEL_DEPLOYMENT_NOTES.txt") -Value $Notes -Encoding UTF8
Write-Host "[6/8] Deployment notes created." -ForegroundColor Green

# -------------------------------------------------------------------
# 7. Report project state WITHOUT modifying application logic yet
# -------------------------------------------------------------------
Write-Host "[7/8] Checking important project files..." -ForegroundColor Green

$Checks = @(
    "manage.py",
    "requirements.txt",
    "kensova_core\settings.py",
    "kensova_core\urls.py",
    "store_app",
    ".gitignore",
    ".env.example"
)

foreach ($item in $Checks) {
    $full = Join-Path $ProjectRoot $item
    if (Test-Path $full) {
        Write-Host "      OK  $item" -ForegroundColor Green
    } else {
        Write-Host "      --  $item (not found)" -ForegroundColor Yellow
    }
}

# -------------------------------------------------------------------
# 8. Show Git status if Git exists; do not push anything yet.
# -------------------------------------------------------------------
Write-Host "[8/8] Checking Git..." -ForegroundColor Green

$git = Get-Command git -ErrorAction SilentlyContinue
if ($git) {
    git status --short
    Write-Host ""
    Write-Host "Git is installed. NO PUSH HAS BEEN PERFORMED." -ForegroundColor Yellow
} else {
    Write-Host "Git is not installed or not in PATH. No Git action performed." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " PREPARATION COMPLETE" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Your original project files were not deleted." -ForegroundColor White
Write-Host "Your SQLite database was backed up before any preparation." -ForegroundColor White
Write-Host ""
Write-Host "Database backup:" -ForegroundColor Yellow
Write-Host "  $DbBackup"
Write-Host ""
Write-Host "IMPORTANT: Do NOT push yet." -ForegroundColor Red
Write-Host "Next we will modify settings.py so the same Django code supports:"
Write-Host "  Local  -> SQLite"
Write-Host "  Vercel -> PostgreSQL"
Write-Host ""
Write-Host "Press Enter to finish."
Read-Host
