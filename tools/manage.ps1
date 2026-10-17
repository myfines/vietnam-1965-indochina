$ErrorActionPreference='Stop'
while ($true) {
 Write-Host 'Vietnam 1965: 1 Mount | 2 Enable | 3 Disable/restore | 4 Unmount | 5 Status | 6 Enable and launch | 0 Exit'
 $choice=Read-Host 'Select'
 if ($choice -eq '6') {
  if (Get-Process hoi4 -ErrorAction SilentlyContinue) { Write-Host 'Save and close the running game first.'; continue }
  & (Join-Path $PSScriptRoot 'mount-mod.ps1') -Mode Enable
  $root=Split-Path $PSScriptRoot -Parent
  $report=Get-Content -LiteralPath (Join-Path $root 'runtime/install-report.json') -Raw | ConvertFrom-Json
  Start-Process -FilePath (Join-Path $report.game 'hoi4.exe') -WorkingDirectory $report.game
  return
 }
 $mode=switch ($choice) { '1' {'Mount'} '2' {'Enable'} '3' {'Disable'} '4' {'Unmount'} '5' {'Status'} '0' {return} default {''} }
 if ($mode) { & (Join-Path $PSScriptRoot 'mount-mod.ps1') -Mode $mode }
}
