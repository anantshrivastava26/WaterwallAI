# PowerShell bootstrap for WaterwallAI dev env
$ErrorActionPreference = "Stop"

if (-not (Test-Path ".venv")) {
    python -m venv .venv
}
. .\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt

if (-not (Test-Path ".env")) {
    Copy-Item .env.example .env
    Write-Host "Created .env from .env.example — edit as needed."
}

New-Item -ItemType Directory -Force -Path data | Out-Null

Write-Host "Setup complete. Activate with: . .\.venv\Scripts\Activate.ps1"
