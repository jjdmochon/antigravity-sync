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
$manifestPath    = "$userProfile\.agents\sync-manifest.txt"  # lo que este equipo conoce de Drive (ver sync-manifest.ps1)
. "$driveSyncDir\sync-manifest.ps1"

$excludeDirs  = @(".venv", "venv", ".git", "__pycache__", ".pytest_cache", "node_modules", ".ruff_cache", "*.bak*")
$excludeFiles = @("desktop.ini", "*.pyc", "*.pyo", "Thumbs.db", ".DS_Store", "*.bak*")
# Carpetas del nucleo que no viajan: synced lo escribe la app de Claude en cada equipo y
# skill-catalog se regenera aqui mismo a partir de la biblioteca local.
$localOnlyCore = @("synced", "skill-catalog")
# Datos propios de cada equipo dentro de config (los mismos que excluye .gitignore): rutas
# absolutas de workspaces y estado local. No se traen de Drive: llevan la letra de unidad del
# otro equipo (I: alli, K: aqui) y romperian los workspaces de este.
$localOnlyConfigDirs  = @("projects", "sidecars")
$localOnlyConfigFiles = @(".migrated")
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"

function Backup-LocalCopy {
    # Aparta la copia local como <nombre>.bak-<fecha> antes de que Drive la sustituya.
    param([string]$Path)
    $backup = "$Path.bak-$stamp"
    Copy-Item -LiteralPath $Path -Destination $backup -Force
    Write-Host "  [!] Drive sustituye $Path. La version local queda en $(Split-Path $backup -Leaf)." -ForegroundColor Yellow
}

function Copy-FromDrive {
    <#
      Copia un fichero de Drive sin pisar cambios locales. Si la copia local es distinta y mas
      reciente (cambios aun sin sync-push), no se toca; si Drive es mas reciente, la local se
      aparta como .bak-<fecha> antes de sustituirla. Antes se copiaba siempre con -Force.
    #>
    param([string]$Source, [string]$Dest)
    if (Test-Path -LiteralPath $Dest) {
        if ((Get-FileHash -LiteralPath $Source).Hash -eq (Get-FileHash -LiteralPath $Dest).Hash) { return }
        if ((Get-Item -LiteralPath $Dest).LastWriteTimeUtc -gt (Get-Item -LiteralPath $Source).LastWriteTimeUtc) {
            Write-Host "  [!] $Dest es mas reciente que el de Drive: no se toca. Si es el bueno, haz sync-push." -ForegroundColor Yellow
            return
        }
        Backup-LocalCopy $Dest
    }
    Copy-Item -LiteralPath $Source -Destination $Dest -Force
}

function Sync-FromDrive {
    <#
      Trae una carpeta de Drive sin purga y con /XO: no borra lo que solo exista en este equipo ni
      pisa ficheros locales mas recientes. Lo usan config y claude_agents. Antes ambas iban con /MIR,
      que devolvia config.json a la version de Drive aunque la local fuera de hoy y borraba los
      subagentes que solo existian en este equipo.
    #>
    param([string]$Source, [string]$Dest, [string[]]$ExcludeDirs, [string[]]$ExcludeFiles)
    if (-not (Test-Path -LiteralPath $Dest)) { New-Item -ItemType Directory -Force -Path $Dest | Out-Null }
    $cfgArgs = @($Source, $Dest, "/E", "/XO", "/XD") + $ExcludeDirs + @("/XF") + $ExcludeFiles + @("/R:1", "/W:1")
    # Pasada en seco (/L) para apartar antes las copias locales que Drive va a sustituir.
    # /NC /NS dejan solo la ruta completa: no depende del idioma de robocopy.
    $incoming = robocopy @cfgArgs /L /NJH /NJS /NDL /NC /NS /FP /NP | ForEach-Object { $_.Trim() } |
                Where-Object { $_.StartsWith($Source, [System.StringComparison]::OrdinalIgnoreCase) }
    foreach ($src in $incoming) {
        $local = Join-Path $Dest $src.Substring($Source.Length).TrimStart([char]92)
        if ((Test-Path -LiteralPath $local) -and
            (Get-FileHash -LiteralPath $src).Hash -ne (Get-FileHash -LiteralPath $local).Hash) {
            Backup-LocalCopy $local
        }
    }
    robocopy @cfgArgs /NP /NFL /NDL | Out-Null
}

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
if (Test-Path "$driveSyncDir\GEMINI.md") { Copy-FromDrive "$driveSyncDir\GEMINI.md" (Join-Path $geminiDir "GEMINI.md") }
if (Test-Path "$driveSyncDir\CLAUDE.md") { Copy-FromDrive "$driveSyncDir\CLAUDE.md" (Join-Path $claudeDir "CLAUDE.md") }
# Catalogos fechados (GLOBAL_AGENTS_AND_TOOLS_<fecha>.md, SUBAGENTS_TEMPLATES_<fecha>.md).
# Las versiones antiguas se archivan en archive\ y en ~\.gemini\archive\.
foreach ($pattern in @("GLOBAL_AGENTS_AND_TOOLS_*.md", "SUBAGENTS_TEMPLATES_*.md", "CHEMBIO_MEDCHEM_TOOLKIT_*.md")) {
    Get-ChildItem "$driveSyncDir" -File -Filter $pattern | ForEach-Object { Copy-FromDrive $_.FullName (Join-Path $geminiDir $_.Name) }
}

