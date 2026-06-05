# Esegui UNA VOLTA: tasto destro su PowerShell -> Esegui come amministratore
Set-Location $PSScriptRoot

$taskName = "RighettoSocialPubblica"
$ps1 = Join-Path $PSScriptRoot "pubblica_cron.ps1"

if (-not (Test-Path $ps1)) {
    Write-Error "Manca pubblica_cron.ps1"
    exit 1
}

$tr = "powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$ps1`""

schtasks /Delete /TN $taskName /F 2>$null | Out-Null
schtasks /Create /TN $taskName /TR $tr /SC MINUTE /MO 10 /F | Out-Null

Write-Host "OK: attivita $taskName ogni 10 minuti."
Write-Host ""
Write-Host "Token Meta (circa 60 gg): .\rinnova_token.ps1"
Write-Host "Recupero post saltati:    .\recupera_post.ps1"
Write-Host "Test:                     .\pubblica_cron.ps1"
