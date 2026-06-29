$ErrorActionPreference = "Stop"

Write-Host "=============================================" -ForegroundColor Cyan
Write-Host " SETJA Installer Compiler (.EXE Builder)" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

$iscc_global = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
$iscc_local = "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe"

$iscc = ""
if (Test-Path $iscc_global) { $iscc = $iscc_global }
elseif (Test-Path $iscc_local) { $iscc = $iscc_local }

if (-not $iscc) {
    Write-Host "Inno Setup is not installed. Downloading and installing Inno Setup Compiler..." -ForegroundColor Yellow
    Write-Host "Please wait..."
    winget install -e --id JRSoftware.InnoSetup --silent --accept-package-agreements --accept-source-agreements
    
    if (Test-Path $iscc_global) { $iscc = $iscc_global }
    elseif (Test-Path $iscc_local) { $iscc = $iscc_local }
}

if (-not $iscc) {
    Write-Host ""
    Write-Host "[ERROR] Failed to find Inno Setup compiler." -ForegroundColor Red
    Write-Host "Please install it manually from https://jrsoftware.org/isinfo.php" -ForegroundColor Red
    Pause
    exit 1
}

Write-Host ""
Write-Host "Compiling SETJA_Installer.iss into a professional .exe setup..." -ForegroundColor Cyan
& $iscc ".\SETJA_Installer.iss"

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "SUCCESS! The installer is ready." -ForegroundColor Green
    Write-Host "You can find it here: SETJA_Setup_v1.0.exe" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "[ERROR] Compilation failed." -ForegroundColor Red
}

Write-Host ""
Pause
