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
    Write-Host "[SYNC-PULL] ERROR: no encuentro Antigravity-Sync. Edita la lista de rutas." -ForegroundColor Red
    exit 1
}

$userProfile     = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::UserProfile)
$geminiDir       = "$userProfile\.gemini"
$configDir       = "$geminiDir\config"
$claudeDir       = "$userProfile\.claude"
$claudeAgentsDir = "$claudeDir\agents"
$agentsSkillsDir = "$userProfile\.agents\skills"          # nucleo: se carga siempre
$libraryDir      = "$userProfile\.agents\skill-library"   # biblioteca: bajo demanda (skill-catalog)
$archiveDir      = "$userProfile\.agents\skill-archive"
$claudeSkillsDir = "$claudeDir\skills"
$geminiSkillsDir = "$configDir\skills"

$excludeDirs  = @(".venv", "venv", ".git", "__pycache__", ".pytest_cache", "node_modules", ".ruff_cache", "*.bak*")
$excludeFiles = @("desktop.ini", "*.pyc", "*.pyo", "Thumbs.db", ".DS_Store", "*.bak*")
# Carpetas del nucleo que no viajan: synced lo escribe la app de Claude en cada equipo y
# skill-catalog se regenera aqui mismo a partir de la biblioteca local.
$localOnlyCore = @("synced", "skill-catalog")

