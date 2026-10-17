param(
 [ValidateSet('Status','Mount','Enable','Disable','Unmount')][string]$Mode='Status',
 [string]$ModPath='', [string]$GamePath='', [string]$UserDir=''
)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if (!$UserDir) { $UserDir=Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'Paradox Interactive\Hearts of Iron IV' }
if (!$ModPath) {
 $ModPath=Join-Path $root 'theater-mod'
 if (!(Test-Path -LiteralPath (Join-Path $ModPath 'descriptor.mod'))) { $ModPath=Join-Path $root 'runtime\theater-mod' }
}
$ModPath=[IO.Path]::GetFullPath($ModPath)
$modDir=Join-Path $UserDir 'mod'
$entry='mod/vietnam_1965_theater.mod'
$descriptor=Join-Path $modDir 'vietnam_1965_theater.mod'
$loadFile=Join-Path $UserDir 'dlc_load.json'
$backup=Join-Path $root 'runtime\dlc_load.before-enable.json'
function Read-Load {
 if (Test-Path -LiteralPath $loadFile) { return ([IO.File]::ReadAllText($loadFile) | ConvertFrom-Json) }
 return [pscustomobject]@{enabled_mods=@();disabled_dlcs=@()}
}
function Write-Load($load) {
 [IO.Directory]::CreateDirectory($UserDir) | Out-Null
 [IO.File]::WriteAllText($loadFile,($load | ConvertTo-Json -Depth 10),[Text.UTF8Encoding]::new($false))
}
function Disable-Local {
 $load=Read-Load; $enabled=@($load.enabled_mods)
 if ($enabled.Count -eq 1 -and $enabled[0] -eq $entry -and (Test-Path -LiteralPath $backup)) {
  $saved=[IO.File]::ReadAllText($backup) | ConvertFrom-Json
  $load.enabled_mods=@($saved.enabled_mods)
 } else { $load.enabled_mods=@($enabled | Where-Object { $_ -ne $entry }) }
 Write-Load $load
}
if ($Mode -eq 'Status') {
 $load=Read-Load
 [pscustomobject]@{Mounted=(Test-Path -LiteralPath $descriptor);Enabled=(@($load.enabled_mods) -contains $entry);ModPath=$ModPath;Descriptor=$descriptor}
 exit 0
}
if ($Mode -in @('Mount','Enable')) {
 if (!(Test-Path -LiteralPath (Join-Path $ModPath 'descriptor.mod'))) {
  $installer=Join-Path $PSScriptRoot 'install.py'
  if (!(Test-Path -LiteralPath $installer)) { throw 'Mod files missing.' }
  $installArgs=@($installer)
  if ($GamePath) { $installArgs+=@('--game',$GamePath) }
  & python @installArgs
  if ($LASTEXITCODE -ne 0) { throw 'Local installation failed.' }
 }
 $source=Join-Path $ModPath 'descriptor.mod'
 if (!(Test-Path -LiteralPath $source)) { throw "Missing descriptor: $source" }
 [IO.Directory]::CreateDirectory($modDir) | Out-Null
 $text=[IO.File]::ReadAllText($source)
 $text=[regex]::Replace($text,'(?m)^\s*path\s*=.*\r?\n?','')
 $text += [Environment]::NewLine + 'path="' + $ModPath.Replace('\','/') + '"' + [Environment]::NewLine
 [IO.File]::WriteAllText($descriptor,$text,[Text.UTF8Encoding]::new($false))
 $legacy=Join-Path $modDir 'vietnam_1965_local.mod'
 if (Test-Path -LiteralPath $legacy) { [IO.File]::WriteAllText($legacy,$text,[Text.UTF8Encoding]::new($false)) }
}
if ($Mode -eq 'Enable') {
 $load=Read-Load
 if (@($load.enabled_mods) -notcontains $entry) {
  [IO.Directory]::CreateDirectory((Split-Path $backup -Parent)) | Out-Null
  [IO.File]::WriteAllText($backup,($load | ConvertTo-Json -Depth 10),[Text.UTF8Encoding]::new($false))
 }
 $load.enabled_mods=@($entry)
 Write-Load $load
}
if ($Mode -in @('Disable','Unmount')) { Disable-Local }
if ($Mode -eq 'Unmount') {
 foreach ($name in @('vietnam_1965_theater.mod','vietnam_1965_local.mod')) {
  $p=Join-Path $modDir $name
  if (Test-Path -LiteralPath $p) { Remove-Item -LiteralPath $p }
 }
}
Write-Output "$Mode complete. Mod: $ModPath"
