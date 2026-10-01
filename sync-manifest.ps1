# Registro de la ultima sincronizacion (lo cargan sync-pull.ps1 y sync-push.ps1).
#
# sync-push sube nucleo y biblioteca con /MIR, que borra en Drive lo que este equipo no tiene.
# Eso es correcto si lo borraste aqui, pero no si lo subio el otro equipo y aun no hiciste
# sync-pull. Para distinguirlo, cada sincronizacion guarda en ~\.agents\sync-manifest.txt la
# lista de ficheros de Drive que este equipo conoce. sync-push solo deja borrar en Drive lo que
# esta en esa lista. No se usan fechas de fichero: robocopy conserva la original al copiar y una
# skill descomprimida de un zip llega con fechas antiguas.

function Get-SyncTreeFiles {
    # Rutas relativas (<Prefix>\...) de los ficheros bajo $Root, con las exclusiones de robocopy.
    param([string]$Root, [string]$Prefix, [string[]]$SkipTopDirs = @(), [string[]]$SkipRelDirs = @(),
          [string[]]$ExcludeDirs = @(), [string[]]$ExcludeFiles = @())
    $out = New-Object System.Collections.Generic.List[string]
    if (-not (Test-Path -LiteralPath $Root)) { return ,$out }
    $stack = New-Object System.Collections.Generic.Stack[string]
    $stack.Push("")
    while ($stack.Count -gt 0) {
        $rel  = $stack.Pop()
        $full = if ($rel) { Join-Path $Root $rel } else { $Root }
        foreach ($item in Get-ChildItem -LiteralPath $full -Force -ErrorAction SilentlyContinue) {
            $itemRel = if ($rel) { Join-Path $rel $item.Name } else { $item.Name }
            if ($item.PSIsContainer) {
                if (-not $rel -and $item.Name -in $SkipTopDirs) { continue }
                if ($itemRel -in $SkipRelDirs) { continue }
                if (@($ExcludeDirs | Where-Object { $item.Name -like $_ }).Count -gt 0) { continue }
                $stack.Push($itemRel)
            } elseif (@($ExcludeFiles | Where-Object { $item.Name -like $_ }).Count -eq 0) {
                $out.Add((Join-Path $Prefix $itemRel))
            }
        }
    }
    return ,$out
}

function Get-SyncedFiles {
    # Ficheros de nucleo (agents_skills\...) y biblioteca (skill_library\...) bajo dos raices,
    # con las mismas exclusiones que usa sync-push al subirlos.
    param([string]$CoreRoot, [string]$LibraryRoot, [string[]]$LocalOnlyCore, [string[]]$ExcludeDirs, [string[]]$ExcludeFiles)
    $core = Get-SyncTreeFiles -Root $CoreRoot -Prefix "agents_skills" -SkipTopDirs $LocalOnlyCore `
                -ExcludeDirs $ExcludeDirs -ExcludeFiles $ExcludeFiles
    $lib  = Get-SyncTreeFiles -Root $LibraryRoot -Prefix "skill_library" `
                -SkipRelDirs @("tooluniverse-antibody-engineering\ClaudeScientificSkills") `
                -ExcludeDirs $ExcludeDirs -ExcludeFiles $ExcludeFiles
    $all = New-Object System.Collections.Generic.List[string]
    $all.AddRange($core); $all.AddRange($lib)
    return ,$all
}

function Save-SyncManifest {
    param([string]$Path, [string[]]$Entries, [string]$Origin)
    $header = "# Ficheros de Drive (nucleo y biblioteca) conocidos por este equipo tras $Origin " +
              "el $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss'). Lo generan sync-pull y sync-push; no editar."
    $parent = Split-Path $Path -Parent
    if (-not (Test-Path -LiteralPath $parent)) { New-Item -ItemType Directory -Force -Path $parent | Out-Null }
    Set-Content -LiteralPath $Path -Value (@($header) + @($Entries | Sort-Object -Unique)) -Encoding UTF8
}

function Read-SyncManifest {
    # Devuelve un HashSet (sin distinguir mayusculas) o $null si este equipo nunca sincronizo.
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) { return $null }
    $set = New-Object 'System.Collections.Generic.HashSet[string]' ([System.StringComparer]::OrdinalIgnoreCase)
    foreach ($line in Get-Content -LiteralPath $Path -Encoding UTF8) {
        if ($line -and -not $line.StartsWith("#")) { [void]$set.Add($line) }
    }
    return ,$set
}

function Get-UnknownPurges {
    # Lo que /MIR borraria en Drive (esta en Drive y no aqui) y que este equipo no conocia en su
    # ultima sincronizacion: llego del otro equipo despues.
    param([string[]]$DriveFiles, [string[]]$LocalFiles, $Known)
    $local = New-Object 'System.Collections.Generic.HashSet[string]' ([System.StringComparer]::OrdinalIgnoreCase)
    foreach ($f in $LocalFiles) { [void]$local.Add($f) }
    @($DriveFiles | Where-Object { -not $local.Contains($_) -and -not $Known.Contains($_) })
}
