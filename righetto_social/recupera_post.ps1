# Pubblica subito tutto cio che e in agenda oggi (recupero se PC spento)
Set-Location $PSScriptRoot

python verifica_meta.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "Prima: .\rinnova_token.ps1"
    exit 1
}

Write-Host "Pubblicazione forzata agenda di oggi..."
python publish_from_agenda.py --modo manuale --forza
exit $LASTEXITCODE
