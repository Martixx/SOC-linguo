$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$source = Join-Path $root "baterias_normalized"
$normal = Join-Path $root "batteries\normal"
$natural = Join-Path $root "batteries\natural-english"

if (-not (Test-Path $source)) {
    throw "No se encuentra la carpeta: $source"
}

New-Item -ItemType Directory -Force $normal, $natural | Out-Null
Remove-Item (Join-Path $normal "*.json") -Force -ErrorAction SilentlyContinue
Remove-Item (Join-Path $natural "*.json") -Force -ErrorAction SilentlyContinue

$results = foreach ($file in Get-ChildItem $source -Filter *.json) {
    try {
        $data = Get-Content $file.FullName -Raw -Encoding UTF8 | ConvertFrom-Json
        if (-not $data.name -or -not $data.category -or -not $data.questions) {
            throw "Faltan name, category o questions"
        }

        switch ($data.category) {
            "normal"  { Copy-Item $file.FullName $normal -Force }
            "natural" { Copy-Item $file.FullName $natural -Force }
            default   { throw "Categoría desconocida: $($data.category)" }
        }

        [PSCustomObject]@{
            File = $file.Name
            Category = $data.category
            Questions = $data.questions.Count
            Status = "OK"
        }
    }
    catch {
        [PSCustomObject]@{
            File = $file.Name
            Category = ""
            Questions = 0
            Status = "ERROR: $($_.Exception.Message)"
        }
    }
}

$errors = $results | Where-Object { $_.Status -ne "OK" }
if ($errors) {
    $errors | Format-Table -AutoSize
    throw "Se encontraron JSON no válidos. No publiques el repositorio todavía."
}

$summary = $results | Group-Object Category | ForEach-Object {
    [PSCustomObject]@{
        Category = $_.Name
        Batteries = $_.Count
        Questions = ($_.Group | Measure-Object Questions -Sum).Sum
    }
}

$summary | Format-Table -AutoSize
$totalBatteries = $results.Count
$totalQuestions = ($results | Measure-Object Questions -Sum).Sum

if ($totalBatteries -ne 32 -or $totalQuestions -ne 1810) {
    throw "Recuento inesperado: $totalBatteries baterías y $totalQuestions preguntas. Esperado: 32 y 1810."
}

$normalCount = (Get-ChildItem $normal -Filter *.json).Count
$naturalCount = (Get-ChildItem $natural -Filter *.json).Count
if ($normalCount -ne 24 -or $naturalCount -ne 8) {
    throw "Distribución inesperada: $normalCount Normal y $naturalCount Natural English. Esperado: 24 y 8."
}

Write-Host "Proyecto preparado correctamente: 32 baterías, 1810 preguntas, 24 Normal y 8 Natural English." -ForegroundColor Green
