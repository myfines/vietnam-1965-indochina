$ErrorActionPreference='Stop'
while ($true) {
 Write-Host 'Vietnam 1965: 1 Mount | 2 Enable | 3 Disable/restore | 4 Unmount | 5 Status | 6 Enable and launch | 0 Exit'
 $choice=(Read-Host 'Select').Trim()
 if ($choice -eq '6') {
  & (Join-Path $PSScriptRoot 'launch.ps1')
  return
 }
 $mode=switch ($choice) { '1' {'Mount'} '2' {'Enable'} '3' {'Disable'} '4' {'Unmount'} '5' {'Status'} '0' {return} default {''} }
 if ($mode) { & (Join-Path $PSScriptRoot 'mount-mod.ps1') -Mode $mode }
 else { Write-Host 'Enter a number from 0 to 6.' }
}
