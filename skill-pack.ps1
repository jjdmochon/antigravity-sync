<#
  skill-pack: carga de forma permanente un grupo de skills de la biblioteca en un workspace.

    skill-pack list                         packs disponibles y cuantas skills tiene cada uno
    skill-pack status  [-Workspace <ruta>]  packs activos en el workspace
    skill-pack enable  <pack> [-Workspace <ruta>] [-Force]
    skill-pack disable <pack> [-Workspace <ruta>]

  Crea junctions (no copias) en <workspace>\.agents\skills\<skill> (Antigravity/Gemini) y
  <workspace>\.claude\skills\<skill> (Claude Code) que apuntan a ~\.agents\skill-library.
  Una sola copia real: editar la skill desde el workspace edita la biblioteca.

  No hace falta activar un pack para usar sus skills: skill-catalog las hace accesibles
  desde cualquier carpeta. Un pack solo sirve para que esten cargadas sin pedirlas.
  Cada pack suma su descripcion al presupuesto de contexto de ese workspace.
#>
param(
    [Parameter(Position = 0)][ValidateSet("list", "status", "enable", "disable")][string]$Action = "list",
    [Parameter(Position = 1)][string]$Pack,
    [string]$Workspace = (Get-Location).Path,
    [switch]$Force
)
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$userProfile = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::UserProfile)
$libraryDir  = "$userProfile\.agents\skill-library"
$packsFile   = Join-Path $PSScriptRoot "skill-packs.json"

if (-not (Test-Path $packsFile))  { Write-Host "No encuentro $packsFile" -ForegroundColor Red; exit 1 }
if (-not (Test-Path $libraryDir)) { Write-Host "No existe $libraryDir. Ejecuta sync-pull." -ForegroundColor Red; exit 1 }

$packs = Get-Content $packsFile -Raw -Encoding UTF8 | ConvertFrom-Json
$packNames = $packs.PSObject.Properties.Name | Where-Object { $_ -notlike "_*" }
$library = (Get-ChildItem $libraryDir -Directory).Name

function Get-PackSkills([string]$Name) {
    $patterns = $packs.$Name
    $library | Where-Object { $skill = $_; $patterns | Where-Object { $skill -match $_ } }
}

$targets = @("$Workspace\.agents\skills", "$Workspace\.claude\skills")

switch ($Action) {
    "list" {
        foreach ($p in $packNames) { "{0,-18} {1,3} skills" -f $p, @(Get-PackSkills $p).Count }
    }
    "status" {
        foreach ($p in $packNames) {
            $skills = @(Get-PackSkills $p)
            $linked = @($skills | Where-Object { (Get-Item "$($targets[0])\$_" -Force -ErrorAction SilentlyContinue).LinkType -eq "Junction" })
            if ($linked.Count) { "{0,-18} {1}/{2} activas" -f $p, $linked.Count, $skills.Count }
        }
    }
    "enable" {
        if ($Pack -notin $packNames) { Write-Host "Pack desconocido. Disponibles: $($packNames -join ', ')" -ForegroundColor Red; exit 1 }
        # Un junction dentro de Google Drive apunta a una ruta local (C:\Users\<usuario>) que
        # no existe igual en el otro equipo, y Drive puede intentar subir su contenido.
        $resolved = (Resolve-Path $Workspace).Path
        $root = [System.IO.Path]::GetPathRoot($resolved)
        $isDrive = ($resolved -match '\\Mi unidad\\|\\My Drive\\|\\Google Drive\\') -or
                   ((Get-PSDrive ($root.Substring(0,1)) -ErrorAction SilentlyContinue).Description -match 'Google')
        if ($isDrive -and -not $Force) {
            Write-Host "[!] $resolved esta en Google Drive. No creo junctions ahi (romperian el otro equipo)." -ForegroundColor Yellow
            Write-Host "    En workspaces de Drive usa skill-catalog (no necesita nada) o -Force si sabes lo que haces." -ForegroundColor Yellow
            exit 1
        }
        $n = 0
        foreach ($skill in Get-PackSkills $Pack) {
            foreach ($t in $targets) {
                if (-not (Test-Path $t)) { New-Item -ItemType Directory -Force -Path $t | Out-Null }
                $link = "$t\$skill"
                if (Test-Path $link) { continue }
                cmd /c mklink /J "$link" "$libraryDir\$skill" | Out-Null
                $n++
            }
        }
        Write-Host "[skill-pack] '$Pack' activado en $Workspace ($n junctions nuevos)." -ForegroundColor Green
    }
    "disable" {
        if ($Pack -notin $packNames) { Write-Host "Pack desconocido. Disponibles: $($packNames -join ', ')" -ForegroundColor Red; exit 1 }
        $n = 0
        foreach ($skill in Get-PackSkills $Pack) {
            foreach ($t in $targets) {
                $item = Get-Item "$t\$skill" -Force -ErrorAction SilentlyContinue
                # Solo se quitan junctions: borrar el enlace no toca la biblioteca.
                if ($item -and $item.LinkType -eq "Junction") { [System.IO.Directory]::Delete($item.FullName); $n++ }
            }
        }
        Write-Host "[skill-pack] '$Pack' desactivado en $Workspace ($n junctions quitados)." -ForegroundColor Green
    }
}
