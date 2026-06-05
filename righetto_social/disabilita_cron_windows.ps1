# Disabilita pubblicazione automatica ogni 10 min (niente flash PowerShell)
Set-Location $PSScriptRoot
$taskName = "RighettoSocialPubblica"
schtasks /Change /TN $taskName /DISABLE 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Task $taskName non trovato (gia rimosso o mai installato)."
    exit 0
}
Write-Host "OK: $taskName DISABILITATO."
Write-Host "Pubblica tu quando vuoi: .\pubblica_adesso.ps1 oppure .\recupera_post.ps1"
Write-Host "Per riattivare il cron: .\installa_cron_windows.ps1 (come amministratore)"
