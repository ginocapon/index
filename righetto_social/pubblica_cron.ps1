# Pubblica da agenda (come cron_pubblica.bat) — chiamato dal Task Scheduler
Set-Location $PSScriptRoot
$ErrorActionPreference = "Continue"

python verifica_meta.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "STOP: token Meta non valido. Esegui: .\rinnova_token.ps1"
    exit 1
}

python publish_from_agenda.py --modo cron
exit $LASTEXITCODE