function Ensure-SkillsJunction {
    <#
      Garantiza que $Link sea un junction a $Target. Si es un directorio real, se aparta
      como .bak-<fecha> y se enlaza (antes divergia en silencio de la copia canonica).
    #>
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

Write-Host "[SYNC-PULL] Actualizando Claude y Gemini desde Google Drive (Antigravity-Sync)..." -ForegroundColor Yellow

# 1. Ficheros maestros
foreach ($dir in @($claudeDir, $geminiDir, $configDir)) {
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
}
if (Test-Path "$driveSyncDir\GEMINI.md")                   { Copy-Item "$driveSyncDir\GEMINI.md" "$geminiDir\" -Force }
if (Test-Path "$driveSyncDir\CLAUDE.md")                   { Copy-Item "$driveSyncDir\CLAUDE.md" "$claudeDir\" -Force }
if (Test-Path "$driveSyncDir\GLOBAL_AGENTS_AND_TOOLS.md")  { Copy-Item "$driveSyncDir\GLOBAL_AGENTS_AND_TOOLS.md" "$geminiDir\" -Force }
if (Test-Path "$driveSyncDir\SUBAGENTS_TEMPLATES.md")      { Copy-Item "$driveSyncDir\SUBAGENTS_TEMPLATES.md" "$geminiDir\" -Force }

# 2. Config (sin tocar skills, que es junction)
$xd = @(); foreach ($d in $excludeDirs)  { $xd += $d }
$xf = @(); foreach ($f in $excludeFiles) { $xf += $f }
if (Test-Path "$driveSyncDir\config") {
    robocopy "$driveSyncDir\config" "$configDir" /MIR /XD skills @xd /XF @xf /NP /NFL /NDL /R:1 /W:1 | Out-Null
}

# 3. Junctions ANTES de espejar, para que .claude\skills y .gemini\config\skills nunca
#    queden como copias reales divergentes.
foreach ($dir in @($agentsSkillsDir, $libraryDir, $archiveDir)) {
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
}
Ensure-SkillsJunction -Link $claudeSkillsDir -Target $agentsSkillsDir
Ensure-SkillsJunction -Link $geminiSkillsDir -Target $agentsSkillsDir

# 4. Biblioteca primero (sin purga: nunca borra skills locales que Drive no tenga).
if (Test-Path "$driveSyncDir\skill_library") {
    robocopy "$driveSyncDir\skill_library" "$libraryDir" /E /XO /XD @xd /XF @xf /NP /NFL /NDL /R:1 /W:1 | Out-Null
}

# 5. Rescate: lo que haya en el nucleo local y ya no forme parte del nucleo de Drive se
#    mueve a la biblioteca en vez de borrarse. Antes /MIR lo eliminaba sin avisar.
$driveCore = @()
if (Test-Path "$driveSyncDir\agents_skills") { $driveCore = (Get-ChildItem "$driveSyncDir\agents_skills" -Directory -Force).Name }
foreach ($dir in Get-ChildItem $agentsSkillsDir -Directory -Force -ErrorAction SilentlyContinue) {
    if ($dir.Name -in $driveCore -or $dir.Name -in $localOnlyCore) { continue }
    $dest = Join-Path $libraryDir $dir.Name
    if (Test-Path $dest) { $dest = Join-Path $archiveDir "$($dir.Name).bak-$(Get-Date -Format 'yyyyMMdd-HHmmss')" }
    Move-Item -LiteralPath $dir.FullName -Destination $dest -Force
    Write-Host "  [>] '$($dir.Name)' ya no es nucleo: movida a $(Split-Path $dest -Parent)" -ForegroundColor Yellow
}

# 6. Nucleo. /XO no pisa ficheros locales mas recientes (cambios aun sin sync-push).
if (Test-Path "$driveSyncDir\agents_skills") {
    robocopy "$driveSyncDir\agents_skills" "$agentsSkillsDir" /MIR /XO /XD @xd @localOnlyCore /XF @xf /NP /NFL /NDL /R:1 /W:1 | Out-Null
}

# 7. Catalogo de la biblioteca (rutas de este equipo).
& "$driveSyncDir\build-skill-catalog.ps1"

# 8. Agentes
if (Test-Path "$driveSyncDir\claude_agents") {
    if (-not (Test-Path $claudeAgentsDir)) { New-Item -ItemType Directory -Force -Path $claudeAgentsDir | Out-Null }
    robocopy "$driveSyncDir\claude_agents" "$claudeAgentsDir" /MIR /XD @xd /XF @xf /NP /NFL /NDL /R:1 /W:1 | Out-Null
}

# 9. Claude Code: MCP de ambito usuario. Idempotente: solo añade los que falten.
if (Get-Command claude -ErrorAction SilentlyContinue) {
    $mcps = [ordered]@{
        "gemini-api-docs" = @("--transport", "http", "gemini-api-docs", "https://gemini-api-docs-mcp.dev")
        "chrome-devtools" = @("chrome-devtools", "--", "npx", "-y", "chrome-devtools-mcp@latest")
        "tooluniverse"    = @("tooluniverse", "--", "uvx", "--from", "tooluniverse", "tooluniverse-smcp-stdio")
    }
    foreach ($name in $mcps.Keys) {
        claude mcp get $name *> $null
        if ($LASTEXITCODE -ne 0) {
            claude mcp add --scope user @($mcps[$name]) *> $null
            Write-Host "  [+] MCP '$name' registrado en Claude Code." -ForegroundColor Green
        }
    }
} else {
    Write-Host "  [!] Claude Code no esta instalado. Instalalo y vuelve a ejecutar sync-pull:" -ForegroundColor Yellow
    Write-Host "      irm https://claude.ai/install.ps1 | iex" -ForegroundColor Yellow
}

# 10. GitHub: git usa la sesion de GitHub CLI (sin tokens en las URL de los remotos).
if (Get-Command gh -ErrorAction SilentlyContinue) {
    gh auth status *> $null
    if ($LASTEXITCODE -eq 0) {
        gh auth setup-git *> $null
        Write-Host "  [+] git enlazado con la sesion de GitHub CLI." -ForegroundColor Green
    } else {
        Write-Host "  [!] GitHub CLI sin sesion. Ejecuta 'gh auth login' y luego vuelve a ejecutar sync-pull." -ForegroundColor Yellow
    }
} else {
    Write-Host "  [!] GitHub CLI no esta instalado: winget install GitHub.cli" -ForegroundColor Yellow
}

# 11. ffmpeg: lo usan /brag (voz, musica, silencedetect) y las skills de audio/video. No viaja por Drive.
if ((Get-Command ffmpeg -ErrorAction SilentlyContinue) -and (Get-Command ffprobe -ErrorAction SilentlyContinue)) {
    Write-Host "  [+] ffmpeg y ffprobe disponibles en el PATH." -ForegroundColor Green
} else {
    Write-Host "  [!] ffmpeg no esta instalado: winget install --id Gyan.FFmpeg -e   (reinicia la terminal despues)" -ForegroundColor Yellow
}

$nCore = (Get-ChildItem $agentsSkillsDir -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -ne "synced" }).Count
$nLib  = (Get-ChildItem $libraryDir -Directory -ErrorAction SilentlyContinue).Count
Write-Host "[SYNC-PULL] Completado: $nCore skills en el nucleo y $nLib en la biblioteca (via skill-catalog)." -ForegroundColor Green
Write-Host "            Recuerda definir TYPESAFE_API_KEY y demas claves en ~\.env en este equipo." -ForegroundColor DarkGray
