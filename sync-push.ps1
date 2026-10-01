[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Localizar la carpeta de Drive. $PSScriptRoot cubre el caso normal; la lista de
# respaldo cubre que la unidad de Drive cambie de letra entre equipos.
$driveSyncDir = $PSScriptRoot
if (-not (Test-Path "$driveSyncDir\README.md")) {
    foreach ($candidate in @("K:\Mi unidad\Antigravity-Sync",
                             "I:\Mi unidad\Antigravity-Sync",
                             "G:\Mi unidad\Antigravity-Sync",
                             "$env:USERPROFILE\Google Drive\Antigravity-Sync")) {
        if (Test-Path "$candidate\README.md") { $driveSyncDir = $candidate; break }
    }
}
if (-not (Test-Path "$driveSyncDir\README.md")) {
    Write-Host "[SYNC-PUSH] ERROR: no encuentro Antigravity-Sync. Edita la lista de rutas." -ForegroundColor Red
    exit 1
}

$userProfile     = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::UserProfile)
$geminiDir       = "$userProfile\.gemini"
$configDir       = "$geminiDir\config"
$claudeDir       = "$userProfile\.claude"
$claudeAgentsDir = "$claudeDir\agents"
$agentsSkillsDir = "$userProfile\.agents\skills"          # nucleo: se carga siempre
$libraryDir      = "$userProfile\.agents\skill-library"   # biblioteca: bajo demanda (skill-catalog)
$claudeSkillsDir = "$claudeDir\skills"
$geminiSkillsDir = "$configDir\skills"

# Basura que no debe viajar a Drive: entornos virtuales con rutas absolutas del
# equipo origen, historial git, cachés, y los desktop.ini que genera Drive.
$excludeDirs  = @(".venv", "venv", ".git", "__pycache__", ".pytest_cache", "node_modules", ".ruff_cache", "*.bak*")
$excludeFiles = @("desktop.ini", "*.pyc", "*.pyo", "Thumbs.db", ".DS_Store", "*.bak*")
$localOnlyCore = @("synced", "skill-catalog")
# Por encima de este numero de skills en el nucleo, el equipo sigue en el esquema antiguo
# (todo cargado) y un push desharia la separacion nucleo/biblioteca en Drive.
$maxCoreSkills = 70

function Ensure-SkillsJunction {
    param([string]$Link, [string]$Target)

    $item = Get-Item $Link -Force -ErrorAction SilentlyContinue
    if ($item -and $item.LinkType -eq "Junction") { return }

    if ($item) {
        $stamp  = Get-Date -Format "yyyyMMdd-HHmmss"
        $backup = "$(Split-Path $Link -Leaf).bak-$stamp"
        Rename-Item -LiteralPath $Link -NewName $backup -Force
        Write-Host "  [!] $Link era un directorio real. Apartado como $backup." -ForegroundColor Yellow
        Write-Host "      Revisalo y borralo cuando confirmes que no perdiste nada." -ForegroundColor Yellow
    }
    $parent = Split-Path $Link -Parent
    if (-not (Test-Path $parent)) { New-Item -ItemType Directory -Force -Path $parent | Out-Null }
    cmd /c mklink /J "$Link" "$Target" | Out-Null
    Write-Host "  [+] Junction creado: $Link -> $Target" -ForegroundColor Green
}

Write-Host "[SYNC-PUSH] Sincronizando Claude, Gemini y Google Drive (Antigravity-Sync)..." -ForegroundColor Yellow

if (-not (Test-Path $agentsSkillsDir)) {
    Write-Host "[SYNC-PUSH] ERROR: no existe el nucleo $agentsSkillsDir." -ForegroundColor Red
    exit 1
}

