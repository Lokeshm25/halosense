$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$python = Join-Path $repoRoot "backend/.venv/Scripts/python.exe"

if (-not (Test-Path $python)) {
    throw "Backend virtual environment not found at backend/.venv. See docs/SETUP.md."
}

Push-Location $repoRoot
try {
    Write-Host "[1/4] Backend tests"
    & $python -m pytest backend/tests -q
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    Write-Host "[2/4] Backend lint"
    & $python -m ruff check backend
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    Write-Host "[3/4] Frontend lint"
    & npm --prefix frontend run lint
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    Write-Host "[4/4] Frontend production build"
    & npm --prefix frontend run build
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
finally {
    Pop-Location
}

Write-Host "Phase 0 verification passed."