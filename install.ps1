[CmdletBinding()]
param(
 [ValidateSet('all','astra','sol')][string]$Character='all',
 [ValidateSet(32,48,64)][int]$Size=48,
 [switch]$Apply,[switch]$Restore,[switch]$VerifyOnly
)
$ErrorActionPreference='Stop'
$packageRoot=$PSScriptRoot
$manifest=Get-Content -LiteralPath (Join-Path $packageRoot 'source\cursor_manifest.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$roles=@('Arrow','Help','AppStarting','Wait','Crosshair','IBeam','NWPen','No','SizeNS','SizeWE','SizeNWSE','SizeNESW','SizeAll','UpArrow','Hand','Pin','Person')
$characters=@($manifest | Select-Object -ExpandProperty character -Unique)
foreach($entry in $manifest){
 $file=Join-Path $packageRoot $entry.file
 if(-not(Test-Path -LiteralPath $file -PathType Leaf)){throw "Missing cursor: $file"}
}
if($Apply -and $Restore){throw 'Choose Apply or Restore.'}
if($Apply -and $Character -eq 'all'){throw 'Use -Character astra or sol with -Apply.'}
if($Character -ne 'all' -and $Character -notin $characters){throw "This package does not contain $Character."}
if($VerifyOnly){Write-Output "Verified $($manifest.Count) cursor files. No installation changes.";return}
$destination=Join-Path $env:LOCALAPPDATA 'AstraSolMintCursors\1.0.0'
$cursorKey='HKCU:\Control Panel\Cursors'
if(-not ('MintCursorNative' -as [type])){
 Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public static class MintCursorNative {
 [DllImport("user32.dll", SetLastError=true)]
 public static extern bool SystemParametersInfo(uint action,uint parameter,IntPtr value,uint flags);
}
'@
}
if($Restore){
 $backups=Get-ChildItem -LiteralPath (Join-Path $destination 'backup') -Filter '*.json' | Sort-Object Name -Descending
 if(-not $backups){throw 'No saved cursor settings found.'}
 $saved=Get-Content -LiteralPath $backups[0].FullName -Raw -Encoding UTF8 | ConvertFrom-Json
 $reg=[Microsoft.Win32.Registry]::CurrentUser.OpenSubKey('Control Panel\Cursors',$true)
 try{
  foreach($entry in $saved){
   if($entry.exists){$kind=[System.Enum]::Parse([Microsoft.Win32.RegistryValueKind],$entry.kind);$reg.SetValue($entry.name,$entry.value,$kind)}
   else{$reg.DeleteValue($entry.name,$false)}
  }
 }finally{$reg.Close()}
 if(-not[MintCursorNative]::SystemParametersInfo(0x57,0,[IntPtr]::Zero,3)){throw 'Windows cursor refresh failed.'}
 Write-Output "Restored settings saved in $($backups[0].Name)";return
}
[void](New-Item -ItemType Directory -Path $destination -Force)
foreach($entry in $manifest){
 $target=Join-Path $destination $entry.file
 [void](New-Item -ItemType Directory -Path (Split-Path -Parent $target) -Force)
 Copy-Item -LiteralPath (Join-Path $packageRoot $entry.file) -Destination $target -Force
 if((Get-FileHash -LiteralPath $target).Hash -ne (Get-FileHash -LiteralPath (Join-Path $packageRoot $entry.file)).Hash){throw "Copy mismatch: $target"}
}
$schemeKey=Join-Path $cursorKey 'Schemes'
if(-not(Test-Path -LiteralPath $schemeKey)){[void](New-Item -Path $schemeKey)}
foreach($c in $characters){foreach($pixels in @(32,48,64)){
 $entries=@($manifest | Where-Object { $_.character -eq $c -and $_.size -eq $pixels })
 if($entries.Count -ne 17){throw "Incomplete scheme: $c $pixels"}
 $paths=foreach($role in $roles){$e=$entries | Where-Object role -eq $role;Join-Path $destination $e.file}
 $display=if($c -eq 'astra'){'Astra'}else{'sol'}
 [void](New-ItemProperty -Path $schemeKey -Name "$display Mint $($pixels)px" -Value ($paths -join ',') -PropertyType String -Force)
}}
if($Apply){
 $reg=[Microsoft.Win32.Registry]::CurrentUser.OpenSubKey('Control Panel\Cursors',$true)
 try{
  $saved=foreach($name in @('')+$roles+@('Scheme Source')){
   $exists=$name -in $reg.GetValueNames()
   [pscustomobject]@{name=$name;exists=$exists;value=if($exists){$reg.GetValue($name,$null,[Microsoft.Win32.RegistryValueOptions]::DoNotExpandEnvironmentNames)}else{$null};kind=if($exists){$reg.GetValueKind($name).ToString()}else{$null}}
  }
  $backupDir=Join-Path $destination 'backup';[void](New-Item -ItemType Directory -Path $backupDir -Force)
  $backup=Join-Path $backupDir ((Get-Date -Format 'yyyyMMdd-HHmmss-ffff')+'.json')
  [IO.File]::WriteAllText($backup,($saved | ConvertTo-Json -Depth 5),[Text.UTF8Encoding]::new($false))
  foreach($role in $roles){
   $e=$manifest | Where-Object { $_.character -eq $Character -and $_.size -eq $Size -and $_.role -eq $role }
   $reg.SetValue($role,(Join-Path $destination $e.file),[Microsoft.Win32.RegistryValueKind]::String)
  }
  $display=if($Character -eq 'astra'){'Astra'}else{'sol'}
  $reg.SetValue('',"$display Mint $($Size)px",[Microsoft.Win32.RegistryValueKind]::String)
  $reg.SetValue('Scheme Source',1,[Microsoft.Win32.RegistryValueKind]::DWord)
 }finally{$reg.Close()}
 if(-not[MintCursorNative]::SystemParametersInfo(0x57,0,[IntPtr]::Zero,3)){throw "Windows refresh failed. Backup: $backup"}
 Write-Output "Applied $Character $Size px. Previous settings: $backup"
}else{Write-Output 'Installed cursor schemes. Open Control Panel > Mouse > Pointers to choose a Mint scheme.'}
