[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Genera ~\.agents\skills\skill-catalog: un indice de todas las skills de la biblioteca
# (~\.agents\skill-library), que ningun agente carga de forma automatica.
# La skill-catalog vive en el nucleo, cuesta ~1 KB de presupuesto y le dice al agente
# donde leer cualquier skill que no tenga cargada. Lo llaman sync-pull y sync-push.

$userProfile = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::UserProfile)
$libraryDir  = "$userProfile\.agents\skill-library"
$catalogDir  = "$userProfile\.agents\skills\skill-catalog"

function Get-SkillDescription {
    param([string]$SkillMd)
    $text = Get-Content -LiteralPath $SkillMd -Raw -Encoding UTF8 -ErrorAction SilentlyContinue
    if (-not $text -or $text -notmatch '(?s)^﻿?---\r?\n(.*?)\r?\n---') { return "" }
    $lines = $Matches[1] -split '\r?\n'
    for ($i = 0; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -match '^description:\s*(.*)$') {
            $value = $Matches[1].Trim()
            # Bloques YAML (>-, |, >) o valor en la linea siguiente: juntar las indentadas.
            if ($value -match '^[>|][-+]?$' -or $value -eq '') {
                $parts = @()
                for ($j = $i + 1; $j -lt $lines.Count -and $lines[$j] -match '^\s+\S'; $j++) { $parts += $lines[$j].Trim() }
                $value = $parts -join ' '
            }
            $value = $value.Trim().Trim('"').Trim("'") -replace '\s+', ' '
            if ($value.Length -gt 220) { $value = $value.Substring(0, 217).TrimEnd() + '...' }
            return $value
        }
    }
    return ""
}

function Get-Family {
    param([string]$Name)
    switch -Regex ($Name) {
        '^tooluniverse|^devtu|^create-tooluniverse|^setup-tooluniverse' { return 'ToolUniverse (router en el nucleo: tooluniverse)' }
        '^alphagenome|^albatross'                                       { return 'Genomica y modelos de secuencia (AlphaGenome, Albatross)' }
        '-database$|^literature-search|^ncbi|^embl|^encode|^ucsc|^foldseek|^protein-|^alphafold|^pymol|^predictingthepast|^scienceskillscommon' { return 'Bases de datos, literatura y estructura' }
        '^bigquery|^bigtable|^gcp|^gcs|^google-cloud|^gcloud|^dataform|^dbt|^data-|^schema-|^federate|^discovering-gcp|^developing-with|^building-data|^enforcing|^notebook' { return 'Google Cloud, BigQuery y datos' }
        '^qfdos|^ugr'                                                   { return 'Docencia UGR' }
        default                                                         { return 'Otras' }
    }
}

if (-not (Test-Path $libraryDir)) {
    Write-Host "[CATALOG] No existe $libraryDir; nada que indexar." -ForegroundColor Yellow
    exit 0
}

$entries = foreach ($dir in Get-ChildItem $libraryDir -Directory | Sort-Object Name) {
    $md = Join-Path $dir.FullName 'SKILL.md'
    if (Test-Path $md) {
        [pscustomobject]@{ Name = $dir.Name; Family = Get-Family $dir.Name; Desc = Get-SkillDescription $md }
    }
}

New-Item -ItemType Directory -Force -Path "$catalogDir\references" | Out-Null

$index = New-Object System.Collections.Generic.List[string]
$index.Add("# Indice de la biblioteca de skills")
$index.Add("")
$index.Add("Generado por build-skill-catalog.ps1 el $(Get-Date -Format 'yyyy-MM-dd HH:mm'). $($entries.Count) skills.")
$index.Add("Ruta de cada una: ``%USERPROFILE%\.agents\skill-library\<nombre>\SKILL.md`` (en este equipo: ``$libraryDir``).")
foreach ($group in $entries | Group-Object Family | Sort-Object Name) {
    $index.Add("")
    $index.Add("## $($group.Name)")
    $index.Add("")
    foreach ($e in $group.Group) { $index.Add("- **$($e.Name)**: $($e.Desc)") }
}
Set-Content -LiteralPath "$catalogDir\references\index.md" -Value $index -Encoding utf8

$skill = @"
---
name: skill-catalog
description: Index of $($entries.Count) extra skills kept out of the context budget (ToolUniverse, AlphaGenome, Albatross, biomedical databases, literature search, PDB/UniProt/Ensembl, Google Cloud/BigQuery, UGR teaching). Use whenever a task needs a skill that is not in the loaded list, before saying a capability is missing.
---

# Skill Catalog (biblioteca bajo demanda)

Las skills de la biblioteca no se cargan solas para no superar el presupuesto de
contexto. Siguen disponibles en cualquier carpeta o workspace.

## Procedimiento

1. Lee ``references/index.md`` (junto a este fichero) y localiza la skill por nombre o descripcion.
2. Lee su ``SKILL.md`` en ``%USERPROFILE%\.agents\skill-library\<nombre>\SKILL.md``
   (en este equipo: ``$libraryDir\<nombre>\SKILL.md``).
3. Sigue sus instrucciones como si estuviera cargada. Las rutas relativas que mencione
   (``scripts/``, ``references/``, ``assets/``) cuelgan de esa carpeta.
4. No digas que una capacidad no existe sin haber consultado antes el indice.

Para ToolUniverse, empieza por la skill ``tooluniverse`` del nucleo, que enruta a las
sub-skills de esta biblioteca.

Para cargar un grupo de skills de forma permanente en un workspace local:
``skill-pack enable <pack>`` (ver ``skill-pack.ps1`` en Antigravity-Sync).
"@
Set-Content -LiteralPath "$catalogDir\SKILL.md" -Value $skill -Encoding utf8

Write-Host "[CATALOG] skill-catalog actualizado: $($entries.Count) skills indexadas." -ForegroundColor Green
