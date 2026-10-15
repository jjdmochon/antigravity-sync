[CmdletBinding()]
param(
    [switch]$Detalle,      # lista todos los ficheros, no solo los primeros
    [switch]$Silencioso,   # una sola linea y solo si hay algo que sincronizar (para hooks)
    [switch]$SinGit        # no consulta GitHub (evita git fetch)
)
# sync-status: dice si toca sync-pull o sync-push SIN modificar nada (solo lectura).
# Compara este equipo con Drive en los mismos ambitos que sync-push/sync-pull y usa el registro
# ~\.agents\sync-manifest.txt para distinguir un borrado local de un fichero nuevo del otro equipo.
# Codigo de salida: 0 al dia, 1 toca push, 2 toca pull, 3 toca pull y despues push.

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

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
    Write-Host "[SYNC-STATUS] ERROR: no encuentro Antigravity-Sync." -ForegroundColor Red
    exit 9
}

$userProfile     = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::UserProfile)
$geminiDir       = "$userProfile\.gemini"
$configDir       = "$geminiDir\config"
$claudeDir       = "$userProfile\.claude"
$agentsSkillsDir = "$userProfile\.agents\skills"
$libraryDir      = "$userProfile\.agents\skill-library"
$manifestPath    = "$userProfile\.agents\sync-manifest.txt"
$claudeMemoryDir = "$claudeDir\projects\$($userProfile -replace '[:\\/]', '-')\memory"
$claudeSettings  = "$claudeDir\settings.json"
. "$driveSyncDir\sync-manifest.ps1"

# Mismas exclusiones que sync-push y sync-pull.
$xd = @(".venv", "venv", ".git", "__pycache__", ".pytest_cache", "node_modules", ".ruff_cache", "*.bak*")
$xf = @("desktop.ini", "*.pyc", "*.pyo", "Thumbs.db", ".DS_Store", "*.bak*")
$localOnlyCore        = @("synced", "skill-catalog", ".trash")
$localOnlyConfigDirs  = @("projects", "sidecars")
$localOnlyConfigFiles = @(".migrated")
$nestedDup = "tooluniverse-antibody-engineering\ClaudeScientificSkills"