# 0. Salvaguardas: no subir desde un equipo sin migrar ni con la biblioteca vacia.
$coreDirs = @(Get-ChildItem $agentsSkillsDir -Directory -Force | Where-Object { $_.Name -notin $localOnlyCore })
if ($coreDirs.Count -gt $maxCoreSkills) {
    Write-Host "[SYNC-PUSH] ABORTADO: $($coreDirs.Count) skills en el nucleo (maximo $maxCoreSkills)." -ForegroundColor Red
    Write-Host "            Este equipo sigue en el esquema antiguo. Ejecuta antes sync-pull, que mueve" -ForegroundColor Red
    Write-Host "            las skills que no son nucleo a ~\.agents\skill-library." -ForegroundColor Red
    exit 1
}
$driveLib = @(); if (Test-Path "$driveSyncDir\skill_library") { $driveLib = (Get-ChildItem "$driveSyncDir\skill_library" -Directory).Name }
$localLib = @(); if (Test-Path $libraryDir) { $localLib = (Get-ChildItem $libraryDir -Directory).Name }
$missing  = @($driveLib | Where-Object { $_ -notin $localLib -and $_ -notin $coreDirs.Name })
if ($missing.Count -gt 0) {
    Write-Host "[SYNC-PUSH] ABORTADO: Drive tiene $($missing.Count) skills de biblioteca que este equipo no tiene" -ForegroundColor Red
    Write-Host "            ($(($missing | Select-Object -First 5) -join ', ')...). Ejecuta antes sync-pull." -ForegroundColor Red
    exit 1
}

Ensure-SkillsJunction -Link $claudeSkillsDir -Target $agentsSkillsDir
Ensure-SkillsJunction -Link $geminiSkillsDir -Target $agentsSkillsDir

# 1. Ficheros maestros de configuracion
foreach ($master in @("$geminiDir\GEMINI.md", "$claudeDir\CLAUDE.md")) {
    if (Test-Path $master) { Copy-Item $master "$driveSyncDir\" -Force }
}
# Catalogos fechados: GLOBAL_AGENTS_AND_TOOLS_<fecha>.md y SUBAGENTS_TEMPLATES_<fecha>.md.
Get-ChildItem "$geminiDir" -File -Filter "GLOBAL_AGENTS_AND_TOOLS_*.md" | Copy-Item -Destination "$driveSyncDir\" -Force
Get-ChildItem "$geminiDir" -File -Filter "SUBAGENTS_TEMPLATES_*.md"     | Copy-Item -Destination "$driveSyncDir\" -Force
Get-ChildItem "$geminiDir" -File -Filter "CHEMBIO_MEDCHEM_TOOLKIT_*.md" | Copy-Item -Destination "$driveSyncDir\" -Force

# 2. Config, nucleo, biblioteca y agentes
$xd = @(); foreach ($d in $excludeDirs)  { $xd += $d }
$xf = @(); foreach ($f in $excludeFiles) { $xf += $f }

& "$driveSyncDir\build-skill-catalog.ps1"

if (Test-Path $configDir) {
    robocopy "$configDir" "$driveSyncDir\config" /MIR /XD skills @xd /XF @xf /NP /NFL /NDL /R:1 /W:1 | Out-Null
}
robocopy "$agentsSkillsDir" "$driveSyncDir\agents_skills" /MIR /XD @xd @localOnlyCore /XF @xf /NP /NFL /NDL /R:1 /W:1 | Out-Null
if (Test-Path $libraryDir) {
    # El duplicado anidado de ClaudeScientificSkills es identico al archivado y nadie lo
    # referencia: 39 MB que no tienen por que viajar.
    $nestedDup = "$libraryDir\tooluniverse-antibody-engineering\ClaudeScientificSkills"
    robocopy "$libraryDir" "$driveSyncDir\skill_library" /MIR /XD @xd "$nestedDup" /XF @xf /NP /NFL /NDL /R:1 /W:1 | Out-Null
}
if (Test-Path $claudeAgentsDir) {
    robocopy "$claudeAgentsDir" "$driveSyncDir\claude_agents" /MIR /XD @xd /XF @xf /NP /NFL /NDL /R:1 /W:1 | Out-Null
}

# 3. claude_skills quedo obsoleto: desde que .claude\skills es un junction, las
#    skills viajan una sola vez en agents_skills. Se avisa, no se borra solo.
if (Test-Path "$driveSyncDir\claude_skills") {
    Write-Host "  [!] '$driveSyncDir\claude_skills' es del esquema antiguo y ya no se actualiza." -ForegroundColor Yellow
    Write-Host "      Puedes moverlo a archive\ cuando quieras." -ForegroundColor Yellow
}

$nCore = (Get-ChildItem "$driveSyncDir\agents_skills" -Directory -ErrorAction SilentlyContinue).Count
$nLib  = (Get-ChildItem "$driveSyncDir\skill_library" -Directory -ErrorAction SilentlyContinue).Count
Write-Host "[SYNC-PUSH] Completado: $nCore skills de nucleo y $nLib de biblioteca en Google Drive." -ForegroundColor Green
