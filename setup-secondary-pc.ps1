# =====================================================================
# Antigravity Sync - Setup para Equipo Secundario (PC B)
# =====================================================================
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ErrorActionPreference = "Continue"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Iniciando configuración de Antigravity en Equipo Secundario" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# Detectar ruta de Google Drive
$driveSyncDir = $PSScriptRoot
if (-not (Test-Path "$driveSyncDir\GEMINI.md")) {
    $candidates = @("K:\Mi unidad\Antigravity-Sync", "G:\Mi unidad\Antigravity-Sync", "D:\Mi unidad\Antigravity-Sync")
    foreach ($cand in $candidates) {
        if (Test-Path "$cand\GEMINI.md") {
            $driveSyncDir = $cand
            break
        }
    }
}

if (-not (Test-Path "$driveSyncDir\GEMINI.md")) {
    Write-Host "[ERROR] No se localizó la carpeta Antigravity-Sync en Google Drive." -ForegroundColor Red
    Write-Host "Por favor ejecuta este script directamente desde la carpeta de Google Drive." -ForegroundColor Yellow
    exit 1
}

Write-Host "[OK] Origen Google Drive detectado: $driveSyncDir" -ForegroundColor Green

$userProfile = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::UserProfile)
$geminiDir = "$userProfile\.gemini"
$configDir = "$geminiDir\config"
$binDir = "$geminiDir\antigravity-ide\bin"
$toolsDir = "$userProfile\tools"

New-Item -ItemType Directory -Force -Path $geminiDir | Out-Null
New-Item -ItemType Directory -Force -Path $binDir | Out-Null
New-Item -ItemType Directory -Force -Path $toolsDir | Out-Null

# 1. Copiar archivos maestros (.md) adaptando rutas de usuario si difieren
Write-Host "`n[1/4] Instalando archivos maestros de configuración..." -ForegroundColor Yellow
$userPlaceholder = [System.Environment]::UserName
$geminiMdContent = (Get-Content "$driveSyncDir\GEMINI.md" -Raw) -replace 'C:\\Users\\[^\\]+\\\.gemini', "$geminiDir"
Set-Content -Path "$geminiDir\GEMINI.md" -Value $geminiMdContent -Encoding UTF8

# Catalogos fechados (GLOBAL_AGENTS_AND_TOOLS_<fecha>.md, SUBAGENTS_TEMPLATES_<fecha>.md).
# Usan %USERPROFILE% y $HOME, asi que no hace falta reescribir rutas.
Get-ChildItem "$driveSyncDir" -File -Filter "GLOBAL_AGENTS_AND_TOOLS_*.md" | Copy-Item -Destination "$geminiDir\" -Force
Get-ChildItem "$driveSyncDir" -File -Filter "SUBAGENTS_TEMPLATES_*.md"     | Copy-Item -Destination "$geminiDir\" -Force
Get-ChildItem "$driveSyncDir" -File -Filter "CHEMBIO_MEDCHEM_TOOLKIT_*.md" | Copy-Item -Destination "$geminiDir\" -Force
Write-Host "  -> GEMINI.md y catalogos de agentes, subagentes y herramientas instalados." -ForegroundColor Green

# 2. Sincronizar / Enlazar carpeta config
Write-Host "`n[2/4] Configurando carpeta de plugins y skills (config)..." -ForegroundColor Yellow
if (Test-Path $configDir) {
    Write-Host "  -> Sincronizando plugins y skills existentes mediante Robocopy..." -ForegroundColor Gray
    robocopy "$driveSyncDir\config" "$configDir" /E /XO /NP /NFL /NDL /R:1 /W:1 | Out-Null
} else {
    Write-Host "  -> Creando Directory Junction hacia Google Drive..." -ForegroundColor Gray
    cmd /c mklink /J "$configDir" "$driveSyncDir\config" | Out-Null
    if (-not (Test-Path $configDir)) {
        New-Item -ItemType Directory -Force -Path $configDir | Out-Null
        robocopy "$driveSyncDir\config" "$configDir" /E /XO /NP /NFL /NDL /R:1 /W:1 | Out-Null
    }
}
Write-Host "  -> Carpeta config vinculada/actualizada con éxito." -ForegroundColor Green

# 3. Clonar watermarks-remover si no existe
Write-Host "`n[3/4] Comprobando toolkit watermarks-remover..." -ForegroundColor Yellow
$wmPath = "$toolsDir\watermarks-remover"
if (-not (Test-Path "$wmPath\service\scripts\clean_file.py")) {
    Write-Host "  -> Clonando watermarks-remover en $wmPath..." -ForegroundColor Gray
    git clone https://github.com/guillaumemeyer/watermarks-remover.git "$wmPath" | Out-Null
}
Write-Host "  -> watermarks-remover listo." -ForegroundColor Green

# 4. Instalar comandos CLI en bin
Write-Host "`n[4/4] Instalando comandos CLI globales en bin..." -ForegroundColor Yellow
$wmClean = '@echo off' + "`r`n" + ('python "' + $wmPath + '\service\scripts\clean_file.py" %*')
Set-Content -Path "$binDir\wm-clean.cmd" -Value $wmClean -Encoding UTF8

$wmInspect = '@echo off' + "`r`n" + ('python "' + $wmPath + '\service\scripts\inspect_file.py" %*')
Set-Content -Path "$binDir\wm-inspect.cmd" -Value $wmInspect -Encoding UTF8

$wmText = '@echo off' + "`r`n" + ('python "' + $wmPath + '\service\scripts\clean_text.py" %*')
Set-Content -Path "$binDir\wm-text.cmd" -Value $wmText -Encoding UTF8

$wmAudit = '@echo off' + "`r`n" + ('python "' + $wmPath + '\service\scripts\audit_dir.py" %*')
Set-Content -Path "$binDir\wm-audit.cmd" -Value $wmAudit -Encoding UTF8

$wmScore = '@echo off' + "`r`n" + ('python "' + $wmPath + '\service\scripts\score_stylometry.py" %*')
Set-Content -Path "$binDir\wm-score.cmd" -Value $wmScore -Encoding UTF8

$wmServe = '@echo off' + "`r`n" + ('python "' + $wmPath + '\service\scripts\server.py" %*')
Set-Content -Path "$binDir\wm-serve.cmd" -Value $wmServe -Encoding UTF8

# Comandos de sincronización rápida
$syncPullCmd = '@echo off' + "`r`n" + 'powershell -ExecutionPolicy Bypass -File "' + $driveSyncDir + '\sync-pull.ps1"'
Set-Content -Path "$binDir\sync-pull.cmd" -Value $syncPullCmd -Encoding UTF8

$syncPushCmd = '@echo off' + "`r`n" + 'powershell -ExecutionPolicy Bypass -File "' + $driveSyncDir + '\sync-push.ps1"'
Set-Content -Path "$binDir\sync-push.cmd" -Value $syncPushCmd -Encoding UTF8

Write-Host "  -> Comandos globales CLI instalados en: $binDir" -ForegroundColor Green

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "  ¡Listo! Tu segundo equipo está 100% sincronizado con:" -ForegroundColor Green
Write-Host "   - 236 Skills globales y todos los plugins de juanjo-copilot" -ForegroundColor White
Write-Host "   - Todas las configuraciones maestras de Antigravity" -ForegroundColor White
Write-Host "   - Herramientas CLI: wm-clean, wm-inspect, wm-score, etc." -ForegroundColor White
Write-Host "============================================================" -ForegroundColor Cyan
