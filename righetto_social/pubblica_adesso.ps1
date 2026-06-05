# Pubblica oggi: slot gia passati (o tutto oggi con --forza)
Set-Location $PSScriptRoot
python verifica_meta.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "Prima: .\rinnova_token.ps1"
    exit 1
}
python publish_from_agenda.py --modo manuale --forza
exit $LASTEXITCODE