function Get-RoboList {
    # Rutas relativas que robocopy /XO copiaria de $Source a $Dest (pasada en seco, no toca nada).
    param([string]$Source, [string]$Dest, [string[]]$XD = @(), [string[]]$XF = @())
    if (-not (Test-Path -LiteralPath $Source)) { return @() }
    $src = $Source.TrimEnd('\')
    $a = @($src, $Dest.TrimEnd('\'), "/E", "/XO", "/L", "/NJH", "/NJS", "/NDL", "/NC", "/NS", "/FP", "/NP", "/R:0", "/W:0")
    if ($XD.Count) { $a += "/XD"; $a += $XD }
    if ($XF.Count) { $a += "/XF"; $a += $XF }
    $out = & robocopy @a
    @($out | ForEach-Object { "$_".Trim() } |
        Where-Object { $_.StartsWith($src + "\", [System.StringComparison]::OrdinalIgnoreCase) } |
        ForEach-Object { $_.Substring($src.Length + 1) })
}

function Remove-Identical {
    # Descarta los que solo difieren en la fecha (mismo contenido). Solo si son pocos: el hash en Drive es lento.
    param([string[]]$Rels, [string]$A, [string]$B)
    if ($Rels.Count -eq 0 -or $Rels.Count -gt 300) { return @($Rels) }
    @($Rels | Where-Object {
        $pa = Join-Path $A $_; $pb = Join-Path $B $_
        -not ((Test-Path -LiteralPath $pa) -and (Test-Path -LiteralPath $pb) -and
              ((Get-FileHash -LiteralPath $pa).Hash -eq (Get-FileHash -LiteralPath $pb).Hash))
    })
}

function Set-Of([string[]]$Items) {
    $s = New-Object 'System.Collections.Generic.HashSet[string]' ([System.StringComparer]::OrdinalIgnoreCase)
    foreach ($i in $Items) { [void]$s.Add($i) }
    return ,$s
}

$toPull = New-Object System.Collections.Generic.List[object]   # @{Area; Item; Nota}
$toPush = New-Object System.Collections.Generic.List[object]
$review = New-Object System.Collections.Generic.List[string]

function Add-Item($list, [string]$area, [string]$item, [string]$nota = "") {
    $list.Add([pscustomobject]@{ Area = $area; Item = $item; Nota = $nota })
}

# --- Registro de la ultima sincronizacion -------------------------------------------------------
$known = Read-SyncManifest $manifestPath
$ultima = "nunca"
if ($null -ne $known) {
    $h = Get-Content -LiteralPath $manifestPath -TotalCount 1 -Encoding UTF8
    if ($h -match '(?<d>\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)') { $ultima = $Matches['d'] }
    if ($h -match 'tras (?<o>sync-\w+)') { $ultima = "$ultima ($($Matches['o']))" }
} else {
    $review.Add("Este equipo no tiene registro de sincronizacion: ejecuta sync-pull antes que nada.")
}

# --- 1. Ficheros maestros y catalogos fechados --------------------------------------------------
$masters = @{}
foreach ($n in @("CLAUDE.md", "GEMINI.md")) { $masters[$n] = $true }
foreach ($p in @("GLOBAL_AGENTS_AND_TOOLS_*.md", "SUBAGENTS_TEMPLATES_*.md", "CHEMBIO_MEDCHEM_TOOLKIT_*.md")) {
    Get-ChildItem $driveSyncDir -File -Filter $p -ErrorAction SilentlyContinue | ForEach-Object { $masters[$_.Name] = $true }
    Get-ChildItem $geminiDir   -File -Filter $p -ErrorAction SilentlyContinue | ForEach-Object { $masters[$_.Name] = $true }
}
foreach ($name in $masters.Keys) {
    $loc = if ($name -eq "CLAUDE.md") { Join-Path $claudeDir $name } else { Join-Path $geminiDir $name }
    $drv = Join-Path $driveSyncDir $name
    $hasL = Test-Path -LiteralPath $loc; $hasD = Test-Path -LiteralPath $drv
    if ($hasL -and -not $hasD) { Add-Item $toPush "Maestros" $name "solo aqui"; continue }
    if ($hasD -and -not $hasL) { Add-Item $toPull "Maestros" $name "solo en Drive"; continue }
    if (-not $hasL -and -not $hasD) { continue }
    if ((Get-FileHash -LiteralPath $loc).Hash -eq (Get-FileHash -LiteralPath $drv).Hash) { continue }
    if ((Get-Item -LiteralPath $loc).LastWriteTimeUtc -gt (Get-Item -LiteralPath $drv).LastWriteTimeUtc) {
        Add-Item $toPush "Maestros" $name "version local mas reciente"
    } else {
        Add-Item $toPull "Maestros" $name "version de Drive mas reciente"
    }
}

# --- 2. Carpetas -------------------------------------------------------------------------------
$configTop = @("skills") + $localOnlyConfigDirs
$areas = @(
    @{ Name = "Nucleo de skills";     Local = $agentsSkillsDir; Drive = "$driveSyncDir\agents_skills"; Prefix = "agents_skills"; Skip = $localOnlyCore; Purge = $true },
    @{ Name = "Biblioteca de skills"; Local = $libraryDir;      Drive = "$driveSyncDir\skill_library"; Prefix = "skill_library"; Skip = @(); Purge = $true },
    @{ Name = "Agentes";              Local = "$claudeDir\agents";   Drive = "$driveSyncDir\claude_agents";   Prefix = $null },
    @{ Name = "Hooks";                Local = "$claudeDir\hooks";    Drive = "$driveSyncDir\claude_hooks";    Prefix = $null },
    @{ Name = "Comandos";             Local = "$claudeDir\commands"; Drive = "$driveSyncDir\claude_commands"; Prefix = $null },
    @{ Name = "Memoria global";       Local = $claudeMemoryDir;      Drive = "$driveSyncDir\claude_memory";   Prefix = $null },
    @{ Name = "Config Gemini";        Local = $configDir;            Drive = "$driveSyncDir\config";          Prefix = $null; Config = $true }
)

foreach ($ar in $areas) {
    $dirsDown = $xd + @($ar.Skip)                 # Drive -> aqui
    $dirsUp   = $xd + @($ar.Skip)                 # aqui -> Drive
    $files    = $xf
    if ($ar.Config) {
        $dirsDown += ($configTop | ForEach-Object { Join-Path $ar.Drive $_ })
        $dirsUp   += ($configTop | ForEach-Object { Join-Path $ar.Local $_ })
        $files     = $xf + $localOnlyConfigFiles
    }
    if ($ar.Prefix -eq "skill_library") { $dirsUp += (Join-Path $ar.Local $nestedDup) }

    $down = @(Get-RoboList -Source $ar.Drive -Dest $ar.Local -XD $dirsDown -XF $files)
    $up   = @(Get-RoboList -Source $ar.Local -Dest $ar.Drive -XD $dirsUp   -XF $files)
    $down = @(Remove-Identical $down $ar.Drive $ar.Local)
    $up   = @(Remove-Identical $up   $ar.Local $ar.Drive)

    if ($ar.Purge -and $null -ne $known) {
        # Fichero de Drive que este equipo conocia y ya no tiene: lo borraste aqui, toca push (no restaurarlo).
        $downKept = @()
        foreach ($r in $down) {
            $full = Join-Path $ar.Local $r
            if (-not (Test-Path -LiteralPath $full) -and $known.Contains((Join-Path $ar.Prefix $r))) {
                Add-Item $toPush $ar.Name $r "borrado aqui (push lo quitara de Drive)"
            } else { $downKept += $r }
        }
        $down = $downKept
    }
    foreach ($r in $down) { Add-Item $toPull $ar.Name $r }
    foreach ($r in $up)   { Add-Item $toPush $ar.Name $r }
}

# Nucleo: lo que el otro equipo borro en Drive y aqui sigue (sync-pull lo borraria aqui).
if ($null -ne $known -and (Test-Path "$driveSyncDir\agents_skills")) {
    $driveCoreFiles = Get-SyncTreeFiles -Root "$driveSyncDir\agents_skills" -Prefix "agents_skills" -SkipTopDirs $localOnlyCore -ExcludeDirs $xd -ExcludeFiles $xf
    $driveSet = Set-Of @($driveCoreFiles | ForEach-Object { $_ })
    $localCoreFiles = Get-SyncTreeFiles -Root $agentsSkillsDir -Prefix "agents_skills" -SkipTopDirs $localOnlyCore -ExcludeDirs $xd -ExcludeFiles $xf
    foreach ($rel in @($localCoreFiles | ForEach-Object { $_ })) {
        if ($known.Contains($rel) -and -not $driveSet.Contains($rel)) {
            Add-Item $toPull "Nucleo de skills" ($rel.Substring("agents_skills\".Length)) "borrado en el otro equipo"
        }
    }
}

# --- 3. Parte compartida de settings.json (autoMode, skillOverrides, hooks) ---------------------
$settingsShared = "$driveSyncDir\claude_settings_shared.json"
$pyExe = $null; $pyPre = @()
if (Get-Command py -ErrorAction SilentlyContinue) { $pyExe = "py"; $pyPre = @("-3") }
elseif (Get-Command python -ErrorAction SilentlyContinue) { $pyExe = "python" }
if ($pyExe -and (Test-Path $claudeSettings) -and (Test-Path $settingsShared)) {
    $tmp = Join-Path $env:TEMP "sync-status-settings.json"
    try {
        & $pyExe @pyPre "$driveSyncDir\claude-settings-sync.py" export $claudeSettings $tmp *> $null
        if ((Test-Path $tmp) -and ((Get-FileHash $tmp).Hash -ne (Get-FileHash $settingsShared).Hash)) {
            $review.Add("settings.json: la parte compartida (autoMode, skillOverrides, hooks) difiere de Drive. Si la cambiaste aqui, push; si viene del otro equipo, pull.")
        }
    } catch { } finally { Remove-Item $tmp -Force -ErrorAction SilentlyContinue }
}

# --- 4. GitHub (informativo: no afecta a pull/push) ---------------------------------------------
$gitLinea = $null
if (-not $SinGit -and (Test-Path "$driveSyncDir\.git") -and (Get-Command git -ErrorAction SilentlyContinue)) {
    Push-Location $driveSyncDir
    try {
        git fetch --quiet 2>$null
        $sucios = @(git status --porcelain 2>$null).Count
        $cnt = (git rev-list --left-right --count "HEAD...@{u}" 2>$null)
        $ahead = 0; $behind = 0
        if ($cnt -match '^(\d+)\s+(\d+)') { $ahead = [int]$Matches[1]; $behind = [int]$Matches[2] }
        $partes = @()
        if ($sucios -gt 0) { $partes += "$sucios fichero(s) sin commit" }
        if ($ahead  -gt 0) { $partes += "$ahead commit(s) sin push a GitHub" }
        if ($behind -gt 0) { $partes += "$behind commit(s) nuevos en GitHub (git pull)" }
        $gitLinea = if ($partes.Count) { $partes -join "; " } else { "al dia con GitHub" }
    } catch { $gitLinea = "no se pudo consultar" } finally { Pop-Location }
}

# --- Veredicto ----------------------------------------------------------------------------------
$nPull = $toPull.Count; $nPush = $toPush.Count
if     ($nPull -eq 0 -and $nPush -eq 0) { $code = 0; $veredicto = "AL DIA: no hace falta sync-pull ni sync-push." ; $color = "Green" }
elseif ($nPull -eq 0)                   { $code = 1; $veredicto = "TOCA sync-push ($nPush cambio(s) de este equipo)."; $color = "Yellow" }
elseif ($nPush -eq 0)                   { $code = 2; $veredicto = "TOCA sync-pull ($nPull cambio(s) de Drive)."; $color = "Yellow" }
else                                    { $code = 3; $veredicto = "TOCA sync-pull y despues sync-push (Drive: $nPull, aqui: $nPush)."; $color = "Magenta" }
if ($null -eq $known) { $code = 2; $veredicto = "TOCA sync-pull (este equipo no tiene registro de sincronizacion)."; $color = "Yellow" }

if ($Silencioso) {
    if ($code -ne 0) { Write-Host "[SYNC] $veredicto" -ForegroundColor $color }
    exit $code
}

function Show-Group([string]$title, $list) {
    if ($list.Count -eq 0) { return }
    Write-Host ""
    Write-Host $title -ForegroundColor Cyan
    foreach ($g in ($list | Group-Object Area)) {
        Write-Host ("  {0}: {1}" -f $g.Name, $g.Count)
        $items = if ($Detalle) { $g.Group } else { $g.Group | Select-Object -First 5 }
        foreach ($i in $items) {
            $n = if ($i.Nota) { "  ($($i.Nota))" } else { "" }
            Write-Host "     - $($i.Item)$n" -ForegroundColor DarkGray
        }
        if (-not $Detalle -and $g.Count -gt 5) { Write-Host "     ... y $($g.Count - 5) mas (usa -Detalle)" -ForegroundColor DarkGray }
    }
}

Write-Host "[SYNC-STATUS] Ultima sincronizacion de este equipo: $ultima" -ForegroundColor Yellow
Write-Host ""
Write-Host $veredicto -ForegroundColor $color
Show-Group "Drive -> este equipo (lo traeria sync-pull):" $toPull
Show-Group "Este equipo -> Drive (lo subiria sync-push):" $toPush
if ($review.Count) {
    Write-Host ""
    Write-Host "Revisar:" -ForegroundColor Cyan
    $review | ForEach-Object { Write-Host "  - $_" -ForegroundColor DarkGray }
}
if ($gitLinea) {
    Write-Host ""
    Write-Host "GitHub (repo antigravity-sync): $gitLinea" -ForegroundColor Cyan
}
exit $code
