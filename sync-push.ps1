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
$manifestPath    = "$userProfile\.agents\sync-manifest.txt"  # lo que este equipo conoce de Drive (ver sync-manifest.ps1)
. "$driveSyncDir\sync-manifest.ps1"

# Basura que no debe viajar a Drive: entornos virtuales con rutas absolutas del
# equipo origen, historial git, cachés, y los desktop.ini que genera Drive.
$excludeDirs  = @(".venv", "venv", ".git", "__pycache__", ".pytest_cache", "node_modules", ".ruff_cache", "*.bak*")
$excludeFiles = @("desktop.ini", "*.pyc", "*.pyo", "Thumbs.db", ".DS_Store", "*.bak*")
$localOnlyCore = @("synced", "skill-catalog")
# Datos propios de cada equipo dentro de config (los mismos que excluye .gitignore): rutas
# absolutas de workspaces y estado local. No suben: sync-pull tampoco los trae.
$localOnlyConfigDirs  = @("projects", "sidecars")
$localOnlyConfigFiles = @(".migrated")
# Por encima de este numero de skills en el nucleo, el equipo sigue en el esquema antiguo
# (todo cargado) y un push desharia la separacion nucleo/biblioteca en Drive.
$maxCoreSkills = 70

function Copy-ToDrive {
    <#
      Sube un fichero a Drive salvo que la copia de Drive sea distinta y mas reciente (cambio del
      otro equipo aun sin sync-pull): en ese caso no se toca y se avisa. Antes se copiaba siempre
      con -Force y un equipo desactualizado pisaba el CLAUDE.md o GEMINI.md bueno.
    #>
    param([string]$Source, [string]$Dest)
    if (Test-Path -LiteralPath $Dest) {
        if ((Get-FileHash -LiteralPath $Source).Hash -eq (Get-FileHash -LiteralPath $Dest).Hash) { return }
        if ((Get-Item -LiteralPath $Dest).LastWriteTimeUtc -gt (Get-Item -LiteralPath $Source).LastWriteTimeUtc) {
            Write-Host "  [!] $Dest es mas reciente en Drive: no se sube. Haz sync-pull y repite." -ForegroundColor Yellow
            return
        }
    }
    Copy-Item -LiteralPath $Source -Destination $Dest -Force
}

function Sync-ConfigToDrive {
    <#
      Sube config sin purga y con /XO: no pisa en Drive la version mas reciente que subio el otro
      equipo, y no sube projects\, sidecars\ ni .migrated. Antes era /MIR: un equipo con un
      config.json antiguo sustituia el de Drive. Lo que se borre aqui no se borra en Drive.
    #>
    param([string]$Source, [string]$Dest, [string[]]$ExcludeDirs, [string[]]$ExcludeFiles)
    robocopy $Source $Dest /E /XO /XD skills @localOnlyConfigDirs @ExcludeDirs /XF @ExcludeFiles @localOnlyConfigFiles /NP /NFL /NDL /R:1 /W:1 | Out-Null
}

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
# Borrados en Drive: /MIR solo puede quitar lo que ya estaba en Drive en la ultima sincronizacion
# de este equipo (lo borraste aqui). Lo que llego despues es del otro equipo y aun no lo tienes.
$known = Read-SyncManifest $manifestPath
if ($null -eq $known) {
    Write-Host "[SYNC-PUSH] ABORTADO: este equipo no tiene registro de sincronizacion ($manifestPath)." -ForegroundColor Red
    Write-Host "            Ejecuta antes sync-pull, que lo crea." -ForegroundColor Red
    exit 1
}
$driveFiles = Get-SyncedFiles -CoreRoot "$driveSyncDir\agents_skills" -LibraryRoot "$driveSyncDir\skill_library" `
                  -LocalOnlyCore $localOnlyCore -ExcludeDirs $excludeDirs -ExcludeFiles $excludeFiles
$localFiles = Get-SyncedFiles -CoreRoot $agentsSkillsDir -LibraryRoot $libraryDir `
                  -LocalOnlyCore $localOnlyCore -ExcludeDirs $excludeDirs -ExcludeFiles $excludeFiles
$unknown = @(Get-UnknownPurges -DriveFiles $driveFiles -LocalFiles $localFiles -Known $known)
if ($unknown.Count -gt 0) {
    Write-Host "[SYNC-PUSH] ABORTADO: Drive tiene $($unknown.Count) ficheros que llegaron despues de tu ultima" -ForegroundColor Red
    Write-Host "            sincronizacion y este push los borraria. Ejecuta antes sync-pull." -ForegroundColor Red
    $unknown | Select-Object -First 5 | ForEach-Object { Write-Host "            - $_" -ForegroundColor Red }
    exit 1
}

Ensure-SkillsJunction -Link $claudeSkillsDir -Target $agentsSkillsDir
Ensure-SkillsJunction -Link $geminiSkillsDir -Target $agentsSkillsDir

# 1. Ficheros maestros de configuracion
foreach ($master in @("$geminiDir\GEMINI.md", "$claudeDir\CLAUDE.md")) {
    if (Test-Path $master) { Copy-ToDrive $master (Join-Path $driveSyncDir (Split-Path $master -Leaf)) }
}
# Catalogos fechados: GLOBAL_AGENTS_AND_TOOLS_<fecha>.md y SUBAGENTS_TEMPLATES_<fecha>.md.
foreach ($pattern in @("GLOBAL_AGENTS_AND_TOOLS_*.md", "SUBAGENTS_TEMPLATES_*.md", "CHEMBIO_MEDCHEM_TOOLKIT_*.md")) {
    Get-ChildItem "$geminiDir" -File -Filter $pattern | ForEach-Object { Copy-ToDrive $_.FullName (Join-Path $driveSyncDir $_.Name) }
}

# 2. Config, nucleo, biblioteca y agentes
$xd = @(); foreach ($d in $excludeDirs)  { $xd += $d }
$xf = @(); foreach ($f in $excludeFiles) { $xf += $f }

& "$driveSyncDir\build-skill-catalog.ps1"

if (Test-Path $configDir) {
    Sync-ConfigToDrive -Source $configDir -Dest "$driveSyncDir\config" -ExcludeDirs $xd -ExcludeFiles $xf
}
# Nucleo y biblioteca: /MIR para que se propaguen borrados y cambios de nivel, y /XO para que un
# equipo desactualizado no pise en Drive un fichero que el otro edito despues. Antes era /MIR a
# secas: el fichero local mas antiguo sustituia al de Drive.
robocopy "$agentsSkillsDir" "$driveSyncDir\agents_skills" /MIR /XO /XD @xd @localOnlyCore /XF @xf /NP /NFL /NDL /R:1 /W:1 | Out-Null
if (Test-Path $libraryDir) {
    # El duplicado anidado de ClaudeScientificSkills es identico al archivado y nadie lo
    # referencia: 39 MB que no tienen por que viajar.
    $nestedDup = "$libraryDir\tooluniverse-antibody-engineering\ClaudeScientificSkills"
    robocopy "$libraryDir" "$driveSyncDir\skill_library" /MIR /XO /XD @xd "$nestedDup" /XF @xf /NP /NFL /NDL /R:1 /W:1 | Out-Null
}
# Tras el push, Drive tiene lo mismo que este equipo: eso pasa a ser lo conocido. Lo que haya
# llegado del otro equipo durante el push no esta en la lista y queda protegido.
Save-SyncManifest -Path $manifestPath -Entries $localFiles -Origin "sync-push"
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
