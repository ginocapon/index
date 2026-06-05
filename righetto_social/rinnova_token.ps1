# Dopo aver incollato il token Explorer in .env → converti in token PAGINA
Set-Location $PSScriptRoot

Write-Host "1/2 Token utente -> token PAGINA..."
python estrai_token_pagina.py --scrivi-env
if ($LASTEXITCODE -ne 0) { exit 1 }

Write-Host ""
Write-Host "2/2 Verifica..."
python verifica_meta.py
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERRORE: deve comparire 'Token tipo: PAGE'"
    exit 1
}

Write-Host ""
Write-Host "OK. Token pronto per ~60 giorni."