# 2. Config (sin tocar skills, que es junction; ni projects\ ni sidecars\, que son de cada equipo)
$xd = @(); foreach ($d in $excludeDirs)  { $xd += $d }
$xf = @(); foreach ($f in $excludeFiles) { $xf += $f }
if (Test-Path "$driveSyncDir\config") {
    Sync-FromDrive -Source "$driveSyncDir\config" -Dest $configDir `
        -ExcludeDirs (@("skills") + $localOnlyConfigDirs + $xd) -ExcludeFiles ($xf + $localOnlyConfigFiles)
}

# 3. Junctions ANTES de espejar, para que .claude\skills y .gemini\config\skills nunca
#    queden como copias reales divergentes.
foreach ($dir in @($agentsSkillsDir, $libraryDir, $archiveDir)) {
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
}
Ensure-SkillsJunction -Link $claudeSkillsDir -Target $agentsSkillsDir
Ensure-SkillsJunction -Link $geminiSkillsDir -Target $agentsSkillsDir

# Foto de nucleo y biblioteca en Drive ANTES de copiar: lo que llegue durante el pull no cuenta
# como conocido y sync-push no podra borrarlo hasta el siguiente sync-pull.
$driveSnapshot = Get-SyncedFiles -CoreRoot "$driveSyncDir\agents_skills" -LibraryRoot "$driveSyncDir\skill_library" `
                     -LocalOnlyCore $localOnlyCore -ExcludeDirs $excludeDirs -ExcludeFiles $excludeFiles

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

# 6. Nucleo. Sin /MIR: /MIR borraba ficheros nuevos de este equipo aun sin sync-push (asi se
#    perdio jev-system-one\mcp\ el 2026-10-02). Ahora se copia sin purga y con /XO, y solo se
#    borra en local lo que el registro dice que ya estaba en Drive y Drive ya no tiene, es decir,
#    lo que el otro equipo borro. Lo nuevo de aqui (fuera del registro) se conserva.
$knownBefore = Read-SyncManifest -Path $manifestPath
if (Test-Path "$driveSyncDir\agents_skills") {
    robocopy "$driveSyncDir\agents_skills" "$agentsSkillsDir" /E /XO /XD @xd @localOnlyCore /XF @xf /NP /NFL /NDL /R:1 /W:1 | Out-Null
    if ($null -ne $knownBefore) {
        $driveSet = New-Object 'System.Collections.Generic.HashSet[string]' ([System.StringComparer]::OrdinalIgnoreCase)
        foreach ($e in $driveSnapshot) { [void]$driveSet.Add($e) }
        $localCore = Get-SyncTreeFiles -Root $agentsSkillsDir -Prefix "agents_skills" -SkipTopDirs $localOnlyCore `
                         -ExcludeDirs $excludeDirs -ExcludeFiles $excludeFiles
        foreach ($rel in $localCore) {
            if ($knownBefore.Contains($rel) -and -not $driveSet.Contains($rel)) {
                $full = Join-Path $agentsSkillsDir ($rel.Substring("agents_skills\".Length))
                Remove-Item -LiteralPath $full -Force -ErrorAction SilentlyContinue
                Write-Host "  [-] Borrado en el otro equipo: $rel" -ForegroundColor Yellow
            }
        }
    } else {
        Write-Host "  [!] Sin registro previo: no se propagan borrados del nucleo en este pull." -ForegroundColor Yellow
    }
    $nuevos = @(Get-SyncTreeFiles -Root $agentsSkillsDir -Prefix "agents_skills" -SkipTopDirs $localOnlyCore `
                    -ExcludeDirs $excludeDirs -ExcludeFiles $excludeFiles | Where-Object { $driveSnapshot -notcontains $_ })
    if ($nuevos.Count -gt 0) {
        Write-Host "  [i] $($nuevos.Count) fichero(s) del nucleo solo en este equipo (se conservan; sync-push los subira)." -ForegroundColor Cyan
    }
}
Save-SyncManifest -Path $manifestPath -Entries $driveSnapshot -Origin "sync-pull"

# 7. Catalogo de la biblioteca (rutas de este equipo).
& "$driveSyncDir\build-skill-catalog.ps1"

# 8. Agentes: sin purga, asi que un subagente que solo exista en este equipo se conserva.
#    Para retirar uno, borralo en los dos equipos (sync-push lo quita de Drive).
if (Test-Path "$driveSyncDir\claude_agents") {
    Sync-FromDrive -Source "$driveSyncDir\claude_agents" -Dest $claudeAgentsDir -ExcludeDirs $xd -ExcludeFiles $xf
}

# 9. Claude Code: MCP de ambito usuario. Idempotente: solo añade los que falten.
if (Get-Command claude -ErrorAction SilentlyContinue) {
    $mcps = [ordered]@{
        "gemini-api-docs" = @("--transport", "http", "gemini-api-docs", "https://gemini-api-docs-mcp.dev")
        "chrome-devtools" = @("chrome-devtools", "--", "npx", "-y", "chrome-devtools-mcp@latest")
        # tooluniverse se quito el 2026-10-01: expone cientos de herramientas y su contenido ya
        # llega por la skill router `tooluniverse` y las sub-skills de la biblioteca.
    }
    foreach ($name in $mcps.Keys) {
        claude mcp get $name *> $null
        if ($LASTEXITCODE -ne 0) {
            # Splatting real (@mcpArgs), no @(...): si claude es el shim claude.ps1 de npm,
            # @(...) le llega como un unico argumento y el add falla con "unknown option".
            $mcpArgs = $mcps[$name]
            $out = claude mcp add --scope user @mcpArgs 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Host "  [+] MCP '$name' registrado en Claude Code." -ForegroundColor Green
            } else {
                Write-Host "  [!] No se pudo registrar el MCP '$name': $($out | Select-Object -Last 1)" -ForegroundColor Yellow
            }
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

# 11b. onetake (biblioteca) renderiza con Playwright + Chromium desde Python. Solo aviso: es opcional.
if (Test-Path "$libraryDir\onetake") {
    py -3.13 -c "import playwright, numpy, scipy, PIL, matplotlib" *> $null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [+] onetake: Python 3.13 con playwright, numpy, scipy, Pillow y matplotlib." -ForegroundColor Green
    } else {
        Write-Host "  [!] onetake necesita: py -3.13 -m pip install --user playwright numpy scipy pillow matplotlib fonttools brotli; py -3.13 -m playwright install chromium" -ForegroundColor Yellow
    }
}

# 12. Claves de API: ~\.env frente a la plantilla .env.example. Solo nombres, nunca valores.
$envTemplate = "$driveSyncDir\.env.example"
$envLocal    = "$userProfile\.env"
if (Test-Path $envTemplate) {
    $wanted = @(Get-Content $envTemplate | Where-Object { $_ -match '^\s*([A-Z0-9_]+)\s*=' } | ForEach-Object { $Matches[1] })
    $have = @{}
    if (Test-Path $envLocal) {
        foreach ($l in Get-Content $envLocal) {
            if ($l -match '^\s*([A-Z0-9_]+)\s*=\s*(.*)$') { $have[$Matches[1]] = $Matches[2].Trim().Trim('"').Trim("'") }
        }
    }
    $faltan = @($wanted | Where-Object { -not $have[$_] })
    if (-not (Test-Path $envLocal)) {
        Write-Host "  [!] No existe $envLocal. Copia la plantilla y rellenala:" -ForegroundColor Yellow
        Write-Host "      Copy-Item '$envTemplate' '$envLocal'" -ForegroundColor Yellow
    } elseif ($faltan.Count -gt 0) {
        Write-Host "  [!] Faltan o estan vacias en ~\.env: $($faltan -join ', ') (ver .env.example)." -ForegroundColor Yellow
    } else {
        Write-Host "  [+] ~\.env tiene las $($wanted.Count) claves de la plantilla." -ForegroundColor Green
    }
}

# 13. Python 3.13 con las dependencias de Jev (las skills llaman a `py -3.13`).
#     `mcp` (>=2) lo necesita el servidor MCP de Jev para la app de escritorio (paso 14).
py -3.13 -c "import typesafe_sdk, dotenv, docx, fitz, mcp.server.mcpserver" *> $null
if ($LASTEXITCODE -eq 0) {
    Write-Host "  [+] Python 3.13 con typesafe-sdk, python-dotenv, python-docx, pymupdf y mcp." -ForegroundColor Green
} else {
    py -3.13 -c "pass" *> $null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  [!] Falta Python 3.13: winget install --id Python.Python.3.13 -e --scope user" -ForegroundColor Yellow
    }
    Write-Host "  [!] Dependencias de Jev: py -3.13 -m pip install --user typesafe-sdk==0.7.1 python-dotenv python-docx pymupdf ""mcp>=2""" -ForegroundColor Yellow
}

# 14. App de escritorio de Claude: registra el MCP local de Jev (jev_gate_text, jev_gate_file,
#     jev_route) para que la app pueda ejecutar las etapas 0 y 4 del pipeline. Solo anade la
#     entrada "jev" si falta o apunta a otra ruta; el resto del fichero no se toca. Copia previa
#     en claude_desktop_config.json.bak-<fecha>. Reiniciar la app para que lo cargue.
$desktopCfg = "$env:APPDATA\Claude\claude_desktop_config.json"
$jevServer  = "$agentsSkillsDir\jev-system-one\mcp\jev_mcp_server.py"
$pyLauncher = (Get-Command py -ErrorAction SilentlyContinue).Source
# Con la app abierta, esta reescribe el fichero desde memoria y borra la entrada en segundos.
$desktopAbierta = @(Get-Process -Name claude -ErrorAction SilentlyContinue |
    Where-Object { $_.Path -match '\\WindowsApps\\Claude_|\\AnthropicClaude\\|\\Programs\\Claude\\' }).Count -gt 0
$cfgActual = if (Test-Path $desktopCfg) { (Get-Content $desktopCfg -Raw -Encoding UTF8 | ConvertFrom-Json).mcpServers.jev } else { $null }
if ($desktopAbierta -and (Test-Path $desktopCfg) -and -not $cfgActual) {
    Write-Host "  [!] La app de escritorio de Claude esta abierta: cierrala del todo (icono de la bandeja -> Quit)" -ForegroundColor Yellow
    Write-Host "      y repite sync-pull para registrar el MCP 'jev'. Abierta, la app deshace el cambio." -ForegroundColor Yellow
} elseif ((Test-Path $desktopCfg) -and (Test-Path $jevServer) -and $pyLauncher) {
    try {
        $cfg = Get-Content $desktopCfg -Raw -Encoding UTF8 | ConvertFrom-Json
        if (-not $cfg.mcpServers) { $cfg | Add-Member -NotePropertyName mcpServers -NotePropertyValue ([pscustomobject]@{}) }
        $actual = $cfg.mcpServers.jev
        if (-not $actual -or ($actual.args -join '|') -ne ("-3.13|$jevServer")) {
            Copy-Item $desktopCfg "$desktopCfg.bak-$(Get-Date -Format 'yyyyMMdd-HHmmss')" -Force
            $cfg.mcpServers | Add-Member -NotePropertyName jev -Force -NotePropertyValue ([pscustomobject]@{
                command = $pyLauncher; args = @("-3.13", $jevServer) })
            [IO.File]::WriteAllText($desktopCfg, ($cfg | ConvertTo-Json -Depth 20), (New-Object Text.UTF8Encoding $false))
            Write-Host "  [+] MCP 'jev' registrado en la app de escritorio de Claude (reiniciala)." -ForegroundColor Green
        }
    } catch {
        Write-Host "  [!] No se pudo registrar Jev en la app de escritorio: $($_.Exception.Message)" -ForegroundColor Yellow
    }
}

$nCore = (Get-ChildItem $agentsSkillsDir -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -ne "synced" }).Count
$nLib  = (Get-ChildItem $libraryDir -Directory -ErrorAction SilentlyContinue).Count
Write-Host "[SYNC-PULL] Completado: $nCore skills en el nucleo y $nLib en la biblioteca (via skill-catalog)." -ForegroundColor Green
