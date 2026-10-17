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
Start-Process -FilePath $exe -WorkingDirectory $report.game
