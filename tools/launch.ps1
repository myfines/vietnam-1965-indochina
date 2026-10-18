param([switch]$CheckOnly)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$reportPath=Join-Path $root 'runtime/install-report.json'
if (!(Test-Path -LiteralPath $reportPath)) {
 if ($CheckOnly) { throw 'Run tools/install.py first.' }
 & python (Join-Path $PSScriptRoot 'install.py')
 if ($LASTEXITCODE -ne 0) { throw 'Installation failed. See README.md.' }
}
$report=Get-Content -LiteralPath $reportPath -Raw | ConvertFrom-Json
$exe=Join-Path $report.game 'hoi4.exe'
$descriptor=Join-Path $report.runtime 'descriptor.mod'
if (!(Test-Path -LiteralPath $exe)) { throw "Game executable missing: $exe" }
if (!(Test-Path -LiteralPath $descriptor)) { throw "Mod descriptor missing: $descriptor" }
if ($CheckOnly) { Write-Output 'Launch paths checked: PASS'; return }
if (Get-Process hoi4 -ErrorAction SilentlyContinue) { throw 'Save and close the running HOI4 game, then try again.' }
& (Join-Path $PSScriptRoot 'mount-mod.ps1') -Mode Enable
Write-Host 'Starting Vietnam 1965. Choose NEW GAME; the theater mod is enabled.'
$started=Get-Date
$process=Start-Process -FilePath $exe -WorkingDirectory $report.game -PassThru
$log=Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'Paradox Interactive\Hearts of Iron IV\logs\game.log'
$deadline=$started.AddSeconds(90)
while ((Get-Date) -lt $deadline) {
 Start-Sleep -Seconds 2
 if ($process.HasExited) { throw 'Game exited before loading the Vietnam theater.' }
 if ((Test-Path -LiteralPath $log) -and (Get-Item -LiteralPath $log).LastWriteTime -ge $started) {
  try {
   $stream=[IO.File]::Open($log,[IO.FileMode]::Open,[IO.FileAccess]::Read,[IO.FileShare]::ReadWrite)
   $reader=[IO.StreamReader]::new($stream)
   try { $content=$reader.ReadToEnd() } finally { $reader.Dispose() }
  } catch [IO.IOException] { continue }
  if ($content -match 'Loaded 1576 provinces\.' -and $content -match '\[1965\.10\.28\.12\]') {
   Write-Host 'VERIFIED: Vietnam map loaded, start date 1965-10-28. Choose NEW GAME.'
   return
  }
  if ($content -match 'Loaded 13414 provinces\.') { throw 'Vanilla loaded instead of Vietnam. See runtime registration and game logs.' }
 }
}
throw 'Loading could not be verified within 90 seconds. Check the game logs.'
