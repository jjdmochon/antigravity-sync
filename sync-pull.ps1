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
$agentsSkillsDir = "$userProfile\.agents\skills"   # <- unica copia canonica
$claudeSkillsDir = "$claudeDir\skills"
$geminiSkillsDir = "$configDir\skills"

$excludeDirs  = @(".venv", "venv", ".git", "__pycache__", ".pytest_cache", "node_modules", ".ruff_cache", "*.bak*")
$excludeFiles = @("desktop.ini", "*.pyc", "*.pyo", "Thumbs.db", ".DS_Store", "*.bak*")

function Ensure-SkillsJunction {
    <#
      Garantiza que $Link sea un junction a $Target.
      El fallo de la version anterior: solo creaba el junction si la ruta no existia,
      asi que un directorio real ya presente se quedaba para siempre y divergia en
      silencio de la copia canonica. Aqui se aparta y se enlaza.
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

# 3. Junctions ANTES de espejar. En la version anterior se creaban despues, cuando
#    ya no servian de nada: si .claude\skills existia como directorio real, el pull
#    llenaba .agents\skills y dejaba la copia vieja de .claude intacta y divergente.
if (-not (Test-Path $agentsSkillsDir)) { New-Item -ItemType Directory -Force -Path $agentsSkillsDir | Out-Null }
Ensure-SkillsJunction -Link $claudeSkillsDir -Target $agentsSkillsDir
Ensure-SkillsJunction -Link $geminiSkillsDir -Target $agentsSkillsDir

# 4. Skills -> copia canonica (las otras dos rutas la ven por el junction)
if (Test-Path "$driveSyncDir\agents_skills") {
    robocopy "$driveSyncDir\agents_skills" "$agentsSkillsDir" /MIR /XD @xd /XF @xf /NP /NFL /NDL /R:1 /W:1 | Out-Null
}

# 5. Agentes
if (Test-Path "$driveSyncDir\claude_agents") {
    if (-not (Test-Path $claudeAgentsDir)) { New-Item -ItemType Directory -Force -Path $claudeAgentsDir | Out-Null }
    robocopy "$driveSyncDir\claude_agents" "$claudeAgentsDir" /MIR /XD @xd /XF @xf /NP /NFL /NDL /R:1 /W:1 | Out-Null
}

# 6. Claude Code: MCP de ambito usuario. Idempotente: solo añade los que falten.
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

# 7. GitHub: git usa la sesion de GitHub CLI (sin tokens en las URL de los remotos).
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

# 8. ffmpeg: lo usan /brag (voz, musica, silencedetect) y las skills de audio/video. No viaja por Drive.
if ((Get-Command ffmpeg -ErrorAction SilentlyContinue) -and (Get-Command ffprobe -ErrorAction SilentlyContinue)) {
    Write-Host "  [+] ffmpeg y ffprobe disponibles en el PATH." -ForegroundColor Green
} else {
    Write-Host "  [!] ffmpeg no esta instalado: winget install --id Gyan.FFmpeg -e   (reinicia la terminal despues)" -ForegroundColor Yellow
}

$n = (Get-ChildItem $agentsSkillsDir -Directory -ErrorAction SilentlyContinue).Count
Write-Host "[SYNC-PULL] Completado: $n skills disponibles en Claude, Gemini y Antigravity." -ForegroundColor Green
Write-Host "            Recuerda definir TYPESAFE_API_KEY y demas claves en ~\.env en este equipo." -ForegroundColor DarkGray
