# Downloads the DS5Dongle BL616 firmware v3.22, extracts it to C:\DS5Dongle and checks SHA256 hashes.
# Baixa o firmware v3.22, extrai em C:\DS5Dongle e confere a integridade (SHA256).
# Uso / Usage:  powershell -ExecutionPolicy Bypass -File docs\baixar-firmware.ps1
& {
  $ErrorActionPreference = 'Stop'
  $ProgressPreference = 'SilentlyContinue'
  [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
  $pasta = 'C:\DS5Dongle'
  $base = 'https://github.com/sqlCRT/ds5dongle-bl618-opensource/releases/download/v3.22'
  $url = "$base/ds5dongle-bl618-lctech616-v3.22.zip"
  $zip = "$pasta\fw-v3.22.zip"
  New-Item -ItemType Directory -Force -Path $pasta | Out-Null
  Invoke-WebRequest -Uri $url -OutFile $zip
  Expand-Archive -Path $zip -DestinationPath $pasta -Force
  $fw = "$pasta\ds5dongle-bl618-lctech616-v3.22"
  $esperado = [ordered]@{
    'ds5dongle-lctech616.bin' = '167e7aecaeeda52656af556485b6eeee4d7d07141cc09754dcf4e82b954655b6'
    'ds5dongle-lctech616-hs.bin' = '4c92de6a9dda8a96714bfc752bd526b9d3b63cd6b1c3d978250d718ce3ec7236'
    'boot2_bl616_isp_release_v8.1.8.bin' = '92a329c660e23f1b488a21779cebb6d5fe0ae61fd25dc00d3df7e4334192ace6'
    'partition.bin' = '99c055a2a7279c04d989a2a270106d2e2584a2d5773b57e40b3af0d87f623d12'
  }
  $ok = $true
  foreach ($nome in $esperado.Keys) {
    $h = (Get-FileHash -Algorithm SHA256 -LiteralPath "$fw\$nome").Hash.ToLower()
    if ($h -eq $esperado[$nome]) {
      Write-Host "OK         $nome" -ForegroundColor Green
    } else {
      Write-Host "DIFERENTE  $nome" -ForegroundColor Red; $ok = $false
    }
  }
  if ($ok) {
    Write-Host "Tudo certo. Arquivos em: $fw" -ForegroundColor Cyan
    Start-Process explorer.exe $fw
  } else {
    Write-Host "Algum arquivo difere do esperado. Nao grave na placa." -ForegroundColor Yellow
  }
}
