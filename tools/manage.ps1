$ErrorActionPreference='Stop'
while ($true) {
 Write-Host 'Vietnam 1965: 1 Mount | 2 Enable (only this mod) | 3 Disable/restore | 4 Unmount | 5 Status | 0 Exit'
 $choice=Read-Host 'Select'
 $mode=switch ($choice) { '1' {'Mount'} '2' {'Enable'} '3' {'Disable'} '4' {'Unmount'} '5' {'Status'} '0' {return} default {''} }
 if ($mode) { & (Join-Path $PSScriptRoot 'mount-mod.ps1') -Mode $mode }
}
