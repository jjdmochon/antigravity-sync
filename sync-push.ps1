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
$agentsSkillsDir = "$userProfile\.agents\skills"   # <- unica copia canonica
$claudeSkillsDir = "$claudeDir\skills"
$geminiSkillsDir = "$configDir\skills"

# Basura que no debe viajar a Drive: entornos virtuales con rutas absolutas del
# equipo origen, historial git, cachés, y los desktop.ini que genera Drive.
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

Write-Host "[SYNC-PUSH] Sincronizando Claude, Gemini y Google Drive (Antigravity-Sync)..." -ForegroundColor Yellow

if (-not (Test-Path $agentsSkillsDir)) {
    Write-Host "[SYNC-PUSH] ERROR: no existe la copia canonica $agentsSkillsDir." -ForegroundColor Red
    exit 1
}
Ensure-SkillsJunction -Link $claudeSkillsDir -Target $agentsSkillsDir
Ensure-SkillsJunction -Link $geminiSkillsDir -Target $agentsSkillsDir

# 1. Ficheros maestros de configuracion
foreach ($pair in @(@("$geminiDir\GEMINI.md"),
                    @("$claudeDir\CLAUDE.md"),
                    @("$geminiDir\GLOBAL_AGENTS_AND_TOOLS.md"),
                    @("$geminiDir\SUBAGENTS_TEMPLATES.md"))) {
    if (Test-Path $pair[0]) { Copy-Item $pair[0] "$driveSyncDir\" -Force }
}

# 2. Config, skills y agentes
$xd = @(); foreach ($d in $excludeDirs)  { $xd += $d }
$xf = @(); foreach ($f in $excludeFiles) { $xf += $f }

if (Test-Path $configDir) {
    robocopy "$configDir" "$driveSyncDir\config" /MIR /XD skills @xd /XF @xf /NP /NFL /NDL /R:1 /W:1 | Out-Null
}
if (Test-Path $agentsSkillsDir) {
    # El duplicado anidado de ClaudeScientificSkills es identico al de nivel
    # superior y nadie lo referencia: 39 MB que no tienen por que viajar.
    $nestedDup = "$agentsSkillsDir\tooluniverse-antibody-engineering\ClaudeScientificSkills"
    robocopy "$agentsSkillsDir" "$driveSyncDir\agents_skills" /MIR /XD @xd "$nestedDup" /XF @xf /NP /NFL /NDL /R:1 /W:1 | Out-Null
}
if (Test-Path $claudeAgentsDir) {
    robocopy "$claudeAgentsDir" "$driveSyncDir\claude_agents" /MIR /XD @xd /XF @xf /NP /NFL /NDL /R:1 /W:1 | Out-Null
}

# 3. claude_skills quedo obsoleto: desde que .claude\skills es un junction, las
#    skills viajan una sola vez en agents_skills. Se avisa, no se borra solo.
if (Test-Path "$driveSyncDir\claude_skills") {
    Write-Host "  [!] '$driveSyncDir\claude_skills' es del esquema antiguo y ya no se actualiza." -ForegroundColor Yellow
    Write-Host "      Las skills viajan en 'agents_skills'. Puedes moverlo a archive\ cuando quieras." -ForegroundColor Yellow
}

$n = (Get-ChildItem "$driveSyncDir\agents_skills" -Directory -ErrorAction SilentlyContinue).Count
Write-Host "[SYNC-PUSH] Completado: $n skills en agents_skills (Google Drive)." -ForegroundColor Green
